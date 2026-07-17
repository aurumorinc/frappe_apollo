import frappe
from frappe_controller.utils.controller import wait_for_event

def on_update(doc, method=None):
	if doc.get_doc_before_save() and doc.get_doc_before_save().status != "Scheduled" and doc.status == "Scheduled":
		frappe.enqueue(
			method="frappe_apollo.apollo.doctype.communication.communication.update_a_contact",
			queue="medium",
			comm_name=doc.name
		)

def update_a_contact(comm_name):
	from frappe_apollo.integrations.apollo import ApolloClient
	from frappe_controller.utils.controller import SuspendJob
	
	comm = frappe.get_doc("Communication", comm_name)
	
	if comm.get("apollo_sync_status") == "Synced":
		return
		
	mcc = frappe.get_doc("Multi Channel Cadence", comm.reference_name)
	
	# Fetch the Email Account via native User Email
	email_account_name = frappe.db.get_value("User Email", {"parent": mcc.sender}, "email_account")
	if not email_account_name:
		wait_for_event(
			event_key="doc:User Email:after_insert",
			condition=f"argument.get('parent') == '{mcc.sender}'"
		)
	email_account = frappe.get_doc("Email Account", email_account_name)
	
	if not email_account.get("apollo_ids"):
		raise Exception("No Apollo Account mapped to this Email Account.")
	
	account_name = email_account.apollo_ids[0].account
	apollo_id = email_account.apollo_ids[0].apollo_id
	
	is_enabled = frappe.db.get_value("Cadence Provider", "Apollo", "enabled")
	if not is_enabled:
		wait_for_event(
			event_key="doc:Cadence Provider:on_update:Apollo",
			condition="argument.get('enabled') == 1"
		)
		
	account = frappe.get_doc("Account", account_name)
	if account.status != "Active":
		wait_for_event(
			event_key="doc:Account:on_update",
			condition=f"argument.get('name') == '{account_name}' and argument.get('status') == 'Active'"
		)
		
	crm_lead_accounts = frappe.get_all("CRM Lead Apollo ID", filters={"parent": mcc.recipient, "account": account_name}, fields=["apollo_id"])
	if not crm_lead_accounts or not crm_lead_accounts[0].get("apollo_id"):
		wait_for_event(
			event_key=f"doc:CRM Lead:on_update:{mcc.recipient}",
			condition=f"any(row.get('account') == '{account_name}' and row.get('apollo_id') for row in argument.get('apollo_ids', []))"
		)
		# fetch again after event
		crm_lead_accounts = frappe.get_all("CRM Lead Apollo ID", filters={"parent": mcc.recipient, "account": account_name}, fields=["apollo_id"])
		
	contact_apollo_id = crm_lead_accounts[0].apollo_id
		
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
	
	step_idx = 1
	if comm.cadence_schedule:
		cadence = frappe.get_doc("Cadence", mcc.cadence_name)
		for idx, sch in enumerate(cadence.cadence_schedules):
			if sch.name == comm.cadence_schedule:
				step_idx = idx + 1
				break
				
	if step_idx > len(seq_doc.sequence_steps):
		wait_for_event(
			event_key="doc:Sequence:on_update",
			condition=f"argument.get('name') == '{seq_doc.name}'"
		)
		
	step = seq_doc.sequence_steps[step_idx - 1]
	
	if not step.subject_custom_field_id or not step.response_custom_field_id:
		wait_for_event(
			event_key="doc:Sequence:on_update",
			condition=f"argument.get('name') == '{seq_doc.name}'" # will loop back
		)
		
	# Wait for actual Field docs to have apollo_id
	subject_field = frappe.get_doc("Field", step.subject_custom_field_id)
	if not subject_field.apollo_id:
		wait_for_event(
			event_key="doc:Field:on_update",
			condition=f"argument.get('name') == '{subject_field.name}' and argument.get('apollo_id')"
		)
		
	response_field = frappe.get_doc("Field", step.response_custom_field_id)
	if not response_field.apollo_id:
		wait_for_event(
			event_key="doc:Field:on_update",
			condition=f"argument.get('name') == '{response_field.name}' and argument.get('apollo_id')"
		)
		
	custom_fields = {
		subject_field.apollo_id: comm.subject,
		response_field.apollo_id: comm.content
	}
	
	client = ApolloClient(account_name)
	try:
		client.update_contact(contact_apollo_id, custom_fields)
		comm.db_set("apollo_id", contact_apollo_id)
		comm.db_set("apollo_sync_status", "Synced")
	except Exception as e:
		frappe.log_error(title="Failed to sync Communication to Apollo", message=str(e))
		raise
