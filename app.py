"""
app.py
------
Flask web front-end for the Inventory Management System.

This reuses the same business logic as the console app (models.py,
inventory.py, sales.py, reports.py, storage.py) -- only the interface
changes, from a menu loop to HTTP routes + HTML templates.

Run locally:
    python app.py            # dev server on http://127.0.0.1:5000

Deploy (e.g. Render):
    gunicorn app:app
"""

import os

from flask import Flask, render_template, request, redirect, url_for, flash

from inventory import InventoryManager
from sales import SalesManager
from utils import LOW_STOCK_THRESHOLD

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

# Single shared instance for the life of the process. Data is persisted
# to data/products.json and data/sales.json on every write, so it
# survives restarts. Note: this file-based storage is fine for a single
# worker; it isn't a substitute for a real database under concurrent load.
inventory = InventoryManager()
sales_mgr = SalesManager(inventory)


# ---------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------
@app.route("/")
def dashboard():
    products = inventory.view_products()
    low_stock = inventory.low_stock_alert()
    summary = sales_mgr.sales_summary()
    recent_sales = sales_mgr.sales[-5:]

    return render_template(
        "dashboard.html",
        active="dashboard",
        total_products=len(products),
        total_stock=sum(p.quantity for p in products),
        low_stock_count=len(low_stock),
        low_stock=low_stock,
        threshold=LOW_STOCK_THRESHOLD,
        total_revenue=summary["total_revenue"],
        recent_sales=list(reversed(recent_sales)),
    )


# ---------------------------------------------------------------------
# Product Management
# ---------------------------------------------------------------------
@app.route("/products")
def list_products():
    query = request.args.get("q", "").strip()
    products = inventory.search_product(query) if query else inventory.view_products()
    return render_template(
        "products.html",
        active="products",
        products=products,
        query=query,
        threshold=LOW_STOCK_THRESHOLD,
    )


@app.route("/products/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        form = request.form
        try:
            price = float(form.get("price", ""))
            quantity = int(form.get("quantity", ""))
        except ValueError:
            flash("Price must be a number and quantity must be a whole number.", "error")
            return render_template("add_product.html", active="products", form=form)

        success, message = inventory.add_product(
            product_id=form.get("product_id", ""),
            name=form.get("name", ""),
            category=form.get("category", ""),
            price=price,
            quantity=quantity,
            supplier=form.get("supplier", ""),
        )
        flash(message, "ok" if success else "error")
        if success:
            return redirect(url_for("list_products"))
        return render_template("add_product.html", active="products", form=form)

    return render_template("add_product.html", active="products", form=None)


@app.route("/products/<product_id>/update", methods=["GET", "POST"])
def update_product(product_id):
    product = inventory._find_by_id(product_id)
    if not product:
        flash(f"Product ID '{product_id}' not found.", "error")
        return redirect(url_for("list_products"))

    if request.method == "POST":
        form = request.form
        try:
            price = float(form["price"]) if form.get("price") else None
            quantity = int(form["quantity"]) if form.get("quantity") else None
        except ValueError:
            flash("Price must be a number and quantity must be a whole number.", "error")
            return render_template("update_product.html", active="products", product=product)

        success, message = inventory.update_product(
            product_id,
            name=form.get("name") or None,
            category=form.get("category") or None,
            price=price,
            quantity=quantity,
        )
        flash(message, "ok" if success else "error")
        return redirect(url_for("list_products"))

    return render_template("update_product.html", active="products", product=product)


@app.route("/products/<product_id>/delete", methods=["POST"])
def delete_product(product_id):
    success, message = inventory.delete_product(product_id)
    flash(message, "ok" if success else "error")
    return redirect(url_for("list_products"))


# ---------------------------------------------------------------------
# Stock Management
# ---------------------------------------------------------------------
@app.route("/products/<product_id>/add-stock", methods=["POST"])
def add_stock(product_id):
    try:
        amount = int(request.form.get("amount", ""))
    except ValueError:
        flash("Stock amount must be a whole number.", "error")
        return redirect(url_for("update_product", product_id=product_id))

    success, message = inventory.add_stock(product_id, amount)
    flash(message, "ok" if success else "error")
    return redirect(url_for("update_product", product_id=product_id))


# ---------------------------------------------------------------------
# Sales Management
# ---------------------------------------------------------------------
@app.route("/sales")
def list_sales():
    return render_template("sales.html", active="sales", sales=sales_mgr.sales)


@app.route("/sales/record", methods=["GET", "POST"])
def record_sale():
    if request.method == "POST":
        form = request.form
        try:
            quantity = int(form.get("quantity", ""))
        except ValueError:
            flash("Quantity sold must be a whole number.", "error")
            return render_template(
                "record_sale.html", active="sales",
                products=inventory.view_products(), form=form,
            )

        success, message = sales_mgr.record_sale(form.get("product_id", ""), quantity)
        flash(message, "ok" if success else "error")
        if success:
            return redirect(url_for("list_sales"))
        return render_template(
            "record_sale.html", active="sales",
            products=inventory.view_products(), form=form,
        )

    return render_template(
        "record_sale.html", active="sales",
        products=inventory.view_products(), form=None,
    )


# ---------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------
@app.route("/reports")
def reports_page():
    products = inventory.view_products()
    categories = {p.category for p in products}
    inv_summary = {
        "total_products": len(products),
        "total_categories": len(categories),
        "available_stock": sum(p.quantity for p in products),
    }

    sales_summary = sales_mgr.sales_summary()
    best = sales_mgr.most_sold_product()
    sales_summary["most_sold_name"] = best[0] if best else None
    sales_summary["most_sold_qty"] = best[1] if best else None

    return render_template(
        "reports.html", active="reports", inv=inv_summary, sales=sales_summary
    )


if __name__ == "__main__":
    # Local development server. In production, Render (or similar) runs:
    #   gunicorn app:app
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
