import frappe
from frappe.tests import UnitTestCase
from frappe_apollo.apollo.doctype.multi_channel_cadence.multi_channel_cadence import before_save, _assign_contact_to_sequence
from frappe_controller.utils.controller import SuspendJob
from unittest.mock import patch, MagicMock

class TestMultiChannelCadence(UnitTestCase):
    @patch("frappe.get_doc")
    @patch("frappe.get_all")
    def test_before_save_ignores_missing_apollo_id(self, mock_get_all, mock_get_doc):
        # MCC setup
        mcc = MagicMock()
        mcc.provider = "Apollo"
        mcc.sender = "user@example.com"
        mcc.apollo_account = None
        mcc.apollo_sequence_id = None
        mcc.cadence = "Cad1"
        
        # Cadence setup
        mock_cadence = MagicMock()
        mock_mapping_active_no_id = MagicMock(sender="user@example.com", status="Active", apollo_id=None)
        mock_mapping_active_with_id = MagicMock(sender="user@example.com", status="Active", apollo_id="seq123", account="Acc1", name="row1")
        mock_cadence.apollo_ids = [mock_mapping_active_no_id, mock_mapping_active_with_id]
        
        mock_get_doc.return_value = mock_cadence
        mock_get_all.return_value = [] # No other MCCs
        
        before_save(mcc)
        
        # Verify that it selected the mapping with the apollo_id, ignoring the one without
        self.assertEqual(mcc.apollo_account, "Acc1")
        self.assertEqual(mcc.apollo_sequence_id, "seq123")
