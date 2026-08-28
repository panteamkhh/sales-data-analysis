"""
data_loader.py
--------------
Loads the raw sheets from the store sales Excel workbook.
"""

import pandas as pd


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
    fact.columns = [
        "Date", "CustomerID", "PromotionID", "ProductID", "UnitsSold",
        "PricePerUnit", "TotalSales", "DiscountPct", "DiscountValue", "NetSales",
    ]

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
