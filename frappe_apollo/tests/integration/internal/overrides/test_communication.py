import frappe
from frappe.tests import IntegrationTestCase
from unittest.mock import patch
from frappe_apollo.overrides.communication import update_contact

class TestCommunication(IntegrationTestCase):
	@classmethod
	@patch("frappe_apollo.integrations.apollo.ApolloClient.create_custom_field")
	def setUpClass(cls, mock_create_custom_field):
		mock_create_custom_field.return_value = {"typed_custom_fields": [{"id": "field_id"}]}
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
		
		# Create Email Template
		if not frappe.db.exists("Email Template", "Test Email Template"):
			frappe.get_doc({
				"doctype": "Email Template",
				"name": "Test Email Template",
				"subject": "Test",
				"response": "Test"
			}).insert()
		
		# Enable Apollo Settings
		settings = frappe.get_single("Apollo Settings")
		settings.enable = 1
		settings.save()
		
		# Create Campaign
		campaign_name = frappe.db.get_value("Campaign", {"campaign_name": "Test Campaign Comm"}, "name")
		if not campaign_name:
			campaign = frappe.get_doc({
				"doctype": "Campaign",
				"campaign_name": "Test Campaign Comm",
				"campaign_schedules": [
					{"reference_doctype": "Email Template", "reference_name": "Test Email Template", "send_after_days": 1}
				]
			}).insert()
			campaign_name = campaign.name
			
		cls.campaign_name = campaign_name
			
		# Create Account
		if not frappe.db.exists("Account", "Test Account Comm"):
			frappe.get_doc({
				"doctype": "Account",
				"account_name": "Test Account Comm",
				"api_key": "key"
			}).insert()
			
		# Create Mailbox
		if not frappe.db.exists("Mailbox", "test@comm.com"):
			frappe.get_doc({
				"doctype": "Mailbox",
				"email_id": "test@comm.com",
				"id": "mb_comm",
				"account": "Test Account Comm"
			}).insert()
			
		# Create User Mailbox
		if not frappe.db.exists("User Mailbox", {"parent": frappe.session.user, "mailbox": "test@comm.com"}):
			user = frappe.get_doc("User", frappe.session.user)
			user.append("user_mailboxes", {"mailbox": "test@comm.com"})
			user.save(ignore_permissions=True)
			
		# Create Lead
		if not frappe.db.exists("CRM Lead", {"email": "test@leadcomm.com"}):
			frappe.get_doc({
				"doctype": "CRM Lead",
				"first_name": "Test",
				"email": "test@leadcomm.com"
			}).insert()
			
		# Create People
		lead_name = frappe.db.get_value("CRM Lead", {"email": "test@leadcomm.com"}, "name")
		if not frappe.db.exists("People", {"lead": lead_name, "account": "Test Account Comm"}):
			frappe.get_doc({
				"doctype": "People",
				"lead": lead_name,
				"account": "Test Account Comm",
				"id": "apollo_contact_id"
			}).insert()

	@classmethod
	def tearDownClass(cls):
		frappe.db.rollback()
		super().tearDownClass()

	@patch("frappe_apollo.overrides.communication.enqueue")
	def test_on_update(self, mock_enqueue):
		lead_name = frappe.db.get_value("CRM Lead", {"email": "test@leadcomm.com"}, "name")
		
		mcc = frappe.get_doc({
			"doctype": "Multi Channel Campaign",
			"campaign_name": self.campaign_name,
			"recipient": lead_name,
			"sender": frappe.session.user,
			"status": "Draft",
			"start_date": frappe.utils.nowdate()
		}).insert()
		
		comm = frappe.get_doc({
			"doctype": "Communication",
			"communication_type": "Communication",
			"reference_doctype": "Multi Channel Campaign",
			"reference_name": mcc.name,
			"delivery_status": ""
		}).insert()
		
		# Change status to Scheduled
		comm.delivery_status = "Scheduled"
		comm.save()
		
		mock_enqueue.assert_called_once()
		self.assertEqual(mock_enqueue.call_args[1]["communication_name"], comm.name)

	@patch("frappe_apollo.integrations.apollo.ApolloClient.create_custom_field")
	@patch("frappe_apollo.integrations.apollo.ApolloClient.update_contact")
	@patch("frappe_controller.utils.controller.emit_event")
	def test_update_contact(self, mock_emit_event, mock_update_contact, mock_create_custom_field):
		mock_create_custom_field.return_value = {"typed_custom_fields": [{"id": "field_id"}]}
		lead_name = frappe.db.get_value("CRM Lead", {"email": "test@leadcomm.com"}, "name")
		
		mcc = frappe.get_doc({
			"doctype": "Multi Channel Campaign",
			"campaign_name": self.campaign_name,
			"recipient": lead_name,
			"sender": frappe.session.user,
			"status": "Draft",
			"step_idx": 1,
			"start_date": frappe.utils.nowdate()
		}).insert()
		
		seq = frappe.get_doc({
			"doctype": "Sequence",
			"campaign": self.campaign_name,
			"sender": frappe.session.user,
			"account": "Test Account Comm",
			"id": "seq_test_comm"
		}).insert()
		
		# Mock custom fields
		seq.sequence_steps[0].subject_custom_field_id = "subj_id"
		seq.sequence_steps[0].response_custom_field_id = "body_id"
		seq.save()
		
		comm = frappe.get_doc({
			"doctype": "Communication",
			"communication_type": "Communication",
			"reference_doctype": "Multi Channel Campaign",
			"reference_name": mcc.name,
			"delivery_status": "Scheduled",
			"subject": "Test Subject",
			"content": "Test Content"
		}).insert()
		
		update_contact(comm.name)
		
		mock_update_contact.assert_called_once_with("apollo_contact_id", {
			"subj_id": "Test Subject",
			"body_id": "Test Content"
		})
		
		mock_emit_event.assert_any_call("communication_scheduled", {
			"campaign_name": self.campaign_name,
			"step_idx": 1,
			"mcc": mcc.name
		})
		
		comm.reload()
		self.assertEqual(comm.apollo_sync_status, "Synced")
