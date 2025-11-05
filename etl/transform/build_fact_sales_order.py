import pandas as pd
from pathlib import Path

RAW = Path("raw")
DW  = Path("dw")

def build_fact_sales_order(raw_dir: Path = RAW, dw_dir: Path = DW):
    orders = pd.read_csv(raw_dir / "sales_order.csv", parse_dates=["order_date"])
    orders["date_id"] = orders["order_date"].dt.strftime("%Y%m%d").astype(int)

    dim_customer = pd.read_csv(dw_dir / "dim_customer.csv")[["customer_id", "customer_sk"]]
    dim_channel  = pd.read_csv(dw_dir / "dim_channel.csv")[["channel_id", "channel_sk"]]
    dim_store    = pd.read_csv(dw_dir / "dim_store.csv")[["store_id", "store_sk"]]
    dim_address  = pd.read_csv(dw_dir / "dim_address.csv")[["address_id", "address_sk"]]

    fact = (
        orders
        .merge(dim_customer, on="customer_id", how="left")
        .merge(dim_channel, on="channel_id", how="left")
        .merge(dim_store, on="store_id", how="left")
    )

    fact = fact.merge(
        dim_address,
        left_on="billing_address_id",
        right_on="address_id",
        how="left"
    )
    fact = fact.rename(columns={"address_sk": "billing_address_sk"})

    fact = fact.merge(
        dim_address,
        left_on="shipping_address_id",
        right_on="address_id",
        how="left",
        suffixes=("", "_ship")
    )
    fact = fact.rename(columns={"address_sk": "shipping_address_sk"})

    fact = (
        fact[[
            "order_id",
            "date_id",
            "customer_sk", "channel_sk", "store_sk",
            "billing_address_sk", "shipping_address_sk",
            "status", "currency_code",
            "subtotal", "tax_amount", "shipping_fee", "total_amount"
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
