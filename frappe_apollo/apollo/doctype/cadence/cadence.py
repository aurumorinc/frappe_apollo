import frappe

def on_update(doc, method=None):
	frappe.enqueue(
		method="frappe_apollo.apollo.doctype.sequence.sequence.on_cadence_update",
		queue="low",
		cadence_name=doc.name
	)
