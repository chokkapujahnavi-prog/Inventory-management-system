"""
sales.py
--------
Sales Management Module.

Handles recording sales transactions (which also reduce stock via the
InventoryManager) and producing a sales summary.
"""

from datetime import datetime
import storage
from utils import print_table


class SalesManager:
    def __init__(self, inventory_manager):
        # SalesManager depends on InventoryManager to validate stock
        # and to update quantities when a sale is recorded.
        self.inventory_manager = inventory_manager
        self.sales = storage.load_sales()

    def _persist(self):
        storage.save_sales(self.sales)

    def record_sale(self, product_id, quantity_sold):
        """
        Record a sale for a given product ID and quantity.
        Reduces stock automatically and calculates the total sale amount.
        Returns (success, message).
        """
        if quantity_sold <= 0:
            return False, "Quantity sold must be a positive number."

        product = self.inventory_manager._find_by_id(product_id)
        if not product:
            return False, f"Product ID '{product_id}' not found."

        success, message = self.inventory_manager.reduce_stock(product_id, quantity_sold)
        if not success:
            return False, message

        total_amount = round(product.price * quantity_sold, 2)
        sale_record = {
            "sale_id": len(self.sales) + 1,
            "product_id": product.product_id,
            "product_name": product.name,
            "quantity_sold": quantity_sold,
            "unit_price": product.price,
            "total_amount": total_amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.sales.append(sale_record)
        self._persist()

        return True, (
            f"Sale recorded: {quantity_sold} x '{product.name}' "
            f"for a total of {total_amount:.2f}."
        )

    def display_sales(self):
        headers = ["Sale ID", "Product ID", "Product Name", "Qty Sold", "Unit Price", "Total", "Date"]
        rows = [
            [s["sale_id"], s["product_id"], s["product_name"], s["quantity_sold"],
             f"{s['unit_price']:.2f}", f"{s['total_amount']:.2f}", s["date"]]
            for s in self.sales
        ]
        print_table(headers, rows)

    def sales_summary(self):
        """Return a dict summarizing total quantity sold and total revenue."""
        total_quantity = sum(s["quantity_sold"] for s in self.sales)
        total_revenue = sum(s["total_amount"] for s in self.sales)
        return {
            "total_products_sold": total_quantity,
            "total_revenue": round(total_revenue, 2),
        }

    def most_sold_product(self):
        """Return (product_name, total_quantity) for the best-selling product, or None."""
        if not self.sales:
            return None

        totals = {}
        for s in self.sales:
            key = (s["product_id"], s["product_name"])
            totals[key] = totals.get(key, 0) + s["quantity_sold"]

        best_key = max(totals, key=totals.get)
        return best_key[1], totals[best_key]
