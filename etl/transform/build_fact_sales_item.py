import pandas as pd
from pathlib import Path

RAW = Path("raw")
DW  = Path("dw")

def build_fact_sales_item(raw_dir: Path = RAW, dw_dir: Path = DW):
    items  = pd.read_csv(raw_dir / "sales_order_item.csv")
    orders = pd.read_csv(raw_dir / "sales_order.csv", parse_dates=["order_date"])

    orders["date_id"] = orders["order_date"].dt.strftime("%Y%m%d").astype(int)

    ctx = orders[[
        "order_id", "date_id", "customer_id", "channel_id", "store_id"
    ]]

    dim_product  = pd.read_csv(dw_dir / "dim_product.csv")[["product_id", "product_sk"]]
    dim_customer = pd.read_csv(dw_dir / "dim_customer.csv")[["customer_id", "customer_sk"]]
    dim_channel  = pd.read_csv(dw_dir / "dim_channel.csv")[["channel_id", "channel_sk"]]
    dim_store    = pd.read_csv(dw_dir / "dim_store.csv")[["store_id", "store_sk"]]

    fact = (
        items.merge(ctx, on="order_id", how="left")
             .merge(dim_product, on="product_id", how="left")
             .merge(dim_customer, on="customer_id", how="left")
             .merge(dim_channel, on="channel_id", how="left")
             .merge(dim_store, on="store_id", how="left")
    )

    fact = (
        fact[[
            "order_item_id",
            "date_id",
            "product_sk", "customer_sk", "channel_sk", "store_sk",
            "quantity", "unit_price", "discount_amount", "line_total"
        ]]
        .sort_values(["date_id", "order_item_id"])
        .reset_index(drop=True)
    )

    return fact

if __name__ == "__main__":
    DW.mkdir(exist_ok=True)
    out = build_fact_sales_item()
    out.to_csv(DW / "fact_sales_item.csv", index=False)
    print("✅ fact_sales_item.csv creado en dw/")



