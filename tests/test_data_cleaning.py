import pandas as pd
import pytest

from src.data_cleaning import clean_customers, clean_fact


def test_clean_customers_strips_whitespace():
    frame = pd.DataFrame({"City": [" Nagpur "], "State": [" Maharashtra "], "Customer Name": ["A"]})
    result = clean_customers(frame)
    assert result.loc[0, "City"] == "Nagpur"
    assert result.loc[0, "State"] == "Maharashtra"


def test_clean_customers_missing_column_raises():
    with pytest.raises(ValueError):
        clean_customers(pd.DataFrame({"City": ["Nagpur"]}))


def test_clean_fact_zero_promotion_becomes_nan():
    frame = pd.DataFrame({"PromotionID": [0, 1], "Date": ["2022-01-01", "2022-01-02"]})
    result = clean_fact(frame)
    assert pd.isna(result.loc[0, "PromotionID"])
    assert result.loc[1, "PromotionID"] == 1


def test_clean_fact_converts_date_dtype():
    frame = pd.DataFrame({"PromotionID": [1], "Date": ["2022-01-01"]})
    result = clean_fact(frame)
    assert pd.api.types.is_datetime64_any_dtype(result["Date"])
