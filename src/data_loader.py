import os

import pandas as pd

from .config import DATA_FILE

# Sheet names in the source workbook. ``Dim Promotion`` has a trailing space
# in the file, which we keep here on purpose.
FACT_SHEET = "Sheet3"
CUSTOMER_SHEET = "Dim Customers"
PRODUCT_SHEET = "Dim Product"
PROMOTION_SHEET = "Dim Promotion "

FACT_COLUMNS = [
    "Date",
    "CustomerID",
    "PromotionID",
    "ProductID",
    "UnitsSold",
    "PricePerUnit",
    "TotalSales",
    "DiscountPct",
    "DiscountValue",
    "NetSales",
]

REQUIRED_SHEETS = [FACT_SHEET, CUSTOMER_SHEET, PRODUCT_SHEET, PROMOTION_SHEET]


def _validate_sheets(workbook: pd.ExcelFile) -> None:
    missing = [sheet for sheet in REQUIRED_SHEETS if sheet not in workbook.sheet_names]
    if missing:
        raise ValueError(
            f"Missing sheet(s) {missing} in workbook. " f"Available sheets: {workbook.sheet_names}"
        )


def load_data(filepath: str | os.PathLike | None = None) -> dict:
    """Read the raw Excel workbook into a dict of DataFrames.

    Returns keys ``fact``, ``customers``, ``products`` and ``promotions``.
    The fact sheet's positional columns are renamed to the snake-friendly
    names defined in :data:`FACT_COLUMNS`.
    """
    path = DATA_FILE if filepath is None else filepath
    path = os.fspath(path)

    with pd.ExcelFile(path) as workbook:
        _validate_sheets(workbook)

        fact = workbook.parse(FACT_SHEET)
        customers = workbook.parse(CUSTOMER_SHEET)
        products = workbook.parse(PRODUCT_SHEET)
        promotions = workbook.parse(PROMOTION_SHEET)

    if len(fact.columns) != len(FACT_COLUMNS):
        raise ValueError(
            f"Expected {len(FACT_COLUMNS)} columns in '{FACT_SHEET}', "
            f"found {len(fact.columns)}."
        )
    fact.columns = FACT_COLUMNS

    return {
        "fact": fact,
        "customers": customers,
        "products": products,
        "promotions": promotions,
    }
