import frappe
from frappe.tests import IntegrationTestCase
from unittest.mock import patch, MagicMock

class TestOAuth(IntegrationTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		
		# Create Account
		if not frappe.db.exists("Account", "Test Account OAuth"):
			frappe.get_doc({
				"doctype": "Account",
				"account_name": "Test Account OAuth",
				"webhook_bearer_token": "secret123",
				"client_id": "client_id",
				"client_secret": "client_secret"
			}).insert()

	@classmethod
	def tearDownClass(cls):
		frappe.db.rollback()
		super().tearDownClass()

	@patch("frappe_apollo.oauth.requests.post")
	def test_oauth_callback(self, mock_post):
		mock_response = MagicMock()
		mock_response.status_code = 200
		mock_response.json.return_value = {
			"access_token": "new_access",
			"refresh_token": "new_refresh"
		}
		mock_post.return_value = mock_response
		
		frappe.local.response = {}
		
		from frappe_apollo.oauth import callback
		callback("auth_code_123", "Test Account OAuth")
		
		account = frappe.get_doc("Account", "Test Account OAuth")
		self.assertEqual(account.get_password("access_token"), "new_access")
		self.assertEqual(account.get_password("refresh_token"), "new_refresh")
		
		self.assertEqual(frappe.local.response["type"], "redirect")
		self.assertEqual(frappe.local.response["location"], "/app/account/Test Account OAuth")
