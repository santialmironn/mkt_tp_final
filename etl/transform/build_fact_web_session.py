import pandas as pd
from pathlib import Path

RAW = Path("raw")
DW  = Path("dw")

def build_fact_web_session(raw_dir: Path = RAW):
    sess = pd.read_csv(raw_dir / "web_session.csv", parse_dates=["started_at","ended_at"])

    sess["started_date_id"] = sess["started_at"].dt.strftime("%Y%m%d").astype(int)
    sess["ended_date_id"]   = sess["ended_at"].dt.strftime("%Y%m%d").astype("Int64")
    sess["started_at_time"] = sess["started_at"].dt.strftime("%H:%M:%S")
    sess["ended_at_time"]   = sess["ended_at"].dt.strftime("%H:%M:%S")

    fact = (
        sess[[
            "session_id",
            "started_date_id","ended_date_id",
            "customer_id",
            "source","device",
            "started_at_time","ended_at_time"
        ]]
        .sort_values(["started_date_id","session_id"])
        .reset_index(drop=True)
    )
    return fact

if __name__ == "__main__":
    DW.mkdir(exist_ok=True)
    out = build_fact_web_session()
    out.to_csv(DW / "fact_web_session.csv", index=False)
    print("✅ fact_web_session.csv creado en dw/")
