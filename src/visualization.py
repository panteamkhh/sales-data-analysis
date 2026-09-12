"""
visualization.py
-----------------
Chart-rendering functions, one per project question. Every function
saves a PNG into the screenshots/ folder (for the README / GitHub
preview) and returns the matplotlib Figure so it also renders inline
in the notebook.

Style (shared with the companion project):
- whitegrid theme, white background, notebook context
- 9x6 figures at 140 dpi, padded onto a fixed white 1260x840 (3:2) canvas
  so a two-column README grid aligns exactly
- bold titles, base font 11, single accent ``#2a6f97`` / contrast ``#c1121f``
"""

import os

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from PIL import Image

from .config import SCREENSHOTS_DIR

FIG_SIZE = (9, 6)
DPI = 140
CANVAS_SIZE = (FIG_SIZE[0] * DPI, FIG_SIZE[1] * DPI)  # fixed 3:2 canvas (1260x840)
ACCENT = "#2a6f97"
CONTRAST = "#c1121f"

sns.set_theme(style="whitegrid", context="notebook")
plt.rcParams["figure.figsize"] = FIG_SIZE
plt.rcParams["figure.dpi"] = DPI
plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["axes.titlesize"] = 13
plt.rcParams["font.size"] = 11


def _compact_number(value, _pos=None) -> str:
    """Format large numbers compactly, e.g. 13_000_000 -> '13M'."""
    for suffix, divisor in (("B", 1e9), ("M", 1e6), ("K", 1e3)):
        if abs(value) >= divisor:
            return f"{value / divisor:.1f}".rstrip("0").rstrip(".") + suffix
    return f"{value:.0f}"


def _save(fig, filename: str):
    """Save then pad the figure onto a fixed white 3:2 canvas."""
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    path = os.path.join(SCREENSHOTS_DIR, filename)
    fig.savefig(path)

    image = Image.open(path).convert("RGB")
    image.thumbnail(CANVAS_SIZE, Image.LANCZOS)
    canvas = Image.new("RGB", CANVAS_SIZE, "white")
    canvas.paste(
        image,
        ((CANVAS_SIZE[0] - image.width) // 2, (CANVAS_SIZE[1] - image.height) // 2),
    )
    canvas.save(path)


def _compact_axis(ax, which: str = "x"):
    target = ax.xaxis if which == "x" else ax.yaxis
    target.set_major_formatter(mticker.FuncFormatter(_compact_number))


# Q1 -----------------------------------------------------------------
def plot_top_bottom(top_n, bottom_n, metric_label: str, filename: str):
    is_money = metric_label in {"Sales", "Profit"}
    axis_label = f"{metric_label} (INR)" if is_money else metric_label

    fig, axes = plt.subplots(1, 2, figsize=FIG_SIZE)

    sns.barplot(
        x=top_n.values, y=top_n.index, hue=top_n.index, legend=False, palette="crest", ax=axes[0]
    )
    axes[0].set_title(f"Top 5 Products by {metric_label}")
    axes[0].set_xlabel(axis_label)
    axes[0].set_ylabel("")

    sns.barplot(
        x=bottom_n.values,
        y=bottom_n.index,
        hue=bottom_n.index,
        legend=False,
        palette="mako",
        ax=axes[1],
    )
    axes[1].set_title(f"Bottom 5 Products by {metric_label}")
    axes[1].set_xlabel(axis_label)
    axes[1].set_ylabel("")

    if is_money:
        for ax in axes:
            _compact_axis(ax)

    fig.tight_layout()
    _save(fig, filename)
    return fig


# Q2 -----------------------------------------------------------------
def plot_sales_trends(daily, monthly, quarterly, yearly):
    fig, axes = plt.subplots(2, 2, figsize=FIG_SIZE)

    axes[0, 0].plot(daily.index, daily.values, linewidth=0.8, color=ACCENT)
    axes[0, 0].set_title("Daily Sales Trend")
    axes[0, 0].xaxis.set_major_locator(mticker.MaxNLocator(8))
    axes[0, 0].tick_params(axis="x", rotation=45)

    axes[0, 1].plot(range(len(monthly)), monthly.values, marker="o", color=ACCENT)
    axes[0, 1].set_title("Monthly Sales Trend")
    step = max(1, len(monthly) // 8)
    axes[0, 1].set_xticks(range(0, len(monthly), step))
    axes[0, 1].set_xticklabels(monthly.index.strftime("%Y-%m")[::step], rotation=90)

    axes[1, 0].plot(range(len(quarterly)), quarterly.values, marker="s", color=ACCENT)
    axes[1, 0].set_title("Quarterly Sales Trend")
    axes[1, 0].set_xticks(range(len(quarterly)))
    axes[1, 0].set_xticklabels(quarterly.index.to_period("Q").astype(str), rotation=90)

    axes[1, 1].bar(yearly.index.year.astype(str), yearly.values, color=ACCENT)
    axes[1, 1].set_title("Yearly Sales Trend")

    for row in axes:
        for ax in row:
            ax.set_ylabel("Total Sales (INR)")
            _compact_axis(ax, "y")

    fig.tight_layout()
    _save(fig, "02_sales_trends.png")
    return fig


# Q3 -----------------------------------------------------------------
def plot_sales_profit_relationship(master, corr: float):
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    sns.scatterplot(data=master, x="TotalSales", y="Profit", alpha=0.3, s=14, color=ACCENT, ax=ax)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title(f"Sales vs. Profit (log-log, r = {corr:.2f})")
    ax.set_xlabel("Total Sales (INR, log scale)")
    ax.set_ylabel("Profit (INR, log scale)")
    _save(fig, "03_sales_profit_relationship.png")
    return fig


# Q4 -----------------------------------------------------------------
def plot_period_comparison(result_df, labels):
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    result_df[[labels[0], labels[1]]].plot(
        kind="bar", ax=ax, color=[ACCENT, CONTRAST], width=0.75, rot=0
    )
    ax.set_title(f"{labels[0]} vs. {labels[1]}")
    ax.set_xlabel("")
    ax.set_ylabel("Value (INR / units)")
    ax.legend(loc="upper right", frameon=False)
    fig.tight_layout()
    _save(fig, "04_period_comparison.png")
    return fig


# Q5 -----------------------------------------------------------------
def plot_avg_discount(avg_discount):
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    sns.barplot(
        x=avg_discount.values,
        y=avg_discount.index,
        hue=avg_discount.index,
        legend=False,
        palette="mako",
        ax=ax,
    )
    ax.set_title("Average Discount by Promotion")
    ax.set_xlabel("Average Discount (%)")
    ax.set_ylabel("")
    fig.tight_layout()
    _save(fig, "05_avg_discount_by_promotion.png")
    return fig


# Q8 -----------------------------------------------------------------
def plot_sales_by_city(sales_by_city):
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    sns.barplot(
        x=sales_by_city.values,
        y=sales_by_city.index,
        hue=sales_by_city.index,
        legend=False,
        palette="crest",
        ax=ax,
    )
    ax.set_title("Total Sales by City")
    ax.set_xlabel("Total Sales (INR)")
    ax.set_ylabel("")
    _compact_axis(ax)
    fig.tight_layout()
    _save(fig, "08_sales_by_city.png")
    return fig
