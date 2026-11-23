# User stories and acceptance criteria

| ID | User story | Acceptance criteria |
|---|---|---|
| US-01 | As staff, I want to add a product so that it appears in inventory. | Valid product saves; duplicate name is rejected; negative values are rejected. |
| US-02 | As staff, I want to edit product details so that records stay current. | Updated values appear in product list after save. |
| US-03 | As staff, I want to delete a product that is no longer sold. | Product is removed after confirmation. |
| US-04 | As staff, I want to record a sale so stock stays accurate. | Sale is saved and stock decreases by exactly the sold quantity. |
| US-05 | As owner, I want overselling prevented. | A sale larger than available stock is rejected and stock is unchanged. |
| US-06 | As owner, I want low-stock alerts. | Products at or below their reorder threshold appear on dashboard. |
| US-07 | As owner, I want a weekly demand estimate. | Forecast page shows an estimate or an insufficient-data message/method. |
| US-08 | As owner, I want a reorder suggestion. | Suggested top-up is never negative and is visible beside each product. |
| US-09 | As operator, I want a health endpoint. | GET /health returns JSON with status=ok. |

## Two-sprint plan
- Sprint 1: product CRUD, sales entry, stock validation, dashboard.
- Sprint 2: weekly demand forecast, reorder suggestions, CI, tests, container packaging and documentation.
