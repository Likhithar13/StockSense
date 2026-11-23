from datetime import date, datetime, timedelta
from app import db
from models import Product, Sale

def seed_demo_data():
    if Product.query.first():
        return
    demo = [
        ("Rice 5kg", "Groceries", 420, 22, 10, [40,45,50,48,55,60,58,65]),
        ("Milk 1L", "Dairy", 58, 8, 12, [72,75,78,80,82,85,87,90]),
        ("Biscuits", "Snacks", 25, 35, 10, [30,32,31,35,36,38,40,42]),
        ("Cooking Oil 1L", "Groceries", 145, 14, 8, [18,20,19,22,23,25,24,27]),
        ("Tea 250g", "Beverages", 110, 18, 7, [12,13,14,13,15,16,17,18]),
    ]
    for name, category, price, stock, level, weekly in demo:
        product = Product(name=name, category=category, price=price,
                          quantity=stock, reorder_level=level)
        db.session.add(product)
        db.session.flush()
        for index, quantity in enumerate(weekly):
            sold_day = date.today() - timedelta(days=7 * (7 - index) + 1)
            db.session.add(Sale(product_id=product.id, quantity=quantity,
                                sold_at=datetime.combine(sold_day, datetime.min.time())))
    db.session.commit()
