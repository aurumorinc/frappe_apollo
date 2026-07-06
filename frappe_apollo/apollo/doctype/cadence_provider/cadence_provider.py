import frappe
from frappe_cadence.cadence.doctype.cadence_provider.cadence_provider import CadenceProviderBase
from frappe_apollo.integrations.apollo import ApolloClient, ApolloRateLimitError
from frappe_controller.utils.background_jobs import enqueue
from frappe_controller.utils.controller import wait_for_event

class ApolloCadenceProvider(CadenceProviderBase):

    def on_mcc_status_changed(self, mcc_doc, old_status, new_status):
        if old_status == "Draft" and new_status == "Scheduled":
            enqueue(
                method="frappe_apollo.apollo.doctype.cadence_provider.cadence_provider.async_sync_lead_and_assign_sequence",
                queue="medium",
                mcc_name=mcc_doc.name
            )

    def on_cadence_updated(self, cadence_doc):
        pass

    def on_communication_status_changed(self, comm_doc, old_status, new_status):
        if new_status == "Scheduled":
            enqueue(
                method="frappe_apollo.apollo.doctype.cadence_provider.cadence_provider.async_sync_communication_to_apollo",
                queue="medium",
                comm_name=comm_doc.name
            )


def async_sync_lead_and_assign_sequence(mcc_name):
    mcc = frappe.get_doc("Multi Channel Cadence", mcc_name)

    # Idempotency check: if already synced, return
    # Assuming apollo_sync_status is a field. For MCC we might need to check if the assignment happened.
    # For now we'll just proceed as create_contact is likely idempotent and add_contact handles duplicates or we can check 'People'
    
    lead = frappe.get_doc("CRM Lead", mcc.recipient)
    sender = mcc.sender

    # Check Provider Status
    settings = frappe.get_doc("Apollo Settings")
    if not settings.enable:
        wait_for_event(
            event_key="doc:Apollo Settings:on_update",
            condition="argument.get('enable') == 1"
        )

    # Find Mailbox
    mailbox_id = frappe.db.get_value("User Mailbox", {"parent": sender}, "mailbox")
    if not mailbox_id:
        frappe.log_error(f"No Apollo Mailbox assigned to user {sender}")
        wait_for_event(
            event_key="doc:User Mailbox:after_insert",
            condition=f"argument.get('parent') == '{sender}'"
        )
        
    mailbox = frappe.get_doc("Mailbox", mailbox_id)
    account_name = mailbox.account

    client = ApolloClient(account_name)

    # Lead Syncing
    people_id = frappe.db.get_value("People", {"lead": lead.name, "account": account_name}, "id")
    if not people_id:
        lead_data = {
            "first_name": lead.first_name,
            "last_name": lead.last_name,
            "email": lead.email,
            "organization_name": lead.organization
        }
        people_id = client.create_contact(lead_data)
        if people_id:
            frappe.get_doc({
                "doctype": "People",
                "lead": lead.name,
                "account": account_name,
                "id": people_id
            }).insert(ignore_permissions=True)

    if not people_id:
        frappe.log_error("Could not create/find Apollo contact")
        # In a real scenario we might wait or fail, returning for now
        return

    # Find Sequence
    sequence = frappe.get_all("Sequence", filters={
        "campaign": mcc.cadence_name,
        "account": account_name
    }, fields=["id"], limit=1)

    if not sequence:
        frappe.log_error(f"No Apollo Sequence found for Cadence {mcc.cadence_name} and Account {account_name}")
        wait_for_event(
            event_key="doc:Sequence:after_insert",
            condition=f"argument.get('campaign') == '{mcc.cadence_name}' and argument.get('account') == '{account_name}'"
        )

    sequence_id = sequence[0].id
    
    # ApolloRateLimitError will naturally bubble up and frappe_controller will retry it
    client.add_contacts_to_sequence(people_id, sequence_id, mailbox.id)


def async_sync_communication_to_apollo(comm_name):
    comm = frappe.get_doc("Communication", comm_name)
    
    # Idempotency check
    if comm.get("apollo_sync_status") == "Synced":
        return

    mcc = frappe.get_doc("Multi Channel Cadence", comm.reference_name)

    # Check Provider Status
    settings = frappe.get_doc("Apollo Settings")
    if not settings.enable:
        wait_for_event(
            event_key="doc:Apollo Settings:on_update",
            condition="argument.get('enable') == 1"
        )

    # Find Mailbox
    mailbox_id = frappe.db.get_value("User Mailbox", {"parent": mcc.sender}, "mailbox")
    if not mailbox_id:
        frappe.log_error(f"No Apollo Mailbox assigned to user {mcc.sender}")
        wait_for_event(
            event_key="doc:User Mailbox:after_insert",
            condition=f"argument.get('parent') == '{mcc.sender}'"
        )

    mailbox = frappe.get_doc("Mailbox", mailbox_id)
    account_name = mailbox.account

    # Find Sequence
    sequence = frappe.get_all("Sequence", filters={
        "campaign": mcc.cadence_name,
        "account": account_name
    }, limit=1)

    if not sequence:
        frappe.log_error(f"No Apollo Sequence found for Cadence {mcc.cadence_name} and Account {account_name}")
        wait_for_event(
            event_key="doc:Sequence:after_insert",
            condition=f"argument.get('campaign') == '{mcc.cadence_name}' and argument.get('account') == '{account_name}'"
        )

    seq_doc = frappe.get_doc("Sequence", sequence[0].name)

    # Find People
    people_id = frappe.db.get_value("People", {"lead": mcc.recipient, "account": account_name}, "id")
    if not people_id:
        frappe.log_error(f"No Apollo Contact found for Lead {mcc.recipient} and Account {account_name}")
        # Wait for people doc creation (which happens in lead sync)
        wait_for_event(
            event_key="doc:People:after_insert",
            condition=f"argument.get('lead') == '{mcc.recipient}' and argument.get('account') == '{account_name}'"
        )

    # Payload Validation
    if not comm.content or not comm.subject:
        return

    step_idx = 1
    if comm.cadence_schedule:
        cadence = frappe.get_doc("Cadence", mcc.cadence_name)
        for idx, sch in enumerate(cadence.cadence_schedules):
            if sch.name == comm.cadence_schedule:
                step_idx = idx + 1
                break

    if step_idx > len(seq_doc.sequence_steps):
        # Could wait for sequence steps update
        return

    step = seq_doc.sequence_steps[step_idx - 1]

    if not step.subject_custom_field_id or not step.response_custom_field_id:
        frappe.log_error("Missing custom field IDs in Apollo sequence step")
        # Could wait for field provision but relying on sequence steps should be enough for now
        return

    custom_fields = {
        step.subject_custom_field_id: comm.subject,
        step.response_custom_field_id: comm.content
    }

    client = ApolloClient(account_name)
    
    # ApolloRateLimitError will naturally bubble up
    client.update_contact(people_id, custom_fields)

    comm.apollo_sync_status = "Synced"
    comm.save(ignore_permissions=True)
