import frappe
from frappe.tests import UnitTestCase
from frappe_apollo.overrides.communication import update_contact
from unittest.mock import patch, MagicMock

class TestCommunicationOverride(UnitTestCase):

    @patch("frappe.get_doc")
    def test_idempotency(self, mock_get_doc):
        mock_comm = MagicMock()
        mock_comm.get.return_value = "Synced"
        mock_get_doc.return_value = mock_comm
        
        # Should return early
        update_contact("Comm-1")
        # Ensure it didn't call get_doc for anything else (e.g. MCC)
        self.assertEqual(mock_get_doc.call_count, 1)

    @patch("frappe_controller.utils.controller.wait_for_event")
    @patch("frappe.get_doc")
    @patch("frappe.db.get_value")
    def test_wait_state_settings(self, mock_get_value, mock_get_doc, mock_wait):
        from frappe_controller.utils.controller import SuspendJob
        mock_wait.side_effect = SuspendJob("Suspended")

        mock_comm = MagicMock()
        mock_comm.get.return_value = None
        
        mock_mcc = MagicMock()
        mock_settings = MagicMock()
        mock_settings.enable = 0

        # Return Sequence: Comm, MCC, Settings
        mock_get_doc.side_effect = [mock_comm, mock_mcc]
        mock_get_value.return_value = 0

        with self.assertRaises(SuspendJob):
            update_contact("Comm-1")

        mock_wait.assert_called_once_with(
            event_key="doc:Cadence Provider:on_update:Apollo",
            condition="argument.get('enabled') == 1"
        )

    @patch("frappe_controller.utils.controller.wait_for_event")
    @patch("frappe.db.get_value")
    @patch("frappe.get_doc")
    def test_wait_state_mailbox(self, mock_get_doc, mock_get_value, mock_wait):
        from frappe_controller.utils.controller import SuspendJob
        mock_wait.side_effect = SuspendJob("Suspended")

        mock_comm = MagicMock()
        mock_comm.get.return_value = None
        
        mock_mcc = MagicMock()
        mock_mcc.sender = "user@example.com"
        
        mock_get_doc.side_effect = [mock_comm, mock_mcc]
        
        def mock_get_value_side_effect(*args, **kwargs):
            if args[0] == "Cadence Provider": return 1
            if args[0] == "User Mailbox": return None
            return None
        mock_get_value.side_effect = mock_get_value_side_effect

        with self.assertRaises(SuspendJob):
            update_contact("Comm-1")

        mock_wait.assert_called_once_with(
            event_key="doc:User Mailbox:after_insert",
            condition="argument.get('parent') == 'user@example.com'"
        )

    @patch("frappe_controller.utils.controller.wait_for_event")
    @patch("frappe.get_all")
    @patch("frappe.db.get_value")
    @patch("frappe.get_doc")
    def test_wait_state_sequence(self, mock_get_doc, mock_get_value, mock_get_all, mock_wait):
        from frappe_controller.utils.controller import SuspendJob
        mock_wait.side_effect = SuspendJob("Suspended")

        mock_comm = MagicMock()
        mock_comm.get.return_value = None
        
        mock_mcc = MagicMock()
        mock_mcc.sender = "user@example.com"
        mock_mcc.campaign_name = "Camp-1"
        
        mock_mailbox = MagicMock()
        mock_mailbox.account = "Acc-1"

        mock_get_doc.side_effect = [mock_comm, mock_mcc, mock_mailbox]
        mock_get_value.side_effect = [1, "Mailbox-1"] # Cadence Provider -> enabled, User Mailbox -> Mailbox ID
        
        mock_get_all.return_value = [] # Sequence not found

        with self.assertRaises(SuspendJob):
            update_contact("Comm-1")

        mock_wait.assert_called_once_with(
            event_key="doc:Sequence:after_insert",
            condition="argument.get('campaign') == 'Camp-1' and argument.get('account') == 'Acc-1'"
        )

    @patch("frappe_controller.utils.controller.wait_for_event")
    @patch("frappe.get_all")
    @patch("frappe.db.get_value")
    @patch("frappe.get_doc")
    def test_wait_state_people(self, mock_get_doc, mock_get_value, mock_get_all, mock_wait):
        from frappe_controller.utils.controller import SuspendJob
        mock_wait.side_effect = SuspendJob("Suspended")

        mock_comm = MagicMock()
        mock_comm.get.return_value = None
        
        mock_mcc = MagicMock()
        mock_mcc.sender = "user@example.com"
        mock_mcc.campaign_name = "Camp-1"
        mock_mcc.recipient = "Lead-1"
        
        mock_mailbox = MagicMock()
        mock_mailbox.account = "Acc-1"
        
        mock_seq_doc = MagicMock()

        mock_get_doc.side_effect = [mock_comm, mock_mcc, mock_mailbox, mock_seq_doc]
        
        # First call gets mailbox, second call gets people
        def mock_get_value_side_effect(*args, **kwargs):
            if args[0] == "Cadence Provider":
                return 1
            if args[0] == "User Mailbox":
                return "Mailbox-1"
            if args[0] == "People":
                return None
            return None
            
        mock_get_value.side_effect = mock_get_value_side_effect
        
        mock_get_all.return_value = [MagicMock(name="Seq-1")] # Sequence found

        with self.assertRaises(SuspendJob):
            update_contact("Comm-1")

        mock_wait.assert_called_once_with(
            event_key="doc:People:after_insert",
            condition="argument.get('lead') == 'Lead-1' and argument.get('account') == 'Acc-1'"
        )

    @patch("frappe_controller.utils.controller.emit_event")
    @patch("frappe_apollo.integrations.apollo.ApolloClient")
    @patch("frappe.get_all")
    @patch("frappe.db.get_value")
    @patch("frappe.get_doc")
    def test_success_and_state_machine_emission(self, mock_get_doc, mock_get_value, mock_get_all, mock_client_cls, mock_emit):
        mock_comm = MagicMock()
        mock_comm.get.return_value = None
        mock_comm.content = "content"
        mock_comm.subject = "subject"
        
        mock_mcc = MagicMock()
        mock_mcc.name = "MCC-1"
        mock_mcc.sender = "user@example.com"
        mock_mcc.campaign_name = "Camp-1"
        mock_mcc.recipient = "Lead-1"
        mock_mcc.get.return_value = 1 # step_idx
        
        mock_mailbox = MagicMock()
        mock_mailbox.account = "Acc-1"
        
        mock_step = MagicMock()
        mock_step.subject_custom_field_id = "sf-1"
        mock_step.response_custom_field_id = "rf-1"
        
        mock_seq_doc = MagicMock()
        mock_seq_doc.sequence_steps = [mock_step]

        mock_get_doc.side_effect = [mock_comm, mock_mcc, mock_mailbox, mock_seq_doc]
        
        def mock_get_value_side_effect(*args, **kwargs):
            if args[0] == "Cadence Provider": return 1
            if args[0] == "User Mailbox":
                return "Mailbox-1"
            if args[0] == "People":
                return "person-id-1"
            return None
            
        mock_get_value.side_effect = mock_get_value_side_effect
        
        mock_get_all.return_value = [MagicMock(name="Seq-1")]

        mock_client = mock_client_cls.return_value

        update_contact("Comm-1")

        mock_client.update_contact.assert_called_once_with(
            "person-id-1",
            {"sf-1": "subject", "rf-1": "content"}
        )
        
        mock_emit.assert_called_once_with("communication_scheduled", {
            "campaign_name": "Camp-1",
            "step_idx": 1,
            "mcc": "MCC-1"
        })
        
        self.assertEqual(mock_comm.apollo_sync_status, "Synced")
        mock_comm.save.assert_called_once_with(ignore_permissions=True)
