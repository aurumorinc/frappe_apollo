import frappe
from frappe.tests import UnitTestCase
from frappe_apollo.apollo.doctype.cadence_provider.cadence_provider import (
    ApolloCadenceProvider,
    async_sync_lead_and_assign_sequence,
    async_sync_communication_to_apollo,
)
from unittest.mock import patch, MagicMock

class TestApolloCadenceProvider(UnitTestCase):

    def get_mock_doc_side_effect(self, mock_mcc, mock_lead, mock_settings, mock_mailbox=None):
        def side_effect(*args, **kwargs):
            if args and isinstance(args[0], dict):
                if args[0].get("doctype") == "Sequence": return MagicMock()
                if args[0].get("doctype") == "Error Log": return MagicMock()
            if kwargs and kwargs.get("doctype") == "Sequence": return MagicMock()
            if kwargs and kwargs.get("doctype") == "Error Log": return MagicMock()

            doc_name = args[0] if args else kwargs.get("doctype")
            if doc_name == "Multi Channel Cadence": return mock_mcc
            if doc_name == "CRM Lead": return mock_lead
            if doc_name == "Apollo Settings": return mock_settings
            if doc_name == "Mailbox": return mock_mailbox
            return MagicMock()
        return side_effect
        mock_mcc = MagicMock()
        mock_mcc.name = "MCC-1"
        provider = ApolloCadenceProvider()
        provider.on_mcc_update(mock_mcc, "Draft", "Scheduled")
        
        mock_enqueue.assert_called_once_with(
            method="frappe_apollo.apollo.doctype.cadence_provider.cadence_provider.async_sync_lead_and_assign_sequence",
            queue="medium",
            mcc_name="MCC-1"
        )

    @patch("frappe_apollo.apollo.doctype.cadence_provider.cadence_provider.enqueue")
    def test_on_cadence_update(self, mock_enqueue):
        mock_doc = MagicMock()
        mock_doc.name = "Cadence-1"
        provider = ApolloCadenceProvider()
        provider.on_cadence_update(mock_doc)
        
        mock_enqueue.assert_called_once_with(
            method="frappe_apollo.apollo.doctype.sequence.sequence.on_cadence_update",
            queue="low",
            cadence_name="Cadence-1"
        )

    @patch("frappe_apollo.apollo.doctype.cadence_provider.cadence_provider.enqueue")
    def test_on_mcc_update_ignore_other_states(self, mock_enqueue):
        mock_mcc = MagicMock()
        provider = ApolloCadenceProvider()
        provider.on_mcc_update(mock_mcc, "Scheduled", "In Progress")
        mock_enqueue.assert_not_called()

    @patch("frappe_apollo.apollo.doctype.cadence_provider.cadence_provider.enqueue")
    def test_on_communication_update_to_scheduled(self, mock_enqueue):
        mock_comm = MagicMock()
        mock_comm.name = "Comm-1"
        provider = ApolloCadenceProvider()
        provider.on_communication_update(mock_comm, "Draft", "Scheduled")
        
        mock_enqueue.assert_called_once_with(
            method="frappe_apollo.apollo.doctype.cadence_provider.cadence_provider.async_sync_communication_to_apollo",
            queue="medium",
            comm_name="Comm-1"
        )

    @patch("frappe_apollo.apollo.doctype.cadence_provider.cadence_provider.wait_for_event")
    @patch("frappe.get_doc")
    @patch("frappe.db.get_value")
    @patch("frappe.log_error")
    def test_async_sync_lead_missing_mailbox_suspends(self, mock_log_error, mock_get_value, mock_get_doc, mock_wait):
        from frappe_controller.utils.controller import SuspendJob
        mock_wait.side_effect = SuspendJob("Suspended")
        
        mock_mcc = MagicMock()
        mock_mcc.recipient = "Lead-1"
        mock_mcc.sender = "user@example.com"
        
        mock_lead = MagicMock()
        mock_settings = MagicMock()
        mock_settings.enable = 1
        
        # Return MCC, Lead, Settings
        def mock_get_doc_side_effect(*args, **kwargs):
            if args and args[0] == "Multi Channel Cadence": return mock_mcc
            if args and args[0] == "CRM Lead": return mock_lead
            if args and args[0] == "Apollo Settings": return mock_settings
            return MagicMock()
        mock_get_doc.side_effect = mock_get_doc_side_effect
        
        # db.get_value for mailbox returns None
        mock_get_value.return_value = None
        
        with self.assertRaises(SuspendJob):
            async_sync_lead_and_assign_sequence("MCC-1")
            
        mock_wait.assert_called_with(
            event_key="doc:User Mailbox:after_insert",
            condition="argument.get('parent') == 'user@example.com'"
        )

    @patch("frappe_apollo.apollo.doctype.cadence_provider.cadence_provider.wait_for_event")
    @patch("frappe.get_all")
    @patch("frappe.get_doc")
    @patch("frappe.db.get_value")
    @patch("frappe.log_error")
    def test_async_sync_lead_missing_sequence_suspends(self, mock_log_error, mock_get_value, mock_get_doc, mock_get_all, mock_wait):
        from frappe_controller.utils.controller import SuspendJob
        mock_wait.side_effect = SuspendJob("Suspended")
        
        mock_mcc = MagicMock()
        mock_mcc.recipient = "Lead-1"
        mock_mcc.sender = "user@example.com"
        mock_mcc.cadence_name = "Cadence-1"
        
        mock_lead = MagicMock()
        mock_settings = MagicMock()
        mock_settings.enable = 1
        
        mock_mailbox = MagicMock()
        mock_mailbox.account = "Account-1"
        
        mock_get_doc.side_effect = self.get_mock_doc_side_effect(mock_mcc, mock_lead, mock_settings, locals().get("mock_mailbox"))
        mock_get_value.side_effect = ["Mailbox-1", "people-1"]
        
        # Return empty list for Sequence
        mock_get_all.return_value = []
        
        with self.assertRaises(SuspendJob):
            async_sync_lead_and_assign_sequence("MCC-1")
            
        mock_wait.assert_called_with(
            event_key="doc:Sequence:after_insert",
            condition="argument.get('cadence') == 'Cadence-1' and argument.get('account') == 'Account-1'"
        )

    @patch("frappe_apollo.apollo.doctype.cadence_provider.cadence_provider.ApolloClient")
    @patch("frappe.get_all")
    @patch("frappe.get_doc")
    @patch("frappe.db.get_value")
    def test_async_sync_lead_rate_limit_bubbles_up(self, mock_get_value, mock_get_doc, mock_get_all, mock_client_cls):
        from frappe_apollo.integrations.apollo import ApolloRateLimitError
        
        mock_mcc = MagicMock()
        mock_mcc.recipient = "Lead-1"
        mock_mcc.sender = "user@example.com"
        mock_mcc.cadence_name = "Cadence-1"
        
        mock_lead = MagicMock()
        mock_settings = MagicMock()
        mock_settings.enable = 1
        
        mock_mailbox = MagicMock()
        mock_mailbox.account = "Account-1"
        mock_mailbox.id = "mailbox-1"
        
        mock_get_doc.side_effect = self.get_mock_doc_side_effect(mock_mcc, mock_lead, mock_settings, locals().get("mock_mailbox"))
        mock_get_value.side_effect = ["Mailbox-1", "people-1"]
        
        mock_seq = MagicMock()
        mock_seq.id = "seq-1"
        mock_get_all.return_value = [mock_seq]
        
        mock_client = mock_client_cls.return_value
        mock_client.add_contacts_to_sequence.side_effect = ApolloRateLimitError("Rate Limited")
        
        with self.assertRaises(ApolloRateLimitError):
            async_sync_lead_and_assign_sequence("MCC-1")

    @patch("frappe_apollo.apollo.doctype.cadence_provider.cadence_provider.ApolloClient")
    @patch("frappe.get_doc")
    def test_async_sync_communication_idempotent(self, mock_get_doc, mock_client_cls):
        mock_comm = MagicMock()
        mock_comm.get.return_value = "Synced"
        mock_get_doc.return_value = mock_comm
        
        # Should return early
        async_sync_communication_to_apollo("Comm-1")
        mock_client_cls.assert_not_called()

    @patch("frappe_apollo.apollo.doctype.cadence_provider.cadence_provider.wait_for_event")
    @patch("frappe.get_all")
    @patch("frappe.get_doc")
    @patch("frappe.db.get_value")
    @patch("frappe.log_error")
    def test_async_sync_communication_missing_people_suspends(self, mock_log_error, mock_get_value, mock_get_doc, mock_get_all, mock_wait):
        from frappe_controller.utils.controller import SuspendJob
        mock_wait.side_effect = SuspendJob("Suspended")

        mock_comm = MagicMock()
        mock_comm.get.return_value = None
        mock_comm.reference_name = "MCC-1"

        mock_mcc = MagicMock()
        mock_mcc.recipient = "Lead-1"
        mock_mcc.sender = "user@example.com"
        mock_mcc.cadence_name = "Cadence-1"

        mock_settings = MagicMock()
        mock_settings.enable = 1

        mock_mailbox = MagicMock()
        mock_mailbox.account = "Account-1"

        def mock_get_doc_side_effect(*args, **kwargs):
            doc_name = args[0] if args else kwargs.get("doctype")
            if doc_name == "Communication": return mock_comm
            if doc_name == "Multi Channel Cadence": return mock_mcc
            if doc_name == "Apollo Settings": return mock_settings
            if doc_name == "Mailbox": return mock_mailbox
            return MagicMock()
            
        mock_get_doc.side_effect = mock_get_doc_side_effect

        def mock_get_value_side_effect(*args, **kwargs):
            if args[0] == "User Mailbox": return "Mailbox-1"
            if args[0] == "People": return None # Trigger suspend
            return None
        mock_get_value.side_effect = mock_get_value_side_effect

        mock_seq = MagicMock()
        mock_seq.name = "Seq-1"
        mock_get_all.return_value = [mock_seq]

        with self.assertRaises(SuspendJob):
            async_sync_communication_to_apollo("Comm-1")

        mock_wait.assert_called_with(
            event_key="doc:People:after_insert",
            condition="argument.get('lead') == 'Lead-1' and argument.get('account') == 'Account-1'"
        )

    @patch("frappe.get_all")
    @patch("frappe.get_doc")
    @patch("frappe.db.get_value")
    @patch("frappe.log_error")
    def test_async_sync_communication_missing_custom_fields(self, mock_log_error, mock_get_value, mock_get_doc, mock_get_all):
        mock_comm = MagicMock()
        mock_comm.get.return_value = None
        mock_comm.reference_name = "MCC-1"
        mock_comm.content = "Content"
        mock_comm.subject = "Subject"
        mock_comm.cadence_schedule = "Sch-1"

        mock_mcc = MagicMock()
        mock_mcc.recipient = "Lead-1"
        mock_mcc.sender = "user@example.com"
        mock_mcc.cadence_name = "Cadence-1"

        mock_settings = MagicMock()
        mock_settings.enable = 1

        mock_mailbox = MagicMock()
        mock_mailbox.account = "Account-1"

        mock_cadence = MagicMock()
        mock_sch = MagicMock()
        mock_sch.name = "Sch-1"
        mock_cadence.cadence_schedules = [mock_sch]

        mock_seq_doc = MagicMock()
        mock_step = MagicMock()
        mock_step.subject_custom_field_id = None
        mock_step.response_custom_field_id = None
        mock_seq_doc.sequence_steps = [mock_step]

        def mock_get_doc_side_effect(*args, **kwargs):
            doc_name = args[0] if args else kwargs.get("doctype")
            if doc_name == "Communication": return mock_comm
            if doc_name == "Multi Channel Cadence": return mock_mcc
            if doc_name == "Apollo Settings": return mock_settings
            if doc_name == "Mailbox": return mock_mailbox
            if doc_name == "Cadence": return mock_cadence
            if doc_name == "Sequence": return mock_seq_doc
            return MagicMock()
            
        mock_get_doc.side_effect = mock_get_doc_side_effect

        def mock_get_value_side_effect(*args, **kwargs):
            if args[0] == "User Mailbox": return "Mailbox-1"
            if args[0] == "People": return "people-1"
            return None
        mock_get_value.side_effect = mock_get_value_side_effect

        mock_seq = MagicMock()
        mock_seq.name = "Seq-1"
        mock_get_all.return_value = [mock_seq]

        # Should return early gracefully (no exception, no wait, just log_error)
        async_sync_communication_to_apollo("Comm-1")

        mock_log_error.assert_called_with("Missing custom field IDs in Apollo sequence step")
