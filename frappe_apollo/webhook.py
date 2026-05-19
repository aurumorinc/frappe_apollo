import frappe
from frappe import _
from frappe_controller.utils.background_jobs import enqueue

@frappe.whitelist(allow_guest=True)
def handle():
	"""
	Public endpoint for Apollo webhooks.
	"""
	token = frappe.get_request_header("Authorization")
	if not token or not token.startswith("Bearer "):
		frappe.throw(_("Unauthorized"), frappe.AuthenticationError)
		
	bearer_token = token.split(" ")[1]
	
	# Verify token against active Accounts
	accounts = frappe.get_all("Account", fields=["name", "webhook_bearer_token"])
	authorized = False
	for acc in accounts:
		if acc.webhook_bearer_token and frappe.get_doc("Account", acc.name).get_password("webhook_bearer_token") == bearer_token:
			authorized = True
			break
			
	if not authorized:
		frappe.throw(_("Unauthorized"), frappe.AuthenticationError)
		
	payload = frappe.request.get_json()
	
	# Enqueue FS Job
	enqueue(
		method="frappe_apollo.webhook.process_webhook",
		queue="low",
		payload=payload
	)
	
	return {"status": "ok"}

def process_webhook(payload):
	"""
	FS Job: Handles Apollo webhook data asynchronously.
	"""
	event = payload.get("event")
	
	if event == "message_sent":
		_handle_message_sent(payload)
	elif event == "message_replied":
		_handle_message_replied(payload)

def _handle_message_sent(payload):
	# Find Communication
	# Apollo payload might contain contact_id, emailer_campaign_id, etc.
	# We need to map this back to our Communication record.
	# This might require storing Apollo's message ID or similar in Communication.
	# For now, follow blueprint: "Finds the Communication, marks it as Sent, and emits campaign_step_completed"
	contact_id = payload.get("contact_id")
	sequence_id = payload.get("emailer_campaign_id")
	
	# Find People record to get Lead
	people = frappe.get_all("People", filters={"id": contact_id}, fields=["lead", "account"])
	if not people:
		return
		
	lead_name = people[0].lead
	account_name = people[0].account
	
	# Find Sequence to get Campaign
	sequence = frappe.get_all("Sequence", filters={"id": sequence_id, "account": account_name}, fields=["campaign"])
	if not sequence:
		return
		
	campaign_name = sequence[0].campaign
	
	# Find the Scheduled Communication for this Lead and Campaign
	comms = frappe.get_all("Communication", filters={
		"reference_doctype": "Multi Channel Campaign",
		"delivery_status": "Scheduled",
		"sender": ["!=", ""], # Add more filters to be specific
	}, fields=["name"])
	
	for comm_info in comms:
		comm = frappe.get_doc("Communication", comm_info.name)
		# Verify it belongs to the right MCC
		mcc = frappe.get_doc("Multi Channel Campaign", comm.reference_name)
		if mcc.recipient == lead_name and mcc.campaign_name == campaign_name:
			comm.delivery_status = "Sent"
			comm.save(ignore_permissions=True)
			
			# Emit event to trigger next step generation in frappe_campaign
			from frappe_controller.utils.controller import emit_event
			emit_event("campaign_step_completed", {
				"campaign_name": campaign_name,
				"lead": lead_name,
				"mcc": mcc.name
			})
			break

def _handle_message_replied(payload):
	contact_id = payload.get("contact_id")
	sequence_id = payload.get("emailer_campaign_id")
	
	people = frappe.get_all("People", filters={"id": contact_id}, fields=["lead", "account"])
	if not people:
		return
		
	lead_name = people[0].lead
	account_name = people[0].account
	
	sequence = frappe.get_all("Sequence", filters={"id": sequence_id, "account": account_name}, fields=["campaign", "name"])
	if not sequence:
		return
		
	campaign_name = sequence[0].campaign
	
	# Mark campaign as Completed
	mccs = frappe.get_all("Multi Channel Campaign", filters={
		"recipient": lead_name,
		"campaign_name": campaign_name
	})
	for mcc in mccs:
		doc = frappe.get_doc("Multi Channel Campaign", mcc.name)
		doc.status = "Completed"
		doc.save(ignore_permissions=True)
		
	# Create inbound Communication
	frappe.get_doc({
		"doctype": "Communication",
		"communication_type": "Communication",
		"communication_medium": "Email",
		"sent_or_received": "Received",
		"subject": payload.get("subject", "Reply from Apollo"),
		"content": payload.get("body", ""),
		"sender": payload.get("email"),
		"reference_doctype": "Multi Channel Campaign",
		"reference_name": mccs[0].name if mccs else None
	}).insert(ignore_permissions=True)
	
