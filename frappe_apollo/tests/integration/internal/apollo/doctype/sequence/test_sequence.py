import frappe
from frappe.tests import IntegrationTestCase
from unittest.mock import patch, MagicMock
from frappe_apollo.apollo.doctype.sequence.sequence import (
	create_contact_add_to_sequence,
	create_contact,
	add_contact_to_sequence,
	provision_custom_field
)

class TestSequence(IntegrationTestCase):
	@classmethod
	@patch("frappe_apollo.apollo.doctype.sequence.sequence.enqueue")
	def setUpClass(cls, mock_enqueue):
		super().setUpClass()
		
		# Create Custom Fields if they don't exist
		if not frappe.db.exists("Custom Field", "User-user_mailboxes"):
			frappe.get_doc({
				"doctype": "Custom Field",
				"dt": "User",
				"fieldname": "user_mailboxes",
				"label": "User Mailboxes",
				"fieldtype": "Table",
				"options": "User Mailbox"
			}).insert(ignore_permissions=True)
			
		if not frappe.db.exists("Custom Field", "Communication-apollo_sync_status"):
			frappe.get_doc({
				"doctype": "Custom Field",
				"dt": "Communication",
				"fieldname": "apollo_sync_status",
				"label": "Apollo Sync Status",
				"fieldtype": "Select",
				"options": "Pending\nSynced\nError",
				"default": "Pending"
			}).insert(ignore_permissions=True)
			
		frappe.db.commit()
		frappe.clear_cache(doctype="User")
		frappe.clear_cache(doctype="Communication")
		
		frappe.db.delete("Campaign")
		frappe.db.delete("Sequence")
		frappe.db.delete("Multi Channel Campaign")
		frappe.db.delete("Communication")
		frappe.db.delete("Field")
		
		# Create Email Template
		if not frappe.db.exists("Email Template", "Test Email Template"):
			frappe.get_doc({
				"doctype": "Email Template",
				"name": "Test Email Template",
				"subject": "Test",
				"response": "Test"
			}).insert()
			
		# Create Campaign
		if not frappe.db.exists("Campaign", "Test Campaign Seq"):
			frappe.get_doc({
				"doctype": "Campaign",
				"campaign_name": "Test Campaign Seq",
				"campaign_schedules": [
					{"reference_doctype": "Email Template", "reference_name": "Test Email Template", "send_after_days": 1},
					{"reference_doctype": "Email Template", "reference_name": "Test Email Template", "send_after_days": 2},
					{"reference_doctype": "Email Template", "reference_name": "Test Email Template", "send_after_days": 3}
				]
			}).insert()
			
		# Create Account
		if not frappe.db.exists("Account", "Test Account Seq"):
			frappe.get_doc({
				"doctype": "Account",
				"account_name": "Test Account Seq",
				"api_key": "key"
			}).insert()
			
		# Create Mailbox
		if not frappe.db.exists("Mailbox", "test@seq.com"):
			frappe.get_doc({
				"doctype": "Mailbox",
				"email_id": "test@seq.com",
				"id": "mb_seq",
				"account": "Test Account Seq"
			}).insert()
			
		# Create User Mailbox
		if not frappe.db.exists("User Mailbox", {"parent": frappe.session.user, "mailbox": "test@seq.com"}):
			user = frappe.get_doc("User", frappe.session.user)
			user.append("user_mailboxes", {"mailbox": "test@seq.com"})
			user.save(ignore_permissions=True)

	@classmethod
	def tearDownClass(cls):
		frappe.db.rollback()
		super().tearDownClass()

	@patch("frappe_apollo.apollo.doctype.sequence.sequence.enqueue")
	def test_populate_sequence_steps(self, mock_enqueue):
		seq = frappe.get_doc({
			"doctype": "Sequence",
			"campaign": "Test Campaign Seq",
			"sender": frappe.session.user,
			"account": "Test Account Seq",
			"id": "seq_test_1"
		}).insert()
		
		# Should have 3 steps because Campaign has 3 Email Template schedules
		self.assertEqual(len(seq.sequence_steps), 3)

	@patch("frappe_apollo.apollo.doctype.sequence.sequence.enqueue")
	def test_on_update(self, mock_enqueue):
		seq = frappe.get_doc({
			"doctype": "Sequence",
			"campaign": "Test Campaign Seq",
			"sender": frappe.session.user,
			"account": "Test Account Seq",
			"id": "seq_test_2"
		}).insert()
		
		# Should call enqueue for provision_custom_field at least 6 times (3 steps * 2 fields)
		self.assertGreaterEqual(mock_enqueue.call_count, 6)
		
		# Verify first call
		call_1 = mock_enqueue.call_args_list[0]
		self.assertEqual(call_1.kwargs["method"], "frappe_apollo.apollo.doctype.sequence.sequence.provision_custom_field")
		self.assertEqual(call_1.kwargs["sequence_name"], seq.name)
		self.assertEqual(call_1.kwargs["step_idx"], 1)
		self.assertEqual(call_1.kwargs["field_type"], "subject")

	@patch("frappe_apollo.integrations.apollo.ApolloClient.create_custom_field")
	def test_provision_custom_field(self, mock_create_custom_field):
		mock_create_custom_field.return_value = {"typed_custom_fields": [{"id": "field_id_123"}]}
		
		seq = frappe.get_doc({
			"doctype": "Sequence",
			"campaign": "Test Campaign Seq",
			"sender": frappe.session.user,
			"account": "Test Account Seq",
			"id": "seq_test_cf"
		}).insert()
		
		field_id = provision_custom_field(seq.name, 1, "subject")
		
		self.assertEqual(field_id, "field_id_123")
		mock_create_custom_field.assert_called_once_with(f"Seq seq_test_cf Step 1 Subject", "string")
		
		seq.reload()
		self.assertEqual(seq.sequence_steps[0].subject_custom_field_id, "field_id_123")

	@patch("frappe_apollo.apollo.doctype.sequence.sequence.enqueue")
	def test_create_contact_add_to_sequence_workflow(self, mock_enqueue):
		# Mock the promises
		mock_promise_1 = MagicMock()
		mock_promise_1.result.return_value = "people_id_123"
		
		mock_promise_2 = MagicMock()
		
		mock_enqueue.side_effect = [mock_promise_1, mock_promise_2]
		
		create_contact_add_to_sequence("Test MCC")
		
		self.assertEqual(mock_enqueue.call_count, 2)
		
		# Verify first call
		call_1 = mock_enqueue.call_args_list[0]
		self.assertEqual(call_1.kwargs["method"], "frappe_apollo.apollo.doctype.sequence.sequence.create_contact")
		self.assertEqual(call_1.kwargs["campaign_name"], "Test MCC")
		
		# Verify second call
		call_2 = mock_enqueue.call_args_list[1]
		self.assertEqual(call_2.kwargs["method"], "frappe_apollo.apollo.doctype.sequence.sequence.add_contact_to_sequence")
		self.assertEqual(call_2.kwargs["campaign_name"], "Test MCC")
		self.assertEqual(call_2.kwargs["people_id"], "people_id_123")

	@patch("frappe_apollo.integrations.apollo.ApolloClient.create_contact")
	def test_create_contact(self, mock_create_contact):
		mock_create_contact.return_value = "apollo_contact_id"
		
		# Create Lead
		lead = frappe.get_doc({
			"doctype": "CRM Lead",
			"first_name": "Test",
			"email": "test@lead.com"
		}).insert()
		
		# Create MCC
		mcc = frappe.get_doc({
			"doctype": "Multi Channel Campaign",
			"campaign_name": "Test Campaign Seq",
			"recipient": lead.name,
			"sender": frappe.session.user,
			"status": "Draft",
			"start_date": frappe.utils.nowdate()
		}).insert()
		
		people_id = create_contact(mcc.name)
		
		self.assertEqual(people_id, "apollo_contact_id")
		mock_create_contact.assert_called_once()
		
		# Verify People record
		self.assertTrue(frappe.db.exists("People", {"lead": lead.name, "account": "Test Account Seq"}))

	@patch("frappe_apollo.integrations.apollo.ApolloClient.add_contacts_to_sequence")
	def test_add_contact_to_sequence(self, mock_add_contacts):
		# Create Lead
		lead = frappe.get_doc({
			"doctype": "CRM Lead",
			"first_name": "Test2",
			"email": "test2@lead.com"
		}).insert()
		
		# Create MCC
		mcc = frappe.get_doc({
			"doctype": "Multi Channel Campaign",
			"campaign_name": "Test Campaign Seq",
			"recipient": lead.name,
			"sender": frappe.session.user,
			"status": "Draft",
			"start_date": frappe.utils.nowdate()
		}).insert()
		
		# Create Sequence
		frappe.get_doc({
			"doctype": "Sequence",
			"campaign": "Test Campaign Seq",
			"sender": frappe.session.user,
			"account": "Test Account Seq",
			"id": "seq_test_add"
		}).insert()
		
		# Create Step 1 Communication
		frappe.get_doc({
			"doctype": "Communication",
			"communication_type": "Communication",
			"reference_doctype": "Multi Channel Campaign",
			"reference_name": mcc.name,
			"delivery_status": "Scheduled"
		}).insert()
		
		add_contact_to_sequence(mcc.name, "people_id_123")
		
		mock_add_contacts.assert_called_once_with("people_id_123", "seq_test_add", "mb_seq")
