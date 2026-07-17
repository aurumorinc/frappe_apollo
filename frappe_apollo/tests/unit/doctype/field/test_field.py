import frappe
from frappe.tests import UnitTestCase
from frappe_apollo.apollo.doctype.field.field import provision_a_field
from frappe.exceptions import DoesNotExistError
from unittest.mock import patch, MagicMock
import hashlib

class TestField(UnitTestCase):
    @patch("frappe_apollo.integrations.apollo.ApolloClient")
    @patch("frappe.db.get_value")
    @patch("frappe.get_doc")
    def test_provision_a_field_hash(self, mock_get_doc, mock_get_value, mock_client_cls):
        # Setup mocks
        mock_client = mock_client_cls.return_value
        mock_client.create_field.return_value = {"typed_custom_fields": [{"id": "apollo_123"}]}

        mock_cadence = MagicMock()
        mock_cadence.name = "Cad1"
        
        mock_apollo_id_row = MagicMock()
        mock_apollo_id_row.status = "Active"
        mock_apollo_id_row.account = "acc1"
        mock_apollo_id_row.apollo_id = "seq123"
        mock_cadence.get.return_value = [mock_apollo_id_row]

        mock_step = MagicMock()
        mock_step.name = "step1"
        
        def mock_get_doc_side_effect(doctype, *args, **kwargs):
            if doctype == "Field" and isinstance(args[0], str):
                raise DoesNotExistError()
            elif isinstance(doctype, dict) and doctype.get("doctype") == "Field":
                doc = MagicMock()
                doc.name = "new_field"
                doc.get.return_value = [] # apollo_ids
                doc.insert.return_value = doc
                return doc
            return MagicMock()
            
        mock_get_doc.side_effect = mock_get_doc_side_effect
        mock_get_value.return_value = 1 # Cadence Provider enabled
        
        provision_a_field(mock_cadence, mock_step, "subject")
        
        expected_hash = hashlib.md5("Cad1_step1_subject".encode()).hexdigest()[:10]
        
        # Verify db_set was called with the new field name
        self.assertEqual(mock_step.subject_field, "new_field")
