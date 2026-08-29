"""
data_cleaning.py
----------------
Basic cleaning routines applied to the raw tables before analysis.
"""

import numpy as np
import pandas as pd


def clean_customers(customers: pd.DataFrame) -> pd.DataFrame:
    """Strip stray whitespace from City / State text fields."""
    customers = customers.copy()
    customers["City"] = customers["City"].astype(str).str.strip()
    customers["State"] = customers["State"].astype(str).str.strip()
    return customers


def clean_fact(fact: pd.DataFrame) -> pd.DataFrame:
    """
    - Convert PromotionID == 0 to NaN (0 means 'no promotion applied').
    - Ensure Date column is a proper datetime.
    """
    fact = fact.copy()
    fact["PromotionID"] = fact["PromotionID"].replace(0, np.nan)
    # Keep PromotionID as a generic object dtype (not float64) so it can
    # always be merged against Dim Promotion's string IDs ("PR001", ...)
    # later on, even in edge-case slices where every row happens to have
    # the same value (which would otherwise let pandas infer a pure
    # numeric dtype).
    fact["PromotionID"] = fact["PromotionID"].astype(object)
    # dayfirst=True matches the source header ("Date (dd/mm/yyyy)"); it's a
    # no-op when Excel already hands back native datetime values, but
    # protects against ambiguous day/month parsing if the column is ever
    # exported as plain text (e.g. after a CSV round-trip).
    fact["Date"] = pd.to_datetime(fact["Date"], dayfirst=True)
    return fact
