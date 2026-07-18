import frappe
import unittest
from frappe_apollo.integrations.apollo import ApolloClient
from frappe_apollo.tests.integration.external.conftest import my_vcr

class TestApolloExternalAPI(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		import os
		# Use the account provided by the user via site_config or environment variable
		cls.account_name = frappe.conf.get("apollo_test_account") or os.environ.get("APOLLO_TEST_ACCOUNT")
		cls.sequence_id = frappe.conf.get("apollo_test_sequence_id") or os.environ.get("APOLLO_TEST_SEQUENCE_ID")
		
		# If no real credentials are provided, use dummy ones for VCR replay
		if not cls.account_name:
			cls.account_name = "Dummy VCR Account"
			if not frappe.db.exists("Account", cls.account_name):
				frappe.get_doc({
					"doctype": "Account",
					"account_name": cls.account_name,
					"api_key": "dummy_api_key_for_vcr"
				}).insert()
				
		if not cls.sequence_id:
			cls.sequence_id = "6a0cdfe8da382d001cc8423e" # Default sequence ID from cassettes
		
		# Check if the account exists in the database (for real accounts)
		if not frappe.db.exists("Account", cls.account_name):
			raise unittest.SkipTest(f"Account '{cls.account_name}' not found in database. Skipping external tests.")
			
		cls.client = ApolloClient(cls.account_name)

	@classmethod
	def tearDownClass(cls):
		frappe.db.rollback()
		super().tearDownClass()

	def tearDown(self):
		frappe.db.rollback()
		super().tearDown()

	@my_vcr.use_cassette('test_get_email_accounts.yaml')
	def test_get_email_accounts_live(self):
		response = self.client.get_email_accounts()
		self.assertIn("email_accounts", response)
		self.assertIsInstance(response["email_accounts"], list)

	@my_vcr.use_cassette('test_search_sequences.yaml')
	def test_search_sequences_live(self):
		response = self.client.search_sequences()
		self.assertIn("emailer_campaigns", response)
		self.assertIsInstance(response["emailer_campaigns"], list)

	@my_vcr.use_cassette('test_create_contact.yaml')
	def test_create_contact_live(self):
		lead_data = {
			"first_name": "Test",
			"last_name": "External API",
			"email": "test_external_api_create@example.com"
		}
		contact_id = self.client.create_contact(lead_data)
		self.assertIsNotNone(contact_id)

	@my_vcr.use_cassette('test_create_custom_field.yaml')
	def test_create_custom_field_live(self):
		field_name = "Test External Field VCR"
		response = self.client.create_custom_field(field_name, "string")
		self.assertIn("typed_custom_field", response)
		self.assertEqual(response["typed_custom_field"]["name"], field_name)

	@my_vcr.use_cassette('test_update_contact.yaml')
	def test_update_contact_live(self):
		# Setup: Create a contact to update
		lead_data = {
			"first_name": "Test",
			"last_name": "External API Update",
			"email": "test_external_api_update@example.com"
		}
		contact_id = self.client.create_contact(lead_data)
		self.assertIsNotNone(contact_id)
			
		# Act: Update the contact
		custom_fields = {
			"test_external_field": "Test Value"
		}
		response = self.client.update_contact(contact_id, custom_fields)
		
		# Assert
		self.assertIn("contact", response)

	@my_vcr.use_cassette('test_add_contacts_to_sequence.yaml')
	def test_add_contacts_to_sequence_live(self):
		# Setup: Get a mailbox ID
		accounts_response = self.client.get_email_accounts()
		if not accounts_response.get("email_accounts"):
			self.skipTest("No email accounts available to send from")
		mailbox_id = accounts_response["email_accounts"][0].get("id")
		
		# Setup: Create a contact to add to the sequence
		lead_data = {
			"first_name": "Test",
			"last_name": "External API Sequence",
			"email": "test_external_api_sequence@example.com"
		}
		contact_id = self.client.create_contact(lead_data)
		self.assertIsNotNone(contact_id)
			
		# Act: Add to sequence
		response = self.client.add_contacts_to_sequence(contact_id, self.sequence_id, mailbox_id)
		
		# Assert
		self.assertIn("contacts", response)

	@my_vcr.use_cassette('test_create_sequence.yaml')
	def test_create_sequence_live(self):
		import os
		if not frappe.conf.get("apollo_test_account") and not os.environ.get("APOLLO_TEST_ACCOUNT"):
			if not os.path.exists(os.path.join(os.path.dirname(__file__), 'cassettes', 'test_create_sequence.yaml')):
				self.skipTest("No credentials and no cassette found for this test.")

		sequence_name = "Test External Sequence VCR"
		sequence_id = self.client.create_sequence(sequence_name)
		self.assertIsNotNone(sequence_id)

	@my_vcr.use_cassette('test_update_sequence.yaml')
	def test_update_sequence_live(self):
		import os
		if not frappe.conf.get("apollo_test_account") and not os.environ.get("APOLLO_TEST_ACCOUNT"):
			if not os.path.exists(os.path.join(os.path.dirname(__file__), 'cassettes', 'test_update_sequence.yaml')):
				self.skipTest("No credentials and no cassette found for this test.")

		# Setup: Create a sequence to update
		sequence_id = self.client.create_sequence("Test External Sequence Update VCR")
		self.assertIsNotNone(sequence_id)
		
		# Act: Update the sequence
		payload = {"emailer_steps": []}
		response = self.client.update_sequence(sequence_id, payload)
		
		# Assert
		self.assertIn("emailer_campaign", response)
