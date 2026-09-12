"""End-to-end runner: load -> clean -> derive -> analyze -> plot -> export.

Usage:
    python -m src.run_analysis
    python -m src.run_analysis --input data/store_data.xlsx --output-dir output
"""

import argparse
from pathlib import Path

import pandas as pd

from . import analysis, visualization
from .config import DATA_FILE, OUTPUT_DIR
from .data_cleaning import clean_customers, clean_fact
from .data_loader import load_data
from .feature_engineering import build_master_table, compute_derived_columns


def build_master(filepath=DATA_FILE) -> pd.DataFrame:
    """Run the full load/clean/derive/join pipeline and return the master table."""
    raw = load_data(filepath)
    fact = clean_fact(raw["fact"])
    customers = clean_customers(raw["customers"])
    products = raw["products"]
    promotions = raw["promotions"]

    fact = compute_derived_columns(fact, products, promotions)
    return build_master_table(fact, products, customers, promotions)


def run(filepath=DATA_FILE, output_dir=OUTPUT_DIR, export: bool = True) -> pd.DataFrame:
    """Execute every analysis question and render all charts."""
    master = build_master(filepath)

    top_sales, bottom_sales = analysis.top_bottom_products(master, "TotalSales")
    visualization.plot_top_bottom(top_sales, bottom_sales, "Sales", "01_top_bottom_sales.png")

    top_profit, bottom_profit = analysis.top_bottom_products(master, "Profit")
    visualization.plot_top_bottom(top_profit, bottom_profit, "Profit", "01_top_bottom_profit.png")

    top_qty, bottom_qty = analysis.top_bottom_products(master, "UnitsSold")
    visualization.plot_top_bottom(
        top_qty, bottom_qty, "Quantity Sold", "01_top_bottom_quantity.png"
    )

    daily = analysis.sales_trend(master, freq="D")
    monthly = analysis.sales_trend(master, freq="ME")
    quarterly = analysis.sales_trend(master, freq="QE")
    yearly = analysis.sales_trend(master, freq="YE")
    visualization.plot_sales_trends(daily, monthly, quarterly, yearly)

    corr = analysis.sales_profit_correlation(master)
    visualization.plot_sales_profit_relationship(master, corr)

    labels = ("H1 2022", "H2 2022")
    comparison = analysis.compare_periods(
        master,
        period1=("2022-01-01", "2022-06-30"),
        period2=("2022-07-01", "2022-12-31"),
        labels=labels,
    )
    visualization.plot_period_comparison(comparison, labels)

    avg_discount = analysis.avg_discount_by_promotion(master)
    visualization.plot_avg_discount(avg_discount)

    city_sales = analysis.sales_by_city(master)
    visualization.plot_sales_by_city(city_sales)

    if export:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        master.to_csv(output_dir / "master_sales_data.csv", index=False)

    print(f"Orders: {analysis.total_orders(master):,}")
    print(f"Sales vs. Profit correlation (r): {corr:.3f}")
    print(f"Charts written to: {visualization.SCREENSHOTS_DIR}")
    return master


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Run the sales analysis end-to-end.")
    parser.add_argument("--input", default=str(DATA_FILE), help="Path to the source .xlsx workbook")
    parser.add_argument(
        "--output-dir", default=str(OUTPUT_DIR), help="Where to write master_sales_data.csv"
    )
    parser.add_argument("--no-export", action="store_true", help="Skip writing the CSV export")
    args = parser.parse_args(argv)

    run(filepath=args.input, output_dir=args.output_dir, export=not args.no_export)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
