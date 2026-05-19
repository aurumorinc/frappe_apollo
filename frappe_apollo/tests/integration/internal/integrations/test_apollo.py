import frappe
from frappe.tests import IntegrationTestCase
from unittest.mock import patch, MagicMock
from frappe_apollo.integrations.apollo import ApolloClient, ApolloRateLimitError
import requests

class TestApolloClient(IntegrationTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		# Create test account
		if not frappe.db.exists("Account", "Test Apollo Account"):
			frappe.get_doc({
				"doctype": "Account",
				"account_name": "Test Apollo Account",
				"api_key": "test_api_key"
			}).insert()
			
		if not frappe.db.exists("Account", "Test OAuth Account"):
			frappe.get_doc({
				"doctype": "Account",
				"account_name": "Test OAuth Account",
				"client_id": "test_client_id",
				"client_secret": "test_client_secret",
				"access_token": "test_access_token",
				"refresh_token": "test_refresh_token"
			}).insert()

	@classmethod
	def tearDownClass(cls):
		frappe.db.rollback()
		super().tearDownClass()

	def tearDown(self):
		# Reset OAuth token in case it was changed by a test
		if frappe.db.exists("Account", "Test OAuth Account"):
			account = frappe.get_doc("Account", "Test OAuth Account")
			account.access_token = "test_access_token"
			account.refresh_token = "test_refresh_token"
			account.save(ignore_permissions=True)
			frappe.db.commit()
		super().tearDown()

	@patch("frappe_apollo.integrations.apollo.requests.request")
	def test_api_key_auth(self, mock_request):
		mock_response = MagicMock()
		mock_response.status_code = 200
		mock_response.json.return_value = {"email_accounts": []}
		mock_request.return_value = mock_response
		
		client = ApolloClient("Test Apollo Account")
		client.get_email_accounts()
		
		mock_request.assert_called_once()
		headers = mock_request.call_args[1]["headers"]
		self.assertEqual(headers["X-Api-Key"], "test_api_key")
		self.assertEqual(headers["Cache-Control"], "no-cache")

	@patch("frappe_apollo.integrations.apollo.requests.request")
	def test_oauth_auth(self, mock_request):
		mock_response = MagicMock()
		mock_response.status_code = 200
		mock_response.json.return_value = {"email_accounts": []}
		mock_request.return_value = mock_response
		
		client = ApolloClient("Test OAuth Account")
		client.get_email_accounts()
		
		mock_request.assert_called_once()
		headers = mock_request.call_args[1]["headers"]
		self.assertEqual(headers["Authorization"], "Bearer test_access_token")

	@patch("frappe_apollo.integrations.apollo.requests.post")
	@patch("frappe_apollo.integrations.apollo.requests.request")
	def test_oauth_token_refresh(self, mock_request, mock_post):
		# First request returns 401
		mock_response_401 = MagicMock()
		mock_response_401.status_code = 401
		
		# Second request returns 200
		mock_response_200 = MagicMock()
		mock_response_200.status_code = 200
		mock_response_200.json.return_value = {"email_accounts": []}
		
		mock_request.side_effect = [mock_response_401, mock_response_200]
		
		# Mock refresh token response
		mock_refresh_response = MagicMock()
		mock_refresh_response.status_code = 200
		mock_refresh_response.json.return_value = {
			"access_token": "new_access_token",
			"refresh_token": "new_refresh_token"
		}
		mock_post.return_value = mock_refresh_response
		
		client = ApolloClient("Test OAuth Account")
		client.get_email_accounts()
		
		# Assert refresh was called
		mock_post.assert_called_once()
		self.assertEqual(mock_post.call_args[1]["data"]["grant_type"], "refresh_token")
		
		# Assert second request used new token
		self.assertEqual(mock_request.call_count, 2)
		headers = mock_request.call_args_list[1][1]["headers"]
		self.assertEqual(headers["Authorization"], "Bearer new_access_token")
		
		# Assert DB was updated
		account = frappe.get_doc("Account", "Test OAuth Account")
		self.assertEqual(account.get_password("access_token"), "new_access_token")

	@patch("frappe_apollo.integrations.apollo.requests.request")
	def test_rate_limiting(self, mock_request):
		mock_response = MagicMock()
		mock_response.status_code = 429
		mock_request.return_value = mock_response
		
		client = ApolloClient("Test Apollo Account")
		with self.assertRaises(ApolloRateLimitError):
			client.get_email_accounts()

	@patch("frappe_apollo.integrations.apollo.requests.request")
	def test_create_contact(self, mock_request):
		mock_response = MagicMock()
		mock_response.status_code = 200
		mock_response.json.return_value = {"contact": {"id": "new_contact_id"}}
		mock_request.return_value = mock_response
		
		client = ApolloClient("Test Apollo Account")
		contact_id = client.create_contact({"first_name": "Test"})
		
		self.assertEqual(contact_id, "new_contact_id")
		payload = mock_request.call_args[1]["json"]
		self.assertTrue(payload["run_dedupe"])

	@patch("frappe_apollo.integrations.apollo.requests.request")
	def test_update_contact(self, mock_request):
		mock_response = MagicMock()
		mock_response.status_code = 200
		mock_request.return_value = mock_response
		
		client = ApolloClient("Test Apollo Account")
		client.update_contact("contact_123", {"field_1": "value_1"})
		
		payload = mock_request.call_args[1]["json"]
		self.assertEqual(payload["typed_custom_fields"]["field_1"], "value_1")

	@patch("frappe_apollo.integrations.apollo.requests.request")
	def test_add_contacts_to_sequence(self, mock_request):
		mock_response = MagicMock()
		mock_response.status_code = 200
		mock_request.return_value = mock_response
		
		client = ApolloClient("Test Apollo Account")
		client.add_contacts_to_sequence("contact_123", "seq_123", "mb_123")
		
		payload = mock_request.call_args[1]["json"]
		self.assertEqual(payload["contact_ids[]"], ["contact_123"])
		self.assertEqual(payload["emailer_campaign_id"], "seq_123")
		self.assertEqual(payload["send_email_from_email_account_id"], "mb_123")

	@patch("frappe_apollo.integrations.apollo.requests.request")
	def test_add_contacts_to_sequence_fallback(self, mock_request):
		# First request returns 422
		mock_response_422 = MagicMock()
		mock_response_422.status_code = 422
		http_error = requests.exceptions.HTTPError()
		http_error.response = mock_response_422
		
		# Second request returns 200
		mock_response_200 = MagicMock()
		mock_response_200.status_code = 200
		
		mock_request.side_effect = [http_error, mock_response_200]
		
		client = ApolloClient("Test Apollo Account")
		client.add_contacts_to_sequence("contact_123", "seq_123", "mb_123")
		
		self.assertEqual(mock_request.call_count, 2)
		# Assert second call used params instead of json
		self.assertIn("params", mock_request.call_args_list[1][1])

	@patch("frappe_apollo.integrations.apollo.requests.request")
	def test_create_custom_field(self, mock_request):
		mock_response = MagicMock()
		mock_response.status_code = 200
		mock_request.return_value = mock_response
		
		client = ApolloClient("Test Apollo Account")
		client.create_custom_field("Test Field", "string")
		
		payload = mock_request.call_args[1]["json"]
		self.assertEqual(payload["label"], "Test Field")
		self.assertEqual(payload["type"], "string")
		self.assertEqual(payload["modality"], "contact")

	@patch("frappe_apollo.integrations.apollo.requests.request")
	def test_update_contact_status_sequence(self, mock_request):
		mock_response = MagicMock()
		mock_response.status_code = 200
		mock_request.return_value = mock_response
		
		client = ApolloClient("Test Apollo Account")
		client.update_contact_status_sequence("contact_123", "seq_123", "mark_as_finished")
		
		payload = mock_request.call_args[1]["json"]
		self.assertEqual(payload["contact_ids[]"], ["contact_123"])
		self.assertEqual(payload["emailer_campaign_ids[]"], ["seq_123"])
		self.assertEqual(payload["mode"], "mark_as_finished")
