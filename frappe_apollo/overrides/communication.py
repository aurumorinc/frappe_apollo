import frappe
from frappe import _
from frappe_controller.utils.background_jobs import enqueue

def update_contact(communication_name):
	"""
	FS Job: Injects generated subject/body into Apollo custom fields.
	"""
	from frappe_apollo.integrations.apollo import ApolloClient
	from frappe_controller.utils.controller import emit_event, wait_for_event
	
	comm = frappe.get_doc("Communication", communication_name)
	if comm.get("apollo_sync_status") == "Synced":
		return

	mcc = frappe.get_doc("Multi Channel Campaign", comm.reference_name)
	
	# Check Provider Status
	settings = frappe.get_doc("Apollo Settings")
	if not settings.enable:
		wait_for_event(
			event_key="doc:Apollo Settings:on_update",
			condition="argument.get('enable') == 1"
		)

	# Find Sequence
	# We need to know which Account this MCC is routed through.
	# MCC -> sender -> User Mailbox -> Mailbox -> Account
	mailbox_id = frappe.db.get_value("User Mailbox", {"parent": mcc.sender}, "mailbox")
	if not mailbox_id:
		wait_for_event(
			event_key="doc:User Mailbox:after_insert",
			condition=f"argument.get('parent') == '{mcc.sender}'"
		)
		
	mailbox = frappe.get_doc("Mailbox", mailbox_id)
	account_name = mailbox.account
	
	sequence = frappe.get_all("Sequence", filters={
		"campaign": mcc.campaign_name,
		"account": account_name
	}, limit=1)
	
	if not sequence:
		wait_for_event(
			event_key="doc:Sequence:after_insert",
			condition=f"argument.get('campaign') == '{mcc.campaign_name}' and argument.get('account') == '{account_name}'"
		)
		
	seq_doc = frappe.get_doc("Sequence", sequence[0].name)
	
	# Find People
	people_id = frappe.db.get_value("People", {"lead": mcc.recipient, "account": account_name}, "id")
	if not people_id:
		wait_for_event(
			event_key="doc:People:after_insert",
			condition=f"argument.get('lead') == '{mcc.recipient}' and argument.get('account') == '{account_name}'"
		)
		
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
	
	if not step.subject_custom_field_id or not step.response_custom_field_id:
		return

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
