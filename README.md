# Inventory Management System

An **Inventory Management System** built in Python as part of a Python
Development Internship project. It helps businesses manage products, stock
levels, sales records, and inventory updates. It ships in two forms that
share the same underlying logic:

- a **console app** (`main.py`) — the original menu-driven interface, and
- a **web app** (`app.py`) — a Flask front-end over the same data, deployable
  to a platform like Render.

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

- **Python 3.x**
- `json` — data persistence
- `os` — file/directory handling
- `datetime` — timestamping sales records
- **Flask** — powers the optional web interface (`app.py`)
- **gunicorn** — production WSGI server used to run the web interface when deployed

The console app (`main.py`) uses only the Python standard library — no
installation required, and a lightweight built-in table printer is used
instead of `pandas`/`tabulate` so it works out of the box. Flask and
gunicorn are only needed if you run the web version.

## Project Structure

```
inventory_management_system/
│
├── main.py          # Console entry point (menu-driven interface)
├── app.py           # Web entry point (Flask app, same logic underneath)
├── models.py         # Product data structure (OOP class)
├── inventory.py       # Product Management + Stock Management modules
├── sales.py          # Sales Management module
├── reports.py         # Inventory Report + Sales Report module (console)
├── storage.py         # JSON file read/write (persistence layer)
├── utils.py           # Shared helpers: table printing, input validation
├── requirements.txt    # Flask + gunicorn (needed for the web app)
├── Procfile            # Tells Render/Heroku how to start the web app
├── templates/          # HTML templates for the web app (Jinja2)
├── static/style.css     # Stylesheet for the web app
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

### Running the Web Version Locally

1. Install the extra dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the Flask dev server:
   ```bash
   python3 app.py
   ```
3. Open **http://127.0.0.1:5000** in your browser.

### Deploying the Web Version to Render

1. Push this whole folder (including `requirements.txt`, `Procfile`, `app.py`,
   `templates/`, and `static/`) to a GitHub repository.
2. In Render, create a **new Web Service** from that repo.
3. Render will detect `requirements.txt` automatically for the build step
   (`pip install -r requirements.txt`).
4. Set the **Start Command** to:
   ```
   gunicorn app:app
   ```
   (This is also what the included `Procfile` specifies, so Render may
   pick it up automatically.)
5. Leave the **Root Directory** as the folder containing `app.py` if you
   didn't put the project at the repo root.
6. Deploy. Render assigns the app a public URL once the build succeeds.

**Note on storage**: the web app persists data to `data/products.json` and
`data/sales.json` on disk, same as the console app. Most PaaS platforms
(including Render's free tier) use an **ephemeral filesystem** — files
written while the app is running are lost on redeploy or restart. For a
real production deployment, swap `storage.py` for a proper database, or
attach a persistent disk if your platform supports one.

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
