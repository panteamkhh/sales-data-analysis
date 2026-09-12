import pandas as pd
import pytest

from src import analysis


def test_top_bottom_products_ordering(master):
    top, bottom = analysis.top_bottom_products(master, "TotalSales", n=2)
    assert list(top.index) == ["Widget", "Gadget"]
    assert list(bottom.index) == ["Gadget", "Widget"]
    assert top.iloc[0] >= top.iloc[1]


def test_top_bottom_products_sales_values(master):
    top, _ = analysis.top_bottom_products(master, "TotalSales", n=2)
    # Widget: 2*100 + 10*100 (discounted sales still counted on TotalSales)
    assert top.loc["Widget"] == pytest.approx(1200.0)


def test_sales_profit_correlation_is_bounded(master):
    corr = analysis.sales_profit_correlation(master)
    assert -1.0 <= corr <= 1.0


def test_compare_periods_reports_change(master):
    result = analysis.compare_periods(
        master,
        period1=("2022-01-01", "2022-06-30"),
        period2=("2022-07-01", "2022-12-31"),
        labels=("H1", "H2"),
    )
    assert set(result.index) == {"Total Sales", "Total Profit", "Total Quantity", "Orders"}
    assert "Change %" in result.columns


def test_compare_periods_handles_empty_base(master):
    result = analysis.compare_periods(
        master,
        period1=("2000-01-01", "2000-12-31"),
        period2=("2022-01-01", "2022-12-31"),
    )
    assert pd.isna(result.loc["Total Sales", "Change %"])


def test_avg_discount_by_promotion_sorted(master):
    avg = analysis.avg_discount_by_promotion(master)
    assert avg.is_monotonic_decreasing
    assert "No Promotion" in avg.index


def test_total_orders(master):
    assert analysis.total_orders(master) == 3


def test_filter_orders_by_customer_zero():
    frame = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2022-01-01", "2022-01-02"]),
            "CustomerID": [0, 5],
            "Customer Name": ["Zero Customer", "Five Customer"],
            "Product Name": ["Widget", "Gadget"],
            "UnitsSold": [1, 1],
            "TotalSales": [100.0, 250.0],
            "DiscountPct": [0.0, 0.0],
            "DiscountValue": [0.0, 0.0],
            "NetSales": [100.0, 250.0],
            "Profit": [10.0, 25.0],
            "Promotion Name": ["No Promotion", "Summer Sale"],
            "City": ["Nagpur", "Bhopal"],
        }
    )
    filtered = analysis.filter_orders(frame, customer_id=0)
    assert len(filtered) == 1
    assert filtered.iloc[0]["Customer Name"] == "Zero Customer"


def test_filter_orders_by_date_and_product(master):
    filtered = analysis.filter_orders(
        master,
        product_name="Widget",
        date_range=("2022-01-01", "2022-06-30"),
    )
    assert len(filtered) == 1


def test_sales_by_city_sorted(master):
    result = analysis.sales_by_city(master)
    assert result.is_monotonic_decreasing
