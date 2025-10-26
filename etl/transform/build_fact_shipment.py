import pandas as pd
from pathlib import Path

RAW = Path("raw")
DW  = Path("dw")

def build_fact_shipment(raw_dir: Path = RAW):
    ship   = pd.read_csv(raw_dir / "shipment.csv", parse_dates=["shipped_at","delivered_at"])
    orders = pd.read_csv(raw_dir / "sales_order.csv")

    ship["shipped_date_id"]   = ship["shipped_at"].dt.strftime("%Y%m%d").astype("Int64")
    ship["delivered_date_id"] = ship["delivered_at"].dt.strftime("%Y%m%d").astype("Int64")
    ship["shipped_at_time"]   = ship["shipped_at"].dt.strftime("%H:%M:%S")
    ship["delivered_at_time"] = ship["delivered_at"].dt.strftime("%H:%M:%S")

    ctx = orders[["order_id","customer_id","channel_id","store_id","shipping_address_id"]]
    fact = ship.merge(ctx, on="order_id", how="left")

    fact = (
        fact[[
            "shipment_id",
            "shipped_date_id","delivered_date_id",
            "customer_id","channel_id","store_id","shipping_address_id",
            "carrier","tracking_number","status",
            "shipped_at_time","delivered_at_time"
        ]]
        .sort_values(["shipped_date_id","shipment_id"])
        .reset_index(drop=True)
    )
    return fact

if __name__ == "__main__":
    DW.mkdir(exist_ok=True)
    out = build_fact_shipment()
    out.to_csv(DW / "fact_shipment.csv", index=False)
    print("✅ fact_shipment.csv creado en dw/")
