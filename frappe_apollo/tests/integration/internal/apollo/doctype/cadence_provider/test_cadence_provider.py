import frappe
from frappe.tests import IntegrationTestCase
from unittest.mock import patch, MagicMock
from frappe_apollo.apollo.doctype.cadence_provider.cadence_provider import async_sync_lead_and_assign_sequence, async_sync_communication_to_apollo
from frappe_controller.utils.controller import SuspendJob

class TestCadenceProvider(IntegrationTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Clean up any previous records
        frappe.db.sql("DELETE FROM `tabCommunication` WHERE subject = 'Test Comm Subject'")
        frappe.db.sql("DELETE FROM `tabPeople` WHERE lead = 'Test Lead'")
        frappe.db.sql("DELETE FROM `tabCRM Lead` WHERE email = 'john@example.com'")
        frappe.db.sql("DELETE FROM `tabMulti Channel Cadence` WHERE sender = 'test_user@example.com'")
        frappe.db.sql("DELETE FROM `tabUser Mailbox` WHERE parent = 'test_user@example.com'")
        frappe.db.sql("DELETE FROM `tabSequence` WHERE cadence = 'Test Cadence'")
        frappe.db.sql("DELETE FROM `tabAccount` WHERE name = 'Test Account'")
        frappe.db.sql("DELETE FROM `tabMailbox` WHERE name = 'Test Mailbox'")
        frappe.db.sql("DELETE FROM `tabMailbox` WHERE name = 'test_user@example.com'")
        frappe.db.sql("DELETE FROM `tabCadence` WHERE name = 'Test Cadence'")
        frappe.db.sql("DELETE FROM `tabCadence` WHERE name = 'Test Happy Cadence'")
        frappe.db.sql("DELETE FROM `tabCadence` WHERE name = 'Test Comm Cadence'")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def tearDown(self):
        frappe.flags.current_job_id = None
        frappe.flags.current_job_step = None
        frappe.db.rollback()
        super().tearDown()

    @patch("frappe_apollo.apollo.doctype.cadence_provider.cadence_provider.ApolloClient")
    @patch("frappe_apollo.apollo.doctype.cadence_provider.cadence_provider.wait_for_event")
    def test_async_sync_lead_suspends_on_missing_mailbox(self, mock_wait_for_event, mock_client):
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
            settings.save(ignore_permissions=True)

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
        self.assertEqual(context.exception.payload, f"argument.get('cadence') == '{cadence.name}' and argument.get('account') == 'Test Account'")

    @patch("frappe_apollo.apollo.doctype.cadence_provider.cadence_provider.ApolloClient")
    def test_async_sync_lead_and_assign_sequence_happy_path(self, mock_client_class):
        mock_client = MagicMock()
        mock_client.create_contact.return_value = "apollo_people_123"
        mock_client_class.return_value = mock_client

        settings = frappe.get_doc("Apollo Settings")
        settings.enable = 1
        settings.save(ignore_permissions=True)
        
        if not frappe.db.exists("Account", "Test Account"):
            frappe.get_doc({"doctype": "Account", "account_name": "Test Account"}).insert(ignore_permissions=True)
        
        if not frappe.db.exists("Mailbox", "test_user@example.com"):
            frappe.get_doc({
                "doctype": "Mailbox",
                "name": "test_user@example.com",
                "account": "Test Account",
                "email_id": "test_user@example.com",
                "id": "apollo_mailbox_123"
            }).insert(ignore_permissions=True)
            
        if not frappe.db.exists("User Mailbox", {"parent": "test_user@example.com"}):
            frappe.get_doc({
                "doctype": "User Mailbox",
                "parent": "test_user@example.com",
                "parenttype": "User",
                "parentfield": "user_mailboxes",
                "mailbox": "test_user@example.com"
            }).insert(ignore_permissions=True, ignore_links=True)

        lead = frappe.get_doc({
            "doctype": "CRM Lead",
            "first_name": "Jane",
            "email": "jane@example.com",
            "organization": "Test Org"
        }).insert(ignore_permissions=True, ignore_links=True)

        cadence = frappe.get_doc({
            "doctype": "Cadence",
            "cadence_name": "Test Happy Cadence"
        }).insert(ignore_permissions=True)

        sequence = frappe.get_doc({
            "doctype": "Sequence",
            "cadence": cadence.name,
            "account": "Test Account",
            "id": "apollo_seq_123"
        }).insert(ignore_permissions=True)

        mcc = frappe.get_doc({
            "doctype": "Multi Channel Cadence",
            "recipient": lead.name,
            "sender": "test_user@example.com",
            "cadence_name": cadence.name,
            "start_date": "2024-01-01"
        }).insert(ignore_permissions=True, ignore_links=True)

        frappe.flags.current_job_id = "test_job_happy_lead"
        
        # Execute
        async_sync_lead_and_assign_sequence(mcc.name)

        # Assertions
        mock_client.create_contact.assert_called_once_with({
            "first_name": "Jane",
            "last_name": None,
            "email": "jane@example.com",
            "organization_name": "Test Org"
        })
        mock_client.add_contacts_to_sequence.assert_called_once_with(
            "apollo_people_123", "apollo_seq_123", "apollo_mailbox_123"
        )
        
        people_id = frappe.db.get_value("People", {"lead": lead.name, "account": "Test Account"}, "id")
        self.assertEqual(people_id, "apollo_people_123")

    @patch("frappe_apollo.apollo.doctype.cadence_provider.cadence_provider.ApolloClient")
    def test_async_sync_communication_to_apollo_happy_path(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        settings = frappe.get_doc("Apollo Settings")
        settings.enable = 1
        settings.save(ignore_permissions=True)
            
        if not frappe.db.exists("Account", "Test Account"):
            frappe.get_doc({"doctype": "Account", "account_name": "Test Account"}).insert(ignore_permissions=True)
        
        if not frappe.db.exists("Mailbox", "test_user@example.com"):
            frappe.get_doc({
                "doctype": "Mailbox",
                "name": "test_user@example.com",
                "account": "Test Account",
                "email_id": "test_user@example.com",
                "id": "apollo_mailbox_123"
            }).insert(ignore_permissions=True)
            
        if not frappe.db.exists("User Mailbox", {"parent": "test_user@example.com"}):
            frappe.get_doc({
                "doctype": "User Mailbox",
                "parent": "test_user@example.com",
                "parenttype": "User",
                "parentfield": "user_mailboxes",
                "mailbox": "test_user@example.com"
            }).insert(ignore_permissions=True, ignore_links=True)

        lead = frappe.get_doc({
            "doctype": "CRM Lead",
            "first_name": "Bob",
            "email": "bob@example.com"
        }).insert(ignore_permissions=True)
        
        frappe.get_doc({
            "doctype": "People",
            "lead": lead.name,
            "account": "Test Account",
            "id": "apollo_people_456"
        }).insert(ignore_permissions=True)

        cadence = frappe.get_doc({
            "doctype": "Cadence",
            "cadence_name": "Test Comm Cadence"
        })
        cadence.append("cadence_schedules", {
            "title": "Step 1",
            "wait_period": 0,
            "wait_duration": "Hours",
            "reference_doctype": "Email Template",
            "reference_name": "Test Template",
            "send_after_days": 0
        })
        cadence.insert(ignore_permissions=True, ignore_links=True)
        
        schedule_name = cadence.cadence_schedules[0].name

        sequence = frappe.get_doc({
            "doctype": "Sequence",
            "cadence": cadence.name,
            "account": "Test Account",
            "id": "apollo_seq_456"
        })
        sequence.append("sequence_steps", {
            "subject_custom_field_id": "cf_sub_1",
            "response_custom_field_id": "cf_res_1"
        })
        sequence.insert(ignore_permissions=True)

        mcc = frappe.get_doc({
            "doctype": "Multi Channel Cadence",
            "recipient": lead.name,
            "sender": "test_user@example.com",
            "cadence_name": cadence.name,
            "start_date": "2024-01-01"
        }).insert(ignore_permissions=True, ignore_links=True)
        
        comm = frappe.get_doc({
            "doctype": "Communication",
            "reference_doctype": "Multi Channel Cadence",
            "reference_name": mcc.name,
            "cadence_schedule": schedule_name,
            "subject": "Test Comm Subject",
            "content": "Test Comm Content",
            "status": "Scheduled"
        }).insert(ignore_permissions=True)

        frappe.flags.current_job_id = "test_job_happy_comm"
        
        # Execute
        async_sync_communication_to_apollo(comm.name)

        # Assertions
        mock_client.update_contact.assert_called_once_with(
            "apollo_people_456", 
            {
                "cf_sub_1": "Test Comm Subject",
                "cf_res_1": "Test Comm Content"
            }
        )
        
        comm.reload()
        self.assertEqual(comm.apollo_sync_status, "Synced")
