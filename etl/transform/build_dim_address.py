import pandas as pd
from pathlib import Path

def build_dim_address(raw_dir: str = "raw"):
    """Construye la dimensión de direcciones desnormalizando con provincias."""
    address = pd.read_csv(Path(raw_dir) / "address.csv")
    province = pd.read_csv(Path(raw_dir) / "province.csv").rename(columns={"name": "province_name", "code": "province_code"})

    df = (
        address.merge(province[["province_id", "province_name", "province_code"]], on="province_id", how="left")
        [["address_id", "line1", "line2", "city", "province_name", "province_code",
          "postal_code", "country_code", "created_at"]]
        .drop_duplicates()
    )
    return df

if __name__ == "__main__":
    out = build_dim_address()
    Path("dw").mkdir(exist_ok=True)
    out.to_csv(Path("dw") / "dim_address.csv", index=False)
    print("✅ dim_address.csv creado en dw/")
