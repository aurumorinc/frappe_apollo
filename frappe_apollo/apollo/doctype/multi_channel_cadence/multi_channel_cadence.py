import frappe
from frappe_controller.utils.controller import wait_for_event

def on_update(doc, method=None):
	# If Draft -> Scheduled
	if doc.get_doc_before_save() and doc.get_doc_before_save().status == "Draft" and doc.status == "Scheduled":
		frappe.enqueue(
			method="frappe_apollo.apollo.doctype.multi_channel_cadence.multi_channel_cadence.add_a_contact_to_sequence",
			queue="medium",
			mcc_name=doc.name
		)

def add_a_contact_to_sequence(mcc_name):
	frappe.enqueue(
		method="frappe_apollo.apollo.doctype.crm_lead.crm_lead._create_a_contact",
		queue="medium",
		mcc_name=mcc_name
	)
	frappe.enqueue(
		method="frappe_apollo.apollo.doctype.sequence.sequence._assign_contact_to_sequence",
		queue="medium",
		mcc_name=mcc_name
	)
