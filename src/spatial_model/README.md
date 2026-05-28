# Pipeline de Simulación Epidemiológica Espacial — FMD México

> Modelo Gravitatorio + SIR sobre Grafo + XGBoost Risk Scoring
> Generado automáticamente. Última actualización: Mayo 2026.

---

## Arquitectura del Pipeline

```
data/raw/
├── inegi/estados_mexico.geojson     # Polígonos de 32 estados (fuente: INEGI via GitHub)
└── siap/inventario_bovino_2023.csv  # Inventario bovino oficial (fuente: SIAP/SADER)

data/processed/spatial/
├── nodos_estados.geojson            # Estados con centroides calculados (EPSG:6372)
├── nodos_estados.csv                # Tabla plana de nodos (lat, lon, inventario)
├── distancias_carretera.csv         # Matriz NxN de distancias reales por carretera (OSRM)
├── matriz_gravedad.csv              # Red gravitatoria: 992 conexiones con F_ij y prob_contagio
├── edges_gravedad.json              # Mismo dato en JSON (para web apps)
├── sir_full_state_history_180d.csv  # Historial completo S-I-R por estado por día (5,760 registros)
├── sir_simulation_results_180d.csv  # Historial agregado nacional
├── sir_state_history_180d.csv       # Solo columna I por estado (para bar chart race)
├── fmd_spread_simulation.gif        # Animación del mapa (45 días)
├── fmd_spread_simulation_180d.gif   # Animación del mapa (180 días)
├── bar_chart_race.html              # Animación interactiva tipo YouTube (45 días)
├── bar_chart_race_180d.html         # Animación interactiva tipo YouTube (180 días)
├── xgboost_features.csv             # Features de grafo + targets del SIR
├── sir_vs_xgboost_comparison.csv    # Tabla comparativa SIR vs XGBoost
└── charts/
    ├── sir_nacional_apilado.png       # Gráfica apilada S-I-R nacional
    ├── sir_top8_estados_apilado.png   # Gráficas apiladas top 8 estados
    ├── xgboost_importance_*.png       # Feature importance del XGBoost
    ├── sir_vs_xgboost_*.png           # Scatter plots SIR vs XGB
    └── tabla_cronologia_infeccion.csv # Cronología de infección por estado
```

---

## Scripts del Pipeline (Orden de Ejecución)

### Fase 1: Extracción y Preprocesamiento

| Script | Propósito | Input | Output |
| --- | --- | --- | --- |
| `01_data_prep.py` | Une polígonos INEGI con inventario SIAP. Proyecta a EPSG:6372 (Lambert México) y calcula centroides precisos en metros. | `data/raw/inegi/*.geojson`, `data/raw/siap/*.csv` | `nodos_estados.geojson`, `nodos_estados.csv` |
| `01b_road_distances.py` | Consulta la API pública de OSRM para obtener la matriz 32x32 de distancias reales por carretera entre capitales estatales. | `nodos_estados.csv` | `distancias_carretera.csv` |

### Fase 2: Modelo Gravitatorio

| Script | Propósito | Input | Output |
| --- | --- | --- | --- |
| `02_gravity_model.py` | Calcula la fuerza gravitatoria F_ij = k * (P_i * P_j) / d_ij² para los 992 pares de estados. Normaliza a probabilidad de contagio base [0, 1]. | `nodos_estados.csv`, `distancias_carretera.csv` | `matriz_gravedad.csv`, `edges_gravedad.json` |

**Fórmula Gravitatoria:**
```
F_ij = K * (P_i^α * P_j^β) / d_ij^γ

Donde:
  K     = 1e-6 (escalar)
  P_i   = inventario bovino del estado i
  P_j   = inventario bovino del estado j
  d_ij  = distancia por carretera en km (OSRM)
  α = β = 1.0, γ = 2.0
```

### Fase 3: Simulación SIR Espacial

| Script | Propósito | Input | Output |
| --- | --- | --- | --- |
| `03_spatial_sir.py` | Simulación SIR de 180 días con propagación estocástica entre estados. Genera GIF animado del mapa. | `nodos_estados.geojson`, `matriz_gravedad.csv` | `fmd_spread_simulation_180d.gif`, `sir_state_history_180d.csv` |
| `03b_sir_full_history.py` | Re-corre el SIR guardando los 3 compartimentos (S, I, R) por estado por día. Alimenta las gráficas apiladas y el XGBoost. | Mismos | `sir_full_state_history_180d.csv` |

**Parámetros Epidémicos:**
```
β (tasa contagio local)    = 0.6
γ (tasa sacrificio/remoción) = 0.1  (periodo infeccioso ~10 días)
β_spatial (fuerza inter-estatal) = 0.8
Paciente Cero: Veracruz, 100 cabezas
Semilla aleatoria: 42 (reproducible)
```

**Mecánica de Propagación Espacial:**
```
Para cada estado infectado i:
  prevalencia_i = I_i / N_i
  Para cada estado sano j:
    prob_chispazo = prob_gravedad_ij * prevalencia_i * β_spatial
    Si random() < prob_chispazo:
      Estado j se infecta con 50 cabezas iniciales
```

### Fase 4: Visualizaciones

| Script | Propósito | Input | Output |
| --- | --- | --- | --- |
| `04_bar_chart_race.py` | Genera animación HTML interactiva (Bar Chart Race, 45 días) | `sir_state_history.csv` | `bar_chart_race.html` |
| `04_bar_chart_race_180.py` | Versión extendida a 180 días con eje dinámico (barras crecen y se encogen) | `sir_state_history_180d.csv` | `bar_chart_race_180d.html` |
| `04b_stacked_sir_charts.py` | Gráficas apiladas S-I-R a nivel nacional y por estado (top 8). Incluye tabla cronológica. | `sir_full_state_history_180d.csv` | `charts/*.png`, `tabla_cronologia_infeccion.csv` |

### Fase 5: Machine Learning (XGBoost)

| Script | Propósito | Input | Output |
| --- | --- | --- | --- |
| `05_xgboost_risk.py` | Entrena XGBoost con 13 features de grafo (centralidades, PageRank, flujos) para predecir riesgo sistémico. Genera feature importance y comparación SIR vs XGB. | `nodos_estados.csv`, `matriz_gravedad.csv`, `distancias_carretera.csv`, `sir_full_state_history_180d.csv` | `xgboost_features.csv`, `sir_vs_xgboost_comparison.csv`, `charts/xgboost_*.png` |

**Features del XGBoost (13):**
```
1.  inventario_bovino       — Tamaño del hato estatal
2.  degree_centrality       — Centralidad de grado (NetworkX)
3.  betweenness_centrality  — Centralidad de intermediación
4.  closeness_centrality    — Centralidad de cercanía
5.  pagerank                — PageRank (importancia relativa en la red)
6.  weighted_in_flux        — Suma de flujos gravitatorios entrantes
7.  weighted_out_flux       — Suma de flujos gravitatorios salientes
8.  max_in_prob             — Máxima probabilidad de recibir contagio
9.  max_out_prob            — Máxima probabilidad de enviar contagio
10. avg_dist_carretera      — Distancia promedio por carretera a los demás
11. min_dist_carretera      — Distancia al vecino más cercano
12. lat                     — Latitud del centroide
13. lon                     — Longitud del centroide
```

---

## Fuentes de Datos

| Dataset | Fuente Oficial | URL / Método | Formato |
| --- | --- | --- | --- |
| Polígonos Estatales | INEGI Marco Geoestadístico | GitHub (angelnmara/geojson) basado en INEGI | GeoJSON, 198 KB |
| Inventario Bovino 2023 | SIAP / SADER | `nube.agricultura.gob.mx/poblacion_ganadera/` | CSV, 32 registros |
| Distancias por Carretera | OSRM (Open Source Routing Machine) | API pública `router.project-osrm.org/table/v1/driving/` | JSON → CSV |
| Red de Caminos (implícita) | OpenStreetMap via OSRM | Incluida en el routing de OSRM | Procesada por API |

---

## Resultados Clave

- **Hato Nacional:** 34,478,458 cabezas de ganado bovino
- **Pico de Infección:** Día 58, ~10.2 Millones de cabezas infectadas simultáneamente
- **Sacrificio Total (Día 179):** 33,421,804 cabezas (96.9% del hato nacional)
- **Estados Afectados:** 27 de 32 (sobreviven: BCS, BC, Quintana Roo, CDMX, Quintana Roo)
- **Top 5 Rutas de Mayor Riesgo:** Puebla↔Veracruz, Michoacán↔Jalisco, Chiapas↔Tabasco
- **XGBoost R² (Pico):** 0.843 — Feature #1: inventario_bovino, Feature #2: weighted_out_flux

---

## Análisis Crítico: Evolución del Modelo y Machine Learning

### 1. ¿Por qué el pico bajó de 17M a 10.2M de infectados?
En el **Modelo SIR Inicial (No Espacial)**, observamos un pico de ~17 millones de cabezas. En este nuevo **Modelo SIR Espacial sobre Grafo**, el pico se redujo a ~10.2 millones. ¿A qué se debe esta caída masiva?
* **Fricción Geográfica (El fin de la "Mezcla Homogénea"):** El primer modelo asumía que cualquier vaca en México podía contagiar instantáneamente a cualquier otra (mezcla perfecta). El modelo espacial introduce *fricción*. Para que el virus pase de Veracruz a Chihuahua, debe viajar a través de la red carretera, superando la distancia física y las probabilidades comerciales del modelo gravitatorio.
* **Picos Desfasados (Staggered Peaks):** Debido a esta fricción, el virus no explota en todo el país al mismo tiempo. Veracruz llega a su pico en las primeras semanas, pero Chihuahua no recibe la infección hasta el Día 44. Cuando los estados del norte apenas están empezando a ver casos, el centro y sur ya están en fase de sacrificio masivo (R). **La geografía "aplanó la curva" nacional.**

### 2. El rol del XGBoost: Predicción vs. Simulación
Es importante entender que **XGBoost no reemplaza al simulador SIR, ni genera series de tiempo** (por lo tanto, no se puede hacer un Bar Chart Race con él).
* **Simulador SIR:** Genera la evolución diaria y la dinámica temporal. Es computacionalmente costoso y altamente estocástico (depende del azar para los contagios entre estados).
* **XGBoost Regressor:** Actúa como un modelo de **Credit Scoring de Riesgo Epidémico**. En lugar de simular 180 días, toma la topología de la red (flujos carreteros, centralidad, inventario) y predice instantáneamente la devastación final (R² = 0.843). Su propósito es responder preguntas de negocio en milisegundos: *"Si construimos una nueva carretera entre el estado A y B, ¿cómo cambia el riesgo sistémico del país?"*

---

## Reproducibilidad

```bash
# Ejecutar todo el pipeline en orden:
cd src/spatial_model/
python3 01_data_prep.py
python3 01b_road_distances.py
python3 02_gravity_model.py
python3 03_spatial_sir.py
python3 03b_sir_full_history.py
python3 04_bar_chart_race.py
python3 04_bar_chart_race_180.py
python3 04b_stacked_sir_charts.py
python3 05_xgboost_risk.py
```

**Dependencias:**
```
geopandas, pandas, numpy, matplotlib, networkx, xgboost, scikit-learn, 
requests, Pillow, bar_chart_race
```
