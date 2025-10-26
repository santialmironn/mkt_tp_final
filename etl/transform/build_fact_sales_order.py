import pandas as pd
from pathlib import Path

RAW = Path("raw")
DW  = Path("dw")

def build_fact_sales_order(raw_dir: Path = RAW):
    orders = pd.read_csv(raw_dir / "sales_order.csv", parse_dates=["order_date"])
    orders["date_id"] = orders["order_date"].dt.strftime("%Y%m%d").astype(int)
    fact = (
        orders[[
            "order_id",
            "date_id",
            "customer_id",
            "channel_id",
            "store_id",
            "billing_address_id",
            "shipping_address_id",
            "status",
            "currency_code",
            "subtotal",
            "tax_amount",
            "shipping_fee",
            "total_amount"
        ]]
        .sort_values(["date_id", "order_id"])
        .reset_index(drop=True)
    )
    return fact

if __name__ == "__main__":
    DW.mkdir(exist_ok=True)
    out = build_fact_sales_order()
    out.to_csv(DW / "fact_sales_order.csv", index=False)
    print("✅ fact_sales_order.csv creado en dw/")

