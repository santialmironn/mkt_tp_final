import pandas as pd
from pathlib import Path

RAW = Path("raw")
DW  = Path("dw")

def build_fact_nps_response(raw_dir: Path = RAW, dw_dir: Path = DW):
    nps = pd.read_csv(raw_dir / "nps_response.csv", parse_dates=["responded_at"])

    nps["responded_date_id"] = nps["responded_at"].dt.strftime("%Y%m%d").astype(int)
    nps["responded_at_time"] = nps["responded_at"].dt.strftime("%H:%M:%S")

    dim_customer = pd.read_csv(dw_dir / "dim_customer.csv")[["customer_id", "customer_sk"]]
    dim_channel  = pd.read_csv(dw_dir / "dim_channel.csv")[["channel_id", "channel_sk"]]

    fact = (
        nps.merge(dim_customer, on="customer_id", how="left")
           .merge(dim_channel, on="channel_id", how="left")
    )

    fact = (
        fact[[
            "nps_id",
            "responded_date_id",
            "customer_sk", "channel_sk",
            "score", "comment", "responded_at_time"
        ]]
        .sort_values(["responded_date_id", "nps_id"])
        .reset_index(drop=True)
    )

    return fact

if __name__ == "__main__":
    DW.mkdir(exist_ok=True)
    out = build_fact_nps_response()
    out.to_csv(DW / "fact_nps_response.csv", index=False)
    print("✅ fact_nps_response.csv creado en dw/")
