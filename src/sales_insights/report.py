from datetime import datetime, timezone
from pathlib import Path

from sales_insights.analysis import (
    load_data,
    monthly_revenue,
    revenue_by_region,
    top_products,
)

DATA_PATH = Path("data/sales.csv")
OUTPUT_PATH = Path("site/index.html")


def build_report(df):
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sections = [
        ("Revenue by Region", revenue_by_region(df)),
        ("Top Products", top_products(df)),
        ("Monthly Revenue", monthly_revenue(df)),
    ]
    body = "".join(
        f"<h2>{title}</h2>{series.to_frame().to_html()}" for title, series in sections
    )
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Sales Insights</title></head>
<body style="font-family: sans-serif; max-width: 700px; margin: auto;">
<h1>Sales Insights Report</h1>
<p>Total revenue: ${df["revenue"].sum():,.2f}</p>
{body}
<p><small>Generated: {generated}</small></p>
</body>
</html>"""


def main():
    df = load_data(DATA_PATH)
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text(build_report(df), encoding="utf-8")
    print(f"Report written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
