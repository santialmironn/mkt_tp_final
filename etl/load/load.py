# etl/load/load.py
from pathlib import Path
import pandas as pd

def load_data_to_dw(dataframes: dict[str, pd.DataFrame], dw_dir: str | Path = "dw"):
    """
    Carga los DataFrames transformados al data warehouse (carpeta 'dw').

    - Crea la carpeta si no existe.
    - Guarda cada DataFrame como CSV usando su clave como nombre de archivo.
    - Omite tablas vacías o no válidas.
    """
    dw_path = Path(dw_dir)
    dw_path.mkdir(parents=True, exist_ok=True)

    print("\n=== 🚀 Iniciando carga de datos al DW ===")

    for name, df in dataframes.items():
        if not isinstance(df, pd.DataFrame):
            print(f"⚠️  '{name}' no es un DataFrame, se omite.")
            continue
        if df.empty:
            print(f"⚠️  '{name}' está vacío, se omite.")
            continue

        filename = f"{name}.csv"
        filepath = dw_path / filename
        df.to_csv(filepath, index=False)
        print(f"💾 {filename} guardado en {dw_path}/")

    print("=== ✅ Carga completada correctamente ===\n")


