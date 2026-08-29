"""
data_loader.py
--------------
Loads the raw sheets from the store sales Excel workbook.

Schema note (v2): the fact sheet ("Sheet3") now ships 11 columns instead
of 10 - a "Profit" column was added after the workbook was rebuilt in
Power BI, and the raw headers changed slightly ("Product ID" instead of
"ProductID", "Discount" instead of "Discount Value"). The rename below
is purely positional, so it is robust to those header-text changes, but
it WILL break if columns are re-ordered or a column is added/removed.
If load_data() raises a length-mismatch error, check the sheet's raw
headers against FACT_COLUMNS below.
"""

import pandas as pd

# Standardized internal names for the 11 raw fact-table columns, in the
# exact order they appear in "Sheet3" as of the v2 workbook.
FACT_COLUMNS = [
    "Date", "CustomerID", "PromotionID", "ProductID", "UnitsSold",
    "PricePerUnit", "TotalSales", "DiscountPct", "DiscountValue",
    "NetSales", "Profit",
]


def load_data(filepath: str) -> dict:
    """
    Load all four sheets of the store data workbook.

    Parameters
    ----------
    filepath : str
        Path to the .xlsx workbook.

    Returns
    -------
    dict with keys: 'fact', 'customers', 'products', 'promotions'
    """
    fact = pd.read_excel(filepath, sheet_name="Sheet3")
    if len(fact.columns) != len(FACT_COLUMNS):
        raise ValueError(
            f"Expected {len(FACT_COLUMNS)} columns in 'Sheet3', found "
            f"{len(fact.columns)}: {list(fact.columns)}. The workbook "
            "schema may have changed - update FACT_COLUMNS in data_loader.py."
        )
    fact.columns = FACT_COLUMNS

    customers = pd.read_excel(filepath, sheet_name="Dim Customers")
    products = pd.read_excel(filepath, sheet_name="Dim Product")
    # NOTE: the source sheet name has a trailing space
    promotions = pd.read_excel(filepath, sheet_name="Dim Promotion ")

    return {
        "fact": fact,
        "customers": customers,
        "products": products,
        "promotions": promotions,
    }
