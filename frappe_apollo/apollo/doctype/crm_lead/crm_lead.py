import frappe

def _create_a_contact(mcc_name):
	from frappe_controller.utils.controller import wait_for_event

	mcc = frappe.get_doc("Multi Channel Cadence", mcc_name)
	sender = mcc.sender
	lead_name = mcc.recipient

	# Find Email Account to get Apollo Account
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

	# Wait for Apollo Settings & Account
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

	# Ensure the CRM Lead has an entry for this account in apollo_ids
	lead = frappe.get_doc("CRM Lead", lead_name)
	apollo_accounts = [acc.account for acc in lead.get("apollo_ids", [])]

	if account_name not in apollo_accounts:
		lead.append("apollo_ids", {
			"account": account_name,
			"apollo_id": ""
		})
		lead.save(ignore_permissions=True)

	# We check if apollo_id is set
	current_row = next((row for row in lead.get("apollo_ids", []) if row.account == account_name), None)
	if current_row and not current_row.apollo_id:
		# Enqueue creation in Apollo
		frappe.enqueue(
			method="frappe_apollo.apollo.doctype.crm_lead.crm_lead.create_a_contact",
			queue="short",
			lead_name=lead_name,
			account_name=account_name
		)

		wait_for_event(
			event_key=f"doc:CRM Lead:on_update:{lead_name}",
			condition=f"any(row.get('account') == '{account_name}' and row.get('apollo_id') for row in argument.get('apollo_ids', []))"
		)


def create_a_contact(lead_name, account_name):
	from frappe_apollo.integrations.apollo import ApolloClient
	from frappe_controller.utils.controller import SuspendJob

	is_enabled = frappe.db.get_value("Cadence Provider", "Apollo", "enabled")
	if not is_enabled:
		raise SuspendJob("Apollo Cadence Provider is disabled.")

	account = frappe.get_doc("Account", account_name)
	if account.status != "Active":
		raise SuspendJob("Apollo Account is not Active.")

	lead = frappe.get_doc("CRM Lead", lead_name)

	client = ApolloClient(account_name)

	try:
		lead_data = {
			"first_name": lead.first_name,
			"last_name": lead.last_name,
			"email": lead.email,
			"organization_name": lead.organization
		}
		apollo_id = client.create_contact(lead_data)
		if apollo_id:
			# Get latest lead doc because it could be modified
			lead = frappe.get_doc("CRM Lead", lead_name)
			current_row = next((row for row in lead.get("apollo_ids", []) if row.account == account_name), None)
			if current_row:
				current_row.apollo_id = apollo_id
				lead.save(ignore_permissions=True)
	except Exception as e:
		frappe.log_error(title="Failed to create Contact in Apollo", message=str(e))
		raise
