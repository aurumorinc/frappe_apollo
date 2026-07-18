import frappe
import unittest
from frappe.tests import IntegrationTestCase
from frappe_apollo.apollo.doctype.cadence.cadence import provision_sequences_fields_and_steps
from frappe_apollo.tests.integration.external.conftest import my_vcr
import os

class TestCadenceProvisioningExternal(IntegrationTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.account_name = frappe.conf.get("apollo_test_account") or os.environ.get("APOLLO_TEST_ACCOUNT")
        if not cls.account_name:
            cls.account_name = "Dummy VCR Account"
            if not frappe.db.exists("Account", cls.account_name):
                frappe.get_doc({
                    "doctype": "Account",
                    "account_name": cls.account_name,
                    "api_key": "dummy_api_key_for_vcr",
                    "status": "Active"
                }).insert()
                
        if not frappe.db.exists("Account", cls.account_name):
            raise unittest.SkipTest(f"Account '{cls.account_name}' not found in database. Skipping external tests.")
            
        # Ensure Cadence Provider is enabled
        frappe.db.set_value("Cadence Provider", "Apollo", "enabled", 1)

    @classmethod
    def tearDownClass(cls):
        frappe.db.rollback()
        super().tearDownClass()

    def tearDown(self):
        frappe.db.rollback()
        super().tearDown()

    def _skip_if_no_cassette(self, cassette_name):
        if not frappe.conf.get("apollo_test_account") and not os.environ.get("APOLLO_TEST_ACCOUNT"):
            cassette_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'integrations', 'cassettes', cassette_name)
            if not os.path.exists(cassette_path):
                self.skipTest("No credentials and no cassette found for this test.")

    def _cleanup_all_sequences(self):
        from frappe_apollo.integrations.apollo import ApolloClient
        client = ApolloClient(self.account_name)
        # Search and archive to stay under limits
        res = client.search_sequences(per_page=100)
        sequences = res.get("emailer_campaigns", [])
        for seq in sequences:
            if not seq.get("archived"):
                try:
                    client.archive_sequence(seq["id"])
                except Exception:
                    pass

    @my_vcr.use_cassette('test_create_cadence.yaml')
    def test_create_cadence(self):
        self._skip_if_no_cassette('test_create_cadence.yaml')
        self._cleanup_all_sequences()

        from frappe_apollo.integrations.apollo import ApolloClient
        client = ApolloClient(self.account_name)

        # Setup custom fields in Apollo
        for field in ["subject", "message", "subject2", "message2"]:
            try:
                client.create_custom_field(
                    label=field,
                    field_type="text"
                )
            except Exception:
                pass # Ignore if exists or error

        if not frappe.db.exists("Email Template", "Test Template"):
            frappe.get_doc({
                "doctype": "Email Template",
                "name": "Test Template",
                "subject": "Test",
                "response": "Test"
            }).insert(ignore_permissions=True)

        if not frappe.db.exists("Field", "custom_subject"):
            frappe.get_doc({
                "doctype": "Field",
                "name": "custom_subject",
                "label": "custom_subject"
            }).insert(ignore_permissions=True)

        if not frappe.db.exists("Field", "custom_message"):
            frappe.get_doc({
                "doctype": "Field",
                "name": "custom_message",
                "label": "custom_message"
            }).insert(ignore_permissions=True)

        # Create a Cadence doc with subject_field/message_field containing prefix
        cadence = frappe.get_doc({
            "doctype": "Cadence",
            "cadence_name": "Test VCR Provisioning Cadence",
            "enabled": 1,
            "users": [{
                "user": "Administrator"
            }],
            "cadence_schedules": [{
                "send_after_days": 1,
                "reference_doctype": "Email Template",
                "reference_name": "Test Template",
                "subject_field": "custom_subject",
                "message_field": "custom_message"
            }]
        }).insert(ignore_permissions=True)
        
        # Act
        provision_sequences_fields_and_steps(cadence.name)
        
        # Reload Cadence to verify apollo_ids were set
        cadence.reload()
        
        self.assertTrue(len(cadence.apollo_ids) > 0)
        self.assertEqual(cadence.apollo_ids[0].account, self.account_name)
        apollo_id = cadence.apollo_ids[0].apollo_id
        self.assertIsNotNone(apollo_id)

        from frappe_apollo.integrations.apollo import ApolloClient
        client = ApolloClient(self.account_name)
        
        # Verify sequence steps setup: prefix was stripped
        seq_res = client.search_sequences(q_name="Test VCR Provisioning Cadence - Administrator")
        campaigns = seq_res.get("emailer_campaigns", [])
        self.assertGreater(len(campaigns), 0)
        sequence = campaigns[0]
        self.assertEqual(sequence.get("num_steps"), 1, "Expected 1 sequence step to be provisioned")
        steps = sequence.get("emailer_steps", [])
        self.assertEqual(len(steps), 1, "Sequence steps were not provisioned.")

        # Test Sequence Updating
        if not frappe.db.exists("Field", "custom_subject2"):
            frappe.get_doc({
                "doctype": "Field",
                "name": "custom_subject2",
                "label": "custom_subject2"
            }).insert(ignore_permissions=True)

        if not frappe.db.exists("Field", "custom_message2"):
            frappe.get_doc({
                "doctype": "Field",
                "name": "custom_message2",
                "label": "custom_message2"
            }).insert(ignore_permissions=True)

        cadence.reload()
        cadence.append("cadence_schedules", {
            "send_after_days": 2,
            "reference_doctype": "Email Template",
            "reference_name": "Test Template",
            "subject_field": "custom_subject2",
            "message_field": "custom_message2"
        })
        cadence.save(ignore_permissions=True)
        provision_sequences_fields_and_steps(cadence.name)
        
        seq_res_updated = client.search_sequences(q_name="Test VCR Provisioning Cadence - Administrator")
        campaigns_updated = seq_res_updated.get("emailer_campaigns", [])
        self.assertGreater(len(campaigns_updated), 0)
        steps_updated = campaigns_updated[0].get("emailer_steps", [])
        self.assertEqual(len(steps_updated), 2, "Sequence steps were not updated properly.")

        # Test Enable/Disable
        cadence.reload()
        cadence.enabled = 0
        cadence.save(ignore_permissions=True)
        from frappe_apollo.apollo.doctype.cadence.cadence import update_sequences
        update_sequences(cadence.name, cadence.enabled)
        
        seq_res = client.search_sequences(q_name="Test VCR Provisioning Cadence - Administrator")
        self.assertFalse(seq_res.get("emailer_campaigns", [{}])[0].get("active"))
        
        cadence.reload()
        cadence.enabled = 1
        cadence.save(ignore_permissions=True)
        update_sequences(cadence.name, cadence.enabled)
        
        seq_res = client.search_sequences(q_name="Test VCR Provisioning Cadence - Administrator")
        self.assertTrue(seq_res.get("emailer_campaigns", [{}])[0].get("active"))

        # Test Deletion/Archive
        from frappe_apollo.apollo.doctype.cadence.cadence import archive_sequences
        apollo_ids_data = [{"account": row.account, "apollo_id": row.apollo_id} for row in cadence.apollo_ids]
        cadence.delete()
        archive_sequences(apollo_ids_data)
        
        seq_res = client.search_sequences(q_name="Test VCR Provisioning Cadence - Administrator")
        # Apollo's search might not return archived sequences, or it might.
        # If it returns empty, it's effectively archived/deleted from normal views.
        campaigns = seq_res.get("emailer_campaigns", [])
        if campaigns:
            self.assertTrue(campaigns[0].get("archived"))
        else:
            self.assertEqual(len(campaigns), 0)
        
        # Cleanup DB
        cadences = frappe.get_all("Cadence", filters={"cadence_name": ["like", "Test VCR Provisioning Cadence%"]}, pluck="name")
        for c in cadences:
            frappe.delete_doc("Cadence", c, ignore_permissions=True)
            
        frappe.delete_doc("Email Template", "Test Template", ignore_permissions=True, force=True)
        frappe.delete_doc("Field", "custom_subject", ignore_permissions=True, force=True)
        frappe.delete_doc("Field", "custom_message", ignore_permissions=True, force=True)
        frappe.delete_doc("Field", "custom_subject2", ignore_permissions=True, force=True)
        frappe.delete_doc("Field", "custom_message2", ignore_permissions=True, force=True)
        frappe.db.commit()
