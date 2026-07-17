import frappe
from frappe.tests import IntegrationTestCase
from unittest.mock import patch, MagicMock
from frappe_apollo.apollo.doctype.mailbox.mailbox import queue_get_mailboxes, get_mailboxes

class TestMailboxIntegration(IntegrationTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        frappe.db.sql("DELETE FROM `tabAccount` WHERE name = 'Mailbox Test Account'")
        frappe.db.sql("DELETE FROM `tabMailbox` WHERE account = 'Mailbox Test Account'")
        
        frappe.get_doc({
            "doctype": "Account",
            "account_name": "Mailbox Test Account",
            "api_key": "some_key"
        }).insert(ignore_permissions=True)

    @classmethod
    def tearDownClass(cls):
        frappe.db.rollback()
        super().tearDownClass()

    @patch("frappe.enqueue")
    def test_queue_get_mailboxes(self, mock_enqueue):
        queue_get_mailboxes()
        # Should enqueue one or more jobs depending on total accounts, but at least for our Test Account
        found = False
        for call in mock_enqueue.call_args_list:
            if call[1].get("account_name") == "Mailbox Test Account":
                found = True
                break
        self.assertTrue(found, "get_mailboxes was not queued for Mailbox Test Account")

    @patch("frappe_apollo.integrations.apollo.ApolloClient")
    def test_get_mailboxes(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.get_email_accounts.return_value = {
            "email_accounts": [
                {
                    "id": "mailbox_id_1",
                    "email": "test1@example.com",
                    "active": True
                },
                {
                    "id": "mailbox_id_2",
                    "email": "test2@example.com",
                    "active": False
                }
            ]
        }

        get_mailboxes("Mailbox Test Account")

        mock_client.get_email_accounts.assert_called_once()

        mailboxes = frappe.get_all("Mailbox", filters={"account": "Mailbox Test Account"}, fields=["email_id", "apollo_id"])
        self.assertEqual(len(mailboxes), 1)
        
        # Verify properties
        m1 = next(m for m in mailboxes if m.apollo_id == "mailbox_id_1")
        self.assertEqual(m1.email_id, "test1@example.com")
