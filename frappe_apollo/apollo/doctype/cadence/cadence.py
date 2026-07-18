import frappe
from frappe_apollo.integrations.apollo import ApolloClient

def on_update(doc, method=None):
	# Enqueue sequence fields and steps provisioning
	frappe.enqueue(
		method="frappe_apollo.apollo.doctype.cadence.cadence.provision_sequences_fields_and_steps",
		queue="low",
		cadence_name=doc.name
	)

def provision_sequences_fields_and_steps(cadence_name):
	_provision_sequences(cadence_name)
	frappe.get_attr("frappe_apollo.apollo.doctype.field.field.provision_cadence_fields")(cadence_name)
	_setup_sequence_steps(cadence_name)

def _provision_sequences(cadence_name):
	doc = frappe.get_doc("Cadence", cadence_name)
	# Fetch active Apollo Account documents and senders from cadence.users
	if not doc.get("users"):
		return
		
	# Build current apollo_ids map
	existing_ids = {}
	if doc.get("apollo_ids"):
		for row in doc.apollo_ids:
			existing_ids[(row.account, row.sender)] = row.apollo_id
			
	modified = False
	for user_row in doc.users:
		# Need to find an active Apollo Account for this sender
		# Depending on the setup, an Account doc maps a frappe user to apollo
		# Let's search for Account records
		account_names = frappe.get_all("Account", filters={"status": "Active"}, pluck="name")
		if not account_names:
			continue
			
		for account_name in account_names:
			# If already provisioned, skip
			if (account_name, user_row.user) in existing_ids and existing_ids[(account_name, user_row.user)]:
				continue
				
			# Needs provisioning
			client = ApolloClient(account_name)
			try:
				apollo_id = client.create_sequence(
					name=f"{doc.cadence_name} - {user_row.user}",
					permissions="team_can_use",
					active=True
				)
				if apollo_id:
					doc.append("apollo_ids", {
						"account": account_name,
						"sender": user_row.user,
						"apollo_id": apollo_id,
						"status": "Active"
					})
					modified = True
			except Exception as e:
				frappe.log_error(f"Failed to create Apollo sequence for Cadence {cadence_name}", str(e))
				
	if modified:
		doc.save(ignore_permissions=True)
		frappe.db.commit()

def _setup_sequence_steps(cadence_name):
	doc = frappe.get_doc("Cadence", cadence_name)
	emailer_steps = []
	accumulated_wait = 0
	
	if not doc.get("cadence_schedules"):
		return
		
	for sch in doc.cadence_schedules:
		accumulated_wait += (sch.send_after_days or 0)
		if sch.reference_doctype == "Email Template":
			# Need subject and message field labels
			subject_field = sch.get("subject_field")
			message_field = sch.get("message_field")
			
			if subject_field and message_field:
				emailer_touches = [{
					"type": "auto_email",
					"include_signature": True,
					"emailer_template": {
						"subject": f"{subject_field}",
						"body_html": f"{message_field}"
					}
				}]
				emailer_steps.append({
					"type": "auto_email",
					"wait_time": accumulated_wait,
					"wait_mode": "day",
					"emailer_touches": emailer_touches
				})
				accumulated_wait = 0
				
	if emailer_steps and doc.get("apollo_ids"):
		# Update unique sequences
		unique_sequence_ids = set()
		for row in doc.apollo_ids:
			if row.apollo_id and row.status == "Active" and row.account:
				unique_sequence_ids.add((row.account, row.apollo_id))
				
		for account, seq_id in unique_sequence_ids:
			client = ApolloClient(account)
			try:
				client.update_sequence(seq_id, {"emailer_steps": emailer_steps})
			except Exception as e:
				frappe.log_error(f"Failed to update Apollo sequence {seq_id} for Cadence {cadence_name}", str(e))
