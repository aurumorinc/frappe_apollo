import frappe
from frappe.model.document import Document
from frappe_controller.utils.background_jobs import enqueue

class People(Document):
	def after_insert(self):
		enqueue(
			method="frappe_apollo.apollo.doctype.people.people.create_people",
			queue="short",
			people_name=self.name
		)

def create_people(people_name):
	from frappe_apollo.integrations.apollo import ApolloClient
	from frappe_controller.utils.controller import SuspendJob
	
	settings = frappe.get_single("Apollo Settings")
	if not settings.enabled:
		raise SuspendJob("Apollo Settings is disabled.")
		
	people = frappe.get_doc("People", people_name)
	if people.apollo_id:
		return
		
	account = frappe.get_doc("Account", people.account)
	if account.status != "Active":
		raise SuspendJob("Apollo Account is not Active.")
		
	lead = frappe.get_doc("CRM Lead", people.lead)
	client = ApolloClient(people.account)
	
	try:
		lead_data = {
			"first_name": lead.first_name,
			"last_name": lead.last_name,
			"email": lead.email,
			"organization_name": lead.organization
		}
		apollo_id = client.create_people(lead_data)
		if apollo_id:
			people.db_set("apollo_id", apollo_id)
	except Exception as e:
		frappe.log_error(title="Failed to create People in Apollo", message=str(e))
		raise

def _create_people(mcc_name):
	from frappe_controller.utils.controller import wait_for_event
	
	mcc = frappe.get_doc("Multi Channel Cadence", mcc_name)
	sender = mcc.sender
	
	# Find Mailbox to get Account
	mailbox_id = frappe.db.get_value("User Mailbox", {"parent": sender}, "mailbox")
	if not mailbox_id:
		wait_for_event(
			event_key="doc:User Mailbox:after_insert",
			condition=f"argument.get('parent') == '{sender}'"
		)
		
	mailbox = frappe.get_doc("Mailbox", mailbox_id)
	account_name = mailbox.account
	
	# Wait for Apollo Settings & Account
	settings = frappe.get_single("Apollo Settings")
	if not settings.enabled:
		wait_for_event(
			event_key="doc:Apollo Settings:on_update",
			condition="argument.get('enabled') == 1"
		)
		
	account = frappe.get_doc("Account", account_name)
	if account.status != "Active":
		wait_for_event(
			event_key="doc:Account:on_update",
			condition=f"argument.get('name') == '{account_name}' and argument.get('status') == 'Active'"
		)
		
	# Local People doc creation if not exists
	people_name = frappe.db.get_value("People", {"lead": mcc.recipient, "account": account_name}, "name")
	if not people_name:
		people_doc = frappe.get_doc({
			"doctype": "People",
			"lead": mcc.recipient,
			"account": account_name
		})
		people_doc.insert(ignore_permissions=True)
		people_name = people_doc.name
		
	people = frappe.get_doc("People", people_name)
	if not people.apollo_id:
		wait_for_event(
			event_key="doc:People:on_update",
			condition=f"argument.get('name') == '{people_name}' and argument.get('apollo_id')"
		)
