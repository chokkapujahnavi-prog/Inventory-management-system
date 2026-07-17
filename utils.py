"""
utils.py
--------
Small shared helper functions: input validation and console table
printing. Kept dependency-free (no pandas/tabulate required) so the
project runs on a bare Python 3 install, but works fine alongside
those libraries if the user has them.
"""

LOW_STOCK_THRESHOLD = 10


def print_table(headers, rows):
    """Print a simple, aligned text table -- no external libraries needed."""
    if not rows:
        print("(no records to display)")
        return

    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    def format_row(row):
        return " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))

    separator = "-+-".join("-" * w for w in col_widths)

    print(format_row(headers))
    print(separator)
    for row in rows:
        print(format_row(row))


def input_nonempty(prompt):
    """Prompt until the user provides a non-empty string."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("[Error] This field cannot be empty. Please try again.")


def input_float(prompt, allow_negative=False):
    """Prompt for a valid float value (e.g. price)."""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if not allow_negative and value < 0:
                print("[Error] Value cannot be negative. Please try again.")
                continue
            return value
        except ValueError:
            print("[Error] Please enter a valid number (e.g. 199.99).")


def input_int(prompt, allow_negative=False):
    """Prompt for a valid integer value (e.g. quantity)."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if not allow_negative and value < 0:
                print("[Error] Value cannot be negative. Please try again.")
                continue
            return value
        except ValueError:
            print("[Error] Please enter a valid whole number (e.g. 25).")


def input_menu_choice(prompt, valid_choices):
    """Prompt until the user enters one of the valid menu choices."""
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print(f"[Error] Invalid choice. Please select one of: {', '.join(valid_choices)}")
