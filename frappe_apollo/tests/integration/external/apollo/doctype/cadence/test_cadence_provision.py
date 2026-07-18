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

    @my_vcr.use_cassette('test_auto_provision_sequence.yaml')
    def test_provision_sequences_fields_and_steps_live(self):
        import os
        if not frappe.conf.get("apollo_test_account") and not os.environ.get("APOLLO_TEST_ACCOUNT"):
            # Check if cassette exists, if not, skip
            cassette_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'integrations', 'cassettes', 'test_auto_provision_sequence.yaml')
            if not os.path.exists(cassette_path):
                self.skipTest("No credentials and no cassette found for this test.")

        if not frappe.db.exists("Email Template", "Test Template"):
            frappe.get_doc({
                "doctype": "Email Template",
                "name": "Test Template",
                "subject": "Test",
                "response": "Test"
            }).insert(ignore_permissions=True)

        # Create a Cadence doc
        cadence = frappe.get_doc({
            "doctype": "Cadence",
            "cadence_name": "Test VCR Provisioning Cadence",
            "users": [{
                "user": "Administrator"
            }],
            "cadence_schedules": [{
                "send_after_days": 1,
                "reference_doctype": "Email Template",
                "reference_name": "Test Template"
            }]
        }).insert(ignore_permissions=True)
        
        # Act
        provision_sequences_fields_and_steps(cadence.name)
        
        # Reload Cadence to verify apollo_ids were set
        cadence.reload()
        
        self.assertTrue(len(cadence.apollo_ids) > 0)
        self.assertEqual(cadence.apollo_ids[0].account, self.account_name)
        self.assertIsNotNone(cadence.apollo_ids[0].apollo_id)
