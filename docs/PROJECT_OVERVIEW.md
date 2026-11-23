# StockSense: Retail Inventory with Demand Forecast

## Problem and users
Small retailers can overstock slow-moving items and run out of popular ones. Primary users are shop owners and store staff.

## Architecture
Bootstrap browser UI -> Flask routes -> SQLAlchemy models -> PostgreSQL database.
A forecasting service groups sales into weekly totals and applies a scikit-learn linear regression model. A reorder service estimates a suggested top-up. GitHub Actions/Jenkins run automated tests and build the Docker image.

## Main use cases
- Shop staff create and maintain product records.
- Staff record sales; stock is reduced transactionally.
- Owners review low-stock alerts.
- Owners review next-week demand forecasts and reorder suggestions.

## Important limitation
The starter forecasting model is intentionally simple and educational. It needs enough representative sales history, and does not yet model holidays, promotions, supplier lead time, stock-outs, or seasonality. The owner must make the final ordering decision.
