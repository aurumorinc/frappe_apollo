Get a List of Email Accounts

# Get a List of Email Accounts

Use the Get a List of Email Accounts endpoint to retrieve information about the linked email inboxes that your teammates use in your Apollo account. <br><br>In particular, this endpoint returns IDs for each of your team's linked email accounts, which can be used with the <a href="https://docs.apollo.io/reference/add-contacts-to-sequence" target="_blank">Add Contacts to a Sequence endpoint</a>. <br><br>This endpoint does not require any parameters. <br><br>This endpoint requires a master API key. If you attempt to call the endpoint without a master key, you will receive a `403` response. Refer to <a href="https://docs.apollo.io/docs/create-api-key" target="_blank">Create API Keys</a> to learn how to create a master API key.

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
    "/email_accounts": {
      "get": {
        "summary": "Get a List of Email Accounts",
        "description": "Use the Get a List of Email Accounts endpoint to retrieve information about the linked email inboxes that your teammates use in your Apollo account. <br><br>In particular, this endpoint returns IDs for each of your team's linked email accounts, which can be used with the <a href=\"https://docs.apollo.io/reference/add-contacts-to-sequence\" target=\"_blank\">Add Contacts to a Sequence endpoint</a>. <br><br>This endpoint does not require any parameters. <br><br>This endpoint requires a master API key. If you attempt to call the endpoint without a master key, you will receive a `403` response. Refer to <a href=\"https://docs.apollo.io/docs/create-api-key\" target=\"_blank\">Create API Keys</a> to learn how to create a master API key.",
        "operationId": "get-a-list-of-email-accounts",
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n  \"email_accounts\": [\n    {\n      \"aliases\": [\n        \"test.james@apollomail.io\"\n      ],\n      \"id\": \"6630ffa2a7f52601c7578345\",\n      \"user_id\": \"66302798d03b9601c7934ebc\",\n      \"email\": \"test.james@apollomail.io\",\n      \"type\": \"gmail\",\n      \"active\": true,\n      \"default\": true,\n      \"seconds_delay_between_emails\": 600,\n      \"provider_display_name\": \"Gmail\",\n      \"nylas_provider\": null,\n      \"last_synced_at\": \"2024-09-19T18:50:45.088+00:00\",\n      \"email_sending_policy_cd\": \"default\",\n      \"sendgrid_api_user\": null,\n      \"mailgun_domains\": null,\n      \"nylas_api_version\": null,\n      \"signature_edit_disabled\": false,\n      \"revoked_at\": null,\n      \"inactive_reason\": null,\n      \"created_at\": \"2024-04-30T14:26:42.061Z\",\n      \"sendgrid_api_key_v3\": null,\n      \"email_daily_threshold\": 50,\n      \"deliverability_score\": {\n        \"_id\": \"66de4138d8a8a300016b404e\",\n        \"avg_click_rate\": 0,\n        \"avg_daily_sent\": 0,\n        \"avg_delivered_rate\": 0,\n        \"avg_hard_bounce_rate\": 0,\n        \"avg_open_rate\": 0,\n        \"avg_reply_rate\": 0,\n        \"avg_spam_block_rate\": 0,\n        \"avg_unsubscribe_rate\": 0,\n        \"click_rate_score\": 0,\n        \"concurrency_locks\": null,\n        \"created_at\": \"2024-09-09T00:28:41.695Z\",\n        \"daily_email_sent_score\": 0,\n        \"date_from\": \"2024-09-09\",\n        \"date_to\": \"2024-09-15\",\n        \"deliverability_score\": 0,\n        \"domain_health_score\": 5,\n        \"email_account_domain_age_score\": 5,\n        \"email_account_id\": \"6630ffa2a7f52601c7578345\",\n        \"hard_bounce_score\": 0,\n        \"open_rate_score\": 0,\n        \"random\": 0.6074748,\n        \"reply_rate_score\": 0,\n        \"spam_block_score\": 0,\n        \"sum_clicked_count\": 0,\n        \"sum_delivered_count\": 0,\n        \"sum_hard_bounced_count\": 0,\n        \"sum_opened_count\": 0,\n        \"sum_replied_count\": 0,\n        \"sum_sent_count\": 0,\n        \"sum_spam_blocked_count\": 0,\n        \"sum_unsubscribed_count\": 0,\n        \"team_id\": \"6095a710bd01d100a506d4ac\",\n        \"unsubscribe_rate_score\": 0,\n        \"updated_at\": \"2024-09-09T00:28:41.695Z\",\n        \"user_id\": \"66302798d03b9601c7934ebc\",\n        \"id\": \"66de4138d8a8a300016b404e\",\n        \"key\": \"66de4138d8a8a300016b404e\"\n      },\n      \"max_outbound_emails_per_hour\": 6,\n      \"limits_editable\": true,\n      \"is_opted_in_mailwarming\": null,\n      \"mailwarming_max\": 0,\n      \"mailwarming_to_send_daily\": 0,\n      \"mailwarming_to_send_incrementor\": 0,\n      \"mailwarming_status\": \"never_started\",\n      \"mailwarming_eta\": null,\n      \"mailwarming_subject_token\": null,\n      \"mailwarming_score\": 0,\n      \"mailwarming_score_banner\": \"start_warm_up_for_score\",\n      \"mailwarming_on_weekdays_only\": true,\n      \"true_warmup_enabled\": false,\n      \"true_warmup_daily_limit\": 0,\n      \"true_warmup_progress\": 0,\n      \"true_warmup_status\": null,\n      \"true_warmup_approximate_end_date\": null,\n      \"true_warmup_last_throttled_at\": null,\n      \"true_warmup_enable_thresholds\": false,\n      \"true_warmup_thresholds\": {\n        \"open_rate\": 20,\n        \"reply_rate\": 1,\n        \"bounce_rate\": 1,\n        \"spam_block_rate\": 1\n      },\n      \"active_campaigns_count\": 2,\n      \"nudge_user_to_send_mails\": true,\n      \"signature_html\": \"<div>James O'Sullivan</div><div>Apollo Academy Sales Instructor</div><div>james.osullivan@apollo.io</div><div><br></div><div><a href=\\\"http://www.berkley.edu\\\" rel=\\\"noopener noreferrer\\\" target=\\\"_blank\\\">Apollo Knowledge Base</a></div><div><br></div><div>Book time to meet with me <a href=\\\"https://app.apollo.io/#/meet/james_o'sullivan_ebc/30-min\\\" rel=\\\"noopener noreferrer\\\" target=\\\"_blank\\\">here</a>.</div>\",\n      \"fields_fully_loaded\": true\n    },\n    {\n      \"aliases\": [\n        \"test.janet@apollomail.io\"\n      ],\n      \"id\": \"6631066fab78f601c7b0a8bf\",\n      \"user_id\": \"663027d1d03b9606c1934335\",\n      \"email\": \"test.janet@apollomail.io\",\n      \"type\": \"gmail\",\n      \"active\": true,\n      \"default\": true,\n      \"seconds_delay_between_emails\": 500,\n      \"provider_display_name\": \"Gmail\",\n      \"nylas_provider\": null,\n      \"last_synced_at\": \"2024-09-19T18:49:21.990+00:00\",\n      \"email_sending_policy_cd\": \"default\",\n      \"sendgrid_api_user\": null,\n      \"mailgun_domains\": null,\n      \"nylas_api_version\": null,\n      \"signature_edit_disabled\": false,\n      \"revoked_at\": null,\n      \"inactive_reason\": null,\n      \"created_at\": \"2024-04-30T14:55:43.556Z\",\n      \"sendgrid_api_key_v3\": null,\n      \"email_daily_threshold\": 50,\n      \"deliverability_score\": {\n        \"_id\": \"66de40f0d8a8a300016b4014\",\n        \"avg_click_rate\": 0,\n        \"avg_daily_sent\": 0,\n        \"avg_delivered_rate\": 0,\n        \"avg_hard_bounce_rate\": 0,\n        \"avg_open_rate\": 0,\n        \"avg_reply_rate\": 0,\n        \"avg_spam_block_rate\": 0,\n        \"avg_unsubscribe_rate\": 0,\n        \"click_rate_score\": 0,\n        \"concurrency_locks\": null,\n        \"created_at\": \"2024-09-09T00:27:28.539Z\",\n        \"daily_email_sent_score\": 0,\n        \"date_from\": \"2024-09-09\",\n        \"date_to\": \"2024-09-15\",\n        \"deliverability_score\": 0,\n        \"domain_health_score\": 5,\n        \"email_account_domain_age_score\": 5,\n        \"email_account_id\": \"6631066fab78f601c7b0a8bf\",\n        \"hard_bounce_score\": 0,\n        \"open_rate_score\": 0,\n        \"random\": 0.64551977,\n        \"reply_rate_score\": 0,\n        \"spam_block_score\": 0,\n        \"sum_clicked_count\": 0,\n        \"sum_delivered_count\": 0,\n        \"sum_hard_bounced_count\": 0,\n        \"sum_opened_count\": 0,\n        \"sum_replied_count\": 0,\n        \"sum_sent_count\": 0,\n        \"sum_spam_blocked_count\": 0,\n        \"sum_unsubscribed_count\": 0,\n        \"team_id\": \"6095a710bd01d100a506d4ac\",\n        \"unsubscribe_rate_score\": 0,\n        \"updated_at\": \"2024-09-09T00:27:28.539Z\",\n        \"user_id\": \"663027d1d03b9606c1934335\",\n        \"id\": \"66de40f0d8a8a300016b4014\",\n        \"key\": \"66de40f0d8a8a300016b4014\"\n      },\n      \"max_outbound_emails_per_hour\": 6,\n      \"limits_editable\": true,\n      \"is_opted_in_mailwarming\": null,\n      \"mailwarming_max\": 0,\n      \"mailwarming_to_send_daily\": 0,\n      \"mailwarming_to_send_incrementor\": 0,\n      \"mailwarming_status\": \"never_started\",\n      \"mailwarming_eta\": null,\n      \"mailwarming_subject_token\": null,\n      \"mailwarming_score\": 0,\n      \"mailwarming_score_banner\": \"start_warm_up_for_score\",\n      \"mailwarming_on_weekdays_only\": true,\n      \"true_warmup_enabled\": false,\n      \"true_warmup_daily_limit\": 0,\n      \"true_warmup_progress\": 0,\n      \"true_warmup_status\": null,\n      \"true_warmup_approximate_end_date\": null,\n      \"true_warmup_last_throttled_at\": null,\n      \"true_warmup_enable_thresholds\": false,\n      \"true_warmup_thresholds\": {\n        \"open_rate\": 20,\n        \"reply_rate\": 1,\n        \"bounce_rate\": 1,\n        \"spam_block_rate\": 1\n      },\n      \"active_campaigns_count\": 2,\n      \"nudge_user_to_send_mails\": true,\n      \"signature_html\": \"<div>Janet Testing</div><div><a href=\\\"http://www.berkley.edu\\\" target=\\\"_blank\\\">Apollo Knowledge Base</a></div><div> </div>\",\n      \"fields_fully_loaded\": true\n    }\n  ]\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "email_accounts": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "aliases": {
                            "type": "array",
                            "items": {
                              "type": "string",
                              "example": "test.james@apollomail.io"
                            }
                          },
                          "id": {
                            "type": "string",
                            "example": "6630ffa2a7f52601c7578345"
                          },
                          "user_id": {
                            "type": "string",
                            "example": "66302798d03b9601c7934ebc"
                          },
                          "email": {
                            "type": "string",
                            "example": "test.james@apollomail.io"
                          },
                          "type": {
                            "type": "string",
                            "example": "gmail"
                          },
                          "active": {
                            "type": "boolean",
                            "example": true,
                            "default": true
                          },
                          "default": {
                            "type": "boolean",
                            "example": true,
                            "default": true
                          },
                          "seconds_delay_between_emails": {
                            "type": "integer",
                            "example": 600,
                            "default": 0
                          },
                          "provider_display_name": {
                            "type": "string",
                            "example": "Gmail"
                          },
                          "nylas_provider": {},
                          "last_synced_at": {
                            "type": "string",
                            "example": "2024-09-19T18:50:45.088+00:00"
                          },
                          "email_sending_policy_cd": {
                            "type": "string",
                            "example": "default"
                          },
                          "sendgrid_api_user": {},
                          "mailgun_domains": {},
                          "nylas_api_version": {},
                          "signature_edit_disabled": {
                            "type": "boolean",
                            "example": false,
                            "default": true
                          },
                          "revoked_at": {},
                          "inactive_reason": {},
                          "created_at": {
                            "type": "string",
                            "example": "2024-04-30T14:26:42.061Z"
                          },
                          "sendgrid_api_key_v3": {},
                          "email_daily_threshold": {
                            "type": "integer",
                            "example": 50,
                            "default": 0
                          },
                          "deliverability_score": {
                            "type": "object",
                            "properties": {
                              "_id": {
                                "type": "string",
                                "example": "66de4138d8a8a300016b404e"
                              },
                              "avg_click_rate": {
                                "type": "integer",
                                "example": 0,
                                "default": 0
                              },
                              "avg_daily_sent": {
                                "type": "integer",
                                "example": 0,
                                "default": 0
                              },
                              "avg_delivered_rate": {
                                "type": "integer",
                                "example": 0,
                                "default": 0
                              },
                              "avg_hard_bounce_rate": {
                                "type": "integer",
                                "example": 0,
                                "default": 0
                              },
                              "avg_open_rate": {
                                "type": "integer",
                                "example": 0,
                                "default": 0
                              },
                              "avg_reply_rate": {
                                "type": "integer",
                                "example": 0,
                                "default": 0
                              },
                              "avg_spam_block_rate": {
                                "type": "integer",
                                "example": 0,
                                "default": 0
                              },
                              "avg_unsubscribe_rate": {
                                "type": "integer",
                                "example": 0,
                                "default": 0
                              },
                              "click_rate_score": {
                                "type": "integer",
                                "example": 0,
                                "default": 0
                              },
                              "concurrency_locks": {},
                              "created_at": {
                                "type": "string",
                                "example": "2024-09-09T00:28:41.695Z"
                              },
                              "daily_email_sent_score": {
                                "type": "integer",
                                "example": 0,
                                "default": 0
                              },
                              "date_from": {
                                "type": "string",
                                "example": "2024-09-09"
                              },
                              "date_to": {
                                "type": "string",
                                "example": "2024-09-15"
                              },
                              "deliverability_score": {
                                "type": "integer",
                                "example": 0,
                                "default": 0
                              },
                              "domain_health_score": {
                                "type": "integer",
                                "example": 5,
                                "default": 0
                              },
                              "email_account_domain_age_score": {
                                "type": "integer",
                                "example": 5,
                                "default": 0
                              },
                              "email_account_id": {
                                "type": "string",
                                "example": "6630ffa2a7f52601c7578345"
                              },
                              "hard_bounce_score": {
                                "type": "integer",
                                "example": 0,
                                "default": 0
                              },
                              "open_rate_score": {
                                "type": "integer",
                                "example": 0,
                                "default": 0
                              },
                              "random": {
                                "type": "number",
                                "example": 0.6074748,
                                "default": 0
                              },
                              "reply_rate_score": {
                                "type": "integer",
                                "example": 0,
                                "default": 0
                              },
                              "spam_block_score": {
                                "type": "integer",
                                "example": 0,
                                "default": 0
                              },
                              "sum_clicked_count": {
                                "type": "integer",
                                "example": 0,
                                "default": 0
                              },
                              "sum_delivered_count": {
                                "type": "integer",
                                "example": 0,
                                "default": 0
                              },
                              "sum_hard_bounced_count": {
                                "type": "integer",
                                "example": 0,
                                "default": 0
                              },
                              "sum_opened_count": {
                                "type": "integer",
                                "example": 0,
                                "default": 0
                              },
                              "sum_replied_count": {
                                "type": "integer",
                                "example": 0,
                                "default": 0
                              },
                              "sum_sent_count": {
                                "type": "integer",
                                "example": 0,
                                "default": 0
                              },
                              "sum_spam_blocked_count": {
                                "type": "integer",
                                "example": 0,
                                "default": 0
                              },
                              "sum_unsubscribed_count": {
                                "type": "integer",
                                "example": 0,
                                "default": 0
                              },
                              "team_id": {
                                "type": "string",
                                "example": "6095a710bd01d100a506d4ac"
                              },
                              "unsubscribe_rate_score": {
                                "type": "integer",
                                "example": 0,
                                "default": 0
                              },
                              "updated_at": {
                                "type": "string",
                                "example": "2024-09-09T00:28:41.695Z"
                              },
                              "user_id": {
                                "type": "string",
                                "example": "66302798d03b9601c7934ebc"
                              },
                              "id": {
                                "type": "string",
                                "example": "66de4138d8a8a300016b404e"
                              },
                              "key": {
                                "type": "string",
                                "example": "66de4138d8a8a300016b404e"
                              }
                            }
                          },
                          "max_outbound_emails_per_hour": {
                            "type": "integer",
                            "example": 6,
                            "default": 0
                          },
                          "limits_editable": {
                            "type": "boolean",
                            "example": true,
                            "default": true
                          },
                          "is_opted_in_mailwarming": {},
                          "mailwarming_max": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "mailwarming_to_send_daily": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "mailwarming_to_send_incrementor": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "mailwarming_status": {
                            "type": "string",
                            "example": "never_started"
                          },
                          "mailwarming_eta": {},
                          "mailwarming_subject_token": {},
                          "mailwarming_score": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "mailwarming_score_banner": {
                            "type": "string",
                            "example": "start_warm_up_for_score"
                          },
                          "mailwarming_on_weekdays_only": {
                            "type": "boolean",
                            "example": true,
                            "default": true
                          },
                          "true_warmup_enabled": {
                            "type": "boolean",
                            "example": false,
                            "default": true
                          },
                          "true_warmup_daily_limit": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "true_warmup_progress": {
                            "type": "integer",
                            "example": 0,
                            "default": 0
                          },
                          "true_warmup_status": {},
                          "true_warmup_approximate_end_date": {},
                          "true_warmup_last_throttled_at": {},
                          "true_warmup_enable_thresholds": {
                            "type": "boolean",
                            "example": false,
                            "default": true
                          },
                          "true_warmup_thresholds": {
                            "type": "object",
                            "properties": {
                              "open_rate": {
                                "type": "integer",
                                "example": 20,
                                "default": 0
                              },
                              "reply_rate": {
                                "type": "integer",
                                "example": 1,
                                "default": 0
                              },
                              "bounce_rate": {
                                "type": "integer",
                                "example": 1,
                                "default": 0
                              },
                              "spam_block_rate": {
                                "type": "integer",
                                "example": 1,
                                "default": 0
                              }
                            }
                          },
                          "active_campaigns_count": {
                            "type": "integer",
                            "example": 2,
                            "default": 0
                          },
                          "nudge_user_to_send_mails": {
                            "type": "boolean",
                            "example": true,
                            "default": true
                          },
                          "signature_html": {
                            "type": "string",
                            "example": "<div>James O'Sullivan</div><div>Apollo Academy Sales Instructor</div><div>james.osullivan@apollo.io</div><div><br></div><div><a href=\"http://www.berkley.edu\" rel=\"noopener noreferrer\" target=\"_blank\">Apollo Knowledge Base</a></div><div><br></div><div>Book time to meet with me <a href=\"https://app.apollo.io/#/meet/james_o'sullivan_ebc/30-min\" rel=\"noopener noreferrer\" target=\"_blank\">here</a>.</div>"
                          },
                          "fields_fully_loaded": {
                            "type": "boolean",
                            "example": true,
                            "default": true
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
          "403": {
            "description": "403",
            "content": {
              "application/json": {
                "examples": {
                  "Need master API key": {
                    "value": "{\n  \"error\": \"api/v1/email_accounts/index is not accessible with this api_key\",\n  \"error_code\": \"API_INACCESSIBLE\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "error": {
                      "type": "string",
                      "example": "api/v1/email_accounts/index is not accessible with this api_key"
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
                    "value": "{\n    \"message\": \"The maximum number of api calls allowed for api/v1/email_accounts is 600 times per hour. Please upgrade your plan from https://app.apollo.io/#/settings/plans/upgrade.\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "message": {
                      "type": "string",
                      "example": "The maximum number of api calls allowed for api/v1/email_accounts is 600 times per hour. Please upgrade your plan from https://app.apollo.io/#/settings/plans/upgrade."
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