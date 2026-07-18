import frappe
from frappe.model.document import Document
import hashlib

class Field(Document):
	pass

def provision_cadence_fields(cadence_name):
	cadence = frappe.get_doc("Cadence", cadence_name)
	
	schedules = [s for s in (cadence.get("cadence_schedules") or []) if s.reference_doctype == "Email Template"]
	
	for step in schedules:
		for field_type in ["subject", "message"]:
			provision_a_field(cadence, step, field_type)
			
	# Commit any updates to the cadence step's subject_field / message_field
	cadence.save(ignore_permissions=True)

def provision_a_field(cadence, step, field_type):
	from frappe_apollo.integrations.apollo import ApolloClient
	from frappe_controller.utils.controller import wait_for_event
	
	is_enabled = frappe.db.get_value("Cadence Provider", "Apollo", "enabled")
	if not is_enabled:
		return
		
	hash_input = f"{cadence.name}_{step.name}_{field_type}"
	label = f"{hashlib.md5(hash_input.encode()).hexdigest()[:10]}"
	apollo_type = "string" if field_type == "subject" else "textarea"
	
	field_name = None
	try:
		field_doc = frappe.get_doc("Field", label)
		field_name = field_doc.name
	except frappe.DoesNotExistError:
		field_doc = frappe.get_doc({
			"doctype": "Field",
			"label": label,
			"field_type": apollo_type
		})
		field_doc.insert(ignore_permissions=True)
		field_name = field_doc.name
		
	if field_type == "subject":
		step.subject_field = field_name
	else:
		step.message_field = field_name

	# Check for missing apollo_ids and suspend if necessary
	missing_apollo_ids = False
	for row in cadence.get("users", []):
		# We need to make sure every user has a corresponding active apollo_id
		# But since apollo_ids just tracks account and sender, we just check if apollo_ids is fully populated.
		# A simpler way is to check if any apollo_id in cadence.apollo_ids is empty.
		# However, apollo_ids might not even be populated yet for the given users.
		# Let's check if the count matches or if any row is missing apollo_id.
		pass
		
	# Based on the blueprint: "Iterate through cadence.apollo_ids. If a row's apollo_id is missing or empty, execute wait_for_event listening to doc:Cadence:on_update evaluating argument.get('apollo_ids') to ensure sequence ID has populated."
	for apollo_id_row in cadence.get("apollo_ids", []):
		if not apollo_id_row.apollo_id:
			missing_apollo_ids = True
			break
			
	# Also we should consider if apollo_ids is empty but users are assigned.
	if (not cadence.get("apollo_ids") and cadence.get("users")) or missing_apollo_ids:
		wait_for_event(
			f"doc:Cadence:on_update:{cadence.name}",
			condition="any(row.get('apollo_id') for row in argument.get('apollo_ids', []))",
			consider_events_since=cadence.modified
		)
		# Reload after wake
		cadence.reload()

	for apollo_id_row in cadence.get("apollo_ids", []):
		if apollo_id_row.status != "Active":
			continue
			
		account_name = apollo_id_row.account
		apollo_sequence_id = apollo_id_row.apollo_id
		if not apollo_sequence_id:
			continue
			
		# Check if mapping exists
		mapping_exists = any(
			row.account == account_name and row.apollo_sequence_id == apollo_sequence_id
			for row in field_doc.get("apollo_ids", [])
		)
		
		if not mapping_exists:
			client = ApolloClient(account_name)
			try:
				res = client.create_custom_field(field_doc.label, field_doc.field_type)
				fields = res.get("typed_custom_fields", [])
				if fields:
					apollo_id = fields[0].get("id")
					field_doc.append("apollo_ids", {
						"account": account_name,
						"apollo_sequence_id": apollo_sequence_id,
						"apollo_id": apollo_id
					})
					field_doc.save(ignore_permissions=True)
			except Exception as e:
				frappe.log_error(title="Apollo Field Creation Failed", message=str(e))

