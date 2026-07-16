import frappe
from frappe_controller.utils.background_jobs import enqueue
from frappe_controller.utils.controller import wait_for_event

def on_update(doc, method=None):
	# If Draft -> Scheduled
	if doc.get_doc_before_save() and doc.get_doc_before_save().status == "Draft" and doc.status == "Scheduled":
		enqueue(
			method="frappe_apollo.apollo.doctype.multi_channel_cadence.multi_channel_cadence.add_people_to_sequence",
			queue="medium",
			mcc_name=doc.name
		)

def add_people_to_sequence(mcc_name):
	enqueue(
		method="frappe_apollo.apollo.doctype.people.people._create_people",
		queue="medium",
		mcc_name=mcc_name
	)
	enqueue(
		method="frappe_apollo.apollo.doctype.sequence.sequence._assign_people_to_sequence",
		queue="medium",
		mcc_name=mcc_name
	)
