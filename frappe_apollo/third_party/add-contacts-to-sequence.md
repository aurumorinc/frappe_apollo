Add Contacts to a Sequence

# Add Contacts to a Sequence

Use the Add Contacts to a Sequence endpoint to add contacts to the existing sequences in your team's Apollo account. <br><br>In Apollo terminology, a contact is a person that your team has explicitly added to your database. Only contacts can be added to sequences. To enrich a person's data, call the <a href="https://docs.apollo.io/reference/people-enrichment" target="_blank">People Enrichment endpoint</a>. Then, to add the person as a contact in your database, call the <a href="https://docs.apollo.io/reference/create-a-contact#/" target="_blank">Create a Contact endpoint</a>. <br><br>This endpoint requires a master API key. If you attempt to call the endpoint without a master key, you will receive a `403` response. Refer to <a href="https://docs.apollo.io/docs/create-api-key" target="_blank">Create API Keys</a> to learn how to create a master API key.

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "apollo-rest-api",
    "version": "1.0"
  },
  "servers": [
    {
      "url": "https://api.apollo.io/api/v1"
    }
  ],
  "components": {
    "securitySchemes": {
      "apiKey": {
        "type": "apiKey",
        "in": "header",
        "name": "x-api-key",
        "description": "API key"
      },
      "bearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "[Recommended] OAuth Access token"
      }
    }
  },
  "security": [
    {
      "bearerAuth": []
    },
    {
      "apiKey": []
    }
  ],
  "paths": {
    "/emailer_campaigns/{sequence_id}/add_contact_ids": {
      "post": {
        "summary": "Add Contacts to a Sequence",
        "description": "Use the Add Contacts to a Sequence endpoint to add contacts to the existing sequences in your team's Apollo account. <br><br>In Apollo terminology, a contact is a person that your team has explicitly added to your database. Only contacts can be added to sequences. To enrich a person's data so that they become a contact, call the <a href=\"https://docs.apollo.io/reference/people-enrichment\" target=\"_blank\">People Enrichment endpoint</a>. <br><br>This endpoint requires a master API key. If you attempt to call the endpoint without a master key, you will receive a `403` response. Refer to <a href=\"https://docs.apollo.io/docs/create-api-key\" target=\"_blank\">Create API Keys</a> to learn how to create a master API key.",
        "operationId": "add-contacts-to-sequence",
        "parameters": [
          {
            "name": "sequence_id",
            "in": "path",
            "description": "The Apollo ID for the sequence to which you want to add contacts. <br><br>To find sequence IDs, call the <a href=\"https://docs.apollo.io/reference/search-for-sequences\" target=\"_blank\">Search for Sequences endpoint</a> and identify the `id` value for the sequence. <br><br>Example: `66e9e215ece19801b219997f`",
            "required": true,
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "emailer_campaign_id",
            "in": "query",
            "description": "The same ID as the `sequence_id`. <br><br>Example: `66e9e215ece19801b219997f`",
            "required": true,
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "contact_ids[]",
            "in": "query",
            "description": "The Apollo IDs for the contacts that you want to add to the sequence. <br><br>To find contact IDs, call the <a href=\"https://docs.apollo.io/reference/search-for-contacts\" target=\"_blank\">Search for Contacts endpoint</a> and identify the `id` value for the contact. <br><br>Example: `66e34b81740c50074e3d1bd4`<br><br>Note: Either `contact_ids[]` or `label_names[]` must be provided.",
            "required": false,
            "schema": {
              "type": "array",
              "items": {
                "type": "string"
              }
            }
          },
          {
            "name": "label_names[]",
            "in": "query",
            "description": "Alternative to `contact_ids[]`. Array of label names to identify contacts to add to the sequence. Contacts with these labels will be added to the sequence. <br><br>Note: Either `contact_ids[]` or `label_names[]` must be provided.",
            "required": false,
            "schema": {
              "type": "array",
              "items": {
                "type": "string"
              }
            }
          },
          {
            "name": "send_email_from_email_account_id",
            "in": "query",
            "description": "The Apollo ID(s) for the email account(s) used to send to contacts you add to the sequence. Accepts either one id as a string, or multiple ids as an array of strings (multi-mailbox / rotation). To find email account IDs, call the <a href=\"https://docs.apollo.io/reference/get-a-list-of-email-accounts\" target=\"_blank\">Get a List of Email Accounts endpoint</a> and identify the `id` value for each email account. <br><br>Examples: `6633baaece5fbd01c791d7ca` (string) or `[\"6633baaece5fbd01c791d7ca\", \"6633baaece5fbd01c791d7cb\"]` (array).",
            "required": true,
            "schema": {
              "oneOf": [
                {
                  "type": "string",
                  "description": "Single email account ID."
                },
                {
                  "type": "array",
                  "items": {
                    "type": "string"
                  },
                  "minItems": 1,
                  "description": "One or more email account IDs."
                }
              ]
            }
          },
          {
            "name": "send_email_from_email_address",
            "in": "query",
            "description": "Optional specific email address to send from within the email account.",
            "required": false,
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "sequence_no_email",
            "in": "query",
            "description": "Set to `true` if you want to add contacts to the sequence even if they do not have an email address.",
            "required": false,
            "schema": {
              "type": "boolean",
              "default": false
            }
          },
          {
            "name": "sequence_unverified_email",
            "in": "query",
            "description": "Set to `true` if you want to add contacts to the sequence if they have an unverified email address.",
            "required": false,
            "schema": {
              "type": "boolean",
              "default": false
            }
          },
          {
            "name": "sequence_job_change",
            "in": "query",
            "description": "Set to `true` if you want to add contacts to the sequence even if they have recently changed jobs.",
            "required": false,
            "schema": {
              "type": "boolean",
              "default": false
            }
          },
          {
            "name": "sequence_active_in_other_campaigns",
            "in": "query",
            "description": "Set to `true` if you want to add contacts to the sequence even if they have been added to other sequences. This parameter does not differentiate between active and paused sequences.",
            "required": false,
            "schema": {
              "type": "boolean",
              "default": false
            }
          },
          {
            "name": "sequence_finished_in_other_campaigns",
            "in": "query",
            "description": "Set to `true` if you want to add contacts to the sequence if they have been marked as `finished` in another sequence.",
            "required": false,
            "schema": {
              "type": "boolean",
              "default": false
            }
          },
          {
            "name": "sequence_same_company_in_same_campaign",
            "in": "query",
            "description": "Set to `true` if you want to add contacts to the sequence even if other contacts from the same company are already in the sequence.",
            "required": false,
            "schema": {
              "type": "boolean",
              "default": false
            }
          },
          {
            "name": "contacts_without_ownership_permission",
            "in": "query",
            "description": "Set to `true` if you want to add contacts even if you don't have ownership permission for them.",
            "required": false,
            "schema": {
              "type": "boolean",
              "default": false
            }
          },
          {
            "name": "add_if_in_queue",
            "in": "query",
            "description": "Set to `true` if you want to add contacts even if they are currently in the queue for processing.",
            "required": false,
            "schema": {
              "type": "boolean",
              "default": false
            }
          },
          {
            "name": "contact_verification_skipped",
            "in": "query",
            "description": "Set to `true` if you want to skip contact verification during the addition process.",
            "required": false,
            "schema": {
              "type": "boolean",
              "default": false
            }
          },
          {
            "name": "user_id",
            "in": "query",
            "description": "The ID for the user in your team's Apollo account. <br><br>This is the user taking the action to add contacts to a sequence. When the sequence is updated, the activity log shows the user that added the contacts. <br><br>Use the <a href=\"https://docs.apollo.io/reference/get-a-list-of-users\" target=\"_blank\">Get a List of Users endpoint</a> to retrieve IDs for all of the users within your Apollo account. <br><br>Example: `66302798d03b9601c7934ebf`",
            "required": false,
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "status",
            "in": "query",
            "description": "Initial status for added contacts. When set to `paused` along with `auto_unpause_at`, enables scheduled addition of contacts.",
            "required": false,
            "schema": {
              "type": "string",
              "enum": [
                "active",
                "paused"
              ]
            }
          },
          {
            "name": "auto_unpause_at",
            "in": "query",
            "description": "DateTime when paused contacts should be automatically unpaused. Must be used with `status=paused`. Format: ISO 8601 datetime string.",
            "required": false,
            "schema": {
              "type": "string",
              "format": "date-time"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": {
                      "contacts": [
                        {
                          "contact_roles": [],
                          "id": "66e34b81740c50074e3d1bd4",
                          "first_name": "Fyodor",
                          "last_name": "Dostoevsky",
                          "name": "Fyodor Dostoevsky",
                          "linkedin_url": null,
                          "title": "Chief Writer",
                          "contact_stage_id": null,
                          "owner_id": "67b307d00957c2000d08872b",
                          "creator_id": "60affe7d6e270a00f5db6fe4",
                          "person_id": null,
                          "email_needs_tickling": null,
                          "organization_name": "Apollo.io",
                          "source": "api",
                          "original_source": "api",
                          "organization_id": null,
                          "headline": null,
                          "photo_url": null,
                          "present_raw_address": "St. Petersburg, Russia",
                          "linkedin_uid": null,
                          "extrapolated_email_confidence": null,
                          "salesforce_id": null,
                          "salesforce_lead_id": null,
                          "salesforce_contact_id": null,
                          "salesforce_account_id": null,
                          "crm_owner_id": null,
                          "created_at": "2024-09-12T20:13:53.207Z",
                          "emailer_campaign_ids": [
                            "66e9e215ece19801b219997f"
                          ],
                          "direct_dial_status": null,
                          "direct_dial_enrichment_failed_at": null,
                          "city": "Saint Petersburg",
                          "country": "Russia",
                          "state": "Saint Petersburg",
                          "email_status": "verified",
                          "email_source": null,
                          "account_id": null,
                          "last_activity_date": "2025-03-09T20:31:17.000+00:00",
                          "hubspot_vid": null,
                          "hubspot_company_id": null,
                          "crm_id": null,
                          "sanitized_phone": "+15553039182",
                          "merged_crm_ids": null,
                          "updated_at": "2025-05-23T13:38:25.109Z",
                          "queued_for_crm_push": false,
                          "suggested_from_rule_engine_config_id": null,
                          "email_unsubscribed": null,
                          "person_deleted": null,
                          "call_opted_out": null,
                          "label_ids": [],
                          "has_pending_email_arcgate_request": false,
                          "has_email_arcgate_request": false,
                          "existence_level": "full",
                          "email": "fyodor.dostoevsky@apollo.io",
                          "email_from_customer": true,
                          "typed_custom_fields": {},
                          "custom_field_errors": null,
                          "crm_record_url": null,
                          "email_status_unavailable_reason": null,
                          "email_true_status": "User Managed",
                          "updated_email_true_status": true,
                          "source_display_name": "Created from API",
                          "twitter_url": null,
                          "facebook_url": null,
                          "contact_campaign_statuses": [
                            {
                              "id": "68782af181c7f0002159df25",
                              "emailer_campaign_id": "66e9e215ece19801b219997f",
                              "send_email_from_user_id": "66302798d03b9601c7934ebf",
                              "inactive_reason": "Sequence inactive",
                              "status": "paused",
                              "added_at": "2025-07-16T22:42:57.372+00:00",
                              "added_by_user_id": "60affe7d6e270a00f5db6fe4",
                              "finished_at": null,
                              "paused_at": null,
                              "auto_unpause_at": null,
                              "send_email_from_email_address": "test.brandan.blevins@apollomail.io",
                              "send_email_from_email_account_id": "6633baaece5fbd01c791d7ca",
                              "manually_set_unpause": null,
                              "failure_reason": null,
                              "current_step_id": null,
                              "in_response_to_emailer_message_id": null,
                              "cc_emails": null,
                              "bcc_emails": null,
                              "to_emails": null,
                              "current_step_position": null
                            }
                          ],
                          "contact_emails": [
                            {
                              "email_md5": "cf4604bbd3c12ca9e36e20aa0aefac29",
                              "email_sha256": "b5d981918efbd5a93eb10f834643a4277034f24e3b5cabc2631440c7ade49cf8",
                              "email_status": "verified",
                              "extrapolated_email_confidence": null,
                              "position": 0,
                              "email": "fyodor.dostoevsky@apollo.io",
                              "free_domain": false,
                              "source": "User Managed",
                              "third_party_vendor_name": null,
                              "vendor_validation_statuses": [],
                              "email_needs_tickling": null,
                              "email_true_status": "User Managed",
                              "email_status_unavailable_reason": null
                            }
                          ],
                          "time_zone": "Asia/Krasnoyarsk",
                          "intent_strength": null,
                          "show_intent": false,
                          "phone_numbers": [
                            {
                              "raw_number": "555-303-9182",
                              "sanitized_number": "+15553039182",
                              "type": "work_direct",
                              "position": 0,
                              "status": "no_status",
                              "dnc_status": null,
                              "dnc_other_info": {},
                              "dialer_flags": null,
                              "source_name": "User Managed",
                              "vendor_validation_statuses": [],
                              "third_party_vendor_name": null
                            }
                          ],
                          "account_phone_note": null,
                          "free_domain": false,
                          "email_domain_catchall": false
                        }
                      ],
                      "skipped_contact_ids": {
                        "66e34b81740c50074e3d1bd5": "contact_not_found"
                      },
                      "emailer_campaign": {
                        "id": "66e9e215ece19801b219997f",
                        "name": "Target Copywriting Clients in Dublin",
                        "archived": true,
                        "created_at": "2024-09-17T20:09:57.837Z",
                        "emailer_schedule_id": "6095a711bd01d100a506d52a",
                        "max_emails_per_day": null,
                        "user_id": "66302798d03b9601c7934ebf",
                        "active": false,
                        "loaded_stats": true
                      },
                      "emailer_steps": [
                        {
                          "id": "66e9e232ece19801b21999a4",
                          "emailer_campaign_id": "66e9e215ece19801b219997f",
                          "position": 1,
                          "wait_time": 4,
                          "type": "auto_email",
                          "wait_mode": "hour"
                        }
                      ],
                      "emailer_touches": [
                        {
                          "id": "66e9e232ece19801b21999a6",
                          "emailer_step_id": "66e9e232ece19801b21999a4",
                          "emailer_template_id": "66e9e232ece19801b21999a5",
                          "status": "approved",
                          "type": "new_thread"
                        }
                      ],
                      "team": {
                        "id": "6095a710bd01d100a506d4ac",
                        "sequences_finder_empty": false
                      },
                      "signals_hash": null
                    }
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "contacts": {
                      "type": "array",
                      "description": "Array of contacts that were successfully added to the sequence",
                      "items": {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "string",
                            "description": "Unique identifier for the contact"
                          },
                          "first_name": {
                            "type": "string",
                            "nullable": true
                          },
                          "last_name": {
                            "type": "string",
                            "nullable": true
                          },
                          "name": {
                            "type": "string",
                            "description": "Full name of the contact"
                          },
                          "email": {
                            "type": "string",
                            "nullable": true
                          },
                          "title": {
                            "type": "string",
                            "nullable": true
                          },
                          "organization_name": {
                            "type": "string",
                            "nullable": true
                          },
                          "linkedin_url": {
                            "type": "string",
                            "nullable": true
                          },
                          "contact_stage_id": {
                            "type": "string",
                            "nullable": true
                          },
                          "owner_id": {
                            "type": "string",
                            "nullable": true
                          },
                          "creator_id": {
                            "type": "string"
                          },
                          "person_id": {
                            "type": "string",
                            "nullable": true
                          },
                          "organization_id": {
                            "type": "string",
                            "nullable": true
                          },
                          "account_id": {
                            "type": "string",
                            "nullable": true
                          },
                          "source": {
                            "type": "string"
                          },
                          "original_source": {
                            "type": "string"
                          },
                          "created_at": {
                            "type": "string",
                            "format": "date-time"
                          },
                          "updated_at": {
                            "type": "string",
                            "format": "date-time"
                          },
                          "emailer_campaign_ids": {
                            "type": "array",
                            "items": {
                              "type": "string"
                            }
                          },
                          "email_status": {
                            "type": "string",
                            "nullable": true
                          },
                          "city": {
                            "type": "string",
                            "nullable": true
                          },
                          "country": {
                            "type": "string",
                            "nullable": true
                          },
                          "state": {
                            "type": "string",
                            "nullable": true
                          },
                          "sanitized_phone": {
                            "type": "string",
                            "nullable": true
                          },
                          "time_zone": {
                            "type": "string",
                            "nullable": true
                          },
                          "contact_campaign_statuses": {
                            "type": "array",
                            "items": {
                              "type": "object",
                              "properties": {
                                "id": {
                                  "type": "string"
                                },
                                "emailer_campaign_id": {
                                  "type": "string"
                                },
                                "status": {
                                  "type": "string"
                                },
                                "added_at": {
                                  "type": "string",
                                  "format": "date-time"
                                },
                                "send_email_from_email_account_id": {
                                  "type": "string"
                                },
                                "send_email_from_email_address": {
                                  "type": "string",
                                  "nullable": true
                                },
                                "inactive_reason": {
                                  "type": "string",
                                  "nullable": true
                                }
                              }
                            }
                          },
                          "contact_emails": {
                            "type": "array",
                            "items": {
                              "type": "object",
                              "properties": {
                                "email": {
                                  "type": "string"
                                },
                                "email_status": {
                                  "type": "string"
                                },
                                "position": {
                                  "type": "integer"
                                },
                                "email_md5": {
                                  "type": "string"
                                },
                                "email_sha256": {
                                  "type": "string"
                                },
                                "free_domain": {
                                  "type": "boolean"
                                },
                                "source": {
                                  "type": "string"
                                },
                                "email_true_status": {
                                  "type": "string"
                                }
                              }
                            }
                          },
                          "phone_numbers": {
                            "type": "array",
                            "items": {
                              "type": "object",
                              "properties": {
                                "raw_number": {
                                  "type": "string"
                                },
                                "sanitized_number": {
                                  "type": "string"
                                },
                                "type": {
                                  "type": "string"
                                },
                                "position": {
                                  "type": "integer"
                                },
                                "status": {
                                  "type": "string"
                                },
                                "source_name": {
                                  "type": "string"
                                }
                              }
                            }
                          },
                          "label_ids": {
                            "type": "array",
                            "items": {
                              "type": "string"
                            }
                          },
                          "typed_custom_fields": {
                            "type": "object"
                          },
                          "free_domain": {
                            "type": "boolean"
                          },
                          "email_domain_catchall": {
                            "type": "boolean"
                          }
                        }
                      }
                    },
                    "skipped_contact_ids": {
                      "type": "object",
                      "description": "Hash mapping contact IDs to reasons why they were skipped during the addition process. Each key is a contact ID and each value is a reason code.",
                      "properties": {
                        "<contact_id>": {
                          "type": "string",
                          "description": "Reason why this contact was skipped",
                          "x-enumDescriptions": {
                            "contact_not_found": "Contact ID was not found for the team",
                            "contacts_already_exists_in_current_campaign": "Contact is already a part of current sequence",
                            "contacts_active_in_other_campaigns": "Contact is active in other sequence",
                            "contacts_finished_in_other_campaigns": "Contact is finished in other sequence",
                            "contacts_without_email": "Contact does not have email",
                            "contacts_unverified_email": "Contact does not have verified email",
                            "contacts_with_job_change": "Contact has a pending job change event",
                            "contacts_in_same_company": "Contact from the same company is part of the current sequence (Including for completeness, but extremely rare - only for old users who had opted in for such feature)",
                            "contacts_without_ownership_permission": "User does not have permission to reach out to contact",
                            "contacts_in_pending_state": "Contact is already part of account queue (Rare for api only users - only applicable for users who are using account based workflows in apollo)",
                            "contacts_with_unverified_user_managed_email": "Contact has unverified user-managed email"
                          }
                        }
                      }
                    },
                    "emailer_campaign": {
                      "type": "object",
                      "description": "Complete emailer campaign object with statistics",
                      "properties": {
                        "id": {
                          "type": "string"
                        },
                        "name": {
                          "type": "string"
                        },
                        "archived": {
                          "type": "boolean"
                        },
                        "active": {
                          "type": "boolean"
                        },
                        "created_at": {
                          "type": "string",
                          "format": "date-time"
                        },
                        "user_id": {
                          "type": "string"
                        },
                        "emailer_schedule_id": {
                          "type": "string",
                          "nullable": true
                        },
                        "max_emails_per_day": {
                          "type": "integer",
                          "nullable": true
                        },
                        "same_account_reply_policy_cd": {
                          "type": "string",
                          "nullable": true
                        },
                        "excluded_account_stage_ids": {
                          "type": "array",
                          "items": {
                            "type": "string"
                          }
                        },
                        "excluded_contact_stage_ids": {
                          "type": "array",
                          "items": {
                            "type": "string"
                          }
                        },
                        "label_ids": {
                          "type": "array",
                          "items": {
                            "type": "string"
                          }
                        },
                        "permissions": {
                          "type": "string"
                        },
                        "loaded_stats": {
                          "type": "boolean"
                        },
                        "unique_scheduled": {
                          "oneOf": [
                            {
                              "type": "integer"
                            },
                            {
                              "type": "string",
                              "enum": [
                                "loading"
                              ]
                            }
                          ]
                        },
                        "unique_delivered": {
                          "type": "integer"
                        },
                        "unique_bounced": {
                          "type": "integer"
                        },
                        "unique_opened": {
                          "type": "integer"
                        },
                        "unique_replied": {
                          "type": "integer"
                        },
                        "bounce_rate": {
                          "type": "number"
                        },
                        "open_rate": {
                          "type": "number"
                        },
                        "reply_rate": {
                          "type": "number"
                        },
                        "contact_statuses": {
                          "type": "object",
                          "properties": {
                            "active": {
                              "oneOf": [
                                {
                                  "type": "integer"
                                },
                                {
                                  "type": "string",
                                  "enum": [
                                    "loading"
                                  ]
                                }
                              ]
                            },
                            "failed": {
                              "type": "integer"
                            },
                            "paused": {
                              "oneOf": [
                                {
                                  "type": "integer"
                                },
                                {
                                  "type": "string",
                                  "enum": [
                                    "loading"
                                  ]
                                }
                              ]
                            },
                            "finished": {
                              "oneOf": [
                                {
                                  "type": "integer"
                                },
                                {
                                  "type": "string",
                                  "enum": [
                                    "loading"
                                  ]
                                }
                              ]
                            },
                            "bounced": {
                              "oneOf": [
                                {
                                  "type": "integer"
                                },
                                {
                                  "type": "string",
                                  "enum": [
                                    "loading"
                                  ]
                                }
                              ]
                            }
                          }
                        },
                        "sharing_permission": {
                          "type": "object",
                          "properties": {
                            "visibility": {
                              "type": "string"
                            },
                            "access_type": {
                              "type": "string"
                            },
                            "object_type": {
                              "type": "string"
                            },
                            "object_id": {
                              "type": "string"
                            },
                            "is_owner": {
                              "type": "boolean"
                            },
                            "owner_id": {
                              "type": "string"
                            },
                            "sharing_accesses": {
                              "type": "array",
                              "items": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "string"
                                  },
                                  "shared_by": {
                                    "type": "string"
                                  },
                                  "user_or_team_id": {
                                    "type": "string"
                                  },
                                  "user_or_team_type": {
                                    "type": "string"
                                  },
                                  "access_type": {
                                    "type": "string"
                                  },
                                  "object_id": {
                                    "type": "string"
                                  },
                                  "object_type": {
                                    "type": "string"
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    },
                    "emailer_steps": {
                      "type": "array",
                      "description": "Array of sequence steps",
                      "items": {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "string"
                          },
                          "emailer_campaign_id": {
                            "type": "string"
                          },
                          "position": {
                            "type": "integer"
                          },
                          "wait_time": {
                            "type": "integer"
                          },
                          "type": {
                            "type": "string",
                            "enum": [
                              "auto_email",
                              "call",
                              "action_item",
                              "manual_email"
                            ]
                          },
                          "wait_mode": {
                            "type": "string",
                            "enum": [
                              "hour",
                              "day",
                              "week"
                            ]
                          },
                          "note": {
                            "type": "string",
                            "nullable": true
                          },
                          "priority": {
                            "type": "string",
                            "enum": [
                              "high",
                              "medium",
                              "low"
                            ],
                            "nullable": true
                          },
                          "counts": {
                            "type": "object",
                            "properties": {
                              "active": {
                                "type": "integer"
                              },
                              "paused": {
                                "type": "integer"
                              },
                              "finished": {
                                "type": "integer"
                              },
                              "bounced": {
                                "type": "integer"
                              }
                            }
                          },
                          "unique_scheduled": {
                            "oneOf": [
                              {
                                "type": "integer"
                              },
                              {
                                "type": "string",
                                "enum": [
                                  "loading"
                                ]
                              }
                            ]
                          },
                          "unique_skipped": {
                            "oneOf": [
                              {
                                "type": "integer"
                              },
                              {
                                "type": "string",
                                "enum": [
                                  "loading"
                                ]
                              }
                            ]
                          },
                          "unique_completed": {
                            "oneOf": [
                              {
                                "type": "integer"
                              },
                              {
                                "type": "string",
                                "enum": [
                                  "loading"
                                ]
                              }
                            ]
                          }
                        }
                      }
                    },
                    "emailer_touches": {
                      "type": "array",
                      "description": "Array of email templates/touches for the sequence",
                      "items": {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "string"
                          },
                          "emailer_step_id": {
                            "type": "string"
                          },
                          "emailer_template_id": {
                            "type": "string"
                          },
                          "status": {
                            "type": "string",
                            "enum": [
                              "approved",
                              "pending",
                              "draft"
                            ]
                          },
                          "type": {
                            "type": "string",
                            "enum": [
                              "new_thread",
                              "reply"
                            ]
                          },
                          "include_signature": {
                            "type": "boolean"
                          },
                          "has_personalized_opener": {
                            "type": "boolean"
                          },
                          "template_type": {
                            "type": "string"
                          },
                          "unique_scheduled": {
                            "oneOf": [
                              {
                                "type": "integer"
                              },
                              {
                                "type": "string",
                                "enum": [
                                  "loading"
                                ]
                              }
                            ]
                          },
                          "unique_delivered": {
                            "type": "integer"
                          },
                          "unique_bounced": {
                            "type": "integer"
                          },
                          "unique_opened": {
                            "type": "integer"
                          },
                          "unique_replied": {
                            "type": "integer"
                          },
                          "bounce_rate": {
                            "type": "number",
                            "nullable": true
                          },
                          "open_rate": {
                            "type": "number",
                            "nullable": true
                          },
                          "reply_rate": {
                            "type": "number",
                            "nullable": true
                          }
                        }
                      }
                    },
                    "team": {
                      "type": "object",
                      "properties": {
                        "id": {
                          "type": "string",
                          "example": "6095a710bd01d100a506d4ac"
                        },
                        "sequences_finder_empty": {
                          "type": "boolean",
                          "example": false
                        }
                      }
                    },
                    "signals_hash": {
                      "type": "object",
                      "description": "Optional signals data for play recommendations and analytics",
                      "nullable": true
                    }
                  },
                  "required": [
                    "contacts",
                    "skipped_contact_ids",
                    "emailer_campaign",
                    "emailer_steps",
                    "emailer_touches",
                    "team"
                  ]
                }
              }
            }
          },
          "401": {
            "description": "Unauthorized - Invalid API key",
            "content": {
              "text/plain": {
                "schema": {
                  "type": "string"
                },
                "examples": {
                  "Invalid API Key": {
                    "value": "Invalid access credentials."
                  }
                }
              }
            }
          },
          "403": {
            "description": "Forbidden - Master API key required",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "error": {
                      "type": "string"
                    },
                    "error_code": {
                      "type": "string"
                    }
                  }
                },
                "examples": {
                  "Master API Key Required": {
                    "value": {
                      "error": "api/v1/emailer_campaigns/add_contact_ids is not accessible with this api_key",
                      "error_code": "API_INACCESSIBLE"
                    }
                  }
                }
              }
            }
          },
          "422": {
            "description": "Unprocessable Entity - Validation errors",
            "content": {
              "application/json": {
                "examples": {
                  "Add contact IDs": {
                    "value": "{\n  \"error\": \"Please specify either contact_ids or label_names.\"\n}"
                  },
                  "Add IDs": {
                    "value": "{\n  \"error\": \"Please specify a emailer_campaign_id and send_email_from_email_account_id.\"\n}"
                  },
                  "Inactive Email Accounts": {
                    "value": "{\n  \"error\": \"These mailboxes are no longer active. test@example.com\"\n}"
                  },
                  "Aggregate Accounts Not Supported": {
                    "value": "{\n  \"error\": \"Aggregate accounts are not supported for this sequence. These are the aggregate accounts: 6633baaece5fbd01c791d7ca\"\n}"
                  }
                },
                "schema": {
                  "oneOf": [
                    {
                      "title": "Add contact IDs",
                      "type": "object",
                      "properties": {
                        "error": {
                          "type": "string",
                          "example": "Please specify either contact_ids or label_names."
                        }
                      }
                    },
                    {
                      "title": "Add IDs",
                      "type": "object",
                      "properties": {
                        "error": {
                          "type": "string",
                          "example": "Please specify a emailer_campaign_id and send_email_from_email_account_id."
                        }
                      }
                    },
                    {
                      "title": "Inactive Email Accounts",
                      "type": "object",
                      "properties": {
                        "error": {
                          "type": "string",
                          "example": "These mailboxes are no longer active. test@example.com"
                        }
                      }
                    },
                    {
                      "title": "Aggregate Accounts Not Supported",
                      "type": "object",
                      "properties": {
                        "error": {
                          "type": "string",
                          "example": "Aggregate accounts are not supported for this sequence. These are the aggregate accounts: 6633baaece5fbd01c791d7ca"
                        }
                      }
                    }
                  ]
                }
              }
            }
          },
          "429": {
            "description": "Too Many Requests - Rate limit exceeded",
            "content": {
              "application/json": {
                "examples": {
                  "Too many requests": {
                    "value": "{\n    \"message\": \"The maximum number of api calls allowed for api/v1/emailer_campaigns/{sequence_id}/add_contact_ids is 600 times per hour. Please upgrade your plan from https://app.apollo.io/#/settings/plans/upgrade.\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "message": {
                      "type": "string",
                      "example": "The maximum number of api calls allowed for api/v1/emailer_campaigns/{sequence_id}/add_contact_ids is 600 times per hour. Please upgrade your plan from https://app.apollo.io/#/settings/plans/upgrade."
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "x-readme": {
    "headers": [
      {
        "key": "Cache-Control",
        "value": "no-cache"
      },
      {
        "key": "Content-Type",
        "value": "application/json"
      }
    ],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```