"""
feature_engineering.py
-----------------------
Computes the columns that are missing from the raw fact table
(PricePerUnit, TotalSales, DiscountPct, DiscountValue, NetSales, Profit)
and builds the final denormalized "master" table used for analysis.

Assumptions (documented explicitly since the source data does not
provide these values directly):

1. PricePerUnit is looked up from Dim Product.
2. DiscountPct is parsed from Dim Promotion's "Price Reduction Type"
   text field (e.g. "20% off" -> 0.20). Orders with no promotion get 0%.
   The one non-percentage promotion, "Buy 1 Get 1 Free", is treated as
   an effective 50% discount (1 of 2 units is free).
3. Profit is not present in the source data (no Cost column), so it is
   estimated using a configurable flat margin on Net Sales
   (default PROFIT_MARGIN = 0.10, matching the Profit measure used in the
   companion Power BI model). Replace this with real cost data if / when
   it becomes available.
"""

import pandas as pd

PROFIT_MARGIN = 0.10  # flat profit margin on Net Sales (matches the Power BI model)


def _parse_discount(reduction_type) -> float:
    if pd.isna(reduction_type):
        return 0.0
    reduction_type = str(reduction_type).strip()
    if "Buy 1 Get 1" in reduction_type:
        return 0.50
    if "%" in reduction_type:
        return float(reduction_type.replace("% off", "").strip()) / 100
    return 0.0


def compute_derived_columns(
    fact: pd.DataFrame,
    products: pd.DataFrame,
    promotions: pd.DataFrame,
    profit_margin: float = PROFIT_MARGIN,
) -> pd.DataFrame:
    """Fill in PricePerUnit, TotalSales, DiscountPct, DiscountValue, NetSales, Profit."""
    fact = fact.copy()

    price_map = products.set_index("ProductID")["Price (INR)"]
    fact["PricePerUnit"] = fact["ProductID"].map(price_map)
    fact["TotalSales"] = fact["UnitsSold"] * fact["PricePerUnit"]

    promotions = promotions.copy()
    promotions["DiscountPct"] = promotions["Price Reduction Type"].apply(_parse_discount)
    promo_map = promotions.set_index("PromotionID")["DiscountPct"]

    fact["DiscountPct"] = fact["PromotionID"].map(promo_map).fillna(0.0)
    fact["DiscountValue"] = fact["TotalSales"] * fact["DiscountPct"]
    fact["NetSales"] = fact["TotalSales"] - fact["DiscountValue"]
    fact["Profit"] = fact["NetSales"] * profit_margin

    fact["Year"] = fact["Date"].dt.year
    fact["Quarter"] = fact["Date"].dt.to_period("Q").astype(str)
    fact["Month"] = fact["Date"].dt.to_period("M").astype(str)

    return fact


def build_master_table(
    fact: pd.DataFrame,
    products: pd.DataFrame,
    customers: pd.DataFrame,
    promotions: pd.DataFrame,
) -> pd.DataFrame:
    """Join the fact table with all dimension tables into one flat table."""
    master = (
        fact.merge(products, on="ProductID", how="left")
        .merge(customers, left_on="CustomerID", right_on="Customer ID", how="left")
        .merge(
            promotions[["PromotionID", "Promotion Name", "Ad Type", "Coupon Code", "Price Reduction Type"]],
            on="PromotionID",
            how="left",
        )
    )
    master["Promotion Name"] = master["Promotion Name"].fillna("No Promotion")
    return master
