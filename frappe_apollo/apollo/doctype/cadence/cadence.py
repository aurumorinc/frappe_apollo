import frappe

def on_update(doc, method=None):
	# Enqueue field provisioning for all steps
	frappe.enqueue(
		method="frappe_apollo.apollo.doctype.field.field.provision_cadence_fields",
		queue="low",
		cadence_name=doc.name
	)
