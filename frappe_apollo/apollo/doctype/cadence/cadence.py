import frappe
from frappe_controller.utils.background_jobs import enqueue

def on_update(doc, method=None):
	enqueue(
		method="frappe_apollo.apollo.doctype.sequence.sequence.on_cadence_update",
		queue="low",
		cadence_name=doc.name
	)
