import pandas as pd


def load_data(filepath: str) -> dict:
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
