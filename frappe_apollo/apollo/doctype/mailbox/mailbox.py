import frappe
from frappe.model.document import Document

class Mailbox(Document):
	pass

@frappe.whitelist()
def queue_get_mailboxes():
	"""
	RQ Job: A daily cron job that sweeps all active Accounts and enqueues the FS Job get_mailboxes for each.
	"""
	accounts = frappe.get_all("Account", filters={"api_key": ["!=", ""]}) # Simplified check for active
	for acc in accounts:
		frappe.enqueue(
			method="frappe_apollo.apollo.doctype.mailbox.mailbox.get_mailboxes",
			queue="low",
			account_name=acc.name
		)

def get_mailboxes(account_name):
	"""
	FS Job: Uses ApolloClient.get_email_accounts() to fetch mailboxes.
	Upserts Mailbox records in Frappe.
	"""
	from frappe_apollo.integrations.apollo import ApolloClient
	
	client = ApolloClient(account_name)
	try:
		mailboxes = client.get_email_accounts()
		for mb in mailboxes.get("email_accounts", []):
			if not mb.get("active"):
				continue
				
			email_id = mb.get("email")
			if not email_id:
				continue
				
			if frappe.db.exists("Mailbox", email_id):
				doc = frappe.get_doc("Mailbox", email_id)
				doc.apollo_id = mb.get("id")
				doc.account = account_name
				doc.save()
			else:
				frappe.get_doc({
					"doctype": "Mailbox",
					"email_id": email_id,
					"apollo_id": mb.get("id"),
					"account": account_name
				}).insert()
	except Exception:
		frappe.log_error(f"Failed to get mailboxes for {account_name}", "Apollo Integration")
		raise
