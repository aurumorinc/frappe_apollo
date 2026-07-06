import frappe
from frappe.tests import IntegrationTestCase
from unittest.mock import patch, MagicMock
from frappe_apollo.apollo.doctype.cadence_provider.cadence_provider import async_sync_lead_and_assign_sequence

class TestResumptionLogic(IntegrationTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Clean up any previous records
        frappe.db.sql("DELETE FROM `tabCRM Lead` WHERE email = 'john@example.com'")
        frappe.db.sql("DELETE FROM `tabMulti Channel Cadence` WHERE sender = 'test_user@example.com'")
        frappe.db.sql("DELETE FROM `tabUser Mailbox` WHERE parent = 'test_user@example.com'")
        frappe.db.sql("DELETE FROM `tabAccount` WHERE name = 'Test Account'")
        frappe.db.sql("DELETE FROM `tabMailbox` WHERE name = 'Test Mailbox'")
        frappe.db.sql("DELETE FROM `tabCadence` WHERE name = 'Test Cadence'")

    @classmethod
    def tearDownClass(cls):
        frappe.flags.current_job_id = None
        frappe.flags.current_job_step = None
        frappe.db.rollback()
        super().tearDownClass()

    @patch("frappe_apollo.apollo.doctype.cadence_provider.cadence_provider.ApolloClient")
    @patch("frappe_apollo.apollo.doctype.cadence_provider.cadence_provider.wait_for_event")
    def test_wait_for_user_mailbox(self, mock_wait_for_event, mock_client):
        from frappe_controller.utils.controller import SuspendJob
        def mock_wait_side_effect(event_key, condition, **kwargs):
            raise SuspendJob(event_key=event_key, payload=condition)
        mock_wait_for_event.side_effect = mock_wait_side_effect

        # Create Apollo Settings
        if not frappe.db.exists("Apollo Settings", "Apollo Settings"):
            frappe.get_doc({
                "doctype": "Apollo Settings",
                "enable": 1
            }).insert(ignore_permissions=True)
        else:
            settings = frappe.get_doc("Apollo Settings")
            settings.enable = 1
            settings.save()

        # Create Lead
        lead = frappe.get_doc({
            "doctype": "CRM Lead",
            "first_name": "John",
            "email": "john@example.com"
        }).insert(ignore_permissions=True)

        cadence = frappe.get_doc({
            "doctype": "Cadence",
            "cadence_name": "Test Cadence"
        }).insert(ignore_permissions=True)

        # Create MCC
        mcc = frappe.get_doc({
            "doctype": "Multi Channel Cadence",
            "recipient": lead.name,
            "sender": "test_user@example.com",
            "cadence_name": cadence.name,
            "start_date": "2024-01-01"
        }).insert(ignore_permissions=True, ignore_links=True)

        # Run async function, it should throw SuspendJob because there is no User Mailbox
        frappe.flags.current_job_id = "test_job_123"
        with self.assertRaises(SuspendJob) as context:
            async_sync_lead_and_assign_sequence(mcc.name)

        self.assertEqual(context.exception.event_key, "doc:User Mailbox:after_insert")
        self.assertEqual(context.exception.payload, "argument.get('parent') == 'test_user@example.com'")

        frappe.flags.current_job_id = None
        frappe.flags.current_job_step = None

        # Create Account and Mailbox
        frappe.get_doc({
            "doctype": "Account",
            "account_name": "Test Account"
        }).insert(ignore_permissions=True)
        
        frappe.get_doc({
            "doctype": "Mailbox",
            "name": "Test Mailbox",
            "account": "Test Account",
            "email_id": "test_user@example.com"
        }).insert(ignore_permissions=True)

        # Create User Mailbox
        frappe.get_doc({
            "doctype": "User Mailbox",
            "parent": "test_user@example.com",
            "parenttype": "User",
            "parentfield": "user_mailboxes",
            "mailbox": "test_user@example.com"
        }).insert(ignore_permissions=True, ignore_links=True)

        # Run async function again, it should progress to the next Wait-State (Sequence)
        frappe.flags.current_job_id = "test_job_124"
        with self.assertRaises(SuspendJob) as context:
            async_sync_lead_and_assign_sequence(mcc.name)

        self.assertEqual(context.exception.event_key, "doc:Sequence:after_insert")
        self.assertEqual(context.exception.payload, f"argument.get('campaign') == '{cadence.name}' and argument.get('account') == 'Test Account'")
