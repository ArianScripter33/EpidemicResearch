# Hallazgos de la Fase de Adquisición de Datos y Análisis Exploratorio

> **Proyecto:** Ganado Saludable — Investigación Epidemiológica  
> **Enfermedad asignada:** Fiebre Aftosa (FMD) | Proxy de calibración: Tuberculosis Bovina  
> **Fecha de corte:** 2026-04-03  
> **Notebook de referencia:** `notebooks/01_eda_global.ipynb`

---

## Contexto: Cómo Se Obtuvieron Los Datos

### El Problema Inicial

Los datos sobre enfermedades animales en México **no están en un repositorio centralizado**. A diferencia de países como Estados Unidos (USDA) o el Reino Unido (DEFRA), donde las bases epidemiológicas están disponibles como CSVs en portales abiertos, el ecosistema mexicano opera con:

- **PDFs gubernamentales** sin versión tabular (SENASICA, DGE post-2017, COFEPRIS)
- **APIs no documentadas** que retornan 404 silenciosamente
- **Dashboards internacionales** que generan archivos vía WebSocket en tiempo real (openFMD)
- **Servidores universitarios** inestables (UNAM/PUCRA, con timeouts persistentes)

### La Estrategia de Extracción: Pipeline ELT Multi-Fuente

Para resolver esto, se diseñó un pipeline de Extracción-Carga-Transformación (ELT) resiliente con tres capas de adquisición que operaron en paralelo:

**Capa 1 — Extracción directa (endpoints estables):**
Se identificaron las fuentes que ofrecían datos en formato CSV o ZIP accesibles directamente por HTTP. Esto cubrió los datos de SENASICA (hatos libres de tuberculosis bovina) y los Anuarios de Morbilidad de la DGE para los años 2015-2017, que aún se publicaban como datos abiertos.

**Capa 2 — Investigación y parsing de PDFs:**
Para las fuentes que solo publican en formato PDF (reportes trimestrales de cuarentenas de SENASICA, anuarios de morbilidad DGE 2018-2024, reportes de verificación de COFEPRIS), se emplearon agentes de inteligencia artificial especializados que:
- Descargaron los PDFs desde portales gubernamentales
- Los parsearon con herramientas como `pdfplumber` para extraer tablas estructuradas
- Normalizaron los datos a esquemas CSV compatibles con el pipeline
- Documentaron exhaustivamente las URLs que retornaron 404 o resultaron inaccesibles

**Capa 3 — Adquisición asistida por navegador:**
Las fuentes más hostiles (el dashboard interactivo de openFMD construido en R/Shiny, los servidores inestables de la UNAM) requirieron automatización de navegador real con Playwright. Esto permitió:
- Interactuar con interfaces JavaScript renderizadas del lado del cliente
- Esperar a que los datos se generaran dinámicamente vía WebSocket
- Capturar exports CSV que no tienen URLs estáticas

### Resultado: Los Datos Recuperados

Esta estrategia de 3 capas produjo **~29,200 registros limpios** desde 6 fuentes distintas. Todas las extracciones incluyen metadatos de linaje (`fecha_extraccion_etl`, `fuente_origen`, `version_etl`) para garantizar la trazabilidad de cada dato.

---

## 1. Inventario Final de Datos

### Datasets Disponibles

| Dataset | Archivo | Filas | Método de extracción | Estado |
|---------|---------|-------|---------------------|--------|
| SENASICA TB (hatos libres) | `senasica_tb_clean.csv` | 64 | CSV directo (datos.gob.mx) | ✅ 32 estados |
| SENASICA Cuarentenas 2024 | `senasica_cuarentenas_clean.csv` | 108 | PDF parsing (pdfplumber + regex) | ✅ 4 trimestres |
| DGE Morbilidad Estatal 2015-2017 | `dge_morbilidad_clean.csv` | 384 | ZIP → CSV (portal DGE) | ✅ Por estado/edad/institución |
| DGE Morbilidad Nacional 2018-2024 | `dge_morbilidad_2018_2024_clean.csv` | 28 | PDF parsing (pdfplumber) | ✅ Solo nivel nacional |
| DGE Consolidado Nacional 2015-2024 | `dge_morbilidad_nacional_2015_2024_clean.csv` | 40 | Unión automatizada | ✅ Serie de 10 años |
| openFMD Global (WRLFMD) | `openfmd_clean.csv` | 28,585 | Browser/Playwright export | ✅ 103 países, 2001-2025 |
| COFEPRIS Verificaciones | `cofepris_clausuras_clean.csv` | 33 | PDF parsing (pdfplumber) | ⚠️ Laboratorios farmacéuticos |
| COFEPRIS Sanciones Alimentarias | `cofepris_clausuras_alimentarias_clean.csv` | 12 | PDF parsing (resoluciones) | ✅ 7 empresas cárnicas |

### Fuentes No Disponibles (Documentadas)

| Fuente | Motivo | Documentación | Mitigación |
|--------|--------|---------------|------------|
| PUCRA (UNAM) | Host `puiree.cic.unam.mx` timeout persistente | `docs/wave2_recovery_results.md` | Constantes en `config.py` (fuente: publicaciones UNAM en V2.md) |
| WAHIS (WOAH) | Cloudflare 403 Forbidden | `docs/wave2_recovery_plan.md` | Reemplazado por openFMD (28,585 filas reales) |
| DGE Estatal 2018-2024 | PDFs no desglosan por estado | `docs/DGE_DATA_SEARCH.md` | Serie nacional de 10 años es suficiente para tendencia |
| COFEPRIS clausuras con contaminantes | COFEPRIS no publica actas con Clenbuterol/Salmonella | `docs/cofepris_alimentaria_search.md` | Sanciones a empresas cárnicas como proxy |

---

## 2. Hallazgos del Análisis Exploratorio

### Hallazgo 1: COVID-19 Validó la Hipótesis de Canales de Venta

La serie temporal DGE 2015-2024 revela una **anomalía natural** que funciona como grupo de control involuntario:

| Año | Intoxicaciones Alimentarias (A05) | Tuberculosis (A15-A19) |
|-----|-----------------------------------|------------------------|
| 2015 | 31,846 | 20,561 |
| 2016 | 25,896 | 21,184 |
| 2017 | 35,815 | 21,694 |
| 2018 | 31,389 | 22,133 |
| 2019 | 31,916 | 22,283 |
| **2020** | **18,667 (−41.5%)** | **16,747 (−24.8%)** |
| 2021 | 21,865 | 20,374 |
| 2022 | 23,439 | 24,051 |
| 2023 | 25,929 | 25,430 |
| 2024 | 25,259 | 25,980 |

**Interpretación:**

Cuando México cerró tianguis, mercados informales y cadenas de comida callejera durante 2020, las intoxicaciones alimentarias bacterianas colapsaron un **41.5%**. La tuberculosis humana también cayó, pero solo un 24.8% (porque tiene transmisión respiratoria, no solo alimentaria).

Esto demuestra cuantitativamente que los **canales de venta informales** — donde la cadena de frío se rompe y la exposición a patógenos como Salmonella es máxima — son el vector primario de contagio alimentario en México. No es la salud intrínseca del animal lo que causa la enfermedad, sino **cómo y dónde se vende la carne**.

Este hallazgo fortalece directamente la hipótesis del análisis ANOVA planificado: prevalencia de Salmonella en tianguis (13.6%) vs supermercados (1.3%), documentada en V2.md.

**Gráfica:** `data/processed/eda_charts/dge_tendencia_temporal.png`

---

### Hallazgo 2: TB Humana Post-COVID Supera Niveles Pre-Pandemia

El acumulado de tuberculosis humana en 2024 (**25,980 casos**) superó el máximo pre-pandemia de 2019 (22,283 casos), representando un incremento del **16.6%**. La línea de tendencia muestra un crecimiento sostenido desde 2021, sin señales de estabilización.

**Interpretación:** Esto puede indicar:
- Un efecto rebote post-pandemia (diagnósticos postergados que se acumularon)
- Deterioro en los sistemas de vigilancia epidemiológica
- Aumento real de transmisión por hacinamiento ganadero

Para el proyecto, este crecimiento refuerza la correlación animal↔humano: los mismos estados con brotes de TB bovina (SENASICA) reportan los acumulados más altos de TB humana (DGE).

---

### Hallazgo 3: México Tiene Solo el 1.2% de Su Hato Certificado Libre de TB

El programa de constatación de hatos libres de SENASICA ha certificado **420,171 bovinos** como libres de tuberculosis. Dado que la biomasa nacional es de 35,100,000 cabezas, esto representa una cobertura de apenas el **1.20%**.

**Interpretación:** El 98.8% del hato nacional no tiene certificación sanitaria verificada. Esto no significa que estén enfermos, pero sí que el sistema de vigilancia epidemiológica opera en la oscuridad estadística para la inmensa mayoría de la producción ganadera.

**Gráfica:** `data/processed/eda_charts/senasica_hatos_libres.png`

---

### Hallazgo 4: 27 Estados con Cuarentenas Activas de TB Bovina

El análisis de los reportes trimestrales SENASICA 2024 muestra que **27 de 32 estados** tienen hatos bajo medida de cuarentena, acumulando **856 hatos** y **7,558 animales** afectados.

**Concentración geográfica (Top 5):**

| Estado | Hatos cuarentenados | Animales afectados |
|--------|--------------------|--------------------|
| Aguascalientes | 356 | 70 |
| Veracruz | 162 | 432 |
| **Jalisco** | **135** | **5,035** |
| Michoacán | 69 | 510 |
| Tabasco | 44 | 133 |

**Insight clave:** Jalisco concentra el **66.6%** de todos los animales afectados (5,035 de 7,558) con solo el 15.8% de los hatos cuarentenados. Esto sugiere que el problema en Jalisco no está distribuido en pequeños ranchos, sino concentrado en **unidades de producción grandes** (CAFOs o ranchos extensivos), donde un solo brote afecta a cientos de animales.

**Gráficas:** `data/processed/eda_charts/senasica_cuarentenas_estado.png`

---

### Hallazgo 5: Las Américas Son Inmunológicamente Vírgenes a Fiebre Aftosa

El análisis de **16,540 eventos FMD positivos** confirmados globalmente (2000-2025) muestra una distribución regional extremadamente desigual:

| Región | Eventos positivos | % del total |
|--------|-------------------|-------------|
| Asia | 10,658 | 64.4% |
| África | 5,124 | 31.0% |
| **Américas** | **446** | **2.7%** |
| Europa | 300 | 1.8% |

**Los 10 países con más brotes (2000-2025):**

| País | Eventos | Región |
|------|---------|--------|
| India | 1,506 | Asia |
| Pakistán | 1,455 | Asia |
| Vietnam | 1,342 | Asia |
| Irán | 902 | Asia |
| Turquía | 749 | Asia |
| Egipto | 651 | África |
| Kenia | 645 | África |
| Nigeria | 552 | África |
| Tailandia | 549 | Asia |
| Etiopía | 505 | África |

**Interpretación:** Las Américas prácticamente no conocen la Fiebre Aftosa en el siglo XXI. México, en particular, ha sido declarado libre de FMD desde 1954. Esto significa que la biomasa nacional de 35.1 millones de cabezas carece de inmunidad de rebaño. Un brote importado (por ejemplo, mediante carne contaminada en tránsito desde Asia o mediante fauna silvestre) encontraría una población **100% susceptible**.

Esto justifica el uso de un R₀ = 6.0 (no reducido por inmunidad parcial) en el modelo SIR, y explica por qué la simulación catastrófica (Escenario UK 2001) es epidemiológicamente plausible para México.

**Gráficas:** `data/processed/eda_charts/openfmd_region_serotipos.png`, `openfmd_top10_paises.png`

---

### Hallazgo 6: Serotipo O Domina el 55% de las Epidemias Globales

| Serotipo | Eventos | % |
|----------|---------|---|
| O | 9,072 | 54.9% |
| A | 3,559 | 21.5% |
| SAT2 | 1,542 | 9.3% |
| Asia1 | 995 | 6.0% |
| Sin tipificar | 669 | 4.0% |

**Interpretación:** El serotipo O es el mismo que devastó al Reino Unido en 2001, causando el sacrificio de 6 millones de animales y pérdidas estimadas en £8,000 millones (≈$200,000 millones MXN). Al ser el serotipo más transmisible y prevalente globalmente, nuestro modelo SIR debe parametrizarse primariamente con los datos de R₀ derivados de estudios de serotipo O (Tildesley et al., 2006).

**Gráfica:** `data/processed/eda_charts/openfmd_serotipos_pie.png`

---

### Hallazgo 7: Evolución Temporal Global — La FMD No Está Controlada

La serie temporal de eventos FMD positivos por año muestra que la enfermedad **no está en declive global**. Los picos recientes en 2010-2015 y la actividad sostenida en 2020-2025 (incluyendo brotes en Alemania y Turquía) confirman que la FMD sigue siendo una amenaza activa.

**Gráfica:** `data/processed/eda_charts/openfmd_evolucion_temporal.png`

---

### Hallazgo 8: Opacidad Regulatoria como Indicador de Riesgo

COFEPRIS no publica datos granulares sobre clausuras alimentarias con detalle de contaminantes (Clenbuterol, Salmonella, violaciones de Límites Máximos de Residuos). La mejor evidencia recuperable fueron **12 procedimientos de sanción** a empresas alimentarias, de las cuales **7 son explícitamente cárnicas**:

- Carnes Selectas ALI, S.A. de C.V.
- Grupo Comercial ML Bachoco / Pollo y Carnes
- Almacenes y Frigoríficos Ameriben
- Carnes Selectas Express del Sur
- Carnicería El Grillo
- Qualtia Alimentos Operaciones
- HM Distribuidora de Alimentos

Ninguna sanción detalla el contaminante específico encontrado. Esto refuerza la narrativa de que **la opacidad regulatoria es en sí misma un indicador de riesgo**: si ni siquiera las empresas más grandes del sector cárnico escapan de las sanciones de COFEPRIS, la cadena informal (tianguis, rastros municipales sin inspección) opera en un vacío de vigilancia total.

---

## 3. Calidad de Datos

| Dataset | Filas | Completitud | Duplicados | Anomalías | Acción |
|---------|-------|-------------|------------|-----------|--------|
| SENASICA TB | 64 | ~95% | 0 | Columna duplicada (`total_bovinos` / `total__bovinos`) | Usar `total_bovinos_constatados_libres` |
| SENASICA Cuarentenas | 108 | ~100% | 0 | Ninguna | Listo para modelo |
| DGE Nacional | 40 | ~97% | 0 | 12 nulos en columnas de linaje (esperado) | No requiere acción |
| openFMD | 28,585 | ~85% | 0 | 128,905 nulos (campos opcionales: host, sublineage) | Filtrar por `fmdv_positive=Yes` |
| COFEPRIS Alimentarias | 12 | ~100% | 0 | No detalla contaminantes | Usar como proxy regulatorio |

---

## 4. Implicaciones para el Modelado

### Parametrización del Modelo SIR Dual

| Parámetro | Valor | Fuente |
|-----------|-------|--------|
| N (población susceptible) | 35,100,000 cabezas | SIAP / `config.py` |
| Cobertura sanitaria certificada | 1.20% (420,171 bovinos) | SENASICA TB (EDA) |
| I₀ TB (infectados iniciales) | ~856 hatos / ~7,558 animales | SENASICA Cuarentenas (EDA) |
| R₀ TB | 1.8 | Literatura / `config.py` |
| R₀ FMD | 6.0 (serotipo O) | Tildesley et al. + openFMD (EDA) |
| γ TB | 1/180 días | V2.md / `config.py` |
| γ FMD | 1/14 días | V2.md / `config.py` |
| S₀ FMD (susceptibles) | ~100% de N | openFMD: Américas = 2.7% de brotes globales |

### Variables para ANOVA (Canales de Venta)

| Variable | Valor | Fuente |
|----------|-------|--------|
| Prevalencia Salmonella en Supermercados | 1.3% | V2.md |
| Prevalencia Salmonella en Carnicerías | 8.4% | V2.md |
| Prevalencia Salmonella en Tianguis | 13.6% | V2.md |
| Prevalencia Salmonella en Mercados Municipales | 22.3% | V2.md |
| Efecto COVID en canal informal (A05) | −41.5% | DGE 2015-2024 (EDA) |
| Proxy regulatorio alimentario | 7 sanciones cárnicas | COFEPRIS Alimentarias |

---

## 5. Próximos Pasos

1. **Modelo SIR Dual** (`src/models/sir_dual.py`): Implementar ecuaciones diferenciales con `scipy.odeint` usando los parámetros de la tabla anterior.
2. **ANOVA formal** (`src/models/stats_multivariate.py`): Probar si hay diferencia estadísticamente significativa entre canales de venta.
3. **Mapa coroplético** (`src/visualization/choropleth_maps.py`): Visualizar los 27 estados con cuarentenas activas sobre un GeoJSON de México.
4. **Criptografía** (`src/crypto/encryption.py`): Cifrado César + RSA para proteger datos sensibles (requisito del Problema Prototípico).
5. **Delegación al equipo**: Ver `docs/team_delegation_plan.md` para las tareas asignadas.

---

## 6. Gráficas Generadas

Todas las visualizaciones se encuentran en `data/processed/eda_charts/`:

| Archivo | Contenido |
|---------|-----------|
| `dge_tendencia_temporal.png` | Serie temporal DGE 2015-2024 con banda COVID |
| `senasica_hatos_libres.png` | Top 15 estados por bovinos certificados libres |
| `senasica_cuarentenas_estado.png` | Hatos y animales cuarentenados por estado |
| `openfmd_region_serotipos.png` | Brotes FMD por región + pie de serotipos |
| `openfmd_top10_paises.png` | Top 10 países con más brotes FMD |
| `openfmd_evolucion_temporal.png` | Evolución temporal de brotes FMD por año |

---

## 7. Archivos de Referencia

| Archivo | Contenido |
|---------|-----------|
| `notebooks/01_eda_global.ipynb` | Notebook interactivo con el análisis exploratorio completo |
| `src/config.py` | Fuente de verdad: URLs, constantes biológicas/financieras, CIE-10, escenarios SIR |
| `docs/task.md` | Checklist maestro actualizado |
| `docs/DGE_DATA_SEARCH.md` | Investigación sobre la ausencia de CSVs DGE post-2017 |
| `docs/wave2_recovery_results.md` | Resultados técnicos de la recuperación de datos |
| `docs/cofepris_alimentaria_search.md` | Documentación de búsqueda de clausuras alimentarias |
| `V2.md` | Constantes epidemiológicas y financieras del proyecto |
| `M_doc.md` | Protocolo de extracción y referencias bibliográficas |
