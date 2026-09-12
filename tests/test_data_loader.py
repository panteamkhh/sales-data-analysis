import pandas as pd
import pytest

from src.config import DATA_FILE
from src.data_loader import FACT_COLUMNS, load_data


def test_load_data_reads_all_tables():
    if not DATA_FILE.exists():
        pytest.skip("sample workbook not available")
    data = load_data()
    assert set(data) == {"fact", "customers", "products", "promotions"}
    assert list(data["fact"].columns) == FACT_COLUMNS
    assert len(data["fact"]) > 0
    assert {"Customer ID", "City"}.issubset(data["customers"].columns)
    assert {"ProductID", "Price (INR)"}.issubset(data["products"].columns)


def test_load_data_accepts_explicit_path():
    if not DATA_FILE.exists():
        pytest.skip("sample workbook not available")
    data = load_data(DATA_FILE)
    assert isinstance(data["fact"], pd.DataFrame)


def test_load_data_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_data("does_not_exist.xlsx")
