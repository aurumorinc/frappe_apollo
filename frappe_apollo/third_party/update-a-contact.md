Update a Contact

# Update a Contact

Use the Update a Contact endpoint to update existing contacts in your team's Apollo account. <br><br>In Apollo terminology, a contact is a person that your team has explicitly added to your database. A contact will have their data enriched in some way, such as accessing an email address or a phone number. <br><br>To create a new contact, use the <a href="https://docs.apollo.io/reference/create-a-contact" target="_blank">Create a Contact endpoint</a> instead. To update the contact stage for multiple contacts, use the <a href="https://docs.apollo.io/reference/update-contact-stage" target="_blank">Update Contact Stage for Multiple Contacts</a> endpoint.

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
    "/contacts/{contact_id}": {
      "patch": {
        "summary": "Update a Contact",
        "description": "Use the Update a Contact endpoint to update existing contacts in your team's Apollo account. <br><br>In Apollo terminology, a contact is a person that your team has explicitly added to your database. A contact will have their data enriched in some way, such as accessing an email address or a phone number. <br><br>To create a new contact, use the <a href=\"https://docs.apollo.io/reference/create-a-contact\" target=\"_blank\">Create a Contact endpoint</a> instead. To update the contact stage for multiple contacts, use the <a href=\"https://docs.apollo.io/reference/update-contact-stage\" target=\"_blank\">Update Contact Stage for Multiple Contacts</a> endpoint.",
        "operationId": "update-a-contact",
        "parameters": [
          {
            "name": "contact_id",
            "in": "path",
            "description": "The Apollo ID for the contact that you want to update. <br><br>To find contact IDs, call the <a href=\"https://docs.apollo.io/reference/search-for-contacts\" target=\"_blank\">Search for Contacts endpoint</a> and identify the `id` value for the contact. <br><br>Example: `66e34b81740c50074e3d1bd4`",
            "schema": {
              "type": "string"
            },
            "required": true
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "first_name": {
                    "type": "string",
                    "description": "Update the contact's first name. Example: `Tim`"
                  },
                  "last_name": {
                    "type": "string",
                    "description": "Update the contact's last name. Example: `Zheng`"
                  },
                  "organization_name": {
                    "type": "string",
                    "description": "Update the employer (company) name. Example: `apollo`"
                  },
                  "title": {
                    "type": "string",
                    "description": "Update the job title. Example: `senior research analyst`"
                  },
                  "account_id": {
                    "type": "string",
                    "description": "Update the account ID. Example: `63f53afe4ceeca00016bdd2f`"
                  },
                  "email": {
                    "type": "string",
                    "description": "Update the contact email. Example: `example@email.com`"
                  },
                  "website_url": {
                    "type": "string",
                    "description": "Update the employer website URL. Example: `https://www.apollo.io/`"
                  },
                  "label_names": {
                    "type": "array",
                    "description": "Replace lists this contact belongs to. (Passing new values will overwrite existing lists.)",
                    "items": {
                      "type": "string"
                    }
                  },
                  "contact_stage_id": {
                    "type": "string",
                    "description": "Update the contact stage ID. Example: `6095a710bd01d100a506d4af`"
                  },
                  "present_raw_address": {
                    "type": "string",
                    "description": "Update location (city/state/country). Example: `Atlanta, United States`"
                  },
                  "direct_phone": {
                    "type": "string",
                    "description": "Primary phone."
                  },
                  "corporate_phone": {
                    "type": "string",
                    "description": "Work/office phone."
                  },
                  "mobile_phone": {
                    "type": "string",
                    "description": "Mobile phone."
                  },
                  "home_phone": {
                    "type": "string",
                    "description": "Home phone."
                  },
                  "other_phone": {
                    "type": "string",
                    "description": "Alternate phone."
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
                        "title": "Chief Writer",
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
                        "sanitized_phone": "+15553039182",
                        "merged_crm_ids": null,
                        "updated_at": "2024-09-12T20:14:53.134Z",
                        "queued_for_crm_push": false,
                        "suggested_from_rule_engine_config_id": null,
                        "email_unsubscribed": null,
                        "label_ids": [
                          "66e361494acd1307386d4073"
                        ],
                        "typed_custom_fields": {
                          "5b75f1c11dc2727d43ae3bb9": "test",
                          "5c4296857f799409361890ea": "test2"
                        },
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
                        "contact_rule_config_statuses": [],
                        "source_display_name": "Created from API",
                        "twitter_url": null,
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
                            "raw_number": "555-303-9182",
                            "sanitized_number": "+15553039182",
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
                        "email_domain_catchall": false
                      },
                      "labels": [
                        {
                          "id": "66e361494acd1307386d4073",
                          "modality": "contacts",
                          "cached_count": 0,
                          "name": "2024 fiction writers of america attendees",
                          "created_at": "2024-09-12T21:46:49.464Z",
                          "updated_at": "2024-09-12T21:46:49.544Z",
                          "user_id": "60affe7d6e270a00f5db6fe4"
                        }
                      ]
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
                          "example": "Chief Writer"
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
                          "example": "+15553039182"
                        },
                        "merged_crm_ids": {},
                        "updated_at": {
                          "type": "string",
                          "example": "2024-09-12T20:14:53.134Z"
                        },
                        "queued_for_crm_push": {
                          "type": "boolean",
                          "example": false,
                          "default": true
                        },
                        "suggested_from_rule_engine_config_id": {},
                        "email_unsubscribed": {},
                        "label_ids": {
                          "type": "array",
                          "items": {
                            "type": "string",
                            "example": "66e361494acd1307386d4073"
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
                          "example": "fyodor.dostoevsky@apollo.io"
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
                                "example": "555-303-9182"
                              },
                              "sanitized_number": {
                                "type": "string",
                                "example": "+15553039182"
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
                            "example": "66e361494acd1307386d4073"
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
                            "example": "2024 fiction writers of america attendees"
                          },
                          "created_at": {
                            "type": "string",
                            "example": "2024-09-12T21:46:49.464Z"
                          },
                          "updated_at": {
                            "type": "string",
                            "example": "2024-09-12T21:46:49.544Z"
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
                    "value": "{\n  \"error\": \"Parameters misconfigured. 5234234 is not a valid ID\"\n}"
                  },
                  "Check the contact stage ID": {
                    "value": "{\n  \"error\": \"Parameters misconfigured. 2342432 is not a valid ID\"\n}"
                  },
                  "Contact has been deleted": {
                    "value": "{\n  \"error\": \"Cannot update contact as it is deleted.\",\n  \"deleted_contact_ids\": [\n    \"66e34b81740c50074e3d1bd4\"\n  ]\n}"
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
                          "example": "Parameters misconfigured. 5234234 is not a valid ID"
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
                    },
                    {
                      "title": "Contact has been deleted",
                      "type": "object",
                      "properties": {
                        "error": {
                          "type": "string",
                          "example": "Cannot update contact as it is deleted."
                        },
                        "deleted_contact_ids": {
                          "type": "array",
                          "items": {
                            "type": "string",
                            "example": "66e34b81740c50074e3d1bd4"
                          }
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
                    "value": "{\n    \"message\": \"The maximum number of api calls allowed for api/v1/contacts/{contact_id} is 600 times per hour. Please upgrade your plan from https://app.apollo.io/#/settings/plans/upgrade.\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "message": {
                      "type": "string",
                      "example": "The maximum number of api calls allowed for api/v1/contacts/{contact_id} is 600 times per hour. Please upgrade your plan from https://app.apollo.io/#/settings/plans/upgrade."
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