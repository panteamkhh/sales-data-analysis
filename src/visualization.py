"""
visualization.py
-----------------
Chart-rendering functions, one per project question. Every function
saves a PNG into the screenshots/ folder (for the README / GitHub
preview) and returns the matplotlib Figure so it also renders inline
in the notebook.
"""

import os

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

from .config import SCREENSHOTS_DIR

sns.set_theme(style="whitegrid", palette="viridis")
plt.rcParams["figure.figsize"] = (10, 5)
plt.rcParams["axes.titlesize"] = 13
plt.rcParams["axes.titleweight"] = "bold"

CURRENCY_FORMAT = "INR {x:,.0f}"
CURRENCY_PREFIX = "INR "


def _save(fig, filename: str):
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    fig.savefig(os.path.join(SCREENSHOTS_DIR, filename), dpi=150, bbox_inches="tight")


def _format_currency(axis, which: str = "x"):
    """Apply an INR thousands-separated formatter to a matplotlib axis."""
    formatter = mticker.StrMethodFormatter(CURRENCY_FORMAT)
    target = axis.xaxis if which == "x" else axis.yaxis
    target.set_major_formatter(formatter)


# Q1 -----------------------------------------------------------------
def plot_top_bottom(top_n, bottom_n, metric_label: str, filename: str):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    sns.barplot(
        x=top_n.values, y=top_n.index, hue=top_n.index, legend=False, palette="crest", ax=axes[0]
    )
    axes[0].set_title(f"Top 5 Products by {metric_label}")
    axes[0].set_xlabel(metric_label)

    sns.barplot(
        x=bottom_n.values,
        y=bottom_n.index,
        hue=bottom_n.index,
        legend=False,
        palette="flare",
        ax=axes[1],
    )
    axes[1].set_title(f"Bottom 5 Products by {metric_label}")
    axes[1].set_xlabel(metric_label)

    if "sales" in metric_label.lower() or "profit" in metric_label.lower():
        for ax in axes:
            _format_currency(ax)

    fig.tight_layout()
    _save(fig, filename)
    return fig


# Q2 -----------------------------------------------------------------
def plot_sales_trends(daily, monthly, quarterly, yearly):
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))

    axes[0, 0].plot(daily.index, daily.values, linewidth=0.8, color="#2c7fb8")
    axes[0, 0].set_title("Daily Sales Trend")

    axes[0, 1].plot(monthly.index, monthly.values, marker="o", color="#31a354")
    axes[0, 1].set_title("Monthly Sales Trend")
    axes[0, 1].tick_params(axis="x", rotation=90)
    axes[0, 1].xaxis.set_major_locator(mticker.MaxNLocator(12))

    axes[1, 0].plot(quarterly.index, quarterly.values, marker="s", color="#de2d26")
    axes[1, 0].set_title("Quarterly Sales Trend")
    axes[1, 0].tick_params(axis="x", rotation=90)

    axes[1, 1].bar(yearly.index.astype(str), yearly.values, color="#756bb1")
    axes[1, 1].set_title("Yearly Sales Trend")

    for row in axes:
        for ax in row:
            ax.set_ylabel("Total Sales (INR)")
            _format_currency(ax, "y")

    fig.tight_layout()
    _save(fig, "02_sales_trends.png")
    return fig


# Q3 -----------------------------------------------------------------
def plot_sales_profit_relationship(master, corr: float):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.regplot(
        data=master,
        x="TotalSales",
        y="Profit",
        scatter_kws={"alpha": 0.3, "s": 15},
        line_kws={"color": "red"},
        ax=ax,
    )
    ax.set_title(f"Sales vs. Profit Relationship (r = {corr:.2f})")
    ax.set_xlabel("Total Sales (INR)")
    ax.set_ylabel("Profit (INR)")
    _format_currency(ax)
    _format_currency(ax, "y")
    _save(fig, "03_sales_profit_relationship.png")
    return fig


# Q4 -----------------------------------------------------------------
def plot_period_comparison(result_df, labels):
    fig, ax = plt.subplots(figsize=(8, 5))
    result_df[[labels[0], labels[1]]].plot(kind="bar", ax=ax, color=["#3182bd", "#e6550d"])
    ax.set_title(f"{labels[0]} vs. {labels[1]}")
    ax.set_ylabel(f"Value ({CURRENCY_PREFIX.strip()}, units vary)")
    plt.xticks(rotation=0)
    _save(fig, "04_period_comparison.png")
    return fig


# Q5 -----------------------------------------------------------------
def plot_avg_discount(avg_discount):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(
        x=avg_discount.values,
        y=avg_discount.index,
        hue=avg_discount.index,
        legend=False,
        palette="mako",
        ax=ax,
    )
    ax.set_xlabel("Average Discount (%)")
    ax.set_title("Average Discount by Promotion Category")
    _save(fig, "05_avg_discount_by_promotion.png")
    return fig


# Q8 -----------------------------------------------------------------
def plot_sales_by_city(sales_by_city):
    fig, ax = plt.subplots(figsize=(9, 7))
    sns.barplot(
        x=sales_by_city.values,
        y=sales_by_city.index,
        hue=sales_by_city.index,
        legend=False,
        palette="rocket_r",
        ax=ax,
    )
    ax.set_xlabel("Total Sales (INR)")
    ax.set_title("Total Sales by City")
    _format_currency(ax)
    _save(fig, "08_sales_by_city.png")
    return fig
