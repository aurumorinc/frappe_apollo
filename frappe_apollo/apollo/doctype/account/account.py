import frappe
from frappe.model.document import Document
from urllib.parse import urlparse, urlunparse

class Account(Document):
	def on_update(self):
		# Sweeps all linked Sequence records and triggers their on_update logic
		sequences = frappe.get_all("Sequence", filters={"account": self.name})
		for seq in sequences:
			doc = frappe.get_doc("Sequence", seq.name)
			doc.save()
			
	def after_insert(self):
		frappe.enqueue(
			method="frappe_apollo.apollo.doctype.mailbox.mailbox.get_mailboxes",
			queue="low",
			account_name=self.name
		)

	@frappe.whitelist()
	def get_authorization_url(self):
		raw_uri = frappe.utils.get_url("/api/method/frappe_apollo.oauth.callback")
		parsed = urlparse(raw_uri)
		redirect_uri = urlunparse(parsed._replace(netloc=parsed.hostname))
		
		url = f"https://app.apollo.io/#/oauth/authorize?client_id={self.client_id}&redirect_uri={redirect_uri}&response_type=code&state={self.name}"
		return url

