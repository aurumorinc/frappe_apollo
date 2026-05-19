import frappe
from frappe.tests import IntegrationTestCase
from unittest.mock import patch

class TestAccount(IntegrationTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		
		# Create Campaign
		if not frappe.db.exists("Campaign", "Test Campaign"):
			frappe.get_doc({
				"doctype": "Campaign",
				"campaign_name": "Test Campaign"
			}).insert()
			
		# Create Account
		if not frappe.db.exists("Account", "Test Account"):
			frappe.get_doc({
				"doctype": "Account",
				"account_name": "Test Account",
				"api_key": "key"
			}).insert()
			
		# Create Sequence
		if not frappe.db.exists("Sequence", {"campaign": "Test Campaign", "account": "Test Account"}):
			frappe.get_doc({
				"doctype": "Sequence",
				"campaign": "Test Campaign",
				"sender": frappe.session.user,
				"account": "Test Account",
				"id": "seq_1"
			}).insert()

	@classmethod
	def tearDownClass(cls):
		frappe.db.rollback()
		super().tearDownClass()

	@patch("frappe_apollo.apollo.doctype.sequence.sequence.Sequence.on_update")
	def test_on_update(self, mock_sequence_on_update):
		account = frappe.get_doc("Account", "Test Account")
		account.api_key = "new_key"
		account.save()
		
		# Verify Sequence on_update was called
		mock_sequence_on_update.assert_called()
