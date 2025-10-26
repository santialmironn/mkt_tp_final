# etl/transform/build_fact_sales_item.py
import pandas as pd
from pathlib import Path

RAW = Path("raw")
DW  = Path("dw")

def build_fact_sales_item(raw_dir: Path = RAW):
    items  = pd.read_csv(raw_dir / "sales_order_item.csv")
    orders = pd.read_csv(raw_dir / "sales_order.csv", parse_dates=["order_date"])

    orders["date_id"] = orders["order_date"].dt.strftime("%Y%m%d").astype(int)

    ctx = orders[[
        "order_id", "date_id", "customer_id", "channel_id", "store_id"
    ]]

    fact = (
        items.merge(ctx, on="order_id", how="left")
             [[
                "order_item_id", "order_id",
                "date_id", "product_id",
                "customer_id", "channel_id", "store_id",
                "quantity", "unit_price", "discount_amount", "line_total"
             ]]
             .sort_values(["date_id","order_id","order_item_id"])
             .reset_index(drop=True)
    )
    return fact

if __name__ == "__main__":
    DW.mkdir(exist_ok=True)
    out = build_fact_sales_item()
    out.to_csv(DW / "fact_sales_item.csv", index=False)
    print("✅ fact_sales_item.csv (FKs mínimas + medidas) creado en dw/")

