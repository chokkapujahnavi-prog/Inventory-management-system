"""
models.py
---------
Defines the Product data structure used throughout the Inventory
Management System.
"""


class Product:
    """Represents a single product in the inventory."""

    def __init__(self, product_id, name, category, price, quantity, supplier):
        self.product_id = str(product_id).strip()
        self.name = str(name).strip()
        self.category = str(category).strip()
        self.price = float(price)
        self.quantity = int(quantity)
        self.supplier = str(supplier).strip()

    def to_dict(self):
        """Convert the Product object into a plain dictionary (for JSON storage)."""
        return {
            "product_id": self.product_id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "quantity": self.quantity,
            "supplier": self.supplier,
        }

    @staticmethod
    def from_dict(data):
        """Create a Product object from a dictionary (loaded from JSON)."""
        return Product(
            product_id=data["product_id"],
            name=data["name"],
            category=data["category"],
            price=data["price"],
            quantity=data["quantity"],
            supplier=data["supplier"],
        )

    def as_row(self):
        """Return a list of values used for tabular display."""
        return [
            self.product_id,
            self.name,
            self.category,
            f"{self.price:.2f}",
            self.quantity,
            self.supplier,
        ]
