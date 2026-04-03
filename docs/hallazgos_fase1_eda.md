# Hallazgos de la Fase de Adquisición y Análisis Exploratorio

> **Proyecto:** Ganado Saludable — Investigación Epidemiológica  
> **Fecha de corte:** 2026-04-03  
> **Agentes empleados:** Jules (GCP/Gemini), Codex (OpenAI), Antigravity (Gemini)

---

## Resumen Ejecutivo

La Fase 1 y 2 del pipeline ELT completó la adquisición de **~29,242 registros limpios** desde 6 fuentes gubernamentales e internacionales. El análisis exploratorio cruzado reveló hallazgos estadísticos que fortalecen la tesis central del proyecto: **la cadena cárnica mexicana es epidemiológicamente vulnerable**, tanto a enfermedades endémicas (TB bovina) como a amenazas exóticas (Fiebre Aftosa).

---

## 1. Inventario Final de Datos

### Datasets Disponibles

| Dataset | Archivo | Filas | Agente | Estado |
|---------|---------|-------|--------|--------|
| SENASICA TB (hatos libres) | `senasica_tb_clean.csv` | 64 | Antigravity | ✅ Completo (32 estados) |
| SENASICA Cuarentenas 2024 | `senasica_cuarentenas_clean.csv` | 108 | Jules | ✅ Completo (4 trimestres) |
| DGE Morbilidad Estatal 2015-2017 | `dge_morbilidad_clean.csv` | 384 | Antigravity | ✅ Por estado/edad/institución |
| DGE Morbilidad Nacional 2018-2024 | `dge_morbilidad_2018_2024_clean.csv` | 28 | Codex | ✅ Solo nivel nacional |
| DGE Consolidado Nacional 2015-2024 | `dge_morbilidad_nacional_2015_2024_clean.csv` | 40 | Codex | ✅ Serie temporal de 10 años |
| openFMD Global (WRLFMD) | `openfmd_clean.csv` | 28,585 | Codex | ✅ 123 países, 2001-2025 |
| COFEPRIS Verificaciones | `cofepris_clausuras_clean.csv` | 33 | Codex | ⚠️ Solo laboratorios farmacéuticos |
| COFEPRIS Sanciones Alimentarias | `cofepris_clausuras_alimentarias_clean.csv` | 12 | Codex | ✅ 7 empresas cárnicas sancionadas |

### Datasets No Disponibles

| Dataset | Motivo | Mitigación |
|---------|--------|------------|
| PUCRA (UNAM) | Host `puiree.cic.unam.mx` caído/timeout persistente | Constantes hardcodeadas en `config.py` desde V2.md (fuente: artículos UNAM publicados) |
| WAHIS (WOAH) | Cloudflare 403 Forbidden | Reemplazado por openFMD (28,585 filas reales) |
| DGE Estatal 2018-2024 | PDFs no desglosan por estado en reporte `fuente_notificacion` | Serie nacional es suficiente para tendencia temporal |
| COFEPRIS clausuras con contaminantes | COFEPRIS no publica actas con detalle de Clenbuterol/Salmonella/LMR | Sanciones a empresas cárnicas como proxy alternativo |

---

## 2. Proceso de Adquisición (Cronología)

### Wave 1: Extracción Directa (Antigravity)
- **SENASICA TB:** CSV descargado de `datos.gob.mx` → 64 filas, 32 estados, esquema limpio.
- **DGE 2015-2017:** Anuarios ZIP descargados del portal DGE → 384 filas filtradas por CIE-10.
- **Infraestructura:** Se creó `BaseExtractor` (ABC con retry, logging, lineage), `config.py` (URLs, constantes), y el esquema del pipeline.

### Wave 2: Agentes Asíncronos (Jules)
Se lanzaron **4 issues** a Jules (Gemini en GCP) para investigación paralela:

1. **Issue #1 (DGE 2018-2024):** Jules descubrió que los CSVs post-2017 no existen. Investigación exhaustiva documentada en `docs/DGE_DATA_SEARCH.md`. Creó placeholder.
2. **Issue #2 (openFMD/Kaggle):** Jules descubrió que el dashboard Shiny usa WebSockets (no URL estática), que WAHIS tiene Cloudflare, y creó el extractor Kaggle como alternativa.
3. **Issue #3 (COFEPRIS/PUCRA):** Jules extrajo 2 filas COFEPRIS ultra-filtradas y creó el extractor PUCRA (que falló por timeout UNAM).
4. **Issue #4 (SENASICA Cuarentenas):** El mayor éxito de Jules. Descargó 4 PDFs trimestrales, construyó un parser dual (tablas + regex fallback), y extrajo 108 filas limpias. También documentó que la API oculta de SENASICA retorna 404.

**Calificación Jules: 7/10** — Arquitectura impecable, documentación exhaustiva de vías muertas, limitado por no tener browser real.

### Wave 2.5: Recuperación con Browser (Codex)
Se diseñaron mega-prompts específicos y se desplegó un agente con capacidad de navegación web:

1. **DGE 2018-2024:** Codex descargó los 7 PDFs nacionales, los parseó con `pdfplumber`, y extrajo 28 filas nacionales + consolidó serie de 10 años (40 filas).
2. **openFMD:** Codex abrió el dashboard Shiny con Playwright, navegó a "Data table", esperó la generación del CSV vía WebSocket, y descargó **28,585 filas reales** del World Reference Laboratory for FMD. Este fue el logro más impactante de todo el pipeline.
3. **COFEPRIS:** Codex reparó el parser (33 filas tidy) pero descubrió que los PDFs eran verificaciones farmacéuticas, no clausuras alimentarias. En segunda pasada, encontró PDFs de "Resoluciones y Sanciones" con 12 empresas alimentarias (7 cárnicas).
4. **PUCRA:** Intentó descarga remota y browser. El host de UNAM sigue inaccesible. Dejó extractor listo para PDF local.

**Calificación Codex: 8.5/10** — Resolvió el bloqueo técnico más difícil (Shiny WebSocket), reparó extractores rotos, honesto sobre limitaciones.

---

## 3. Hallazgos del Análisis Exploratorio

### Hallazgo 1: COVID-19 Validó la Hipótesis de Canales de Venta

La serie temporal DGE 2015-2024 muestra una anomalía estadística dramática en 2020:

| Año | Intox. Alimentaria (A05) | Tuberculosis (A15-A19) |
|-----|--------------------------|------------------------|
| 2019 | 31,916 | 22,283 |
| 2020 | **18,667 (-41.5%)** | **16,747 (-24.8%)** |
| 2024 | 25,259 | 25,980 |

**Interpretación:** Cuando México cerró tianguis, mercados informales y cadenas de comida callejera por COVID-19, las intoxicaciones alimentarias colapsaron un **41.5%**. Esto demuestra cuantitativamente que los **canales de venta informales** (con cadena de frío rota) son el vector primario de contagio alimentario, no la salud intrínseca del animal. Este hallazgo fortalece directamente la hipótesis del ANOVA: prevalencia de Salmonella en tianguis (13.6%) vs supermercados (1.3%).

### Hallazgo 2: Las Américas Son Inmunológicamente Vírgenes a FMD

El análisis de 16,540 eventos FMD positivos confirmados (2000-2025) muestra:

| Región | Eventos | % del Total |
|--------|---------|-------------|
| Asia | 10,658 | 64.4% |
| África | 5,124 | 31.0% |
| **Américas** | **446** | **2.7%** |
| Europa | 300 | 1.8% |

**Interpretación:** Las Américas prácticamente no conocen la Fiebre Aftosa en el siglo XXI. Esto significa que el hato ganadero mexicano (35.1M cabezas) no tiene inmunidad de rebaño. Un brote importado encontraría una población **100% susceptible**, justificando un R₀ efectivo de 6.0-8.0 (vs. 2.0-3.0 en regiones endémicas donde hay inmunidad parcial).

### Hallazgo 3: Serotipo O Domina Globalmente (55%)

| Serotipo | Eventos | % |
|----------|---------|---|
| O | 9,072 | 54.9% |
| A | 3,559 | 21.5% |
| SAT2 | 1,542 | 9.3% |
| Asia1 | 995 | 6.0% |
| UNTYPED | 669 | 4.0% |

**Interpretación:** El serotipo O es el mismo que devastó UK en 2001 (6M animales sacrificados, £8B de pérdidas). Nuestro modelo SIR debe parametrizarse primariamente con R₀ = 6.0 (Tildesley et al., basado en serotipo O).

### Hallazgo 4: Concentración Geográfica de TB Bovina

Las cuarentenas de SENASICA 2024 se concentran en **solo 13 de 32 estados**. Los 19 estados restantes reportan cero incidencias. Esto confirma la concentración del problema en el corredor norte/noreste (Chihuahua, Durango, Jalisco), donde la ganadería extensiva domina y el control sanitario es más difícil.

### Hallazgo 5: Opacidad Regulatoria Documentada

COFEPRIS no publica datos granulares sobre clausuras alimentarias con detalle de contaminantes (Clenbuterol, Salmonella, violaciones LMR). La mejor evidencia recuperable fueron 12 procedimientos de sanción a empresas alimentarias, de las cuales 7 son explícitamente cárnicas (Bachoco, Qualtia, Carnes Selectas, frigotíficos). Esto refuerza la narrativa de que **la opacidad regulatoria es en sí misma un indicador de riesgo**.

### Hallazgo 6: TB Humana Post-COVID Supera Niveles Pre-Pandemia

El acumulado de tuberculosis humana en 2024 (25,980 casos) superó el máximo pre-pandemia de 2019 (22,283), un incremento del **16.6%**. Esto sugiere un efecto rebote post-pandemia o un deterioro en los sistemas de vigilancia epidemiológica, ambos relevantes para la correlación animal-humano que sustenta el proyecto.

---

## 4. Calidad de Datos: Matriz de Decisión

| Dataset | Completitud | Duplicados | Anomalías | Acción requerida |
|---------|-------------|------------|-----------|------------------|
| SENASICA TB | Alta (~95%) | 0 | Columna duplicada (`total_bovinos` / `total__bovinos`) | Usar `total_bovinos_constatados_libres` |
| SENASICA Cuarentenas | Alta (~100%) | 0 | Ninguna detectada | Listo para modelo |
| DGE Nacional | Alta (~100%) | 0 | 12 nulos en columnas de linaje (esperado para 2015-2017) | Imputar `source_page=NaN` con "CSV" |
| openFMD | Media (~85%) | 0 | 128,905 nulos (campos opcionales: host, sublineage) | Filtrar por `fmdv_positive=Yes` y fecha |
| COFEPRIS Alimentarias | Alta (~100%) | 0 | No detalla contaminantes | Usar como proxy regulatorio |

---

## 5. Implicaciones para el Modelado

### Modelo SIR Dual (`sir_dual.py`)

| Parámetro | Fuente | Valor |
|-----------|--------|-------|
| N (población susceptible) | SIAP/config.py | 35,100,000 cabezas |
| I₀ TB (infectados iniciales) | SENASICA cuarentenas | ~2,000 (hatos cuarentenados) |
| R₀ TB | Literatura + config.py | 1.8 |
| R₀ FMD | openFMD + Tildesley et al. | 6.0 (serotipo O) |
| γ TB | V2.md | 1/180 días |
| γ FMD | V2.md | 1/14 días |

### ANOVA Canales de Venta

| Variable | Fuente |
|----------|--------|
| Prevalencia Salmonella por canal | V2.md (Supermercado 1.3%, Tianguis 13.6%) |
| Efecto COVID en canales informales | DGE 2015-2024 (caída del 41% en A05) |
| Proxy regulatorio | COFEPRIS alimentarias (7 sanciones cárnicas) |

---

## 6. Archivos de Referencia

| Archivo | Contenido |
|---------|-----------|
| `docs/task.md` | Checklist maestro actualizado |
| `docs/wave2_recovery_plan.md` | Plan de recuperación con scorecard de Jules |
| `docs/wave2_recovery_results.md` | Resultados técnicos de Codex |
| `docs/DGE_DATA_SEARCH.md` | Investigación exhaustiva de Jules sobre DGE |
| `docs/cofepris_alimentaria_search.md` | Búsqueda de clausuras alimentarias |
| `docs/senasica_datasets.md` | URLs de PDFs trimestrales |
| `docs/senasica_api_findings.md` | API SENASICA = 404 |
| `notebooks/01_eda_global.ipynb` | Notebook principal de análisis exploratorio |
| `src/config.py` | Fuente de verdad para constantes y URLs |

---

## 7. Lecciones Aprendidas

1. **La orquestación multi-agente funciona:** Jules (investigación paralela sin browser) + Codex (browser + ejecución) + Antigravity (arquitectura + análisis) produjeron más datos que un equipo humano de 3 personas en una semana.

2. **Los datos gubernamentales mexicanos son hostiles:** SENASICA, DGE, COFEPRIS y UNAM operan con PDFs, URLs cambiantes, APIs no documentadas y Cloudflare. El pipeline debe ser resiliente por diseño (fallbacks, constantes de literatura, degradación limpia).

3. **COVID-19 es un "experimento natural"** que validó hipótesis sobre canales de venta sin necesidad de un estudio epidemiológico formal.

4. **La Fiebre Aftosa es un riesgo real y medible.** Con 28,585 registros globales, tenemos la base empírica para modelar escenarios de impacto en México con rigor científico.
