import frappe
from frappe.model.document import Document
from frappe_controller.utils.background_jobs import enqueue

class Sequence(Document):
	def on_update(self):
		self._populate_sequence_steps()
		self._enqueue_provision_custom_fields()
		self._enqueue_pending_jobs()

	def _populate_sequence_steps(self):
		"""
		Ensures the number of Sequence Step rows matches the number of Email schedules in the Campaign.
		"""
		if not self.campaign:
			return
			
		campaign = frappe.get_doc("Campaign", self.campaign)
		# Filter schedules to only include those where reference_doctype == "Email Template"
		email_schedules = [s for s in (campaign.get("campaign_schedules") or []) if s.reference_doctype == "Email Template"]
		
		current_steps = self.get("sequence_steps") or []
		if len(current_steps) < len(email_schedules):
			for i in range(len(current_steps), len(email_schedules)):
				self.append("sequence_steps", {})
			self.save()

	def _enqueue_provision_custom_fields(self):
		"""
		Enqueues jobs to provision custom fields in Apollo for each sequence step if missing.
		"""
		for idx, step in enumerate(self.sequence_steps, 1):
			if not step.subject_custom_field_id:
				enqueue(
					method="frappe_apollo.apollo.doctype.sequence.sequence.provision_custom_field",
					queue="low",
					sequence_name=self.name,
					step_idx=idx,
					field_type="subject"
				)
				
			if not step.response_custom_field_id:
				enqueue(
					method="frappe_apollo.apollo.doctype.sequence.sequence.provision_custom_field",
					queue="low",
					sequence_name=self.name,
					step_idx=idx,
					field_type="response"
				)

	def _enqueue_pending_jobs(self):
		# Finds all pending Multi Channel Campaigns and enqueues create_contact_add_to_sequence
		mccs = frappe.get_all("Multi Channel Campaign", filters={
			"campaign_name": self.campaign,
			"status": ["in", ["Draft", "In Progress"]]
		})
		for mcc in mccs:
			enqueue(
				method="frappe_apollo.apollo.doctype.sequence.sequence.create_contact_add_to_sequence",
				queue="low",
				campaign_name=mcc.name
			)
			
		# Finds all pending Communication records and enqueues update_contact
		comms = frappe.get_all("Communication", filters={
			"reference_doctype": "Multi Channel Campaign",
			"delivery_status": "Scheduled",
			"apollo_sync_status": ["!=", "Synced"]
		})
		for comm in comms:
			enqueue(
				method="frappe_apollo.overrides.communication.update_contact",
				queue="low",
				communication_name=comm.name
			)

def provision_custom_field(sequence_name, step_idx, field_type):
	"""
	FS Job: Provisions a single custom field in Apollo.
	"""
	from frappe_apollo.integrations.apollo import ApolloClient
	
	sequence = frappe.get_doc("Sequence", sequence_name)
	step = sequence.sequence_steps[step_idx - 1]
	
	client = ApolloClient(sequence.account)
	
	if field_type == "subject":
		label = f"Seq {sequence.id} Step {step_idx} Subject"
		apollo_type = "string"
	else:
		label = f"Seq {sequence.id} Step {step_idx} Body"
		apollo_type = "textarea"
		
	# Check if Field record already exists in Frappe
	existing_field = frappe.db.get_value("Field", {"account": sequence.account, "label": label}, "id")
	field_id = existing_field
	
	if not field_id:
		try:
			res = client.create_custom_field(label, apollo_type)
			fields = res.get("typed_custom_fields", [])
			if fields:
				field_id = fields[0].get("id")
				frappe.get_doc({
					"doctype": "Field",
					"account": sequence.account,
					"label": label,
					"id": field_id
				}).insert()
		except Exception as e:
			frappe.log_error(f"Failed to create custom field {label} in Apollo", "Apollo Integration")
			raise e
			
	if field_id:
		if field_type == "subject":
			step.db_set("subject_custom_field_id", field_id)
		else:
			step.db_set("response_custom_field_id", field_id)
			
	return field_id

def on_mcc_after_insert(doc, method=None):
	enqueue(
		method="frappe_apollo.apollo.doctype.sequence.sequence.create_contact_add_to_sequence",
		queue="low",
		campaign_name=doc.name
	)

def create_contact_add_to_sequence(campaign_name):
	"""
	FS Job Workflow: Syncs lead to Apollo and adds to sequence.
	"""
	# 1. Sync Lead to Apollo
	people_id = enqueue(
		method="frappe_apollo.apollo.doctype.sequence.sequence.create_contact",
		queue="low",
		campaign_name=campaign_name
	).result()
	
	if not people_id:
		return
		
	# 2. Add Contact to Sequence
	enqueue(
		method="frappe_apollo.apollo.doctype.sequence.sequence.add_contact_to_sequence",
		queue="low",
		campaign_name=campaign_name,
		people_id=people_id
	).result()

def create_contact(campaign_name):
	"""
	FS Job: Syncs lead to Apollo.
	"""
	from frappe_apollo.integrations.apollo import ApolloClient
	
	mcc = frappe.get_doc("Multi Channel Campaign", campaign_name)
	lead = frappe.get_doc("CRM Lead", mcc.recipient)
	sender = mcc.sender
	
	# Find Mailbox
	mailbox_id = frappe.db.get_value("User Mailbox", {"parent": sender}, "mailbox")
	if not mailbox_id:
		frappe.throw(f"No Apollo Mailbox assigned to user {sender}")
		
	mailbox = frappe.get_doc("Mailbox", mailbox_id)
	account_name = mailbox.account
	
	client = ApolloClient(account_name)
	
	# Lead Syncing
	people_id = frappe.db.get_value("People", {"lead": lead.name, "account": account_name}, "id")
	if not people_id:
		lead_data = {
			"first_name": lead.first_name,
			"last_name": lead.last_name,
			"email": lead.email,
			"organization_name": lead.organization
		}
		people_id = client.create_contact(lead_data)
		frappe.get_doc({
			"doctype": "People",
			"lead": lead.name,
			"account": account_name,
			"id": people_id
		}).insert()
		
	return people_id

def add_contact_to_sequence(campaign_name, people_id):
	"""
	FS Job: Adds contact to sequence.
	"""
	from frappe_apollo.integrations.apollo import ApolloClient
	
	mcc = frappe.get_doc("Multi Channel Campaign", campaign_name)
	sender = mcc.sender
	
	# Find Mailbox
	mailbox_id = frappe.db.get_value("User Mailbox", {"parent": sender}, "mailbox")
	if not mailbox_id:
		frappe.throw(f"No Apollo Mailbox assigned to user {sender}")
		
	mailbox = frappe.get_doc("Mailbox", mailbox_id)
	account_name = mailbox.account
	
	# Find Sequence
	sequence = frappe.get_all("Sequence", filters={
		"campaign": mcc.campaign_name,
		"account": account_name
	}, fields=["id"], limit=1)
	
	if not sequence:
		# Eventual Consistency: Raise exception to trigger retry
		raise frappe.ValidationError(f"No Apollo Sequence found for Campaign {mcc.campaign_name} and Account {account_name}")
		
	sequence_id = sequence[0].id
	
	# Safeguard: Wait for Step 1 Communication to be scheduled
	# This is a conceptual wait_for_event, in FS jobs it might be implemented differently
	# For now, we check if Step 1 communication exists and is synced
	step1_comm = frappe.get_all("Communication", filters={
		"reference_doctype": "Multi Channel Campaign",
		"reference_name": campaign_name,
		"delivery_status": "Scheduled"
		# Add logic to identify Step 1 if needed
	}, limit=1)
	
	if not step1_comm:
		# Gracefully abort and wait for Step 1 to be generated
		return

	# Sequence Assignment
	client = ApolloClient(account_name)
	client.add_contacts_to_sequence(people_id, sequence_id, mailbox.id)

def on_campaign_update(doc, method=None):
	"""
	Hook handler for Campaign on_update.
	"""
	sequences = frappe.get_all("Sequence", filters={"campaign": doc.name})
	for seq in sequences:
		seq_doc = frappe.get_doc("Sequence", seq.name)
		seq_doc.save()

