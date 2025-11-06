# Proyecto EcoBottle - Diseño e Implementación de un Data Warehouse Comercial


## 1. Introducción y Objetivos
El objetivo principal de este proyecto es **diseñar e implementar un mini ecosistema de datos comercial**, aplicando un proceso **ETL completo (Extracción, Transformación y Carga)** que permita la creación de un **modelo dimensional (esquema estrella)** para análisis y reporting.

El caso de negocio corresponde a **EcoBottle**, una empresa dedicada a la venta de botellas reutilizables a través de canales físicos y digitales.  

El propósito es centralizar la información de distintas fuentes, **desnormalizar las tablas operativas** y construir un **Data Warehouse (DW)** optimizado para consultas analíticas.

---

## 2. Flujo de Datos (ETL)
El proyecto implementa un flujo ETL con las siguientes fases:

1. **Extracción (Extract):**  
   Se leen los archivos `.csv` provenientes de sistemas operacionales desde el directorio `raw/`.

2. **Transformación (Transform):**  
   Es la etapa más importante del proceso, donde se aplica el **modelado dimensional** según la metodología de **Kimball**:
   - **Limpieza de datos:** estandarización de formatos de fecha, eliminación de duplicados y corrección de valores nulos.
   - **Desnormalización:** combinación de tablas normalizadas en estructuras planas que representan entidades de negocio.
   - **Creación de Dimensiones (Dims):** se generan las tablas maestras (`dim_product`, `dim_customer`, `dim_channel`, etc.) asignando una **clave sustituta (SK)**.
   - **Creación de Hechos (Facts):** se construyen las tablas de hechos (`fact_order`, `fact_payment`, etc.) vinculando las dimensiones mediante sus claves SK.

3. **Carga (Load):**  
   Los DataFrames finales del proceso ETL se exportan como archivos `.csv` dentro del directorio `dw/`, listos para ser utilizados en herramientas de BI.

---

## 3. ⚙️ Instrucciones de Ejecución

Se deberan seguir estos pasos para replicar el proceso ETL y generar los archivos finales:

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/santialmironn/mkt_tp_final.git
   cd mkt_tp_final
2. **Crear entorno virtual**
   ```bash
   # macOS / Linux
   python -m venv venv
   source venv/bin/activate 

   # Windows 
   python -m venv venv
   .\venv\Scripts\activate    
3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
4. **Ejecutar el proceso ETL**
   ```bash
   python main.py
---

## 4. Modelo de Datos (Esquema Estrella)
El modelo dimensional está conformado por **seis esquemas estrella**, cada uno asociado a un proceso clave del negocio.

###  Fact_Sales_Order  
📦 Representa las órdenes o pedidos de los clientes.

![Fact_Order](assets/fact_sales_order.png)

### Fact_Sales_Item  
🧾 Detalle de los productos vendidos por pedido.

![Fact_Order_Item](assets/fact_sales_item.png)

### Fact_Shipment  
🚚 Información de los envíos y entregas.

![Fact_Shipment](assets/fact_shipment.png)

### Fact_Nps_Response  
💬 Respuestas de encuestas de satisfacción (NPS).

![Fact_Nps_Response](assets/fact_nps_response.png)

### Fact_Web_Session  
🌐 Registro de sesiones web y comportamiento del cliente.

![Fact_Web_Session](assets/fact_web_session.png)

### Fact_Payment  
💰 Pagos realizados por los clientes.

![Fact_Payment](assets/fact_payment.png)

---


   