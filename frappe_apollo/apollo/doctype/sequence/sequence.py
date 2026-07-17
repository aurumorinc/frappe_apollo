import frappe
from frappe.model.document import Document

class Sequence(Document):
	def before_save(self):
		self._populate_sequence_steps()

	def on_update(self):
		self._enqueue_provision_fields()
		
	def after_save(self):
		frappe.enqueue(
			"frappe_apollo.apollo.doctype.sequence.sequence.get_sequence_status",
			queue="short",
			sequence_name=self.name
		)

	def _populate_sequence_steps(self):
		if not self.cadence:
			return
			
		cadence = frappe.get_doc("Cadence", self.cadence)
		email_schedules = [s for s in (cadence.get("cadence_schedules") or []) if s.reference_doctype == "Email Template"]
		
		current_steps = self.get("sequence_steps") or []
		if len(current_steps) < len(email_schedules):
			for i in range(len(current_steps), len(email_schedules)):
				self.append("sequence_steps", {})

	def _enqueue_provision_fields(self):
		for idx, step in enumerate(self.sequence_steps, 1):
			if not step.subject_custom_field_id:
				frappe.enqueue(
					method="frappe_apollo.apollo.doctype.field.field.provision_a_field",
					queue="low",
					sequence_name=self.name,
					step_idx=idx,
					field_type="subject"
				)
				
			if not step.response_custom_field_id:
				frappe.enqueue(
					method="frappe_apollo.apollo.doctype.field.field.provision_a_field",
					queue="low",
					sequence_name=self.name,
					step_idx=idx,
					field_type="response"
				)

def get_sequence_status(sequence_name):
	from frappe_apollo.integrations.apollo import ApolloClient
	from frappe_controller.utils.controller import SuspendJob

	is_enabled = frappe.db.get_value("Cadence Provider", "Apollo", "enabled")
	if not is_enabled:
		raise SuspendJob("Apollo Cadence Provider is disabled.")

	sequence = frappe.get_doc("Sequence", sequence_name)
	account = frappe.get_doc("Account", sequence.account)
	if account.status != "Active":
		raise SuspendJob("Apollo Account is not Active.")
		
	if not sequence.apollo_id:
		return
		
	client = ApolloClient(sequence.account)
	try:
		res = client.search_sequences(q_name=sequence.apollo_id)
		campaigns = res.get("emailer_campaigns", [])
		found = any(str(c.get("id")) == str(sequence.apollo_id) for c in campaigns)
		if not found:
			sequence.db_set("status", "Inactive")
	except Exception as e:
		frappe.log_error(title="Failed to sync Sequence status", message=str(e))
		raise

def get_all_sequence_status():
	sequences = frappe.get_all("Sequence", filters={"status": "Active"}, pluck="name")
	for seq_name in sequences:
		frappe.enqueue(
			"frappe_apollo.apollo.doctype.sequence.sequence.get_sequence_status",
			queue="short",
			sequence_name=seq_name
		)

def _assign_contact_to_sequence(mcc_name):
	from frappe_apollo.integrations.apollo import ApolloClient
	from frappe_controller.utils.controller import wait_for_event
	
	mcc = frappe.get_doc("Multi Channel Cadence", mcc_name)
	sender = mcc.sender
	
	email_account_name = frappe.db.get_value("User Email", {"parent": sender}, "email_account")
	if not email_account_name:
		wait_for_event(
			event_key="doc:User Email:after_insert",
			condition=f"argument.get('parent') == '{sender}'"
		)
		
	email_account = frappe.get_doc("Email Account", email_account_name)
	if not email_account.get("apollo_ids"):
		raise Exception("No Apollo Account mapped to this Email Account.")
	
	account_name = email_account.apollo_ids[0].account
	apollo_mailbox_id = email_account.apollo_ids[0].apollo_id
	
	crm_lead_accounts = frappe.get_all("CRM Lead Apollo ID", filters={"parent": mcc.recipient, "account": account_name}, fields=["apollo_id"])
	if not crm_lead_accounts or not crm_lead_accounts[0].get("apollo_id"):
		wait_for_event(
			event_key=f"doc:CRM Lead:on_update:{mcc.recipient}",
			condition=f"any(row.get('account') == '{account_name}' and row.get('apollo_id') for row in argument.get('apollo_ids', []))"
		)
		# refetch
		crm_lead_accounts = frappe.get_all("CRM Lead Apollo ID", filters={"parent": mcc.recipient, "account": account_name}, fields=["apollo_id"])

	contact_apollo_id = crm_lead_accounts[0].apollo_id

	# Sequence wait for 'Active' status
	sequence = frappe.get_all("Sequence", filters={
		"cadence": mcc.cadence_name,
		"account": account_name
	}, limit=1)
	
	if not sequence:
		wait_for_event(
			event_key="doc:Sequence:after_insert",
			condition=f"argument.get('cadence') == '{mcc.cadence_name}' and argument.get('account') == '{account_name}'"
		)
		
	seq_doc = frappe.get_doc("Sequence", sequence[0].get("name"))
	if seq_doc.status != "Active" or not seq_doc.apollo_id:
		wait_for_event(
			event_key="doc:Sequence:on_update",
			condition=f"argument.get('name') == '{seq_doc.name}' and argument.get('status') == 'Active' and argument.get('apollo_id')"
		)
		
	# Call API
	client = ApolloClient(account_name)
	try:
		client.add_contacts_to_sequence(contact_apollo_id, seq_doc.apollo_id, apollo_mailbox_id)
	except Exception as e:
		frappe.log_error(title="Failed to assign sequence in Apollo", message=str(e))
		raise

def on_cadence_update(cadence_name):
	try:
		sequences = frappe.get_all("Sequence", filters={"cadence": cadence_name}, pluck="name")
		for seq_name in sequences:
			sequence = frappe.get_doc("Sequence", seq_name)
			sequence.save(ignore_permissions=True)
	except Exception as e:
		frappe.log_error(title="Failed to update Apollo Sequences for Cadence", message=str(e))
