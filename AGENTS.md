# AI Agent Guidelines for Frappe Apollo

This document provides context and strict guidelines for AI agents working on the `frappe_apollo` repository.

## 1. Framework Context
This is a **Frappe** application. It uses Frappe's DocType system for database modeling and the `bench` CLI for execution. However, we strictly override Frappe's default testing structure to follow standard Python Testing Standards.

## 2. Testing Architecture
You MUST adhere to the following testing rules:

### Directory Structure
- **Internal Tests**: `frappe_apollo/tests/integration/internal/`
  - These tests use the local database and mock all external API calls.
  - They must mirror the source tree (e.g., `frappe_apollo/integrations/apollo.py` is tested in `frappe_apollo/tests/integration/internal/integrations/test_apollo.py`).
- **External Tests**: `frappe_apollo/tests/integration/external/`
  - These tests interact with the live Apollo API using `vcrpy`.
  - They must also mirror the source tree.

### VCR.py Configuration
- External tests use `vcrpy` to record HTTP interactions into YAML cassettes.
- **CRITICAL**: The VCR configuration in `conftest.py` MUST scrub sensitive headers (`Authorization`, `X-Api-Key`). Never commit real credentials to the repository.
- The `record_mode` is dynamic:
  - If `APOLLO_TEST_ACCOUNT` is provided, `record_mode='once'` (records new cassettes).
  - If no credentials are provided, `record_mode='none'` (replays existing cassettes using a dummy account).

### Test Isolation
- Tests MUST be isolated. Do not rely on the execution order of tests.
- Do not use `setUpClass` to create shared state that mutates across tests. Each test should create its own required state (e.g., creating a contact before updating it).
- Do not add API cleanup logic (like deleting contacts via the Apollo API) unless explicitly requested, as the API key may lack deletion permissions. Rely on Frappe's `IntegrationTestCase` database rollback for local cleanup.

## 3. Integration Guidelines
- **ApolloClient**: All interactions with the Apollo API must go through the `ApolloClient` wrapper in `frappe_apollo/integrations/apollo.py`.
- **Authentication**: The client supports both API Key and OAuth 2.0 authentication. It automatically handles OAuth token refreshes if a `401 Unauthorized` response is received.
- **Rate Limiting**: The client raises an `ApolloRateLimitError` if a `429 Too Many Requests` response is received. Agents should handle this gracefully in background jobs.
