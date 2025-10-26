# etl/extract/extract.py
import pandas as pd
from pathlib import Path

def extract_raw_data(raw_dir: str = "raw") -> dict[str, pd.DataFrame]:
    raw_path = Path(raw_dir)
    if not raw_path.exists():
        raise FileNotFoundError(f"❌ No existe la carpeta: {raw_path.resolve()}")

    data: dict[str, pd.DataFrame] = {}
    for file in sorted(raw_path.glob("*.csv")):
        df = pd.read_csv(file)
        data[file.stem] = df
        print(f"📥 '{file.name}' leído ({len(df)} filas, {len(df.columns)} cols)")

    print(f"\n✅ {len(data)} archivos leídos desde {raw_path.resolve()}")
    return data

if __name__ == "__main__":
    print("\n=== 🚀 Iniciando extracción de datos ===")
    data = extract_raw_data("raw")
    print("Archivos cargados:", list(data.keys()))
    print("=== ✅ Extracción completada ===\n")
