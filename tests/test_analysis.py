import pandas as pd
import pytest

from sales_insights.analysis import (
    load_data,
    monthly_revenue,
    revenue_by_region,
    top_products,
)


@pytest.fixture
def sample_df():
    # Revenues: 2*10=20 (East, Jan), 1*50=50 (West, Jan), 4*10=40 (East, Feb)
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2026-01-10", "2026-01-20", "2026-02-05"]),
            "region": ["East", "West", "East"],
            "product": ["Widget", "Gadget", "Widget"],
            "quantity": [2, 1, 4],
            "unit_price": [10.0, 50.0, 10.0],
        }
    )
    df["revenue"] = df["quantity"] * df["unit_price"]
    return df


def test_revenue_by_region(sample_df):
    result = revenue_by_region(sample_df)
    assert result["East"] == 60
    assert result["West"] == 50
    assert result.index[0] == "East"  # sorted highest first


def test_top_products_respects_n(sample_df):
    result = top_products(sample_df, n=1)
    assert len(result) == 1
    assert result.index[0] == "Widget"


def test_monthly_revenue(sample_df):
    result = monthly_revenue(sample_df)
    assert list(result.values) == [70, 40]


def test_load_data_computes_revenue(tmp_path):
    csv = tmp_path / "sales.csv"
    csv.write_text(
        "date,region,product,quantity,unit_price\n2026-01-01,East,Widget,3,10.0\n"
    )
    df = load_data(csv)
    assert df["revenue"].iloc[0] == 30


def test_load_data_rejects_missing_columns(tmp_path):
    csv = tmp_path / "bad.csv"
    csv.write_text("date,region,product,quantity\n2026-01-01,East,Widget,3\n")
    with pytest.raises(ValueError, match="unit_price"):
        load_data(csv)


def test_real_dataset_total():
    df = load_data("data/sales.csv")
    assert df["revenue"].sum() == 3131
