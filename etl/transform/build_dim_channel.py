# etl/transform/build_dim_channel.py
import pandas as pd
from pathlib import Path
from etl.load.load import load_data_to_dw

def build_dim_channel(raw_dir: str = "raw", dw_dir: str = "dw"):
    df = pd.read_csv(Path(raw_dir) / "channel.csv")
    df = df.rename(columns={"name": "channel_name", "code": "channel_code"})
    df = df[["channel_id", "channel_code", "channel_name"]].drop_duplicates()
    load_data_to_dw({"dim_channel": df}, dw_dir)
    return df

if __name__ == "__main__":
    build_dim_channel()
