import frappe
from frappe.tests import IntegrationTestCase

class TestSequenceIntegration(IntegrationTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        frappe.db.delete("Sequence")
        frappe.db.delete("Cadence")
        frappe.db.delete("Cadence Provider")
        frappe.db.delete("Multi Channel Cadence")
        
        # Create a Cadence
        cls.cadence = frappe.get_doc({
            "doctype": "Cadence",
            "cadence_name": "Test Decoupled Cadence"
        }).insert(ignore_permissions=True, ignore_if_duplicate=True)
        
        account_name = frappe.db.get_value("Account", None, "name")
        if not account_name:
            account = frappe.get_doc({
                "doctype": "Account",
                "account_name": "Dummy Account"
            }).insert(ignore_permissions=True, ignore_if_duplicate=True)
            account_name = account.name

        # Create a Sequence related to the Cadence
        cls.sequence = frappe.get_doc({
            "doctype": "Sequence",
            "cadence": cls.cadence.name,
            "account": account_name,
            "sender": frappe.session.user,
            "id": "seq-apollo-123"
        }).insert(ignore_permissions=True, ignore_if_duplicate=True)

        # Ensure Apollo Cadence Provider is enabled
        if not frappe.db.exists("Cadence Provider", "Apollo"):
            frappe.get_doc({
                "doctype": "Cadence Provider",
                "provider_name": "Apollo",
                "enabled": 1
            }).insert(ignore_permissions=True)
        else:
            frappe.db.set_value("Cadence Provider", "Apollo", "enabled", 1)

        # Create a Dummy Email Template
        if not frappe.db.exists("Email Template", "Dummy Email"):
            frappe.get_doc({
                "doctype": "Email Template",
                "name": "Dummy Email",
                "subject": "Hello",
                "response": "World"
            }).insert(ignore_permissions=True, ignore_if_duplicate=True)

    @classmethod
    def tearDownClass(cls):
        frappe.db.rollback()
        super().tearDownClass()

    def test_cadence_update_populates_sequence(self):
        # Initial check
        self.sequence.reload()
        self.assertEqual(len(self.sequence.sequence_steps), 0)
        
        # Add a schedule to the Cadence
        self.cadence.append("cadence_schedules", {
            "reference_doctype": "Email Template",
            "reference_name": "Dummy Email",
            "send_after_days": 1
        })
        self.cadence.save(ignore_permissions=True)
        
        # Trigger on_update to broadcast events (which enqueues the job)
        self.cadence.on_update()
        
        # We need to manually execute the enqueued jobs since we are in a test
        # But wait, enqueued jobs might be complex to execute manually in IntegrationTest.
        # Alternatively, we can just call the broadcast_event directly, or on_cadence_update.
        
        # Let's call the newly decoupled module level function to simulate the worker
        from frappe_cadence.cadence.doctype.cadence_provider.cadence_provider import on_cadence_update
        on_cadence_update(self.cadence)
        
        # Then, Apollo Cadence Provider will enqueue another job `on_cadence_update` in sequence.py
        from frappe_apollo.apollo.doctype.sequence.sequence import on_cadence_update as seq_on_cadence_update
        seq_on_cadence_update(self.cadence.name)
        
        # Check if the Sequence has been updated
        self.sequence.reload()
        self.assertEqual(len(self.sequence.sequence_steps), 1)
