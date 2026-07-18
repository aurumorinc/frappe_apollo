import frappe
from frappe.tests import UnitTestCase
from frappe_apollo.apollo.doctype.cadence.cadence import _provision_sequences, _setup_sequence_steps
from unittest.mock import patch, MagicMock

class TestCadenceProvisioning(UnitTestCase):
    @patch("frappe_apollo.apollo.doctype.cadence.cadence.ApolloClient")
    @patch("frappe.get_doc")
    @patch("frappe.get_all")
    def test_provision_sequences(self, mock_get_all, mock_get_doc, mock_client_cls):
        mock_cadence = MagicMock()
        mock_cadence.cadence_name = "Test Cadence"
        mock_user = MagicMock()
        mock_user.user = "test@example.com"
        mock_cadence.users = [mock_user]
        mock_cadence.get.return_value = [mock_user]
        mock_cadence.apollo_ids = []
        
        mock_get_doc.return_value = mock_cadence
        mock_get_all.return_value = ["Account1"]
        
        mock_client = mock_client_cls.return_value
        mock_client.create_sequence.return_value = "seq_123"
        
        _provision_sequences("Cad1")
        
        mock_client.create_sequence.assert_called_once_with(
            name="Test Cadence - test@example.com",
            permissions="team_can_use",
            active=True
        )
        mock_cadence.append.assert_called_once_with("apollo_ids", {
            "account": "Account1",
            "sender": "test@example.com",
            "apollo_id": "seq_123",
            "status": "Active"
        })
        mock_cadence.save.assert_called_once_with(ignore_permissions=True)

    @patch("frappe_apollo.apollo.doctype.cadence.cadence.ApolloClient")
    @patch("frappe.get_doc")
    def test_setup_sequence_steps(self, mock_get_doc, mock_client_cls):
        mock_cadence = MagicMock()
        mock_cadence.name = "Cad1"
        
        mock_sch1 = MagicMock()
        mock_sch1.send_after_days = 2
        mock_sch1.reference_doctype = "Email Template"
        mock_sch1.name = "step1"
        mock_sch1.get.side_effect = lambda k: "lbl_subject_step1" if k == "subject_field" else "lbl_message_step1"
        
        mock_sch2 = MagicMock()
        mock_sch2.send_after_days = 3
        mock_sch2.reference_doctype = "Other Channel"
        mock_sch2.name = "step2"
        
        mock_sch3 = MagicMock()
        mock_sch3.send_after_days = 1
        mock_sch3.reference_doctype = "Email Template"
        mock_sch3.name = "step3"
        mock_sch3.get.side_effect = lambda k: "lbl_subject_step3" if k == "subject_field" else "lbl_message_step3"
        
        mock_cadence.cadence_schedules = [mock_sch1, mock_sch2, mock_sch3]
        mock_cadence.apollo_ids = [MagicMock(apollo_id="seq_123", status="Active", account="Account1")]
        mock_cadence.get.side_effect = lambda k: mock_cadence.cadence_schedules if k == "cadence_schedules" else mock_cadence.apollo_ids
        
        mock_get_doc.return_value = mock_cadence
        
        mock_client = mock_client_cls.return_value
        
        _setup_sequence_steps("Cad1")
        
        # Verify accumulated wait
        # Step1: Wait = 2
        # Step2: Other channel (wait = 3)
        # Step3: Email (wait = 1 + 3 = 4)
        
        expected_emailer_steps = [
            {
                "type": "auto_email",
                "wait_time": 2,
                "wait_mode": "day",
                "emailer_touches": [{
                    "type": "auto_email",
                    "include_signature": True,
                    "emailer_template": {
                        "subject": "{{lbl_subject_step1}}",
                        "body_html": "{{lbl_message_step1}}"
                    }
                }]
            },
            {
                "type": "auto_email",
                "wait_time": 4, # 3 from Other Channel + 1 from Email Template
                "wait_mode": "day",
                "emailer_touches": [{
                    "type": "auto_email",
                    "include_signature": True,
                    "emailer_template": {
                        "subject": "{{lbl_subject_step3}}",
                        "body_html": "{{lbl_message_step3}}"
                    }
                }]
            }
        ]
        
        mock_client.update_sequence.assert_called_once_with(
            "seq_123",
            {"emailer_steps": expected_emailer_steps}
        )
