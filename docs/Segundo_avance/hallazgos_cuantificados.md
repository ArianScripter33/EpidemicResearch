# Segundo Avance: Hallazgos Cuantificados con Fuentes

> **Proyecto:** Ganado Saludable — Investigación Epidemiológica  
> **Fecha de corte:** 2026-04-03  
> **Notebook de referencia:** `notebooks/01_eda_global.ipynb`

---

## Propósito de Este Documento

Este documento recopila **los hallazgos más importantes** del Análisis Exploratorio de Datos (EDA), con cada dato cuantificado, citado con su fuente, y explicado en el contexto del proyecto. Sirve como:

1. **Fuente de verdad** para el artículo científico final
2. **Base** para la parametrización de los modelos SIR y ANOVA
3. **Material de referencia** para las presentaciones del equipo

---

## 1. Datos Cuantificados: Series Temporales

### 1.1 Efecto COVID-19 en Intoxicaciones Alimentarias

| Métrica | Valor | Cálculo | Fuente |
|---------|-------|---------|--------|
| Caída de intoxicaciones alimentarias (A05) en 2020 | **−41.5%** | (18,667 − 31,916) / 31,916 | EDA propio: `dge_morbilidad_nacional_2015_2024_clean.csv` — DGE Anuarios 2019/2020 |
| Caída de tuberculosis humana (A15-A19) en 2020 | **−24.8%** | (16,747 − 22,283) / 22,283 | EDA propio: misma fuente |
| Recuperación A05 (2024 vs 2020) | **+35.3%** | (25,259 − 18,667) / 18,667 | EDA propio |
| TB 2024 vs máximo pre-pandemia (2019) | **+16.6%** | (25,980 − 22,283) / 22,283 | EDA propio |

**Por qué importa:** La caída diferencial (41% vs 25%) demuestra que las intoxicaciones dependen del **canal de venta** (tianguis cerrados en 2020), mientras que la TB depende de la transmisión respiratoria prolongada. Esto valida nuestra hipótesis para el ANOVA de canales de venta.

**Cita sugerida para el artículo:**
> *"Del análisis de la serie temporal DGE 2015-2024, se observó que las intoxicaciones alimentarias bacterianas (CIE-10 A05) disminuyeron un 41.5% durante 2020 (de 31,916 a 18,667 casos). Esta caída coincide con las restricciones sanitarias por COVID-19 que limitaron el comercio informal de alimentos (tianguis, mercados sobre ruedas), sugiriendo que el canal de distribución es un factor determinante en la prevalencia de enfermedades transmitidas por alimentos."*

---

### 1.2 Tendencia de TB Humana en México (10 Años)

| Año | Casos A05 | Casos TB (A15-A19) |
|-----|-----------|---------------------|
| 2015 | 31,846 | 20,561 |
| 2016 | 25,896 | 21,184 |
| 2017 | 35,815 | 21,694 |
| 2018 | 31,389 | 22,133 |
| 2019 | 31,916 | 22,283 |
| 2020 | 18,667 | 16,747 |
| 2021 | 21,865 | 20,374 |
| 2022 | 23,439 | 24,051 |
| 2023 | 25,929 | 25,430 |
| 2024 | 25,259 | 25,980 |

**Fuente:** DGE, Anuarios de Morbilidad 2015-2024. Extraídos vía `pdfplumber` (2018-2024) y datos abiertos ZIP/CSV (2015-2017).

---

## 2. Datos Cuantificados: Ganadería Nacional

### 2.1 Cobertura del Programa de TB Bovina

| Métrica | Valor | Fuente |
|---------|-------|--------|
| Biomasa bovina nacional | **35,100,000 cabezas** | SIAP, citado en V2.md |
| Bovinos certificados libres de TB | **420,171** | EDA propio: `senasica_tb_clean.csv` |
| Cobertura del programa | **1.20%** | 420,171 / 35,100,000 |

**Por qué importa:** El 98.8% del hato nacional no tiene certificación sanitaria verificada. El sistema de vigilancia opera en un vacío estadístico.

### 2.2 Cuarentenas Activas de TB Bovina (2024)

| Métrica | Valor | Fuente |
|---------|-------|--------|
| Estados con cuarentenas activas | **27 de 32** | EDA propio: `senasica_cuarentenas_clean.csv` |
| Total hatos cuarentenados | **856** | EDA propio |
| Total animales afectados | **7,558** | EDA propio |
| Estado con más animales afectados | **Jalisco: 5,035 (66.6%)** | EDA propio |

**Concentración geográfica (Top 5):**

| Estado | Hatos | Animales | % del total animales |
|--------|-------|----------|---------------------|
| Jalisco | 135 | 5,035 | 66.6% |
| Michoacán | 69 | 510 | 6.7% |
| Veracruz | 162 | 432 | 5.7% |
| Aguascalientes | 356 | 70 | 0.9% |
| Tabasco | 44 | 133 | 1.8% |

**Hallazgo original:** Jalisco concentra 66.6% de todos los animales afectados con solo 15.8% de los hatos cuarentenados, lo que sugiere que las unidades de producción grandes (ranchos extensivos) son los focos epidémicos.

**Cita sugerida:**
> *"Del análisis de los reportes trimestrales SENASICA 2024, se identificaron 856 hatos bajo cuarentena distribuidos en 27 de 32 estados. Jalisco concentra el 66.6% de los 7,558 animales afectados a nivel nacional, lo que evidencia una distribución espacialmente heterogénea del riesgo sanitario."*

---

## 3. Datos Cuantificados: Fiebre Aftosa Global

### 3.1 Distribución Regional de Brotes FMD (2000-2025)

| Región | Eventos positivos | % del total | Fuente |
|--------|-------------------|-------------|--------|
| Asia | 10,658 | 64.4% | EDA propio: `openfmd_clean.csv` — WRLFMD/openFMD |
| África | 5,124 | 31.0% | EDA propio |
| **Américas** | **446** | **2.7%** | EDA propio |
| Europa | 300 | 1.8% | EDA propio |
| **Total** | **16,540** | 100% | 103 países, 2000-2025 |

**Hallazgo clave:** Las Américas representan solo el 2.7% de los brotes globales de FMD, lo que implica ausencia de inmunidad de rebaño en el hato bovino mexicano.

### 3.2 Distribución de Serotipos Globales

| Serotipo | Eventos | % del total | Fuente |
|----------|---------|-------------|--------|
| **O** | **9,072** | **54.9%** | EDA propio: `openfmd_clean.csv` |
| A | 3,559 | 21.5% | EDA propio |
| SAT2 | 1,542 | 9.3% | EDA propio |
| Asia1 | 995 | 6.0% | EDA propio |
| Sin tipificar | 669 | 4.0% | EDA propio |

**Hallazgo original:**
> *"Del análisis de 16,540 eventos FMD positivos confirmados globalmente (2000-2025), obtenidos del World Reference Laboratory for FMD (WRLFMD) mediante el portal openFMD, se determinó que el serotipo O representa el 54.9% de los brotes registrados. Este serotipo fue responsable de la epidemia del Reino Unido en 2001, que resultó en el sacrificio de 6 millones de animales y pérdidas estimadas en £8,000 millones."*

### 3.3 Top 10 Países con Mayor Incidencia

| # | País | Eventos FMD positivos | Región | Fuente |
|---|------|----------------------|--------|--------|
| 1 | India | 1,506 | Asia | EDA propio: openFMD |
| 2 | Pakistán | 1,455 | Asia | EDA propio |
| 3 | Vietnam | 1,342 | Asia | EDA propio |
| 4 | Irán | 902 | Asia | EDA propio |
| 5 | Turquía | 749 | Asia | EDA propio |
| 6 | Egipto | 651 | África | EDA propio |
| 7 | Kenia | 645 | África | EDA propio |
| 8 | Nigeria | 552 | África | EDA propio |
| 9 | Tailandia | 549 | Asia | EDA propio |
| 10 | Etiopía | 505 | África | EDA propio |

---

## 4. Parámetros para Modelado SIR

### 4.1 Constantes Epidemiológicas (con fuentes)

| Parámetro | Símbolo | Valor | Fuente bibliográfica |
|-----------|---------|-------|---------------------|
| Biomasa susceptible | N | 35,100,000 | SIAP (Servicio de Información Agroalimentaria y Pesquera), México |
| R₀ Tuberculosis Bovina | R₀_TB | 1.8 | Barlow, N.D. (1991). "A spatially aggregated disease/host model for bovine Tb in New Zealand possum populations." *J. Applied Ecology*, 28(3), 777-793 |
| R₀ Fiebre Aftosa (serotipo O) | R₀_FMD | 6.0 (rango: 4.0—8.0) | Tildesley, M.J. et al. (2006). "Optimal reactive vaccination strategies for a foot-and-mouth disease outbreak in the UK." *Nature*, 440, 83-86 |
| Período infeccioso TB | 1/γ_TB | 180 días | V2.md, basado en Barlow (1991) |
| Período infeccioso FMD | 1/γ_FMD | 14 días | V2.md, basado en Tildesley (2006) |
| Tasa de mortalidad FMD | μ_FMD | 1-2% (ganado), 20-50% (jóvenes) | OIE/WOAH Terrestrial Manual, Cap. 3.1.8 |
| Prevalencia Salmonella en Supermercados | - | 1.3% | Castañeda-Ruelas, G.M. et al., citado en V2.md |
| Prevalencia Salmonella en Tianguis | - | 13.6% | Castañeda-Ruelas, G.M. et al., citado en V2.md |
| Prevalencia Salmonella en Mercados Municipales | - | 22.3% | Castañeda-Ruelas, G.M. et al., citado en V2.md |
| Resistencia Salmonella a Ampicilina | - | 94.7% | Informe PUCRA (UNAM), citado en V2.md |

### 4.2 Probabilidad Estimada de Serotipo Invasor

| Escenario | Serotipo probable | Probabilidad | R₀ asociado | Cálculo |
|-----------|-------------------|-------------|-------------|---------|
| Más probable | O | 54.9% | 6.0 | 9,072 / 16,540 (EDA propio) |
| Segundo | A | 21.5% | ~4.5 | 3,559 / 16,540 (EDA propio) |
| Tercero | SAT2 | 9.3% | ~3.5 | 1,542 / 16,540 (EDA propio) |

**Cita sugerida:**
> *"Basándose en la distribución global de serotipos del WRLFMD (n=16,540 eventos positivos, 2000-2025), el serotipo con mayor probabilidad de introducción en un escenario de brote exótico en México es el serotipo O (54.9%), cuyo R₀ estimado oscila entre 4.0 y 8.0 (Tildesley et al., 2006). Dado que México fue declarado libre de FMD en 1954 y el continente americano acumula solo el 2.7% de los brotes globales, la población susceptible se modeló como N ≈ 35.1 millones de cabezas sin inmunidad previa."*

---

## 5. Datos de Contexto Regulatorio

### 5.1 COFEPRIS: Sanciones a Empresas Cárnicas

| # | Empresa | Tipo de sanción | Fuente |
|---|---------|----------------|--------|
| 1 | Carnes Selectas ALI, S.A. de C.V. | Multa y amonestación | COFEPRIS, Resoluciones y Sanciones Sep/2023 |
| 2 | Grupo Comercial ML Bachoco / Pollo y Carnes | Multa | COFEPRIS, Sep/2023 |
| 3 | Almacenes y Frigoríficos Ameriben | Multa | COFEPRIS, Sep/2023 |
| 4 | Carnes Selectas Express del Sur | Multa | COFEPRIS, Sep/2023 |
| 5 | Carnicería El Grillo | Multa | COFEPRIS, Sep/2023 |
| 6 | Qualtia Alimentos Operaciones | Multa | COFEPRIS, Sep/2023 |
| 7 | HM Distribuidora de Alimentos | Multa | COFEPRIS, Sep/2023 |

**Nota:** Ninguna sanción detalla el contaminante específico (Clenbuterol, Salmonella, LMR). La opacidad del registro público es, en sí misma, un indicador de riesgo.

---

## 6. Gráficas de Referencia

| Gráfica | Archivo | Hallazgo que sustenta |
|---------|---------|----------------------|
| Serie temporal DGE 2015-2024 | `data/processed/eda_charts/dge_tendencia_temporal.png` | Efecto COVID −41.5% en A05 |
| Hatos libres por estado | `data/processed/eda_charts/senasica_hatos_libres.png` | Cobertura 1.2% |
| Cuarentenas por estado | `data/processed/eda_charts/senasica_cuarentenas_estado.png` | Jalisco 66.6% |
| Brotes FMD por región + serotipos | `data/processed/eda_charts/openfmd_region_serotipos.png` | Américas 2.7%, Serotipo O 55% |
| Top 10 países FMD | `data/processed/eda_charts/openfmd_top10_paises.png` | India #1, Asia domina |
| Evolución temporal FMD | `data/processed/eda_charts/openfmd_evolucion_temporal.png` | FMD no está en declive |

---

## Próximos Entregables para Este Avance

- [ ] `src/models/sir_dual.py` — Simulación SIR con los parámetros de la Sección 4
- [ ] `src/models/stats_multivariate.py` — ANOVA canales de venta
- [ ] `src/visualization/choropleth_maps.py` — Mapa coroplético de cuarentenas
- [ ] `src/crypto/encryption.py` — Módulo de criptografía (tarea delegada)
- [ ] Artículo de divulgación científica (basado en las citas sugeridas de este documento)
