import frappe
from frappe_controller.utils.background_jobs import enqueue

def on_update(doc, method=None):
	# If Apollo settings change, all sequences need to self-hydrate
	if doc.name == "Apollo":
		# Only enqueue for cadences linked to sequences
		sequences = frappe.get_all("Sequence", pluck="cadence")
		unique_cadences = list(set(sequences))
		for cadence_name in unique_cadences:
			enqueue(
				method="frappe_apollo.apollo.doctype.sequence.sequence.on_cadence_update",
				queue="low",
				cadence_name=cadence_name
			)
