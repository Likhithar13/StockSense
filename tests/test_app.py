from models import Product, Sale
from app import db

def test_dashboard_and_health(client):
    assert client.get("/").status_code == 200
    assert client.get("/health").json["status"] == "ok"

def test_add_product(client, app):
    response = client.post("/products", data={"name":"Test item","category":"Test",
        "price":"10","quantity":"5","reorder_level":"2"}, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert Product.query.filter_by(name="Test item").first() is not None

def test_sale_decrements_stock(client, app):
    with app.app_context():
        p = Product(name="Widget", price=5, quantity=4, reorder_level=1)
        db.session.add(p); db.session.commit(); pid = p.id
    response = client.post("/sales", data={"product_id":str(pid),"quantity":"3"}, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert db.session.get(Product, pid).quantity == 1
        assert Sale.query.filter_by(product_id=pid).count() == 1

def test_sale_cannot_make_stock_negative(client, app):
    with app.app_context():
        p = Product(name="Limited", price=5, quantity=2, reorder_level=1)
        db.session.add(p); db.session.commit(); pid = p.id
    client.post("/sales", data={"product_id":str(pid),"quantity":"3"}, follow_redirects=True)
    with app.app_context():
        assert db.session.get(Product, pid).quantity == 2
        assert Sale.query.filter_by(product_id=pid).count() == 0
