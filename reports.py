"""
reports.py
----------
Reporting Module.

Generates the Inventory Report and Sales Report shown from the main menu.
"""


def inventory_report(inventory_manager):
    """Print a summary report of the current inventory."""
    products = inventory_manager.view_products()
    total_products = len(products)
    categories = {p.category for p in products}
    total_stock = sum(p.quantity for p in products)

    print("\n===== INVENTORY REPORT =====")
    print(f"Total Products     : {total_products}")
    print(f"Total Categories   : {len(categories)}")
    print(f"Available Stock    : {total_stock} units")
    print("=============================\n")


def sales_report(sales_manager):
    """Print a summary report of sales activity."""
    summary = sales_manager.sales_summary()
    best = sales_manager.most_sold_product()

    print("\n======= SALES REPORT =======")
    print(f"Total Products Sold : {summary['total_products_sold']}")
    print(f"Revenue Generated   : {summary['total_revenue']:.2f}")
    if best:
        print(f"Most Sold Product   : {best[0]} ({best[1]} units)")
    else:
        print("Most Sold Product   : N/A (no sales recorded yet)")
    print("=============================\n")
