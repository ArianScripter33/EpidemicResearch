# Protocolo de Deep Research V3  

Arquitectura de Extracción de Datos Zoonóticos y Shocks Epidemiológicos (México / Internacional)



A continuación presento un diseño operativo para tu Data Warehouse relacional, organizado por vectores. Para cada punto incluyo:

- Ruta/URL institucional.
- Formato del dato.
- Estrategia de extracción y pseudocódigo en Python.
- Cómo encaja en el modelo relacional para vincular: **ganado – salud humana – impacto económico**.

---

## Vector 1 – Tuberculosis Bovina (Puente Zoonótico Animal–Humano)

### 1.1 Dato Animal (SENASICA / SADER)

#### 1.1.1 Hatos libres y prevalencia (aproximación a prevalencia de M. bovis)

**a) Hatos libres de tuberculosis bovina (datos abiertos)**  

- **Portal de datos abiertos**:  
  - Ficha de conjunto:  
    - <https://www.datos.gob.mx/dataset/constatacion_hatos_libres_tuberculosis_bovina> [1]  
  - Descargas CSV identificadas:  
    - Diciembre 2025:  
      `https://repodatos.atdt.gob.mx/api_update/senasica/constatacion_hatos_libres_tuberculosis_bovina/hatos_libres_tuberculosis.csv`  
    - Junio 2025:  
      `https://repodatos.atdt.gob.mx/api_update/senasica/constatacion_hatos_libres_tuberculosis_bovina/47_tuberculosis-bovina.csv` [1]  

- **Formato**: CSV.  
  El dataset integra **número de hatos certificados como libres de TB bovina**, desagregados por **estado** y **tipo de producción**.

- **Uso epidemiológico**:  
  - Para aproximar prevalencia a nivel estatal puedes combinar:
    - `hatos_totales` (otra fuente, p.ej. censo pecuario / SIAP).
    - `hatos_libres` (este CSV).  
  - Prevalencia aproximada = 1 − (hatos_libres / hatos_totales).

**Pseudocódigo (ingesta de CSV de hatos libres)**

```python
import requests
import pandas as pd

CSV_URLS = [
    "https://repodatos.atdt.gob.mx/api_update/senasica/constatacion_hatos_libres_tuberculosis_bovina/hatos_libres_tuberculosis.csv",
    "https://repodatos.atdt.gob.mx/api_update/senasica/constatacion_hatos_libres_tuberculosis_bovina/47_tuberculosis-bovina.csv",
]

def ingest_hatos_libres():
    frames = []
    for url in CSV_URLS:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        df = pd.read_csv(pd.io.common.BytesIO(r.content))
        df["source_url"] = url
        frames.append(df)
    df_all = pd.concat(frames, ignore_index=True)
    # Normalizar nombres de estados, tipos de producción, etc.
    return df_all
```

**Modelo relacional sugerido**

- `dim_estado(estado_id, nombre_estado, region)`  
- `dim_tiempo(fecha, año, trimestre, mes)`  
- `fact_hatos_tb(estado_id, fecha_id, tipo_produccion, num_hatos_libres, fuente)`

#### 1.1.2 Cuarentenas, despoblación y sacrificios (por estado)

SENASICA publica boletines trimestrales de **cuarentenas por TB bovina** que, típicamente, incluyen número de **hatos en cuarentena, zona buffer, despoblación**.

- **Cuarentenas 2024**:  
  <https://www.gob.mx/senasica/documentos/cuarentenas-tuberculosis-bovina-2024?state=published> [2]  
  Descargas identificadas (PDF):

  - 4° trim. 2024:  
    `https://www.gob.mx/cms/uploads/attachment/file/979992/1._Cuarentenas_Tb_4to_tmt.pdf`
  - 3er trim. 2024:  
    `https://www.gob.mx/cms/uploads/attachment/file/958502/1_Cuarentenas_Tercer_2024.pdf`
  - 2° trim. 2024:  
    `https://www.gob.mx/cms/uploads/attachment/file/935619/1_CUARENTENAS_2DO_TRIMESTRE_2024.pdf`
  - 1er trim. 2024:  
    `https://www.gob.mx/cms/uploads/attachment/file/914491/1_CUARENTENAS_Primer_2024.pdf` [2]  

- **Formato**: PDF (en muchos casos con tablas escaneadas).

- **Estrategia de extracción**:
  - Si las tablas son texto real: `camelot` o `tabula-py` con `flavor="stream"` o `"lattice"`.
  - Si son imágenes escaneadas: `pytesseract` + `opencv` para OCR, seguido de regex para parsear columnas (estado, #hatos, #cabezas, tipo de acción).

**Pseudocódigo (extracción de tablas de PDFs de cuarentenas)**

```python
import camelot
import pandas as pd

PDFS_CUARENTENAS = [
    "1._Cuarentenas_Tb_4to_tmt.pdf",
    "1_Cuarentenas_Tercer_2024.pdf",
    # ...
]

def extract_cuarentenas(pdf_path):
    tables = camelot.read_pdf(pdf_path, pages="all", flavor="stream")
    dfs = [t.df for t in tables]
    df = pd.concat(dfs, ignore_index=True)
    # Limpiar encabezados, renombrar columnas, convertir a numérico
    return df

def pipeline_cuarentenas():
    all_frames = []
    for pdf in PDFS_CUARENTENAS:
        df = extract_cuarentenas(pdf)
        df["source_pdf"] = pdf
        all_frames.append(df)
    return pd.concat(all_frames, ignore_index=True)
```

**Modelo relacional sugerido**

- `fact_cuarentenas_tb(estado_id, fecha_id, num_hatos_cuarentena, num_animales, tipo_medida, fuente_pdf)`

---

### 1.2 Dato Humano (SINAIS / DGE / INSP)

#### 1.2.1 Acceso a morbilidad y mortalidad por CIE‑10 (incluida TB)

La vía más directa y trazable para analítica es **Anuarios de Morbilidad** y sus datos abiertos:

- **Portal datos abiertos DGE**:  
  <https://www.gob.mx/salud/documentos/datos-abiertos-152127> [3]  

- **Enlaces de datos estructurados** (ejemplos):
  - Anuario de Morbilidad 2015:  
    `https://epidemiologia.salud.gob.mx/anuario/datos_abiertos/Anuario_2015.zip`
  - Anuario 2016:  
    `https://epidemiologia.salud.gob.mx/anuario/datos_abiertos/Anuario_2016.zip`
  - Anuario 2017:  
    `https://epidemiologia.salud.gob.mx/anuario/datos_abiertos/Anuario_2017.zip` [3]  

- **Formato**: ZIP que contiene CSV (se indica explícitamente que los archivos son CSV).

Dentro de los CSV puedes filtrar por códigos CIE‑10:

- Tuberculosis respiratoria: `A15–A16`.
- Otras TB: `A17–A19`.
- Para zoonosis específica por M. bovis no hay un código separado en CIE‑10 estándar; TB por M. bovis se clasifica bajo los códigos TB generales. Si se requiere especificidad “zoonótica” tendrás que acotar usando variables auxiliares (ocupación, región ganadera, etc.) o usar definiciones propias.

**Pseudocódigo (descarga y filtrado de TB)**

```python
import zipfile, io, requests, pandas as pd

def load_anuario_year(year):
    url = f"https://epidemiologia.salud.gob.mx/anuario/datos_abiertos/Anuario_{year}.zip"
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        # Nombres típicos, pueden variar ligeramente según año
        morb_name = [f for f in z.namelist() if "Morbilidad" in f][0]
        df_morb = pd.read_csv(z.open(morb_name), encoding="latin1")
    return df_morb

def filter_tb(df_morb):
    tb_mask = df_morb["CIE10"].str.startswith(("A15","A16","A17","A18","A19"))
    return df_morb[tb_mask]

# Uso:
# df_morb_2022 = load_anuario_year(2022)
# df_tb_2022 = filter_tb(df_morb_2022)
```

#### 1.2.2 Cubos Dinámicos (SINAIS / DGIS)

- **Página general de Cubos Dinámicos DGIS**:  
  <http://www.dgis.salud.gob.mx/contenidos/basesdedatos/BD_Cubos_gobmx.html> [4]  

- **Plataforma SINBA para instalación local de cubos**:  
  <https://sinba.salud.gob.mx/CubosDinamicos> [5]  
  Aquí se documenta la instalación de componentes OLE DB y OWC (Office Web Components) para explotar cubos OLAP de forma local.

- **Formato / acceso**:
  - No se exponen endpoints HTTP/REST directos ni descarga masiva en CSV.
  - El uso previsto es **cliente MS Office + OLE DB** para consultas MDX.
  - Para una automatización avanzada podrías:
    1. Instalar los cubos en un servidor Windows con SQL Server Analysis Services.
    2. Conectarte vía `pyodbc` u `adodbapi` a la base analítica y exportar vistas a CSV.

Dado que ya tienes acceso a los *Anuarios CSV*, recomiendo usar **Anuarios** como backend principal y usar Cubos sólo de validación.

---

### 1.3 Dato Económico – Indemnización por Tuberculosis Bovina

No encontré un **tabulador único y explícito** publicado en CSV con “\$ por vaca sacrificada por TB”; la información está dispersa en:

1. **Normativa de campañas y acuerdos**  
   - Acuerdo para la Campaña Nacional contra TB bovina (SADER/SENASICA):  
     Página: <https://www.gob.mx/senasica/documentos/acuerdo-para-la-operacion-de-la-campana-nacional-contra-la-tuberculosis-bovina-mycobacterium-bovis?state=published> [6]  
     PDF DOF:  
     `https://www.gob.mx/cms/uploads/attachment/file/964169/2024_12_30_MAT_sader_-_Acuerdo_TB.pdf` [7]  
     → Aquí se menciona **indemnización** como parte del paquete de medidas, pero no se especifican montos exactos por animal (documento principalmente normativo).

2. **Seguros pecuarios de Fondo de Aseguramiento**  
   - Condiciones generales del seguro pecuario (ejemplo nacional):  
     `https://www.gob.mx/cms/uploads/attachment/file/71582/DC-S0074-0111-2016_Pecuario.pdf` [8]  
     Contiene:
     - Definición de suma asegurada por unidad de riesgo.
     - Regla de indemnización: suma asegurada − deducible − salvamento.
     - Topes (p.ej. hasta el 2% de animales asegurados para ciertas causas).
   - Presentación fondos de aseguramiento (incluye “Seguro de tuberculosis bovina”):  
     `https://www.gob.mx/cms/uploads/attachment/file/72238/PRESENTACION_CONSTITUCION_DE_FONDOS.pdf` [9]

3. **Tabla de equivalencias de ganado (para valorar animales)**  
   - DOF – Tabla de equivalencias de ganado mayor y menor:  
     <http://www.dof.gob.mx/nota_detalle.php?codigo=2054508&fecha=02/05/2000> [10]  
     Ejemplos:
     - 1 vaca de 400–450 kg → 1.0 unidad animal.
     - 1 toro adulto → 1.25 UA, etc.  

**Uso práctico para tu modelo**:

- Definir un **valor por Unidad Animal (UA)** según precios de mercado (p.ej. series de precios de bovino de SIAP).
- Calcular indemnización aproximada:

```python
def indemnizacion_aproximada(num_animales, ua_factor, precio_por_ua, porcentaje=0.85):
    valor_base = num_animales * ua_factor * precio_por_ua
    return porcentaje * valor_base  # p.ej. 85% del valor del animal
```

**Modelo relacional sugerido**

- `dim_especie(tipo_ganado, ua_factor)`
- `fact_indemnizacion_tb(estado_id, fecha_id, num_animales_sacrificados, ua_factor, precio_ua, porc_indemnizacion, monto_estimado_mxn)`

---

## Vector 2 – Fiebre Aftosa (Shock Exógeno y Simulacros)

### 2.1 Dato Preventivo Nacional (CPA–SENASICA)

México es libre de fiebre aftosa; la información es de **planificación y respuesta** (no de casos).

**Documentos clave de CPA/SENASICA**

- **Plan de Acción Inmediata – Fiebre Aftosa**:  
  PDF: `https://dj.senasica.gob.mx/Contenido/files/2021/julio/PAIFiebreAftosa07-06-21_e83a982d-b6b5-40b0-a3ae-41321c88bbfa.pdf` [11]  
  Incluye:
  - Descripción de la enfermedad como exótica.
  - Estructura de respuesta, centros de operación, protocolos, fases.

- **Manuales CPA (emergencias zoosanitarias, útil para todos los simulacros)**:  
  Página: <https://www.gob.mx/senasica/documentos/manuales-cpa?state=published> [12]  
  PDFs relevantes:
  - *Plan de Emergencia para la Peste Porcina Africana* (aunque no aftosa, sí sirve como plantilla de megasimulacro):  
    `https://www.gob.mx/cms/uploads/attachment/file/660359/Plan_de_emergencia_CPA_FINAL_compressed__1_.pdf` [12]  
  - Manual de limpieza y desinfección.  
  - Manual de sacrificio humanitario y disposición sanitaria.  
  - Manual de cuarentena y control en la movilización:  
    `https://www.gob.mx/cms/uploads/attachment/file/483430/Manual_de_procedimientos_de_cuarentena_y_control_en_la_movilizaci_n.pdf` [13]  

**Formato**: PDF.

**Estrategia de uso para modelar capacidad de respuesta**

1. Extraer de los PDFs:
   - Tiempos objetivo de respuesta (`t_deteccion`, `t_notificacion`, `t_cuarentena`).
   - Estructura de cadena de mando y recursos (número de brigadas, laboratorios).
2. Modelar capacidad en términos de:
   - **Capacidad de pruebas por día**, **capacidad de sacrificio diario**.
   - **Tiempo esperado de control** de un foco simulado.

**Pseudocódigo (extracción de KPI de texto)**

```python
from PyPDF2 import PdfReader
import re

def extract_kpis_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = "\n".join([p.extract_text() or "" for p in reader.pages]).lower()
    # Buscar patrones de tiempo ("días", "horas", etc.)
    kpis = {}
    for label, pattern in {
        "tiempo_activacion_coes": r"(\d+)\s*d[ií]as\s+para\s+activar\s+el\s+centro",
        "proposito_simulacro": r"objetivo[s]?:\s*(.+?)(?:\n\n|\.)",
    }.items():
        m = re.search(pattern, text)
        if m:
            kpis[label] = m.group(1)
    return kpis
```

---

### 2.2 Datos de Entrenamiento Internacional (UK 2001 y Sudamérica)

No se encontró un CSV simple con toda la serie de FMD 2001 de UK o de Sudamérica en organismos como DEFRA/WOAH, pero sí:

#### 2.2.1 openFMD / WRLFMD

- **Dashboard FMDwatch**:  
  <https://openfmd.org/dashboard/fmdwatch/> [14]  
  - Permite descargar un CSV con datos de **casos por país/fecha** (botón “Download CSV”).
  - Este CSV sirve para entrenar modelos de series de tiempo (Chronos) para FMD a nivel país o región.

**Pseudocódigo (descarga genérica)**

```python
import requests

def download_fmd_global_csv(year=None):
    base_url = "https://openfmd.org/dashboard/fmdwatch/"
    # La URL real de descarga suele ser un endpoint tipo /download?year=YYYY
    # Aquí se ilustra la estructura, aunque debes inspeccionar manualmente:
    params = {"year": year} if year else {}
    r = requests.get(base_url + "download", params=params, timeout=120)
    r.raise_for_status()
    with open(f"fmdwatch_{year or 'all'}.csv", "wb") as f:
        f.write(r.content)
```

#### 2.2.2 Datos de UK 2001 (mapas diarios)

- **Conjuntos Data.gov.uk / Defra** (mapas diarios y estatus por condado):
  - Ejemplo (county status map):  
    `https://www.data.gov.uk/dataset/04c9892c-1944-4bdb-8bab-a7200085c946/foot-and-mouth-disease-2001-county-status-map-15-10-2001` [15]  
    Los recursos concretos son JPEG como:  
    `http://data.defra.gov.uk/Agriculture/APHA0702-FMD_County_Status_20011015.jpg`
  - Mapas diarios:  
    `https://www.data.gov.uk/dataset/65d6d8f2-c7a0-45b0-8e26-07d0cfb0f11b/foot-and-mouth-disease-2001-daily-overview-maps-week-commencing-09-04-2001` [16]  

- **Formato**: JPEG (no CSV).  
  - Para reconstruir series a partir de estos mapas se requeriría OCR/visión computacional (reconocer legendas y números de casos).  
  - Dado el costo técnico, para modelos Chronos es más práctico apoyarse en:
    - openFMD (para series globales).
    - Artículos científicos con tablas de R0 estimados (p.ej. trabajos de PLOS One sobre el brote 2001).

#### 2.2.3 Sudamérica – situación FMD

- **World Reference Laboratory – Región Sudamérica**:  
  <https://www.wrlfmd.org/country-reports/south-america> [17]  
  - Proporciona informes por país con últimas epidemias, serotipos circulantes.
- **PANAFTOSA / PAHO**:  
  Diversos reportes y análisis (no en formato CSV directo, pero sí tablas en PDF) [18].

**Modelo relacional sugerido**

- `dim_pais(pais_id, nombre, region, es_mexico)`
- `fact_fmd_casos(pais_id, fecha_id, num_casos, serotipo, fuente, r0_estimado, perdida_pib_agro_pct)`

---

## Vector 3 – Resistencia Antimicrobiana (RAM) y Superbacterias

### 3.1 Redes de Vigilancia PUCRA / UNAM

**Reportes PUCRA**

- **Resistencia Antimicrobiana en México 2017–2024**:  
  `https://puiree.cic.unam.mx/divulgacion/docs/pucra2025.pdf` [19]  
- **Resistencia Antimicrobiana 2017–2023**:  
  `https://puiree.cic.unam.mx/divulgacion/docs/pucra2024.pdf` [20]  
- **Resistencia Antimicrobiana 2017–2022**:  
  `https://puiree.cic.unam.mx/divulgacion/docs/pucra23.pdf` [21]  

- **Formato**: PDF con tablas de aislamientos hospitalarios (p. ej. *E. coli*, *K. pneumoniae*), tasas de resistencia, CMI, etc.

En el PDF 2025 se observan, por ejemplo:

- Tablas como “Cuadro 2. Aislamientos de *Escherichia coli* y *Klebsiella pneumoniae* a partir de urocultivos. Instituciones de la Red PUCRA 2017–2024” [19].  
- Anexos con puntos de corte CLSI (p.ej. Tabla A‑1 para enterobacterias) [19].

No se observó mención explícita de `blaCTX-M` en el fragmento inspeccionado, pero es habitual que estos anuarios contengan secciones de genes de resistencia o al menos patrones de resistencia fenotípica compatibles con BLEE.

**Estrategia de extracción**

- extraer tablas con `camelot` o `tabula-py`.
- Crear una tabla de hechos de resistencia con dimensiones:

  - `dim_bacteria(bacteria_id, genero, especie)`
  - `dim_antimicrobiano(antibiotico_id, nombre, grupo)`
  - `fact_ram(hospital_id, fecha_id, bacteria_id, antibiotico_id, porcentaje_resistente, n_aislamientos, fuente_pdf)`

**Pseudocódigo (extracción simplificada de tablas)**

```python
import camelot
import pandas as pd

def extract_tables_pucra(pdf_path):
    tables = camelot.read_pdf(pdf_path, pages="all", flavor="stream")
    all_df = []
    for t in tables:
        df = t.df
        all_df.append(df)
    df_all = pd.concat(all_df, ignore_index=True)
    return df_all

# Luego filtras por tablas relevantes (que contengan "E. coli", "Klebsiella", etc.).
```

---

### 3.2 Vigilancia Minorista (COFEPRIS / PNT, LMR y patógenos en alimentos)

No existe un dataset público directo tipo “CSV de rastros clausurados por LMR”. Hay que combinar:

1. **Actas de verificación sanitaria (COFEPRIS)**  
   Página:  
   <https://www.gob.mx/cofepris/documentos/actas-de-verificacion-sanitaria> [22]  

   - Contiene múltiples formatos de actas (AC‑01, AC‑02, …, AC‑82), p.ej.:  
     - `AC-01__Acta_de_verificacion_sanitaria_general.pdf`  
       → `https://www.gob.mx/cms/uploads/attachment/file/1002939/AC-02__Acta_de_verificaci_n_sanitaria_general.pdf`  
     - Actas específicas para farmacias, dispositivos, hemoderivados, etc. [22].

   - Estas actas son **plantillas** de inspección. Para encontrar clausuras concretas (p.ej. rastros por clembuterol), hay que ir a comunicados de prensa o a solicitudes en la **Plataforma Nacional de Transparencia (PNT)**.

2. **Prensa / comunicados de clausuras**  
   Ejemplo:  
   - “Cofepris suspendió 10 rastros donde se detectó presencia de clembuterol…”:  
     <https://www.gob.mx/cofepris/prensa/cofepris-suspendio-10-rastros-donde-se-detecto-presencia-de-clembuterol-o-malas-practicas-higienicas-en-2014-57004> [23]

3. **Plataforma Nacional de Transparencia (PNT)**  
   - URL base: <https://www.plataformadetransparencia.org.mx/> [24]  
   - Lógica de trabajo:
     1. Acceder manualmente, identificar el Sujeto Obligado (COFEPRIS o equivalentes estatales).
     2. Usar el buscador interno con términos como “acta de clausura rastro”, “clembuterol”, “LMR”, “Salmonella”, etc.
     3. Los resultados suelen ser fichas con enlace a PDF o Excel.

**Estrategia de scraping con Selenium**

Dado que la PNT es altamente dinámica (JavaScript), la automatización requiere Selenium:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def scrape_pnt_actas_lmr():
    opts = Options()
    opts.headless = True
    driver = webdriver.Chrome(options=opts)
    driver.get("https://www.plataformadetransparencia.org.mx/")

    # 1. Localizar cuadro de búsqueda global
    search_box = driver.find_element(By.CSS_SELECTOR, "input[type='search']")
    search_box.send_keys("clembuterol rastro clausura")
    search_box.submit()
    time.sleep(5)

    # 2. Extraer resultados (títulos, enlaces)
    results = driver.find_elements(By.CSS_SELECTOR, "a.result-link")
    actas = []
    for r in results:
        title = r.text
        url = r.get_attribute("href")
        actas.append({"title": title, "url": url})
    driver.quit()
    return actas
```

Luego, para cada URL de resultado que apunte a un PDF, se descarga con `requests` y se hace extracción de texto/tablas (PyPDF2, camelot, OCR si es escaneado).

**Modelo relacional sugerido**

- `dim_establecimiento(id, tipo, giro, estado, municipio)`
- `fact_clausura(id_establecimiento, fecha_id, motivo, agente_detectado, lmr_excedido, autoridad, fuente_url)`

---

## Esquema global del Data Warehouse

A alto nivel, un esquema en estrella puede quedar así:

- **Dimensiones**:
  - `dim_tiempo`
  - `dim_estado` / `dim_pais`
  - `dim_especie_ganado`
  - `dim_establecimiento` (rastro, supermercado, hospital)
  - `dim_bacteria`, `dim_antimicrobiano`
- **Tablas de hechos**:
  - `fact_hatos_tb` — situación zoosanitaria bovina.
  - `fact_cuarentenas_tb` — medidas de control en hatos.
  - `fact_morbilidad_tb_humana` — casos y defunciones TB (CIE‑10).
  - `fact_indemnizacion_tb` — estimaciones de indemnización.
  - `fact_fmd_casos` — brotes y casos de FMD (openFMD, WRLFMD).
  - `fact_ram` — resistencia antimicrobiana hospitalaria (PUCRA).
  - `fact_clausura` — clausuras por LMR o patógenos en alimentos (COFEPRIS/PNT).

Con esta arquitectura puedes:

- Vincular **hatos infectados / en cuarentena** con:
  - **Casos humanos** (por entidad y año/trimestre).
  - **Costos económicos** (indemnización estimada por UA).
- Entrenar **modelos Chronos**:
  - Series de tiempo de **casos FMD** por país.
  - Series de **prevalencia TB bovina** y **TB humana asociada**.
- Integrar **RAM** como capa de impacto sanitario secundario, asociada a:
  - Hospitales ubicados en estados con alta carga zoonótica
  - Patrones de consumo de antibióticos veterinarios (si se agregan otras fuentes).

---

## Referencias

[1] CONSTATACIÓN DE HATOS LIBRES DE TUBERCULOSIS BOVINA. <https://www.datos.gob.mx/dataset/constatacion_hatos_libres_tuberculosis_bovina>  
[2] CUARENTENAS TUBERCULOSIS BOVINA 2024. <https://www.gob.mx/senasica/documentos/cuarentenas-tuberculosis-bovina-2024?state=published>  
[3] DATOS ABIERTOS DIRECCIÓN GENERAL DE EPIDEMIOLOGÍA. <https://www.gob.mx/salud/documentos/datos-abiertos-152127>  
[4] CUBOS DINÁMICOS – DGIS. <http://www.dgis.salud.gob.mx/contenidos/basesdedatos/BD_Cubos_gobmx.html>  
[5] CUBOS DINÁMICOS – SINBA. <https://sinba.salud.gob.mx/CubosDinamicos>  
[6] ACUERDO PARA LA OPERACIÓN DE LA CAMPAÑA NACIONAL CONTRA LA TUBERCULOSIS BOVINA. <https://www.gob.mx/senasica/documentos/acuerdo-para-la-operacion-de-la-campana-nacional-contra-la-tuberculosis-bovina-mycobacterium-bovis>  
[7] 2024_12_30_MAT_SADER_-_ACUERDO_TB.PDF. <https://www.gob.mx/cms/uploads/attachment/file/964169/2024_12_30_MAT_sader_-_Acuerdo_TB.pdf>  
[8] CONDICIONES GENERALES DEL SEGURO PECUARIO. <https://www.gob.mx/cms/uploads/attachment/file/71582/DC-S0074-0111-2016_Pecuario.pdf>  
[9] PRESENTACIÓN CONSTITUCIÓN DE FONDOS DE ASEGURAMIENTO. <https://www.gob.mx/cms/uploads/attachment/file/72238/PRESENTACION_CONSTITUCION_DE_FONDOS.pdf>  
[10] TABLA DE EQUIVALENCIAS DE GANADO MAYOR Y MENOR. <http://www.dof.gob.mx/nota_detalle.php?codigo=2054508&fecha=02/05/2000>  
[11] PAI FIEBRE AFTOSA 07-06-21. <https://dj.senasica.gob.mx/Contenido/files/2021/julio/PAIFiebreAftosa07-06-21_e83a982d-b6b5-40b0-a3ae-41321c88bbfa.pdf>  
[12] MANUALES CPA – SENASICA. <https://www.gob.mx/senasica/documentos/manuales-cpa?state=published>  
[13] MANUAL DE PROCEDIMIENTOS DE CUARENTENA Y CONTROL EN LA MOVILIZACIÓN. <https://www.gob.mx/cms/uploads/attachment/file/483430/Manual_de_procedimientos_de_cuarentena_y_control_en_la_movilizaci_n.pdf>  
[14] FMDWATCH – OPENFMD. <https://openfmd.org/dashboard/fmdwatch/>  
[15] FOOT AND MOUTH DISEASE 2001 – COUNTY STATUS MAP 15-10-2001. <https://www.data.gov.uk/dataset/04c9892c-1944-4bdb-8bab-a7200085c946/foot-and-mouth-disease-2001-county-status-map-15-10-2001>  
[16] FOOT AND MOUTH DISEASE 2001 – DAILY OVERVIEW MAPS (WEEK 09-04-2001). <https://www.data.gov.uk/dataset/65d6d8f2-c7a0-45b0-8e26-07d0cfb0f11b/foot-and-mouth-disease-2001-daily-overview-maps-week-commencing-09-04-2001>  
[17] SOUTH AMERICA – WORLD REFERENCE LABORATORY FOR FMD. <https://www.wrlfmd.org/country-reports/south-america>  
[18] FOOT-AND-MOUTH DISEASE DOCUMENTS – PAHO/PANAFTOSA. <https://www.paho.org/en/documents/topics/foot-and-mouth-disease>  
[19] RESISTENCIA ANTIMICROBIANA EN MÉXICO 2017–2024 (PUCRA 2025). <https://puiree.cic.unam.mx/divulgacion/docs/pucra2025.pdf>  
[20] RESISTENCIA ANTIMICROBIANA EN MÉXICO 2017–2023 (PUCRA 2024). <https://puiree.cic.unam.mx/divulgacion/docs/pucra2024.pdf>  
[21] RESISTENCIA ANTIMICROBIANA 2017–2022 (PUCRA 23). <https://puiree.cic.unam.mx/divulgacion/docs/pucra23.pdf>  
[22] ACTAS DE VERIFICACIÓN SANITARIA – COFEPRIS. <https://www.gob.mx/cofepris/documentos/actas-de-verificacion-sanitaria>  
[23] COFEPRIS SUSPENDIÓ 10 RASTROS POR CLEMBUTEROL. <https://www.gob.mx/cofepris/prensa/cofepris-suspendio-10-rastros-donde-se-detecto-presencia-de-clembuterol-o-malas-practicas-higienicas-en-2014-57004>  
[24] PLATAFORMA NACIONAL DE TRANSPARENCIA. <https://www.plataformadetransparencia.org.mx/>
