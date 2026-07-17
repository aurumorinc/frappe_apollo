import frappe
from frappe import _

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
	frappe.enqueue(
		method="frappe_apollo.webhook.process_webhook",
		queue="low",
		payload=payload
	)
	
	return {"status": "ok"}

def process_webhook(payload):
	"""
	FS Job: Handles Apollo webhook data asynchronously.
	"""
	from frappe_apollo.apollo.doctype.cadence_provider.cadence_provider import ApolloCadenceProvider

	event = payload.get("event")
	contact_id = payload.get("contact_id")
	sequence_id = payload.get("emailer_campaign_id")
	
	if not contact_id or not sequence_id:
		return
		
	people = frappe.get_all("People", filters={"id": contact_id}, fields=["lead", "account"])
	if not people:
		frappe.log_error("people not found")
		return
		
	lead_name = people[0].lead
	account_name = people[0].account
	
	sequence = frappe.get_all("Sequence", filters={"id": sequence_id, "account": account_name}, fields=["campaign"])
	if not sequence:
		frappe.log_error("sequence not found")
		return
		
	cadence_name = sequence[0].campaign
	
	mccs = frappe.get_all("Multi Channel Cadence", filters={
		"recipient": lead_name,
		"cadence_name": cadence_name
	}, fields=["name"], order_by="creation desc", limit=1)
	
	if not mccs:
		frappe.log_error("mccs not found")
		return
		
	mcc_name = mccs[0].name
	
	context = {"mcc_name": mcc_name}
	
	if event == "message_sent":
		comms = frappe.get_all("Communication", filters={
			"reference_doctype": "Multi Channel Cadence",
			"reference_name": mcc_name,
			"delivery_status": "Scheduled"
		}, fields=["name"], order_by="creation desc", limit=1)
		
		if comms:
			context["communication_name"] = comms[0].name
			ApolloCadenceProvider.report_event("message_sent", context, payload)
		else:
			frappe.log_error("comms not found")
	elif event == "message_replied":
		ApolloCadenceProvider.report_event("message_replied", context, payload)
		
	elif event == "message_opened":
		comms = frappe.get_all("Communication", filters={
			"reference_doctype": "Multi Channel Cadence",
			"reference_name": mcc_name,
			"delivery_status": "Sent"
		}, fields=["name"], order_by="creation desc", limit=1)
		
		if comms:
			context["communication_name"] = comms[0].name
			ApolloCadenceProvider.report_event("message_opened", context, payload)
			
	elif event == "bounce":
		ApolloCadenceProvider.report_event("bounce", context, payload)
	
