import frappe
from frappe.tests import UnitTestCase
from frappe_apollo.apollo.doctype.sequence.sequence import Sequence, provision_custom_field, on_cadence_update
from unittest.mock import patch, MagicMock

class TestSequence(UnitTestCase):

    @patch("frappe_apollo.apollo.doctype.sequence.sequence.frappe.get_all")
    @patch("frappe_apollo.apollo.doctype.sequence.sequence.frappe.get_doc")
    def test_on_cadence_update(self, mock_get_doc, mock_get_all):
        mock_get_all.return_value = ["Seq-1", "Seq-2"]
        mock_seq_1 = MagicMock()
        mock_seq_2 = MagicMock()
        mock_get_doc.side_effect = [mock_seq_1, mock_seq_2]
        
        on_cadence_update("Cadence-1")
        
        mock_get_all.assert_called_once_with("Sequence", filters={"cadence": "Cadence-1"}, pluck="name")
        mock_seq_1._populate_sequence_steps.assert_called_once()
        mock_seq_1.save.assert_called_once_with(ignore_permissions=True)
        mock_seq_2._populate_sequence_steps.assert_called_once()
        mock_seq_2.save.assert_called_once_with(ignore_permissions=True)

    @patch("frappe.get_doc")
    def test_populate_sequence_steps(self, mock_get_doc):
        # Create a mock cadence with 3 email schedules and 1 other schedule
        mock_cadence = MagicMock()
        mock_schedule_1 = MagicMock(reference_doctype="Email Template")
        mock_schedule_2 = MagicMock(reference_doctype="Email Template")
        mock_schedule_3 = MagicMock(reference_doctype="SMS Template")
        mock_cadence.get.return_value = [mock_schedule_1, mock_schedule_2, mock_schedule_3]
        mock_get_doc.return_value = mock_cadence

        # Our sequence initially has 0 steps
        seq = Sequence({"doctype": "Sequence"})
        seq.cadence = "Cadence-1"
        seq.sequence_steps = []
        seq.save = MagicMock()

        seq._populate_sequence_steps()

        # Should add 2 steps because there are 2 email schedules
        self.assertEqual(len(seq.sequence_steps), 2)
        seq.save.assert_called_once()

    @patch("frappe_apollo.apollo.doctype.sequence.sequence.enqueue")
    def test_enqueue_provision_custom_fields(self, mock_enqueue):
        seq = Sequence({"doctype": "Sequence"})
        seq.name = "Seq-1"
        
        step_1 = MagicMock()
        step_1.subject_custom_field_id = "sub-1"
        step_1.response_custom_field_id = None
        
        step_2 = MagicMock()
        step_2.subject_custom_field_id = None
        step_2.response_custom_field_id = None

        seq.sequence_steps = [step_1, step_2]

        seq._enqueue_provision_custom_fields()

        # step_1 needs response, step_2 needs subject & response -> 3 calls
        self.assertEqual(mock_enqueue.call_count, 3)

        # check what was enqueued
        calls = mock_enqueue.call_args_list
        self.assertEqual(calls[0][1]["field_type"], "response")
        self.assertEqual(calls[0][1]["step_idx"], 1)

        self.assertEqual(calls[1][1]["field_type"], "subject")
        self.assertEqual(calls[1][1]["step_idx"], 2)

        self.assertEqual(calls[2][1]["field_type"], "response")
        self.assertEqual(calls[2][1]["step_idx"], 2)

    @patch("frappe_apollo.integrations.apollo.ApolloClient")
    @patch("frappe.get_doc")
    @patch("frappe.db.get_value")
    def test_provision_custom_field_skip_existing(self, mock_get_value, mock_get_doc, mock_client_cls):
        mock_get_value.return_value = "existing-field-id"

        mock_seq = MagicMock()
        mock_step = MagicMock()
        mock_seq.sequence_steps = [mock_step]
        mock_get_doc.return_value = mock_seq

        # Should return existing field ID and set it on the step
        field_id = provision_custom_field("Seq-1", 1, "subject")
        self.assertEqual(field_id, "existing-field-id")
        mock_step.db_set.assert_called_once_with("subject_custom_field_id", "existing-field-id")

    @patch("frappe_apollo.integrations.apollo.ApolloClient")
    @patch("frappe.get_doc")
    @patch("frappe.db.get_value")
    def test_provision_custom_field_creates_new(self, mock_get_value, mock_get_doc, mock_client_cls):
        mock_get_value.return_value = None

        mock_seq = MagicMock()
        mock_seq.id = "seq-123"
        mock_seq.account = "Acc-1"
        mock_step = MagicMock()
        mock_seq.sequence_steps = [mock_step]
        
        # We need mock_get_doc to return mock_seq for the "Sequence" get,
        # and a MagicMock for the "Field" get (where it does .insert())
        mock_field_doc = MagicMock()
        
        def mock_get_doc_side_effect(*args, **kwargs):
            if args and isinstance(args[0], str) and args[0] == "Sequence":
                return mock_seq
            if args and isinstance(args[0], dict) and args[0].get("doctype") == "Field":
                return mock_field_doc
            if kwargs and kwargs.get("doctype") == "Field":
                return mock_field_doc
            return MagicMock()
            
        mock_get_doc.side_effect = mock_get_doc_side_effect

        mock_client = mock_client_cls.return_value
        mock_client.create_custom_field.return_value = {
            "typed_custom_fields": [{"id": "new-field-id"}]
        }

        field_id = provision_custom_field("Seq-1", 1, "response")
        
        # Verify client called correctly
        mock_client.create_custom_field.assert_called_once_with(
            "Seq seq-123 Step 1 Body", "textarea"
        )
        # Verify field was created in Frappe
        mock_field_doc.insert.assert_called_once()
        # Verify step was updated
        mock_step.db_set.assert_called_once_with("response_custom_field_id", "new-field-id")
        
        self.assertEqual(field_id, "new-field-id")
