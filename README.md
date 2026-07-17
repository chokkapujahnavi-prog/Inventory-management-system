# Inventory Management System

A console-based **Inventory Management System** built in Python as part of a
Python Development Internship project. It helps businesses manage products,
stock levels, sales records, and inventory updates through a simple,
menu-driven interface.

## Project Overview

### Objective
Automate everyday inventory tasks — adding products, tracking stock,
recording sales, and generating reports — using core Python concepts:
object-oriented programming, file handling, and user interaction.

### Features
- **Product Management**: add, view, search (by ID or name), update, and
  delete products.
- **Stock Management**: add stock, reduce stock, and see a low-stock alert
  (default threshold: 10 units).
- **Sales Management**: record a sale (automatically reduces stock and
  calculates the total amount) and view a sales summary.
- **Reporting**: an Inventory Report (total products, categories, stock)
  and a Sales Report (total sold, revenue, best-selling product).
- **Data Persistence**: all data is stored locally in JSON files, so it
  survives between program runs.
- **Error Handling**: invalid input, duplicate product IDs, missing
  products, negative/insufficient stock, and file I/O errors are all
  handled with clear messages instead of crashing.

## Technologies Used

- **Python 3.x** (standard library only — no installation required)
- `json` — data persistence
- `os` — file/directory handling
- `datetime` — timestamping sales records

No third-party packages (like `pandas` or `tabulate`) are required to run
the project; a lightweight built-in table printer is used instead so the
project works out of the box on any machine with Python 3 installed.

## Project Structure

```
inventory_management_system/
│
├── main.py          # Menu-driven console interface (entry point)
├── models.py         # Product data structure (OOP class)
├── inventory.py       # Product Management + Stock Management modules
├── sales.py          # Sales Management module
├── reports.py         # Inventory Report + Sales Report module
├── storage.py         # JSON file read/write (persistence layer)
├── utils.py           # Shared helpers: table printing, input validation
├── README.md
└── data/
    ├── products.json  # Sample product records
    └── sales.json     # Sample sales records
```

Each module has a single responsibility, which keeps the code easy to
navigate and extend:

- `models.Product` — defines what a product *is*.
- `storage.py` — defines how data is *saved and loaded*.
- `inventory.InventoryManager` — defines product/stock *operations*.
- `sales.SalesManager` — defines sales *operations* (depends on
  `InventoryManager` to check and reduce stock).
- `reports.py` — turns the data in `InventoryManager`/`SalesManager` into
  human-readable summaries.
- `main.py` — wires everything together behind the console menu.

## How to Run

1. **Prerequisite**: Python 3.x installed (no other packages needed).
2. Open a terminal and navigate to the project folder:
   ```bash
   cd inventory_management_system
   ```
3. Run the application:
   ```bash
   python3 main.py
   ```
   (On Windows, use `python main.py`.)
4. Use the on-screen menu to interact with the system:
   ```
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
   ```
5. All changes are saved automatically to `data/products.json` and
   `data/sales.json` after every add/update/delete/sale, so you can close
   and reopen the program without losing data.

### Sample Data
The project ships with a few sample products (`P001`–`P004`) and two
sample sales records in the `data/` folder so you can explore the
features (e.g. option 8/9 for reports, or option 10 for the low-stock
alert) immediately without entering data manually. Feel free to delete
the contents of `data/products.json` and `data/sales.json` (replace with
`[]`) to start with a clean inventory.

## Sample Output

**Main Menu**
```
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
Enter your choice (1-11): 2
```

**View Products**
```
--- Product Inventory ---
Product ID | Name               | Category    | Price | Quantity | Supplier
-----------+--------------------+-------------+-------+----------+----------------
P001       | Wireless Mouse     | Electronics | 15.99 | 50       | TechSupply Co.
P002       | Bluetooth Keyboard | Electronics | 25.50 | 8        | TechSupply Co.
P003       | Notebook           | Stationery  | 2.75  | 120      | PaperWorks Ltd.
P004       | Ballpoint Pen      | Stationery  | 0.99  | 5        | PaperWorks Ltd.
```

**Recording a Sale**
```
--- Record Sale ---
Enter Product ID: P001
Enter Quantity Sold: 5
[OK] Sale recorded: 5 x 'Wireless Mouse' for a total of 79.95.
```

**Inventory Report**
```
===== INVENTORY REPORT =====
Total Products     : 4
Total Categories   : 2
Available Stock    : 183 units
=============================
```

**Sales Report**
```
======= SALES REPORT =======
Total Products Sold : 20
Revenue Generated   : 180.42
Most Sold Product   : Notebook (10 units)
=============================
```

*(Note: replace the text blocks above with actual terminal screenshots
before submitting, if screenshots are required by your program.)*

## Error Handling Highlights
- Adding a product with an existing ID is rejected.
- Selling or reducing more stock than is available is rejected.
- Negative prices/quantities are rejected at input time.
- Searching/updating/deleting a non-existent Product ID returns a clear
  "not found" message instead of crashing.
- Corrupted or missing JSON data files are handled gracefully (the app
  starts with empty data rather than crashing).
## Author
- Name : Ch Jahnavi
- College : Pragati Engineering College

## License
This project is based on educational and internship purpose
