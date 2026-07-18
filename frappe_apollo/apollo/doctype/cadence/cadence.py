import frappe
from frappe_apollo.integrations.apollo import ApolloClient
from frappe_controller.utils.background_jobs import enqueue

def on_update(doc, method=None):
	# Enqueue sequence fields and steps provisioning
	enqueue(
		"frappe_apollo.apollo.doctype.cadence.cadence.provision_sequences_fields_and_steps",
		queue="low",
		cadence_name=doc.name
	)

	if doc.has_value_changed("enabled"):
		enqueue(
			"frappe_apollo.apollo.doctype.cadence.cadence.update_sequences",
			queue="low",
			cadence_name=doc.name,
			is_enabled=doc.enabled
		)

def update_sequences(cadence_name, is_enabled):
	doc = frappe.get_doc("Cadence", cadence_name)
	if not doc.get("apollo_ids"):
		return
	
	for row in doc.apollo_ids:
		if row.status == "Active" and row.apollo_id and row.account:
			client = ApolloClient(row.account)
			try:
				if is_enabled:
					client.approve_sequence(row.apollo_id)
				else:
					client.abort_sequence(row.apollo_id)
			except Exception as e:
				frappe.log_error(f"Failed to {'enable' if is_enabled else 'disable'} Apollo sequence {row.apollo_id} for Cadence {cadence_name}", str(e))

def on_trash(doc, method=None):
	if doc.get("apollo_ids"):
		apollo_ids = [{"account": i.account, "apollo_id": i.apollo_id} for i in doc.apollo_ids if i.apollo_id and i.account]
		if apollo_ids:
			enqueue(
				"frappe_apollo.apollo.doctype.cadence.cadence.archive_sequences",
				queue="low",
				apollo_ids=apollo_ids
			)

def archive_sequences(apollo_ids):
	for item in apollo_ids:
		client = ApolloClient(item["account"])
		try:
			client.archive_sequence(item["apollo_id"])
		except Exception as e:
			frappe.log_error(f"Failed to archive Apollo sequence {item['apollo_id']}", str(e))

def provision_sequences_fields_and_steps(cadence_name):
	emailer_steps = _get_sequence_steps(cadence_name)
	_provision_sequences(cadence_name, emailer_steps)
	frappe.get_attr("frappe_apollo.apollo.doctype.field.field.provision_cadence_fields")(cadence_name)

def _provision_sequences(cadence_name, emailer_steps=None):
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
			client = ApolloClient(account_name)
			
			# If already provisioned, just update the steps
			if (account_name, user_row.user) in existing_ids and existing_ids[(account_name, user_row.user)]:
				seq_id = existing_ids[(account_name, user_row.user)]
				if emailer_steps:
					try:
						client.update_sequence(seq_id, {"emailer_steps": emailer_steps})
					except Exception as e:
						frappe.log_error(f"Failed to update Apollo sequence {seq_id} for Cadence {cadence_name}", str(e))
				continue
				
			# Needs provisioning
			try:
				apollo_id = client.create_sequence(
					name=f"{doc.cadence_name} - {user_row.user}",
					permissions="team_can_use",
					active=True,
					emailer_steps=emailer_steps
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

def _get_sequence_steps(cadence_name):
	doc = frappe.get_doc("Cadence", cadence_name)
	emailer_steps = []
	accumulated_wait = 0
	
	if not doc.get("cadence_schedules"):
		return []
		
	for sch in doc.cadence_schedules:
		accumulated_wait += (sch.send_after_days or 0)
		if sch.reference_doctype == "Email Template":
			# Need subject and message field labels
			subject_field = sch.get("subject_field")
			message_field = sch.get("message_field")
			
			if subject_field and message_field:
				if subject_field.startswith("custom_"):
					subject_field = subject_field[7:]
				if message_field.startswith("custom_"):
					message_field = message_field[7:]

				emailer_touches = [{
					"type": "auto_email",
					"include_signature": True,
					"emailer_template": {
						"subject": f"{{{{{subject_field}}}}}",
						"body_html": f"{{{{{message_field}}}}}"
					}
				}]
				emailer_steps.append({
					"type": "auto_email",
					"wait_time": accumulated_wait,
					"wait_mode": "day",
					"emailer_touches": emailer_touches
				})
				accumulated_wait = 0
				
	return emailer_steps
