"""
main.py
-------
Entry point for the Inventory Management System.

Run this file to start the menu-driven console application:
    python main.py
"""

from inventory import InventoryManager
from sales import SalesManager
import reports
from utils import (
    input_nonempty,
    input_float,
    input_int,
    input_menu_choice,
    LOW_STOCK_THRESHOLD,
)

MENU_TEXT = """
========== INVENTORY MANAGEMENT SYSTEM ==========
1. Add Product
2. View Products
3. Search Product
4. Update Product
5. Delete Product
6. Add Stock
7. Record Sale
8. Inventory Report
9. Sales Report
10. Low Stock Alert
11. Exit
===================================================
"""


def handle_add_product(inv):
    print("\n--- Add New Product ---")
    product_id = input_nonempty("Product ID: ")
    name = input_nonempty("Product Name: ")
    category = input_nonempty("Category: ")
    price = input_float("Price: ")
    quantity = input_int("Quantity Available: ")
    supplier = input_nonempty("Supplier Name: ")

    success, message = inv.add_product(product_id, name, category, price, quantity, supplier)
    print(("[OK] " if success else "[Error] ") + message)


def handle_view_products(inv):
    print("\n--- Product Inventory ---")
    inv.display_products()


def handle_search_product(inv):
    print("\n--- Search Product ---")
    term = input_nonempty("Enter Product ID or Product Name: ")
    results = inv.search_product(term)
    if results:
        inv.display_products(results)
    else:
        print(f"[Info] No products found matching '{term}'.")


def handle_update_product(inv):
    print("\n--- Update Product ---")
    product_id = input_nonempty("Enter Product ID to update: ")
    if not inv._find_by_id(product_id):
        print(f"[Error] Product ID '{product_id}' not found.")
        return

    print("Leave a field blank to keep its current value.")
    name = input("New Product Name: ").strip()
    category = input("New Category: ").strip()
    price_raw = input("New Price: ").strip()
    quantity_raw = input("New Quantity: ").strip()

    price = None
    quantity = None
    try:
        if price_raw:
            price = float(price_raw)
        if quantity_raw:
            quantity = int(quantity_raw)
    except ValueError:
        print("[Error] Price/Quantity must be valid numbers. Update cancelled.")
        return

    success, message = inv.update_product(
        product_id,
        name=name or None,
        price=price,
        quantity=quantity,
        category=category or None,
    )
    print(("[OK] " if success else "[Error] ") + message)


def handle_delete_product(inv):
    print("\n--- Delete Product ---")
    product_id = input_nonempty("Enter Product ID to delete: ")
    confirm = input(f"Are you sure you want to delete '{product_id}'? (y/n): ").strip().lower()
    if confirm != "y":
        print("[Info] Deletion cancelled.")
        return
    success, message = inv.delete_product(product_id)
    print(("[OK] " if success else "[Error] ") + message)


def handle_add_stock(inv):
    print("\n--- Add Stock ---")
    product_id = input_nonempty("Enter Product ID: ")
    amount = input_int("Enter quantity to add: ")
    success, message = inv.add_stock(product_id, amount)
    print(("[OK] " if success else "[Error] ") + message)


def handle_record_sale(inv, sales_mgr):
    print("\n--- Record Sale ---")
    product_id = input_nonempty("Enter Product ID: ")
    quantity = input_int("Enter Quantity Sold: ")
    success, message = sales_mgr.record_sale(product_id, quantity)
    print(("[OK] " if success else "[Error] ") + message)


def handle_low_stock_alert(inv):
    print(f"\n--- Low Stock Alert (below {LOW_STOCK_THRESHOLD} units) ---")
    low_stock = inv.low_stock_alert()
    if low_stock:
        inv.display_products(low_stock)
    else:
        print("[Info] All products are sufficiently stocked.")


def main():
    inv = InventoryManager()
    sales_mgr = SalesManager(inv)

    actions = {
        "1": lambda: handle_add_product(inv),
        "2": lambda: handle_view_products(inv),
        "3": lambda: handle_search_product(inv),
        "4": lambda: handle_update_product(inv),
        "5": lambda: handle_delete_product(inv),
        "6": lambda: handle_add_stock(inv),
        "7": lambda: handle_record_sale(inv, sales_mgr),
        "8": lambda: reports.inventory_report(inv),
        "9": lambda: reports.sales_report(sales_mgr),
        "10": lambda: handle_low_stock_alert(inv),
    }

    print("Welcome to the Inventory Management System!")

    while True:
        print(MENU_TEXT)
        choice = input_menu_choice(
            "Enter your choice (1-11): ",
            [str(i) for i in range(1, 12)],
        )

        if choice == "11":
            print("Exiting Inventory Management System. Goodbye!")
            break

        try:
            actions[choice]()
        except Exception as e:
            # Catch-all safety net so an unexpected error never crashes the app.
            print(f"[Error] Something went wrong: {e}")


if __name__ == "__main__":
    main()
