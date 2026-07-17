import frappe
from frappe_controller.utils.controller import wait_for_event

def on_update(doc, method=None):
	# If Draft -> Scheduled
	if doc.get_doc_before_save() and doc.get_doc_before_save().status == "Draft" and doc.status == "Scheduled":
		frappe.enqueue(
			method="frappe_apollo.overrides.multi_channel_cadence.add_a_contact_to_sequence",
			queue="medium",
			mcc_name=doc.name
		)

