"""
storage.py
----------
Handles all file/data-persistence operations for the Inventory
Management System. Data is stored locally as JSON files so that
information survives between program runs.
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")
SALES_FILE = os.path.join(DATA_DIR, "sales.json")


def _ensure_data_dir():
    """Make sure the data directory exists before reading/writing files."""
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_json(file_path, default):
    """Generic helper to safely load JSON data from a file."""
    _ensure_data_dir()
    if not os.path.exists(file_path):
        return default
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return default
            return json.loads(content)
    except (json.JSONDecodeError, OSError) as e:
        print(f"[Warning] Could not read '{file_path}' ({e}). Starting with empty data.")
        return default


def _save_json(file_path, data):
    """Generic helper to safely save JSON data to a file."""
    _ensure_data_dir()
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True
    except OSError as e:
        print(f"[Error] Could not write to '{file_path}': {e}")
        return False


def load_products():
    """Load product records as a list of dictionaries."""
    return _load_json(PRODUCTS_FILE, [])


def save_products(products):
    """Save a list of product dictionaries to products.json."""
    return _save_json(PRODUCTS_FILE, products)


def load_sales():
    """Load sales records as a list of dictionaries."""
    return _load_json(SALES_FILE, [])


def save_sales(sales):
    """Save a list of sales dictionaries to sales.json."""
    return _save_json(SALES_FILE, sales)
