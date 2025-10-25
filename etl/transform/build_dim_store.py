import pandas as pd
from pathlib import Path

def build_dim_store(raw_dir: str = "raw"):
    """Construye la dimensión de tiendas uniendo dirección y provincia."""
    store = pd.read_csv(Path(raw_dir) / "store.csv").rename(columns={"name": "store_name"})
    address = pd.read_csv(Path(raw_dir) / "address.csv")
    province = pd.read_csv(Path(raw_dir) / "province.csv").rename(columns={"name": "province_name", "code": "province_code"})

    df = (
        store.merge(address, on="address_id", how="left")
        .merge(province[["province_id", "province_name", "province_code"]], on="province_id", how="left")
        [["store_id", "store_name", "address_id", "line1", "line2", "city",
          "province_name", "province_code", "postal_code", "country_code"]]
        .drop_duplicates()
    )
    return df

if __name__ == "__main__":
    out = build_dim_store()
    Path("dw").mkdir(exist_ok=True)
    out.to_csv(Path("dw") / "dim_store.csv", index=False)
    print("✅ dim_store.csv creado en dw/")
