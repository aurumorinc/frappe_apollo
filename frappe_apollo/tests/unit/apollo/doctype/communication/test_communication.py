import frappe
from frappe.tests import UnitTestCase
from frappe_apollo.apollo.doctype.communication.communication import update_a_contact, on_update
from unittest.mock import patch, MagicMock

class TestCommunicationOverride(UnitTestCase):

    @patch("frappe.enqueue")
    def test_on_update_enqueues_when_status_changes_to_scheduled(self, mock_enqueue):
        mock_doc = MagicMock()
        mock_doc_before = MagicMock()
        mock_doc_before.status = "Draft"
        mock_doc.get_doc_before_save.return_value = mock_doc_before
        mock_doc.status = "Scheduled"
        mock_doc.name = "Comm-1"

        on_update(mock_doc)

        mock_enqueue.assert_called_once_with(
            method="frappe_apollo.apollo.doctype.communication.communication.update_a_contact",
            queue="medium",
            comm_name="Comm-1"
        )

    @patch("frappe.enqueue")
    def test_on_update_does_not_enqueue_when_status_not_changed_to_scheduled(self, mock_enqueue):
        mock_doc = MagicMock()
        mock_doc_before = MagicMock()
        mock_doc_before.status = "Scheduled"
        mock_doc.get_doc_before_save.return_value = mock_doc_before
        mock_doc.status = "Scheduled"
        
        on_update(mock_doc)
        mock_enqueue.assert_not_called()

        mock_doc_before.status = "Draft"
        mock_doc.status = "Sent"
        on_update(mock_doc)
        mock_enqueue.assert_not_called()

    @patch("frappe.get_doc")
    def test_idempotency(self, mock_get_doc):
        mock_comm = MagicMock()
        mock_comm.get.return_value = "Synced"
        mock_get_doc.return_value = mock_comm
        
        # Should return early
        update_a_contact("Comm-1")
        # Ensure it didn't call get_doc for anything else (e.g. MCC)
        self.assertEqual(mock_get_doc.call_count, 1)

    @patch("frappe_apollo.apollo.doctype.communication.communication.wait_for_event")
    @patch("frappe.get_doc")
    @patch("frappe.db.get_value")
    def test_wait_state_email_account(self, mock_get_value, mock_get_doc, mock_wait):
        from frappe_controller.utils.controller import SuspendJob
        mock_wait.side_effect = SuspendJob("Suspended")

        mock_comm = MagicMock()
        mock_comm.get.return_value = None
        mock_mcc = MagicMock()
        mock_mcc.sender = "user@example.com"

        mock_get_doc.side_effect = [mock_comm, mock_mcc]
        mock_get_value.return_value = None # User Email not found

        with self.assertRaises(SuspendJob):
            update_a_contact("Comm-1")

        mock_wait.assert_called_once_with(
            event_key="doc:User Email:after_insert",
            condition="argument.get('parent') == 'user@example.com'"
        )

    @patch("frappe_apollo.apollo.doctype.communication.communication.wait_for_event")
    @patch("frappe.get_all")
    @patch("frappe.db.get_value")
    @patch("frappe.get_doc")
    def test_wait_state_people(self, mock_get_doc, mock_get_value, mock_get_all, mock_wait):
        from frappe_controller.utils.controller import SuspendJob
        mock_wait.side_effect = SuspendJob("Suspended")

        mock_comm = MagicMock()
        mock_comm.get.return_value = None
        
        mock_mcc = MagicMock()
        mock_mcc.sender = "user@example.com"
        mock_mcc.recipient = "Lead-1"
        
        mock_email_account = MagicMock()
        mock_acc = MagicMock()
        mock_acc.account = "Acc-1"
        mock_acc.apollo_id = "apollo-1"
        mock_email_account.apollo_accounts = [mock_acc]
        
        mock_account = MagicMock()
        mock_account.status = "Active"

        mock_get_doc.side_effect = [mock_comm, mock_mcc, mock_email_account, mock_account]
        
        def mock_get_value_side_effect(*args, **kwargs):
            if args[0] == "User Email":
                return "Email-Acc-1"
            if args[0] == "Cadence Provider":
                return 1
            if args[0] == "People":
                return None
            return None
            
        mock_get_value.side_effect = mock_get_value_side_effect

        with self.assertRaises(SuspendJob):
            update_a_contact("Comm-1")

        mock_wait.assert_called_once_with(
            event_key="doc:People:after_insert",
            condition="argument.get('lead') == 'Lead-1' and argument.get('account') == 'Acc-1'"
        )

    @patch("frappe_apollo.integrations.apollo.ApolloClient")
    @patch("frappe.get_all")
    @patch("frappe.db.get_value")
    @patch("frappe.get_doc")
    def test_success(self, mock_get_doc, mock_get_value, mock_get_all, mock_client_cls):
        mock_comm = MagicMock()
        mock_comm.get.return_value = None
        mock_comm.content = "content"
        mock_comm.subject = "subject"
        mock_comm.cadence_schedule = "Sch-1"
        
        mock_mcc = MagicMock()
        mock_mcc.name = "MCC-1"
        mock_mcc.sender = "user@example.com"
        mock_mcc.cadence_name = "Cadence-1"
        mock_mcc.recipient = "Lead-1"
        
        mock_email_account = MagicMock()
        mock_acc = MagicMock()
        mock_acc.account = "Acc-1"
        mock_acc.apollo_id = "apollo-1"
        mock_email_account.apollo_accounts = [mock_acc]
        
        mock_account = MagicMock()
        mock_account.status = "Active"
        
        mock_people = MagicMock()
        mock_people.apollo_id = "apollo-person-1"
        
        mock_cadence = MagicMock()
        mock_sch = MagicMock()
        mock_sch.name = "Sch-1"
        mock_cadence.cadence_schedules = [mock_sch]
        
        mock_step = MagicMock()
        mock_step.subject_custom_field_id = "sf-1"
        mock_step.response_custom_field_id = "rf-1"
        
        mock_seq_doc = MagicMock()
        mock_seq_doc.sequence_steps = [mock_step]
        
        mock_subject_field = MagicMock()
        mock_subject_field.apollo_id = "apollo-sf-1"
        
        mock_response_field = MagicMock()
        mock_response_field.apollo_id = "apollo-rf-1"

        mock_get_doc.side_effect = [
            mock_comm, 
            mock_mcc, 
            mock_email_account, 
            mock_account, 
            mock_people,
            mock_seq_doc,
            mock_cadence,
            mock_subject_field,
            mock_response_field
        ]
        
        def mock_get_value_side_effect(*args, **kwargs):
            if args[0] == "User Email":
                return "Email-Acc-1"
            if args[0] == "Cadence Provider":
                return 1
            if args[0] == "People":
                return "People-1"
            return None
            
        mock_get_value.side_effect = mock_get_value_side_effect
        
        mock_get_all.return_value = [MagicMock(name="Seq-1")]

        mock_client = mock_client_cls.return_value

        update_a_contact("Comm-1")

        mock_client.update_contact.assert_called_once_with(
            "apollo-person-1",
            {"apollo-sf-1": "subject", "apollo-rf-1": "content"}
        )
        
        mock_comm.db_set.assert_any_call("apollo_id", "apollo-person-1")
        mock_comm.db_set.assert_any_call("apollo_sync_status", "Synced")
