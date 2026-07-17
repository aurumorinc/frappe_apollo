import frappe
from frappe.tests import IntegrationTestCase
from frappe_apollo.apollo.doctype.communication.communication import update_a_contact
from frappe_controller.utils.controller import SuspendJob
from unittest.mock import patch, MagicMock

class TestCommunicationIntegration(IntegrationTestCase):
    @patch("frappe_apollo.apollo.doctype.communication.communication.wait_for_event", side_effect=SuspendJob("wait"))
    @patch("frappe.db.get_value")
    @patch("frappe.get_doc")
    @patch("frappe.get_all")
    def test_missing_custom_fields_raises_wait(self, mock_get_all, mock_get_doc, mock_get_value, mock_wait):
        # Setup mocks
        def mock_get_value_side_effect(dt, name_or_filters=None, fieldname=None):
            if dt == "Cadence Provider": return 1
            if dt == "User Email": return "Email-Acc-1"
            if dt == "People": return "people1"
            return "val"
        mock_get_value.side_effect = mock_get_value_side_effect
        
        
        mock_comm = MagicMock()
        mock_comm.get.return_value = None
        mock_comm.reference_name = "mcc1"
        mock_comm.cadence_schedule = "sch1"
        
        mock_mcc = MagicMock()
        mock_mcc.sender = "user1"
        mock_mcc.recipient = "lead1"
        mock_mcc.cadence_name = "cad1"
        
        mock_email_account = MagicMock()
        mock_acc = MagicMock()
        mock_acc.account = "acc1"
        mock_acc.apollo_id = "mb_apollo_1"
        mock_email_account.apollo_accounts = [mock_acc]
        mock_email_account.get.return_value = [mock_acc]
        
        mock_account = MagicMock()
        mock_account.status = "Active"
        
        mock_people = MagicMock()
        mock_people.apollo_id = "pid1"
        
        mock_sequence = MagicMock()
        mock_sequence.name = "seq1"
        mock_step = MagicMock()
        mock_step.subject_custom_field_id = None # Missing field
        mock_sequence.sequence_steps = [mock_step]
        
        mock_cadence = MagicMock()
        mock_sch = MagicMock()
        mock_sch.name = "sch1"
        mock_cadence.cadence_schedules = [mock_sch]
        
        def mock_get_doc_side_effect(*args, **kwargs):
            doctype = args[0] if args and isinstance(args[0], str) else (args[0].get('doctype') if args else kwargs.get('doctype'))
            if doctype == "Communication": return mock_comm
            if doctype == "Multi Channel Cadence": return mock_mcc
            if doctype == "Email Account": return mock_email_account
            if doctype == "Account": return mock_account
            if doctype == "People": return mock_people
            if doctype == "Sequence": return mock_sequence
            if doctype == "Cadence": return mock_cadence
            return MagicMock()
            
        mock_get_doc.side_effect = mock_get_doc_side_effect
        mock_get_all.return_value = [{"name": "seq1"}]
        
        with self.assertRaises(SuspendJob):
            update_a_contact("comm1")

    @patch("frappe_apollo.apollo.doctype.communication.communication.wait_for_event", side_effect=SuspendJob("wait"))
    @patch("frappe.db.get_value")
    @patch("frappe.get_doc")
    @patch("frappe.get_all")
    @patch("frappe_apollo.integrations.apollo.ApolloClient")
    def test_valid_sync(self, mock_client_class, mock_get_all, mock_get_doc, mock_get_value, mock_wait):
        # Setup mocks
        def mock_get_value_side_effect(dt, name_or_filters=None, fieldname=None):
            if dt == "Cadence Provider": return 1
            if dt == "User Email": return "Email-Acc-1"
            if dt == "People": return "people1"
            return "val"
        mock_get_value.side_effect = mock_get_value_side_effect
        
        
        mock_comm = MagicMock()
        mock_comm.get.return_value = None
        mock_comm.reference_name = "mcc1"
        mock_comm.cadence_schedule = "sch1"
        mock_comm.subject = "Test Sub"
        mock_comm.content = "Test Content"
        
        mock_mcc = MagicMock()
        mock_mcc.sender = "user1"
        mock_mcc.recipient = "lead1"
        mock_mcc.cadence_name = "cad1"
        
        mock_email_account = MagicMock()
        mock_acc = MagicMock()
        mock_acc.account = "acc1"
        mock_acc.apollo_id = "mb_apollo_1"
        mock_email_account.apollo_accounts = [mock_acc]
        mock_email_account.get.return_value = [mock_acc]
        
        mock_account = MagicMock()
        mock_account.status = "Active"
        
        mock_people = MagicMock()
        mock_people.apollo_id = "pid1"
        
        mock_sequence = MagicMock()
        mock_sequence.name = "seq1"
        mock_step = MagicMock()
        mock_step.subject_custom_field_id = "f1"
        mock_step.response_custom_field_id = "f2"
        mock_sequence.sequence_steps = [mock_step]
        
        mock_cadence = MagicMock()
        mock_sch = MagicMock()
        mock_sch.name = "sch1"
        mock_cadence.cadence_schedules = [mock_sch]
        
        mock_field_1 = MagicMock()
        mock_field_1.apollo_id = "af1"
        mock_field_2 = MagicMock()
        mock_field_2.apollo_id = "af2"
        
        def mock_get_doc_side_effect(*args, **kwargs):
            doctype = args[0] if args and isinstance(args[0], str) else (args[0].get('doctype') if args else kwargs.get('doctype'))
            name = args[1] if len(args) > 1 else kwargs.get('name')
            if doctype == "Communication": return mock_comm
            if doctype == "Multi Channel Cadence": return mock_mcc
            if doctype == "Email Account": return mock_email_account
            if doctype == "Account": return mock_account
            if doctype == "People": return mock_people
            if doctype == "Sequence": return mock_sequence
            if doctype == "Cadence": return mock_cadence
            if doctype == "Field":
                if name == "f1": return mock_field_1
                if name == "f2": return mock_field_2
            return MagicMock()
            
        mock_get_doc.side_effect = mock_get_doc_side_effect
        mock_get_all.return_value = [{"name": "seq1"}]
        
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        update_a_contact("comm1")
        
        mock_client.update_contact.assert_called_once_with("pid1", {"af1": "Test Sub", "af2": "Test Content"})
