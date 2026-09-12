import numpy as np
import pandas as pd

REQUIRED_CUSTOMER_COLUMNS = {"City", "State"}
REQUIRED_FACT_COLUMNS = {"PromotionID", "Date"}


def _require_columns(df: pd.DataFrame, columns: set, name: str) -> None:
    missing = columns - set(df.columns)
    if missing:
        raise ValueError(f"{name} is missing required column(s): {sorted(missing)}")


def clean_customers(customers: pd.DataFrame) -> pd.DataFrame:
    """Strip stray whitespace from City / State text fields."""
    _require_columns(customers, REQUIRED_CUSTOMER_COLUMNS, "customers")
    customers = customers.copy()
    customers["City"] = customers["City"].astype(str).str.strip()
    customers["State"] = customers["State"].astype(str).str.strip()
    return customers


def clean_fact(fact: pd.DataFrame) -> pd.DataFrame:
    """
    - Convert PromotionID == 0 to NaN (0 means 'no promotion applied').
    - Ensure Date column is a proper datetime.
    """
    _require_columns(fact, REQUIRED_FACT_COLUMNS, "fact")
    fact = fact.copy()
    fact["PromotionID"] = fact["PromotionID"].replace(0, np.nan)
    fact["Date"] = pd.to_datetime(fact["Date"])
    return fact
