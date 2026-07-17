import frappe
from frappe.tests import IntegrationTestCase
from frappe_apollo.apollo.doctype.field.field import create_a_field
from frappe_controller.utils.controller import SuspendJob
from unittest.mock import patch, MagicMock

class TestFieldIntegration(IntegrationTestCase):
    @patch("frappe.db.get_value")
    def test_settings_disabled_raises_suspend(self, mock_get_value):
        mock_get_value.return_value = 0
        
        with self.assertRaises(SuspendJob):
            create_a_field("TestField")
            
    @patch("frappe.get_doc")
    @patch("frappe_apollo.integrations.apollo.ApolloClient")
    @patch("frappe.db.get_value")
    def test_create_field_success(self, mock_get_value, mock_client_class, mock_get_doc):
        mock_get_value.return_value = 1
        
        mock_field = MagicMock()
        mock_field.apollo_id = None
        mock_field.label = "Test Label"
        mock_field.field_type = "string"
        mock_field.account = "Test Account"
        
        mock_account = MagicMock()
        mock_account.status = "Active"
        
        def mock_get_doc_side_effect(doctype, name):
            if doctype == "Field": return mock_field
            if doctype == "Account": return mock_account
            return MagicMock()
            
        mock_get_doc.side_effect = mock_get_doc_side_effect
        
        mock_client = MagicMock()
        mock_client.create_field.return_value = {"typed_custom_fields": [{"id": "apollo_123"}]}
        mock_client_class.return_value = mock_client
        
        create_a_field("TestField")
        
        mock_client.create_field.assert_called_once_with("Test Label", "string")
        mock_field.db_set.assert_called_once_with("apollo_id", "apollo_123")
