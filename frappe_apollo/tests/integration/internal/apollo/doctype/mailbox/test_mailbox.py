import frappe
from frappe.tests import IntegrationTestCase
from unittest.mock import patch, MagicMock
from frappe_apollo.apollo.doctype.mailbox.mailbox import queue_get_mailboxes, get_mailboxes

class TestMailbox(IntegrationTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.db.delete("Account")
		# Create test accounts
		if not frappe.db.exists("Account", "Active Account 1"):
			frappe.get_doc({
				"doctype": "Account",
				"account_name": "Active Account 1",
				"api_key": "key1"
			}).insert()
			
		if not frappe.db.exists("Account", "Active Account 2"):
			frappe.get_doc({
				"doctype": "Account",
				"account_name": "Active Account 2",
				"api_key": "key2"
			}).insert()
			
		if not frappe.db.exists("Account", "Inactive Account"):
			frappe.get_doc({
				"doctype": "Account",
				"account_name": "Inactive Account",
				"api_key": ""
			}).insert()

	@classmethod
	def tearDownClass(cls):
		frappe.db.rollback()
		super().tearDownClass()

	@patch("frappe_apollo.apollo.doctype.mailbox.mailbox.enqueue")
	def test_queue_get_mailboxes(self, mock_enqueue):
		queue_get_mailboxes()
		
		# Should be called twice for the two active accounts
		self.assertEqual(mock_enqueue.call_count, 2)
		
		# Verify the arguments
		call_args = [call[1]["account_name"] for call in mock_enqueue.call_args_list]
		self.assertIn("Active Account 1", call_args)
		self.assertIn("Active Account 2", call_args)
		self.assertNotIn("Inactive Account", call_args)

	@patch("frappe_apollo.integrations.apollo.ApolloClient.get_email_accounts")
	def test_get_mailboxes(self, mock_get_email_accounts):
		mock_get_email_accounts.return_value = {
			"email_accounts": [
				{"id": "mb_1", "email": "test1@example.com", "active": True},
				{"id": "mb_2", "email": "test2@example.com", "active": True},
				{"id": "mb_3", "email": "test3@example.com", "active": False} # Should be ignored
			]
		}
		
		get_mailboxes("Active Account 1")
		
		# Verify mailboxes were created
		self.assertTrue(frappe.db.exists("Mailbox", "test1@example.com"))
		self.assertTrue(frappe.db.exists("Mailbox", "test2@example.com"))
		self.assertFalse(frappe.db.exists("Mailbox", "test3@example.com"))
		
		mb1 = frappe.get_doc("Mailbox", "test1@example.com")
		self.assertEqual(mb1.id, "mb_1")
		self.assertEqual(mb1.account, "Active Account 1")
