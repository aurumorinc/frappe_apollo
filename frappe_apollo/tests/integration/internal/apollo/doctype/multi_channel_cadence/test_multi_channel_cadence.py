import frappe
from frappe.tests import IntegrationTestCase
from frappe_apollo.apollo.doctype.multi_channel_cadence.multi_channel_cadence import add_a_contact_to_sequence
from frappe_apollo.apollo.doctype.people.people import _create_a_contact
from frappe_apollo.apollo.doctype.sequence.sequence import _assign_contact_to_sequence
from frappe_controller.utils.controller import SuspendJob
from unittest.mock import patch, MagicMock

class TestMCCIntegration(IntegrationTestCase):
    @patch("frappe_controller.utils.controller.wait_for_event", side_effect=SuspendJob("wait"))
    @patch("frappe.db.get_value")
    @patch("frappe.get_doc")
    @patch("frappe.get_all")
    def test_sequence_inactive_raises_wait(self, mock_get_all, mock_get_doc, mock_get_value, mock_wait):
        # Setup mocks
        def mock_get_value_side_effect(dt, name_or_filters=None, fieldname=None):
            if dt == "Cadence Provider": return 1
            if dt == "User Email": return "Email-Acc-1"
            if dt == "People": return "people1"
            return "val"
        mock_get_value.side_effect = mock_get_value_side_effect
        
        
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
        mock_sequence.status = "Inactive" # This should cause wait
        mock_sequence.apollo_id = "seq1"
        mock_sequence.name = "seq_doc_1"
        
        def mock_get_doc_side_effect(*args, **kwargs):
            doctype = args[0] if args and isinstance(args[0], str) else (args[0].get('doctype') if args else kwargs.get('doctype'))
            if doctype == "Multi Channel Cadence": return mock_mcc
            if doctype == "Email Account": return mock_email_account
            if doctype == "Account": return mock_account
            if doctype == "People": return mock_people
            if doctype == "Sequence": return mock_sequence
            return MagicMock()
            
        mock_get_doc.side_effect = mock_get_doc_side_effect
        
        mock_get_all.return_value = [{"name": "seq_doc_1"}]
        
        with self.assertRaises(SuspendJob):
            _assign_contact_to_sequence("mcc1")

    @patch("frappe_controller.utils.controller.wait_for_event", side_effect=SuspendJob("wait"))
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
        mock_sequence.status = "Active"
        mock_sequence.apollo_id = "seq1"
        mock_sequence.name = "seq_doc_1"
        
        def mock_get_doc_side_effect(*args, **kwargs):
            doctype = args[0] if args and isinstance(args[0], str) else (args[0].get('doctype') if args else kwargs.get('doctype'))
            if doctype == "Multi Channel Cadence": return mock_mcc
            if doctype == "Email Account": return mock_email_account
            if doctype == "Account": return mock_account
            if doctype == "People": return mock_people
            if doctype == "Sequence": return mock_sequence
            return MagicMock()
            
        mock_get_doc.side_effect = mock_get_doc_side_effect
        mock_get_all.return_value = [{"name": "seq_doc_1"}]
        
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        _create_a_contact("mcc1")
        _assign_contact_to_sequence("mcc1")
        
        mock_client.add_contacts_to_sequence.assert_called_once_with("pid1", "seq1", "mb_apollo_1")
