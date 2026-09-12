import pandas as pd
import pytest

from src.feature_engineering import (
    _parse_discount,
    compute_derived_columns,
)


@pytest.mark.parametrize(
    ("terms", "expected"),
    [
        ("20% off", 0.20),
        ("70% off", 0.70),
        ("Buy 1 Get 1 Free", 0.50),
        ("buy 1 get 1", 0.50),
        ("10 %", 0.10),
        (None, 0.0),
        (float("nan"), 0.0),
        ("", 0.0),
    ],
)
def test_parse_discount_known_terms(terms, expected):
    assert _parse_discount(terms) == pytest.approx(expected)


def test_parse_discount_warns_on_unknown_terms():
    with pytest.warns(UserWarning):
        assert _parse_discount("Mystery deal") == 0.0


def test_compute_derived_columns_values(fact, products, promotions):
    result = compute_derived_columns(fact, products, promotions)

    assert result.loc[0, "PricePerUnit"] == 100.0
    assert result.loc[0, "TotalSales"] == 200.0
    assert result.loc[0, "DiscountPct"] == pytest.approx(0.20)
    assert result.loc[0, "DiscountValue"] == pytest.approx(40.0)
    assert result.loc[0, "NetSales"] == pytest.approx(160.0)
    assert result.loc[0, "Profit"] == pytest.approx(16.0)


def test_compute_derived_columns_no_promotion_is_zero(fact, products, promotions):
    result = compute_derived_columns(fact, products, promotions)
    assert result.loc[1, "DiscountPct"] == 0.0
    assert result.loc[1, "NetSales"] == pytest.approx(250.0)


def test_compute_derived_columns_adds_calendar_fields(fact, products, promotions):
    result = compute_derived_columns(fact, products, promotions)
    assert result.loc[0, "Year"] == 2022
    assert result.loc[0, "Quarter"] == "2022Q1"
    assert result.loc[0, "Month"] == "2022-03"


def test_build_master_table_fills_missing_promotion(master):
    assert len(master) == 3
    assert master["Promotion Name"].notna().all()
    assert (master["Promotion Name"] == "No Promotion").sum() == 1
    assert "City" in master.columns
    assert "Price (INR)" in master.columns


def test_compute_derived_columns_does_not_mutate_input(fact, products):
    before = fact.copy()
    empty_promotions = pd.DataFrame(columns=["PromotionID", "Price Reduction Type"])
    compute_derived_columns(fact, products, empty_promotions)
    pd.testing.assert_frame_equal(fact, before)
