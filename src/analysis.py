"""
analysis.py
-----------
One function per project question (Q1-Q8). Each function takes the
master table (see feature_engineering.build_master_table) and returns
plain pandas objects (Series / DataFrame). Plotting lives in
visualization.py so analysis logic stays independent of chart rendering.
"""

import pandas as pd


# Q1 -----------------------------------------------------------------
def top_bottom_products(master: pd.DataFrame, metric: str, n: int = 5) -> tuple[pd.Series, pd.Series]:
    """Return (top_n, bottom_n) product totals for a given metric column."""
    grouped = master.groupby("Product Name")[metric].sum().sort_values(ascending=False)
    return grouped.head(n), grouped.tail(n)


# Q2 -----------------------------------------------------------------
def sales_trend(master: pd.DataFrame, freq: str = "D") -> pd.Series:
    """
    Aggregate Total Sales over time.
    freq: 'D' daily, 'ME' monthly, 'QE' quarterly, 'YE' yearly
    """
    series = master.set_index("Date")["TotalSales"].resample(freq).sum()
    return series


# Q3 -----------------------------------------------------------------
def sales_profit_correlation(master: pd.DataFrame) -> float:
    """Pearson correlation coefficient between Total Sales and Profit."""
    return master["TotalSales"].corr(master["Profit"])


# Q4 -----------------------------------------------------------------
def compare_periods(
    master: pd.DataFrame,
    period1: tuple[str, str],
    period2: tuple[str, str],
    labels: tuple[str, str] = ("Period 1", "Period 2"),
) -> pd.DataFrame:
    """Compare Sales / Profit / Quantity / Orders between two date ranges."""

    def summarize(period):
        start, end = pd.to_datetime(period[0]), pd.to_datetime(period[1])
        subset = master[(master["Date"] >= start) & (master["Date"] <= end)]
        return pd.Series(
            {
                "Total Sales": subset["TotalSales"].sum(),
                "Total Profit": subset["Profit"].sum(),
                "Total Quantity": subset["UnitsSold"].sum(),
                "Orders": len(subset),
            }
        )

    result = pd.DataFrame({labels[0]: summarize(period1), labels[1]: summarize(period2)})
    result["Change %"] = ((result[labels[1]] - result[labels[0]]) / result[labels[0]] * 100).round(1)
    return result


# Q5 -----------------------------------------------------------------
def avg_discount_by_promotion(master: pd.DataFrame) -> pd.Series:
    """Average discount percentage per promotion category, sorted descending."""
    return (
        master.groupby("Promotion Name")["DiscountPct"]
        .mean()
        .sort_values(ascending=False)
        * 100
    )


# Q6 -----------------------------------------------------------------
def total_orders(master: pd.DataFrame) -> int:
    """Total number of orders (rows) in the fact table."""
    return len(master)


# Q7 -----------------------------------------------------------------
def filter_orders(
    master: pd.DataFrame,
    product_name: str = None,
    date_range: tuple[str, str] = None,
    customer_id: int = None,
    promotion: str = None,
) -> pd.DataFrame:
    """
    Return Sales / Profit / Discount / Net Sales and all remaining fields
    for each order, filterable by Product, Date range, Customer ID or
    Promotion category (mirrors the Power BI visual-filter requirement).
    """
    df = master.copy()
    if product_name:
        df = df[df["Product Name"] == product_name]
    if date_range:
        start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        df = df[(df["Date"] >= start) & (df["Date"] <= end)]
    if customer_id:
        df = df[df["CustomerID"] == customer_id]
    if promotion:
        df = df[df["Promotion Name"] == promotion]

    cols = [
        "Date", "Customer Name", "Product Name", "UnitsSold", "TotalSales",
        "DiscountPct", "DiscountValue", "NetSales", "Profit", "Promotion Name", "City",
    ]
    return df[cols].reset_index(drop=True)


# Q8 -----------------------------------------------------------------
def sales_by_city(master: pd.DataFrame) -> pd.Series:
    """Total sales aggregated by customer city, sorted descending."""
    return master.groupby("City")["TotalSales"].sum().sort_values(ascending=False)
