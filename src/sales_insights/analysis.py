import pandas as pd

REQUIRED_COLUMNS = {"date", "region", "product", "quantity", "unit_price"}


def load_data(path):
    df = pd.read_csv(path, parse_dates=["date"])
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    df["revenue"] = df["quantity"] * df["unit_price"]
    return df


def revenue_by_region(df):
    return df.groupby("region")["revenue"].sum().sort_values(ascending=False)


def top_products(df, n=3):
    return df.groupby("product")["revenue"].sum().nlargest(n)


def monthly_revenue(df):
    return df.groupby(df["date"].dt.to_period("M"))["revenue"].sum()
