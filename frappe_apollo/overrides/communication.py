import frappe
from frappe import _
from frappe_controller.utils.background_jobs import enqueue

def on_update(doc, method=None):
	"""
	Hook handler for Communication on_update.
	"""
	if not frappe.db.get_single_value("Apollo Settings", "enable"):
		return
		
	if doc.reference_doctype == "Multi Channel Campaign" and doc.delivery_status == "Scheduled" and doc.apollo_sync_status != "Synced":
		enqueue(
			method="frappe_apollo.overrides.communication.update_contact",
			queue="low",
			communication_name=doc.name
		)

def update_contact(communication_name):
	"""
	FS Job: Injects generated subject/body into Apollo custom fields.
	"""
	from frappe_apollo.integrations.apollo import ApolloClient
	from frappe_controller.utils.controller import emit_event
	
	comm = frappe.get_doc("Communication", communication_name)
	mcc = frappe.get_doc("Multi Channel Campaign", comm.reference_name)
	
	# Find Sequence
	# We need to know which Account this MCC is routed through.
	# MCC -> sender -> User Mailbox -> Mailbox -> Account
	mailbox_id = frappe.db.get_value("User Mailbox", {"parent": mcc.sender}, "mailbox")
	if not mailbox_id:
		return
		
	mailbox = frappe.get_doc("Mailbox", mailbox_id)
	account_name = mailbox.account
	
	sequence = frappe.get_all("Sequence", filters={
		"campaign": mcc.campaign_name,
		"account": account_name
	}, limit=1)
	
	if not sequence:
		raise frappe.ValidationError(f"No Apollo Sequence found for Campaign {mcc.campaign_name} and Account {account_name}")
		
	seq_doc = frappe.get_doc("Sequence", sequence[0].name)
	
	# Find People
	people_id = frappe.db.get_value("People", {"lead": mcc.recipient, "account": account_name}, "id")
	if not people_id:
		raise frappe.ValidationError(f"No Apollo Contact found for Lead {mcc.recipient} and Account {account_name}")
		
	# Payload Validation
	if not comm.content or not comm.subject:
		return
		
	# Identify Step Index
	# This depends on how frappe_campaign tracks steps. 
	# Assuming MCC has a field 'step_idx' or we can derive it.
	# For now, we'll try to find the matching step in Sequence.
	step_idx = mcc.get("step_idx", 1) # Default to 1
	if step_idx > len(seq_doc.sequence_steps):
		return
		
	step = seq_doc.sequence_steps[step_idx - 1]
	
	custom_fields = {
		step.subject_custom_field_id: comm.subject,
		step.response_custom_field_id: comm.content
	}
	
	client = ApolloClient(account_name)
	client.update_contact(people_id, custom_fields)
	
	# State Machine
	if step_idx == 1:
		emit_event("communication_scheduled", {
			"campaign_name": mcc.campaign_name,
			"step_idx": 1,
			"mcc": mcc.name
		})
		
	comm.apollo_sync_status = "Synced"
	comm.save(ignore_permissions=True)
