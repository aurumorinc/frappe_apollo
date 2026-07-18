import frappe
from frappe.tests import IntegrationTestCase
from unittest.mock import patch, MagicMock
from frappe_apollo.apollo.doctype.email_account.email_account import queue_get_email_accounts, get_email_accounts

class TestEmailAccountIntegration(IntegrationTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if frappe.db.exists("Account", "Mailbox Test Account"):
            frappe.delete_doc("Account", "Mailbox Test Account", force=1, ignore_permissions=True)
        if frappe.db.exists("Account", "Another Test Account"):
            frappe.delete_doc("Account", "Another Test Account", force=1, ignore_permissions=True)
            
        frappe.db.sql("DELETE FROM `tabAccount` WHERE name IN ('Mailbox Test Account', 'Another Test Account')")
        cls._cleanup_email_accounts()
        
        frappe.get_doc({
            "doctype": "Account",
            "account_name": "Mailbox Test Account",
            "api_key": "some_key"
        }).insert(ignore_permissions=True)
        
        frappe.get_doc({
            "doctype": "Account",
            "account_name": "Another Test Account",
            "api_key": "some_key"
        }).insert(ignore_permissions=True)

    @classmethod
    def tearDownClass(cls):
        frappe.db.rollback()
        super().tearDownClass()

    @classmethod
    def _cleanup_email_accounts(cls):
        accounts = frappe.get_all("Email Account", filters={"email_id": ["in", ("test1@example.com", "test2@example.com")]})
        for acc in accounts:
            frappe.delete_doc("Email Account", acc.name, force=1, ignore_permissions=True)
        frappe.db.sql("DELETE FROM `tabEmail Account Apollo ID`")

    def setUp(self):
        super().setUp()
        self._cleanup_email_accounts()

    def tearDown(self):
        self._cleanup_email_accounts()
        super().tearDown()

    @patch("frappe.enqueue")
    def test_queue_get_email_accounts(self, mock_enqueue):
        queue_get_email_accounts()
        found = False
        for call in mock_enqueue.call_args_list:
            if call[1].get("account_name") == "Mailbox Test Account":
                found = True
                break
        self.assertTrue(found, "get_email_accounts was not queued for Mailbox Test Account")

    @patch("frappe_apollo.integrations.apollo.ApolloClient")
    def test_get_email_accounts_creation(self, mock_client_cls):
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

        get_email_accounts("Mailbox Test Account")

        mock_client.get_email_accounts.assert_called_once()

        mailboxes = frappe.get_all("Email Account", filters={"email_id": "test1@example.com"})
        self.assertEqual(len(mailboxes), 1)
        
        mb_doc = frappe.get_doc("Email Account", mailboxes[0].name)
        self.assertEqual(mb_doc.email_id, "test1@example.com")
        self.assertEqual(mb_doc.service, "Apollo")
        self.assertEqual(len(mb_doc.get("apollo_ids")), 1)
        self.assertEqual(mb_doc.apollo_ids[0].account, "Mailbox Test Account")
        self.assertEqual(mb_doc.apollo_ids[0].apollo_id, "mailbox_id_1")

    @patch("frappe_apollo.integrations.apollo.ApolloClient")
    def test_get_email_accounts_append(self, mock_client_cls):
        frappe.get_doc({
            "doctype": "Email Account",
            "email_id": "test1@example.com",
            "service": "Apollo",
            "enable_outgoing": 0,
            "enable_incoming": 0,
            "apollo_ids": [
                {
                    "account": "Mailbox Test Account",
                    "apollo_id": "mailbox_id_1"
                }
            ]
        }).insert(ignore_permissions=True)
            
        mock_client = mock_client_cls.return_value
        mock_client.get_email_accounts.return_value = {
            "email_accounts": [
                {
                    "id": "mailbox_id_1_alt",
                    "email": "test1@example.com",
                    "active": True
                }
            ]
        }

        get_email_accounts("Another Test Account")

        mailboxes = frappe.get_all("Email Account", filters={"email_id": "test1@example.com"})
        self.assertEqual(len(mailboxes), 1)
        
        mb_doc = frappe.get_doc("Email Account", mailboxes[0].name)
        
        # It should now have 2 apollo accounts
        self.assertEqual(len(mb_doc.get("apollo_ids")), 2)
        accounts = [acc.account for acc in mb_doc.get("apollo_ids")]
        self.assertIn("Mailbox Test Account", accounts)
        self.assertIn("Another Test Account", accounts)
        
        alt_acc = next(acc for acc in mb_doc.apollo_ids if acc.account == "Another Test Account")
        self.assertEqual(alt_acc.apollo_id, "mailbox_id_1_alt")
