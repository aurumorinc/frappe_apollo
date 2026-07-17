# Frappe Apollo

Frappe Apollo is a powerful integration app that connects your Frappe/ERPNext instance with [Apollo.io](https://www.apollo.io/). It enables seamless synchronization of contacts, automated sequence management, and real-time webhook processing to streamline your sales and marketing workflows directly from your ERP.

## Features

- **Account Management**: Securely connect to Apollo using either API Keys or OAuth 2.0.
- **Contact Synchronization**: Automatically create and update Apollo contacts from Frappe CRM Leads.
- **Sequence Automation**: Add contacts to Apollo sequences (Emailer Campaigns) directly from Frappe Multi-Channel Campaigns.
- **Real-time Webhooks**: Listen to Apollo webhooks (e.g., `message_sent`, `message_replied`) to automatically update communication statuses and campaign progress in Frappe.
- **Custom Fields**: Provision and map custom fields between Frappe and Apollo.

## Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/your-repo/frappe_apollo.git --branch main
bench install-app frappe_apollo
```

## Configuration

1. Navigate to **Cadence Provider** in your Frappe instance and enable the Apollo integration.
2. Create a new **Account** document.
3. Choose your authentication method:
   - **API Key**: Enter your Apollo Master API Key.
   - **OAuth 2.0**: Enter your Client ID and Client Secret, then click "Authorize" to complete the OAuth flow.
4. Configure your Apollo Webhook URL to point to `<your-site-url>/api/method/frappe_apollo.webhook.handle` and set the Bearer Token in your Account settings.

## Testing

This app follows strict Python Testing Standards, separating tests into `internal` and `external` integration tests.

### Running Internal Tests
Internal tests use the local database and mock external API calls. They do not require any credentials and are safe to run in CI/CD pipelines.
```bash
bench run-tests --app frappe_apollo
```

### Running External Tests
External tests interact with the live Apollo API. To ensure tests are fast, deterministic, and don't exhaust rate limits, we use `vcrpy` to record HTTP interactions into "cassettes" (YAML files).

**Replaying Tests (No Credentials Required)**
If the cassettes are already committed to the repository, you can run the external tests without any credentials. VCR will intercept the requests and replay the recorded responses.
```bash
bench run-tests --module frappe_apollo.tests.integration.external.integrations.test_apollo
```

**Recording New Cassettes (Credentials Required)**
If you write new external tests or need to update existing ones, you must provide real Apollo credentials to hit the live API and record the new cassettes.
```bash
APOLLO_TEST_ACCOUNT="your_account@example.com" APOLLO_TEST_SEQUENCE_ID="your_sequence_id" bench run-tests --module frappe_apollo.tests.integration.external.integrations.test_apollo
```
*Note: VCR is configured to automatically scrub sensitive headers (`Authorization`, `X-Api-Key`) from the recorded cassettes.*

## Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/frappe_apollo
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- `ruff` (Linting and Import Sorting)
- `eslint` (JavaScript Linting)
- `prettier` (Code Formatting)

## License

MIT
