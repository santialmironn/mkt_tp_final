import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT))

from etl.extract.extract import extract_raw_data

from etl.transform.build_dim_channel import build_dim_channel
from etl.transform.build_dim_customer import build_dim_customer
from etl.transform.build_dim_product import build_dim_product
from etl.transform.build_dim_address import build_dim_address
from etl.transform.build_dim_store import build_dim_store
from etl.transform.build_dim_calendar import build_dim_calendar

from etl.transform.build_fact_sales_order import build_fact_sales_order
from etl.transform.build_fact_sales_item import build_fact_sales_item
from etl.transform.build_fact_payment import build_fact_payment
from etl.transform.build_fact_shipment import build_fact_shipment
from etl.transform.build_fact_web_session import build_fact_web_session
from etl.transform.build_fact_nps_response import build_fact_nps_response

DW = ROOT / "dw"


def main():
    print("\n=== 🚀 INICIO PIPELINE ETL ===\n")

    DW.mkdir(exist_ok=True)

    print("📥 Extrayendo datos desde 'raw/'...")
    extract_raw_data("raw")  

    print("\n🧱 Construyendo dimensiones...")
    dim_funcs = [
        ("dim_channel", build_dim_channel),
        ("dim_customer", build_dim_customer),
        ("dim_product", build_dim_product),
        ("dim_address", build_dim_address),
        ("dim_store", build_dim_store),
        ("dim_calendar", build_dim_calendar),
    ]

    for name, func in dim_funcs:
        df = func()
        out_path = DW / f"{name}.csv"
        df.to_csv(out_path, index=False)  # siempre actualiza
        print(f"✅ {name} actualizado ({len(df)} filas)")


    print("\n📊 Construyendo tablas de hechos...")
    fact_funcs = [
        ("fact_sales_order",   build_fact_sales_order),
        ("fact_sales_item",    build_fact_sales_item),
        ("fact_payment",       build_fact_payment),
        ("fact_shipment",      build_fact_shipment),
        ("fact_web_session",   build_fact_web_session),
        ("fact_nps_response",  build_fact_nps_response),
    ]

    for name, func in fact_funcs:
        df = func() 
        out_path = DW / f"{name}.csv"
        df.to_csv(out_path, index=False)
        print(f"✅ {name} ({len(df)} filas)")

    print("\n=== ✅ PIPELINE COMPLETADA ===\n")


if __name__ == "__main__":
    main()
