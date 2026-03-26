# Ganado Saludable — ELT Pipeline Architecture & Implementation Plan (V4 Definitiva)

## Context & Problem

**Enfermedad asignada: Fiebre Aftosa (FMD).** México es libre de FMD desde 1954, por lo que no hay datos nacionales de brotes. Usamos **Tuberculosis Bovina como proxy de calibración epidemiológica** (datos reales SENASICA) y transferimos los parámetros al escenario catastrófico de FMD (R0 ≈ 6.0 vs R0_TB ≈ 1.8).

Los datos gubernamentales están atrapados en infraestructuras hostiles (SINAIS con ActiveX/OWC11, SENASICA con APIs ocultas, PNT con JavaScript dinámico).

### Documentos Analizados — Cross-Reference

| Documento | Rol en el Pipeline | Hallazgo Clave |
|---|---|---|
| **V2.md** | PRD — Variables y targets | N=35.1M cabezas, Ampicilina 94.7% resistencia, blaCTX-M 23.5%, target CIE-10 A05, 300M MXN/año campaña TB |
| **M_doc.md** | Manual de extracción (Navaja de Ockham) | Enfoque pragmático: CSV directos donde existen, Selenium solo para PNT, Anuarios como backend principal vs Cubos. **24 referencias verificadas.** |
| **Protocolo Zoonótica PDF** | Versión "hacker" avanzada | API oculta SENASICA `/api/Statistics/.../ObtenerDatos`, bypass `_VIEWSTATE` SINAIS, intercepción de red |
| **Problema Prototípico PDF** | Requisitos universitarios (7 materias) | Criptografía (César/RSA), Estadística Multivariada (Chernoff, Andrews), IA (XGBoost), NoSQL (MongoDB), EDOs (SIR), Finanzas Corporativas (VPN/ROI), Innovación Social |

### Estrategia de Extracción: Dual-Path (Pragmático + Hacker)

> [!IMPORTANT]
> **Arquitectura de Resiliencia Dual:**
> - **Primary Path (M_doc):** CSV directos de datos abiertos + Anuarios ZIP (rápidos, estables, verificados).
> - **Secondary Path (Protocolo/Doc A):** API oculta SENASICA + bypass SINAIS ViewState (para cuando el primary falla o se necesitan datos más granulares).
> - **Cada extractor implementa ambas rutas con fallback automático.**

---

## Estructura de Directorios Propuesta

```text
EpidemicResearch/
├── docs/
│   ├── implementation_plan.md      # Este documento
│   ├── task.md                     # Checklist de progreso
│   └── presentation_script.md      # Guion narrativo para coloquio
├── src/
│   ├── __init__.py
│   ├── config.py                   # URLs, timeouts, retry, constantes V2 + FMD
│   ├── base_extractor.py           # ABC con metadata lineage
│   ├── crypto/
│   │   ├── __init__.py
│   │   └── encryption.py           # César + RSA para IDs IoT/hatos
│   ├── extractors/
│   │   ├── __init__.py
│   │   ├── senasica_tb.py          # API oculta + CSV fallback (proxy calibración)
│   │   ├── sinais_cubos.py         # ViewState bypass + Anuarios fallback
│   │   ├── dge_morbilidad.py       # Anuarios ZIP→CSV (CIE-10)
│   │   ├── pnt_cofepris.py         # Selenium PNT clausuras + clembuterol proxy
│   │   ├── openfmd.py              # FMD global CSV (Chronos + SIR FMD)
│   │   └── pucra_ram.py            # RAM PDF tables (camelot)
│   ├── warehouse/
│   │   ├── __init__.py
│   │   ├── dimensions.py           # Pydantic: dim_tiempo, dim_geografia, etc.
│   │   ├── facts.py                # Pydantic: fact_hatos_tb, fact_morbilidad, etc.
│   │   ├── schema.py               # Star schema assembler
│   │   └── nosql_client.py         # MongoDB adapter (requisito NoSQL)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── sir_prep.py             # SIR DUAL: calibración TB → simulación FMD
│   │   ├── xgboost_prep.py         # Feature eng → target A05 (+ proxy clembuterol)
│   │   ├── chronos_prep.py         # Time series formatter (AWS Chronos)
│   │   ├── stats_multivariate.py   # PCA, ANOVA, Regresión Múltiple
│   │   └── financial_roi.py        # VPN, ROI, Apalancamiento
│   └── visualization/
│       ├── __init__.py
│       ├── chernoff_faces.py       # 32 Caras de Chernoff (estados de México)
│       ├── andrews_curves.py       # Curvas de Andrews (clusters epidemiológicos)
│       ├── choropleth_maps.py      # Mapas coropléticos estatales de riesgo
│       ├── sir_plots.py            # Curvas SIR + diagramas de fase TB vs FMD
│       └── dashboard.py            # Streamlit/Plotly Dash (visualización interactiva)
├── tests/
│   ├── __init__.py
│   ├── test_extractors.py          # Mock HTTP responses
│   ├── test_warehouse.py           # Schema validation
│   ├── test_models.py              # Model prep + stats tests
│   └── test_crypto.py              # César/RSA bidireccional
├── notebooks/
│   ├── 01_eda_senasica.ipynb       # Exploración datos SENASICA
│   ├── 02_eda_morbilidad.ipynb     # Exploración datos DGE/SINAIS
│   ├── 03_multivariate_analysis.ipynb  # PCA, Chernoff, Andrews, ANOVA
│   ├── 04_sir_simulation.ipynb     # Simulación SIR dual interactiva
│   ├── 05_xgboost_training.ipynb   # Entrenamiento + SHAP values
│   └── 06_financial_analysis.ipynb # VPN, ROI, escenarios
├── data/                           # Downloaded raw data (gitignored)
│   ├── raw/
│   └── processed/
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Component 1: Core Infrastructure & Crypto

### [NEW] `src/config.py`

**URLs consolidadas** de todos los endpoints verificados en M_doc.md (refs [1]-[24]):

| Fuente | URL / Endpoint | Formato | Ref |
|---|---|---|---|
| SENASICA Hatos Libres (Dic 2025) | `https://repodatos.atdt.gob.mx/.../hatos_libres_tuberculosis.csv` | CSV | [1] |
| SENASICA Hatos Libres (Jun 2025) | `https://repodatos.atdt.gob.mx/.../47_tuberculosis-bovina.csv` | CSV | [1] |
| SENASICA API Oculta | `https://dj.senasica.gob.mx/sias/api/Statistics/SaludAnimal/TuberculosisBovina/ObtenerDatos` | JSON | Doc A |
| Cuarentenas TB 2024 (4 PDFs) | `https://www.gob.mx/cms/uploads/attachment/file/97xxxx/...` | PDF | [2] |
| DGE Anuarios (2015-2022) | `https://epidemiologia.salud.gob.mx/anuario/datos_abiertos/Anuario_{year}.zip` | ZIP→CSV | [3] |
| SINAIS Cubos Dinámicos | `http://www.dgis.salud.gob.mx/contenidos/basesdedatos/BD_Cubos_gobmx.html` | OWC11/OLAP | [4] |
| Acuerdo TB DOF | `https://www.gob.mx/cms/uploads/attachment/file/964169/...Acuerdo_TB.pdf` | PDF | [7] |
| Seguro Pecuario | `https://www.gob.mx/cms/uploads/attachment/file/71582/...Pecuario.pdf` | PDF | [8] |
| openFMD Dashboard | `https://openfmd.org/dashboard/fmdwatch/` | CSV (download) | [14] |
| WRLFMD Sudamérica | `https://www.wrlfmd.org/country-reports/south-america` | Reportes por país | [17] |
| PANAFTOSA/OPS | `https://www.paho.org/en/documents/topics/foot-and-mouth-disease` | PDF/reportes | [18] |
| Plan de Acción FMD | `https://dj.senasica.gob.mx/.../PAIFiebreAftosa07-06-21.pdf` | PDF | [11] |
| Manuales CPA | `https://www.gob.mx/senasica/documentos/manuales-cpa` | PDFs | [12] |
| PUCRA 2025 | `https://puiree.cic.unam.mx/divulgacion/docs/pucra2025.pdf` | PDF | [19] |
| PUCRA 2024 | `https://puiree.cic.unam.mx/divulgacion/docs/pucra2024.pdf` | PDF | [20] |
| PNT Base | `https://www.plataformadetransparencia.org.mx/` | JS dinámico | [24] |

**Constantes biológicas del V2.md:**
- `N_BIOMASA = 35_100_000` (32.6M carne + 2.5M leche)
- `CONFINAMIENTO_ANUAL = 2_800_000` cabezas
- `RESISTENCIA_AMPICILINA = 0.947`
- `RESISTENCIA_CARBENICILINA = 0.842`
- `RESISTENCIA_TETRACICLINA = 0.684`
- `PREVALENCIA_BLACTX_M = 0.235`
- `PREVALENCIA_BLATEM = 0.150`
- `PRESUPUESTO_TB_MXN = 300_000_000` (campaña nacional anual)
- `ECOLI_O157_PIEL = 0.909` (90.9% en hisopados pre-evisceración)

**Constantes FMD (literatura + M_doc):**
- `R0_FMD_LOW = 4.0` (estimación conservadora)
- `R0_FMD_HIGH = 8.0` (escenario UK 2001, Tildesley et al.)
- `PERIODO_INFECCIOSO_FMD_DIAS = 14`
- `COSTO_UK_2001_MXN = 200_000_000_000` (~£8B)
- `ANIMALES_SACRIFICADOS_UK_2001 = 6_000_000`

**Prevalencia minorista (V2.md §3):**
- Supermercados: 1.3% Salmonella
- Carnicerías: 8.4%
- Tianguis: 13.6%
- Mercados Municipales: 22.3%

### [NEW] `src/base_extractor.py`
- `BaseExtractor` ABC con:
  - `extract()` → raw data
  - `transform()` → cleaned DataFrame
  - `inject_lineage(df)` → añade `fecha_extraccion_etl`, `fuente_origen`, `version_etl`
  - Retry decorator con `tenacity` (backoff exponencial para servidores gubernamentales)
  - Logging estructurado (JSON)

### [NEW] `src/crypto/encryption.py`
- **César:** Ofuscación rápida de identificadores de lotes (`"LOTE"` → `"ORWH"` con desplazamiento n=3, según Problema Prototípico §Criptografía).
- **RSA (asimétrico):** Cifrado de payloads IoT para garantizar integridad de datos de sensores ante inyección de datos falsos.
- Funciones: `caesar_encrypt()`, `caesar_decrypt()`, `rsa_keygen()`, `rsa_encrypt()`, `rsa_decrypt()`.

---

## Component 2: Extractors (Módulo 1) — Dual Path

### [NEW] `src/extractors/senasica_tb.py`
- **Primary (M_doc §1.1.1):** Download CSVs de hatos libres TB bovina desde `repodatos.atdt.gob.mx`.
- **Secondary (Doc A):** Intercepción de API REST oculta: `POST/GET` a `/api/Statistics/SaludAnimal/TuberculosisBovina/ObtenerDatos`.
- **Cuarentenas (M_doc §1.1.2):** PDF extraction con `camelot` (flavor `stream`) para tablas de cuarentenas trimestrales.
- Normalización de estados y tipos de producción.

**Modelo relacional sugerido (M_doc):**
- `fact_hatos_tb(estado_id, fecha_id, tipo_produccion, num_hatos_libres, fuente)`
- `fact_cuarentenas_tb(estado_id, fecha_id, num_hatos_cuarentena, num_animales, tipo_medida, fuente_pdf)`

### [NEW] `src/extractors/sinais_cubos.py`
- **Primary (Doc A — Bypass OWC11):** `requests.Session()` que:
  1. Hace GET inicial para obtener `_VIEWSTATE` y `_EVENTVALIDATION`.
  2. Inyecta payload POST con parámetros de reporte (CIE-10 A15-A19, A05).
  3. Fuerza descarga del archivo Excel/CSV del backend.
- **Fallback:** Si el bypass falla, redirige a DGE Anuarios.

### [NEW] `src/extractors/dge_morbilidad.py`
- **Fuente:** Anuarios ZIP de `epidemiologia.salud.gob.mx` (M_doc §1.2.1).
- Download ZIP → extract CSV → filter by CIE-10 codes.
- **Códigos target:**
  - TB respiratoria: `A15–A16`
  - Otras TB (extrapulmonar, zoonótica): `A17–A19`
  - Intoxicaciones alimentarias (target XGBoost): `A05`
- **Encoding:** `latin1` para CSVs del gobierno.
- **Nota (M_doc §1.2.1):** TB por M. bovis no tiene código CIE-10 separado; se clasifica bajo TB general. Para especificidad zoonótica: filtrar por ocupación + región ganadera.

### [NEW] `src/extractors/pnt_cofepris.py`
- **Fuente:** PNT `plataformadetransparencia.org.mx` (M_doc §3.2).
- Selenium headless para JS dinámico.
- **Queries de búsqueda:** "clembuterol rastro clausura", "LMR Salmonella", "acta clausura establecimiento".
- Manejo de modales emergentes y tiempos de espera.
- Descarga de PDFs resultado → extracción texto con `PyPDF2` / `camelot`.
- **"Proxy de Opacidad":** Las clausuras por clembuterol se usan como indicador proxy de abuso de antibióticos (contribución metodológica original). Los establecimientos que violan normas de clembuterol tienen alta probabilidad de violar LMR antibióticos. Esta variable alimenta el XGBoost como feature de bioseguridad.

### [NEW] `src/extractors/openfmd.py`
- **Fuente principal:** openFMD dashboard CSV (M_doc §2.2.1).
- **Fuentes complementarias:** WRLFMD Sudamérica [17], PANAFTOSA/OPS [18].
- Download CSV global de casos FMD por país/fecha.
- Para entrenamiento de modelos Chronos + **calibración de R0 para escenario FMD mexicano.**
- Variables: `pais_id, fecha, num_casos, serotipo, r0_estimado`.
- **Manuales CPA (PDFs):** Extracción de KPIs de capacidad de respuesta: t_detección, t_cuarentena, brigadas, capacidad de sacrificio/día.

### [NEW] `src/extractors/pucra_ram.py`
- **Fuente:** PDFs PUCRA/UNAM 2022-2025 (M_doc §3.1, refs [19]-[21]).
- `camelot` para extraer tablas de resistencia antimicrobiana.
- **Parse:** bacteria (E. coli, K. pneumoniae), antimicrobiano, % resistencia, n_aislamientos.
- Mapeo a genes de resistencia del V2.md: blaCTX-M, blaTEM, tet(A), tet(B), gyrA, gyrB.

---

## Component 3: Data Warehouse & NoSQL (Módulo 2)

### [NEW] `src/warehouse/dimensions.py`

Pydantic models para **dimensiones del Star Schema**:
- `DimTiempo(fecha, año, trimestre, mes)`
- `DimGeografia(estado_id, nombre_estado, region, es_frontera, num_hatos_censados)`
- `DimPatogeno(patogeno_id, nombre, tipo, gen_resistencia)` — genes V2.md: blaCTX-M, blaTEM, tet(A/B)
- `DimAntimicrobiano(antibiotico_id, nombre, grupo_farmacologico)` — Tetraciclinas, Penicilinas, Fluoroquinolonas
- `DimEstablecimiento(id, tipo, giro, estado, municipio)` — rastro, supermercado, hospital
- `DimEspecie(tipo_ganado, ua_factor)` — factor Unidad Animal del DOF (M_doc §1.3: vaca 400-450kg = 1.0 UA, toro = 1.25 UA)

### [NEW] `src/warehouse/facts.py`

Pydantic models para **tablas de hechos**:
- `FactHatosTB` — hatos libres/cuarentena por estado (SENASICA)
- `FactCuarentenasTB` — cuarentenas, despoblación, sacrificios (SENASICA PDFs)
- `FactMorbilidadHumana` — casos CIE-10 TB (A15-A19) + intoxicaciones (A05) (DGE/SINAIS)
- `FactIndemnizacionTB` — costo estimado por despoblación (M_doc §1.3: `monto = num_animales * ua_factor * precio_ua * 0.85`)
- `FactFMDCasos` — brotes internacionales para Chronos (openFMD)
- `FactRAM` — resistencia antimicrobiana hospitalaria (PUCRA)
- `FactClausura` — clausuras por LMR/patógenos (PNT/COFEPRIS)

### [NEW] `src/warehouse/nosql_client.py`
- **MongoDB Adapter** (cumple requisito académico NoSQL del Problema Prototípico).
- Serializa modelos Pydantic → documentos BSON.
- Colecciones: una por fact table + dimensiones compartidas.
- Facilita almacenamiento de datos **no estructurados** (actas PNT, texto libre de clausuras).

---

## Component 4: Model Preparation & Financials (Módulo 3)

### [NEW] `src/models/sir_prep.py` — **DUAL MODE (TB Calibración → FMD Simulación)**

Extrae del warehouse: S_0, I_0. Opera en dos modos:

**Modo 1 — Calibración (TB Bovina):**
- R0_tb ≈ 1.5–2.0 (calibrado con cuarentenas SENASICA 2024)
- γ_tb ≈ 1/180 días (período infeccioso ~6 meses)
- β_tb = R0_tb × γ_tb

**Modo 2 — Simulación (Fiebre Aftosa):**
- R0_fmd ≈ 4.0–8.0 (literatura: UK 2001, Tildesley et al.)
- γ_fmd ≈ 1/14 días (período infeccioso ~2 semanas)
- β_fmd = R0_fmd × γ_fmd
- Factor de transferencia: β_fmd / β_tb ≈ 3.3x–5x

**6 escenarios:** TB sin intervención, TB vacunación, TB cuarentena, FMD sin intervención (R0=6), FMD con cuarentena+sacrificio (R0→2), FMD escenario UK 2001 (R0=8).

Genera DataFrame compatible con `scipy.integrate.odeint`.

### [NEW] `src/models/xgboost_prep.py`
- **Features (X):**
  - Volumen de alimento animal (SIAP/SADER)
  - Prevalencia de Salmonella por canal de comercialización (V2.md §3: 1.3%-22.3%)
  - Clausuras PNT por estado
  - Densidad ganadera por estado
  - Resistencia antimicrobiana (% ampicilina, carbenicilina)
  - Variables climáticas (sequía, temperatura)
  - **Clausuras por clembuterol por estado (Proxy de Opacidad)** — indicador de bioseguridad deficiente
- **Target (y):** Casos intoxicación humana CIE-10 A05 (del V2.md §6).
- Join multi-tabla vía llaves geográficas: `estado_id` + `fecha_id`.
- Feature scaling, null imputation, one-hot encoding donde aplique.

### [NEW] `src/models/stats_multivariate.py`
- **PCA (Análisis de Componentes Principales):** Reducción dimensional de variables ganaderas. Output: scree plot + biplot.
- **ANOVA / MANOVA:** Test de diferencia significativa en prevalencia de Salmonella entre 4 canales de comercialización (supermercados 1.3% vs tianguis 13.6% vs mercados 22.3%).
- **Regresión Lineal Múltiple:** Variable dependiente = casos A05, independientes = densidad ganadera, prevalencia Salmonella, clausuras. Output: tabla de coeficientes + R².
- Estas funciones alimentan tanto los notebooks de EDA como las visualizaciones de Chernoff/Andrews.

### [NEW] `src/models/chronos_prep.py`
- Formatea series temporales para **AWS Chronos** (predicción de trayectorias de brotes).
- Series candidatas:
  - **Casos FMD por país (openFMD) — serie principal para la enfermedad asignada**
  - Prevalencia TB bovina por estado (SENASICA) — serie de calibración
  - TB humana asociada por estado (DGE/SINAIS)
- Output: DataFrames con columnas `ds` (timestamp) y `y` (valor).

### [NEW] `src/models/financial_roi.py`
- Motor de cálculo de **Finanzas Corporativas** (requisito Problema Prototípico §Finanzas):
  - **VPN (Valor Presente Neto):** Flujos de ahorro por detección temprana vs. costo del sistema IoT.
  - **ROI:** Retorno sobre inversión en prevención primaria.
  - **Apalancamiento:** Ratio deuda/capital para financiamiento del sistema.
  - **Análisis dual:**
    - **TB crónico:** Indemnización ~$39M MXN/brote (M_doc §1.3)
    - **FMD catastrófico:** Referencia UK 2001 ~$200B MXN. Detección 48h temprana = diferencia entre contener en 1 estado ($2B) o perder control nacional ($200B).

---

## Component 5: Visualization & Statistical Analysis (Módulo 4)

### [NEW] `src/visualization/chernoff_faces.py`
- Genera **32 Caras de Chernoff** (una por estado de México).
- Rasgos faciales codifican: prevalencia TB, resistencia RAM, clausuras COFEPRIS, densidad ganadera, clausuras clembuterol.
- Librería: `matplotlib` + custom face renderer.

### [NEW] `src/visualization/andrews_curves.py`
- **Curvas de Andrews** (series de Fourier) para visualizar clusters de estados con perfiles epidemiológicos similares.
- Input: matriz multivariada del PCA.
- Output: gráfico multidimensional con colores por cluster.

### [NEW] `src/visualization/choropleth_maps.py`
- **Mapas coropléticos** de México por estado.
- Variables a mapear: prevalencia TB, densidad ganadera, clausuras por clembuterol, riesgo A05 predicho por XGBoost.
- Librerías: `plotly.express` o `geopandas` + `matplotlib`.

### [NEW] `src/visualization/sir_plots.py`
- Genera las curvas S(t), I(t), R(t) para los 6 escenarios SIR.
- **Gráfica comparativa lado a lado:** TB (R0=1.8, lenta) vs FMD (R0=6.0, explosiva).
- Diagramas de fase (S vs I) para ambas enfermedades.
- Output: figuras para el artículo + presentación.

### [NEW] `src/visualization/dashboard.py`
- **Dashboard interactivo** con Streamlit o Plotly Dash.
- Panels: mapa coroplético + selector de estado + curvas SIR + tabla de métricas financieras.
- Para demo en vivo durante la presentación del coloquio.

---

## User Review Required

> [!WARNING]
> **Decisiones que requieren tu input antes de codear:**

1. **NoSQL:** ¿MongoDB con Docker local, o prefieres solo el adapter Pydantic sin levantar infraestructura?
2. **PNT/Selenium:** ¿Automatizado completo o semi-manual (tú identificas PDFs, el script los descarga)?
3. **Prioridad de Extractores:** Mi recomendación de orden:
   - **Wave 1:** SENASICA CSV + DGE Anuarios (validación rápida, endpoints estables)
   - **Wave 2:** openFMD + PUCRA (datos internacionales + PDF parsing)
   - **Wave 3:** SINAIS bypass + PNT Selenium (extracción hostil, más frágil)
4. **Criptografía:** ¿Módulo funcional `src/crypto/` con César+RSA, o solo documentación teórica?
5. **Dashboard:** ¿Streamlit (más rápido) o Plotly Dash (más control)?

---

## Verification Plan

### Automated Tests
```bash
# Desde la raíz del proyecto
python -m pytest tests/ -v --tb=short

# Test individual de extractores (usa mocks, no requiere internet)
python -m pytest tests/test_extractors.py -v

# Test de esquema warehouse
python -m pytest tests/test_warehouse.py -v

# Test de cifrado bidireccional
python -m pytest tests/test_crypto.py -v
```

### Smoke Test (requiere internet)
```bash
# Descarga real de un CSV de SENASICA para validar endpoint vivo
python -c "from src.extractors.senasica_tb import SenasicaTBExtractor; e = SenasicaTBExtractor(); print(e.extract().head())"
```

### Local E2E (con Docker)
```bash
# Levantar MongoDB
docker run -d --name ganado-mongo -p 27017:27017 mongo:latest

# Pipeline completo: SENASICA → MongoDB → SIR prep
python -c "
from src.extractors.senasica_tb import SenasicaTBExtractor
from src.warehouse.nosql_client import MongoClient
from src.models.sir_prep import SIRPrep

data = SenasicaTBExtractor().extract()
MongoClient().insert('fact_hatos_tb', data)
sir_df = SIRPrep().prepare()
print(sir_df.head())
"
```

### Manual Verification
- Verificar que `fecha_extraccion_etl` se inyecta en cada DataFrame extraído
- Revisar que los códigos CIE-10 filtrados sean correctos (A15-A19, A05)
- Validar que los modelos Pydantic aceptan datos reales sin errores de validación
- Confirmar que el cifrado César es reversible (`decrypt(encrypt("LOTE", 3), 3) == "LOTE"`)
- Validar que las colecciones MongoDB contienen documentos con keys de linaje
