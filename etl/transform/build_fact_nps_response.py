import pandas as pd
from pathlib import Path

RAW = Path("raw")
DW  = Path("dw")

def build_fact_nps_response(raw_dir: Path = RAW):
    nps = pd.read_csv(raw_dir / "nps_response.csv", parse_dates=["responded_at"])

    nps["responded_date_id"] = nps["responded_at"].dt.strftime("%Y%m%d").astype(int)
    nps["responded_at_time"] = nps["responded_at"].dt.strftime("%H:%M:%S")

    fact = (
        nps[[
            "nps_id",
            "responded_date_id",
            "customer_id",
            "channel_id",
            "score","comment",
            "responded_at_time"
        ]]
        .sort_values(["responded_date_id","nps_id"])
        .reset_index(drop=True)
    )
    return fact

if __name__ == "__main__":
    DW.mkdir(exist_ok=True)
    out = build_fact_nps_response()
    out.to_csv(DW / "fact_nps_response.csv", index=False)
    print("✅ fact_nps_response.csv creado en dw/")
