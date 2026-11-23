# Software Requirements Specification (SRS)

## 1. Purpose
StockSense supports small retail shops with inventory tracking, sales recording, low-stock alerts and per-product demand estimates.

## 2. Users
- Shop owner: reviews stock, forecasts and suggested replenishment.
- Store staff: maintains product records and records sales.

## 3. Functional requirements
| ID | Requirement |
|---|---|
| FR-01 | The system shall allow staff to add a product with name, category, price, quantity and reorder threshold. |
| FR-02 | The system shall list and update existing products. |
| FR-03 | The system shall allow staff to delete a product. |
| FR-04 | The system shall record a sale for a selected product. |
| FR-05 | A successful sale shall reduce stock by the sold quantity. |
| FR-06 | The system shall reject sales that exceed available stock. |
| FR-07 | The dashboard shall show product count, units in stock, units sold and low-stock items. |
| FR-08 | The system shall estimate next-week demand from recorded sales history. |
| FR-09 | The system shall show a suggested reorder quantity. |
| FR-10 | The system shall expose a health endpoint for deployment checks. |

## 4. Non-functional requirements
- NFR-01: Inventory quantities must never become negative through the sale workflow.
- NFR-02: The UI shall be responsive using Bootstrap.
- NFR-03: Core business rules shall have automated tests.
- NFR-04: The application shall be containerizable with Docker.
- NFR-05: Database credentials and secret keys must be configured outside source code in production.

## 5. Assumptions and exclusions
The initial version does not include authentication, barcode scanning, supplier integrations, purchase-order creation, or multi-store tenancy. Forecasts are advisory only.
