# main.py
from pathlib import Path
from etl.extract.extract import extract_raw_data
from etl.load.load import load_data_to_dw

# importación de transformaciones
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

RAW = Path("raw")
DW  = Path("dw")

def main():
    print("\n=== INICIO PIPELINE ETL ===\n")

    print("📥 Extrayendo datos desde 'raw/'...")
    data = extract_raw_data(RAW)

    print("\nCreando dimensiones...")
    dim_functions = [
        build_dim_channel,
        build_dim_customer,
        build_dim_product,
        build_dim_address,
        build_dim_store,
        build_dim_calendar
    ]
    for func in dim_functions:
        df = func()
        print(f"✅ {func.__name__} completada ({len(df)} filas)")

    print("\nCreando tablas de hechos...")
    fact_functions = [
        build_fact_sales_order,
        build_fact_sales_item,
        build_fact_payment,
        build_fact_shipment,
        build_fact_web_session,
        build_fact_nps_response
    ]
    for func in fact_functions:
        df = func()
        print(f"✅ {func.__name__} completada ({len(df)} filas)")

    print("\n💾 Verificando carga en 'dw/'...")
    load_data_to_dw({}, DW)

    print("\n=== ✅ PIPELINE COMPLETADA ===\n")

if __name__ == "__main__":
    main()
