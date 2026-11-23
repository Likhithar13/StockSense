from datetime import date
import numpy as np
from sklearn.linear_model import LinearRegression
from sqlalchemy import func
from app import db
from models import Sale

def weekly_sales(product_id):
    rows = (db.session.query(func.date(Sale.sold_at), func.sum(Sale.quantity))
            .filter(Sale.product_id == product_id)
            .group_by(func.date(Sale.sold_at))
            .order_by(func.date(Sale.sold_at)).all())
    if not rows:
        return []
    daily = [(date.fromisoformat(str(day)), int(qty)) for day, qty in rows]
    first_day = daily[0][0]
    buckets = {}
    for day, qty in daily:
        week = (day - first_day).days // 7
        buckets[week] = buckets.get(week, 0) + qty
    return [buckets.get(i, 0) for i in range(max(buckets) + 1)]

def forecast_product(product_id):
    values = weekly_sales(product_id)
    if not values:
        return 0, "insufficient data", None
    if len(values) < 3:
        return max(0, int(round(float(np.mean(values))))), "historical average (limited data)", None
    x = np.arange(len(values)).reshape(-1, 1)
    y = np.array(values, dtype=float)
    # Hold out the latest observation for a simple historical error estimate.
    validation_model = LinearRegression().fit(x[:-1], y[:-1])
    validation_prediction = max(0, float(validation_model.predict(x[-1:])[0]))
    error = abs(y[-1] - validation_prediction) / y[-1] * 100 if y[-1] else None
    model = LinearRegression().fit(x, y)
    next_week = max(0, int(round(float(model.predict([[len(values)]])[0]))))
    return next_week, "linear trend", round(error, 2) if error is not None else None
