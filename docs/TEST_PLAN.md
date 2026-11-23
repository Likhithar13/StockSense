# Test plan

## Scope
Product CRUD validation, sale recording, stock integrity, dashboard summaries, forecast service and health endpoint.

## Manual test cases
| ID | Steps | Expected result |
|---|---|---|
| TC-01 | Add product with valid values. | Product appears in product list. |
| TC-02 | Add product with duplicate name. | Validation message; duplicate not created. |
| TC-03 | Add product with negative stock. | Request rejected; record not created. |
| TC-04 | Record sale quantity 2 for stock 5. | Sale recorded; stock becomes 3. |
| TC-05 | Record sale quantity 6 for stock 5. | Sale rejected; stock remains 5. |
| TC-06 | Set stock equal to reorder threshold. | Product appears in low-stock alerts. |
| TC-07 | Open forecast page with no sales. | Insufficient data shown safely. |
| TC-08 | Open /health. | JSON status is ok. |

## Automated tests
Run `pytest --cov=app --cov=services --cov-report=term-missing`.
The included tests cover health/dashboard, product creation, sale decrement, oversell prevention and reorder arithmetic.

## Concurrency test recommendation
For the final academic submission, add a PostgreSQL integration test that starts two simultaneous sales against the same small stock balance. Confirm that only the sale(s) within available stock succeed and the final quantity is never negative. SQLite is used for fast local unit tests.
