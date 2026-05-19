Update Contact Status in a Sequence

# Update Contact Status in a Sequence

Use the Update Contact Status in a Sequence endpoint to either mark contacts as having `finished` a sequence, or to remove them from a sequence entirely. <br><br>This endpoint requires a master API key. If you attempt to call the endpoint without a master key, you will receive a `403` response. Refer to <a href="https://docs.apollo.io/docs/create-api-key" target="_blank">Create API Keys</a> to learn how to create a master API key.

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
    "/emailer_campaigns/remove_or_stop_contact_ids": {
      "post": {
        "summary": "Update Contact Status in a Sequence",
        "description": "Use the Update Contact Status in a Sequence endpoint to either mark contacts as having `finished` a sequence, or to remove them from a sequence entirely. <br><br>This endpoint requires a master API key. If you attempt to call the endpoint without a master key, you will receive a `403` response. Refer to <a href=\"https://docs.apollo.io/docs/create-api-key\" target=\"_blank\">Create API Keys</a> to learn how to create a master API key.",
        "operationId": "update-contact-status-sequence",
        "parameters": [
          {
            "name": "emailer_campaign_ids[]",
            "in": "query",
            "description": "The Apollo IDs for the sequences that you want to update. If you add multiple sequences, you will update the status of the contacts across the chosen sequences. <br><br>To find sequence IDs, call the <a href=\"https://docs.apollo.io/reference/search-for-sequences\" target=\"_blank\">Search for Sequences endpoint</a> and identify the `id` value for the sequence. <br><br>Example: `66e9e215ece19801b219997f`",
            "required": true,
            "schema": {
              "type": "array",
              "items": {
                "type": "string"
              }
            }
          },
          {
            "name": "contact_ids[]",
            "in": "query",
            "description": "The Apollo IDs for the contacts in the sequences. These are the contacts whose sequence status you want to update. <br><br>To find contact IDs, call the <a href=\"https://docs.apollo.io/reference/search-for-contacts\" target=\"_blank\">Search for Contacts endpoint</a> and identify the `id` value for the contact. <br><br>Example: `66e34b81740c50074e3d1bd4`",
            "required": true,
            "schema": {
              "type": "array",
              "items": {
                "type": "string"
              }
            }
          },
          {
            "name": "mode",
            "in": "query",
            "description": "Choose 1 of the following options to update the sequence status of the contacts:   <ul> <li> `mark_as_finished`: Mark the contacts as having finished the sequence. </li> <li> `remove`: Remove the contacts from the sequence. </li> <li> `stop`: Indicate that the contacts progress in the sequence has halted.  </li> </ul>",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "OK": {
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
                          "custom_field_errors": {},
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
                              "inactive_reason": "manually finished",
                              "status": "finished",
                              "added_at": "2025-07-16T22:42:57.372+00:00",
                              "added_by_user_id": "60affe7d6e270a00f5db6fe4",
                              "finished_at": "2025-07-16T22:45:21.237+00:00",
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
                          "email_domain_catchall": false,
                          "typed_custom_fields": {
                            "5b75f1c11dc2727d43ae3bb9": "test",
                            "5c4296857f799409361890ea": "test2"
                          }
                        }
                      ],
                      "emailer_campaigns": [
                        {
                          "id": "66e9e215ece19801b219997f"
                        }
                      ],
                      "num_contacts": 3,
                      "contact_statuses": {
                        "active": "loading",
                        "failed": 0,
                        "paused": "loading",
                        "finished": "loading",
                        "bounced": "loading",
                        "hard_bounced": "loading",
                        "spam_blocked": "loading",
                        "not_sent": "loading"
                      },
                      "emailer_steps": [
                        {
                          "id": "66e9e232ece19801b21999a4",
                          "emailer_campaign_id": "66e9e215ece19801b219997f",
                          "position": 1,
                          "wait_time": 4,
                          "type": "auto_email",
                          "wait_mode": "hour",
                          "note": null,
                          "max_emails_per_day": null,
                          "exact_datetime": null,
                          "priority": null,
                          "auto_skip_in_x_days": null,
                          "counts": {
                            "active": 0,
                            "paused": 0,
                            "finished": 4,
                            "bounced": 0,
                            "spam_blocked": 0,
                            "hard_bounced": 0,
                            "not_sent": 0
                          },
                          "ab_test_details": {}
                        },
                        {
                          "id": "66e9e250ece19802d1196d07",
                          "emailer_campaign_id": "66e9e215ece19801b219997f",
                          "position": 2,
                          "wait_time": 3,
                          "type": "call",
                          "wait_mode": "day",
                          "note": "",
                          "max_emails_per_day": null,
                          "exact_datetime": null,
                          "priority": "high",
                          "auto_skip_in_x_days": null,
                          "counts": {
                            "active": 0,
                            "paused": 0,
                            "finished": 0,
                            "bounced": 0,
                            "spam_blocked": 0,
                            "hard_bounced": 0,
                            "not_sent": 0
                          },
                          "ab_test_details": {},
                          "note_text": "",
                          "unique_scheduled": "loading",
                          "unique_skipped": "loading",
                          "unique_completed": "loading",
                          "outcomes": []
                        },
                        {
                          "id": "66e9e265ece198053919497b",
                          "emailer_campaign_id": "66e9e215ece19801b219997f",
                          "position": 3,
                          "wait_time": 3,
                          "type": "action_item",
                          "wait_mode": "day",
                          "note": "Decide the next step to take for contacts in the sequence.",
                          "max_emails_per_day": null,
                          "exact_datetime": null,
                          "priority": "medium",
                          "auto_skip_in_x_days": null,
                          "counts": {
                            "active": 0,
                            "paused": 0,
                            "finished": 0,
                            "bounced": 0,
                            "spam_blocked": 0,
                            "hard_bounced": 0,
                            "not_sent": 0
                          },
                          "ab_test_details": {},
                          "unique_scheduled": "loading",
                          "unique_skipped": "loading",
                          "unique_completed": "loading"
                        }
                      ]
                    },
                    "summary": "OK"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "entity_progress_job": {
                      "type": "object",
                      "properties": {
                        "id": {
                          "type": "string",
                          "example": "66e9fca8cc087302d18b83be"
                        },
                        "user_id": {
                          "type": "string",
                          "example": "60affe7d6e270a00f5db6fe4"
                        },
                        "job_type": {
                          "type": "string",
                          "example": "sequence_remove_stop_contacts"
                        },
                        "entity_ids": {
                          "type": "array",
                          "items": {
                            "type": "string",
                            "example": "66e9e9e21fbdad01b2b33bbd"
                          }
                        },
                        "params": {
                          "type": "object",
                          "properties": {
                            "sequence_ids": {
                              "type": "array",
                              "items": {
                                "type": "string",
                                "example": "66e9e215ece19801b219997f"
                              }
                            },
                            "mode": {
                              "type": "string",
                              "example": "mark_as_finished"
                            },
                            "stop_reason": {},
                            "api_key": {
                              "type": "string",
                              "example": "EYTFL4PLnkGKwhplo2vQNQ"
                            },
                            "access_token": {}
                          }
                        },
                        "progress": {
                          "type": "integer",
                          "example": 0,
                          "default": 0
                        },
                        "batch_size": {
                          "type": "integer",
                          "example": 999,
                          "default": 0
                        }
                      }
                    }
                  }
                }
              }
            }
          },
          "401": {
            "description": "401",
            "content": {
              "text/plain": {
                "examples": {
                  "Check API key": {
                    "value": "Invalid access credentials."
                  }
                }
              }
            }
          },
          "403": {
            "description": "403",
            "content": {
              "application/json": {
                "examples": {
                  "Need master API key": {
                    "value": "{\n  \"error\": \"api/v1/emailer_campaigns/remove_or_stop_contact_ids is not accessible with this api_key\",\n  \"error_code\": \"API_INACCESSIBLE\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "error": {
                      "type": "string",
                      "example": "api/v1/emailer_campaigns/remove_or_stop_contact_ids is not accessible with this api_key"
                    },
                    "error_code": {
                      "type": "string",
                      "example": "API_INACCESSIBLE"
                    }
                  }
                }
              }
            }
          },
          "429": {
            "description": "429",
            "content": {
              "application/json": {
                "examples": {
                  "Too many requests": {
                    "value": "{\n    \"message\": \"The maximum number of api calls allowed for api/v1/emailer_campaigns/remove_or_stop_contact_ids is 600 times per hour. Please upgrade your plan from https://app.apollo.io/#/settings/plans/upgrade.\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "message": {
                      "type": "string",
                      "example": "The maximum number of api calls allowed for api/v1/emailer_campaigns/remove_or_stop_contact_ids is 600 times per hour. Please upgrade your plan from https://app.apollo.io/#/settings/plans/upgrade."
                    }
                  }
                }
              }
            }
          }
        },
        "deprecated": false
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