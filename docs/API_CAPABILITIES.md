# API capabilities

Official source: https://crm.propgen.ai/public_api/docs/openapi.yaml
Retrieved 2026-11-16. Base URL: https://crm.propgen.ai/public_api/v1 (relative server resolved against official host).
Authentication: X-API-Key or Authorization: Bearer. Client uses X-API-Key.
Verified working: specification retrieval only. No live API operation authenticated: key absent.
Every operation below: **Documented but not live-tested; live verification blocked by configuration**.
Generic executor implements all listed operations; mocked tests are representative, not a live permission audit.
No separate leads resource, contract-signing endpoint, or general server-error log endpoint is documented.
Data rooms are /datenraums (read only). Automation editing, deployment, dry runs, execution, metrics and run steps ARE documented.
API key scopes are independent; restricted records may omit sensitive fields. See operation descriptions below for exact permissions and limitations.
Rate limits: configured per-key limit, hard 1,200/key/minute and 6,000/IP/minute; 20 invalid requests/minute block IP for 10 minutes. Honor Retry-After.
Cursor pagination uses data plus meta.has_more/next_cursor where documented; other endpoints are not assumed paginated.
All request parameters, bodies and response schemas are recorded below; referenced schemas are in the bundled OpenAPI.

## GET /projects

List projects

Requires `projects.list`. Ordered by ID ascending, cursor-paged. q searches titles via Elasticsearch; keep q, parent_id and limit unchanged while paging. Search returns 503 if Elasticsearch is unavailable.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Success",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/Project"
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "limit": {
                    "type": "integer"
                  },
                  "has_more": {
                    "type": "boolean"
                  },
                  "next_cursor": {
                    "type": "string",
                    "nullable": true
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing scope"
    },
    "404": {
      "description": "Record, parent or association not found in this shop"
    },
    "422": {
      "description": "Invalid payload, hierarchy or cursor"
    },
    "503": {
      "description": "Elasticsearch unavailable"
    }
  },
  "parameters": [
    {
      "name": "parent_id",
      "in": "query",
      "schema": {
        "type": "integer",
        "nullable": true
      },
      "description": "Omit for all projects; empty value returns root projects."
    },
    {
      "name": "q",
      "in": "query",
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "limit",
      "in": "query",
      "schema": {
        "type": "integer",
        "default": 50,
        "maximum": 200,
        "minimum": 1
      }
    },
    {
      "name": "cursor",
      "in": "query",
      "schema": {
        "type": "string"
      }
    }
  ]
}
```

## POST /projects

Create project

Requires `projects.add`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "project"
          ],
          "properties": {
            "project": {
              "allOf": [
                {
                  "$ref": "#/components/schemas/ProjectInput"
                },
                {
                  "required": [
                    "title"
                  ]
                }
              ]
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Success",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Project"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing scope"
    },
    "404": {
      "description": "Record, parent or association not found in this shop"
    },
    "422": {
      "description": "Invalid payload, hierarchy or cursor"
    }
  }
}
```

## GET /projects/{id}

Fetch project

Requires `projects.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Success",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Project"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing scope"
    },
    "404": {
      "description": "Record, parent or association not found in this shop"
    },
    "422": {
      "description": "Invalid payload, hierarchy or cursor"
    }
  }
}
```

## PATCH /projects/{id}

Update project

Requires `projects.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "schema": {
        "type": "string"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "project"
          ],
          "properties": {
            "project": {
              "$ref": "#/components/schemas/ProjectInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Success",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Project"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing scope"
    },
    "404": {
      "description": "Record, parent or association not found in this shop"
    },
    "422": {
      "description": "Invalid payload, hierarchy or cursor"
    },
    "412": {
      "description": "ETag mismatch"
    }
  }
}
```

## PUT /projects/{id}

Update project (partial)

Requires `projects.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "schema": {
        "type": "string"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "project"
          ],
          "properties": {
            "project": {
              "$ref": "#/components/schemas/ProjectInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Success",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Project"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing scope"
    },
    "404": {
      "description": "Record, parent or association not found in this shop"
    },
    "422": {
      "description": "Invalid payload, hierarchy or cursor"
    },
    "412": {
      "description": "ETag mismatch"
    }
  }
}
```

## DELETE /projects/{id}

Soft-delete project

Requires `projects.delete`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Soft-deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing scope"
    },
    "404": {
      "description": "Record, parent or association not found in this shop"
    },
    "422": {
      "description": "Invalid payload, hierarchy or cursor"
    }
  }
}
```

## GET /projects/{id}/associations

Fetch project associations

Requires `projects.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Success",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/ProjectAssociations"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing scope"
    },
    "404": {
      "description": "Record, parent or association not found in this shop"
    },
    "422": {
      "description": "Invalid payload, hierarchy or cursor"
    }
  }
}
```

## PATCH /projects/{id}/associations

Update submitted project associations

Requires `projects.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "schema": {
        "type": "string"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "associations"
          ],
          "properties": {
            "associations": {
              "$ref": "#/components/schemas/ProjectAssociationsInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Success",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/ProjectAssociations"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing scope"
    },
    "404": {
      "description": "Record, parent or association not found in this shop"
    },
    "422": {
      "description": "Invalid payload, hierarchy or cursor"
    },
    "412": {
      "description": "ETag mismatch"
    }
  }
}
```

## PUT /projects/{id}/associations

Update submitted project associations

Requires `projects.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "schema": {
        "type": "string"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "associations"
          ],
          "properties": {
            "associations": {
              "$ref": "#/components/schemas/ProjectAssociationsInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Success",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/ProjectAssociations"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing scope"
    },
    "404": {
      "description": "Record, parent or association not found in this shop"
    },
    "422": {
      "description": "Invalid payload, hierarchy or cursor"
    },
    "412": {
      "description": "ETag mismatch"
    }
  }
}
```

## GET /lookups/projects

Project selection lookup

Requires `projects.read`. Returns all active projects, ordered by title and ID. Optional parent_id restricts to direct children; an empty value returns roots.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Success",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "integer"
                    },
                    "name": {
                      "type": "string"
                    },
                    "parent_id": {
                      "type": "integer",
                      "nullable": true
                    }
                  }
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "total": {
                    "type": "integer"
                  },
                  "type": {
                    "type": "string",
                    "enum": [
                      "projects"
                    ]
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing scope"
    },
    "404": {
      "description": "Record, parent or association not found in this shop"
    },
    "422": {
      "description": "Invalid payload, hierarchy or cursor"
    }
  },
  "parameters": [
    {
      "name": "parent_id",
      "in": "query",
      "schema": {
        "type": "integer",
        "nullable": true
      }
    }
  ]
}
```

## GET /automation_deployments

List automation deployments

Requires `automation_deployments.read`. Results are limited to the API key's shop and omit actor identifiers.

Status: documented, not live-tested.

```json
{
  "responses": {
    "200": {
      "description": "Deployment history (at most 100, newest first)",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/AutomationDeploymentListResponse"
          }
        }
      }
    },
    "403": {
      "description": "Missing `automation_deployments.read`"
    }
  }
}
```

## POST /automation_deployments

Deploy an exact automation draft revision

Requires `automation_deployments.write`, and `automation_email.send` for plans using `email_draft.delivery_mode: send`. Send `Idempotency-Key` and exact `If-Match: "revision-N"`. Depending on shop policy, the deployment becomes active directly, remains pending_approval for a human decision, or is rejected.

Status: documented, not live-tested.

```json
{
  "parameters": [
    {
      "$ref": "#/components/parameters/AutomationDraftIfMatch"
    },
    {
      "$ref": "#/components/parameters/AutomationIdempotencyKey"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/AutomationDeploymentRequest"
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Deployed directly",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/AutomationDeploymentResponse"
          }
        }
      }
    },
    "202": {
      "description": "Awaiting human approval",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/AutomationDeploymentResponse"
          }
        }
      }
    },
    "412": {
      "description": "Stale revision"
    },
    "428": {
      "description": "Missing If-Match"
    }
  }
}
```

## GET /automation_deployments/{id}

Read an automation deployment

Requires `automation_deployments.read`. Cross-shop IDs return 404.

Status: documented, not live-tested.

```json
{
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer",
        "minimum": 1
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Deployment",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/AutomationDeploymentResponse"
          }
        }
      }
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## POST /automation_deployments/rollback

Roll back to a historical revision

Requires `automation_deployments.write`, and `automation_email.send` when rolling back to a plan using `email_draft.delivery_mode: send`. Send `Idempotency-Key`, exact `If-Match`, `automation_draft_id`, and historical `revision`. A rollback appends a new draft revision and deployment; history is never rewritten.

Status: documented, not live-tested.

```json
{
  "parameters": [
    {
      "$ref": "#/components/parameters/AutomationDraftIfMatch"
    },
    {
      "$ref": "#/components/parameters/AutomationIdempotencyKey"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/AutomationRollbackRequest"
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Rollback revision deployed",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/AutomationDeploymentResponse"
          }
        }
      }
    },
    "202": {
      "description": "Rollback awaits human approval",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/AutomationDeploymentResponse"
          }
        }
      }
    },
    "412": {
      "description": "Stale current revision"
    },
    "428": {
      "description": "Missing If-Match"
    }
  }
}
```

## GET /automation_capabilities

Discover supported automation plan capabilities

Requires `automation_plans.read`. Returns the exact triggers, conditions, steps, references, limits, and safety policies supported by the current schema version.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Versioned capability catalog. Includes a JSON Schema Draft 2020-12 in `data.plan_json_schema`.",
      "headers": {
        "ETag": {
          "description": "Private validator for conditional capability discovery",
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/AutomationCapabilityResponse"
          }
        }
      }
    },
    "304": {
      "description": "Capability catalog has not changed for this shop"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_plans.read`"
    }
  }
}
```

## GET /automation_reference_types

Discover semantic automation reference types

Requires `automation_plans.read`. Every type names its selectors, lookup path, stable match states, sensitivity, and dependencies. Pipeline stages explicitly require a pipeline context.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Stable reference type catalog",
      "headers": {
        "ETag": {
          "description": "Private validator for conditional discovery",
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/AutomationReferenceTypeResponse"
          }
        }
      }
    },
    "304": {
      "description": "Reference type catalog has not changed"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_plans.read`"
    }
  }
}
```

## GET /automation_references/{type}

Discover shop-local values for one reference type

Requires `automation_plans.read`. Lists values with opaque, shop-bound cursor pagination. Sensitive `user` and `mail_account` types require an exact selector and cannot be listed without selection. Supplying one selector (`key`, `name`, or `email`, where supported), or `query` across the type's advertised selectors, performs an exact, shop-scoped lookup and returns `not_found`, `unique`, or `ambiguous` in `meta.match_state`; ambiguous results intentionally return no candidate. Fuzzy name/text search is never emulated with SQL LIKE/ILIKE; entity text search remains on the canonical Elasticsearch search endpoints. `pipeline_stage` requires `pipeline`, containing the selected pipeline key or exact name.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "type",
      "in": "path",
      "required": true,
      "schema": {
        "type": "string",
        "enum": [
          "dashboard_phase",
          "pipeline",
          "pipeline_stage",
          "task_category",
          "mail_account",
          "user",
          "team",
          "source",
          "retention_reason",
          "email_snippet",
          "event_category",
          "email_tag",
          "contact_status",
          "company_status",
          "property_status",
          "contact_tag",
          "company_tag",
          "property_tag",
          "booking_page",
          "note_label",
          "note_tag",
          "datenraum_template",
          "newsletter_tag",
          "project"
        ]
      }
    },
    {
      "name": "cursor",
      "in": "query",
      "schema": {
        "type": "string"
      },
      "description": "Opaque cursor returned by this endpoint."
    },
    {
      "name": "limit",
      "in": "query",
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 100,
        "default": 50
      }
    },
    {
      "name": "query",
      "in": "query",
      "schema": {
        "type": "string"
      },
      "description": "Exact lookup across the type's advertised semantic selectors."
    },
    {
      "name": "key",
      "in": "query",
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "name",
      "in": "query",
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "email",
      "in": "query",
      "schema": {
        "type": "string",
        "format": "email"
      }
    },
    {
      "name": "pipeline",
      "in": "query",
      "schema": {
        "type": "string"
      },
      "description": "Required pipeline key or exact name for pipeline_stage."
    }
  ],
  "responses": {
    "200": {
      "description": "Paginated values or exact-match state",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/AutomationReferenceDiscoveryResponse"
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_plans.read`"
    },
    "422": {
      "description": "Unsupported type",
      "selector/cursor error": null,
      "unselected sensitive type (`selector_required_for_sensitive_type`)": null,
      "or missing/invalid pipeline context": null
    }
  }
}
```

## GET /automation_recipes

List declarative automation recipes

Requires `automation_plans.read`. Recipes are stable facades over selected built-in blueprints and always compile email delivery to drafts.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Shop-aware recipe list"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_plans.read`"
    }
  }
}
```

## GET /automation_recipes/{id}

Fetch one declarative automation recipe

Requires `automation_plans.read`. The path ID is the stable recipe key.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "string"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Recipe definition and required semantic references"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_plans.read`"
    },
    "404": {
      "description": "Recipe not found"
    }
  }
}
```

## POST /automation_plans/resolve

Resolve and compile a declarative automation plan

Requires `automation_plans.validate`. Resolution is side-effect free and shop-scoped. Unknown capabilities return
`valid: false` with a structured `capability_missing` issue; they are never approximated. Unknown input fields are errors.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "plan"
          ],
          "properties": {
            "plan": {
              "$ref": "#/components/schemas/AutomationPlan"
            }
          }
        },
        "example": {
          "plan": {
            "schema_version": "2026-08-26",
            "external_key": "consultant.deal.follow_up",
            "name": "Deal nach Phasenwechsel nachfassen",
            "trigger": {
              "type": "deal_stage_changed",
              "pipeline": {
                "name": "Vertrieb"
              },
              "to_stage": {
                "name": "Qualifiziert"
              }
            },
            "conditions": [
              {
                "field": "deal.to_stage",
                "operator": "equals",
                "value": {
                  "name": "Qualifiziert"
                }
              }
            ],
            "steps": [
              {
                "type": "wait_for_deal_follow_up",
                "duration": {
                  "value": 2,
                  "unit": "hours"
                }
              },
              {
                "type": "create_task",
                "title": "Deal nachfassen",
                "creator": {
                  "email": "consultant-owner@example.test"
                }
              }
            ]
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Resolution result; inspect `data.valid`, `data.issues`, and `data.capability_gaps`"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_plans.validate`"
    },
    "422": {
      "description": "Missing or malformed plan envelope"
    }
  }
}
```

## POST /automation_plans/dry_runs

Safely dry-run a declarative plan

Requires `automation_plans.dry_run`. No run, action output, email, task, note, or temporary automation is persisted. Interactive plans require `preview_user` and return `data.interactive_preview` with matched, failed, checks and the prepared action, evaluated with that user's permissions. This does not open a browser form. Updated events simulate changes to the root record's current values.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "plan",
            "root_entity"
          ],
          "properties": {
            "plan": {
              "$ref": "#/components/schemas/AutomationPlan"
            },
            "root_entity": {
              "$ref": "#/components/schemas/AutomationRootEntity"
            },
            "preview_user": {
              "allOf": [
                {
                  "$ref": "#/components/schemas/AutomationReference"
                }
              ],
              "description": "Required for interactive plans; email selector for a user in this shop. The root must be visible to this user."
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Sanitized transient run and step results"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_plans.dry_run`"
    },
    "422": {
      "description": "Invalid plan or root entity; foreign IDs use the same not-found issue"
    }
  }
}
```

## POST /automation_plans/diff

Compare two normalized automation plans

Requires `automation_plans.read`. `against` must contain exactly one of `draft_id`, `external_key`, or `plan`. Stored comparisons use the shop-owned API draft's original plan.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "plan",
            "against"
          ],
          "properties": {
            "plan": {
              "$ref": "#/components/schemas/AutomationPlan"
            },
            "against": {
              "type": "object",
              "description": "Exactly one comparison target"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Structural trigger",
      "condition": null,
      "and step differences with `identical`": null
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_plans.read`"
    },
    "404": {
      "description": "Stored draft not found in this shop"
    },
    "422": {
      "description": "Invalid plan or comparison target; plan errors include the compiler resolution"
    }
  }
}
```

## POST /automation_plans/backtest

Simulate a plan against recent shop records

Requires `automation_plans.read`. Runs the dry-run simulator in rolled-back transactions. Schedule and webhook plans are unsupported. `sample_size` defaults to 5 and is clamped to 10.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "plan"
          ],
          "properties": {
            "plan": {
              "$ref": "#/components/schemas/AutomationPlan"
            },
            "sample_size": {
              "type": "integer",
              "default": 5,
              "maximum": 10
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Per-record condition matches and redacted simulation steps",
      "with aggregate meta": null
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_plans.read`"
    },
    "422": {
      "description": "Invalid plan or `backtest_not_supported`"
    }
  }
}
```

## GET /automations

List all automations in the shop

Requires `automations.read`. Results are ordered by `updated_at,id` descending. API-draft identifiers are visible shop-wide to keys with this scope; configuration graphs, trigger configuration, webhook tokens, and extension configuration are never returned.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "status",
      "in": "query",
      "schema": {
        "type": "string",
        "enum": [
          "active",
          "inactive"
        ]
      }
    },
    {
      "name": "trigger_name",
      "in": "query",
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "source",
      "in": "query",
      "schema": {
        "type": "string",
        "enum": [
          "api",
          "ui"
        ]
      }
    },
    {
      "name": "external_key",
      "in": "query",
      "description": "Matches API drafts in the authenticated shop; unknown values return an empty page",
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "limit",
      "in": "query",
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 100,
        "default": 50
      }
    },
    {
      "name": "cursor",
      "in": "query",
      "description": "Opaque cursor bound to the shop and API key",
      "schema": {
        "type": "string"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Cursor-paginated automation inventory"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automations.read`"
    },
    "422": {
      "description": "Invalid status, source, or cursor (`invalid_status`, `invalid_source`, `invalid_cursor`)"
    }
  }
}
```

## GET /automations/{id}

Read an automation with run statistics and provenance

Requires `automations.read`. Cross-shop and unknown IDs return the same 404. Draft provenance and external keys are resolved by the authenticated shop and scopes; the creating API key is not an ownership boundary.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Safe automation detail",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/AutomationInventoryDetail"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automations.read`"
    },
    "404": {
      "description": "Automation not found in this shop"
    }
  }
}
```

## POST /automations/{id}/runs

Start an API-managed manual automation

Requires `automation_runs.execute` and `Idempotency-Key`. Only active API-managed automations with a manual trigger are accepted. Single-entity triggers require their configured `entity_type` and a shop-owned `entity_id`. Approval-gated starts are not available to API keys.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "Idempotency-Key",
      "in": "header",
      "required": true,
      "schema": {
        "type": "string",
        "maxLength": 255
      }
    }
  ],
  "responses": {
    "202": {
      "description": "Redacted operation receipt with run ID",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/AutomationRunOperationResponse"
          }
        }
      }
    },
    "403": {
      "description": "Missing `automation_runs.execute`"
    },
    "404": {
      "description": "Automation or entity not found in this shop"
    },
    "409": {
      "description": "Policy or idempotency conflict"
    },
    "422": {
      "description": "Invalid input",
      "missing idempotency key": null,
      "or unsupported operation": null
    }
  }
}
```

## GET /automation_drafts

List API automation drafts in the shop

Requires `automation_plans.read`. Draft visibility is scoped to the authenticated shop; the creating key is provenance, not an authorization boundary.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "limit",
      "in": "query",
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 100,
        "default": 50
      }
    },
    {
      "name": "cursor",
      "in": "query",
      "description": "Opaque cursor returned by the previous page. Cursors are bound to the authenticated shop and API key.",
      "schema": {
        "type": "string"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Inactive draft summaries ordered by `updated_at",
      "id` descending; `meta.next_cursor` is present only when `has_more` is true": null
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_plans.read`"
    },
    "422": {
      "description": "Invalid or manipulated cursor (`error: invalid_cursor`)"
    }
  }
}
```

## POST /automation_drafts

Create an idempotent inactive automation draft

Requires `automation_drafts.write` and an `Idempotency-Key` header. The key is unique per shop and API key.
A replay with the same normalized plan returns the original draft and `Idempotency-Replayed: true`; different input returns 409.
The resulting Automation is always `inactive`. It can be activated with the dedicated lifecycle scope.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "Idempotency-Key",
      "in": "header",
      "required": true,
      "schema": {
        "type": "string",
        "maxLength": 255
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "plan"
          ],
          "properties": {
            "plan": {
              "$ref": "#/components/schemas/AutomationPlan"
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "New inactive draft; ETag is `\"revision-1\"`"
    },
    "200": {
      "description": "Idempotent replay"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_drafts.write`"
    },
    "409": {
      "description": "Idempotency or external-key conflict"
    },
    "422": {
      "description": "Invalid plan or missing idempotency key"
    }
  }
}
```

## GET /automation_drafts/{id}

Fetch an automation draft

Requires `automation_plans.read`. Returns the normalized plan, diagnostic compiled snapshot, provenance, and revision metadata. Scoped to the authenticated shop.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "$ref": "#/components/parameters/AutomationDraftId"
    }
  ],
  "responses": {
    "200": {
      "description": "Draft detail with revision ETag"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_plans.read`"
    },
    "404": {
      "description": "Draft not found for this shop"
    }
  }
}
```

## PATCH /automation_drafts/{id}

Replace a draft plan using optimistic locking

Requires `automation_drafts.write` and `If-Match: "revision-N"`. `external_key` is immutable.
An automation activated by a shop user can never be changed or deactivated through this endpoint.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "$ref": "#/components/parameters/AutomationDraftId"
    },
    {
      "$ref": "#/components/parameters/AutomationDraftIfMatch"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "plan"
          ],
          "properties": {
            "plan": {
              "$ref": "#/components/schemas/AutomationPlan"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Updated inactive draft and next revision ETag"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_drafts.write`"
    },
    "404": {
      "description": "Draft not found for this shop"
    },
    "409": {
      "description": "Immutable external key or automation no longer inactive"
    },
    "412": {
      "description": "Stale revision"
    },
    "428": {
      "description": "If-Match required"
    }
  }
}
```

## PUT /automation_drafts/{id}

Replace a draft plan using optimistic locking

Requires `automation_drafts.write`.
Same full-plan replacement contract and safety checks as PATCH. The complete `plan` is compiled
and replaces the prior plan; omitted plan fields are not merged from the previous revision.
Requires `automation_drafts.write` and `If-Match: "revision-N"`.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "$ref": "#/components/parameters/AutomationDraftId"
    },
    {
      "$ref": "#/components/parameters/AutomationDraftIfMatch"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "plan"
          ],
          "properties": {
            "plan": {
              "$ref": "#/components/schemas/AutomationPlan"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Updated inactive draft and next revision ETag"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_drafts.write`"
    },
    "404": {
      "description": "Draft not found for this shop"
    },
    "409": {
      "description": "Immutable external key or automation no longer inactive"
    },
    "412": {
      "description": "Stale revision"
    },
    "428": {
      "description": "If-Match required"
    }
  }
}
```

## DELETE /automation_drafts/{id}

Delete an inactive draft and its linked automation

Requires `automation_drafts.write`. Deletion is allowed only while inactive and only when no persisted run history exists. Success returns 204 with no body.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "$ref": "#/components/parameters/AutomationDraftId"
    }
  ],
  "responses": {
    "204": {
      "description": "Draft and linked automation deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_drafts.write`"
    },
    "404": {
      "description": "Draft not found for this shop"
    },
    "409": {
      "description": "Automation is active (`draft_no_longer_inactive`) or has history (`runs_present` or `deployments_present`)"
    }
  }
}
```

## GET /automation_drafts/by_external_key/{external_key}

Fetch an automation draft by external key

Requires `automation_plans.read`. Returns the same detail payload and revision ETag as the ID-based draft endpoint. Draft visibility is scoped to the authenticated shop; the creating API key is provenance, not an authorization boundary.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "external_key",
      "in": "path",
      "required": true,
      "schema": {
        "type": "string",
        "maxLength": 100
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Shop-owned draft detail with revision ETag"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_plans.read`"
    },
    "404": {
      "description": "Draft not found for this external key in the authenticated shop"
    }
  }
}
```

## PUT /automation_drafts/by_external_key/{external_key}

Create or replace desired draft state by external key

Requires `automation_drafts.write`. Creates with 201, updates with 200, and avoids a revision when the canonical plan is unchanged. No If-Match or Idempotency-Key is required.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "external_key",
      "in": "path",
      "required": true,
      "schema": {
        "type": "string",
        "maxLength": 100
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "plan"
          ],
          "properties": {
            "plan": {
              "$ref": "#/components/schemas/AutomationPlan"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Updated or unchanged draft; `meta.action` identifies the outcome"
    },
    "201": {
      "description": "Created draft; `meta.action` is `created`"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_drafts.write`"
    },
    "422": {
      "description": "Invalid plan or external-key mismatch"
    }
  }
}
```

## GET /automation_drafts/{id}/export

Export a portable automation plan bundle

Requires `automation_plans.read`. Returns the original plan and a shop-scoped semantic reference manifest; webhook tokens and compiled internals are excluded.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "$ref": "#/components/parameters/AutomationDraftId"
    }
  ],
  "responses": {
    "200": {
      "description": "Schema version",
      "original plan": null,
      "reference manifest": null,
      "and export timestamp": null
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_plans.read`"
    },
    "404": {
      "description": "Draft not found for this shop"
    }
  }
}
```

## POST /automation_drafts/{id}/activate

Activate an inactive API-managed automation

Requires `automation_drafts.activate`, and `automation_email.send` for plans using `email_draft.delivery_mode: send`. Strict transition from inactive to active; activation validates email action parameters and marks lifecycle management as API-controlled. Already active returns `already_active`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "$ref": "#/components/parameters/AutomationDraftId"
    }
  ],
  "responses": {
    "200": {
      "description": "Serialized active draft with revision ETag"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_drafts.activate`"
    },
    "404": {
      "description": "Draft not found for this shop"
    },
    "409": {
      "description": "Already active"
    },
    "422": {
      "description": "Model validation failed (`activation_failed`, with safe validation details)"
    }
  }
}
```

## POST /automation_drafts/{id}/rotate_webhook_token

Rotate a webhook automation token

Requires `automation_drafts.write` and a webhook-triggered draft. The response URL contains
the newly generated full token exactly once; ordinary draft detail responses expose only a
token preview and a redaction indicator.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "$ref": "#/components/parameters/AutomationDraftId"
    }
  ],
  "responses": {
    "200": {
      "description": "Fresh webhook URL and token metadata",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "required": [
              "data"
            ],
            "properties": {
              "data": {
                "type": "object",
                "required": [
                  "webhook"
                ],
                "properties": {
                  "webhook": {
                    "type": "object",
                    "required": [
                      "url",
                      "token_preview",
                      "redacted"
                    ],
                    "properties": {
                      "url": {
                        "type": "string",
                        "format": "uri"
                      },
                      "token_preview": {
                        "type": "string"
                      },
                      "redacted": {
                        "type": "boolean",
                        "enum": [
                          false
                        ]
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
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_drafts.write`"
    },
    "404": {
      "description": "Draft not found for this shop"
    },
    "422": {
      "description": "Draft does not use a webhook trigger"
    }
  }
}
```

## POST /automation_drafts/{id}/deactivate

Deactivate an API-activated automation

Requires `automation_drafts.activate`. Only automations previously activated through this API may be deactivated. UI-activated automations remain immutable and return `activation_not_api_managed`. To edit an active draft, deactivate it, PATCH it with If-Match, then activate it again.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "$ref": "#/components/parameters/AutomationDraftId"
    }
  ],
  "responses": {
    "200": {
      "description": "Serialized inactive draft with revision ETag"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_drafts.activate`"
    },
    "404": {
      "description": "Draft not found for this shop"
    },
    "409": {
      "description": "Already inactive or not API-managed (`already_inactive`, `activation_not_api_managed`)"
    }
  }
}
```

## GET /automation_drafts/{id}/revisions

List immutable draft revisions

Requires `automation_plans.read`. Scoped to the authenticated shop and ordered by revision ascending.
List entries contain revision metadata and the normalized summary; `original_plan` and
`compiled_snapshot` are served by the single-revision endpoint. Paginate with `limit`
(default 50, maximum 100) and `after_revision`; `meta.next_after_revision` continues the list.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "$ref": "#/components/parameters/AutomationDraftId"
    },
    {
      "name": "limit",
      "in": "query",
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 100,
        "default": 50
      }
    },
    {
      "name": "after_revision",
      "in": "query",
      "description": "Only revisions greater than this number",
      "schema": {
        "type": "integer",
        "minimum": 0
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Revision metadata and normalized summaries with pagination meta"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_plans.read`"
    },
    "404": {
      "description": "Draft not found for this shop"
    }
  }
}
```

## GET /automation_drafts/{id}/revisions/{revision}

Read one immutable draft revision

Requires `automation_plans.read`. Includes the original plan and the diagnostic compiled snapshot.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "$ref": "#/components/parameters/AutomationDraftId"
    },
    {
      "name": "revision",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer",
        "minimum": 1
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Full revision"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_plans.read`"
    },
    "404": {
      "description": "Draft or revision not found"
    }
  }
}
```

## GET /automation_drafts/{id}/stats

Read seven-day run statistics for an automation draft

Requires `automation_runs.read`. The draft and its run statistics are scoped to the authenticated shop.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "$ref": "#/components/parameters/AutomationDraftId"
    }
  ],
  "responses": {
    "200": {
      "description": "Run totals and daily counts for the last seven days",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/AutomationRunStats"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_runs.read`"
    },
    "404": {
      "description": "Draft not found for this shop"
    }
  }
}
```

## GET /automation_runs

List automation runs

Requires `automation_runs.read`. Unknown status values return 422 with `error: invalid_status`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "automation_id",
      "in": "query",
      "schema": {
        "type": "integer",
        "minimum": 1
      }
    },
    {
      "name": "external_key",
      "in": "query",
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "status",
      "in": "query",
      "description": "Comma-separated run statuses",
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "dry_run",
      "in": "query",
      "schema": {
        "type": "boolean"
      }
    },
    {
      "name": "revision",
      "in": "query",
      "schema": {
        "type": "integer",
        "minimum": 1
      }
    },
    {
      "name": "deployment_id",
      "in": "query",
      "schema": {
        "type": "integer",
        "minimum": 1
      }
    },
    {
      "name": "failure_code",
      "in": "query",
      "schema": {
        "type": "string",
        "enum": [
          "run_timed_out",
          "run_failed",
          "step_failed"
        ]
      }
    },
    {
      "name": "waiting_reason",
      "in": "query",
      "schema": {
        "type": "string",
        "enum": [
          "approval_required",
          "event_wait",
          "execution_queued"
        ]
      }
    },
    {
      "name": "correlation_id",
      "in": "query",
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "from",
      "in": "query",
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "to",
      "in": "query",
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "latest_per_automation",
      "in": "query",
      "schema": {
        "type": "boolean"
      }
    },
    {
      "name": "include_steps",
      "in": "query",
      "description": "When true",
      "each run embeds redacted steps and the effective limit is capped at 50": null,
      "schema": {
        "type": "boolean"
      }
    },
    {
      "name": "limit",
      "in": "query",
      "description": "Maximum 100",
      "or 50 when include_steps=true": null,
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 100,
        "default": 50
      }
    },
    {
      "name": "cursor",
      "in": "query",
      "schema": {
        "type": "string"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Runs ordered by `created_at,id` descending with cursor pagination",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/AutomationRunListResponse"
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_runs.read`"
    },
    "422": {
      "description": "Invalid status",
      "timestamp": null,
      "automation ID": null,
      "or cursor": null
    }
  }
}
```

## GET /automation_metrics

Aggregate automation run metrics

Requires `automation_metrics.read`. Uses SQL aggregation and is always scoped to the authenticated shop. The half-open `[from,to)` window is limited to 90 days; hourly buckets are limited to 7 days. At most three group dimensions may be combined.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "from",
      "in": "query",
      "required": true,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "to",
      "in": "query",
      "required": true,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "interval",
      "in": "query",
      "required": true,
      "schema": {
        "type": "string",
        "enum": [
          "hour",
          "day",
          "week"
        ]
      }
    },
    {
      "name": "group_by",
      "in": "query",
      "description": "Comma-separated: automation, external_key, status, revision, deployment",
      "schema": {
        "type": "string"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Totals and grouped time buckets. Durations exclude missing, negative, and over-30-day observations.",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "required": [
              "data"
            ],
            "properties": {
              "data": {
                "type": "object",
                "required": [
                  "from",
                  "to",
                  "interval",
                  "group_by",
                  "totals",
                  "buckets"
                ],
                "properties": {
                  "from": {
                    "type": "string",
                    "format": "date-time"
                  },
                  "to": {
                    "type": "string",
                    "format": "date-time"
                  },
                  "interval": {
                    "type": "string",
                    "enum": [
                      "hour",
                      "day",
                      "week"
                    ]
                  },
                  "group_by": {
                    "type": "array",
                    "maxItems": 3,
                    "items": {
                      "type": "string",
                      "enum": [
                        "automation",
                        "external_key",
                        "status",
                        "revision",
                        "deployment"
                      ]
                    }
                  },
                  "totals": {
                    "$ref": "#/components/schemas/AutomationMetricCounts"
                  },
                  "buckets": {
                    "type": "array",
                    "items": {
                      "$ref": "#/components/schemas/AutomationMetricBucket"
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
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_metrics.read`"
    },
    "422": {
      "description": "`invalid_timestamp`, `invalid_time_range`, `time_range_too_large`, `invalid_interval`, `interval_too_small`, or `invalid_group_by`"
    }
  }
}
```

## GET /automation_runs/{id}

Read an automation run and its redacted steps

Requires `automation_runs.read`. Raw context, input/output payloads, configuration snapshots, and graphs are never returned.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Run detail",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/AutomationRun"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing `automation_runs.read`"
    },
    "404": {
      "description": "Run not found in this shop"
    }
  }
}
```

## POST /automation_runs/{id}/cancel

Cancel a queued or persisted waiting run

Requires `automation_runs.operate` and `Idempotency-Key`. Only queued, waiting, or pending-approval runs can be canceled. Running synchronous effects and terminal runs return `run_not_cancelable` (409).

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "Idempotency-Key",
      "in": "header",
      "required": true,
      "schema": {
        "type": "string",
        "maxLength": 255
      }
    }
  ],
  "responses": {
    "202": {
      "description": "Redacted operation receipt",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/AutomationRunOperationResponse"
          }
        }
      }
    },
    "403": {
      "description": "Missing `automation_runs.operate`"
    },
    "404": {
      "description": "Run not found in this shop"
    },
    "409": {
      "description": "Run is not cancelable or idempotency conflict"
    },
    "422": {
      "description": "Missing or invalid idempotency key"
    }
  }
}
```

## GET /webhooks

List webhooks

Requires `webhooks.list`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "limit",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 200
      }
    },
    {
      "name": "cursor",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Webhook list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/Webhook"
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "limit": {
                    "type": "integer"
                  },
                  "has_more": {
                    "type": "boolean"
                  },
                  "next_cursor": {
                    "type": "string",
                    "nullable": true
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    }
  }
}
```

## POST /webhooks

Create webhook

Requires `webhooks.add`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "webhook": {
              "$ref": "#/components/schemas/WebhookInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Webhook created",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/WebhookWithSecret"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /webhooks/{id}

Fetch webhook

Requires `webhooks.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Webhook payload",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Webhook"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /webhooks/{id}

Update webhook

Requires `webhooks.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "webhook": {
              "$ref": "#/components/schemas/WebhookInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Webhook updated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Webhook"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /webhooks/{id}

Update webhook

Requires `webhooks.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "webhook": {
              "$ref": "#/components/schemas/WebhookInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Webhook updated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Webhook"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## DELETE /webhooks/{id}

Delete webhook

Requires `webhooks.delete`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /companies/{id}/associations

Fetch company associations

Requires `companies.read`. Returns tags, statuses, and relationship IDs for a company.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Company associations",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "object",
                "properties": {
                  "project_ids": {
                    "type": "array",
                    "items": {
                      "type": "integer"
                    }
                  },
                  "id": {
                    "type": "integer"
                  },
                  "tag_ids": {
                    "type": "array",
                    "items": {
                      "type": "integer"
                    }
                  },
                  "status_ids": {
                    "type": "array",
                    "items": {
                      "type": "integer"
                    }
                  },
                  "associations": {
                    "$ref": "#/components/schemas/CompanyAssociations"
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /companies/{id}/associations

Update company associations

Requires `companies.edit`. Updates tags, statuses, and associations for a company.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "ETag from a previous GET response"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "associations": {
              "type": "object",
              "description": "Same association keys as company create/update.",
              "properties": {
                "project_ids": {
                  "type": "array",
                  "items": {
                    "type": "integer"
                  },
                  "description": "Omit to preserve links; [] clears all direct project links."
                }
              }
            }
          }
        },
        "example": {
          "associations": {
            "tag_ids": [
              10
            ],
            "status_ids": [
              22
            ],
            "contact_associations_clients": [
              {
                "contact_id": 5,
                "company_location_id": 12
              }
            ],
            "company_relationships": [
              {
                "related_company_id": 9,
                "custom_label": "Tochterfirma",
                "reciprocal_label": "Mutterfirma"
              }
            ]
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Updated associations"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /companies/{id}/associations

Replace company associations

Requires `companies.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "ETag from a previous GET response"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "associations": {
              "type": "object",
              "description": "Same association keys as company create/update.",
              "properties": {
                "project_ids": {
                  "type": "array",
                  "items": {
                    "type": "integer"
                  },
                  "description": "Omit to preserve links; [] clears all direct project links."
                }
              }
            }
          }
        },
        "example": {
          "associations": {
            "tag_ids": [],
            "status_ids": []
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Updated associations"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /companies/{id}/locations

List company locations

Requires `companies.read`. Returns the complete ordered collection (headquarters first, then `position`, `id`).
Optional `active=true|false` filters the list. No cursor pagination.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "active",
      "in": "query",
      "required": false,
      "schema": {
        "type": "boolean"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Ordered company locations",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "required": [
              "data"
            ],
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/CompanyLocation"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing companies.read"
    },
    "404": {
      "description": "Company not found in this shop"
    },
    "422": {
      "description": "Invalid active filter"
    }
  }
}
```

## POST /companies/{id}/locations

Create a company location

Requires `companies.edit`. The first location becomes headquarters. Headquarters cannot be inactive.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "company_location": {
              "$ref": "#/components/schemas/CompanyLocationInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Created location",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "required": [
              "data"
            ],
            "properties": {
              "data": {
                "$ref": "#/components/schemas/CompanyLocation"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing companies.edit"
    },
    "404": {
      "description": "Company not found in this shop"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /companies/{id}/locations/{location_id}

Fetch a company location

Requires `companies.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "location_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Location",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "required": [
              "data"
            ],
            "properties": {
              "data": {
                "$ref": "#/components/schemas/CompanyLocation"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing companies.read"
    },
    "404": {
      "description": "Company or location not found in this shop"
    }
  }
}
```

## PATCH /companies/{id}/locations/{location_id}

Update a company location

Requires `companies.edit`. Partial update. Setting `headquarters: true` moves the headquarters flag. Headquarters cannot be deactivated.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "location_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "company_location": {
              "$ref": "#/components/schemas/CompanyLocationInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Updated location",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "required": [
              "data"
            ],
            "properties": {
              "data": {
                "$ref": "#/components/schemas/CompanyLocation"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing companies.edit"
    },
    "404": {
      "description": "Company or location not found in this shop"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /companies/{id}/locations/{location_id}

Update a company location

Requires `companies.edit`. Same as PATCH.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "location_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "company_location": {
              "$ref": "#/components/schemas/CompanyLocationInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Updated location",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "required": [
              "data"
            ],
            "properties": {
              "data": {
                "$ref": "#/components/schemas/CompanyLocation"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing companies.edit"
    },
    "404": {
      "description": "Company or location not found in this shop"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## DELETE /companies/{id}/locations/{location_id}

Delete a company location

Requires `companies.edit`. Referenced locations and the last remaining headquarters while other locations exist cannot be deleted (422).

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "location_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing companies.edit"
    },
    "404": {
      "description": "Company or location not found in this shop"
    },
    "422": {
      "description": "Location is still referenced or headquarters cannot be removed"
    }
  }
}
```

## POST /webhooks/{id}/rotate_secret

Rotate webhook secret

Requires `webhooks.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Webhook secret rotated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/WebhookWithSecret"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## POST /webhooks/{id}/test

Send test webhook

Requires `webhooks.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "201": {
      "description": "Test delivery queued",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/WebhookDelivery"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    }
  }
}
```

## POST /webhooks/{id}/verify_signature

Verify webhook signature

Requires `webhooks.read`. Validates a received signature against the webhook secret.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "payload": {
              "type": "string",
              "description": "Raw request body as received"
            },
            "signature": {
              "type": "string",
              "description": "Value of the X-propgen-Signature header or just the v1 hash"
            },
            "signature_header": {
              "type": "string",
              "description": "Alias for signature"
            },
            "timestamp": {
              "type": "string",
              "description": "Optional timestamp; inferred from signature header if present"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Verification result",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "object",
                "properties": {
                  "valid": {
                    "type": "boolean"
                  },
                  "expected_signature": {
                    "type": "string"
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Validation errors"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /webhooks/{id}/deliveries

List webhook deliveries

Requires `webhooks.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "limit",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 200
      }
    },
    {
      "name": "cursor",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Delivery list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/WebhookDelivery"
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "limit": {
                    "type": "integer"
                  },
                  "has_more": {
                    "type": "boolean"
                  },
                  "next_cursor": {
                    "type": "string",
                    "nullable": true
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## POST /webhooks/{id}/deliveries/{delivery_id}/retry

Retry webhook delivery

Requires `webhooks.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "delivery_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Delivery retried",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/WebhookDelivery"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Cannot retry successful delivery"
    }
  }
}
```

## GET /schema/{model}

Fetch form schema for a model

Requires the read scope of the requested model: `contacts.read`, `companies.read`, `properties.read`, `deals.read`, `tasks.read`, `notes.read`, `calendar_events.read` or `emails.read`, matching `{model}`. Returns the dynamic form schema for the requested model, including field definitions and select options.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "model",
      "in": "path",
      "required": true,
      "schema": {
        "type": "string",
        "enum": [
          "contacts",
          "companies",
          "properties",
          "deals",
          "tasks",
          "notes",
          "calendar_events",
          "emails"
        ]
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Schema payload",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "model": {
                "type": "string"
              },
              "schema": {
                "type": "object"
              },
              "generated_at": {
                "type": "string",
                "format": "date-time"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    }
  }
}
```

## GET /schema/{model}/clean

Fetch clean schema for API integrations

Requires the read scope of the requested model: `contacts.read`, `companies.read`, `properties.read`, `deals.read`, `tasks.read`, `notes.read`, `calendar_events.read` or `emails.read`, matching `{model}`.
Returns a compact schema without UI/layout metadata, optimized for API clients.

Example flow:

1) Fetch clean schema
```bash
curl -H "Authorization: Bearer <api_key>" /public_api/v1/schema/contacts/clean
```
2) Use dynamic sources from `input`
```bash
curl -H "Authorization: Bearer <api_key>" /public_api/v1/lookups/contact_statuses
curl -H "Authorization: Bearer <api_key>" "/public_api/v1/search/companies?q=acme"
```


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "model",
      "in": "path",
      "required": true,
      "schema": {
        "type": "string",
        "enum": [
          "contacts",
          "companies",
          "properties",
          "deals",
          "tasks",
          "notes",
          "calendar_events",
          "emails"
        ]
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Clean schema payload",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "model": {
                "type": "string"
              },
              "fields": {
                "type": "array",
                "items": {
                  "type": "object"
                }
              },
              "available_fields": {
                "type": "array",
                "items": {
                  "type": "object"
                }
              },
              "generated_at": {
                "type": "string",
                "format": "date-time"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    }
  }
}
```

## GET /contacts

List contacts

Requires `contacts.list`. Returns contacts using cursor pagination. Default response is summary fields unless `fields=full` is provided. Filters are optional and AND-combined. `tag_ids` and `status_ids` accept comma-separated IDs (OR within each list). Example: `/contacts?tag_ids=5,9&status_ids=12&archived=false&limit=50`

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "limit",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 200
      }
    },
    {
      "name": "cursor",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "updated_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "sort",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "updated_at",
          "created_at"
        ]
      },
      "description": "Sort field for cursor pagination"
    },
    {
      "name": "direction",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "asc",
          "desc"
        ]
      },
      "description": "Sort direction (default asc)"
    },
    {
      "name": "include_deleted",
      "in": "query",
      "required": false,
      "schema": {
        "type": "boolean",
        "description": "Include soft-deleted records"
      }
    },
    {
      "name": "deleted_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time",
        "description": "Return only soft-deleted records deleted since this timestamp"
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated includes (tags,statuses,associations)"
      }
    },
    {
      "name": "status_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated status IDs (any match)",
        "example": "12,34"
      }
    },
    {
      "name": "tag_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated tag IDs (any match)",
        "example": "5,9"
      }
    },
    {
      "name": "archived",
      "in": "query",
      "required": false,
      "schema": {
        "type": "boolean",
        "example": false
      }
    },
    {
      "name": "email",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "email",
        "example": "familie@example.com"
      },
      "description": "Returns every contact that owns this address as primary or additional email (exact match, case-insensitive, surrounding whitespace ignored). Several contacts may share one address, so the result can contain more than one contact; use the returned `id` to address a single contact."
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include_deleted",
      "in": "query",
      "required": false,
      "schema": {
        "type": "boolean"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Contact list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "anyOf": [
                    {
                      "$ref": "#/components/schemas/ContactSummary"
                    },
                    {
                      "$ref": "#/components/schemas/Contact"
                    },
                    {
                      "$ref": "#/components/schemas/RestrictedEntity"
                    }
                  ]
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "limit": {
                    "type": "integer"
                  },
                  "has_more": {
                    "type": "boolean"
                  },
                  "next_cursor": {
                    "type": "string",
                    "nullable": true
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Invalid cursor, updated_since, or fields"
    }
  }
}
```

## POST /contacts

Create contact

Requires `contacts.add`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "contact": {
              "$ref": "#/components/schemas/ContactInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Contact created",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Contact"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Validation errors",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/ValidationFailedResponse"
          }
        }
      }
    }
  }
}
```

## POST /contacts/batch

Batch upsert contacts

Requires `contacts.add` if any item has no `id`, and `contacts.edit` if any item has an `id` or a `lookup`. Upserts multiple contacts in one request. If any item is invalid, the batch fails and no changes are applied. Requires `contacts.add` for new records and `contacts.edit` for items with `id` or `lookup`. Max batch size: 100. Set `validate_only=true` to execute and roll back the complete batch.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "validate_only": {
              "type": "boolean",
              "default": false
            },
            "contacts": {
              "type": "array",
              "items": {
                "$ref": "#/components/schemas/ContactBatchItem"
              }
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Batch result",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/Contact"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Item validation error; the complete batch is rolled back",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/ContactBatchValidationFailedResponse"
          }
        }
      }
    }
  }
}
```

## GET /contacts/{id}

Fetch contact

Requires `contacts.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "ETag from a previous GET response"
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated includes (tags,statuses,associations)"
      }
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include_deleted",
      "in": "query",
      "required": false,
      "schema": {
        "type": "boolean"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Contact payload",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "anyOf": [
                  {
                    "$ref": "#/components/schemas/Contact"
                  },
                  {
                    "$ref": "#/components/schemas/ContactSummary"
                  },
                  {
                    "$ref": "#/components/schemas/RestrictedEntity"
                  }
                ]
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /contacts/{id}

Update contact

Requires `contacts.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "ETag from a previous GET response"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "contact": {
              "$ref": "#/components/schemas/ContactInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Contact updated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Contact"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/ValidationFailedResponse"
          }
        }
      }
    }
  }
}
```

## PUT /contacts/{id}

Update contact

Requires `contacts.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "ETag from a previous GET response"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "contact": {
              "$ref": "#/components/schemas/ContactInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Contact updated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Contact"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/ValidationFailedResponse"
          }
        }
      }
    }
  }
}
```

## DELETE /contacts/{id}

Delete contact (soft delete)

Requires `contacts.delete`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## POST /companies/{id}/restore

Restore company

Requires `companies.delete`. Restores a soft-deleted company.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Restored company",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Company"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## POST /contacts/{id}/restore

Restore contact

Requires `contacts.delete`. Restores a soft-deleted contact.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Restored contact",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Contact"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /contacts/{id}/associations

Fetch contact associations

Requires `contacts.read`. Returns tags, statuses, and relationship IDs for a contact.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Contact associations",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "object",
                "properties": {
                  "project_ids": {
                    "type": "array",
                    "items": {
                      "type": "integer"
                    }
                  },
                  "id": {
                    "type": "integer"
                  },
                  "tag_ids": {
                    "type": "array",
                    "items": {
                      "type": "integer"
                    }
                  },
                  "status_ids": {
                    "type": "array",
                    "items": {
                      "type": "integer"
                    }
                  },
                  "associations": {
                    "type": "object"
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /contacts/{id}/associations

Update contact associations

Requires `contacts.edit`. Updates tags, statuses, and associations for a contact.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "ETag from a previous GET response"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "associations": {
              "type": "object",
              "description": "Same association keys as contact create/update.",
              "properties": {
                "project_ids": {
                  "type": "array",
                  "items": {
                    "type": "integer"
                  },
                  "description": "Omit to preserve links; [] clears all direct project links."
                }
              }
            }
          }
        },
        "example": {
          "associations": {
            "tag_ids": [
              1,
              2
            ],
            "status_ids": [
              3
            ],
            "contact_associations_owners": [
              {
                "property_id": 99
              }
            ],
            "company_associations_clients": [
              {
                "company_id": 42,
                "company_location_id": 12
              }
            ],
            "contact_relationships": [
              {
                "related_contact_id": 7,
                "custom_label": "Ehepartner",
                "reciprocal_label": "Ehepartner"
              }
            ]
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Updated associations"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /contacts/{id}/associations

Replace contact associations

Requires `contacts.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "associations": {
              "type": "object",
              "description": "Same association keys as contact create/update.",
              "properties": {
                "project_ids": {
                  "type": "array",
                  "items": {
                    "type": "integer"
                  },
                  "description": "Omit to preserve links; [] clears all direct project links."
                }
              }
            }
          }
        },
        "example": {
          "associations": {
            "tag_ids": [],
            "status_ids": []
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Updated associations"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /search_profiles/catalog

List available search-profile criteria

Requires `search_profiles.read`. Returns the token shop's selectable property criteria, including custom fields explicitly enabled as searchable. Missing context dimensions are satisfied. Shorthand alternatives on one dimension are OR; structured conditions and all_of/any_of groups retain their meaning. Field and section conditions must match the same complete selection. Selected subtypes belong only to their parent object type. Context controls this offer, not the validity of already saved criteria. Copy canonical case-sensitive values from the schema options. Object types and subtypes accept a scalar (objektart=buero_praxen) or repeated bracket parameters (objektart[]=buero_praxen&objektart[]=einzelhandel&sub_objektart[]=PRAXIS). Option conditions and child hierarchies are returned for client-side option filtering.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "nutzungsart",
      "in": "query",
      "schema": {
        "type": "string"
      },
      "example": "GEWERBE"
    },
    {
      "name": "vermarktungsart",
      "in": "query",
      "schema": {
        "type": "string"
      },
      "example": "MIETE_PACHT"
    },
    {
      "name": "objektart",
      "in": "query",
      "schema": {
        "oneOf": [
          {
            "type": "string"
          },
          {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        ]
      }
    },
    {
      "name": "sub_objektart",
      "in": "query",
      "schema": {
        "oneOf": [
          {
            "type": "string"
          },
          {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        ]
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Available criteria, without a contact or company identifier",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/SearchProfileCatalogField"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing search_profiles.read scope"
    }
  }
}
```

## GET /contacts/{id}/search_profiles

List contact search profiles

Requires `search_profiles.list`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Search profile list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/SearchProfile"
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "total": {
                    "type": "integer"
                  },
                  "profileable_type": {
                    "type": "string"
                  },
                  "profileable_id": {
                    "type": "integer"
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Contact not found"
    }
  }
}
```

## POST /contacts/{id}/search_profiles

Create or CRM-identity upsert contact search profile

Requires `search_profiles.add`, or `search_profiles.edit` when `crm_source` and `crm_import_id` match an existing profile of this record. Set `validate_only=true` to validate and roll back without jobs.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "validate_only": {
              "type": "boolean",
              "default": false
            },
            "search_profile": {
              "$ref": "#/components/schemas/SearchProfileInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Search profile created",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/SearchProfile"
              }
            }
          }
        }
      }
    },
    "200": {
      "description": "Existing CRM-identified search profile updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Contact not found"
    },
    "422": {
      "description": "Validation errors, including field-specific catalog rejection reasons",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/SearchProfileValidationError"
          }
        }
      }
    }
  }
}
```

## GET /contacts/{id}/search_profiles/default_template

Fetch contact search profile template

Requires `search_profiles.read`. Resolves the active template in this order: user, team, usage and object type, usage, target default, then the first eligible template. The final fallback is reported as type_default. Market parameters accept a scalar or repeated bracket parameters. If objektart is omitted, a positive sub_objektart infers its unique parent object type. When both are present, objektart takes precedence.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "nutzungsart",
      "in": "query",
      "schema": {
        "oneOf": [
          {
            "type": "string"
          },
          {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        ]
      }
    },
    {
      "name": "objektart",
      "in": "query",
      "schema": {
        "oneOf": [
          {
            "type": "string"
          },
          {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        ]
      }
    },
    {
      "name": "sub_objektart",
      "in": "query",
      "description": "Infers the unique parent object type only when objektart is omitted.",
      "schema": {
        "oneOf": [
          {
            "type": "string"
          },
          {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        ]
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Default template",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/SearchProfileTemplate"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Contact not found"
    }
  }
}
```

## GET /contacts/{id}/search_profiles/{search_profile_id}

Fetch contact search profile

Requires `search_profiles.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "search_profile_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "schema"
        ]
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Search profile payload",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/SearchProfile"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Contact or search profile not found"
    }
  }
}
```

## PATCH /contacts/{id}/search_profiles/{search_profile_id}

Update contact search profile

Requires `search_profiles.edit`. Partial update. validate_only=true rolls back without persistence, jobs or lifecycle events; returns meta.validate_only.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "search_profile_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "validate_only": {
              "type": "boolean",
              "default": false
            },
            "search_profile": {
              "$ref": "#/components/schemas/SearchProfileInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Search profile updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Contact or search profile not found"
    },
    "422": {
      "description": "Validation errors, including field-specific catalog rejection reasons",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/SearchProfileValidationError"
          }
        }
      }
    }
  }
}
```

## PUT /contacts/{id}/search_profiles/{search_profile_id}

Update contact search profile

Requires `search_profiles.edit`. Partial update. validate_only=true rolls back without persistence, jobs or lifecycle events; returns meta.validate_only.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "search_profile_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "validate_only": {
              "type": "boolean",
              "default": false
            },
            "search_profile": {
              "$ref": "#/components/schemas/SearchProfileInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Search profile updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Contact or search profile not found"
    },
    "422": {
      "description": "Validation errors, including field-specific catalog rejection reasons",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/SearchProfileValidationError"
          }
        }
      }
    }
  }
}
```

## DELETE /contacts/{id}/search_profiles/{search_profile_id}

Archive contact search profile

Requires `search_profiles.delete`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "search_profile_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Archived"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Contact or search profile not found"
    }
  }
}
```

## GET /contacts/{id}/search_profiles/{search_profile_id}/results

Match properties for a contact search profile

Requires `search_profiles.read` and `properties.read`. Returns live matches with score explanations. Each project's or areal's best eligible unit supplies the score, field values and property_id; id identifies the displayed group. parent_id is the matching unit's immediate parent (omitted for root properties). variants contains visible units ordered by score, including explanatory rows that fail required criteria or fall below min_score. Only variants with matches_profile=true qualify as matches; context rows never determine the group score. Profile status criteria and shop isolation apply. Properties holding a status the shop excludes from search profile matching are never returned. Cursor pagination counts groups. Reuse all query parameters with next_cursor; restart without a cursor after changing the profile or query. Score details are included in each result.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "search_profile_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "limit",
      "in": "query",
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 200,
        "default": 25
      }
    },
    {
      "name": "cursor",
      "in": "query",
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "min_score",
      "in": "query",
      "schema": {
        "type": "number",
        "minimum": 0,
        "default": 0.01
      }
    },
    {
      "name": "sort_by",
      "in": "query",
      "description": "score, updated_at, flaeche, preis, teilbar_ab or a numeric/date search-profile field key.",
      "schema": {
        "type": "string",
        "default": "score"
      }
    },
    {
      "name": "sort_dir",
      "in": "query",
      "schema": {
        "type": "string",
        "enum": [
          "asc",
          "desc"
        ],
        "default": "desc"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Matching groups or standalone properties, including score details",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/SearchProfileMatchResults"
          }
        }
      }
    },
    "400": {
      "description": "Invalid cursor or unsupported sort field"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing search_profiles.read or properties.read scope"
    },
    "404": {
      "description": "Contact or search profile not found in this shop"
    },
    "422": {
      "description": "Archived or inactive search profile"
    },
    "503": {
      "description": "Matching temporarily unavailable"
    }
  }
}
```

## POST /contacts/{id}/search_profiles/{search_profile_id}/restore

Restore contact search profile

Requires `search_profiles.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "search_profile_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Restored search profile",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/SearchProfile"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Contact or search profile not found"
    }
  }
}
```

## GET /companies/{id}/search_profiles

List company search profiles

Requires `search_profiles.list`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Search profile list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/SearchProfile"
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "total": {
                    "type": "integer"
                  },
                  "profileable_type": {
                    "type": "string"
                  },
                  "profileable_id": {
                    "type": "integer"
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Company not found"
    }
  }
}
```

## POST /companies/{id}/search_profiles

Create or CRM-identity upsert company search profile

Requires `search_profiles.add`, or `search_profiles.edit` when `crm_source` and `crm_import_id` match an existing profile of this record. Set `validate_only=true` to validate and roll back without jobs.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "validate_only": {
              "type": "boolean",
              "default": false
            },
            "search_profile": {
              "$ref": "#/components/schemas/SearchProfileInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Search profile created"
    },
    "200": {
      "description": "Existing CRM-identified search profile updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Company not found"
    },
    "422": {
      "description": "Validation errors, including field-specific catalog rejection reasons",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/SearchProfileValidationError"
          }
        }
      }
    }
  }
}
```

## GET /companies/{id}/search_profiles/default_template

Fetch company search profile template

Requires `search_profiles.read`. Resolves the active template in this order: user, team, usage and object type, usage, target default, then the first eligible template. The final fallback is reported as type_default. Market parameters accept a scalar or repeated bracket parameters. If objektart is omitted, a positive sub_objektart infers its unique parent object type. When both are present, objektart takes precedence.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "nutzungsart",
      "in": "query",
      "schema": {
        "oneOf": [
          {
            "type": "string"
          },
          {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        ]
      }
    },
    {
      "name": "objektart",
      "in": "query",
      "schema": {
        "oneOf": [
          {
            "type": "string"
          },
          {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        ]
      }
    },
    {
      "name": "sub_objektart",
      "in": "query",
      "description": "Infers the unique parent object type only when objektart is omitted.",
      "schema": {
        "oneOf": [
          {
            "type": "string"
          },
          {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        ]
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Default template",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/SearchProfileTemplate"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Company not found"
    }
  }
}
```

## GET /companies/{id}/search_profiles/{search_profile_id}

Fetch company search profile

Requires `search_profiles.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "search_profile_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "schema"
        ]
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Search profile payload",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/SearchProfile"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Company or search profile not found"
    }
  }
}
```

## PATCH /companies/{id}/search_profiles/{search_profile_id}

Update company search profile

Requires `search_profiles.edit`. Partial update. validate_only=true rolls back without persistence, jobs or lifecycle events; returns meta.validate_only.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "search_profile_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "validate_only": {
              "type": "boolean",
              "default": false
            },
            "search_profile": {
              "$ref": "#/components/schemas/SearchProfileInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Search profile updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Company or search profile not found"
    },
    "422": {
      "description": "Validation errors, including field-specific catalog rejection reasons",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/SearchProfileValidationError"
          }
        }
      }
    }
  }
}
```

## PUT /companies/{id}/search_profiles/{search_profile_id}

Update company search profile

Requires `search_profiles.edit`. Partial update. validate_only=true rolls back without persistence, jobs or lifecycle events; returns meta.validate_only.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "search_profile_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "validate_only": {
              "type": "boolean",
              "default": false
            },
            "search_profile": {
              "$ref": "#/components/schemas/SearchProfileInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Search profile updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Company or search profile not found"
    },
    "422": {
      "description": "Validation errors, including field-specific catalog rejection reasons",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/SearchProfileValidationError"
          }
        }
      }
    }
  }
}
```

## DELETE /companies/{id}/search_profiles/{search_profile_id}

Archive company search profile

Requires `search_profiles.delete`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "search_profile_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Archived"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Company or search profile not found"
    }
  }
}
```

## GET /companies/{id}/search_profiles/{search_profile_id}/results

Match properties for a company search profile

Requires `search_profiles.read` and `properties.read`. Returns live matches with score explanations. Each project's or areal's best eligible unit supplies the score, field values and property_id; id identifies the displayed group. parent_id is the matching unit's immediate parent (omitted for root properties). variants contains visible units ordered by score, including explanatory rows that fail required criteria or fall below min_score. Only variants with matches_profile=true qualify as matches; context rows never determine the group score. Profile status criteria and shop isolation apply. Properties holding a status the shop excludes from search profile matching are never returned. Cursor pagination counts groups. Reuse all query parameters with next_cursor; restart without a cursor after changing the profile or query. Score details are included in each result.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "search_profile_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "limit",
      "in": "query",
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 200,
        "default": 25
      }
    },
    {
      "name": "cursor",
      "in": "query",
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "min_score",
      "in": "query",
      "schema": {
        "type": "number",
        "minimum": 0,
        "default": 0.01
      }
    },
    {
      "name": "sort_by",
      "in": "query",
      "description": "score, updated_at, flaeche, preis, teilbar_ab or a numeric/date search-profile field key.",
      "schema": {
        "type": "string",
        "default": "score"
      }
    },
    {
      "name": "sort_dir",
      "in": "query",
      "schema": {
        "type": "string",
        "enum": [
          "asc",
          "desc"
        ],
        "default": "desc"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Matching groups or standalone properties, including score details",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/SearchProfileMatchResults"
          }
        }
      }
    },
    "400": {
      "description": "Invalid cursor or unsupported sort field"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing search_profiles.read or properties.read scope"
    },
    "404": {
      "description": "Company or search profile not found in this shop"
    },
    "422": {
      "description": "Archived or inactive search profile"
    },
    "503": {
      "description": "Matching temporarily unavailable"
    }
  }
}
```

## POST /companies/{id}/search_profiles/{search_profile_id}/restore

Restore company search profile

Requires `search_profiles.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "search_profile_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Restored search profile",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/SearchProfile"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Company or search profile not found"
    }
  }
}
```

## GET /companies

List companies

Requires `companies.list`. Returns companies using cursor pagination. Default response is summary fields unless `fields=full` is provided. Filters are optional and AND-combined. `tag_ids` and `status_ids` accept comma-separated IDs (OR within each list). Example: `/companies?status_ids=7&active=true&limit=50`

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "limit",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 200
      }
    },
    {
      "name": "cursor",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "updated_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "sort",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "updated_at",
          "created_at"
        ]
      },
      "description": "Sort field for cursor pagination"
    },
    {
      "name": "direction",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "asc",
          "desc"
        ]
      },
      "description": "Sort direction (default asc)"
    },
    {
      "name": "include_deleted",
      "in": "query",
      "required": false,
      "schema": {
        "type": "boolean",
        "description": "Include soft-deleted records"
      }
    },
    {
      "name": "deleted_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time",
        "description": "Return only soft-deleted records deleted since this timestamp"
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated includes (tags,statuses,associations,locations)"
      }
    },
    {
      "name": "status_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated status IDs (any match)",
        "example": "12,34"
      }
    },
    {
      "name": "tag_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated tag IDs (any match)",
        "example": "5,9"
      }
    },
    {
      "name": "active",
      "in": "query",
      "required": false,
      "schema": {
        "type": "boolean",
        "example": true
      }
    },
    {
      "name": "email",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "email",
        "example": "info@example.com"
      },
      "description": "Returns every company that owns this address as primary or additional email (exact match, case-insensitive, surrounding whitespace ignored). Several companies may share one address, so the result can contain more than one company; use the returned `id` to address a single company."
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include_deleted",
      "in": "query",
      "required": false,
      "schema": {
        "type": "boolean"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Company list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/CompanySummary"
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "limit": {
                    "type": "integer"
                  },
                  "has_more": {
                    "type": "boolean"
                  },
                  "next_cursor": {
                    "type": "string",
                    "nullable": true
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Invalid cursor, updated_since, or fields"
    }
  }
}
```

## POST /companies

Create company

Requires `companies.add`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "company": {
              "$ref": "#/components/schemas/CompanyInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Company created",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Company"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Validation errors",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/ValidationFailedResponse"
          }
        }
      }
    }
  }
}
```

## POST /companies/batch

Batch upsert companies

Requires `companies.add` if any item has no `id`, and `companies.edit` if any item has an `id` or a `lookup`. Upserts multiple companies in one request. If any item is invalid, the batch fails and no changes are applied. Requires `companies.add` for new records and `companies.edit` for items with `id` or `lookup`. Max batch size: 100. Set `validate_only=true` to execute and roll back the complete batch.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "validate_only": {
              "type": "boolean",
              "default": false
            },
            "companies": {
              "type": "array",
              "items": {
                "$ref": "#/components/schemas/CompanyBatchItem"
              }
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Batch result",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/Company"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/ValidationFailedResponse"
          }
        }
      }
    }
  }
}
```

## POST /companies/bulk_delete

Bulk delete companies

Requires `companies.delete`. Soft-deletes multiple companies in one request.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "ids": {
              "type": "array",
              "items": {
                "type": "integer"
              }
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Bulk delete result",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "object",
                "properties": {
                  "deleted_ids": {
                    "type": "array",
                    "items": {
                      "type": "integer"
                    }
                  },
                  "not_found_ids": {
                    "type": "array",
                    "items": {
                      "type": "integer"
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
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "413": {
      "description": "Batch limit exceeded"
    },
    "422": {
      "description": "Validation errors",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/ValidationFailedResponse"
          }
        }
      }
    }
  }
}
```

## POST /contacts/bulk_delete

Bulk delete contacts

Requires `contacts.delete`. Soft-deletes multiple contacts in one request.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "ids": {
              "type": "array",
              "items": {
                "type": "integer"
              }
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Bulk delete result",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "object",
                "properties": {
                  "deleted_ids": {
                    "type": "array",
                    "items": {
                      "type": "integer"
                    }
                  },
                  "not_found_ids": {
                    "type": "array",
                    "items": {
                      "type": "integer"
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
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "413": {
      "description": "Batch limit exceeded"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /companies/{id}

Fetch company

Requires `companies.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "ETag from a previous GET response"
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated includes (tags,statuses,associations,locations)"
      }
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include_deleted",
      "in": "query",
      "required": false,
      "schema": {
        "type": "boolean"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Company payload",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Company"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /companies/{id}

Update company

Requires `companies.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "ETag from a previous GET response"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "company": {
              "$ref": "#/components/schemas/CompanyInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Company updated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Company"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /companies/{id}

Update company

Requires `companies.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "ETag from a previous GET response"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "company": {
              "$ref": "#/components/schemas/CompanyInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Company updated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Company"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## DELETE /companies/{id}

Delete company (soft delete)

Requires `companies.delete`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /leases

List leases

Requires `leases.list`. Returns only leases belonging to the API key's shop. Pagination is ordered by `updated_at`, then `id`. Lease search is not indexed yet, so custom-field filters intentionally use strict exact scalar matching only.

Status: documented, not live-tested.

```json
{
  "parameters": [
    {
      "name": "limit",
      "in": "query",
      "schema": {
        "type": "integer",
        "default": 50,
        "maximum": 200
      }
    },
    {
      "name": "cursor",
      "in": "query",
      "schema": {
        "type": "string"
      },
      "description": "Opaque cursor returned by the previous page"
    },
    {
      "name": "filters",
      "in": "query",
      "description": "JSON array of canonical filter objects. Fields are `status`, `property_id`, or a configured scalar `custom_*` field; operators are `eq` and `in`. Unknown fields, operators, types, and status values return `invalid_filter`.",
      "schema": {
        "type": "string"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Cursor-paged lease collection",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/Lease"
                }
              },
              "meta": {
                "$ref": "#/components/schemas/CursorMeta"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Missing or invalid API key"
    },
    "403": {
      "description": "Missing leases.list scope or disallowed IP"
    },
    "422": {
      "description": "Invalid filter or cursor"
    }
  }
}
```

## POST /leases

Create a lease

Requires `leases.add`. The property, contacts, and companies must belong to the API key's shop. Tenant associations are applied by the canonical Lease domain service. At least one active tenant is required.

Status: documented, not live-tested.

```json
{
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "lease"
          ],
          "properties": {
            "lease": {
              "$ref": "#/components/schemas/LeaseInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Created",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Lease"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Missing or invalid API key"
    },
    "403": {
      "description": "Missing leases.add scope or disallowed IP"
    },
    "422": {
      "description": "Invalid payload",
      "association": null,
      "property": null,
      "custom field": null,
      "or lease validation": null
    }
  }
}
```

## GET /leases/{id}

Get a lease

Requires `leases.read`. Returns an ETag. Cross-shop and missing records both return 404.

Status: documented, not live-tested.

```json
{
  "responses": {
    "200": {
      "description": "Lease",
      "headers": {
        "ETag": {
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Lease"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Missing or invalid API key"
    },
    "403": {
      "description": "Missing leases.read scope or disallowed IP"
    },
    "404": {
      "description": "Lease not found"
    }
  }
}
```

## PATCH /leases/{id}

Partially update a lease

Requires `leases.edit`. Omitted fields, custom fields, contacts, and companies remain unchanged. Sending contacts or companies replaces that submitted tenant collection through the canonical Lease service. If-Match is optional; a stale value returns 412.

Status: documented, not live-tested.

```json
{
  "parameters": [
    {
      "name": "If-Match",
      "in": "header",
      "schema": {
        "type": "string"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "lease"
          ],
          "properties": {
            "lease": {
              "$ref": "#/components/schemas/LeaseInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Updated lease",
      "headers": {
        "ETag": {
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Lease"
              }
            }
          }
        }
      }
    },
    "403": {
      "description": "Missing leases.edit scope"
    },
    "404": {
      "description": "Lease not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation failed"
    }
  }
}
```

## PUT /leases/{id}



Requires `leases.edit`.

Status: documented, not live-tested.

```json
{}
```

## DELETE /leases/{id}

Soft-delete a lease

Requires `leases.delete`. The lease is retained as deleted data and excluded from list/show.

Status: documented, not live-tested.

```json
{
  "responses": {
    "204": {
      "description": "Soft-deleted"
    },
    "403": {
      "description": "Missing leases.delete scope"
    },
    "404": {
      "description": "Lease not found"
    }
  }
}
```

## GET /properties

List properties

Requires `properties.list`. Returns properties using cursor pagination. Default response is summary fields unless `fields=full` is provided. Full responses include only website-safe images; summary responses omit images. Filters are optional and AND-combined. `tag_ids`, `status_ids`, and `user_ids` accept comma-separated IDs (OR within each list). Example: `/properties?user_ids=149&archived=true&updated_since=2025-01-15T10:00:00Z` Requires the `properties.list` scope. For exact website/OpenImmo references, use `/properties?einheitennummer=8878` or `/properties?auftragsnummer=WEB-8878` instead of the fuzzy `/search/properties?q=8878` search. Numbers are matched as complete, case-sensitive strings without trimming or numeric conversion; leading zeros are significant. Both parameters together must match the same property. These lookups read current stored values without waiting for search indexing. The response remains a paginated list: use the returned `data[].id` for notes and tasks only when exactly one match exists (`data.length == 1` and `meta.has_more == false`). No match returns HTTP 200 with `data: []`; duplicate references return all matches, not an arbitrary first match. Soft-deleted properties remain excluded unless explicitly requested. GET `/properties/{id}` is unchanged.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "limit",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 200
      }
    },
    {
      "name": "cursor",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "updated_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "sort",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "updated_at",
          "created_at"
        ]
      },
      "description": "Sort field for cursor pagination"
    },
    {
      "name": "direction",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "asc",
          "desc"
        ]
      },
      "description": "Sort direction (default asc)"
    },
    {
      "name": "include_deleted",
      "in": "query",
      "required": false,
      "schema": {
        "type": "boolean",
        "description": "Include soft-deleted records"
      }
    },
    {
      "name": "deleted_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time",
        "description": "Return only soft-deleted records deleted since this timestamp"
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated includes (tags,statuses,associations)"
      }
    },
    {
      "name": "status_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated status IDs (any match)",
        "example": "12,34"
      }
    },
    {
      "name": "tag_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated tag IDs (any match)",
        "example": "5,9"
      }
    },
    {
      "name": "user_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated primary responsible user IDs (any match)",
        "example": "149,207"
      }
    },
    {
      "name": "einheitennummer",
      "in": "query",
      "required": false,
      "description": "Exact unit number (case-sensitive, no partial matching). Empty or non-string values return 422 invalid_einheitennummer.",
      "schema": {
        "type": "string",
        "minLength": 1,
        "example": "8878"
      }
    },
    {
      "name": "auftragsnummer",
      "in": "query",
      "required": false,
      "description": "Exact order number (case-sensitive, no partial matching). Empty or non-string values return 422 invalid_auftragsnummer.",
      "schema": {
        "type": "string",
        "minLength": 1,
        "example": "WEB-8878"
      }
    },
    {
      "name": "archived",
      "in": "query",
      "required": false,
      "schema": {
        "type": "boolean",
        "example": false
      }
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Property list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "anyOf": [
                    {
                      "$ref": "#/components/schemas/PropertySummary"
                    },
                    {
                      "$ref": "#/components/schemas/Property"
                    }
                  ]
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "limit": {
                    "type": "integer"
                  },
                  "has_more": {
                    "type": "boolean"
                  },
                  "next_cursor": {
                    "type": "string",
                    "nullable": true
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Invalid cursor, updated_since, fields, einheitennummer, or auftragsnummer"
    }
  }
}
```

## POST /properties

Create property

Requires `properties.add`. Creates a property. `parent_id` can place a standard property below a project or a project below an areal. Invalid, cross-organization, or cyclic hierarchy assignments return `422`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "property": {
              "$ref": "#/components/schemas/PropertyInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Property created",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Property"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Validation errors, including unsupported property enum values",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/ValidationFailedResponse"
          }
        }
      }
    }
  }
}
```

## POST /properties/batch

Batch upsert properties

Requires `properties.add` if any item has no `id`, and `properties.edit` if any item has an `id`. Upserts multiple properties in one request. If any item is invalid, the batch fails and no changes are applied. Requires `properties.add` for new records and `properties.edit` for items with `id`. Max batch size: 100.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "properties": {
              "type": "array",
              "items": {
                "$ref": "#/components/schemas/PropertyBatchItem"
              }
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Batch result",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/Property"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Item validation error; the complete batch is rolled back",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/PropertyBatchValidationFailedResponse"
          }
        }
      }
    }
  }
}
```

## GET /properties/{id}

Fetch property

Requires `properties.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated includes (tags,statuses,associations)"
      }
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Property payload",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "anyOf": [
                  {
                    "$ref": "#/components/schemas/PropertySummary"
                  },
                  {
                    "$ref": "#/components/schemas/Property"
                  }
                ]
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Invalid fields"
    }
  }
}
```

## PATCH /properties/{id}

Update property

Requires `properties.edit`. Partially updates a property. Submit `parent_id` to move it within the supported hierarchy, or `null` to detach it. Submit `landingpage_id` to assign a compatible property/project landingpage template, or `null` to clear it. Invalid, cross-organization, incompatible, or cyclic assignments return `422`. `etagenposition` (whole number from 1) orders a unit left to right within its floor (`etage`) of its parent project; a position already taken on that floor is assigned to this unit and the units from that position onward move back by one.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "ETag from a previous GET response"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "property": {
              "$ref": "#/components/schemas/PropertyInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Property updated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Property"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors, including unsupported property enum values",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/ValidationFailedResponse"
          }
        }
      }
    }
  }
}
```

## PUT /properties/{id}

Update property

Requires `properties.edit`. Partially updates a property. Submit `parent_id` to move it within the supported hierarchy, or `null` to detach it. Submit `landingpage_id` to assign a compatible property/project landingpage template, or `null` to clear it. Invalid, cross-organization, incompatible, or cyclic assignments return `422`. `etagenposition` (whole number from 1) orders a unit left to right within its floor (`etage`) of its parent project; a position already taken on that floor is assigned to this unit and the units from that position onward move back by one.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "ETag from a previous GET response"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "property": {
              "$ref": "#/components/schemas/PropertyInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Property updated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Property"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors, including unsupported property enum values",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/ValidationFailedResponse"
          }
        }
      }
    }
  }
}
```

## DELETE /properties/{id}

Delete property (soft delete)

Requires `properties.delete`. Areals must be deleted in the CRM with an explicit detach or cascade strategy; this endpoint returns `areal_delete_strategy_required` for them.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Invalid fields"
    }
  }
}
```

## GET /properties/{id}/images

List all property image records

Requires `property_images.list`. Authenticated management feed requiring `property_images.list`. Unlike the website-safe images nested in full property responses, this returns every image record, including hidden, proof-only, processing, unattached, and non-image records. This includes the automatically generated location map (`media_tag: macro_location`, title `Lage`), which is unpublished by default. URLs refer only to the currently selected content (`current_version_id`); alternate content versions are never returned. Size URLs use existing variants and may fall back to the current original URL.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Complete ordered image management feed",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/PropertyImageManagement"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing property_images.list scope"
    },
    "404": {
      "description": "Property not found in the API key shop"
    }
  }
}
```

## GET /properties/{id}/media

List property media

Requires `properties.media`. Returns all property photos and floorplans in their effective gallery order. Creating or changing property coordinates asynchronously creates or replaces one automatic `macro_location` image titled `Lage`, rendered with the location-map style configured for the shop. It is returned here with `publish_on_landingpage: false`; separately uploaded macro-location images are not replaced. Requires `properties.media`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Ordered media list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/PropertyImageManagement"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing properties.media scope"
    },
    "404": {
      "description": "Property not found in the API key shop"
    }
  }
}
```

## POST /properties/{id}/media

Upload property media

Requires `properties.media`. Uploads 1–20 images per multipart request, with a maximum size of 50 MB per file. Supported detected content types are JPEG, PNG, GIF, WebP, HEIC, and HEIF. Client-declared MIME types are not trusted. Optional `media` entries correspond by array index to `files`; `media_tag` takes precedence over `is_floorplan`. Uploads use the same stable storage, original-version, thumbnail, analysis, and deferred medium/large variant pipeline as UI uploads. Requires `properties.media` and emits `properties.updated` once after success.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "multipart/form-data": {
        "schema": {
          "type": "object",
          "required": [
            "files"
          ],
          "properties": {
            "files": {
              "type": "array",
              "minItems": 1,
              "maxItems": 20,
              "items": {
                "type": "string",
                "format": "binary"
              }
            },
            "media": {
              "type": "array",
              "maxItems": 20,
              "items": {
                "$ref": "#/components/schemas/PropertyMediaMetadataInput"
              }
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Uploaded media",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/PropertyImageManagement"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing properties.media scope"
    },
    "404": {
      "description": "Property not found in the API key shop"
    },
    "422": {
      "description": "Missing file",
      "invalid content": null,
      "file too large": null,
      "invalid metadata": null,
      "or processing failure": null
    }
  }
}
```

## PUT /properties/{id}/media/order

Replace the complete property media order

Requires `properties.media`. `media_ids` must contain every current media ID exactly once. The resulting positions determine `einheit.bilder` and `einheit.bild1` through `einheit.bild9`; the first eligible non-floorplan is the title image. Requires `properties.media` and emits `properties.updated`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "media_ids"
          ],
          "properties": {
            "media_ids": {
              "type": "array",
              "uniqueItems": true,
              "items": {
                "type": "integer"
              }
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Reordered complete media list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/PropertyImageManagement"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing properties.media scope"
    },
    "404": {
      "description": "Property not found in the API key shop"
    },
    "422": {
      "description": "Incomplete",
      "duplicate": null,
      "or invalid media IDs": null
    }
  }
}
```

## PATCH /properties/{id}/media/{media_id}

Update property media metadata or position

Requires `properties.media`. Partially updates title, tags, media classification, or position. An explicit empty `tags` array clears tags. `media_tag` takes precedence over `is_floorplan`. Requires `properties.media` and emits `properties.updated`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "media_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/PropertyMediaMetadataPatchInput"
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Updated media",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/PropertyImageManagement"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing properties.media scope"
    },
    "404": {
      "description": "Property or media not found in the API key shop"
    },
    "422": {
      "description": "Invalid metadata",
      "unknown request property": null,
      "or position": null
    }
  }
}
```

## DELETE /properties/{id}/media/{media_id}

Delete property media

Requires `properties.media`. Emits `properties.updated` after deletion.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "media_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing properties.media scope"
    },
    "404": {
      "description": "Property or media not found in the API key shop"
    },
    "422": {
      "description": "Media is still referenced by a reel"
    }
  }
}
```

## GET /properties/{id}/links

List property links

Requires `properties.links`. Returns the property's local, mutable links in creation order. Inherited global links are intentionally omitted. Requires `properties.links`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Ordered property link list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/PropertyLink"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing properties.links scope"
    },
    "404": {
      "description": "Property not found in the API key shop"
    }
  }
}
```

## POST /properties/{id}/links

Create a property link

Requires `properties.links`. Emits `properties.updated` after success.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/PropertyLinkCreateInput"
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Created property link",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/PropertyLink"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing properties.links scope"
    },
    "404": {
      "description": "Property not found in the API key shop"
    },
    "422": {
      "description": "Invalid or unknown request property"
    }
  }
}
```

## GET /properties/{id}/links/{link_id}

Get a property link

Requires `properties.links`. Returns one local property link.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "link_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Property link",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/PropertyLink"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing properties.links scope"
    },
    "404": {
      "description": "Property or link not found in the API key shop"
    }
  }
}
```

## PATCH /properties/{id}/links/{link_id}

Update a property link

Requires `properties.links`. Partially updates a local property link; omitted properties stay unchanged. Requires `properties.links` and emits `properties.updated` after success.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "link_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/PropertyLinkPatchInput"
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Updated property link",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/PropertyLink"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing properties.links scope"
    },
    "404": {
      "description": "Property or link not found in the API key shop"
    },
    "422": {
      "description": "Invalid or unknown request property"
    }
  }
}
```

## PUT /properties/{id}/links/{link_id}

Update a property link

Requires `properties.links`. Same as PATCH.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "link_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/PropertyLinkPatchInput"
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Updated property link",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/PropertyLink"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing properties.links scope"
    },
    "404": {
      "description": "Property or link not found in the API key shop"
    },
    "422": {
      "description": "Invalid or unknown request property"
    }
  }
}
```

## DELETE /properties/{id}/links/{link_id}

Delete a property link

Requires `properties.links`. Emits `properties.updated` after deletion.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "link_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing properties.links scope"
    },
    "404": {
      "description": "Property or link not found in the API key shop"
    }
  }
}
```

## POST /properties/bulk_delete

Bulk delete properties

Requires `properties.delete`. Soft-deletes multiple properties in one request. Areals require an explicit CRM lifecycle strategy and return `areal_delete_strategy_required`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "ids": {
              "type": "array",
              "items": {
                "type": "integer"
              }
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Bulk delete result",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "object",
                "properties": {
                  "deleted_ids": {
                    "type": "array",
                    "items": {
                      "type": "integer"
                    }
                  },
                  "not_found_ids": {
                    "type": "array",
                    "items": {
                      "type": "integer"
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
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "413": {
      "description": "Batch limit exceeded"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /properties/{id}/associations

Fetch property associations

Requires `properties.read`. Returns tags, statuses, and relationship IDs for a property.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Property associations",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "object",
                "properties": {
                  "id": {
                    "type": "integer"
                  },
                  "tag_ids": {
                    "type": "array",
                    "items": {
                      "type": "integer"
                    }
                  },
                  "status_ids": {
                    "type": "array",
                    "items": {
                      "type": "integer"
                    }
                  },
                  "associations": {
                    "type": "object",
                    "properties": {
                      "contacts": {
                        "type": "object",
                        "properties": {
                          "owners": {
                            "type": "array",
                            "items": {
                              "type": "integer"
                            }
                          },
                          "buyers": {
                            "type": "array",
                            "items": {
                              "type": "integer"
                            }
                          },
                          "renters": {
                            "type": "array",
                            "items": {
                              "type": "integer"
                            }
                          },
                          "associated": {
                            "type": "array",
                            "items": {
                              "type": "integer"
                            }
                          }
                        }
                      },
                      "companies": {
                        "type": "object",
                        "properties": {
                          "owners": {
                            "type": "array",
                            "items": {
                              "type": "integer"
                            }
                          }
                        }
                      },
                      "service_providers": {
                        "type": "array",
                        "items": {
                          "type": "object",
                          "properties": {
                            "entity_id": {
                              "type": "integer"
                            },
                            "entity_type": {
                              "type": "string"
                            },
                            "custom_label": {
                              "type": "string",
                              "nullable": true
                            },
                            "reciprocal_label": {
                              "type": "string",
                              "nullable": true
                            }
                          }
                        }
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
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /properties/{id}/associations

Update property associations

Requires `properties.edit`. Updates tags, statuses, and associations for a property.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "associations": {
              "type": "object",
              "description": "Same association keys as property create/update."
            }
          }
        },
        "example": {
          "associations": {
            "tag_ids": [
              7
            ],
            "status_ids": [
              11
            ],
            "contact_associations_owners": [
              {
                "contact_id": 4
              }
            ],
            "company_associations_owners": [
              {
                "company_id": 12
              }
            ],
            "service_provider_relationships": [
              {
                "entity_type": "company",
                "entity_id": 12,
                "custom_label": "Hausverwaltung"
              }
            ]
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Updated associations"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /properties/{id}/associations

Replace property associations

Requires `properties.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "associations": {
              "type": "object",
              "description": "Same association keys as property create/update."
            }
          }
        },
        "example": {
          "associations": {
            "tag_ids": [],
            "status_ids": [],
            "company_associations_owners": []
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Updated associations"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## POST /properties/{id}/restore

Restore property

Requires `properties.delete`. Restores a soft-deleted property.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Restored property",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Property"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /pipelines

List pipelines

Requires `pipelines.list`. Returns pipelines using cursor pagination.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "limit",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 200
      }
    },
    {
      "name": "cursor",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "archived",
      "in": "query",
      "required": false,
      "schema": {
        "type": "boolean"
      }
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated includes (columns)"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Pipeline list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/Pipeline"
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "limit": {
                    "type": "integer"
                  },
                  "has_more": {
                    "type": "boolean"
                  },
                  "next_cursor": {
                    "type": "string",
                    "nullable": true
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Invalid cursor"
    }
  }
}
```

## POST /pipelines

Create pipeline

Requires `pipelines.add`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "pipeline": {
              "$ref": "#/components/schemas/PipelineInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Pipeline created",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Pipeline"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /pipelines/{id}

Fetch pipeline

Requires `pipelines.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated includes (columns)"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Pipeline details",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Pipeline"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /pipelines/{id}

Update pipeline

Requires `pipelines.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "pipeline": {
              "$ref": "#/components/schemas/PipelineInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Pipeline updated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Pipeline"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /pipelines/{id}

Update pipeline

Requires `pipelines.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "pipeline": {
              "$ref": "#/components/schemas/PipelineInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Pipeline updated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Pipeline"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## DELETE /pipelines/{id}

Archive pipeline

Requires `pipelines.delete`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Archived"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## POST /pipelines/{id}/restore

Restore pipeline

Requires `pipelines.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Restored pipeline",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Pipeline"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /pipeline_columns

List pipeline columns

Requires `pipeline_columns.list`. Returns pipeline columns using cursor pagination.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "limit",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 200
      }
    },
    {
      "name": "cursor",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "pipeline_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "archived",
      "in": "query",
      "required": false,
      "schema": {
        "type": "boolean"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Pipeline column list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/PipelineColumn"
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "limit": {
                    "type": "integer"
                  },
                  "has_more": {
                    "type": "boolean"
                  },
                  "next_cursor": {
                    "type": "string",
                    "nullable": true
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Invalid cursor"
    }
  }
}
```

## POST /pipeline_columns

Create pipeline column

Requires `pipeline_columns.add`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "pipeline_column": {
              "$ref": "#/components/schemas/PipelineColumnInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Pipeline column created",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/PipelineColumn"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /pipeline_columns/{id}

Fetch pipeline column

Requires `pipeline_columns.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Pipeline column details",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/PipelineColumn"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /pipeline_columns/{id}

Update pipeline column

Requires `pipeline_columns.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "pipeline_column": {
              "$ref": "#/components/schemas/PipelineColumnInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Pipeline column updated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/PipelineColumn"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /pipeline_columns/{id}

Update pipeline column

Requires `pipeline_columns.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "pipeline_column": {
              "$ref": "#/components/schemas/PipelineColumnInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Pipeline column updated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/PipelineColumn"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## DELETE /pipeline_columns/{id}

Archive pipeline column

Requires `pipeline_columns.delete`. System columns cannot be archived.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Archived"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "System column locked"
    }
  }
}
```

## POST /pipeline_columns/{id}/restore

Restore pipeline column

Requires `pipeline_columns.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Restored pipeline column",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/PipelineColumn"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /deals

List deals

Requires `deals.list`. Returns deals using cursor pagination. Default response is summary fields unless `fields=full` is provided. Filters are optional and AND-combined. ID filters accept comma-separated values (OR within each list).

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "limit",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 200
      }
    },
    {
      "name": "cursor",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "sort",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "updated_at",
          "created_at",
          "closed_at"
        ]
      },
      "description": "Sort field for cursor pagination"
    },
    {
      "name": "direction",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "asc",
          "desc"
        ]
      },
      "description": "Sort direction (default desc)"
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated includes (assignees,contacts,companies,properties,pipeline,pipeline_column,creator)"
      }
    },
    {
      "name": "archived",
      "in": "query",
      "required": false,
      "schema": {
        "type": "boolean"
      }
    },
    {
      "name": "pipeline_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "creator_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "pipeline_column_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "assignee_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated user IDs"
      }
    },
    {
      "name": "contact_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated contact IDs"
      }
    },
    {
      "name": "company_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated company IDs"
      }
    },
    {
      "name": "property_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated property IDs"
      }
    },
    {
      "name": "updated_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "created_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "closed_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "tipster_contact_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Tippgeber-Tool only. Comma-separated contact IDs of the tipster role."
    },
    {
      "name": "tipster_company_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Tippgeber-Tool only. Comma-separated company IDs of the tipster role."
    },
    {
      "name": "tip_type",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Tippgeber-Tool only. Comma-separated tip types (sale, valuation, rental, search_profile, buyer, tenant)."
    },
    {
      "name": "tip_priority",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Tippgeber-Tool only. Comma-separated priorities (first, further)."
    },
    {
      "name": "tip_commission_status",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Tippgeber-Tool only. Comma-separated commission states (agreed, earned, paid_out)."
    },
    {
      "name": "tipster_number",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Tippgeber-Tool only. Comma-separated exact tipster IDs as stored on the deal."
    },
    {
      "name": "tipster_team_number",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Tippgeber-Tool only. Comma-separated exact team IDs as stored on the deal."
    },
    {
      "name": "tip_consent_confirmed_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date"
      },
      "description": "Tippgeber-Tool only. Deals whose consent was confirmed on or after this date."
    },
    {
      "name": "tip_commission_paid_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date"
      },
      "description": "Tippgeber-Tool only. Deals whose commission was paid out on or after this date."
    }
  ],
  "responses": {
    "200": {
      "description": "Deal list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/DealSummary"
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "limit": {
                    "type": "integer"
                  },
                  "has_more": {
                    "type": "boolean"
                  },
                  "next_cursor": {
                    "type": "string",
                    "nullable": true
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Invalid cursor or filters"
    }
  }
}
```

## POST /deals

Create deal

Requires `deals.add`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "deal": {
              "$ref": "#/components/schemas/DealInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Deal created",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Deal"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /deals/{id}

Fetch deal

Requires `deals.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated includes (assignees,contacts,companies,properties,pipeline,pipeline_column,creator)"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Deal details",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Deal"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /deals/{id}

Update deal

Requires `deals.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "deal": {
              "$ref": "#/components/schemas/DealInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Deal updated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Deal"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /deals/{id}

Update deal

Requires `deals.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "deal": {
              "$ref": "#/components/schemas/DealInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Deal updated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Deal"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## DELETE /deals/{id}

Archive deal

Requires `deals.delete`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Archived"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## POST /deals/{id}/restore

Restore deal

Requires `deals.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Restored deal",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Deal"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /deals/{id}/associations

Fetch deal associations

Requires `deals.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Deal associations",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/DealAssociations"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /deals/{id}/associations

Update deal associations

Requires `deals.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "deal": {
              "$ref": "#/components/schemas/DealAssociationsInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Deal associations updated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/DealAssociations"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /deals/{id}/associations

Update deal associations

Requires `deals.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "deal": {
              "$ref": "#/components/schemas/DealAssociationsInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Deal associations updated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/DealAssociations"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /deals/{deal_id}/attachments

List deal attachments

Requires `deal_attachments.list`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "deal_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Attachment list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/DealAttachment"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## POST /deals/{deal_id}/attachments

Upload deal attachments

Requires `deal_attachments.add`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "deal_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "multipart/form-data": {
        "schema": {
          "type": "object",
          "properties": {
            "files": {
              "type": "array",
              "items": {
                "type": "string",
                "format": "binary"
              }
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Attachments uploaded",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/DealAttachment"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Upload failed"
    }
  }
}
```

## DELETE /deals/{deal_id}/attachments/{id}

Delete deal attachment

Requires `deal_attachments.delete`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "deal_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      },
      "description": "Attachment blob ID"
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /deals/{deal_id}/attachments/{id}/download

Download deal attachment

Requires `deal_attachments.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "deal_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      },
      "description": "Attachment blob ID"
    }
  ],
  "responses": {
    "302": {
      "description": "Redirect to download URL"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /tasks

List tasks

Requires `tasks.list`. Returns tasks using cursor pagination. Default response is summary fields unless `fields=full` is provided. Filters are optional and AND-combined. ID filters accept comma-separated values (OR within each list).

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "limit",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 200
      }
    },
    {
      "name": "cursor",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "sort",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "updated_at",
          "created_at",
          "due_at"
        ]
      },
      "description": "Sort field for cursor pagination"
    },
    {
      "name": "direction",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "asc",
          "desc"
        ]
      },
      "description": "Sort direction (default desc)"
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated includes (assignees,contacts,companies,properties,subtasks,category)"
      }
    },
    {
      "name": "status",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "open",
          "completed"
        ]
      }
    },
    {
      "name": "priority",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "low",
          "normal",
          "high"
        ]
      }
    },
    {
      "name": "task_category_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "due_from",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "due_to",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "updated_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "created_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "assignee_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated user IDs"
      }
    },
    {
      "name": "contact_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated contact IDs"
      }
    },
    {
      "name": "company_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated company IDs"
      }
    },
    {
      "name": "property_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated property IDs"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Task list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/TaskSummary"
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "limit": {
                    "type": "integer"
                  },
                  "has_more": {
                    "type": "boolean"
                  },
                  "next_cursor": {
                    "type": "string",
                    "nullable": true
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Invalid cursor or filters"
    }
  }
}
```

## POST /tasks

Create task

Requires `tasks.add`. `team_ids` accepts team IDs returned by `GET /lookups/teams`. Omit it or send `[]` to create a task without a team restriction. Assigning a task category that is restricted to selected CRM users, roles, or teams returns `422 validation_failed`; API keys do not bypass category assignment restrictions.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "task": {
              "$ref": "#/components/schemas/TaskInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Task created",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Task"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Referenced team or association not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /tasks/{id}

Fetch task

Requires `tasks.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Task",
      "headers": {
        "ETag": {
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Task"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /tasks/{id}

Update task

Requires `tasks.edit`. Partial update. Omitted fields, including `team_ids`, remain unchanged; `team_ids: []` clears the team assignment. A task keeps its restricted category. Changing `task_category_id` to a restricted category returns `422 validation_failed`; changing away from one remains allowed.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Optional ETag for optimistic concurrency"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "task": {
              "$ref": "#/components/schemas/TaskInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Task updated",
      "headers": {
        "ETag": {
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Task"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /tasks/{id}

Update task

Requires `tasks.edit`. Partial update. Omitted fields, including `team_ids`, remain unchanged; `team_ids: []` clears the team assignment. A task keeps its restricted category. Changing `task_category_id` to a restricted category returns `422 validation_failed`; changing away from one remains allowed.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Optional ETag for optimistic concurrency"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "task": {
              "$ref": "#/components/schemas/TaskInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Task updated",
      "headers": {
        "ETag": {
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Task"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## DELETE /tasks/{id}

Delete task

Requires `tasks.delete`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /tasks/{id}/associations

Fetch task associations

Requires `tasks.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Associations payload",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/TaskAssociations"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /tasks/{id}/associations

Update task associations

Requires `tasks.edit`. Replaces only submitted association keys. Omitted keys, including `team_ids`, remain unchanged; `team_ids: []` clears the team assignment.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Optional ETag for optimistic concurrency"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "associations": {
              "$ref": "#/components/schemas/TaskAssociationsInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Associations updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /tasks/{id}/associations

Update task associations

Requires `tasks.edit`. Replaces only submitted association keys. Omitted keys, including `team_ids`, remain unchanged; `team_ids: []` clears the team assignment.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Optional ETag for optimistic concurrency"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "associations": {
              "$ref": "#/components/schemas/TaskAssociationsInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Associations updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## POST /tasks/{id}/complete

Mark task as completed

Requires `tasks.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Task completed",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Task"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## POST /tasks/{id}/reopen

Reopen task

Requires `tasks.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Task reopened",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Task"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /tasks/{task_id}/subtasks

List task subtasks

Requires `task_subtasks.list`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "task_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Subtask list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/TaskSubtask"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## POST /tasks/{task_id}/subtasks

Create task subtask

Requires `task_subtasks.add`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "task_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "subtask": {
              "$ref": "#/components/schemas/TaskSubtaskInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Subtask created",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/TaskSubtask"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /tasks/{task_id}/subtasks/{id}

Fetch task subtask

Requires `task_subtasks.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "task_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Subtask",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/TaskSubtask"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /tasks/{task_id}/subtasks/{id}

Update task subtask

Requires `task_subtasks.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "task_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "subtask": {
              "$ref": "#/components/schemas/TaskSubtaskInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Subtask updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /tasks/{task_id}/subtasks/{id}

Update task subtask

Requires `task_subtasks.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "task_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "subtask": {
              "$ref": "#/components/schemas/TaskSubtaskInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Subtask updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## DELETE /tasks/{task_id}/subtasks/{id}

Delete task subtask

Requires `task_subtasks.delete`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "task_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## POST /tasks/{task_id}/subtasks/{id}/complete

Complete task subtask

Requires `task_subtasks.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "task_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Subtask completed",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/TaskSubtask"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## POST /tasks/{task_id}/subtasks/{id}/reopen

Reopen task subtask

Requires `task_subtasks.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "task_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Subtask reopened",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/TaskSubtask"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /tasks/{task_id}/attachments

List task attachments

Requires `task_attachments.list`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "task_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Attachment list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/TaskAttachment"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## POST /tasks/{task_id}/attachments

Upload task attachments

Requires `task_attachments.add`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "task_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "multipart/form-data": {
        "schema": {
          "type": "object",
          "properties": {
            "files": {
              "type": "array",
              "items": {
                "type": "string",
                "format": "binary"
              }
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Attachments uploaded",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/TaskAttachment"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Upload failed"
    }
  }
}
```

## DELETE /tasks/{task_id}/attachments/{id}

Delete task attachment

Requires `task_attachments.delete`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "task_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      },
      "description": "Attachment blob ID"
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /tasks/{task_id}/attachments/{id}/download

Download task attachment

Requires `task_attachments.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "task_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      },
      "description": "Attachment blob ID"
    }
  ],
  "responses": {
    "302": {
      "description": "Redirect to download URL"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /tags

List tags

Requires `tags.list`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "model_type",
      "in": "query",
      "required": false,
      "schema": {
        "$ref": "#/components/schemas/TagModelType"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Tag list"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    }
  }
}
```

## POST /tags

Create tag

Requires `tags.add`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "tag"
          ],
          "properties": {
            "tag": {
              "$ref": "#/components/schemas/TagInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Tag created"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /tags/upsert

Upsert tag by model, category, and name

Requires `tags.add` when the category has no tag with this name, otherwise `tags.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "tag"
          ],
          "properties": {
            "tag": {
              "$ref": "#/components/schemas/TagInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Existing tag updated"
    },
    "201": {
      "description": "Tag created"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /tags/{id}

Fetch tag

Requires `tags.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Tag payload"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /tags/{id}

Update tag

Requires `tags.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "tag"
          ],
          "properties": {
            "tag": {
              "$ref": "#/components/schemas/TagPatchInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Tag updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /tags/{id}

Update tag

Requires `tags.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "tag"
          ],
          "properties": {
            "tag": {
              "$ref": "#/components/schemas/TagPatchInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Tag updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## DELETE /tags/{id}

Delete tag

Requires `tags.delete`. Returns 409 while assigned unless `force=true` is supplied.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "force",
      "in": "query",
      "required": false,
      "schema": {
        "type": "boolean"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "409": {
      "description": "Resource in use"
    }
  }
}
```

## GET /statuses

List statuses

Requires `statuses.list`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "model_type",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "Contact",
          "Company",
          "Property"
        ]
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Status list",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/StatusListResponse"
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    }
  }
}
```

## POST /statuses

Create status

Requires `statuses.add`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "status"
          ],
          "properties": {
            "status": {
              "$ref": "#/components/schemas/StatusInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Status created",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/StatusResponse"
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /statuses/upsert

Upsert status by model and name

Requires `statuses.add` when the model type has no status with this name, otherwise `statuses.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "status"
          ],
          "properties": {
            "status": {
              "$ref": "#/components/schemas/StatusInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Existing status updated",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/StatusResponse"
          }
        }
      }
    },
    "201": {
      "description": "Status created",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/StatusResponse"
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /statuses/{id}

Fetch status

Requires `statuses.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Status payload",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/StatusResponse"
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /statuses/{id}

Update status

Requires `statuses.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "status"
          ],
          "properties": {
            "status": {
              "$ref": "#/components/schemas/StatusPatchInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Status updated",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/StatusResponse"
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /statuses/{id}

Update status

Requires `statuses.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "status"
          ],
          "properties": {
            "status": {
              "$ref": "#/components/schemas/StatusPatchInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Status updated",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/StatusResponse"
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## DELETE /statuses/{id}

Delete status

Requires `statuses.delete`. Returns 409 while assigned unless `force=true` is supplied.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "force",
      "in": "query",
      "required": false,
      "schema": {
        "type": "boolean"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "409": {
      "description": "Resource in use"
    }
  }
}
```

## GET /sources

List sources

Requires `sources.list`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Source list"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    }
  }
}
```

## POST /sources

Create source

Requires `sources.add`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "source"
          ],
          "properties": {
            "source": {
              "$ref": "#/components/schemas/SourceInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Source created"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /sources/upsert

Upsert source by label

Requires `sources.add` when no source has this label, otherwise `sources.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "source"
          ],
          "properties": {
            "source": {
              "$ref": "#/components/schemas/SourceInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Existing source updated"
    },
    "201": {
      "description": "Source created"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /sources/{id}

Fetch source

Requires `sources.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Source payload"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /sources/{id}

Update source

Requires `sources.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "source"
          ],
          "properties": {
            "source": {
              "$ref": "#/components/schemas/SourcePatchInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Source updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /sources/{id}

Update source

Requires `sources.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "source"
          ],
          "properties": {
            "source": {
              "$ref": "#/components/schemas/SourcePatchInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Source updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## DELETE /sources/{id}

Delete source

Requires `sources.delete`. Returns 409 while assigned unless `force=true` is supplied.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "force",
      "in": "query",
      "required": false,
      "schema": {
        "type": "boolean"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "409": {
      "description": "Resource in use"
    }
  }
}
```

## GET /task_categories

List task categories

Requires one of `task_categories.list` or `tasks.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Category list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/TaskCategory"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    }
  }
}
```

## POST /task_categories

Create task category

Requires `task_categories.add`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "task_category": {
              "$ref": "#/components/schemas/TaskCategoryInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Category created",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/TaskCategory"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PATCH /task_categories/{id}

Update task category

Requires `task_categories.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "task_category": {
              "$ref": "#/components/schemas/TaskCategoryInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Category updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /task_categories/{id}

Update task category

Requires `task_categories.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "task_category": {
              "$ref": "#/components/schemas/TaskCategoryInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Category updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## DELETE /task_categories/{id}

Delete task category

Requires `task_categories.delete`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /notes

List notes

Requires `notes.list`. Returns notes using cursor pagination. Default response is summary fields unless `fields=full` is provided. Filters are optional and AND-combined. ID filters accept comma-separated values (OR within each list). The optional `filters` object uses the same field/operator contract as `/search/note`, including custom fields. Archived notes are omitted unless `include_archived=true` is supplied.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "project_ids",
      "in": "query",
      "description": "Comma-separated project IDs (OR). Matches direct links only, without descendants or inferred contact links.",
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "limit",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 200
      }
    },
    {
      "name": "cursor",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated includes (labels,assignees,assignee_teams,contacts,companies,properties,projects,tags)"
      }
    },
    {
      "name": "label_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated label IDs"
      }
    },
    {
      "name": "assignee_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated user IDs"
      }
    },
    {
      "name": "assignee_team_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated team IDs"
      }
    },
    {
      "name": "contact_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated contact IDs"
      }
    },
    {
      "name": "company_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated company IDs"
      }
    },
    {
      "name": "property_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated property IDs"
      }
    },
    {
      "name": "updated_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "include_archived",
      "in": "query",
      "required": false,
      "schema": {
        "type": "boolean",
        "default": false
      }
    },
    {
      "name": "filters",
      "in": "query",
      "required": false,
      "description": "JSON object using the canonical `/search/note` filter contract.",
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "created_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Note list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/NoteSummary"
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "limit": {
                    "type": "integer"
                  },
                  "has_more": {
                    "type": "boolean"
                  },
                  "next_cursor": {
                    "type": "string",
                    "nullable": true
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Invalid cursor or filters"
    }
  }
}
```

## POST /notes

Create note

Requires `notes.add`. Creates a note. Assigning a note category that is restricted to selected CRM users, roles, or teams returns `422 validation_failed`; API keys do not bypass category assignment restrictions.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "note": {
              "$ref": "#/components/schemas/NoteInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Note created",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Note"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /notes/{id}

Fetch note

Requires `notes.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Note",
      "headers": {
        "ETag": {
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Note"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /notes/{id}

Update note

Requires `notes.edit`. Partial update. Omitted association fields remain unchanged; explicit empty arrays clear the submitted association. Existing notes remain readable and editable regardless of their category restriction. Changing to a restricted category returns `422 validation_failed`; changing away from one remains allowed.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Optional ETag for optimistic concurrency"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "note": {
              "$ref": "#/components/schemas/NoteInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Note updated",
      "headers": {
        "ETag": {
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Note"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /notes/{id}

Update note

Requires `notes.edit`. Partial update. Omitted association fields remain unchanged; explicit empty arrays clear the submitted association. Existing notes remain readable and editable regardless of their category restriction. Changing to a restricted category returns `422 validation_failed`; changing away from one remains allowed.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Optional ETag for optimistic concurrency"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "note": {
              "$ref": "#/components/schemas/NoteInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Note updated",
      "headers": {
        "ETag": {
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Note"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## DELETE /notes/{id}

Delete note

Requires `notes.delete`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /notes/{id}/associations

Fetch note associations

Requires `notes.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Associations payload",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/NoteAssociations"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /notes/{id}/associations

Update note associations

Requires `notes.edit`. Replace only submitted association keys. Omitted keys remain unchanged; explicit empty arrays clear submitted associations. Changing `label_ids` to a restricted category returns `422 validation_failed`; changing away from one remains allowed.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Optional ETag for optimistic concurrency"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "associations": {
              "$ref": "#/components/schemas/NoteAssociationsInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Associations updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /notes/{id}/associations

Update note associations

Requires `notes.edit`. Replace only submitted association keys. Omitted keys remain unchanged; explicit empty arrays clear submitted associations. Changing `label_ids` to a restricted category returns `422 validation_failed`; changing away from one remains allowed.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Optional ETag for optimistic concurrency"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "associations": {
              "$ref": "#/components/schemas/NoteAssociationsInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Associations updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /notes/{note_id}/attachments

List note attachments

Requires `note_attachments.list`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "note_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Attachment list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/NoteAttachment"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## POST /notes/{note_id}/attachments

Upload note attachments

Requires `note_attachments.add`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "note_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "multipart/form-data": {
        "schema": {
          "type": "object",
          "properties": {
            "files": {
              "type": "array",
              "items": {
                "type": "string",
                "format": "binary"
              }
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Attachments uploaded",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/NoteAttachment"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Upload failed"
    }
  }
}
```

## DELETE /notes/{note_id}/attachments/{id}

Delete note attachment

Requires `note_attachments.delete`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "note_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      },
      "description": "Attachment blob ID"
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /notes/{note_id}/attachments/{id}/download

Download note attachment

Requires `note_attachments.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "note_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      },
      "description": "Attachment blob ID"
    }
  ],
  "responses": {
    "302": {
      "description": "Redirect to download URL"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /note_labels

List note labels

Requires `note_labels.list`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Label list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/NoteLabel"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    }
  }
}
```

## POST /note_labels

Create note label

Requires `note_labels.add`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "note_label": {
              "$ref": "#/components/schemas/NoteLabelInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Label created",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/NoteLabel"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PATCH /note_labels/{id}

Update note label

Requires `note_labels.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "note_label": {
              "$ref": "#/components/schemas/NoteLabelInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Label updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PUT /note_labels/{id}

Update note label

Requires `note_labels.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "note_label": {
              "$ref": "#/components/schemas/NoteLabelInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Label updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## DELETE /note_labels/{id}

Delete note label

Requires `note_labels.delete`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /booking_pages/{id}/available_slots

Read available booking slots

Requires `booking_pages.read`. Uses the existing active booking page's availability rules. Both bounds are required ISO 8601 timestamps with timezone offsets. Only slots whose start is at or after `from` and end is at or before `to` are returned. This does not reserve a slot.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "from",
      "in": "query",
      "required": true,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "to",
      "in": "query",
      "required": true,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Chronological available slots; an empty array means none are available",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "required": [
              "data"
            ],
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "type": "object",
                  "required": [
                    "start",
                    "end"
                  ],
                  "properties": {
                    "start": {
                      "type": "string",
                      "format": "date-time"
                    },
                    "end": {
                      "type": "string",
                      "format": "date-time"
                    }
                  }
                }
              }
            }
          },
          "example": {
            "data": [
              {
                "start": "2026-09-08T09:00:00+02:00",
                "end": "2026-09-08T09:30:00+02:00"
              }
            ]
          }
        }
      }
    },
    "401": {
      "description": "Missing or invalid API key"
    },
    "403": {
      "description": "Missing scope or IP not allowed"
    },
    "404": {
      "description": "Booking page not found in the API key's shop"
    },
    "422": {
      "description": "`invalid_range` (missing/invalid bounds or to ≤ from), or `booking_page_inactive`"
    },
    "429": {
      "description": "API key rate limit exceeded"
    },
    "503": {
      "description": "`availability_unavailable`; availability could not be calculated, not an empty calendar"
    }
  }
}
```

## POST /booking_pages/{id}/bookings

Book an available appointment for an existing contact

Requires `bookings.add`. Submit an exact start/end pair from the available slots endpoint. Uses the normal booking workflow and revalidates under locks. The contact must belong to the same shop. The page determines the property, owner and calendar. At most one active future booking per contact/page; retries reject rather than replaying a prior response. Does not support arbitrary calendar events, changing bookings, or bypassing booking-page rules.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "booking"
          ],
          "properties": {
            "booking": {
              "type": "object",
              "required": [
                "contact_id",
                "slot_start",
                "slot_end"
              ],
              "properties": {
                "contact_id": {
                  "type": "integer"
                },
                "slot_start": {
                  "type": "string",
                  "format": "date-time"
                },
                "slot_end": {
                  "type": "string",
                  "format": "date-time"
                }
              }
            }
          }
        },
        "example": {
          "booking": {
            "contact_id": 123,
            "slot_start": "2026-09-08T09:00:00+02:00",
            "slot_end": "2026-09-08T09:30:00+02:00"
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Booking and calendar event persisted; external delivery remains asynchronous",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "required": [
              "data"
            ],
            "properties": {
              "data": {
                "type": "object",
                "required": [
                  "id",
                  "booking_page_id",
                  "calendar_event_id",
                  "contact_id",
                  "property_id",
                  "status",
                  "slot_start",
                  "slot_end"
                ],
                "properties": {
                  "id": {
                    "type": "integer"
                  },
                  "booking_page_id": {
                    "type": "integer"
                  },
                  "calendar_event_id": {
                    "type": "integer",
                    "description": "For mass viewings, the shared session calendar event ID"
                  },
                  "contact_id": {
                    "type": "integer"
                  },
                  "property_id": {
                    "type": "integer",
                    "nullable": true
                  },
                  "status": {
                    "type": "string",
                    "enum": [
                      "confirmed"
                    ]
                  },
                  "slot_start": {
                    "type": "string",
                    "format": "date-time"
                  },
                  "slot_end": {
                    "type": "string",
                    "format": "date-time"
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Missing or invalid API key"
    },
    "403": {
      "description": "Missing scope or IP not allowed"
    },
    "404": {
      "description": "Booking page or contact not found in the API key's shop"
    },
    "422": {
      "description": "`invalid_payload`, `booking_page_inactive`, `slot_unavailable`, or `validation_failed` with field errors"
    },
    "429": {
      "description": "API key rate limit exceeded"
    },
    "503": {
      "description": "`availability_unavailable`; availability could not be calculated"
    }
  }
}
```

## GET /calendar_events

List calendar events

Requires `calendar_events.list`. Returns calendar events using cursor pagination. Default response is summary fields unless `fields=full` is provided. Private events are excluded from the public API. Filters are optional and AND-combined. ID filters accept comma-separated values (OR within each list).

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "project_ids",
      "in": "query",
      "description": "Comma-separated project IDs (OR). Matches direct links only, without descendants or inferred contact links.",
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "limit",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 200
      }
    },
    {
      "name": "cursor",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "sort",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "updated_at",
          "created_at",
          "start_at",
          "end_at"
        ]
      },
      "description": "Sort field for cursor pagination"
    },
    {
      "name": "direction",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "asc",
          "desc"
        ]
      },
      "description": "Sort direction (default desc)"
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated includes (category,creator,assignees,contacts,companies,properties)"
      }
    },
    {
      "name": "event_category_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "start_from",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "start_to",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "end_from",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "end_to",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "all_day",
      "in": "query",
      "required": false,
      "schema": {
        "type": "boolean"
      }
    },
    {
      "name": "is_cancelled",
      "in": "query",
      "required": false,
      "schema": {
        "type": "boolean"
      }
    },
    {
      "name": "mail_account_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "provider",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "updated_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "created_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "assignee_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated user IDs"
      }
    },
    {
      "name": "contact_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated contact IDs"
      }
    },
    {
      "name": "company_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated company IDs"
      }
    },
    {
      "name": "property_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated property IDs"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Calendar event list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/CalendarEventSummary"
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "limit": {
                    "type": "integer"
                  },
                  "has_more": {
                    "type": "boolean"
                  },
                  "next_cursor": {
                    "type": "string",
                    "nullable": true
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Invalid cursor or filters"
    }
  }
}
```

## POST /calendar_events

Create calendar event

Requires `calendar_events.add`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "calendar_event": {
              "$ref": "#/components/schemas/CalendarEventInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Calendar event created",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/CalendarEvent"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /activities

List activities

Requires `activities.list`. Returns activity entries using cursor pagination.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "limit",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 200
      }
    },
    {
      "name": "cursor",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated includes (actor,item). Item includes are summary-only."
      }
    },
    {
      "name": "activity_kind",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "note",
          "task",
          "event",
          "email",
          "phone_call",
          "legal_proof",
          "document",
          "datenraum",
          "price_change"
        ]
      }
    },
    {
      "name": "item_type",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "item_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "actor_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "performed_from",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "performed_to",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "created_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "updated_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "contact_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated contact IDs"
      }
    },
    {
      "name": "company_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated company IDs"
      }
    },
    {
      "name": "property_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated property IDs"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Activity list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/ActivitySummary"
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "limit": {
                    "type": "integer"
                  },
                  "has_more": {
                    "type": "boolean"
                  },
                  "next_cursor": {
                    "type": "string",
                    "nullable": true
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Invalid cursor or filters"
    }
  }
}
```

## GET /activities/{id}

Fetch activity

Requires `activities.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated includes (actor,item). Item includes are summary-only."
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Activity details",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Activity"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /phone_calls

List phone calls

Requires `phone_calls.list`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "limit",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 200
      }
    },
    {
      "name": "cursor",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Comma-separated includes (integration,matched_contact,matched_company,matched_property,assigned_user,assignee_teams)"
    },
    {
      "name": "phone_integration_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "matched_contact_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "matched_company_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "matched_property_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "assigned_user_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "assigned_team_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "team_queue",
      "in": "query",
      "required": false,
      "description": "When true, returns missed incoming calls that have a team assignment.",
      "schema": {
        "type": "boolean"
      }
    },
    {
      "name": "direction",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "in",
          "out"
        ]
      }
    },
    {
      "name": "state",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "ringing",
          "active",
          "ended"
        ]
      }
    },
    {
      "name": "created_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "updated_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "started_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "ended_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Phone call list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/PhoneCallSummary"
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "limit": {
                    "type": "integer"
                  },
                  "has_more": {
                    "type": "boolean"
                  },
                  "next_cursor": {
                    "type": "string",
                    "nullable": true
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Invalid cursor or filters"
    }
  }
}
```

## POST /phone_calls

Create phone call

Requires `phone_calls.add`. Creates a real phone-call resource. Do not store phone calls as notes. When both `assigned_user_id` and `assignee_ids` are omitted, `metadata.agent_email` automatically assigns exactly one active user in the API key's shop with that email (case-insensitive, surrounding whitespace ignored). Unknown, ambiguous, deleted or deactivated users leave the call unassigned. Explicit assignments, including null or an empty assignee list, take precedence. This resolution happens only on creation; updating metadata does not reassign existing calls. Requires `phone_calls.add`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "phone_call": {
              "$ref": "#/components/schemas/PhoneCallInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Phone call created",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/PhoneCall"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /phone_calls/{id}

Fetch phone call

Requires `phone_calls.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Comma-separated includes (integration,matched_contact,matched_company,matched_property,assigned_user,assignee_teams)"
    }
  ],
  "responses": {
    "200": {
      "description": "Phone call",
      "headers": {
        "ETag": {
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/PhoneCall"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /phone_calls/{id}

Update phone call

Requires `phone_calls.edit`. Partial update. Omitted association fields remain unchanged; explicit null clears optional associations.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Optional ETag for optimistic concurrency"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "phone_call": {
              "$ref": "#/components/schemas/PhoneCallInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Phone call updated",
      "headers": {
        "ETag": {
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/PhoneCall"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /phone_calls/{id}

Update phone call

Requires `phone_calls.edit`. Partial update. Omitted association fields remain unchanged; explicit null clears optional associations.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Optional ETag for optimistic concurrency"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "phone_call": {
              "$ref": "#/components/schemas/PhoneCallInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Phone call updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## DELETE /phone_calls/{id}

Delete phone call

Requires `phone_calls.delete`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /phone_calls/{id}/associations

Fetch phone call associations

Requires `phone_calls.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Associations payload",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/PhoneCallAssociations"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /phone_calls/{id}/associations

Update phone call associations

Requires `phone_calls.edit`. Replace only submitted association keys. Omitted keys remain unchanged; explicit null clears optional associations.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Optional ETag for optimistic concurrency"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "associations": {
              "$ref": "#/components/schemas/PhoneCallAssociationsInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Associations updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /phone_calls/{id}/associations

Update phone call associations

Requires `phone_calls.edit`. Replace only submitted association keys. Omitted keys remain unchanged; explicit null clears optional associations.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Optional ETag for optimistic concurrency"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "associations": {
              "$ref": "#/components/schemas/PhoneCallAssociationsInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Associations updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /emails

List emails

Requires `emails.list`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "limit",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 200
      }
    },
    {
      "name": "cursor",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated includes (body,attachments,tags,source,contacts,companies,properties)"
      }
    },
    {
      "name": "direction",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "incoming",
          "outgoing"
        ]
      }
    },
    {
      "name": "origin",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "crm",
          "external"
        ]
      }
    },
    {
      "name": "owner_user_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "mail_account_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "source_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "tag_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated tag IDs"
      }
    },
    {
      "name": "contact_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated contact IDs"
      }
    },
    {
      "name": "company_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated company IDs"
      }
    },
    {
      "name": "property_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated property IDs"
      }
    },
    {
      "name": "created_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "updated_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "sent_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "received_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Email list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/EmailSummary"
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "limit": {
                    "type": "integer"
                  },
                  "has_more": {
                    "type": "boolean"
                  },
                  "next_cursor": {
                    "type": "string",
                    "nullable": true
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Invalid cursor or filters"
    }
  }
}
```

## POST /emails

Create email

Requires `emails.add`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "email": {
              "$ref": "#/components/schemas/EmailInput"
            }
          }
        }
      },
      "multipart/form-data": {
        "schema": {
          "type": "object",
          "properties": {
            "email_json": {
              "type": "string",
              "description": "JSON string payload matching EmailInput"
            },
            "attachments": {
              "type": "array",
              "items": {
                "type": "string",
                "format": "binary"
              }
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Email created",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Email"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /emails/{id}

Fetch email

Requires `emails.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated includes (body,attachments,tags,source,contacts,companies,properties)"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Email",
      "headers": {
        "ETag": {
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Email"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /emails/{id}

Update email metadata

Requires `emails.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "email": {
              "type": "object",
              "properties": {
                "tag_ids": {
                  "type": "array",
                  "items": {
                    "type": "integer"
                  }
                },
                "source_id": {
                  "type": "integer",
                  "nullable": true
                },
                "contact_ids": {
                  "type": "array",
                  "items": {
                    "type": "integer"
                  }
                },
                "company_ids": {
                  "type": "array",
                  "items": {
                    "type": "integer"
                  }
                },
                "property_ids": {
                  "type": "array",
                  "items": {
                    "type": "integer"
                  }
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
      "description": "Email updated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Email"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /emails/{id}

Update email metadata

Requires `emails.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "email": {
              "type": "object"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Email updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    }
  }
}
```

## GET /emails/{email_id}/attachments

List email attachments

Requires `emails.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "email_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      },
      "description": "Email ID"
    }
  ],
  "responses": {
    "200": {
      "description": "Attachment list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "type": "object"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /emails/{email_id}/attachments/{id}/download

Download email attachment

Requires `emails.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "email_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      },
      "description": "ActiveStorage attachment id"
    }
  ],
  "responses": {
    "302": {
      "description": "Redirect to file URL"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /legal_proofs

List legal proofs

Requires `legal_proofs.list`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "limit",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 200
      }
    },
    {
      "name": "cursor",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated includes (actor,contact,company,property,emails)"
      }
    },
    {
      "name": "contact_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "company_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "property_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "actor_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "recipient_email",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "created_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "consents_captured_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "confirmation_submitted_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "email_sent_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Legal proof list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/LegalProofSummary"
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "limit": {
                    "type": "integer"
                  },
                  "has_more": {
                    "type": "boolean"
                  },
                  "next_cursor": {
                    "type": "string",
                    "nullable": true
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Invalid cursor or filters"
    }
  }
}
```

## GET /legal_proofs/{id}

Fetch legal proof

Requires `legal_proofs.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated includes (actor,contact,company,property,emails)"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Legal proof",
      "headers": {
        "ETag": {
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/LegalProof"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /datenraums

List datenraums

Requires `datenraums.list`. Rooms opened only as a template preview are not listed.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "limit",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 200
      }
    },
    {
      "name": "cursor",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated includes (recipients)"
      }
    },
    {
      "name": "status",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "active",
          "expired",
          "locked"
        ]
      }
    },
    {
      "name": "property_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "company_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "template_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "contact_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "recipient_email",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "created_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "updated_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Datenraum list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/DatenraumSummary"
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "limit": {
                    "type": "integer"
                  },
                  "has_more": {
                    "type": "boolean"
                  },
                  "next_cursor": {
                    "type": "string",
                    "nullable": true
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Invalid cursor or filters"
    }
  }
}
```

## GET /datenraums/{id}

Fetch datenraum

Requires `datenraums.read`. Rooms opened only as a template preview return 404.
For a key with a user, the room follows the same access as in the app: a room whose linked
property the user may not open returns 404, so neither its blocks nor its recipients are returned.
With `fields=full` (default) the response contains the recipients' answers (`answers`) and the
submission status (`submission_status`, `submitted_at`); the list endpoint does not return them. Answers follow the same rights as in the
app: for a key with a user, that user needs the permission to view data rooms, otherwise `answers` is `null`. Form answers that write CRM fields omit fields the
key's user may not read (field rules of the shop form, e.g. restricted GwG fields); a key without a
user only receives fields without a read restriction.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated includes (recipients)"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Datenraum",
      "headers": {
        "ETag": {
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Datenraum"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /document_activities

List document activities

Requires `document_activities.list`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "limit",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 200
      }
    },
    {
      "name": "cursor",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated includes (actor,contact,company,property,template,file)"
      }
    },
    {
      "name": "contact_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "company_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "property_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "actor_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "template_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "context_type",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "created_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    },
    {
      "name": "updated_since",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "format": "date-time"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Document activity list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/DocumentActivitySummary"
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "limit": {
                    "type": "integer"
                  },
                  "has_more": {
                    "type": "boolean"
                  },
                  "next_cursor": {
                    "type": "string",
                    "nullable": true
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Invalid cursor or filters"
    }
  }
}
```

## GET /document_activities/{id}

Fetch document activity

Requires `document_activities.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated includes (actor,contact,company,property,template,file)"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Document activity",
      "headers": {
        "ETag": {
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/DocumentActivity"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /calendar_events/{id}

Fetch calendar event

Requires `calendar_events.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full"
        ]
      }
    },
    {
      "name": "include",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Calendar event",
      "headers": {
        "ETag": {
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/CalendarEvent"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /calendar_events/{id}

Update calendar event

Requires `calendar_events.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Optional ETag for optimistic concurrency"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "calendar_event": {
              "$ref": "#/components/schemas/CalendarEventInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Calendar event updated",
      "headers": {
        "ETag": {
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/CalendarEvent"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /calendar_events/{id}

Update calendar event

Requires `calendar_events.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Optional ETag for optimistic concurrency"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "calendar_event": {
              "$ref": "#/components/schemas/CalendarEventInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Calendar event updated",
      "headers": {
        "ETag": {
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/CalendarEvent"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## DELETE /calendar_events/{id}

Delete calendar event

Requires `calendar_events.delete`. Events referenced by bookings cannot be deleted through this endpoint. The event and bookings remain unchanged.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "409": {
      "description": "Calendar event is referenced by a booking",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "error": {
                "type": "string",
                "enum": [
                  "resource_in_use"
                ]
              }
            }
          }
        }
      }
    }
  }
}
```

## GET /calendar_events/{id}/associations

Fetch calendar event associations

Requires `calendar_events.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Associations payload",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/CalendarEventAssociations"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /calendar_events/{id}/associations

Update calendar event associations

Requires `calendar_events.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Optional ETag for optimistic concurrency"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "calendar_event": {
              "$ref": "#/components/schemas/CalendarEventAssociationsInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Associations updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /calendar_events/{id}/associations

Update calendar event associations

Requires `calendar_events.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Optional ETag for optimistic concurrency"
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "calendar_event": {
              "$ref": "#/components/schemas/CalendarEventAssociationsInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Associations updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "412": {
      "description": "ETag mismatch"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /event_categories

List event categories

Requires one of `event_categories.list` or `calendar_events.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "active",
      "in": "query",
      "required": false,
      "description": "Filter by active or archived categories. Omit to list both.",
      "schema": {
        "type": "boolean"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Category list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/EventCategory"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    }
  }
}
```

## POST /event_categories

Create event category

Requires `event_categories.add`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "event_category": {
              "$ref": "#/components/schemas/EventCategoryInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Category created",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/EventCategory"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PATCH /event_categories/{id}

Update event category

Requires `event_categories.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "event_category": {
              "$ref": "#/components/schemas/EventCategoryInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Category updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /event_categories/{id}

Update event category

Requires `event_categories.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "event_category": {
              "$ref": "#/components/schemas/EventCategoryInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Category updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## DELETE /event_categories/{id}

Delete event category

Requires `event_categories.delete`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /template_capabilities

Discover template input capabilities

Requires at least one of `text_snippets.add`, `landingpage_templates.add`, or `letter_templates.add`.
Returns the accepted enum values for all three template POST contracts from the same application constants
used by request validation. The `schema_version` changes only for breaking response-shape changes.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Machine-readable template input capabilities",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/TemplateCapabilitiesResponse"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing every supported template add scope"
    }
  }
}
```

## GET /letter_templates

List letter templates

Requires `letter_templates.list`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Shop-scoped letter templates",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "required": [
              "data"
            ],
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/LetterTemplate"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing letter_templates.list scope"
    }
  }
}
```

## POST /letter_templates

Create a letter template

Requires `letter_templates.add`. The uploaded file must be a structurally valid DOCX. Validation errors use
the public request fields and English messages; missing `name` and `file` are reported together. Invalid enum
values return their accepted values under `allowed_values`. Unsafe or unsupported merge commands return
`invalid_merge_template` with the exact expression and its location in the DOCX. Discover current enum values
with `/template_capabilities`.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "multipart/form-data": {
        "schema": {
          "type": "object",
          "required": [
            "name",
            "file"
          ],
          "properties": {
            "name": {
              "type": "string"
            },
            "file": {
              "type": "string",
              "format": "binary"
            },
            "category": {
              "type": "string",
              "enum": [
                "property_expose",
                "letter",
                "contract",
                "report",
                "other"
              ]
            },
            "model": {
              "type": "string",
              "enum": [
                "property",
                "contact",
                "company"
              ],
              "description": "Persisted generation context; defaults category to property_expose for property and letter otherwise."
            },
            "description": {
              "type": "string"
            },
            "active": {
              "type": "boolean"
            },
            "position": {
              "type": "integer",
              "minimum": 0
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Created template",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/LetterTemplateResponse"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing letter_templates.add scope"
    },
    "422": {
      "description": "Public-field validation errors, accepted enum values, an invalid DOCX, or named merge-template findings",
      "content": {
        "application/json": {
          "schema": {
            "oneOf": [
              {
                "$ref": "#/components/schemas/InvalidMergeTemplateResponse"
              },
              {
                "type": "object"
              }
            ]
          }
        }
      }
    }
  }
}
```

## GET /text_snippets

List shop-wide text snippets

Requires `text_snippets.list`. Personal snippets are never exposed. List items omit the body; use the detail endpoint to retrieve complete content.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "model",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "email",
          "task",
          "note",
          "appointment"
        ]
      }
    },
    {
      "name": "category_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Shop-wide text snippets",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "required": [
              "data"
            ],
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/TextSnippet"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing text_snippets.list scope"
    },
    "422": {
      "description": "Invalid model filter"
    }
  }
}
```

## POST /text_snippets

Create a shop-wide text snippet

Requires `text_snippets.add`. Subject and body fields are validated against the `text_snippet` merge contract
before persistence. Validation errors use the public request fields and English messages; missing `name` and
`body_html` are reported together. Invalid `model` values return `allowed_values`; current values are also
available from `/template_capabilities`.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "allOf": [
            {
              "$ref": "#/components/schemas/TextSnippetInput"
            },
            {
              "type": "object",
              "required": [
                "name",
                "body_html"
              ]
            }
          ]
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Created text snippet",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/TextSnippetResponse"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing text_snippets.add scope"
    },
    "422": {
      "description": "Public-field validation errors, invalid model values with accepted values, cross-shop association, or named merge-template findings (`invalid_merge_template` with a `template_too_large` finding naming the affected field when a non-blank `subject`, `body_html`, or `body_text` exceeds 65536 bytes)"
    }
  }
}
```

## GET /text_snippets/{id}

Read a complete shop-wide text snippet

Requires `text_snippets.read`. Returns the complete HTML and plain-text bodies.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Complete text snippet",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/TextSnippetResponse"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing text_snippets.read scope"
    },
    "404": {
      "description": "Text snippet not found in this shop or is personal"
    }
  }
}
```

## PATCH /text_snippets/{id}

Update a shop-wide text snippet

Requires `text_snippets.edit`. The update is partial and preserves the ID. Explicit null clears description, subject, body_text, or category_id; omitted fields remain unchanged.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/TextSnippetInput"
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Updated text snippet",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/TextSnippetResponse"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing text_snippets.edit scope"
    },
    "404": {
      "description": "Text snippet not found in this shop or is personal"
    },
    "422": {
      "description": "Invalid model or metadata, cross-shop association, or named merge-template findings (`invalid_merge_template` with a `template_too_large` finding naming the affected field when a non-blank `subject`, `body_html`, or `body_text` exceeds 65536 bytes)"
    }
  }
}
```

## DELETE /text_snippets/{id}

Delete a shop-wide text snippet

Requires `text_snippets.delete`. Deletion is blocked while an automation or booking page references the snippet.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing text_snippets.delete scope"
    },
    "404": {
      "description": "Text snippet not found in this shop or is personal"
    },
    "409": {
      "description": "Text snippet is referenced",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/TextSnippetUsageConflict"
          }
        }
      }
    }
  }
}
```

## GET /navigation_links

List shared navigation links

Requires `navigation_links.list`. Returns the links shared with all users (`visibility: all`) or with selected
teams (`visibility: teams`), including hidden ones, ordered by position. Personal links of individual users are
never exposed.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Shared navigation links",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "required": [
              "data"
            ],
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/NavigationLink"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing navigation_links.list scope"
    }
  }
}
```

## POST /navigation_links

Create a shared navigation link

Requires `navigation_links.add`. `url` must be an `https://` URL (opens in a new tab) or an address of this propgen
instance, e.g. `/contacts?sort=name` (stored as a path, opens in the same tab). `javascript:`, `data:` and
`http:` URLs are rejected. `visibility` defaults to `all`; `teams` requires at least one `team_ids` entry.
A shop can have at most 10 shared links.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "allOf": [
            {
              "$ref": "#/components/schemas/NavigationLinkInput"
            },
            {
              "type": "object",
              "required": [
                "name",
                "url"
              ]
            }
          ]
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Created navigation link",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/NavigationLinkResponse"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing navigation_links.add scope"
    },
    "422": {
      "description": "Validation errors (missing name or url",
      "unsafe url": null,
      "missing or foreign teams": null,
      "limit reached": null,
      "invalid visibility)": null
    }
  }
}
```

## PATCH /navigation_links/reorder

Reorder shared navigation links

Requires `navigation_links.edit`. `ids` lists links of the given visibility group, each at most once, in the
new order. The listed links swap among the positions they already hold; omitted links keep their positions.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "visibility",
            "ids"
          ],
          "properties": {
            "visibility": {
              "type": "string",
              "enum": [
                "all",
                "teams"
              ]
            },
            "ids": {
              "type": "array",
              "items": {
                "type": "integer"
              }
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Links of the group in their new order",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "required": [
              "data"
            ],
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/NavigationLink"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing navigation_links.edit scope"
    },
    "422": {
      "description": "Invalid visibility",
      "duplicate ids": null,
      "or ids outside the group": null
    }
  }
}
```

## GET /navigation_links/{id}

Read a shared navigation link

Requires `navigation_links.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Navigation link",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/NavigationLinkResponse"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing navigation_links.read scope"
    },
    "404": {
      "description": "Link not found in this shop or is personal"
    }
  }
}
```

## PATCH /navigation_links/{id}

Update a shared navigation link

Requires `navigation_links.edit`. The update is partial; omitted fields remain unchanged. Changing `visibility`
moves the link to the end of its new group. `hidden: true` hides the link for all recipients.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/NavigationLinkInput"
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Updated navigation link",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/NavigationLinkResponse"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing navigation_links.edit scope"
    },
    "404": {
      "description": "Link not found in this shop or is personal"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /navigation_links/{id}

Update a shared navigation link (PUT)

Requires `navigation_links.edit`. Same as PATCH.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/NavigationLinkInput"
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Updated navigation link",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/NavigationLinkResponse"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing navigation_links.edit scope"
    },
    "404": {
      "description": "Link not found in this shop or is personal"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## DELETE /navigation_links/{id}

Delete a shared navigation link

Requires `navigation_links.delete`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing navigation_links.delete scope"
    },
    "404": {
      "description": "Link not found in this shop or is personal"
    }
  }
}
```

## GET /landingpage_templates

List landing page templates

Requires `landingpage_templates.list`. List items omit executable HTML. Optional record_type filtering includes universal templates.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "record_type",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "property",
          "project"
        ]
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Shop-scoped landing page templates",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "required": [
              "data"
            ],
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/LandingpageTemplate"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing landingpage_templates.list scope"
    },
    "422": {
      "description": "Invalid record_type"
    }
  }
}
```

## POST /landingpage_templates

Create a landing page template

Requires `landingpage_templates.add`. The complete HTML/Liquid body is validated against the public-output
`landingpage` merge contract and is limited to 524288 bytes. Unclassified and internal-only fields are rejected
with `field_not_available_on_surface`; custom fields are public by default and can be kept internal with `public_merge: false`. The body may contain executable scripts,
iframes, and external resources and is published without HTML sanitization; grant this scope only to trusted integrations.
Validation errors use the public request fields and English messages; missing `name` and `body` are reported
together. Invalid `template_kind` values return `allowed_values`; discover current values with `/template_capabilities`.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "allOf": [
            {
              "$ref": "#/components/schemas/LandingpageTemplateInput"
            },
            {
              "type": "object",
              "required": [
                "name",
                "body"
              ]
            }
          ]
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Created template",
      "headers": {
        "ETag": {
          "description": "Template version for conditional updates",
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/LandingpageTemplateResponse"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing landingpage_templates.add scope"
    },
    "422": {
      "description": "Public-field validation errors with accepted enum values",
      "Liquid syntax": null,
      "public merge field": null,
      "or body size": null
    }
  }
}
```

## GET /landingpage_templates/{id}

Read a complete landing page template

Requires `landingpage_templates.read`. The response contains executable HTML and Liquid.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Complete shop-scoped template",
      "headers": {
        "ETag": {
          "description": "Template version for conditional updates",
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/LandingpageTemplateResponse"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing landingpage_templates.read scope"
    },
    "404": {
      "description": "Template not found in the API key's shop"
    }
  }
}
```

## PATCH /landingpage_templates/{id}

Update a landing page template

Requires `landingpage_templates.edit`. The update is partial and preserves the ID. The resulting complete body
is validated against the public landingpage merge contract on every update, including metadata-only changes.
Existing published links render the changed body on their next request. System templates allow default-flag
changes only. A template kind cannot be changed when that would make an existing property reference incompatible.
The body is limited to 524288 bytes and may contain unsanitized scripts, iframes, and external resources; grant
this scope only to trusted integrations.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "ETag from a prior create, detail, or update response."
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/LandingpageTemplateInput"
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Updated template",
      "headers": {
        "ETag": {
          "description": "New template version",
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/LandingpageTemplateResponse"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing scope or attempted content change to a system template"
    },
    "404": {
      "description": "Template not found in the API key's shop"
    },
    "412": {
      "description": "If-Match does not match the current template version"
    },
    "422": {
      "description": "Invalid metadata",
      "incompatible referenced properties": null,
      "Liquid syntax": null,
      "public merge field": null,
      "or body size": null
    }
  }
}
```

## DELETE /landingpage_templates/{id}

Delete an unused landing page template

Requires `landingpage_templates.delete`. System templates and templates referenced by properties or published links cannot be deleted.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "If-Match",
      "in": "header",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Optional ETag from a prior detail response."
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing scope or system template"
    },
    "404": {
      "description": "Template not found in the API key's shop"
    },
    "409": {
      "description": "Template is referenced by properties or published links",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/LandingpageTemplateUsageConflict"
          }
        }
      }
    },
    "412": {
      "description": "If-Match does not match the current template version"
    }
  }
}
```

## GET /merge/surfaces

List merge surfaces

Requires `merge_fields.read`. Returns the stable template surfaces supported by the merge contract.
Use each surface key with `/merge/variables` and `/merge/capabilities`. `landingpage` is a public-output
surface and therefore exposes only fields explicitly released for public rendering; the other surfaces
describe authenticated internal output. The response has a private registry-revision ETag.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "If-None-Match",
      "in": "header",
      "required": false,
      "description": "Private ETag from an earlier response for this URL.",
      "schema": {
        "type": "string"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Supported merge surfaces",
      "headers": {
        "ETag": {
          "description": "Private validator derived from registry_revision",
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/MergeSurfacesResponse"
          }
        }
      }
    },
    "304": {
      "description": "Registry revision is unchanged; response body is empty"
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing merge_fields.read scope or source IP not allowed"
    },
    "429": {
      "description": "API-key rate limit exceeded"
    }
  }
}
```

## GET /merge/variables

Discover surface-specific merge variables

Requires `merge_fields.read`. Returns the complete shop-specific `merge-contract.v3` projection for the
required surface, including custom form fields, collection contracts, association fields and numbered
association aliases. Internal surfaces intentionally include entries with `public_merge: false`.
The `landingpage` surface excludes those entries server-side and never relies on client-side filtering.
Property landingpage rich-text fields and their sanitized `_html` variants are included on this surface.
Built-in schema fields default to internal-only and must be present in the curated public inventory.
Shop-defined custom fields default to public because they are curated form and exposé data; a shop can
keep an individual custom field internal with `public_merge: false`. Repeater custom fields expose only
the row keys declared in `input_props.columns[].field` as iterable collection item fields.

On the `landingpage` surface, select fields render their visible option label. Shop-defined custom
multiselect fields have `rendered_type: array`; every item is a visible option label. Use Liquid `join`
for display text and `json_string` when embedding the array as JSON. The `runtime` object documents
these semantics and examples. Internal DOCX multiselect output remains a comma-separated label string.

Personalized landingpage links expose the assigned contact supervisor through `kontakt.betreuer.*`,
using the same public fields as the `user` scope. The `kontakt` scope is absent for anonymous links;
contacts without a supervisor have no populated `kontakt.betreuer` value. Templates can therefore
use `{% if kontakt.betreuer.full_name %}` and fall back to `collection.alle_betreuer` without changing
the behavior of other shop-specific templates.

Collection aliases are emitted as full collection entries and every collection entry has a corresponding
`<path>.length` variable. `firma` is the Propstack-compatible internal alias of the `konto` scope.
Landingpage runtime collections document their registered public template structure. `pois` uses `key_value`
iteration because Liquid exposes each category as a two-element pair; the contract includes the supported
`[0]` key and `[1]` value assignments plus the nested `places` fields. Project landingpages expose the
public child-unit collection as `project_page.units.items`; `project_page.display.units.items` is the alias
used after assigning `project_page.display` to a local variable. Its item contract includes the public fields
for both units and, when `project_page.record_type` is `areal`, buildings. Fields that only apply to one record
type are absent at runtime for the other. Lease and other internal CRM data remain excluded.

`ausloeser_kontakt`, `ausloeser_unternehmen` and `ausloeser_einheit` are internal scopes of automation
emails (`email` surface only: other surfaces neither list them in `scopes` nor accept them as `scope`,
which returns `invalid_scope`). They carry every field of `kontakt`, `unternehmen` and `einheit`, always
`public_merge: false`, and render the contact, company and property of the run's original trigger
(requirements `automation_trigger_contact`, `automation_trigger_company`, `automation_trigger_property`).
Inside an automation loop with a `property_contacts` source, `kontakt` is the loop's recipient and these
scopes keep the trigger's records.

Syntax is already projected for the selected dialect. Liquid and DOCX scalar outputs both return
`{{ path }}`. The private ETag includes surface, scope and registry revision.
On `internal_docx`, tagged property media are also exposed as numbered object paths
`einheit.mikrolage1` through `einheit.mikrolage10`, `einheit.makrolage1` through
`einheit.makrolage10`, and `einheit.areal_luftbild1` through `einheit.areal_luftbild10`.
Each object uses the same media fields as `einheit.grundriss1`; missing positions are empty/falsy.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "surface",
      "in": "query",
      "required": true,
      "description": "Rendering context and template dialect.",
      "schema": {
        "type": "string",
        "enum": [
          "email",
          "text_snippet",
          "landingpage",
          "internal_docx"
        ]
      }
    },
    {
      "name": "scope",
      "in": "query",
      "required": false,
      "description": "Exact merge scope. Omit to return all scopes.",
      "schema": {
        "type": "string",
        "enum": [
          "global",
          "kontakt",
          "unternehmen",
          "einheit",
          "mietvertrag",
          "termin",
          "aufgabe",
          "notiz",
          "deal",
          "projekt",
          "booking",
          "user",
          "unterzeichner",
          "absender",
          "aktueller_nutzer",
          "konto",
          "firma",
          "datenraum",
          "ausloeser_kontakt",
          "ausloeser_unternehmen",
          "ausloeser_einheit"
        ]
      }
    },
    {
      "name": "If-None-Match",
      "in": "header",
      "required": false,
      "description": "Private ETag from an earlier response for this URL.",
      "schema": {
        "type": "string"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Shop- and surface-specific variable contract",
      "headers": {
        "ETag": {
          "description": "Private validator derived from registry_revision and the selected scope",
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/MergeVariablesResponse"
          },
          "example": {
            "schema_version": "merge-contract.v3",
            "registry_revision": "sha256:1b4d6d7a496160e92e35b884c6b59c32c196fa043f77df011d8a39b649421e33",
            "surface": "internal_docx",
            "scope": "einheit",
            "scopes": [
              {
                "key": "einheit",
                "label": "Einheit",
                "model": "Property"
              }
            ],
            "variables": [
              {
                "path": "einheit.custom_hallenflache",
                "scope": "einheit",
                "context_scopes": [
                  "einheit"
                ],
                "label": "Hallenfläche",
                "kind": "field",
                "type": "decimal",
                "rendered_type": "formatted_string",
                "format": "number",
                "syntax": "{{ einheit.custom_hallenflache }}",
                "aliases": [],
                "public_merge": false,
                "internal_only": true,
                "requirements": [
                  "property"
                ],
                "availability": {
                  "status": "conditional",
                  "when": [
                    "property"
                  ]
                }
              }
            ]
          }
        }
      }
    },
    "304": {
      "description": "Registry revision is unchanged; response body is empty"
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing merge_fields.read scope or source IP not allowed"
    },
    "422": {
      "description": "Missing/invalid surface or invalid scope",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/MergeInvalidParameterError"
          },
          "example": {
            "error": "invalid_scope",
            "parameter": "scope",
            "value": "beispiel_scope",
            "allowed_values": [
              "global",
              "kontakt",
              "unternehmen",
              "einheit",
              "mietvertrag",
              "termin",
              "aufgabe",
              "notiz",
              "deal",
              "projekt",
              "booking",
              "user",
              "unterzeichner",
              "absender",
              "aktueller_nutzer",
              "konto",
              "firma",
              "datenraum",
              "ausloeser_kontakt",
              "ausloeser_unternehmen",
              "ausloeser_einheit"
            ]
          }
        }
      }
    },
    "429": {
      "description": "API-key rate limit exceeded"
    }
  }
}
```

## GET /merge/capabilities

Discover the surface-specific template dialect

Requires `merge_fields.read`. Returns the command, expression, loop, end-tag, helper and filter contracts
consumed by the production validator for the required surface. Liquid surfaces describe output/tags,
`contains`, registered collections, standard Liquid filters and propgen filters. DOCX describes commands,
helper arities and typed collection `.length`. The response has a private surface- and revision-aware ETag.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "surface",
      "in": "query",
      "required": true,
      "description": "Rendering context and template dialect.",
      "schema": {
        "type": "string",
        "enum": [
          "email",
          "text_snippet",
          "landingpage",
          "internal_docx"
        ]
      }
    },
    {
      "name": "If-None-Match",
      "in": "header",
      "required": false,
      "description": "Private ETag from an earlier response for this URL.",
      "schema": {
        "type": "string"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Validator-backed surface dialect contract",
      "headers": {
        "ETag": {
          "description": "Private validator derived from registry_revision",
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/MergeCapabilitiesResponse"
          },
          "example": {
            "schema_version": "merge-contract.v3",
            "registry_revision": "sha256:5e9ad0bd4e8947e448337be73c517cae4d88079f802e9e787a3138a376abf291",
            "surface": "internal_docx",
            "dialect": "docx_templates",
            "delimiters": {
              "open": "{{",
              "close": "}}"
            },
            "implicit_ins": "canonical",
            "commands": [
              {
                "name": "INS",
                "supported": true,
                "deprecated": true,
                "expression": "registered_scalar_path_googlemaps_or_string_literal",
                "examples": []
              }
            ],
            "expressions": {
              "types": [
                "registered_path",
                "loop_local",
                "collection_length",
                "comparison",
                "logical",
                "string_includes"
              ],
              "operators": [
                {
                  "token": "===",
                  "arity": 2
                },
                {
                  "token": ".includes",
                  "arity": 2,
                  "receiver_types": [
                    "string",
                    "string_array"
                  ],
                  "argument_type": "string"
                }
              ],
              "examples": [
                "{{ IF collection.kontakte.length > 0 }}{{ END-IF }}"
              ],
              "unsupported": [
                {
                  "syntax": "[]",
                  "reason": "Bracket lookup is outside the typed merge contract."
                }
              ]
            },
            "loops": {
              "source": "registered_collection_or_registered_alias",
              "open": "{{ FOR <local> IN <collection.path> }}",
              "local": "$<local>.<registered-item-field>",
              "local_must_match_collection": true,
              "index": "$idx",
              "index_base": 0,
              "close": "{{ END-FOR <local> }}",
              "close_requires_matching_local": true,
              "nested": true,
              "examples": [
                "{{ FOR kontakt IN collection.kontakte }}{{ $kontakt.first_name }}{{ END-FOR kontakt }}"
              ]
            },
            "end_tags": {
              "IF": {
                "tag": "END-IF",
                "syntax": "{{ END-IF }}"
              },
              "FOR": {
                "tag": "END-FOR",
                "syntax": "{{ END-FOR <matching-local> }}"
              }
            },
            "helpers": [
              {
                "name": "qrcode",
                "canonical_name": "qrcode",
                "commands": [
                  "IMAGE"
                ],
                "arguments": [
                  {
                    "name": "value",
                    "type": "registered_string_path_or_googlemaps",
                    "required": true
                  },
                  {
                    "name": "size_cm",
                    "type": "positive_number",
                    "required": false,
                    "default": 3
                  }
                ],
                "requirements": [
                  "word_image_placeholder"
                ],
                "examples": [
                  "{{ IMAGE qrcode(kontakt.email, 3) }}"
                ]
              }
            ],
            "filters": [],
            "runtime_behavior": {
              "undefined_variables": "empty",
              "automatic_html_escape": false
            }
          }
        }
      }
    },
    "304": {
      "description": "Registry revision is unchanged; response body is empty"
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing merge_fields.read scope or source IP not allowed"
    },
    "422": {
      "description": "Missing or invalid surface"
    },
    "429": {
      "description": "API-key rate limit exceeded"
    }
  }
}
```

## PATCH /letter_templates/{id}

Update a letter template

Requires `letter_templates.edit`. Omitted metadata and file remain unchanged; replacing the file preserves the template ID. Unsafe or unsupported merge commands return `invalid_merge_template` with the exact expression and its DOCX location.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "multipart/form-data": {
        "schema": {
          "type": "object",
          "properties": {
            "name": {
              "type": "string"
            },
            "file": {
              "type": "string",
              "format": "binary"
            },
            "category": {
              "type": "string",
              "enum": [
                "property_expose",
                "letter",
                "contract",
                "report",
                "other"
              ]
            },
            "model": {
              "type": "string",
              "enum": [
                "property",
                "contact",
                "company"
              ]
            },
            "description": {
              "type": "string"
            },
            "active": {
              "type": "boolean"
            },
            "position": {
              "type": "integer",
              "minimum": 0
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Updated template",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/LetterTemplateResponse"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing letter_templates.edit scope"
    },
    "404": {
      "description": "Template not found in this shop"
    },
    "422": {
      "description": "Non-DOCX, corrupt DOCX, invalid metadata, or named merge-template findings",
      "content": {
        "application/json": {
          "schema": {
            "oneOf": [
              {
                "$ref": "#/components/schemas/InvalidMergeTemplateResponse"
              },
              {
                "type": "object"
              }
            ]
          }
        }
      }
    }
  }
}
```

## DELETE /letter_templates/{id}

Delete a letter template

Requires `letter_templates.delete`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing letter_templates.delete scope"
    },
    "404": {
      "description": "Template not found in this shop"
    }
  }
}
```

## GET /letter_templates/{id}/download

Download the original DOCX

Requires `letter_templates.read`. Returns the latest upload byte-for-byte.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Original DOCX",
      "content": {
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {
          "schema": {
            "type": "string",
            "format": "binary"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing letter_templates.read scope"
    },
    "404": {
      "description": "Template not found in this shop"
    }
  }
}
```

## POST /letter_templates/{id}/generate

Generate a document from a letter template

Requires `letter_templates.read`. Generation uses the same property merge context as the CRM UI.
`user_id` selects the sender context. By default the property's primary active responsible user is used;
if unavailable, the first active shop user by ID is used. Without `store_as_document`, the generated file
is returned. With `store_as_document: true`, it is attached to the property and the response contains its ID.
Set `async: true` for background generation, recommended for image-heavy documents. This returns 202
with relative status/download URLs immediately. Missing Large image variants are prepared before rendering.
Poll `status_url` (for example every 2 seconds, respecting rate-limit headers) until `completed` or `failed`.
On completion, fetch `download_url`; with `store_as_document: true`, the status also contains `document_id`.
Use the same API key for all requests. No browser session or Action Cable connection is required.
Omitted `async` or `async: false` preserves synchronous behavior. A new POST starts a new document;
to follow an accepted request, poll its status rather than resubmitting it.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "property_id"
          ],
          "properties": {
            "property_id": {
              "type": "integer"
            },
            "contact_id": {
              "type": "integer"
            },
            "company_id": {
              "type": "integer"
            },
            "company_location_id": {
              "type": "integer"
            },
            "output": {
              "type": "string",
              "enum": [
                "docx"
              ],
              "default": "docx"
            },
            "store_as_document": {
              "type": "boolean",
              "default": false
            },
            "async": {
              "type": "boolean",
              "default": false
            },
            "user_id": {
              "type": "integer"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Generated DOCX",
      "content": {
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {
          "schema": {
            "type": "string",
            "format": "binary"
          }
        }
      }
    },
    "201": {
      "description": "Generated file stored as a property document",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "required": [
              "data"
            ],
            "properties": {
              "data": {
                "type": "object",
                "required": [
                  "document_id",
                  "filename",
                  "content_type"
                ],
                "properties": {
                  "document_id": {
                    "type": "integer"
                  },
                  "filename": {
                    "type": "string"
                  },
                  "content_type": {
                    "type": "string"
                  }
                }
              }
            }
          }
        }
      }
    },
    "202": {
      "description": "Background generation accepted (async true only)",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "required": [
              "data"
            ],
            "properties": {
              "data": {
                "type": "object",
                "required": [
                  "id",
                  "status",
                  "status_url",
                  "download_url"
                ],
                "properties": {
                  "id": {
                    "type": "integer"
                  },
                  "status": {
                    "type": "string",
                    "enum": [
                      "queued",
                      "preparing_images",
                      "rendering",
                      "completed",
                      "failed"
                    ]
                  },
                  "company_location_id": {
                    "type": "integer",
                    "nullable": true
                  },
                  "location_resolution": {
                    "type": "object",
                    "nullable": true,
                    "properties": {
                      "stage": {
                        "type": "integer"
                      },
                      "reason": {
                        "type": "string",
                        "enum": [
                          "explicit",
                          "relationship",
                          "single",
                          "headquarters",
                          "company_address"
                        ]
                      },
                      "address_snapshot": {
                        "type": "object",
                        "nullable": true,
                        "properties": {
                          "name": {
                            "type": "string",
                            "nullable": true
                          },
                          "street": {
                            "type": "string",
                            "nullable": true
                          },
                          "house_number": {
                            "type": "string",
                            "nullable": true
                          },
                          "postal_code": {
                            "type": "string",
                            "nullable": true
                          },
                          "city": {
                            "type": "string",
                            "nullable": true
                          },
                          "address_supplement": {
                            "type": "string",
                            "nullable": true
                          }
                        }
                      }
                    }
                  },
                  "status_url": {
                    "type": "string",
                    "example": "/public_api/v1/document_generations/123"
                  },
                  "download_url": {
                    "type": "string",
                    "example": "/public_api/v1/document_generations/123/download"
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing letter_templates.read scope"
    },
    "404": {
      "description": "Template not found in this shop"
    },
    "422": {
      "description": "Invalid property/user/output, corrupt template, generation error, or unavailable PDF conversion",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "required": [
              "error"
            ],
            "properties": {
              "error": {
                "type": "string"
              },
              "message": {
                "type": "string"
              },
              "template_errors": {
                "type": "array",
                "description": "Actionable DOCX command diagnostics when generation reaches the renderer.",
                "items": {
                  "type": "object",
                  "required": [
                    "command",
                    "reason"
                  ],
                  "properties": {
                    "command": {
                      "type": "string"
                    },
                    "reason": {
                      "type": "string"
                    },
                    "location": {
                      "type": "object",
                      "properties": {
                        "part": {
                          "type": "string"
                        },
                        "paragraph": {
                          "type": "integer"
                        },
                        "offset": {
                          "type": "integer"
                        },
                        "length": {
                          "type": "integer"
                        },
                        "line": {
                          "type": "integer"
                        },
                        "column": {
                          "type": "integer"
                        }
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
    "503": {
      "description": "Background generation could not be enqueued (generation_unavailable)"
    }
  }
}
```

## GET /document_generations/{id}

Read background document generation progress and result

Requires `letter_templates.read` and the same API key that started the generation.
Requests from another key or shop return 404. Authentication, IP restrictions and rate limits apply.
`images_processed` counts checked/prepared images; `images_generated` counts newly created Large variants.
`created_at` to `completed_at` includes queue time. `started_at` to `images_ready_at` covers image preparation.
A failed job remains readable with status `failed`, error `generation_failed`, and available template diagnostics.
`document_id` is non-null only for a stored result that has not subsequently been deleted.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Generation status, including terminal failures",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "required": [
              "data"
            ],
            "properties": {
              "data": {
                "type": "object",
                "properties": {
                  "id": {
                    "type": "integer"
                  },
                  "status": {
                    "type": "string",
                    "enum": [
                      "queued",
                      "preparing_images",
                      "rendering",
                      "completed",
                      "failed"
                    ]
                  },
                  "images_total": {
                    "type": "integer"
                  },
                  "images_processed": {
                    "type": "integer"
                  },
                  "images_generated": {
                    "type": "integer"
                  },
                  "store_as_document": {
                    "type": "boolean"
                  },
                  "document_id": {
                    "type": "integer",
                    "nullable": true
                  },
                  "filename": {
                    "type": "string",
                    "nullable": true
                  },
                  "content_type": {
                    "type": "string",
                    "nullable": true
                  },
                  "company_location_id": {
                    "type": "integer",
                    "nullable": true
                  },
                  "location_resolution": {
                    "type": "object",
                    "nullable": true,
                    "properties": {
                      "stage": {
                        "type": "integer"
                      },
                      "reason": {
                        "type": "string",
                        "enum": [
                          "explicit",
                          "relationship",
                          "single",
                          "headquarters",
                          "company_address"
                        ]
                      },
                      "address_snapshot": {
                        "type": "object",
                        "nullable": true,
                        "properties": {
                          "name": {
                            "type": "string",
                            "nullable": true
                          },
                          "street": {
                            "type": "string",
                            "nullable": true
                          },
                          "house_number": {
                            "type": "string",
                            "nullable": true
                          },
                          "postal_code": {
                            "type": "string",
                            "nullable": true
                          },
                          "city": {
                            "type": "string",
                            "nullable": true
                          },
                          "address_supplement": {
                            "type": "string",
                            "nullable": true
                          }
                        }
                      }
                    }
                  },
                  "error": {
                    "type": "string",
                    "nullable": true,
                    "enum": [
                      "generation_failed",
                      null
                    ]
                  },
                  "created_at": {
                    "type": "string",
                    "format": "date-time"
                  },
                  "updated_at": {
                    "type": "string",
                    "format": "date-time"
                  },
                  "started_at": {
                    "type": "string",
                    "format": "date-time",
                    "nullable": true
                  },
                  "images_ready_at": {
                    "type": "string",
                    "format": "date-time",
                    "nullable": true
                  },
                  "completed_at": {
                    "type": "string",
                    "format": "date-time",
                    "nullable": true
                  },
                  "template_errors": {
                    "type": "array",
                    "items": {
                      "type": "object"
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
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing scope or disallowed IP"
    },
    "404": {
      "description": "Generation not found for this key and shop"
    },
    "429": {
      "description": "Rate limit exceeded; respect Retry-After"
    }
  }
}
```

## GET /document_generations/{id}/download

Download a completed background-generated DOCX

Requires `letter_templates.read` and the same API key that started the generation. Works with either storage mode.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Generated DOCX attachment",
      "content": {
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {
          "schema": {
            "type": "string",
            "format": "binary"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing scope or disallowed IP"
    },
    "404": {
      "description": "Generation not found for this key/shop or result file deleted"
    },
    "409": {
      "description": "Generation is pending or failed (document_not_ready)"
    },
    "429": {
      "description": "Rate limit exceeded; respect Retry-After"
    }
  }
}
```

## PUT /properties/{property_id}/documents/order

Save property document order

Requires `documents.edit`. Saves positions used by the CRM, landingpage and data room.
Supply `ids` with every non-global document of the property exactly once, or use
`sort_by` with `folder_id` to sort all property documents in one folder.
Omit `folder_id` or use null for documents without a folder. Other folders keep their relative
order. Global documents are never changed. Alphabetical sorting uses the display name,
ignoring case and accents; upload date uses `created_at`.
Read saved positions via `GET /documents?entity_type=property&entity_id=42&include_global=false`.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "property_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "ids": {
              "type": "array",
              "items": {
                "type": "integer"
              }
            },
            "sort_by": {
              "type": "string",
              "enum": [
                "name_asc",
                "name_desc",
                "uploaded_asc",
                "uploaded_desc"
              ]
            },
            "folder_id": {
              "type": "integer",
              "nullable": true
            }
          }
        },
        "examples": {
          "alphabetical": {
            "value": {
              "sort_by": "name_asc",
              "folder_id": 12
            }
          },
          "manual": {
            "value": {
              "ids": [
                23,
                21,
                22
              ]
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Saved document order",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "object",
                "properties": {
                  "property_id": {
                    "type": "integer"
                  },
                  "ids": {
                    "type": "array",
                    "items": {
                      "type": "integer"
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
      "description": "Unauthorized"
    },
    "403": {
      "description": "Missing documents.edit scope"
    },
    "404": {
      "description": "Property not found"
    },
    "422": {
      "description": "Invalid sort or incomplete",
      "duplicate or foreign document IDs": null
    }
  }
}
```

## GET /documents

List documents

Requires `documents.list`.
Lists documents for a specific entity as a **full array response**.
This endpoint is intentionally **not cursor-paged**.

Examples:
- Exclude global templates: `/documents?entity_type=property&entity_id=42&include_global=false`
- Filter by folder: `/documents?entity_type=property&entity_id=42&folder_id=12`
- Filter by tags: `/documents?entity_type=property&entity_id=42&tag_ids=5,9`


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "entity_type",
      "in": "query",
      "required": true,
      "schema": {
        "type": "string",
        "enum": [
          "contact",
          "company",
          "property"
        ]
      },
      "example": "property"
    },
    {
      "name": "entity_id",
      "in": "query",
      "required": true,
      "schema": {
        "type": "integer"
      },
      "example": 42
    },
    {
      "name": "include_global",
      "in": "query",
      "required": false,
      "schema": {
        "type": "boolean"
      },
      "example": false
    },
    {
      "name": "folder_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      },
      "example": 12
    },
    {
      "name": "tag_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Comma-separated tag IDs",
      "example": "5,9"
    }
  ],
  "responses": {
    "200": {
      "description": "Document list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/Document"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Invalid entity_type"
    }
  }
}
```

## POST /documents

Upload documents

Requires `documents.add`. Upload one or more files for the given entity.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "multipart/form-data": {
        "schema": {
          "type": "object",
          "properties": {
            "entity_type": {
              "type": "string",
              "enum": [
                "contact",
                "company",
                "property"
              ]
            },
            "entity_id": {
              "type": "integer"
            },
            "folder_id": {
              "type": "integer"
            },
            "files": {
              "type": "array",
              "items": {
                "type": "string",
                "format": "binary"
              }
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Uploaded documents",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/Document"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /documents/{id}

Fetch document metadata

Requires `documents.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "entity_type",
      "in": "query",
      "required": true,
      "schema": {
        "type": "string",
        "enum": [
          "contact",
          "company",
          "property"
        ]
      }
    },
    {
      "name": "entity_id",
      "in": "query",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Document",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Document"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /documents/{id}

Update document metadata

Requires `documents.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "entity_type",
      "in": "query",
      "required": true,
      "schema": {
        "type": "string",
        "enum": [
          "contact",
          "company",
          "property"
        ]
      }
    },
    {
      "name": "entity_id",
      "in": "query",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "title": {
              "type": "string"
            },
            "folder_id": {
              "type": "integer"
            },
            "tag_ids": {
              "type": "array",
              "items": {
                "type": "integer"
              }
            },
            "publish_on_landingpage": {
              "type": "boolean"
            },
            "is_floorplan": {
              "type": "boolean"
            },
            "show_only_with_proof": {
              "type": "boolean"
            },
            "is_pdf_exposee": {
              "type": "boolean"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Document updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /documents/{id}

Update document metadata

Requires `documents.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "entity_type",
      "in": "query",
      "required": true,
      "schema": {
        "type": "string",
        "enum": [
          "contact",
          "company",
          "property"
        ]
      }
    },
    {
      "name": "entity_id",
      "in": "query",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "title": {
              "type": "string"
            },
            "folder_id": {
              "type": "integer"
            },
            "tag_ids": {
              "type": "array",
              "items": {
                "type": "integer"
              }
            },
            "publish_on_landingpage": {
              "type": "boolean"
            },
            "is_floorplan": {
              "type": "boolean"
            },
            "show_only_with_proof": {
              "type": "boolean"
            },
            "is_pdf_exposee": {
              "type": "boolean"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Document updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## DELETE /documents/{id}

Delete document

Requires `documents.delete`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "entity_type",
      "in": "query",
      "required": true,
      "schema": {
        "type": "string",
        "enum": [
          "contact",
          "company",
          "property"
        ]
      }
    },
    {
      "name": "entity_id",
      "in": "query",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /documents/{id}/download

Download document file

Requires `documents.read`.
Redirects to the actual file URL.

Example:
- Response `302 Found`
- `Location: http://localhost:3000/rails/active_storage/blobs/redirect/abc123/vertrag.pdf`


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "entity_type",
      "in": "query",
      "required": true,
      "schema": {
        "type": "string",
        "enum": [
          "contact",
          "company",
          "property"
        ]
      }
    },
    {
      "name": "entity_id",
      "in": "query",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "302": {
      "description": "Redirect to download URL",
      "headers": {
        "Location": {
          "description": "Absolute file URL for the document binary",
          "schema": {
            "type": "string"
          },
          "example": "http://localhost:3000/rails/active_storage/blobs/redirect/abc123/vertrag.pdf"
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /contacts/{id}/documents

List contact documents

Requires `documents.list`. Lists documents for a contact. Global templates are included by default.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "include_global",
      "in": "query",
      "required": false,
      "schema": {
        "type": "boolean"
      }
    },
    {
      "name": "folder_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "tag_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated tag IDs"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Document list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/Document"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## POST /contacts/{id}/documents

Upload contact documents

Requires `documents.add`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "multipart/form-data": {
        "schema": {
          "type": "object",
          "properties": {
            "folder_id": {
              "type": "integer"
            },
            "files": {
              "type": "array",
              "items": {
                "type": "string",
                "format": "binary"
              }
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Uploaded documents",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/Document"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /contacts/{id}/documents/{document_id}

Fetch contact document metadata

Requires `documents.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "document_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Document",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Document"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /contacts/{id}/documents/{document_id}

Update contact document metadata

Requires `documents.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "document_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "title": {
              "type": "string"
            },
            "folder_id": {
              "type": "integer"
            },
            "tag_ids": {
              "type": "array",
              "items": {
                "type": "integer"
              }
            },
            "publish_on_landingpage": {
              "type": "boolean"
            },
            "is_floorplan": {
              "type": "boolean"
            },
            "show_only_with_proof": {
              "type": "boolean"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Document updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /contacts/{id}/documents/{document_id}

Update contact document metadata

Requires `documents.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "document_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "title": {
              "type": "string"
            },
            "folder_id": {
              "type": "integer"
            },
            "tag_ids": {
              "type": "array",
              "items": {
                "type": "integer"
              }
            },
            "publish_on_landingpage": {
              "type": "boolean"
            },
            "is_floorplan": {
              "type": "boolean"
            },
            "show_only_with_proof": {
              "type": "boolean"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Document updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## DELETE /contacts/{id}/documents/{document_id}

Delete contact document

Requires `documents.delete`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "document_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /contacts/{id}/documents/{document_id}/download

Download contact document file

Requires `documents.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "document_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "302": {
      "description": "Redirect to download URL"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /companies/{id}/documents

List company documents

Requires `documents.list`. Lists documents for a company. Global templates are included by default.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "include_global",
      "in": "query",
      "required": false,
      "schema": {
        "type": "boolean"
      }
    },
    {
      "name": "folder_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "tag_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated tag IDs"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Document list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/Document"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## POST /companies/{id}/documents

Upload company documents

Requires `documents.add`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "multipart/form-data": {
        "schema": {
          "type": "object",
          "properties": {
            "folder_id": {
              "type": "integer"
            },
            "files": {
              "type": "array",
              "items": {
                "type": "string",
                "format": "binary"
              }
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Uploaded documents",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/Document"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /companies/{id}/documents/{document_id}

Fetch company document metadata

Requires `documents.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "document_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Document",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Document"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /companies/{id}/documents/{document_id}

Update company document metadata

Requires `documents.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "document_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "title": {
              "type": "string"
            },
            "folder_id": {
              "type": "integer"
            },
            "tag_ids": {
              "type": "array",
              "items": {
                "type": "integer"
              }
            },
            "publish_on_landingpage": {
              "type": "boolean"
            },
            "is_floorplan": {
              "type": "boolean"
            },
            "show_only_with_proof": {
              "type": "boolean"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Document updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /companies/{id}/documents/{document_id}

Update company document metadata

Requires `documents.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "document_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "title": {
              "type": "string"
            },
            "folder_id": {
              "type": "integer"
            },
            "tag_ids": {
              "type": "array",
              "items": {
                "type": "integer"
              }
            },
            "publish_on_landingpage": {
              "type": "boolean"
            },
            "is_floorplan": {
              "type": "boolean"
            },
            "show_only_with_proof": {
              "type": "boolean"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Document updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## DELETE /companies/{id}/documents/{document_id}

Delete company document

Requires `documents.delete`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "document_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /companies/{id}/documents/{document_id}/download

Download company document file

Requires `documents.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "document_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "302": {
      "description": "Redirect to download URL"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /properties/{id}/documents

List property documents

Requires `documents.list`. Lists documents for a property. Global templates are included by default.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "include_global",
      "in": "query",
      "required": false,
      "schema": {
        "type": "boolean"
      }
    },
    {
      "name": "folder_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "tag_ids",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "description": "Comma-separated tag IDs"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Document list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/Document"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## POST /properties/{id}/documents

Upload property documents

Requires `documents.add`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "multipart/form-data": {
        "schema": {
          "type": "object",
          "properties": {
            "folder_id": {
              "type": "integer"
            },
            "files": {
              "type": "array",
              "items": {
                "type": "string",
                "format": "binary"
              }
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Uploaded documents",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/Document"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## GET /properties/{id}/documents/{document_id}

Fetch property document metadata

Requires `documents.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "document_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Document",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Document"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## PATCH /properties/{id}/documents/{document_id}

Update property document metadata

Requires `documents.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "document_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "title": {
              "type": "string"
            },
            "folder_id": {
              "type": "integer"
            },
            "tag_ids": {
              "type": "array",
              "items": {
                "type": "integer"
              }
            },
            "publish_on_landingpage": {
              "type": "boolean"
            },
            "is_floorplan": {
              "type": "boolean"
            },
            "show_only_with_proof": {
              "type": "boolean"
            },
            "is_pdf_exposee": {
              "type": "boolean"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Document updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /properties/{id}/documents/{document_id}

Update property document metadata

Requires `documents.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "document_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "title": {
              "type": "string"
            },
            "folder_id": {
              "type": "integer"
            },
            "tag_ids": {
              "type": "array",
              "items": {
                "type": "integer"
              }
            },
            "publish_on_landingpage": {
              "type": "boolean"
            },
            "is_floorplan": {
              "type": "boolean"
            },
            "show_only_with_proof": {
              "type": "boolean"
            },
            "is_pdf_exposee": {
              "type": "boolean"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Document updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## DELETE /properties/{id}/documents/{document_id}

Delete property document

Requires `documents.delete`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "document_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /properties/{id}/documents/{document_id}/download

Download property document file

Requires `documents.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "document_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "302": {
      "description": "Redirect to download URL"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /folders

List folders

Requires `folders.list`.
Returns the folder tree for the given entity as a **full array response**.
This endpoint is intentionally **not cursor-paged**.
Global folders are included by default.

Example:
- `/folders?entity_type=property&entity_id=42&include_global=false`


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "entity_type",
      "in": "query",
      "required": true,
      "schema": {
        "type": "string",
        "enum": [
          "contact",
          "company",
          "property"
        ]
      },
      "example": "property"
    },
    {
      "name": "entity_id",
      "in": "query",
      "required": true,
      "schema": {
        "type": "integer"
      },
      "example": 42
    },
    {
      "name": "include_global",
      "in": "query",
      "required": false,
      "schema": {
        "type": "boolean"
      },
      "example": false
    }
  ],
  "responses": {
    "200": {
      "description": "Folder tree",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/Folder"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Invalid entity_type"
    }
  }
}
```

## POST /folders

Create folder

Requires `folders.add`. Creates a folder for the given entity (global folders are read-only in the API).

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "entity_type": {
              "type": "string",
              "enum": [
                "contact",
                "company",
                "property"
              ]
            },
            "entity_id": {
              "type": "integer"
            },
            "name": {
              "type": "string"
            },
            "parent_id": {
              "type": "integer",
              "nullable": true
            },
            "metadata": {
              "type": "object",
              "properties": {
                "color": {
                  "type": "string"
                },
                "emoji": {
                  "type": "string"
                }
              }
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Folder created",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/Folder"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PATCH /folders/{id}

Update folder

Requires `folders.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "entity_type": {
              "type": "string",
              "enum": [
                "contact",
                "company",
                "property"
              ]
            },
            "entity_id": {
              "type": "integer"
            },
            "name": {
              "type": "string"
            },
            "parent_id": {
              "type": "integer",
              "nullable": true
            },
            "metadata": {
              "type": "object",
              "properties": {
                "color": {
                  "type": "string"
                },
                "emoji": {
                  "type": "string"
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
      "description": "Folder updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## PUT /folders/{id}

Update folder

Requires `folders.edit`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "properties": {
            "entity_type": {
              "type": "string",
              "enum": [
                "contact",
                "company",
                "property"
              ]
            },
            "entity_id": {
              "type": "integer"
            },
            "name": {
              "type": "string"
            },
            "parent_id": {
              "type": "integer",
              "nullable": true
            },
            "metadata": {
              "type": "object",
              "properties": {
                "color": {
                  "type": "string"
                },
                "emoji": {
                  "type": "string"
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
      "description": "Folder updated"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    },
    "422": {
      "description": "Validation errors"
    }
  }
}
```

## DELETE /folders/{id}

Delete folder

Requires `folders.delete`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "entity_type",
      "in": "query",
      "required": true,
      "schema": {
        "type": "string",
        "enum": [
          "contact",
          "company",
          "property"
        ]
      }
    },
    {
      "name": "entity_id",
      "in": "query",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Deleted"
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## GET /tipster_tool

Read the tipster tool settings

Requires `tipster_tool.read`. Returns the tipster tool settings of the API key's shop and one entry per tip
type in the fixed order `sale`, `valuation`, `rental`, `search_profile`, `buyer`, `tenant`. Settings and tip
types are created with default values on first read. Answers `404` while propgen has not unlocked the module
for the shop.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Tipster tool settings",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "object",
                "properties": {
                  "settings": {
                    "type": "object",
                    "properties": {
                      "active": {
                        "type": "boolean",
                        "description": "Switched on by the account administrator."
                      },
                      "path": {
                        "type": "string",
                        "nullable": true,
                        "description": "Lowercase path of the tool address, unique across all accounts."
                      },
                      "self_registration_enabled": {
                        "type": "boolean"
                      },
                      "approver_user_id": {
                        "type": "integer",
                        "nullable": true,
                        "description": "User who receives registration and profile approvals."
                      },
                      "priority_window_months": {
                        "type": "integer",
                        "description": "Tip priority window in months."
                      },
                      "visible_property_status_ids": {
                        "type": "array",
                        "items": {
                          "type": "integer"
                        },
                        "description": "Property statuses tipsters see in the property search."
                      },
                      "search_suggestions_enabled": {
                        "type": "boolean"
                      },
                      "invited_status_id": {
                        "type": "integer",
                        "nullable": true,
                        "description": "Contact status \"Tippgeber (eingeladen)\"."
                      },
                      "registration_open_status_id": {
                        "type": "integer",
                        "nullable": true,
                        "description": "Contact status \"Tippgeber (Registrierung offen)\"."
                      },
                      "active_status_id": {
                        "type": "integer",
                        "nullable": true,
                        "description": "Contact status \"Tippgeber (aktiv)\"."
                      },
                      "deactivated_status_id": {
                        "type": "integer",
                        "nullable": true,
                        "description": "Contact status \"Tippgeber (deaktiviert)\"."
                      },
                      "source_id": {
                        "type": "integer",
                        "nullable": true,
                        "description": "Source \"Tippgeber\"."
                      },
                      "consent_document": {
                        "type": "object",
                        "nullable": true,
                        "properties": {
                          "filename": {
                            "type": "string"
                          },
                          "content_type": {
                            "type": "string"
                          },
                          "byte_size": {
                            "type": "integer"
                          }
                        }
                      }
                    }
                  },
                  "tip_types": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "speichergrund_id": {
                          "type": "integer",
                          "nullable": true,
                          "description": "Account retention reason applied to the tipped contact, with the tip date as event date. Null means none (default). Equal or longer existing retention remains unchanged."
                        },
                        "tip_type": {
                          "type": "string",
                          "enum": [
                            "sale",
                            "valuation",
                            "rental",
                            "search_profile",
                            "buyer",
                            "tenant"
                          ]
                        },
                        "pipeline_id": {
                          "type": "integer",
                          "nullable": true
                        },
                        "pipeline_column_id": {
                          "type": "integer",
                          "nullable": true,
                          "description": "Start phase of new tips."
                        },
                        "contact_status_ids": {
                          "type": "array",
                          "items": {
                            "type": "integer"
                          }
                        },
                        "contact_tag_ids": {
                          "type": "array",
                          "items": {
                            "type": "integer"
                          }
                        },
                        "property_status_ids": {
                          "type": "array",
                          "items": {
                            "type": "integer"
                          },
                          "description": "Applies to newly created properties only."
                        },
                        "property_tag_ids": {
                          "type": "array",
                          "items": {
                            "type": "integer"
                          },
                          "description": "Applies to newly created properties only."
                        },
                        "extra_fields": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "entity": {
                                "type": "string",
                                "enum": [
                                  "contact",
                                  "property",
                                  "search_profile",
                                  "deal"
                                ]
                              },
                              "field": {
                                "type": "string"
                              },
                              "required": {
                                "type": "boolean"
                              }
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
          "example": {
            "data": {
              "settings": {
                "active": true,
                "path": "mustermann-immobilien",
                "self_registration_enabled": false,
                "approver_user_id": 12,
                "priority_window_months": 18,
                "visible_property_status_ids": [
                  41,
                  42
                ],
                "search_suggestions_enabled": false,
                "invited_status_id": 301,
                "registration_open_status_id": 302,
                "active_status_id": 303,
                "deactivated_status_id": 304,
                "source_id": 77,
                "consent_document": null
              },
              "tip_types": [
                {
                  "tip_type": "sale",
                  "pipeline_id": 3,
                  "pipeline_column_id": 21,
                  "contact_status_ids": [],
                  "contact_tag_ids": [],
                  "property_status_ids": [],
                  "property_tag_ids": [],
                  "extra_fields": [
                    {
                      "entity": "property",
                      "field": "baujahr",
                      "required": true
                    }
                  ]
                }
              ]
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `tipster_tool.read` scope or source IP not allowed"
    },
    "404": {
      "description": "Tipster tool not unlocked for the shop"
    },
    "429": {
      "description": "API-key rate limit exceeded"
    }
  }
}
```

## GET /account

Fetch the account profile

Requires `account.read`. Returns the canonical `konto` merge context for the API key's shop, including
the effective legal-entity profile, logo URLs, Propstack-compatible address aliases, and an `assets`
mapping keyed by account asset key. Manage the shop's default signature through `/account/email_signature`.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Canonical account profile",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/AccountResponse"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `account.read` scope or source IP not allowed"
    },
    "429": {
      "description": "API-key rate limit exceeded"
    }
  }
}
```

## GET /account/email_signature

Read the shop default email signature

Requires `shop_email_signatures.read`. Returns the stored HTML template for the token's shop.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Shop signature",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "object",
                "properties": {
                  "shop_id": {
                    "type": "integer"
                  },
                  "html": {
                    "type": "string"
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing shop signature scope or source IP not allowed"
    }
  }
}
```

## PUT /account/email_signature

Set the shop default email signature

Requires `shop_email_signatures.edit`, granted through administrator-managed API keys.
Uses the same signature sanitizer and merge-field rules as user signatures.
For newly composed emails the precedence is mail account, composing user, then shop.
Shared-mailbox owner signatures do not replace the composing user's signature.
Changes do not rewrite existing drafts or sent messages. An empty string clears the shop default;
omitted or null HTML is rejected. User and mail-account signatures remain untouched.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "email_signature"
          ],
          "properties": {
            "email_signature": {
              "type": "object",
              "required": [
                "html"
              ],
              "properties": {
                "html": {
                  "type": "string"
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
      "description": "Saved signature as data: {shop_id, html}"
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing shop signature scope or source IP not allowed"
    },
    "422": {
      "description": "Invalid signature payload"
    }
  }
}
```

## GET /account/assets

List account assets

Requires `account_assets.read`. Assets belong to the API key's shop and are ordered by key.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Account asset list",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/AccountAssetListResponse"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `account_assets.read` scope or source IP not allowed"
    },
    "429": {
      "description": "API-key rate limit exceeded"
    }
  }
}
```

## POST /account/assets

Upload or replace an account asset

Requires `account_assets.add`. Uploads must be PNG, JPEG, or safe SVG files. Posting an existing key
replaces its current asset and returns a new permanent URL. The prior public file and URL are retained so
signatures that have already been sent keep working.
SVG support is limited to static shapes and paths; text, stylesheets, scripts, external references,
and ID-based references such as `url(#gradient)` are not supported.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "multipart/form-data": {
        "schema": {
          "type": "object",
          "required": [
            "key",
            "file"
          ],
          "properties": {
            "key": {
              "type": "string",
              "pattern": "^[a-z_][a-z0-9_]*$"
            },
            "file": {
              "type": "string",
              "format": "binary",
              "description": "PNG, JPEG, or SVG image."
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Uploaded or replaced account asset",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/AccountAssetResponse"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `account_assets.add` scope or source IP not allowed"
    },
    "422": {
      "description": "Missing file, invalid key, unsupported image type, or unsafe/invalid SVG",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/AccountAssetValidationError"
          }
        }
      }
    },
    "429": {
      "description": "API-key rate limit exceeded"
    }
  }
}
```

## DELETE /account/assets/{key}

Delete an account asset

Requires `account_assets.delete`. If a user or mail-account signature references the asset's merge path
or a current or retained URL, deletion returns `409 asset_in_use` with the references. Repeat with `confirm=true` to delete it.
Deletion removes the current and retained files; already-sent messages using those URLs may lose their images.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "key",
      "in": "path",
      "required": true,
      "schema": {
        "type": "string",
        "pattern": "^[a-z_][a-z0-9_]*$"
      }
    },
    {
      "name": "confirm",
      "in": "query",
      "required": false,
      "description": "Set to true to delete an asset referenced by a signature.",
      "schema": {
        "type": "boolean",
        "default": false
      }
    }
  ],
  "responses": {
    "204": {
      "description": "Account asset deleted"
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `account_assets.delete` scope or source IP not allowed"
    },
    "404": {
      "description": "Asset key not found in the API key's shop"
    },
    "409": {
      "description": "Asset is referenced by one or more signatures and confirmation was not supplied",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/AccountAssetUsageConflict"
          }
        }
      }
    },
    "429": {
      "description": "API-key rate limit exceeded"
    }
  }
}
```

## GET /users/{user_id}/email_signature

Fetch a user's email signature

Requires `email_signatures.read`. The user must belong to the API key's shop; IDs can be discovered through
`/lookups/users`. The response contains the stored sanitized HTML template. For personalization during email
rendering, use the documented email merge fields such as `{{ absender.full_name }}`,
`{{ absender.position }}` and `{{ konto.name }}`.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "user_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Stored user email signature",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/EmailSignatureResponse"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `email_signatures.read` scope or source IP not allowed"
    },
    "404": {
      "description": "User not found in the API key's shop"
    },
    "429": {
      "description": "API-key rate limit exceeded"
    }
  }
}
```

## PUT /users/{user_id}/email_signature

Replace a user's email signature

Requires `email_signatures.edit`. This operation replaces the complete user-level HTML signature. Send an
empty `html` value to clear it. Unsafe elements, event attributes, URLs and CSS are removed using the same
sanitizer as the propgen CRM signature editor; `text-transform` and `border-radius` are supported CSS properties.

In an `img src` or `a href`, one URL merge expression is accepted with this exact shape:
`[mailto:|tel:|http://|https://]{{ path [| default: 'literal' or "literal"] }}`. The prefix and `default`
filter are optional, and the literal cannot contain braces. Allowed paths are `konto.logo_url`,
`konto.logo_document_url`, `konto.logo_landingpage_url`, `konto.homepage_url`, `konto.instagram_url`,
`konto.facebook_url`, `konto.linkedin_url`, `konto.assets.<key>.url`, `absender.avatar_url`,
`absender.avatar_profile_url`, `absender.avatar_thumbnail_url`, `absender.email`, `absender.public_email`,
`absender.mobil`, and `absender.phone`; asset keys match `[a-z_][a-z0-9_]*`. Empty or invalid rendered image
URLs remove the image, while empty or invalid rendered link URLs remove only `href`. Unsafe schemes,
unsupported filters, multiple expressions, and non-whitelisted paths remain rejected.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "user_id",
      "in": "path",
      "required": true,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/EmailSignatureUpdateRequest"
        },
        "example": {
          "email_signature": {
            "html": "<p>Viele Grüße<br><strong>{{ absender.full_name }}</strong><br>{{ absender.position }} · {{ konto.name }}</p>"
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Replaced and sanitized user email signature",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/EmailSignatureResponse"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `email_signatures.edit` scope or source IP not allowed"
    },
    "404": {
      "description": "User not found in the API key's shop"
    },
    "422": {
      "description": "Missing or invalid request payload"
    },
    "429": {
      "description": "API-key rate limit exceeded"
    }
  }
}
```

## GET /cost_centers

List cost centers

Requires `cost_centers.list`. Ordered by code.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "legal_entity_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    },
    {
      "name": "active",
      "in": "query",
      "required": false,
      "description": "Filter by active or deactivated cost centers. Omit to list both.",
      "schema": {
        "type": "boolean"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Cost center list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/CostCenter"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `cost_centers.list` scope or source IP not allowed"
    }
  }
}
```

## POST /cost_centers

Create a cost center

Requires `cost_centers.add`. `code` must be `T` followed by five digits (e.g. `T00210`) and is unique per legal entity. `legal_entity_id` must be one of the organization's own legal entities.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "cost_center"
          ],
          "properties": {
            "cost_center": {
              "$ref": "#/components/schemas/CostCenterInput"
            }
          }
        },
        "example": {
          "cost_center": {
            "code": "T00210",
            "department": "Investment Zinshäuser",
            "abbreviation": "INV-ZH",
            "business_unit": "2. INV",
            "legal_entity_id": 1
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Cost center created",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/CostCenter"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `cost_centers.add` scope or source IP not allowed"
    },
    "422": {
      "description": "Invalid code",
      "duplicate code in the legal entity": null,
      "or unknown legal entity": null
    }
  }
}
```

## GET /cost_centers/{id}

Fetch a cost center

Requires `cost_centers.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Cost center",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/CostCenter"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `cost_centers.read` scope or source IP not allowed"
    },
    "404": {
      "description": "Cost center not found in the API key's organization"
    }
  }
}
```

## PATCH /cost_centers/{id}

Update or deactivate a cost center

Requires `cost_centers.edit`. Partial update; send `active` false to deactivate.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "cost_center"
          ],
          "properties": {
            "cost_center": {
              "$ref": "#/components/schemas/CostCenterInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Cost center updated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/CostCenter"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `cost_centers.edit` scope or source IP not allowed"
    },
    "404": {
      "description": "Cost center not found in the API key's organization"
    },
    "422": {
      "description": "Invalid code",
      "duplicate code in the legal entity": null,
      "or unknown legal entity": null
    }
  }
}
```

## PUT /cost_centers/{id}

Update or deactivate a cost center

Requires `cost_centers.edit`. Partial update; send `active` false to deactivate.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "cost_center"
          ],
          "properties": {
            "cost_center": {
              "$ref": "#/components/schemas/CostCenterInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Cost center updated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/CostCenter"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `cost_centers.edit` scope or source IP not allowed"
    },
    "404": {
      "description": "Cost center not found in the API key's organization"
    },
    "422": {
      "description": "Invalid code",
      "duplicate code in the legal entity": null,
      "or unknown legal entity": null
    }
  }
}
```

## GET /invoice_service_types

List service types

Requires `invoice_service_types.list`. Ordered by invoice type, commission side, quantity unit and rate.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "active",
      "in": "query",
      "required": false,
      "description": "Filter by active or deactivated entries. Omit to list both.",
      "schema": {
        "type": "boolean"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Service types",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/InvoiceServiceType"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `invoice_service_types.list` scope or source IP not allowed"
    }
  }
}
```

## POST /invoice_service_types

Create a service type

Requires `invoice_service_types.add`. `article_numbers` maps the ID of each of the organization's own legal entities to its article number in the billing system.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "invoice_service_type"
          ],
          "properties": {
            "invoice_service_type": {
              "$ref": "#/components/schemas/InvoiceServiceTypeInput"
            }
          }
        },
        "example": {
          "invoice_service_type": {
            "name": "Provision 3 % (Kaufpreis)",
            "invoice_type": "purchase_commission",
            "commission_side": "outer",
            "quantity_unit": "percent",
            "rate": 3,
            "individual": false,
            "for_own_entities": false,
            "parking": false,
            "article_numbers": {
              "1": "00000020"
            }
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Service type created",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/InvoiceServiceType"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `invoice_service_types.add` scope or source IP not allowed"
    },
    "422": {
      "description": "Missing name",
      "unknown invoice type": null,
      "commission side or quantity unit": null,
      "invalid rate or a rate on an individual or flat entry": null,
      "or a blank article number or one for an unknown legal entity": null
    }
  }
}
```

## GET /invoice_service_types/{id}

Fetch a service type

Requires `invoice_service_types.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Service type",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/InvoiceServiceType"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `invoice_service_types.read` scope or source IP not allowed"
    },
    "404": {
      "description": "Service type not found in the API key's organization"
    }
  }
}
```

## PATCH /invoice_service_types/{id}

Update a service type

Requires `invoice_service_types.edit`. Partial update; send `active` false to deactivate.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "invoice_service_type"
          ],
          "properties": {
            "invoice_service_type": {
              "$ref": "#/components/schemas/InvoiceServiceTypeInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Service type updated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/InvoiceServiceType"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `invoice_service_types.edit` scope or source IP not allowed"
    },
    "404": {
      "description": "Service type not found in the API key's organization"
    },
    "422": {
      "description": "Missing name",
      "unknown invoice type": null,
      "commission side or quantity unit": null,
      "invalid rate or a rate on an individual or flat entry": null,
      "or a blank article number or one for an unknown legal entity": null
    }
  }
}
```

## PUT /invoice_service_types/{id}

Update a service type

Requires `invoice_service_types.edit`. Partial update; send `active` false to deactivate.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "invoice_service_type"
          ],
          "properties": {
            "invoice_service_type": {
              "$ref": "#/components/schemas/InvoiceServiceTypeInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Service type updated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/InvoiceServiceType"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `invoice_service_types.edit` scope or source IP not allowed"
    },
    "404": {
      "description": "Service type not found in the API key's organization"
    },
    "422": {
      "description": "Missing name",
      "unknown invoice type": null,
      "commission side or quantity unit": null,
      "invalid rate or a rate on an individual or flat entry": null,
      "or a blank article number or one for an unknown legal entity": null
    }
  }
}
```

## GET /payment_terms

List payment terms

Requires `payment_terms.list`. Default first, then by label.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "active",
      "in": "query",
      "required": false,
      "description": "Filter by active or deactivated entries. Omit to list both.",
      "schema": {
        "type": "boolean"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Payment terms",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/PaymentTerm"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `payment_terms.list` scope or source IP not allowed"
    }
  }
}
```

## POST /payment_terms

Create a payment term

Requires `payment_terms.add`. `sage_key` is required and passed to the billing system unchanged. Marking a term as default removes the mark from the previous default.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "payment_term"
          ],
          "properties": {
            "payment_term": {
              "$ref": "#/components/schemas/PaymentTermInput"
            }
          }
        },
        "example": {
          "payment_term": {
            "label": "14 Tage rein netto",
            "sage_key": "14netto",
            "is_default": true
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Payment term created",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/PaymentTerm"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `payment_terms.add` scope or source IP not allowed"
    },
    "422": {
      "description": "Missing label or Sage key",
      "or an inactive default": null
    }
  }
}
```

## GET /payment_terms/{id}

Fetch a payment term

Requires `payment_terms.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Payment term",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/PaymentTerm"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `payment_terms.read` scope or source IP not allowed"
    },
    "404": {
      "description": "Payment term not found in the API key's organization"
    }
  }
}
```

## PATCH /payment_terms/{id}

Update a payment term

Requires `payment_terms.edit`. Partial update; send `active` false to deactivate.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "payment_term"
          ],
          "properties": {
            "payment_term": {
              "$ref": "#/components/schemas/PaymentTermInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Payment term updated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/PaymentTerm"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `payment_terms.edit` scope or source IP not allowed"
    },
    "404": {
      "description": "Payment term not found in the API key's organization"
    },
    "422": {
      "description": "Missing label or Sage key",
      "or an inactive default": null
    }
  }
}
```

## PUT /payment_terms/{id}

Update a payment term

Requires `payment_terms.edit`. Partial update; send `active` false to deactivate.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "payment_term"
          ],
          "properties": {
            "payment_term": {
              "$ref": "#/components/schemas/PaymentTermInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Payment term updated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/PaymentTerm"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `payment_terms.edit` scope or source IP not allowed"
    },
    "404": {
      "description": "Payment term not found in the API key's organization"
    },
    "422": {
      "description": "Missing label or Sage key",
      "or an inactive default": null
    }
  }
}
```

## GET /invoice_text_templates

List text templates

Requires `invoice_text_templates.list`. Ordered by invoice type.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Text templates",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/InvoiceTextTemplate"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `invoice_text_templates.list` scope or source IP not allowed"
    }
  }
}
```

## POST /invoice_text_templates

Create a text template

Requires `invoice_text_templates.add`. One template per invoice type. Placeholders use the merge syntax `{{ rechnungsvorbereitung.<key> }}`; a line whose placeholder has no value is left out.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "invoice_text_template"
          ],
          "properties": {
            "invoice_text_template": {
              "$ref": "#/components/schemas/InvoiceTextTemplateInput"
            }
          }
        },
        "example": {
          "invoice_text_template": {
            "name": "Kauf",
            "invoice_type": "purchase_commission",
            "header_template": "Kaufvertrag vom {{ rechnungsvorbereitung.vertragsdatum }}",
            "footer_template": "{{ rechnungsvorbereitung.zahlung_erlaeuterung }}",
            "position_template": "Provision vom Kaufpreis"
          }
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Text template created",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/InvoiceTextTemplate"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `invoice_text_templates.add` scope or source IP not allowed"
    },
    "422": {
      "description": "Missing name",
      "unknown invoice type": null,
      "or a template for this invoice type already exists": null
    }
  }
}
```

## GET /invoice_text_templates/{id}

Fetch a text template

Requires `invoice_text_templates.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Text template",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/InvoiceTextTemplate"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `invoice_text_templates.read` scope or source IP not allowed"
    },
    "404": {
      "description": "Text template not found in the API key's organization"
    }
  }
}
```

## PATCH /invoice_text_templates/{id}

Update a text template

Requires `invoice_text_templates.edit`. Partial update.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "invoice_text_template"
          ],
          "properties": {
            "invoice_text_template": {
              "$ref": "#/components/schemas/InvoiceTextTemplateInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Text template updated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/InvoiceTextTemplate"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `invoice_text_templates.edit` scope or source IP not allowed"
    },
    "404": {
      "description": "Text template not found in the API key's organization"
    },
    "422": {
      "description": "Missing name",
      "unknown invoice type": null,
      "or a template for this invoice type already exists": null
    }
  }
}
```

## PUT /invoice_text_templates/{id}

Update a text template

Requires `invoice_text_templates.edit`. Partial update.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "invoice_text_template"
          ],
          "properties": {
            "invoice_text_template": {
              "$ref": "#/components/schemas/InvoiceTextTemplateInput"
            }
          }
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Text template updated",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "$ref": "#/components/schemas/InvoiceTextTemplate"
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `invoice_text_templates.edit` scope or source IP not allowed"
    },
    "404": {
      "description": "Text template not found in the API key's organization"
    },
    "422": {
      "description": "Missing name",
      "unknown invoice type": null,
      "or a template for this invoice type already exists": null
    }
  }
}
```

## GET /users/{user_id}/sales_agent_numbers

Fetch a user's sales agent numbers

Requires `sales_agent_numbers.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Sales agent numbers of the user",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/SalesAgentNumbersResponse"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `sales_agent_numbers.read` scope or source IP not allowed"
    },
    "404": {
      "description": "User not found in the API key's organization"
    }
  }
}
```

## PUT /users/{user_id}/sales_agent_numbers

Replace a user's sales agent numbers

Requires `sales_agent_numbers.edit`. Replaces the complete list; send an empty array to remove all numbers. A number is unique per legal entity. `cost_center_ids` is optional and must name cost centers of the same legal entity. The list is replaced atomically: on a validation error nothing changes.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "type": "object",
          "required": [
            "sales_agent_numbers"
          ],
          "properties": {
            "sales_agent_numbers": {
              "type": "array",
              "items": {
                "$ref": "#/components/schemas/SalesAgentNumberInput"
              }
            }
          }
        },
        "example": {
          "sales_agent_numbers": [
            {
              "number": "V3004",
              "legal_entity_id": 1,
              "cost_center_ids": [
                12
              ]
            },
            {
              "number": "V4006",
              "legal_entity_id": 1,
              "cost_center_ids": [
                14
              ]
            }
          ]
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Replaced sales agent numbers",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/SalesAgentNumbersResponse"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing `sales_agent_numbers.edit` scope or source IP not allowed"
    },
    "404": {
      "description": "User not found in the API key's organization"
    },
    "422": {
      "description": "Missing list",
      "duplicate number": null,
      "unknown legal entity": null,
      "or cost center of another legal entity": null
    }
  }
}
```

## GET /lookups/users

List users for assignments

Requires one of `contacts.read`, `companies.read`, `properties.read`, `deals.read`, `tasks.read`, `notes.read`, `calendar_events.read`, `emails.read`, or `email_signatures.read`.
Returns users that can be assigned in select fields. Requires at least one applicable read scope:
`contacts.read`, `companies.read`, `properties.read`, `deals.read`, `tasks.read`, `notes.read`,
`calendar_events.read`, `emails.read`, or `email_signatures.read`.


Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "User list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "integer"
                    },
                    "name": {
                      "type": "string"
                    },
                    "full_name": {
                      "type": "string"
                    },
                    "email": {
                      "type": "string",
                      "nullable": true
                    },
                    "title": {
                      "type": "string",
                      "nullable": true
                    },
                    "position": {
                      "type": "string",
                      "nullable": true
                    },
                    "mobile": {
                      "type": "string",
                      "nullable": true
                    },
                    "phone": {
                      "type": "string",
                      "nullable": true
                    },
                    "avatar_url": {
                      "type": "string",
                      "format": "uri",
                      "nullable": true,
                      "description": "Original avatar URL."
                    },
                    "avatar_profile_url": {
                      "type": "string",
                      "format": "uri",
                      "nullable": true,
                      "description": "Profile-size avatar URL."
                    },
                    "avatar_thumbnail_url": {
                      "type": "string",
                      "format": "uri",
                      "nullable": true,
                      "description": "Thumbnail avatar URL."
                    },
                    "legal_entities": {
                      "type": "array",
                      "description": "Legal entities the user is assigned to. Empty array when the user has no assignment.",
                      "items": {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "integer"
                          },
                          "name": {
                            "type": "string",
                            "description": "Display name of the legal entity."
                          },
                          "default": {
                            "type": "boolean",
                            "description": "Whether this is the user's default legal entity."
                          }
                        }
                      }
                    }
                  }
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "total": {
                    "type": "integer"
                  },
                  "type": {
                    "type": "string"
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    }
  }
}
```

## GET /lookups/contact_tags

List contact tags

Requires `contacts.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Tag list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "integer"
                    },
                    "name": {
                      "type": "string"
                    },
                    "color": {
                      "type": "string",
                      "nullable": true
                    }
                  }
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "total": {
                    "type": "integer"
                  },
                  "type": {
                    "type": "string"
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## GET /lookups/contact_statuses

List contact statuses

Requires `contacts.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Status list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "integer"
                    },
                    "name": {
                      "type": "string"
                    },
                    "color": {
                      "type": "string",
                      "nullable": true
                    },
                    "status_category_id": {
                      "type": "integer",
                      "nullable": true
                    }
                  }
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "total": {
                    "type": "integer"
                  },
                  "type": {
                    "type": "string"
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## GET /lookups/company_tags

List company tags

Requires `companies.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Tag list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "integer"
                    },
                    "name": {
                      "type": "string"
                    },
                    "color": {
                      "type": "string",
                      "nullable": true
                    }
                  }
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "total": {
                    "type": "integer"
                  },
                  "type": {
                    "type": "string"
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## GET /lookups/company_statuses

List company statuses

Requires `companies.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Status list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "integer"
                    },
                    "name": {
                      "type": "string"
                    },
                    "color": {
                      "type": "string",
                      "nullable": true
                    },
                    "status_category_id": {
                      "type": "integer",
                      "nullable": true
                    }
                  }
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "total": {
                    "type": "integer"
                  },
                  "type": {
                    "type": "string"
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## GET /lookups/property_tags

List property tags

Requires `properties.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Tag list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "integer"
                    },
                    "name": {
                      "type": "string"
                    },
                    "color": {
                      "type": "string",
                      "nullable": true
                    }
                  }
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "total": {
                    "type": "integer"
                  },
                  "type": {
                    "type": "string"
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## GET /lookups/property_statuses

List property statuses

Requires `properties.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Status list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "integer"
                    },
                    "name": {
                      "type": "string"
                    },
                    "color": {
                      "type": "string",
                      "nullable": true
                    },
                    "status_category_id": {
                      "type": "integer",
                      "nullable": true
                    },
                    "stacking_plan_state": {
                      "$ref": "#/components/schemas/StackingPlanState"
                    }
                  }
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "total": {
                    "type": "integer"
                  },
                  "type": {
                    "type": "string"
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## GET /lookups/pipelines

List pipelines

Requires one of `pipelines.read` or `deals.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Pipeline list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "integer"
                    },
                    "name": {
                      "type": "string"
                    },
                    "archived_at": {
                      "type": "string",
                      "format": "date-time",
                      "nullable": true
                    }
                  }
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "total": {
                    "type": "integer"
                  },
                  "type": {
                    "type": "string"
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## GET /lookups/pipeline_columns

List pipeline columns

Requires one of `pipeline_columns.read` or `deals.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "pipeline_id",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Pipeline column list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "integer"
                    },
                    "pipeline_id": {
                      "type": "integer"
                    },
                    "pipeline_name": {
                      "type": "string",
                      "nullable": true
                    },
                    "title": {
                      "type": "string"
                    },
                    "color": {
                      "type": "string",
                      "nullable": true
                    },
                    "system_key": {
                      "type": "string",
                      "nullable": true
                    },
                    "archived_at": {
                      "type": "string",
                      "format": "date-time",
                      "nullable": true
                    }
                  }
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "total": {
                    "type": "integer"
                  },
                  "type": {
                    "type": "string"
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## GET /lookups/speichergruende

List retention reasons (Speichergründe)

Requires `contacts.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Reason list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "integer"
                    },
                    "label": {
                      "type": "string"
                    },
                    "days": {
                      "type": "integer",
                      "nullable": true
                    }
                  }
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "total": {
                    "type": "integer"
                  },
                  "type": {
                    "type": "string"
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## GET /lookups/teams

List teams

Requires one of `contacts.read`, `companies.read`, `properties.read`, `deals.read`, or `tasks.read`. Returns every team in the API key's shop. The IDs can be used as `team_ids`, including for tasks. `cost_center` is the team's optional cost center (read-only), `null` when none is set.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Team list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "integer"
                    },
                    "name": {
                      "type": "string"
                    },
                    "cost_center": {
                      "type": "object",
                      "nullable": true,
                      "description": "The team's cost center (Kostenstelle), read-only.",
                      "properties": {
                        "id": {
                          "type": "integer",
                          "description": "ID as in `GET /cost_centers`"
                        },
                        "code": {
                          "type": "string",
                          "example": "T00210"
                        },
                        "department": {
                          "type": "string",
                          "nullable": true,
                          "description": "Fachbereich",
                          "e.g. Investment Zinshäuser": null
                        },
                        "active": {
                          "type": "boolean",
                          "description": "`false` when the cost center was deactivated in the catalog; the team keeps it until it is changed in the team dialog."
                        }
                      }
                    }
                  }
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "total": {
                    "type": "integer"
                  },
                  "type": {
                    "type": "string"
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## GET /lookups/mail_sources

List mail sources (email sources)

Requires one of `contacts.read` or `properties.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Source list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "integer"
                    },
                    "name": {
                      "type": "string"
                    }
                  }
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "total": {
                    "type": "integer"
                  },
                  "type": {
                    "type": "string"
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## GET /lookups/geolages

List geolages (location taxonomy)

Requires `properties.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Geolage list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "integer"
                    },
                    "name": {
                      "type": "string"
                    },
                    "parent_id": {
                      "type": "integer",
                      "nullable": true
                    }
                  }
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "total": {
                    "type": "integer"
                  },
                  "type": {
                    "type": "string"
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## GET /lookups/landingpages

List landingpage templates

Requires `properties.read`. Without `record_type`, returns all templates. Property/project filters include universal templates.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "record_type",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "property",
          "project"
        ]
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Landingpage list",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "integer"
                    },
                    "name": {
                      "type": "string"
                    }
                  }
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "total": {
                    "type": "integer"
                  },
                  "type": {
                    "type": "string"
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing properties.read scope"
    },
    "422": {
      "description": "Invalid record_type"
    }
  }
}
```

## GET /event_location_presets

List calendar event location presets

Requires `calendar_events.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Location presets",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "type": "object"
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    }
  }
}
```

## GET /event_cancellation_reasons

List calendar event cancellation reasons

Requires `calendar_events.read`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Cancellation reasons",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "integer"
                    },
                    "name": {
                      "type": "string"
                    },
                    "position": {
                      "type": "integer"
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
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    }
  }
}
```

## GET /search/contacts

Search contacts

Requires `contacts.read`. Lookup-style search (Elasticsearch-backed) for contacts. Default `fields=summary` returns lightweight rows for pickers. Use `fields=full` to return the same contact payload as `GET /contacts/:id?fields=full`, plus a top-level `phone_numbers` array (`number` and optional `description` label per row) so integrations can verify which contact matches a dialed number without parsing the nested `data` blob.
For 3CX, use `phone=...&fields=telephony` (requires `contacts.read`). This mode returns only full normalized phone matches, scoped to active contacts in the API key's shop. German national, +49 and 0049 formats are equivalent. International + and 00 prefixes are equivalent; foreign national numbers are not interpreted using a guessed country. Multiple matching contacts are all returned, without pagination; `limit`, `q` and `query` do not affect telephony mode. No match returns `{ "data": [], "meta": { "total": 0 } }`. Encode a leading plus as `%2B` in the URL. `matched_phone` is the verified requested number with separators removed, allowing 3CX to match the dial string. Existing `summary` and `full` responses are unchanged.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "q",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Search query. `query` is accepted as an alias; one of `q` or `query` is required outside telephony mode."
    },
    {
      "name": "query",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Alias for `q`."
    },
    {
      "name": "phone",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Required with `fields=telephony`; not accepted in other modes. Full phone number, not a suffix.",
      "example": "+4917011122233"
    },
    {
      "name": "limit",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 50
      }
    },
    {
      "name": "fields",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string",
        "enum": [
          "summary",
          "full",
          "telephony"
        ]
      },
      "description": "`summary` (default): id, name, email. `full`: full contact resource per `Contact` schema plus top-level `phone_numbers` for disambiguation. `telephony`: flat verified phone matches."
    }
  ],
  "responses": {
    "200": {
      "description": "Search result",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "anyOf": [
                    {
                      "$ref": "#/components/schemas/ContactSearchSummaryRow"
                    },
                    {
                      "$ref": "#/components/schemas/ContactSearchFullRow"
                    },
                    {
                      "$ref": "#/components/schemas/ContactSearchTelephonyRow"
                    },
                    {
                      "$ref": "#/components/schemas/RestrictedEntity"
                    }
                  ]
                }
              },
              "meta": {
                "description": "Telephony mode returns only total, counting verified contacts.",
                "type": "object",
                "properties": {
                  "query": {
                    "type": "string",
                    "nullable": true
                  },
                  "total": {
                    "type": "integer"
                  },
                  "limit": {
                    "type": "integer"
                  },
                  "fields": {
                    "type": "string",
                    "enum": [
                      "summary",
                      "full",
                      "telephony"
                    ],
                    "description": "Echo of the requested `fields` mode (default summary)"
                  }
                }
              }
            }
          }
        }
      }
    },
    "401": {
      "description": "Unauthorized"
    },
    "403": {
      "description": "Forbidden"
    },
    "422": {
      "description": "Missing query, invalid fields, missing_phone or invalid_phone"
    },
    "503": {
      "description": "Telephony search unavailable (search_unavailable); not an empty match result"
    }
  }
}
```

## GET /search/companies

Search companies

Requires `companies.read`. Returns lightweight company records for association inputs.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "q",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Search query. `query` is accepted as an alias; one of `q` or `query` is required."
    },
    {
      "name": "query",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Alias for `q`."
    },
    {
      "name": "limit",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 50
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Search result",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "anyOf": [
                    {
                      "type": "object",
                      "properties": {
                        "id": {
                          "type": "integer"
                        },
                        "company_name": {
                          "type": "string",
                          "nullable": true
                        },
                        "name": {
                          "type": "string",
                          "nullable": true
                        }
                      }
                    },
                    {
                      "$ref": "#/components/schemas/RestrictedEntity"
                    }
                  ]
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "query": {
                    "type": "string",
                    "nullable": true
                  },
                  "total": {
                    "type": "integer"
                  },
                  "limit": {
                    "type": "integer"
                  }
                }
              }
            }
          }
        }
      }
    },
    "422": {
      "description": "Missing query parameter"
    }
  }
}
```

## GET /search/properties

Search properties

Requires `properties.read`. Returns lightweight property records for association inputs.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "q",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Search query. `query` is accepted as an alias; one of `q` or `query` is required."
    },
    {
      "name": "query",
      "in": "query",
      "required": false,
      "schema": {
        "type": "string"
      },
      "description": "Alias for `q`."
    },
    {
      "name": "limit",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 50
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Search result",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "anyOf": [
                    {
                      "type": "object",
                      "properties": {
                        "id": {
                          "type": "integer"
                        },
                        "full_address": {
                          "type": "string",
                          "nullable": true
                        },
                        "objekttitel": {
                          "type": "string",
                          "nullable": true
                        }
                      }
                    },
                    {
                      "$ref": "#/components/schemas/RestrictedEntity"
                    }
                  ]
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "query": {
                    "type": "string",
                    "nullable": true
                  },
                  "total": {
                    "type": "integer"
                  },
                  "limit": {
                    "type": "integer"
                  }
                }
              }
            }
          }
        }
      }
    },
    "422": {
      "description": "Missing query parameter"
    }
  }
}
```

## GET /search/deals

Search deals

Requires `deals.read`. Returns lightweight deal records for association inputs.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "name": "q",
      "in": "query",
      "required": true,
      "schema": {
        "type": "string"
      }
    },
    {
      "name": "limit",
      "in": "query",
      "required": false,
      "schema": {
        "type": "integer",
        "minimum": 1,
        "maximum": 50
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Search result",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "data": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "integer"
                    },
                    "title": {
                      "type": "string",
                      "nullable": true
                    },
                    "deal_id_hash": {
                      "type": "string",
                      "nullable": true
                    },
                    "pipeline_id": {
                      "type": "integer",
                      "nullable": true
                    },
                    "pipeline_column_id": {
                      "type": "integer",
                      "nullable": true
                    }
                  }
                }
              },
              "meta": {
                "type": "object",
                "properties": {
                  "query": {
                    "type": "string",
                    "nullable": true
                  },
                  "total": {
                    "type": "integer"
                  },
                  "limit": {
                    "type": "integer"
                  }
                }
              }
            }
          }
        }
      }
    },
    "422": {
      "description": "Missing query parameter"
    }
  }
}
```

## GET /form_definitions

Discover supported form-definition models

Requires `form_definitions.read`. Returns the bounded model collection and contract version.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Supported form-definition models",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/FormDefinitionDiscovery"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing form_definitions.read scope"
    }
  }
}
```

## GET /form_definitions/{model}

Read the effective form definition

Requires `form_definitions.read`. For notes, omitting `category_key` returns the shop-global field catalog; providing it selects one category-owned layout that references those global definitions. Returns the canonical writable custom fields and customizations together with the fully resolved, effective read view in `effective_schema`. Visibility settings control presentation, not authorization. Returns a strong ETag.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Form definition",
      "headers": {
        "ETag": {
          "schema": {
            "type": "string"
          },
          "description": "Strong configuration version"
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/FormDefinition"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing form_definitions.read scope"
    },
    "422": {
      "description": "Unsupported model; includes the allowed model keys",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/FormDefinitionUnsupportedModel"
          }
        }
      }
    }
  }
}
```

## PUT /form_definitions/{model}

Atomically apply a form definition candidate

Requires `form_definitions.edit` and the current strong ETag in `If-Match`. For notes, omit `category_key` to replace global field definitions (with empty customizations), or provide it to replace one category layout using exact global field definitions. Existing custom fields cannot be omitted, renamed, deleted, or have type/source or provider metadata changed. Configuration is committed even if an Elasticsearch mapping sync fails; retry the same request body using the ETag returned by the successful 200 response as the new `If-Match` value to converge mappings.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "in": "header",
      "name": "If-Match",
      "required": true,
      "schema": {
        "type": "string"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/FormDefinitionCandidateInput"
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Applied definition; warnings and mapping_errors report eventual mapping-sync failures",
      "headers": {
        "ETag": {
          "schema": {
            "type": "string"
          },
          "description": "Strong configuration version"
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/FormDefinitionApplyResponse"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing form_definitions.edit scope"
    },
    "400": {
      "description": "Malformed request body"
    },
    "412": {
      "description": "ETag mismatch; fetch definition_url and retry with current_etag",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/FormDefinitionEtagMismatch"
          }
        }
      }
    },
    "422": {
      "description": "Field-addressed candidate validation errors"
    },
    "428": {
      "description": "If-Match is required"
    }
  }
}
```

## PATCH /form_definitions/{model}

Atomically apply form-definition operations

Requires `form_definitions.edit` and the current strong ETag in `If-Match`. The request is an operations envelope; all operations are validated and applied atomically.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "in": "header",
      "name": "If-Match",
      "required": true,
      "schema": {
        "type": "string"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/FormDefinitionOperationsEnvelope"
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Applied effective definition",
      "headers": {
        "ETag": {
          "schema": {
            "type": "string"
          },
          "description": "Strong configuration version"
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/FormDefinitionApplyResponse"
          }
        }
      }
    },
    "400": {
      "description": "Malformed request body"
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing form_definitions.edit scope"
    },
    "412": {
      "description": "ETag mismatch",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/FormDefinitionEtagMismatch"
          }
        }
      }
    },
    "422": {
      "description": "Invalid operations or unsupported model"
    },
    "428": {
      "description": "If-Match is required"
    }
  }
}
```

## POST /form_definitions/{model}/validate

Validate a form definition candidate without mutation

Requires `form_definitions.edit`. Returns normalization, warnings, field-addressed errors, and a semantic diff.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "in": "path",
      "name": "model",
      "required": true,
      "schema": {
        "type": "string",
        "enum": [
          "properties",
          "contacts",
          "companies",
          "leases",
          "notes"
        ]
      }
    },
    {
      "in": "query",
      "name": "category_key",
      "required": false,
      "schema": {
        "type": "string",
        "pattern": "^[a-z0-9]+(?:[_-][a-z0-9]+)*$"
      },
      "description": "Optional for `model=notes`; omit for the global field catalog or provide a stable category key for one category layout."
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/FormDefinitionCandidateInput"
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Valid candidate",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/FormDefinitionValidationResult"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing form_definitions.edit scope"
    },
    "400": {
      "description": "Malformed request body"
    },
    "422": {
      "description": "Invalid candidate",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/FormDefinitionValidationFailure"
          }
        }
      }
    }
  }
}
```

## POST /form_definitions/{model}/operations/validate

Validate form-definition operations without mutation

Requires `form_definitions.edit`. Applies the operations to the current canonical definition in memory and returns its normalized candidate, errors, warnings, and semantic diff without changing the ETag.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "in": "path",
      "name": "model",
      "required": true,
      "schema": {
        "type": "string",
        "enum": [
          "properties",
          "contacts",
          "companies",
          "leases",
          "notes"
        ]
      }
    },
    {
      "in": "query",
      "name": "category_key",
      "required": false,
      "schema": {
        "type": "string",
        "pattern": "^[a-z0-9]+(?:[_-][a-z0-9]+)*$"
      },
      "description": "Optional for `model=notes`; omit for the global field catalog or provide a stable category key for one category layout."
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/FormDefinitionOperationsEnvelope"
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Valid operations",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/FormDefinitionValidationResult"
          }
        }
      }
    },
    "400": {
      "description": "Malformed request body"
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing form_definitions.edit scope"
    },
    "422": {
      "description": "Invalid operations or unsupported model",
      "content": {
        "application/json": {
          "schema": {
            "oneOf": [
              {
                "$ref": "#/components/schemas/FormDefinitionValidationFailure"
              },
              {
                "$ref": "#/components/schemas/FormDefinitionUnsupportedModel"
              }
            ]
          }
        }
      }
    }
  }
}
```

## DELETE /form_definitions/{model}/customizations

Reset all canonical customizations

Requires `form_definitions.edit` and the current strong ETag. Custom fields are retained; only customizations are removed.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "in": "path",
      "name": "model",
      "required": true,
      "schema": {
        "type": "string",
        "enum": [
          "properties",
          "contacts",
          "companies",
          "leases",
          "notes"
        ]
      }
    },
    {
      "in": "query",
      "name": "category_key",
      "required": false,
      "description": "Required only when resetting one note category layout.",
      "schema": {
        "type": "string",
        "pattern": "^[a-z0-9]+(?:[_-][a-z0-9]+)*$"
      }
    },
    {
      "in": "header",
      "name": "If-Match",
      "required": true,
      "schema": {
        "type": "string"
      }
    }
  ],
  "responses": {
    "200": {
      "description": "Effective definition after reset",
      "headers": {
        "ETag": {
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/FormDefinitionApplyResponse"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing form_definitions.edit scope"
    },
    "412": {
      "description": "ETag mismatch",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/FormDefinitionEtagMismatch"
          }
        }
      }
    },
    "422": {
      "description": "Unsupported model or legacy configuration requiring migration"
    },
    "428": {
      "description": "If-Match is required"
    }
  }
}
```

## GET /form_definitions/{model}/custom_fields

List canonical custom fields

Requires `form_definitions.read`. For notes this endpoint is shop-global and does not accept `category_key`. Returns custom fields only, not fields inherited into the effective schema.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Custom fields",
      "headers": {
        "ETag": {
          "schema": {
            "type": "string"
          }
        }
      },
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/FormDefinitionCustomFieldCollection"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing form_definitions.read scope"
    },
    "400": {
      "description": "category_key is not supported by the global custom-field catalog"
    },
    "422": {
      "description": "Unsupported model"
    }
  }
}
```

## POST /form_definitions/{model}/custom_fields

Create or upsert a custom field

Requires `form_definitions.edit` and the current strong ETag. Accepts either `{ custom_field: field }` or the field object directly. Note field definitions are always shop-global; do not send `category_key`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "parameters": [
    {
      "in": "header",
      "name": "If-Match",
      "required": true,
      "schema": {
        "type": "string"
      }
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "oneOf": [
            {
              "$ref": "#/components/schemas/FormDefinitionCustomFieldInput"
            },
            {
              "type": "object",
              "required": [
                "custom_field"
              ],
              "properties": {
                "custom_field": {
                  "$ref": "#/components/schemas/FormDefinitionCustomFieldInput"
                }
              }
            }
          ]
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Effective definition after upsert",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/FormDefinitionApplyResponse"
          }
        }
      }
    },
    "400": {
      "description": "category_key is not supported by the global custom-field catalog"
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing form_definitions.edit scope"
    },
    "412": {
      "description": "ETag mismatch",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/FormDefinitionEtagMismatch"
          }
        }
      }
    },
    "422": {
      "description": "Field validation errors or unsupported model"
    },
    "428": {
      "description": "If-Match is required"
    }
  }
}
```

## PATCH /form_definitions/{model}/custom_fields/{field}

Upsert a custom field at a stable field key

Requires `form_definitions.edit`. The path field overrides any `field` value in the direct or wrapped request body.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/FormDefinitionCustomFieldInput"
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Effective definition after upsert",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/FormDefinitionApplyResponse"
          }
        }
      }
    },
    "400": {
      "description": "category_key is not supported by the global custom-field catalog"
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing form_definitions.edit scope"
    },
    "412": {
      "description": "ETag mismatch",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/FormDefinitionEtagMismatch"
          }
        }
      }
    },
    "422": {
      "description": "Field validation errors or unsupported model"
    },
    "428": {
      "description": "If-Match is required"
    }
  }
}
```

## DELETE /form_definitions/{model}/custom_fields/{field}

Delete a custom field

Requires `form_definitions.edit`. Deletion is idempotent and removes the deleted field's own assignment, override, and hidden-field entries. It fails validation while another definition dynamically references the field or while records still contain values. Use this dedicated endpoint instead of omitting an existing field from a PUT candidate.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Effective definition after deletion",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/FormDefinitionApplyResponse"
          }
        }
      }
    },
    "400": {
      "description": "category_key is not supported by the global custom-field catalog"
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing form_definitions.edit scope"
    },
    "412": {
      "description": "ETag mismatch",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/FormDefinitionEtagMismatch"
          }
        }
      }
    },
    "422": {
      "description": "Field has stored values",
      "is dynamically referenced": null,
      "or the model is unsupported": null
    },
    "428": {
      "description": "If-Match is required"
    }
  }
}
```

## GET /form_definitions/{model}/field_tags

List field tags for the model

Requires `form_definitions.read`. Results are shop- and model-scoped and ordered by name.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "200": {
      "description": "Field tags",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/FormDefinitionFieldTagCollection"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing form_definitions.read scope"
    },
    "422": {
      "description": "Unsupported model"
    }
  }
}
```

## POST /form_definitions/{model}/field_tags

Create a field tag

Requires `form_definitions.edit`. Accepts either `{ field_tag: tag }` or the tag object directly. Missing color defaults to `#64748B`; category_name is created when needed and defaults to `Allgemein`.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/FormDefinitionFieldTagInput"
        }
      }
    }
  },
  "responses": {
    "201": {
      "description": "Created field tag",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/FormDefinitionFieldTagResponse"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing form_definitions.edit scope"
    },
    "422": {
      "description": "Invalid category",
      "validation errors": null,
      "or unsupported model": null
    }
  }
}
```

## PATCH /form_definitions/{model}/field_tags/{id}

Update a field tag

Requires `form_definitions.edit`. Accepts either `{ field_tag: tag }` or the tag object directly.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/FormDefinitionFieldTagInput"
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Updated field tag",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/FormDefinitionFieldTagResponse"
          }
        }
      }
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing form_definitions.edit scope"
    },
    "404": {
      "description": "Field tag not found in this shop and model"
    },
    "422": {
      "description": "Invalid category",
      "validation errors": null,
      "or unsupported model": null
    }
  }
}
```

## DELETE /form_definitions/{model}/field_tags/{id}

Delete a field tag

Requires `form_definitions.edit`. A tag referenced by `field_overrides.tag_ids` cannot be deleted.

Status: documented, not live-tested.

```json
{
  "security": [
    {
      "BearerAuth": []
    },
    {
      "ApiKeyHeader": []
    }
  ],
  "responses": {
    "204": {
      "description": "Field tag deleted"
    },
    "401": {
      "description": "Invalid or missing API key"
    },
    "403": {
      "description": "Missing form_definitions.edit scope"
    },
    "404": {
      "description": "Field tag not found in this shop and model"
    },
    "409": {
      "description": "Tag is referenced by field_overrides.tag_ids"
    },
    "422": {
      "description": "Unsupported model"
    }
  }
}
```
