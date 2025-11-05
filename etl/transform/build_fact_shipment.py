import pandas as pd
from pathlib import Path

RAW = Path("raw")
DW  = Path("dw")

def build_fact_shipment(raw_dir: Path = RAW, dw_dir: Path = DW):
    ship   = pd.read_csv(raw_dir / "shipment.csv", parse_dates=["shipped_at","delivered_at"])
    orders = pd.read_csv(raw_dir / "sales_order.csv")

    ship["shipped_date_id"]   = ship["shipped_at"].dt.strftime("%Y%m%d").astype("Int64")
    ship["delivered_date_id"] = ship["delivered_at"].dt.strftime("%Y%m%d").astype("Int64")
    ship["shipped_at_time"]   = ship["shipped_at"].dt.strftime("%H:%M:%S")
    ship["delivered_at_time"] = ship["delivered_at"].dt.strftime("%H:%M:%S")

    ctx = orders[["order_id","customer_id","channel_id","store_id","shipping_address_id"]]
    fact = ship.merge(ctx, on="order_id", how="left")

    # cargar dimensiones con SK
    dim_customer = pd.read_csv(dw_dir / "dim_customer.csv")[["customer_id", "customer_sk"]]
    dim_channel  = pd.read_csv(dw_dir / "dim_channel.csv")[["channel_id", "channel_sk"]]
    dim_store    = pd.read_csv(dw_dir / "dim_store.csv")[["store_id", "store_sk"]]
    dim_address  = pd.read_csv(dw_dir / "dim_address.csv")[["address_id", "address_sk"]]

    fact = (
        fact
        .merge(dim_customer, on="customer_id", how="left")
        .merge(dim_channel, on="channel_id", how="left")
        .merge(dim_store, on="store_id", how="left")
        .merge(dim_address, left_on="shipping_address_id", right_on="address_id", how="left")
        .rename(columns={"address_sk": "shipping_address_sk"})
    )

    fact = (
        fact[[
            "shipment_id",
            "shipped_date_id","delivered_date_id",
            "customer_sk","channel_sk","store_sk","shipping_address_sk",
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

