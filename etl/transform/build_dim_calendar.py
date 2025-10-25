import pandas as pd
from pathlib import Path

def build_dim_calendar(raw_dir: str = "raw"):
    """Construye la dimensión calendario en base a las fechas de pedidos."""
    orders = pd.read_csv(Path(raw_dir) / "sales_order.csv")
    order_dates = pd.to_datetime(orders["order_date"])

    start = (order_dates.min() - pd.Timedelta(days=30)).normalize()
    end = (order_dates.max() + pd.Timedelta(days=30)).normalize()
    dates = pd.date_range(start, end, freq="D")

    df = pd.DataFrame({
        "date": dates,
        "date_id": dates.strftime("%Y%m%d").astype(int),
        "year": dates.year,
        "quarter": dates.quarter,
        "month": dates.month,
        "month_name": dates.strftime("%B"),
        "day": dates.day,
        "weekday": dates.weekday + 1,
        "weekday_name": dates.strftime("%A"),
        "is_weekend": dates.weekday >= 5
    })
    return df

if __name__ == "__main__":
    out = build_dim_calendar()
    Path("dw").mkdir(exist_ok=True)
    out.to_csv(Path("dw") / "dim_calendar.csv", index=False)
    print("✅ dim_calendar.csv creado en dw/")
