import frappe
from frappe.model.document import Document
import hashlib

class Field(Document):
	def after_insert(self):
		self.enqueue_create_a_field()

	def enqueue_create_a_field(self):
		frappe.enqueue(
			"frappe_apollo.apollo.doctype.field.field.create_a_field",
			queue="short",
			field_name=self.name
		)

def create_a_field(field_name):
	from frappe_apollo.integrations.apollo import ApolloClient
	from frappe_controller.utils.controller import SuspendJob
	
	settings = frappe.get_single("Apollo Settings")
	if not settings.enabled:
		raise SuspendJob("Apollo Settings is disabled.")
		
	field_doc = frappe.get_doc("Field", field_name)
	if field_doc.apollo_id:
		return
		
	account = frappe.get_doc("Account", field_doc.account)
	if account.status != "Active":
		raise SuspendJob("Apollo Account is not Active.")
		
	client = ApolloClient(field_doc.account)
	try:
		res = client.create_field(field_doc.label, field_doc.field_type)
		fields = res.get("typed_custom_fields", [])
		if fields:
			apollo_id = fields[0].get("id")
			field_doc.db_set("apollo_id", apollo_id)
	except Exception as e:
		frappe.log_error(title="Apollo Field Creation Failed", message=str(e))
		raise

def provision_a_field(sequence_name, step_idx, field_type):
	sequence = frappe.get_doc("Sequence", sequence_name)
	step = sequence.sequence_steps[step_idx - 1]
	
	# MD5 of sequence apollo_id and step index
	hash_input = f"{sequence.apollo_id}_{step_idx}_{field_type}"
	md5_hash = hashlib.md5(hash_input.encode()).hexdigest()[:10]
	label = f"Seq {sequence.apollo_id} {md5_hash} {field_type.capitalize()}"
	apollo_type = "string" if field_type == "subject" else "textarea"
	
	existing_field = frappe.db.get_value("Field", {"account": sequence.account, "label": label}, "name")
	field_name = existing_field
	
	if not field_name:
		field_doc = frappe.get_doc({
			"doctype": "Field",
			"account": sequence.account,
			"label": label,
			"field_type": apollo_type
		})
		field_doc.insert(ignore_permissions=True)
		field_name = field_doc.name
		
	if field_type == "subject":
		step.db_set("subject_custom_field_id", field_name)
	else:
		step.db_set("response_custom_field_id", field_name)
