import pandas as pd
from pathlib import Path

def build_dim_product(raw_dir: str = "raw"):
    """Construye la dimensión de productos uniendo con categorías."""
    product = pd.read_csv(Path(raw_dir) / "product.csv").rename(columns={"name": "product_name"})
    category = pd.read_csv(Path(raw_dir) / "product_category.csv").rename(columns={"name": "category_name"})

    df = (
        product.merge(category[["category_id", "category_name", "parent_id"]], on="category_id", how="left")
        [["product_id", "sku", "product_name", "category_id", "category_name",
          "parent_id", "list_price", "status", "created_at"]]
        .drop_duplicates()
    )
    return df

if __name__ == "__main__":
    out = build_dim_product()
    Path("dw").mkdir(exist_ok=True)
    out.to_csv(Path("dw") / "dim_product.csv", index=False)
    print("✅ dim_product.csv creado en dw/")
