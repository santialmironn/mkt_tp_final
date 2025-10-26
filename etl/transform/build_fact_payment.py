# etl/transform/build_fact_payment.py
import pandas as pd
from pathlib import Path

RAW = Path("raw")
DW  = Path("dw")

def build_fact_payment(raw_dir: Path = RAW):
    pay    = pd.read_csv(raw_dir / "payment.csv", parse_dates=["paid_at"])
    orders = pd.read_csv(raw_dir / "sales_order.csv")

    pay["paid_date_id"] = pay["paid_at"].dt.strftime("%Y%m%d").astype("Int64")
    pay["paid_at_time"] = pay["paid_at"].dt.strftime("%H:%M:%S")

    ctx = orders[[
        "order_id",
        "customer_id", "channel_id", "store_id",
        "billing_address_id"
    ]]

    fact = (
        pay.merge(ctx, on="order_id", how="left")
           [[
               "payment_id",
               "paid_date_id",
               "customer_id", "channel_id", "store_id",
               "billing_address_id",
               "amount",
               "method", "status", "transaction_ref",
               "paid_at_time"
           ]]
           .sort_values(["paid_date_id", "payment_id"])
           .reset_index(drop=True)
    )
    return fact

if __name__ == "__main__":
    DW.mkdir(exist_ok=True)
    out = build_fact_payment()
    out.to_csv(DW / "fact_payment.csv", index=False)
    print("✅ fact_payment.csv creado en dw/")


