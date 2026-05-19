import frappe
from frappe.tests import IntegrationTestCase
from unittest.mock import patch, MagicMock

class TestWebhook(IntegrationTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		
		# Create Account
		if not frappe.db.exists("Account", "Test Account Webhook"):
			frappe.get_doc({
				"doctype": "Account",
				"account_name": "Test Account Webhook",
				"webhook_bearer_token": "secret123",
				"client_id": "client_id",
				"client_secret": "client_secret"
			}).insert()

	@classmethod
	def tearDownClass(cls):
		frappe.db.rollback()
		super().tearDownClass()

	@patch("frappe_apollo.webhook.enqueue")
	def test_webhook_valid(self, mock_enqueue):
		frappe.set_user("Guest")
		frappe.local.request_ip = "127.0.0.1"
		frappe.local.request = frappe._dict({
			"headers": {"Authorization": "Bearer secret123"},
			"get_json": lambda: {"event": "test"}
		})
		
		from frappe_apollo.webhook import handle
		res = handle()
		
		self.assertEqual(res["status"], "ok")
		mock_enqueue.assert_called_once()
		
		frappe.set_user("Administrator")

	def test_webhook_invalid(self):
		frappe.set_user("Guest")
		frappe.local.request_ip = "127.0.0.1"
		frappe.local.request = frappe._dict({
			"headers": {"Authorization": "Bearer wrong_secret"},
			"get_json": lambda: {"event": "test"}
		})
		
		from frappe_apollo.webhook import handle
		with self.assertRaises(frappe.AuthenticationError):
			handle()
			
		frappe.set_user("Administrator")

	@patch("frappe_controller.utils.controller.emit_event")
	def test_process_webhook_message_sent(self, mock_emit_event):
		# Create Campaign
		campaign_name = frappe.db.get_value("Campaign", {"campaign_name": "Test Campaign API"}, "name")
		if not campaign_name:
			campaign = frappe.get_doc({
				"doctype": "Campaign",
				"campaign_name": "Test Campaign API"
			}).insert()
			campaign_name = campaign.name
			
		# Create Lead
		if not frappe.db.exists("CRM Lead", {"email": "test@leadapi.com"}):
			frappe.get_doc({
				"doctype": "CRM Lead",
				"first_name": "Test",
				"email": "test@leadapi.com"
			}).insert()
			
		# Create People
		lead_name = frappe.db.get_value("CRM Lead", {"email": "test@leadapi.com"}, "name")
		if not frappe.db.exists("People", {"lead": lead_name, "account": "Test Account Webhook"}):
			frappe.get_doc({
				"doctype": "People",
				"lead": lead_name,
				"account": "Test Account Webhook",
				"id": "contact_api_123"
			}).insert()
			
		# Create Sequence
		if not frappe.db.exists("Sequence", {"campaign": campaign_name, "account": "Test Account Webhook"}):
			frappe.get_doc({
				"doctype": "Sequence",
				"campaign": campaign_name,
				"sender": frappe.session.user,
				"account": "Test Account Webhook",
				"id": "seq_api_123"
			}).insert()
			
		mcc = frappe.get_doc({
			"doctype": "Multi Channel Campaign",
			"campaign_name": campaign_name,
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
			"delivery_status": "Scheduled",
			"sender": "test@sender.com"
		}).insert()
		
		payload = {
			"event": "message_sent",
			"contact_id": "contact_api_123",
			"emailer_campaign_id": "seq_api_123"
		}
		
		from frappe_apollo.webhook import process_webhook
		process_webhook(payload)
		
		comm.reload()
		self.assertEqual(comm.delivery_status, "Sent")
		mock_emit_event.assert_any_call("campaign_step_completed", {
			"campaign_name": campaign_name,
			"lead": lead_name,
			"mcc": mcc.name
		})

	def test_process_webhook_message_replied(self):
		# Create Campaign
		campaign_name = frappe.db.get_value("Campaign", {"campaign_name": "Test Campaign API"}, "name")
		if not campaign_name:
			campaign = frappe.get_doc({
				"doctype": "Campaign",
				"campaign_name": "Test Campaign API"
			}).insert()
			campaign_name = campaign.name
			
		# Create Lead
		if not frappe.db.exists("CRM Lead", {"email": "test@leadapi.com"}):
			frappe.get_doc({
				"doctype": "CRM Lead",
				"first_name": "Test",
				"email": "test@leadapi.com"
			}).insert()
			
		# Create People
		lead_name = frappe.db.get_value("CRM Lead", {"email": "test@leadapi.com"}, "name")
		if not frappe.db.exists("People", {"lead": lead_name, "account": "Test Account Webhook"}):
			frappe.get_doc({
				"doctype": "People",
				"lead": lead_name,
				"account": "Test Account Webhook",
				"id": "contact_api_123"
			}).insert()
			
		# Create Sequence
		if not frappe.db.exists("Sequence", {"campaign": campaign_name, "account": "Test Account Webhook"}):
			frappe.get_doc({
				"doctype": "Sequence",
				"campaign": campaign_name,
				"sender": frappe.session.user,
				"account": "Test Account Webhook",
				"id": "seq_api_123"
			}).insert()
		
		mcc = frappe.get_doc({
			"doctype": "Multi Channel Campaign",
			"campaign_name": campaign_name,
			"recipient": lead_name,
			"sender": frappe.session.user,
			"status": "Draft",
			"start_date": frappe.utils.nowdate()
		}).insert()
		
		payload = {
			"event": "message_replied",
			"contact_id": "contact_api_123",
			"emailer_campaign_id": "seq_api_123",
			"subject": "Re: Hello",
			"body": "Yes, I am interested.",
			"email": "test@leadapi.com"
		}
		
		from frappe_apollo.webhook import process_webhook
		process_webhook(payload)
		
		mcc.reload()
		self.assertEqual(mcc.status, "Completed")
		
		# Verify inbound communication
		inbound_comm = frappe.get_all("Communication", filters={
			"reference_doctype": "Multi Channel Campaign",
			"reference_name": mcc.name,
			"sent_or_received": "Received"
		})
		self.assertTrue(inbound_comm)
		
