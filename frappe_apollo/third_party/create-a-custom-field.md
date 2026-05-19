Create a Custom Field

# Create a Custom Field

The Create a Custom Field endpoint lets you add custom fields to your Apollo account, helping your team capture unique details about <a href="https://knowledge.apollo.io/hc/en-us/articles/4412498825869-Create-Custom-Contact-Fields" target="_blank">contacts</a>, <a href="https://knowledge.apollo.io/hc/en-us/articles/4412498754445-Create-Custom-Account-Fields" target="_blank">accounts</a>, or <a href="https://knowledge.apollo.io/hc/en-us/articles/4415062486669-Create-a-Deal" target="_blank">deals</a>. Use these fields to enhance your sequences and deliver more personalized, relevant outreach.

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
    "/fields": {
      "post": {
        "summary": "Create a Custom Field",
        "description": "The Create a Custom Field endpoint lets you add custom fields to your Apollo account, helping your team capture unique details about <a href=\"https://knowledge.apollo.io/hc/en-us/articles/4412498825869-Create-Custom-Contact-Fields\" target=\"_blank\">contacts</a>, <a href=\"https://knowledge.apollo.io/hc/en-us/articles/4412498754445-Create-Custom-Account-Fields\" target=\"_blank\">accounts</a>, or <a href=\"https://knowledge.apollo.io/hc/en-us/articles/4415062486669-Create-a-Deal\" target=\"_blank\">deals</a>. Use these fields to enhance your sequences and deliver more personalized, relevant outreach.",
        "operationId": "create-a-custom-field",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "label": {
                    "type": "string",
                    "description": "Name of the custom field you want to create. Example: `Test Name`"
                  },
                  "modality": {
                    "type": "string",
                    "description": "The modality of the custom field you want to create.  Example: `contact`",
                    "enum": [
                      "contact",
                      "account",
                      "opportunity"
                    ]
                  },
                  "type": {
                    "type": "string",
                    "description": "What kind of custom field you want to create. Example: `textarea`",
                    "enum": [
                      "string",
                      "textarea",
                      "number",
                      "date",
                      "datetime",
                      "boolean"
                    ]
                  },
                  "meta": {
                    "type": "object",
                    "properties": {
                      "max_length": {
                        "type": "number"
                      }
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
                      "typed_custom_fields": [
                        {
                          "id": "32d42c92-5be4-4ec4-96c7-f689b43ec8a8",
                          "name": "Test Name",
                          "modality": "contact",
                          "text_field_max_length": 120
                        }
                      ]
                    }
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "typed_custom_fields": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "string",
                            "example": "32d42c92-5be4-4ec4-96c7-f689b43ec8a8"
                          },
                          "name": {
                            "type": "string",
                            "example": "Test Name"
                          },
                          "modality": {
                            "type": "string",
                            "example": "contact"
                          },
                          "text_field_max_length": {
                            "type": "number",
                            "example": 120
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
                    "value": "{\n  \"error\": \"api/v1/fields this api_key\",\n  \"error_code\": \"API_INACCESSIBLE\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "error": {
                      "type": "string",
                      "example": "api/v1/fields is not accessible with this api_key"
                    },
                    "error_code": {
                      "type": "string",
                      "example": "API_INACCESSIBLE"
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