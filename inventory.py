"""
inventory.py
------------
Product Management Module + Stock Management Module.

Contains the InventoryManager class responsible for adding, viewing,
searching, updating, and deleting products, as well as adjusting
stock levels and raising low-stock alerts.
"""

import storage
from models import Product
from utils import print_table, LOW_STOCK_THRESHOLD


class InventoryManager:
    def __init__(self):
        # Load existing products from disk into memory as Product objects.
        raw_products = storage.load_products()
        self.products = [Product.from_dict(p) for p in raw_products]

    # ---------- internal helpers ----------
    def _persist(self):
        """Save the current in-memory product list back to disk."""
        storage.save_products([p.to_dict() for p in self.products])

    def _find_by_id(self, product_id):
        product_id = str(product_id).strip()
        for p in self.products:
            if p.product_id == product_id:
                return p
        return None

    # ---------- Product Management ----------
    def add_product(self, product_id, name, category, price, quantity, supplier):
        """Add a new product. Returns (success, message)."""
        if self._find_by_id(product_id):
            return False, f"Product ID '{product_id}' already exists. Use a unique ID."

        try:
            product = Product(product_id, name, category, price, quantity, supplier)
        except (ValueError, TypeError) as e:
            return False, f"Invalid product data: {e}"

        if product.price < 0:
            return False, "Price cannot be negative."
        if product.quantity < 0:
            return False, "Quantity cannot be negative."

        self.products.append(product)
        self._persist()
        return True, f"Product '{product.name}' added successfully."

    def view_products(self):
        """Return all products for display."""
        return self.products

    def search_product(self, term):
        """Search by Product ID (exact match) or Product Name (partial, case-insensitive)."""
        term_lower = str(term).strip().lower()
        results = [
            p for p in self.products
            if p.product_id.lower() == term_lower or term_lower in p.name.lower()
        ]
        return results

    def update_product(self, product_id, name=None, price=None, quantity=None, category=None):
        """Update selected fields of a product. Returns (success, message)."""
        product = self._find_by_id(product_id)
        if not product:
            return False, f"Product ID '{product_id}' not found."

        if name is not None and name.strip():
            product.name = name.strip()
        if category is not None and category.strip():
            product.category = category.strip()
        if price is not None:
            if price < 0:
                return False, "Price cannot be negative."
            product.price = float(price)
        if quantity is not None:
            if quantity < 0:
                return False, "Quantity cannot be negative."
            product.quantity = int(quantity)

        self._persist()
        return True, f"Product '{product.product_id}' updated successfully."

    def delete_product(self, product_id):
        """Delete a product by ID. Returns (success, message)."""
        product = self._find_by_id(product_id)
        if not product:
            return False, f"Product ID '{product_id}' not found."

        self.products.remove(product)
        self._persist()
        return True, f"Product '{product_id}' deleted successfully."

    # ---------- Stock Management ----------
    def add_stock(self, product_id, amount):
        """Increase inventory quantity for a product."""
        product = self._find_by_id(product_id)
        if not product:
            return False, f"Product ID '{product_id}' not found."
        if amount <= 0:
            return False, "Stock amount to add must be a positive number."

        product.quantity += amount
        self._persist()
        return True, f"Added {amount} units to '{product.name}'. New quantity: {product.quantity}."

    def reduce_stock(self, product_id, amount):
        """Reduce inventory quantity (used internally by sales, or manually)."""
        product = self._find_by_id(product_id)
        if not product:
            return False, f"Product ID '{product_id}' not found."
        if amount <= 0:
            return False, "Stock amount to reduce must be a positive number."
        if amount > product.quantity:
            return False, (
                f"Insufficient stock for '{product.name}'. "
                f"Available: {product.quantity}, requested: {amount}."
            )

        product.quantity -= amount
        self._persist()
        return True, f"Reduced {amount} units from '{product.name}'. New quantity: {product.quantity}."

    def low_stock_alert(self, threshold=LOW_STOCK_THRESHOLD):
        """Return products whose quantity is below the given threshold."""
        return [p for p in self.products if p.quantity < threshold]

    # ---------- Display helper ----------
    def display_products(self, products=None):
        headers = ["Product ID", "Name", "Category", "Price", "Quantity", "Supplier"]
        products = self.products if products is None else products
        rows = [p.as_row() for p in products]
        print_table(headers, rows)
