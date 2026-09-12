import pandas as pd
import pytest


@pytest.fixture
def products() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "ProductID": ["P001", "P002"],
            "Product Name": ["Widget", "Gadget"],
            "Product Line": ["Standard", "Premium"],
            "Price (INR)": [100.0, 250.0],
        }
    )


@pytest.fixture
def promotions() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "PromotionID": ["PR001", "PR002", "PR003"],
            "Promotion Name": ["Summer Sale", "New Year Special", "Clearance Sale"],
            "Ad Type": ["Email", "Social", "Email"],
            "Coupon Code": ["S20", "NYB1", "C70"],
            "Price Reduction Type": ["20% off", "Buy 1 Get 1 Free", "70% off"],
        }
    )


@pytest.fixture
def customers() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Customer ID": [1, 2],
            "Customer Name": ["Aarav Singh", "Aditi Patel"],
            "City": ["Nagpur", "Bhopal"],
            "State": ["Maharashtra", "Madhya Pradesh"],
            "Pincode": [440001, 462001],
            "EmailID": ["1Aarav@gmail.com", "2Aditi@gmail.com"],
            "Phone Number": [860135097, 896750475],
        }
    )


@pytest.fixture
def fact() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Date": pd.to_datetime(["2022-03-01", "2022-08-01", "2022-11-01"]),
            "CustomerID": [1, 2, 1],
            "PromotionID": ["PR001", None, "PR003"],
            "ProductID": ["P001", "P002", "P001"],
            "UnitsSold": [2, 1, 10],
        }
    )


@pytest.fixture
def master(fact, products, customers, promotions) -> pd.DataFrame:
    from src.data_cleaning import clean_customers, clean_fact
    from src.feature_engineering import build_master_table, compute_derived_columns

    cleaned_fact = clean_fact(fact)
    derived = compute_derived_columns(cleaned_fact, products, promotions)
    return build_master_table(derived, products, clean_customers(customers), promotions)
