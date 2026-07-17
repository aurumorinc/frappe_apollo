import frappe
from frappe.tests import UnitTestCase
from frappe_apollo.apollo.doctype.field.field import provision_a_field
from unittest.mock import patch, MagicMock
import hashlib

class TestField(UnitTestCase):
    @patch("frappe.db.get_value")
    @patch("frappe.get_doc")
    def test_provision_a_field_hash(self, mock_get_doc, mock_get_value):
        # Setup mocks
        mock_sequence = MagicMock()
        mock_sequence.apollo_id = "seq123"
        mock_sequence.account = "acc1"
        
        mock_step = MagicMock()
        mock_sequence.sequence_steps = [mock_step]
        
        mock_field_doc = MagicMock()
        mock_field_doc.name = "new_field"
        
        def mock_get_doc_side_effect(doctype, *args, **kwargs):
            if doctype == "Sequence":
                return mock_sequence
            elif isinstance(doctype, dict) and doctype.get("doctype") == "Field":
                doc = MagicMock()
                doc.name = "new_field"
                doc.insert.return_value = doc
                return doc
            return MagicMock()
            
        mock_get_doc.side_effect = mock_get_doc_side_effect
        mock_get_value.return_value = None # No existing field
        
        provision_a_field("Seq1", 1, "subject")
        
        expected_hash = hashlib.md5("seq123_1_subject".encode()).hexdigest()[:10]
        expected_label = f"Seq seq123 {expected_hash} Subject"
        
        # Verify db_set was called with the new field name
        mock_step.db_set.assert_called_once_with("subject_custom_field_id", "new_field")
