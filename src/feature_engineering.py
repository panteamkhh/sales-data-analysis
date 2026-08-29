"""
feature_engineering.py
-----------------------
Fills in any missing values in the fact table's derived columns
(PricePerUnit, TotalSales, DiscountPct, DiscountValue, NetSales, Profit)
and builds the final denormalized "master" table used for analysis.

Schema note (v2): earlier versions of the workbook shipped these six
columns completely empty, so this module used to compute all of them
from scratch. The current workbook (rebuilt in Power BI) already has
them populated for most/all rows. To stay correct either way, every
column below is only RECOMPUTED where the raw value is missing
(NaN) - `pandas.Series.combine_first` keeps the existing raw value
wherever one is present, and only fills gaps with the computed value.
That means this module is safe to run unchanged on the new dataset
even though its main job (filling blanks) rarely triggers anymore.

Assumptions used only for the values that still need to be computed:

1. PricePerUnit is looked up from Dim Product (matches on ProductID).
   The price column in Dim Product may be named "Price (INR)" or
   "Price Per Unit (INR)" depending on workbook version - both are
   supported.
2. DiscountPct is taken from Dim Promotion's numeric "Percentage"
   column when present (v2 workbook), otherwise parsed from the
   "Price Reduction Type" text field (e.g. "20% off" -> 0.20, v1
   workbook). Orders with no promotion get 0%. The one non-percentage
   promotion, "Buy 1 Get 1 Free", is treated as an effective 50%
   discount (1 of 2 units is free).
3. Profit: if the source data doesn't supply it (no Cost column),
   it is estimated using a configurable flat margin on Net Sales
   (default PROFIT_MARGIN = 0.10, matching the margin implied by the
   current dataset's own Profit figures). Replace this with real cost
   data in the source workbook if/when it becomes available.
"""

import pandas as pd

PROFIT_MARGIN = 0.10  # fallback flat profit margin on Net Sales, only
                       # used for rows where Profit is missing


def _find_price_column(products: pd.DataFrame) -> str:
    """Locate the per-unit price column, tolerating header renames."""
    for candidate in ("Price Per Unit (INR)", "Price (INR)", "Price Per Unit", "Price"):
        if candidate in products.columns:
            return candidate
    raise KeyError(
        "Could not find a price column in Dim Product. Expected one of "
        "'Price Per Unit (INR)' or 'Price (INR)'; got: "
        f"{list(products.columns)}"
    )


def _parse_discount_text(reduction_type) -> float:
    if pd.isna(reduction_type):
        return 0.0
    reduction_type = str(reduction_type).strip()
    if "Buy 1 Get 1" in reduction_type:
        return 0.50
    if "%" in reduction_type:
        return float(reduction_type.replace("% off", "").strip()) / 100
    return 0.0


def _promotion_discount_map(promotions: pd.DataFrame) -> pd.Series:
    """
    Build a PromotionID -> discount fraction (0-1) lookup.

    Prefers the numeric "Percentage" column (v2 workbook). Falls back
    to parsing the "Price Reduction Type" text column (v1 workbook) for
    any promotion where "Percentage" is missing or the column doesn't
    exist at all.
    """
    promotions = promotions.copy()

    if "Percentage" in promotions.columns:
        pct_from_number = pd.to_numeric(promotions["Percentage"], errors="coerce") / 100
    else:
        pct_from_number = pd.Series(index=promotions.index, dtype=float)

    if "Price Reduction Type" in promotions.columns:
        pct_from_text = promotions["Price Reduction Type"].apply(_parse_discount_text)
    else:
        pct_from_text = pd.Series(index=promotions.index, dtype=float)

    promotions["DiscountPct"] = pct_from_number.combine_first(pct_from_text)
    return promotions.set_index("PromotionID")["DiscountPct"]


def compute_derived_columns(
    fact: pd.DataFrame,
    products: pd.DataFrame,
    promotions: pd.DataFrame,
    profit_margin: float = PROFIT_MARGIN,
) -> pd.DataFrame:
    """
    Ensure PricePerUnit, TotalSales, DiscountPct, DiscountValue,
    NetSales and Profit are populated, computing only what's missing.
    """
    fact = fact.copy()

    price_col = _find_price_column(products)
    price_map = products.set_index("ProductID")[price_col]
    computed_price = fact["ProductID"].map(price_map)
    fact["PricePerUnit"] = fact["PricePerUnit"].combine_first(computed_price)

    computed_total = fact["UnitsSold"] * fact["PricePerUnit"]
    fact["TotalSales"] = fact["TotalSales"].combine_first(computed_total)

    promo_map = _promotion_discount_map(promotions)
    computed_discount_pct = fact["PromotionID"].map(promo_map).fillna(0.0)
    fact["DiscountPct"] = fact["DiscountPct"].combine_first(computed_discount_pct)

    computed_discount_value = fact["TotalSales"] * fact["DiscountPct"]
    fact["DiscountValue"] = fact["DiscountValue"].combine_first(computed_discount_value)

    computed_net_sales = fact["TotalSales"] - fact["DiscountValue"]
    fact["NetSales"] = fact["NetSales"].combine_first(computed_net_sales)

    computed_profit = fact["NetSales"] * profit_margin
    fact["Profit"] = fact["Profit"].combine_first(computed_profit)

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
