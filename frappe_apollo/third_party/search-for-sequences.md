Search for Sequences

# Search for Sequences

Use the Search for Sequences endpoint to search for the sequences that have been created for your team's Apollo account. <br><br>This endpoint requires a master API key. If you attempt to call the endpoint without a master key, you will receive a `403` response. Refer to <a href="https://docs.apollo.io/docs/create-api-key" target="_blank">Create API Keys</a> to learn how to create a master API key.

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
    "/emailer_campaigns/search": {
      "post": {
        "summary": "Search for Sequences",
        "description": "Use the Search for Sequences endpoint to search for the sequences that have been created for your team's Apollo account. <br><br>This endpoint requires a master API key. If you attempt to call the endpoint without a master key, you will receive a `403` response. Refer to <a href=\"https://docs.apollo.io/docs/create-api-key\" target=\"_blank\">Create API Keys</a> to learn how to create a master API key.",
        "operationId": "search-for-sequences",
        "parameters": [
          {
            "name": "q_name",
            "in": "query",
            "description": "Add keywords to narrow the search of the sequences in your team's Apollo account. <br><br>Keywords should directly match at least part of a sequence's name. For example, searching the keyword `marketing` might return the result `NY Marketing Sequence`, but not `NY Marketer Conference 2025 attendees`. <br><br>This parameter only searches sequence names, not other sequence fields. <br><br>Example: `marketing conference attendees`",
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "page",
            "in": "query",
            "description": "The page number of the Apollo data that you want to retrieve. <br><br>Use this parameter in combination with the `per_page` parameter to make search results for navigable and improve the performance of the endpoint. <br><br>Example: `4`",
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "per_page",
            "in": "query",
            "description": "The number of search results that should be returned for each page. Limiting the number of results per page improves the endpoint's performance. <br><br>Use the `page` parameter to search the different pages of data. <br><br>Example: `10`",
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
                  "Result": {
                    "value": {
                      "pagination": {
                        "page": 1,
                        "per_page": 5,
                        "total_entries": 1,
                        "total_pages": 1
                      },
                      "breadcrumbs": [
                        {
                          "label": "Name",
                          "signal_field_name": "q_name",
                          "value": "Copywriting Dublin",
                          "display_name": "Copywriting Dublin"
                        }
                      ],
                      "emailer_campaigns": [
                        {
                          "id": "66e9e215ece19801b219997f",
                          "name": "Target Copywriting Clients in Dublin",
                          "archived": false,
                          "created_at": "2024-09-17T20:09:57.837Z",
                          "emailer_schedule_id": "6095a711bd01d100a506d52a",
                          "max_emails_per_day": null,
                          "user_id": "66302798d03b9601c7934ebf",
                          "same_account_reply_policy_cd": null,
                          "excluded_account_stage_ids": [
                            "6095a710bd01d100a506d4b8",
                            "6095a710bd01d100a506d4b9",
                            "6095a710bd01d100a506d4ba",
                            "6095a710bd01d100a506d4bb"
                          ],
                          "excluded_contact_stage_ids": [
                            "6095a710bd01d100a506d4b5",
                            "6095a710bd01d100a506d4b4",
                            "6095a710bd01d100a506d4b0",
                            "6095a710bd01d100a506d4b1"
                          ],
                          "contact_email_event_to_stage_mapping": {},
                          "label_ids": [
                            "66e9e215ece19801b2199980",
                            "66e9e215ece19801b2199981",
                            "66e9e215ece19801b2199982"
                          ],
                          "create_task_if_email_open": false,
                          "email_open_trigger_task_threshold": 3,
                          "mark_finished_if_click": false,
                          "active": false,
                          "days_to_wait_before_mark_as_response": 5,
                          "starred_by_user_ids": [
                            "66302798d03b9601c7934ebf"
                          ],
                          "mark_finished_if_reply": true,
                          "mark_finished_if_interested": true,
                          "mark_paused_if_ooo": true,
                          "sequence_by_exact_daytime": null,
                          "permissions": "team_can_use",
                          "last_used_at": null,
                          "sequence_ruleset_id": "6095a711bd01d100a506d4e0",
                          "folder_id": null,
                          "same_account_reply_delay_days": 30,
                          "is_performing_poorly": false,
                          "num_contacts_email_status_extrapolated": 0,
                          "remind_ab_test_results": false,
                          "ab_test_step_ids": [],
                          "prioritized_by_user": null,
                          "creation_type": "new",
                          "num_steps": 3,
                          "unique_scheduled": 0,
                          "unique_delivered": 0,
                          "unique_bounced": 0,
                          "unique_opened": 0,
                          "unique_hard_bounced": 0,
                          "unique_spam_blocked": 0,
                          "unique_replied": 0,
                          "unique_demoed": 0,
                          "unique_clicked": 0,
                          "unique_unsubscribed": 0,
                          "bounce_rate": 0,
                          "hard_bounce_rate": 0,
                          "open_rate": 0,
                          "click_rate": 0,
                          "reply_rate": 0,
                          "spam_block_rate": 0,
                          "opt_out_rate": 0,
                          "demo_rate": 0,
                          "loaded_stats": true,
                          "cc_emails": "",
                          "bcc_emails": "",
                          "underperforming_touches_count": 0
                        }
                      ],
                      "num_fetch_result": null
                    }
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "pagination": {
                      "type": "object",
                      "properties": {
                        "page": {
                          "type": "integer",
                          "example": 1,
                          "default": 0
                        },
                        "per_page": {
                          "type": "integer",
                          "example": 5,
                          "default": 0
                        },
                        "total_entries": {
                          "type": "integer",
                          "example": 1,
                          "default": 0
                        },
                        "total_pages": {
                          "type": "integer",
                          "example": 1,
                          "default": 0
                        }
                      }
                    },
                    "breadcrumbs": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "label": {
                            "type": "string",
                            "example": "Name"
                          },
                          "signal_field_name": {
                            "type": "string",
                            "example": "q_name"
                          },
                          "value": {
                            "type": "string",
                            "example": "Copywriting Dublin"
                          },
                          "display_name": {
                            "type": "string",
                            "example": "Copywriting Dublin"
                          }
                        }
                      }
                    },
                    "emailer_campaigns": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "string",
                            "example": "66e9e215ece19801b219997f"
                          },
                          "name": {
                            "type": "string",
                            "example": "Target Copywriting Clients in Dublin"
                          },
                          "archived": {
                            "type": "boolean",
                            "example": false,
                            "default": true
                          },
                          "created_at": {
                            "type": "string",
                            "example": "2024-09-17T20:09:57.837Z"
                          },
                          "emailer_schedule_id": {
                            "type": "string",
                            "example": "6095a711bd01d100a506d52a"
                          },
                          "max_emails_per_day": {},
                          "user_id": {
                            "type": "string",
                            "example": "66302798d03b9601c7934ebf"
                          },
                          "same_account_reply_policy_cd": {},
                          "excluded_account_stage_ids": {
                            "type": "array",
                            "items": {
                              "type": "string",
                              "example": "6095a710bd01d100a506d4b8"
                            }
                          },
                          "excluded_contact_stage_ids": {
                            "type": "array",
                            "items": {
                              "type": "string",
                              "example": "6095a710bd01d100a506d4b5"
                            }
                          },
                          "contact_email_event_to_stage_mapping": {
                            "type": "object",
                            "properties": {}
                          },
                          "label_ids": {
                            "type": "array",
                            "items": {
                              "type": "string",
                              "example": "66e9e215ece19801b2199980"
                            }
                          },
                          "create_task_if_email_open": {
                            "type": "boolean",
                            "example": false,
                            "default": true
                          },
                          "email_open_trigger_task_threshold": {
                            "type": "integer",
                            "example": 3,
                            "default": 0
                          },
                          "mark_finished_if_click": {
                            "type": "boolean",
                            "example": false,
                            "default": true
                          },
                          "active": {
                            "type": "boolean",
                            "example": false,
                            "default": true
                          },
                          "days_to_wait_before_mark_as_response": {
                            "type": "integer",
                            "example": 5,
                            "default": 0
                          },
                          "starred_by_user_ids": {
                            "type": "array",
                            "items": {
                              "type": "string",
                              "example": "66302798d03b9601c7934ebf"
                            }
                          },
                          "mark_finished_if_reply": {
                            "type": "boolean",
                            "example": true,
                            "default": true
                          },
                          "mark_finished_if_interested": {
                            "type": "boolean",
                            "example": true,
                            "default": true
                          },
                          "mark_paused_if_ooo": {
                            "type": "boolean",
                            "example": true,
                            "default": true
                          },
                          "sequence_by_exact_daytime": {},
                          "permissions": {
                            "type": "string",
                            "example": "team_can_use"
                          },
                          "last_used_at": {},
                          "sequence_ruleset_id": {
                            "type": "string",
                            "example": "6095a711bd01d100a506d4e0"
                          },
                          "folder_id": {},
                          "same_account_reply_delay_days": {
                            "type": "integer",
                            "example": 30,
                            "default": 0
                          },
                          "is_performing_poorly": {
                            "type": "boolean",
                            "example": false,
                            "default": true
                          },
                          "num_contacts_email_status_extrapolated": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "remind_ab_test_results": {
                            "type": "boolean",
                            "example": false,
                            "default": true
                          },
                          "ab_test_step_ids": {
                            "type": "array"
                          },
                          "prioritized_by_user": {},
                          "creation_type": {
                            "type": "string",
                            "example": "new"
                          },
                          "num_steps": {
                            "type": "integer",
                            "example": 3,
                            "default": 0
                          },
                          "unique_scheduled": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "unique_delivered": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "unique_bounced": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "unique_opened": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "unique_hard_bounced": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "unique_spam_blocked": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "unique_replied": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "unique_demoed": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "unique_clicked": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "unique_unsubscribed": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "bounce_rate": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "hard_bounce_rate": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "open_rate": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "click_rate": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "reply_rate": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "spam_block_rate": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "opt_out_rate": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "demo_rate": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "loaded_stats": {
                            "type": "boolean",
                            "example": true,
                            "default": true
                          },
                          "cc_emails": {
                            "type": "string",
                            "example": ""
                          },
                          "bcc_emails": {
                            "type": "string",
                            "example": ""
                          },
                          "underperforming_touches_count": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          }
                        }
                      }
                    },
                    "num_fetch_result": {}
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
                    "value": "{\n  \"error\": \"api/v1/emailer_campaigns/search is not accessible with this api_key\",\n  \"error_code\": \"API_INACCESSIBLE\"\n}"
                  },
                  "Check Apollo pricing plan": {
                    "value": "{\n  \"message\": \"This endpoint is only available to Apollo users on paid plans.\"\n}"
                  }
                },
                "schema": {
                  "oneOf": [
                    {
                      "title": "Need master API key",
                      "type": "object",
                      "properties": {
                        "error": {
                          "type": "string",
                          "example": "api/v1/emailer_campaigns/search is not accessible with this api_key"
                        },
                        "error_code": {
                          "type": "string",
                          "example": "API_INACCESSIBLE"
                        }
                      }
                    },
                    {
                      "title": "Check Apollo pricing plan",
                      "type": "object",
                      "properties": {
                        "message": {
                          "type": "string",
                          "example": "This endpoint is only available to Apollo users on paid plans."
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
                    "value": "{\n    \"message\": \"The maximum number of api calls allowed for api/v1/emailer_campaigns/search is 600 times per hour. Please upgrade your plan from https://app.apollo.io/#/settings/plans/upgrade.\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "message": {
                      "type": "string",
                      "example": "The maximum number of api calls allowed for api/v1/emailer_campaigns/search is 600 times per hour. Please upgrade your plan from https://app.apollo.io/#/settings/plans/upgrade."
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