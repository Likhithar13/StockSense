
import os
import json
from pathlib import Path

import requests
from dotenv import load_dotenv

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify
)

from sqlalchemy import func, update
from sqlalchemy.exc import IntegrityError

from extensions import db
from models import Product, Sale


# Load environment variables from .env
load_dotenv()

PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")


# --------------------------------------------------
# PRODUCT IMAGE SERVICE
# --------------------------------------------------

def get_product_images(products, app):
    image_folder = Path(app.static_folder) / "product_images"
    image_folder.mkdir(parents=True, exist_ok=True)

    product_images = {}

    for product in products:
        image_file = image_folder / f"{product.id}.jpg"
        info_file = image_folder / f"{product.id}.json"

        # Reuse previously downloaded image
        if image_file.exists() and info_file.exists():
            try:
                info = json.loads(
                    info_file.read_text(encoding="utf-8")
                )

                product_images[product.id] = {
                    "image": f"product_images/{product.id}.jpg",
                    "source": info.get(
                        "source",
                        "https://pixabay.com/"
                    )
                }
                continue

            except (ValueError, OSError):
                pass

        if not PIXABAY_API_KEY:
            continue

        try:
            response = requests.get(
                "https://pixabay.com/api/",
                params={
                    "key": PIXABAY_API_KEY,
                    "q": (
    f"computer {product.name}"
    if product.name.lower() in ["mouse", "keyboard"]
    else f"{product.name} {product.category}"
),
                    "image_type": "photo",
                    "safesearch": "true",
                    "per_page": 3
                },
                timeout=15
            )

            response.raise_for_status()

            hits = response.json().get("hits", [])

            if not hits:
                continue

            image_url = hits[0].get("webformatURL")
            source_url = hits[0].get(
                "pageURL",
                "https://pixabay.com/"
            )

            if not image_url:
                continue

            image_response = requests.get(
                image_url,
                timeout=20
            )

            image_response.raise_for_status()

            content_type = image_response.headers.get(
                "Content-Type", ""
            )

            if not content_type.startswith("image/"):
                continue

            image_file.write_bytes(image_response.content)

            info_file.write_text(
                json.dumps({"source": source_url}),
                encoding="utf-8"
            )

            product_images[product.id] = {
                "image": f"product_images/{product.id}.jpg",
                "source": source_url
            }

        except (
            requests.RequestException,
            ValueError,
            OSError
        ) as error:
            print(
                f"Image lookup failed for {product.name}: {error}"
            )

    return product_images


# --------------------------------------------------
# APPLICATION
# --------------------------------------------------

def create_app(test_config=None):

    app = Flask(__name__)

    app.config.update(
        SECRET_KEY=os.getenv(
            "SECRET_KEY",
            "change-this-in-production"
        ),
        SQLALCHEMY_DATABASE_URI=os.getenv(
            "DATABASE_URL",
            "sqlite:///stocksense.db"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    # --------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------

    @app.get("/")
    def dashboard():

        products = Product.query.order_by(
            Product.name
        ).all()

        low_stock = Product.query.filter(
            Product.quantity <= Product.reorder_level
        ).all()

        units = db.session.query(
            func.coalesce(func.sum(Product.quantity), 0)
        ).scalar()

        sold = db.session.query(
            func.coalesce(func.sum(Sale.quantity), 0)
        ).scalar()

        recent = Sale.query.order_by(
            Sale.sold_at.desc()
        ).limit(8).all()

        return render_template(
            "dashboard.html",
            products=products,
            low_stock=low_stock,
            units=units,
            sold=sold,
            recent=recent
        )

    # --------------------------------------------------
    # PRODUCTS
    # --------------------------------------------------

    @app.route("/products", methods=["GET", "POST"])
    def products():

        if request.method == "POST":

            try:
                name = request.form["name"].strip()
                price = float(request.form["price"])
                quantity = int(request.form["quantity"])

                reorder_level = int(
                    request.form.get("reorder_level", 5)
                )

                if (
                    not name
                    or price < 0
                    or quantity < 0
                    or reorder_level < 0
                ):
                    raise ValueError

                product = Product(
                    name=name,
                    category=request.form.get(
                        "category", ""
                    ).strip(),
                    price=price,
                    quantity=quantity,
                    reorder_level=reorder_level
                )

                db.session.add(product)
                db.session.commit()

                flash(
                    "Product added successfully.",
                    "success"
                )

            except (
                ValueError,
                KeyError,
                IntegrityError
            ):
                db.session.rollback()

                flash(
                    "Invalid values or product name already exists.",
                    "danger"
                )

            return redirect(url_for("products"))

        product_list = Product.query.order_by(
            Product.name
        ).all()

        product_images = get_product_images(
            product_list,
            app
        )

        return render_template(
            "products.html",
            products=product_list,
            product_images=product_images
        )

    # --------------------------------------------------
    # UPDATE PRODUCT
    # --------------------------------------------------

    @app.post("/products/<int:product_id>/update")
    def update_product(product_id):

        product = db.get_or_404(Product, product_id)

        try:
            name = request.form["name"].strip()
            price = float(request.form["price"])
            quantity = int(request.form["quantity"])

            level = int(
                request.form["reorder_level"]
            )

            if (
                not name
                or min(price, quantity, level) < 0
            ):
                raise ValueError

            product.name = name

            product.category = request.form.get(
                "category", ""
            ).strip()

            product.price = price
            product.quantity = quantity
            product.reorder_level = level

            db.session.commit()

            flash(
                "Product updated successfully.",
                "success"
            )

        except (
            ValueError,
            KeyError,
            IntegrityError
        ):
            db.session.rollback()

            flash(
                "Invalid details or duplicate product name.",
                "danger"
            )

        return redirect(url_for("products"))

    # --------------------------------------------------
    # DELETE PRODUCT
    # --------------------------------------------------

    @app.post("/products/<int:product_id>/delete")
    def delete_product(product_id):

        product = db.get_or_404(Product, product_id)

        db.session.delete(product)
        db.session.commit()

        # Remove cached image files
        image_folder = Path(app.static_folder) / "product_images"

        for extension in [".jpg", ".json"]:
            image_file = image_folder / (
                str(product_id) + extension
            )

            if image_file.exists():
                image_file.unlink()

        flash(
            "Product deleted successfully.",
            "success"
        )

        return redirect(url_for("products"))

    # --------------------------------------------------
    # SALES
    # --------------------------------------------------

    @app.route("/sales", methods=["GET", "POST"])
    def sales():

        if request.method == "POST":

            try:
                product_id = int(
                    request.form["product_id"]
                )

                quantity = int(
                    request.form["quantity"]
                )

            except (ValueError, KeyError):

                flash(
                    "Choose a product and enter a valid quantity.",
                    "danger"
                )

                return redirect(url_for("sales"))

            if quantity <= 0:

                flash(
                    "Sale quantity must be greater than zero.",
                    "danger"
                )

                return redirect(url_for("sales"))

            result = db.session.execute(
                update(Product)
                .where(
                    Product.id == product_id,
                    Product.quantity >= quantity
                )
                .values(
                    quantity=Product.quantity - quantity
                )
            )

            if result.rowcount != 1:

                db.session.rollback()

                flash(
                    "Sale rejected: product not found or insufficient stock.",
                    "danger"
                )

            else:

                db.session.add(
                    Sale(
                        product_id=product_id,
                        quantity=quantity
                    )
                )

                db.session.commit()

                flash(
                    "Sale recorded and stock updated successfully.",
                    "success"
                )

            return redirect(url_for("sales"))

        product_list = Product.query.filter(
            Product.quantity > 0
        ).order_by(Product.name).all()

        sales_list = Sale.query.order_by(
            Sale.sold_at.desc()
        ).limit(30).all()

        return render_template(
            "sales.html",
            products=product_list,
            sales=sales_list
        )

    # --------------------------------------------------
    # FORECAST
    # --------------------------------------------------

    @app.get("/forecast")
    def forecast():

        from services.forecasting import forecast_product
        from services.reorder import calculate_reorder

        rows = []

        for product in Product.query.order_by(
            Product.name
        ).all():

            demand, method, error = forecast_product(
                product.id
            )

            suggested_order = calculate_reorder(
                product.quantity,
                demand,
                product.reorder_level
            )

            rows.append({
                "product": product,
                "demand": demand,
                "method": method,
                "error": error,
                "suggested_order": suggested_order
            })

        return render_template(
            "forecast.html",
            rows=rows
        )

    # --------------------------------------------------
    # HEALTH CHECK
    # --------------------------------------------------

    @app.get("/health")
    def health():

        return jsonify(
            status="ok",
            service="StockSense"
        )

    # --------------------------------------------------
    # SEED DATA
    # --------------------------------------------------

    @app.cli.command("seed")
    def seed():

        from seed import seed_demo_data

        seed_demo_data()

        print("Demo data ready.")

    return app


# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------

app = create_app()

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
