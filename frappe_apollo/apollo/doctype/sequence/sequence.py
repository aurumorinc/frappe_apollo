import frappe
from frappe.model.document import Document
from frappe_controller.utils.background_jobs import enqueue

class Sequence(Document):
	def on_update(self):
		self._populate_sequence_steps()
		self._enqueue_provision_custom_fields()

	def _populate_sequence_steps(self):
		"""
		Ensures the number of Sequence Step rows matches the number of Email schedules in the Campaign.
		"""
		if not self.campaign:
			return
			
		campaign = frappe.get_doc("Campaign", self.campaign)
		# Filter schedules to only include those where reference_doctype == "Email Template"
		email_schedules = [s for s in (campaign.get("campaign_schedules") or []) if s.reference_doctype == "Email Template"]
		
		current_steps = self.get("sequence_steps") or []
		if len(current_steps) < len(email_schedules):
			for i in range(len(current_steps), len(email_schedules)):
				self.append("sequence_steps", {})
			self.save()

	def _enqueue_provision_custom_fields(self):
		"""
		Enqueues jobs to provision custom fields in Apollo for each sequence step if missing.
		"""
		for idx, step in enumerate(self.sequence_steps, 1):
			if not step.subject_custom_field_id:
				enqueue(
					method="frappe_apollo.apollo.doctype.sequence.sequence.provision_custom_field",
					queue="low",
					sequence_name=self.name,
					step_idx=idx,
					field_type="subject"
				)
				
			if not step.response_custom_field_id:
				enqueue(
					method="frappe_apollo.apollo.doctype.sequence.sequence.provision_custom_field",
					queue="low",
					sequence_name=self.name,
					step_idx=idx,
					field_type="response"
				)

def provision_custom_field(sequence_name, step_idx, field_type):
	"""
	FS Job: Provisions a single custom field in Apollo.
	"""
	from frappe_apollo.integrations.apollo import ApolloClient
	
	sequence = frappe.get_doc("Sequence", sequence_name)
	step = sequence.sequence_steps[step_idx - 1]
	
	client = ApolloClient(sequence.account)
	
	if field_type == "subject":
		label = f"Seq {sequence.id} Step {step_idx} Subject"
		apollo_type = "string"
	else:
		label = f"Seq {sequence.id} Step {step_idx} Body"
		apollo_type = "textarea"
		
	# Check if Field record already exists in Frappe
	existing_field = frappe.db.get_value("Field", {"account": sequence.account, "label": label}, "id")
	field_id = existing_field
	
	if not field_id:
		try:
			res = client.create_custom_field(label, apollo_type)
			fields = res.get("typed_custom_fields", [])
			if fields:
				field_id = fields[0].get("id")
				frappe.get_doc({
					"doctype": "Field",
					"account": sequence.account,
					"label": label,
					"id": field_id
				}).insert()
		except Exception as e:
			frappe.log_error(f"Failed to create custom field {label} in Apollo", "Apollo Integration")
			raise e
			
	if field_id:
		if field_type == "subject":
			step.db_set("subject_custom_field_id", field_id)
		else:
			step.db_set("response_custom_field_id", field_id)
			
	return field_id

