Create a Contact

# Create a Contact

Use the Create a Contact endpoint to add a new contact to your team's Apollo account. <br><br>In Apollo terminology, a contact is a person that your team has explicitly added to your database. A contact will have their data enriched in some way, such as accessing an email address or a phone number. <br><br>By default, Apollo does not apply deduplication processes when you create a new contact via the API. If your entry has the same name, email address, or other details as an existing contact, Apollo will create a new contact instead of updating the existing contact. To enable deduplication and prevent duplicate contacts,  set the <code>run_dedupe</code> parameter to <code>true</code>. <br><br>To update an existing contact, use the <a href="https://docs.apollo.io/reference/update-a-contact" target="_blank">Update a Contact endpoint</a> instead.

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
    "/contacts": {
      "post": {
        "summary": "Create a Contact",
        "description": "Use the Create a Contact endpoint to add a new contact to your team's Apollo account. <br><br>In Apollo terminology, a contact is a person that your team has explicitly added to your database. A contact will have their data enriched in some way, such as accessing an email address or a phone number. <br><br>By default, Apollo does not apply deduplication processes when you create a new contact via the API. If your entry has the same name, email address, or other details as an existing contact, Apollo will create a new contact instead of updating the existing contact. To enable deduplication and prevent duplicate contacts, set the `run_dedupe` parameter to `true`. <br><br>To update an existing contact, use the <a href=\"https://docs.apollo.io/reference/update-a-contact\" target=\"_blank\">Update a Contact endpoint</a> instead.",
        "operationId": "create-a-contact",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "first_name": {
                    "type": "string",
                    "description": "The first name of the contact you want to create. Example: `Tim`"
                  },
                  "last_name": {
                    "type": "string",
                    "description": "The last name of the contact you want to create. Example: `Zheng`"
                  },
                  "organization_name": {
                    "type": "string",
                    "description": "The name of the contact's employer (company). Example: `apollo`"
                  },
                  "title": {
                    "type": "string",
                    "description": "The current job title that the contact holds. Example: `senior research analyst`"
                  },
                  "account_id": {
                    "type": "string",
                    "description": "The Apollo ID for the account. Example: `63f53afe4ceeca00016bdd2f`"
                  },
                  "email": {
                    "type": "string",
                    "description": "The email address of the contact. Example: `example@email.com`"
                  },
                  "website_url": {
                    "type": "string",
                    "description": "The corporate website URL. Example: `https://www.apollo.io/`"
                  },
                  "label_names": {
                    "type": "array",
                    "description": "Lists to which the contact belongs.",
                    "items": {
                      "type": "string"
                    }
                  },
                  "contact_stage_id": {
                    "type": "string",
                    "description": "The Apollo ID for the contact stage. Example: `6095a710bd01d100a506d4ae`"
                  },
                  "present_raw_address": {
                    "type": "string",
                    "description": "The personal location for the contact. Example: `Atlanta, United States`"
                  },
                  "direct_phone": {
                    "type": "string",
                    "description": "The primary phone number. Example: `555-303-1234`"
                  },
                  "corporate_phone": {
                    "type": "string",
                    "description": "The work/office phone number. Example: `+44 7911 123456`"
                  },
                  "mobile_phone": {
                    "type": "string",
                    "description": "The mobile phone number. Example: `555-303-1234`"
                  },
                  "home_phone": {
                    "type": "string",
                    "description": "The home phone number. Example: `555-303-1234`"
                  },
                  "other_phone": {
                    "type": "string",
                    "description": "Alternative phone number. Example: `555-303-1234`"
                  },
                  "typed_custom_fields": {
                    "type": "object",
                    "description": "Add information to <a href=\"https://knowledge.apollo.io/hc/en-us/articles/4412498825869-Create-Custom-Contact-Fields\" target=\"_blank\">custom fields</a> in Apollo. <br><br><b>Your custom fields are unique to your team's Apollo account. This means that the examples in this documentation may not work for your testing purposes.</b> <br><br>To utilize this parameter successfully, call the <a href=\"https://docs.apollo.io/reference/get-a-list-of-all-custom-fields\">Get a List of All Custom Fields</a> endpoint and identify the `id` value for the custom field, as well as the appropriate data type. For example, if a custom field accepts picklist entries, you need to pass the accompanying `id` value for the picklist entry that you want to use as the input value. <br><br><b>Example</b>: When the <a href=\"https://docs.apollo.io/reference/get-a-list-of-all-custom-fields\">Get a List of All Custom Fields</a> endpoint returns an `id` of field: \n * `\"60c39ed82bd02f01154c470a\"` (datetime) \n \n\n then the value passed should be: \n\n `{\"60c39ed82bd02f01154c470a\": \"2025-08-07\"}`",
                    "additionalProperties": {
                      "type": "string"
                    },
                    "example": {
                      "60c39ed82bd02f01154c470a": "2025-08-07"
                    }
                  },
                  "run_dedupe": {
                    "type": "boolean",
                    "description": "Set to `true` to enable deduplication logic that prevents creating duplicate contacts. When enabled, Apollo will check for existing contacts with matching email addresses, names, or other identifying information and return the existing contact instead of creating a duplicate. The default value is `false`. <br><br>When deduplication is enabled, performance may be slightly impacted due to the additional validation checks, but this ensures data integrity and prevents duplicate entries in your database.",
                    "default": false
                  }
                }
              },
              "examples": {
                "Create contact without deduplication": {
                  "summary": "Create a new contact without deduplication (default behavior)",
                  "value": {
                    "first_name": "John",
                    "last_name": "Smith",
                    "email": "john.smith@example.com",
                    "organization_name": "Example Corp",
                    "title": "Software Engineer"
                  }
                },
                "Create contact with deduplication": {
                  "summary": "Create a new contact with deduplication enabled",
                  "value": {
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "email": "jane.doe@example.com",
                    "organization_name": "Example Corp",
                    "title": "Product Manager",
                    "run_dedupe": true
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": {
                      "contact": {
                        "contact_roles": [],
                        "id": "66e34b81740c50074e3d1bd4",
                        "first_name": "Fyodor",
                        "last_name": "Dostoevsky",
                        "name": "Fyodor Dostoevsky",
                        "linkedin_url": null,
                        "title": "Chief Fiction Writer",
                        "contact_stage_id": "6095a710bd01d100a506d4ae",
                        "owner_id": "60affe7d6e270a00f5db6fe4",
                        "creator_id": "60affe7d6e270a00f5db6fe4",
                        "person_id": null,
                        "email_needs_tickling": null,
                        "organization_name": "Apollo.io",
                        "source": "api",
                        "original_source": "api",
                        "organization_id": "5e66b6381e05b4008c8331b8",
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
                        "emailer_campaign_ids": [],
                        "direct_dial_status": null,
                        "direct_dial_enrichment_failed_at": null,
                        "email_status": "verified",
                        "email_source": null,
                        "account_id": "63f53afe4ceeca00016bdd2f",
                        "last_activity_date": null,
                        "hubspot_vid": null,
                        "hubspot_company_id": null,
                        "crm_id": null,
                        "sanitized_phone": "+15553031569",
                        "merged_crm_ids": null,
                        "updated_at": "2024-09-12T20:13:53.331Z",
                        "queued_for_crm_push": true,
                        "suggested_from_rule_engine_config_id": null,
                        "email_unsubscribed": null,
                        "label_ids": [
                          "66e34b81740c50074e3d1bd0",
                          "66e34b81740c50074e3d1bd1",
                          "66e34b81740c50074e3d1bd2",
                          "66e34b81740c50074e3d1bd3"
                        ],
                        "has_pending_email_arcgate_request": false,
                        "has_email_arcgate_request": false,
                        "existence_level": "full",
                        "email": "fyodo@apollo.io",
                        "email_from_customer": true,
                        "custom_field_errors": {},
                        "crm_record_url": null,
                        "email_status_unavailable_reason": null,
                        "email_true_status": "User Managed",
                        "updated_email_true_status": true,
                        "contact_rule_config_statuses": [],
                        "source_display_name": "Created from API",
                        "twitter_url": null,
                        "contact_campaign_statuses": [],
                        "contact_emails": [],
                        "next_contact_id": null,
                        "time_zone": "Asia/Krasnoyarsk",
                        "city": "Saint Petersburg",
                        "state": "Saint Petersburg",
                        "country": "Russia",
                        "intent_strength": null,
                        "show_intent": false,
                        "phone_numbers": [
                          {
                            "raw_number": "555-303-1569",
                            "sanitized_number": "+15553031569",
                            "type": "work_direct",
                            "position": 0,
                            "status": "no_status",
                            "dnc_status": null,
                            "dnc_other_info": null,
                            "dialer_flags": null
                          }
                        ],
                        "account_phone_note": null,
                        "free_domain": false,
                        "is_likely_to_engage": false,
                        "email_domain_catchall": false,
                        "typed_custom_fields": {
                          "5b75f1c11dc2727d43ae3bb9": "test",
                          "5c4296857f799409361890ea": "test2"
                        }
                      },
                      "labels": [
                        {
                          "id": "66e34b81740c50074e3d1bd2",
                          "modality": "contacts",
                          "cached_count": 0,
                          "name": "typewriter",
                          "created_at": "2024-09-12T20:13:53.119Z",
                          "updated_at": "2024-09-12T20:13:53.279Z",
                          "user_id": "60affe7d6e270a00f5db6fe4"
                        },
                        {
                          "id": "66e34b81740c50074e3d1bd1",
                          "modality": "contacts",
                          "cached_count": 0,
                          "name": "fiction",
                          "created_at": "2024-09-12T20:13:53.107Z",
                          "updated_at": "2024-09-12T20:13:53.258Z",
                          "user_id": "60affe7d6e270a00f5db6fe4"
                        },
                        {
                          "id": "66e34b81740c50074e3d1bd0",
                          "modality": "contacts",
                          "cached_count": 0,
                          "name": "writer",
                          "created_at": "2024-09-12T20:13:53.093Z",
                          "updated_at": "2024-09-12T20:13:53.308Z",
                          "user_id": "60affe7d6e270a00f5db6fe4"
                        },
                        {
                          "id": "66e34b81740c50074e3d1bd3",
                          "modality": "contacts",
                          "cached_count": 0,
                          "name": "microsoft word",
                          "created_at": "2024-09-12T20:13:53.132Z",
                          "updated_at": "2024-09-12T20:13:53.313Z",
                          "user_id": "60affe7d6e270a00f5db6fe4"
                        }
                      ]
                    }
                  },
                  "Deduplication-Result": {
                    "summary": "Contact creation with deduplication enabled - existing contact found",
                    "value": {
                      "contact": {
                        "contact_roles": [],
                        "id": "66e34b81740c50074e3d1bd4",
                        "first_name": "Jane",
                        "last_name": "Doe",
                        "name": "Jane Doe",
                        "linkedin_url": null,
                        "title": "Product Manager",
                        "contact_stage_id": "6095a710bd01d100a506d4ae",
                        "owner_id": "60affe7d6e270a00f5db6fe4",
                        "creator_id": "60affe7d6e270a00f5db6fe4",
                        "person_id": null,
                        "email_needs_tickling": null,
                        "organization_name": "Example Corp",
                        "source": "api",
                        "original_source": "api",
                        "organization_id": "5e66b6381e05b4008c8331b8",
                        "headline": null,
                        "photo_url": null,
                        "present_raw_address": null,
                        "linkedin_uid": null,
                        "extrapolated_email_confidence": null,
                        "salesforce_id": null,
                        "salesforce_lead_id": null,
                        "salesforce_contact_id": null,
                        "salesforce_account_id": null,
                        "crm_owner_id": null,
                        "created_at": "2024-09-12T20:13:53.207Z",
                        "emailer_campaign_ids": [],
                        "direct_dial_status": null,
                        "direct_dial_enrichment_failed_at": null,
                        "email_status": "verified",
                        "email_source": null,
                        "account_id": "63f53afe4ceeca00016bdd2f",
                        "last_activity_date": null,
                        "hubspot_vid": null,
                        "hubspot_company_id": null,
                        "crm_id": null,
                        "sanitized_phone": null,
                        "merged_crm_ids": null,
                        "updated_at": "2024-09-12T20:13:53.331Z",
                        "queued_for_crm_push": false,
                        "suggested_from_rule_engine_config_id": null,
                        "email_unsubscribed": null,
                        "label_ids": [],
                        "has_pending_email_arcgate_request": false,
                        "has_email_arcgate_request": false,
                        "existence_level": "full",
                        "email": "jane.doe@example.com",
                        "email_from_customer": true,
                        "custom_field_errors": {},
                        "crm_record_url": null,
                        "email_status_unavailable_reason": null,
                        "email_true_status": "User Managed",
                        "updated_email_true_status": true,
                        "contact_rule_config_statuses": [],
                        "source_display_name": "Created from API",
                        "twitter_url": null,
                        "contact_campaign_statuses": [],
                        "contact_emails": [],
                        "next_contact_id": null,
                        "time_zone": null,
                        "city": null,
                        "state": null,
                        "country": null,
                        "intent_strength": null,
                        "show_intent": false,
                        "phone_numbers": [],
                        "account_phone_note": null,
                        "free_domain": false,
                        "is_likely_to_engage": false,
                        "email_domain_catchall": false,
                        "typed_custom_fields": {}
                      },
                      "labels": [],
                      "dedupe_result": {
                        "found_existing": true,
                        "match_reason": "email_match",
                        "existing_contact_id": "66e34b81740c50074e3d1bd4"
                      }
                    }
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "contact": {
                      "type": "object",
                      "properties": {
                        "contact_roles": {
                          "type": "array"
                        },
                        "id": {
                          "type": "string",
                          "example": "66e34b81740c50074e3d1bd4"
                        },
                        "first_name": {
                          "type": "string",
                          "example": "Fyodor"
                        },
                        "last_name": {
                          "type": "string",
                          "example": "Dostoevsky"
                        },
                        "name": {
                          "type": "string",
                          "example": "Fyodor Dostoevsky"
                        },
                        "linkedin_url": {},
                        "title": {
                          "type": "string",
                          "example": "Chief Fiction Writer"
                        },
                        "contact_stage_id": {
                          "type": "string",
                          "example": "6095a710bd01d100a506d4ae"
                        },
                        "owner_id": {
                          "type": "string",
                          "example": "60affe7d6e270a00f5db6fe4"
                        },
                        "creator_id": {
                          "type": "string",
                          "example": "60affe7d6e270a00f5db6fe4"
                        },
                        "person_id": {},
                        "email_needs_tickling": {},
                        "organization_name": {
                          "type": "string",
                          "example": "Apollo.io"
                        },
                        "source": {
                          "type": "string",
                          "example": "api"
                        },
                        "original_source": {
                          "type": "string",
                          "example": "api"
                        },
                        "organization_id": {
                          "type": "string",
                          "example": "5e66b6381e05b4008c8331b8"
                        },
                        "headline": {},
                        "photo_url": {},
                        "present_raw_address": {
                          "type": "string",
                          "example": "St. Petersburg, Russia"
                        },
                        "linkedin_uid": {},
                        "extrapolated_email_confidence": {
                          "type": "number",
                          "nullable": true
                        },
                        "salesforce_id": {},
                        "salesforce_lead_id": {},
                        "salesforce_contact_id": {},
                        "salesforce_account_id": {},
                        "crm_owner_id": {},
                        "created_at": {
                          "type": "string",
                          "example": "2024-09-12T20:13:53.207Z"
                        },
                        "emailer_campaign_ids": {
                          "type": "array"
                        },
                        "direct_dial_status": {},
                        "direct_dial_enrichment_failed_at": {},
                        "email_status": {
                          "type": "string",
                          "example": "verified"
                        },
                        "email_source": {},
                        "account_id": {
                          "type": "string",
                          "example": "63f53afe4ceeca00016bdd2f"
                        },
                        "last_activity_date": {},
                        "hubspot_vid": {},
                        "hubspot_company_id": {},
                        "crm_id": {},
                        "sanitized_phone": {
                          "type": "string",
                          "example": "+15553031569"
                        },
                        "merged_crm_ids": {},
                        "updated_at": {
                          "type": "string",
                          "example": "2024-09-12T20:13:53.331Z"
                        },
                        "queued_for_crm_push": {
                          "type": "boolean",
                          "example": true,
                          "default": true
                        },
                        "suggested_from_rule_engine_config_id": {},
                        "email_unsubscribed": {},
                        "label_ids": {
                          "type": "array",
                          "items": {
                            "type": "string",
                            "example": "66e34b81740c50074e3d1bd0"
                          }
                        },
                        "has_pending_email_arcgate_request": {
                          "type": "boolean",
                          "example": false,
                          "default": true
                        },
                        "has_email_arcgate_request": {
                          "type": "boolean",
                          "example": false,
                          "default": true
                        },
                        "existence_level": {
                          "type": "string",
                          "example": "full"
                        },
                        "email": {
                          "type": "string",
                          "example": "fyodo@apollo.io"
                        },
                        "email_from_customer": {
                          "type": "boolean",
                          "example": true,
                          "default": true
                        },
                        "typed_custom_fields": {
                          "type": "object",
                          "properties": {}
                        },
                        "custom_field_errors": {
                          "type": "object",
                          "properties": {}
                        },
                        "crm_record_url": {},
                        "email_status_unavailable_reason": {},
                        "email_true_status": {
                          "type": "string",
                          "example": "User Managed"
                        },
                        "updated_email_true_status": {
                          "type": "boolean",
                          "example": true,
                          "default": true
                        },
                        "contact_rule_config_statuses": {
                          "type": "array"
                        },
                        "source_display_name": {
                          "type": "string",
                          "example": "Created from API"
                        },
                        "twitter_url": {},
                        "contact_campaign_statuses": {
                          "type": "array",
                          "description": "Array of campaign statuses for the contact, showing their participation in various email sequences",
                          "items": {
                            "type": "object",
                            "description": "Contact campaign status object representing the contact's current state in a specific email sequence",
                            "properties": {
                              "id": {
                                "type": "string",
                                "description": "Unique identifier for this contact campaign status record",
                                "example": "68782af181c7f0002159df25"
                              },
                              "emailer_campaign_id": {
                                "type": "string",
                                "description": "ID of the email sequence (emailer campaign) this status belongs to",
                                "example": "66e9e215ece19801b219997f"
                              },
                              "send_email_from_user_id": {
                                "type": "string",
                                "description": "ID of the user who is sending emails for this contact in the sequence",
                                "example": "66302798d03b9601c7934ebf"
                              },
                              "inactive_reason": {
                                "type": "string",
                                "nullable": true,
                                "description": "Reason why the contact is inactive in this sequence, if applicable",
                                "example": "Sequence inactive"
                              },
                              "status": {
                                "type": "string",
                                "description": "Current status of the contact in this email sequence",
                                "enum": [
                                  "active",
                                  "failed",
                                  "paused",
                                  "finished"
                                ],
                                "example": "paused"
                              },
                              "added_at": {
                                "type": "string",
                                "format": "date-time",
                                "description": "Timestamp when the contact was added to this sequence",
                                "example": "2025-07-16T22:42:57.372+00:00"
                              },
                              "added_by_user_id": {
                                "type": "string",
                                "description": "ID of the user who added this contact to the sequence",
                                "example": "60affe7d6e270a00f5db6fe4"
                              },
                              "finished_at": {
                                "type": "string",
                                "format": "date-time",
                                "nullable": true,
                                "description": "Timestamp when the contact finished/completed the sequence",
                                "example": null
                              },
                              "paused_at": {
                                "type": "string",
                                "format": "date-time",
                                "nullable": true,
                                "description": "Timestamp when the contact was paused in the sequence",
                                "example": null
                              },
                              "auto_unpause_at": {
                                "type": "string",
                                "format": "date-time",
                                "nullable": true,
                                "description": "Scheduled timestamp for automatically unpausing the contact",
                                "example": null
                              },
                              "send_email_from_email_address": {
                                "type": "string",
                                "nullable": true,
                                "description": "Specific email address used to send emails to this contact",
                                "example": "test.brandan.blevins@apollomail.io"
                              },
                              "send_email_from_email_account_id": {
                                "type": "string",
                                "description": "ID of the email account used to send emails to this contact",
                                "example": "6633baaece5fbd01c791d7ca"
                              },
                              "manually_set_unpause": {
                                "type": "boolean",
                                "nullable": true,
                                "description": "Whether the unpause was manually set by a user",
                                "example": null
                              },
                              "failure_reason": {
                                "type": "string",
                                "nullable": true,
                                "description": "Specific reason for failure if status is 'failed'",
                                "enum": [
                                  "hard_bounced",
                                  "spam_blocked",
                                  "bounced",
                                  "past_date_failure"
                                ],
                                "example": null
                              },
                              "current_step_id": {
                                "type": "string",
                                "nullable": true,
                                "description": "ID of the current step in the sequence that the contact is on",
                                "example": null
                              },
                              "in_response_to_emailer_message_id": {
                                "type": "string",
                                "nullable": true,
                                "description": "ID of the emailer message this campaign status is in response to",
                                "example": null
                              },
                              "cc_emails": {
                                "type": "array",
                                "nullable": true,
                                "description": "Email addresses to CC when sending emails to this contact",
                                "items": {
                                  "type": "string"
                                },
                                "example": null
                              },
                              "bcc_emails": {
                                "type": "array",
                                "nullable": true,
                                "description": "Email addresses to BCC when sending emails to this contact",
                                "items": {
                                  "type": "string"
                                },
                                "example": null
                              },
                              "to_emails": {
                                "type": "array",
                                "nullable": true,
                                "description": "Additional email addresses to include in TO field when sending emails",
                                "items": {
                                  "type": "string"
                                },
                                "example": null
                              },
                              "current_step_position": {
                                "type": "integer",
                                "nullable": true,
                                "description": "Position number of the current step in the sequence (1-based indexing)",
                                "example": null
                              }
                            },
                            "required": [
                              "id",
                              "emailer_campaign_id",
                              "send_email_from_user_id",
                              "status",
                              "added_at",
                              "added_by_user_id",
                              "send_email_from_email_account_id"
                            ]
                          }
                        },
                        "contact_emails": {
                          "type": "array"
                        },
                        "next_contact_id": {},
                        "time_zone": {
                          "type": "string",
                          "example": "Asia/Krasnoyarsk"
                        },
                        "city": {
                          "type": "string",
                          "example": "Saint Petersburg"
                        },
                        "state": {
                          "type": "string",
                          "example": "Saint Petersburg"
                        },
                        "country": {
                          "type": "string",
                          "example": "Russia"
                        },
                        "intent_strength": {},
                        "show_intent": {
                          "type": "boolean",
                          "example": false,
                          "default": true
                        },
                        "phone_numbers": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "raw_number": {
                                "type": "string",
                                "example": "555-303-1569"
                              },
                              "sanitized_number": {
                                "type": "string",
                                "example": "+15553031569"
                              },
                              "type": {
                                "type": "string",
                                "example": "work_direct"
                              },
                              "position": {
                                "type": "integer",
                                "example": 0,
                                "default": 0
                              },
                              "status": {
                                "type": "string",
                                "example": "no_status"
                              },
                              "dnc_status": {},
                              "dnc_other_info": {},
                              "dialer_flags": {}
                            }
                          }
                        },
                        "account_phone_note": {},
                        "free_domain": {
                          "type": "boolean",
                          "example": false,
                          "default": true
                        },
                        "is_likely_to_engage": {
                          "type": "boolean",
                          "example": false,
                          "default": true
                        },
                        "email_domain_catchall": {
                          "type": "boolean",
                          "example": false,
                          "default": true
                        }
                      }
                    },
                    "labels": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "string",
                            "example": "66e34b81740c50074e3d1bd2"
                          },
                          "modality": {
                            "type": "string",
                            "example": "contacts"
                          },
                          "cached_count": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "name": {
                            "type": "string",
                            "example": "typewriter"
                          },
                          "created_at": {
                            "type": "string",
                            "example": "2024-09-12T20:13:53.119Z"
                          },
                          "updated_at": {
                            "type": "string",
                            "example": "2024-09-12T20:13:53.279Z"
                          },
                          "user_id": {
                            "type": "string",
                            "example": "60affe7d6e270a00f5db6fe4"
                          }
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
          "422": {
            "description": "422",
            "content": {
              "application/json": {
                "examples": {
                  "Check the account ID": {
                    "value": "{\n  \"error\": \"Parameters misconfigured. 63f53afe4ceeca00016bdd2fsfsdf is not a valid ID\"\n}"
                  },
                  "Check the contact stage ID": {
                    "value": "{\n  \"error\": \"Parameters misconfigured. 2342432 is not a valid ID\"\n}"
                  }
                },
                "schema": {
                  "oneOf": [
                    {
                      "title": "Check the account ID",
                      "type": "object",
                      "properties": {
                        "error": {
                          "type": "string",
                          "example": "Parameters misconfigured. 63f53afe4ceeca00016bdd2fsfsdf is not a valid ID"
                        }
                      }
                    },
                    {
                      "title": "Check the contact stage ID",
                      "type": "object",
                      "properties": {
                        "error": {
                          "type": "string",
                          "example": "Parameters misconfigured. 2342432 is not a valid ID"
                        }
                      }
                    }
                  ]
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
                    "value": "{\n    \"message\": \"The maximum number of api calls allowed for api/v1/contacts is 600 times per hour. Please upgrade your plan from https://app.apollo.io/#/settings/plans/upgrade.\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "message": {
                      "type": "string",
                      "example": "The maximum number of api calls allowed for api/v1/contacts is 600 times per hour. Please upgrade your plan from https://app.apollo.io/#/settings/plans/upgrade."
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