import pandas as pd
from pathlib import Path

def build_dim_customer(raw_dir: str = "raw"):
    """Construye la dimensión de clientes con surrogate key."""
    df = pd.read_csv(Path(raw_dir) / "customer.csv")
    df = df[["customer_id", "email", "first_name", "last_name", "phone", "status", "created_at"]]
    df = df.drop_duplicates().reset_index(drop=True)

    df.insert(0, "customer_sk", range(1, len(df) + 1))

    return df

if __name__ == "__main__":
    out = build_dim_customer()
    Path("dw").mkdir(exist_ok=True)
    out.to_csv(Path("dw") / "dim_customer.csv", index=False)
    print("✅ dim_customer.csv creado en dw/")
