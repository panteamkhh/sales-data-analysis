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
    fact["Date"] = pd.to_datetime(fact["Date"])
    return fact
