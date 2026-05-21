# Tercer Avance: Modelado Espacial, Machine Learning y Arquitectura de Seguridad

> **Proyecto:** Ganado Saludable — Sistema Integral de Auditoría Epidemiológica Bovina
> **Universidad Nacional "Rosario Castellanos"** — Licenciatura en Ciencias de Datos para Negocios
> **Enfermedad asignada:** Fiebre Aftosa (FMD) | Proxy de calibración: Tuberculosis Bovina
> **Fecha:** Mayo 2026
> **Semestre:** 4° — 2026-1

---

## 1. Introducción

### 1.1 Resumen del Segundo Avance

En el Segundo Avance se completó la primera mitad del proyecto:

- Pipeline ELT multi-fuente operativo (~29,200 registros desde 6 fuentes).
- Análisis Exploratorio (EDA) con 8 hallazgos cuantificados.
- Modelo SIR Dual no-espacial (TB Bovina vs FMD): pico de ~17M infectados.
- Cuantificación económica: $52,800M USD de impacto en 150 días.
- Data Warehouse CSV→JSON con validación Pydantic.
- Arquitectura operativa conceptualizada (App + Dashboard NoSQL).

### 1.2 Qué se ha ejecutado en este Tercer Avance

Este avance marca la transición de un **modelo epidemiológico teórico** a un **sistema de inteligencia geoespacial predictiva**:

- **Modelo Gravitatorio sobre Grafo Dirigido:** Red de 32 nodos (estados) × 992 aristas (carreteras reales vía API OSRM).
- **Simulación SIR Espacial (180 días):** Propagación estocástica con fricción geográfica. El pico nacional se redujo de ~17M a **10.2M** de infectados simultáneos.
- **XGBoost Risk Scoring:** 13 variables topológicas (Node Embeddings) para predecir devastación estatal sin simulación (R² = 0.843).
- **Animación Custom Stacked Race Chart:** Motor de renderizado propio (matplotlib.animation) con barras apiladas bicolor (Infectados + Sacrificados).
- **Documentación técnica completa:** README del pipeline, análisis de features y decisiones arquitectónicas.

---

## 2. Del Modelo Ingenuo al Modelo Espacial: ¿Por Qué Importa la Geografía?

### 2.1 Limitación del Modelo SIR Base (Segundo Avance)

El primer modelo SIR asumía una **mezcla homogénea**: las 35.1 millones de cabezas de ganado convivían en un solo campo virtual. Esto produjo un pico catastrófico de ~17 millones de infectados simultáneos al día ~45, con una curva de contagio casi vertical.

**Problema epistemológico:** En la realidad, una vaca en Veracruz no puede contagiar instantáneamente a una vaca en Chihuahua. El virus viaja en camiones, por carreteras, entre estados que comercian ganado. La geografía impone **fricción**.

### 2.2 El Modelo Gravitatorio (Ley de Newton aplicada a Epidemiología)

Se implementó un modelo de gravedad newtoniana para cuantificar el flujo comercial (y por ende, el riesgo de contagio) entre cada par de estados:

```
F_ij = K × (P_i × P_j) / D_ij²

Donde:
  K     = 1×10⁻⁶ (constante de escala)
  P_i   = Inventario bovino del estado i (SIAP/SADER 2023)
  P_j   = Inventario bovino del estado j
  D_ij  = Distancia real por carretera asfáltica en km (API OSRM)
```

**Código:** `src/spatial_model/02_gravity_model.py`

**Decisiones de diseño críticas:**

1. **Distancia por carretera, no euclidiana.** Los camiones ganaderos no vuelan. La Sierra Madre impone una barrera real que la distancia en línea recta ignora. Se consultó la API pública de OSRM (Open Source Routing Machine) para obtener la matriz 32×32 de distancias reales.

2. **Centroides estatales como proxy.** Se usaron los centroides geográficos de cada estado (calculados en la proyección Lambert Conformal Cónica EPSG:6372) en lugar de ubicaciones individuales de ranchos. Esto se justifica por: (a) restricciones de privacidad de datos del SIAP, (b) eficiencia computacional (32 nodos vs. ~500,000 ranchos que requerirían O(N²) = 2.5×10¹¹ interacciones), y (c) que el centroide aproxima razonablemente el hub logístico de cada estado.

3. **Grafo dirigido ponderado.** La red resultante tiene 992 aristas (32×31) donde cada arista lleva un peso proporcional al flujo gravitatorio normalizado como probabilidad de contagio base [0, 1].

### 2.3 Resultados: Fricción Geográfica y "Picos Desfasados"

La simulación SIR sobre este grafo produce un fenómeno distinto al modelo ingenuo:

| Métrica | Modelo Base (2° Avance) | Modelo Espacial (3° Avance) | Diferencia |
|---------|------------------------|-----------------------------|------------|
| Pico Nacional de Infectados | ~17,000,000 | **10,200,000** | -40% |
| Día del Pico Nacional | ~45 | **58** | +13 días |
| Sacrificio Total (Día 179) | N/A (150 días) | **33,421,804** (96.9%) | — |
| Estados que sobreviven | 0 de 32 | **5 de 32** | — |
| Comportamiento | Explosión simultánea | **Efecto dominó** (ola desfasada) | — |

**¿Por qué bajó el pico?** La geografía desincronizó los brotes estatales. Cuando Veracruz ya está en fase de sacrificio masivo, Chihuahua apenas comienza a ver casos. Los "picos desfasados" (staggered peaks) hacen que el máximo nacional *simultáneo* sea menor, aunque el resultado final acumulado siga siendo catastrófico.

**Parámetros epidémicos utilizados:**

```
β (tasa contagio local)        = 0.6
γ (tasa sacrificio/remoción)   = 0.1 (periodo infeccioso ~10 días)
β_spatial (fuerza inter-estatal) = 0.8
Paciente Cero: Veracruz, 100 cabezas
Semilla aleatoria: 42 (reproducible)
```

**Código:** `src/spatial_model/03_spatial_sir.py`, `src/spatial_model/03b_sir_full_history.py`

![Simulación Espacial SIR — Propagación FMD 180 días](../../data/processed/spatial/fmd_spread_simulation_180d.gif)

*Figura 1. Mapa animado de la propagación de FMD sobre México (180 días). El color rojo indica estados con infección activa; el negro indica hato sacrificado.*

![Gráfica Apilada Nacional S-I-R](../../data/processed/spatial/charts/sir_nacional_apilado.png)

*Figura 2. Evolución nacional S-I-R (Susceptibles, Infectados, Removidos) durante 180 días. El pico de infectados ocurre en el Día 58 con ~10.2M cabezas.*

![Gráficas Apiladas Top 8 Estados](../../data/processed/spatial/charts/sir_top8_estados_apilado.png)

*Figura 3. Evolución S-I-R individual de los 8 estados más afectados. Se observan los "picos desfasados" (staggered peaks) que demuestran el efecto dominó geográfico.*

---

## 3. Cronología de la Infección: El Efecto Dominó Estado por Estado

La simulación SIR espacial permite trazar exactamente **cuándo** y **con qué severidad** cada estado se infecta:

| Estado | Día de Infección | Pico de Infectados | % Sacrificado al Día 60 | Clasificación |
|--------|------------------|--------------------|------------------------|---------------|
| Veracruz | 0 (Paciente Cero) | 2,646,298 | 96.79% | 🔴 Epicentro |
| Puebla | 25 | 428,422 | 68.56% | 🔴 Onda Primaria |
| Guanajuato | 26 | 457,385 | 64.63% | 🔴 Onda Primaria |
| México | 27 | 335,894 | 63.78% | 🔴 Onda Primaria |
| Chiapas | 27 | 1,503,947 | 47.59% | 🟠 Onda Secundaria |
| Michoacán | 28 | 1,151,854 | 45.87% | 🟠 Onda Secundaria |
| Tamaulipas | 28 | 697,685 | 52.00% | 🟠 Onda Secundaria |
| Jalisco | 34 | 1,783,195 | 9.86% | 🟡 Onda Tardía |
| Chihuahua | 44 | 1,283,594 | 0.29% | 🟡 Onda Tardía |
| Zacatecas | 51 | 577,097 | 0.04% | ⚪ Onda Final |
| Sinaloa | 56 | 949,511 | 0.00% | ⚪ Onda Final |
| Colima | 71 | 109,156 | 0.00% | ⚪ Onda Final |

**Observaciones clave:**

- **Jalisco** tiene el pico individual más alto (1.78M) pero se infecta tardíamente (Día 34). Esto se debe a que es un nodo masivo (alto inventario) pero está geográficamente al occidente, lejos del epicentro en Veracruz.
- **Chiapas** tiene el segundo pico más alto (1.5M) y se infecta temprano (Día 27), porque está conectado por la carretera costera del Golfo con Veracruz y Tabasco.
- Los **5 estados sobrevivientes** (Baja California, Baja California Sur, Quintana Roo, CDMX y uno más) se salvan por su aislamiento geográfico extremo o su inventario bovino insignificante.

---

## 4. Machine Learning: XGBoost Risk Scoring (Credit Scoring Epidémico)

### 4.1 Propósito

Mientras que el simulador SIR genera la "película" temporal de la infección (costoso, estocástico, toma segundos), el **XGBoost Regressor** actúa como un **tasador instantáneo de riesgo estructural**. Lee la topología del grafo carretero y predice en milisegundos qué tan devastado quedará cada estado.

**Analogía financiera:** El SIR es como correr un modelo de Monte Carlo de 10,000 escenarios para valuar una opción financiera. El XGBoost es como el Credit Score de FICO: te dice el riesgo sin simular toda la vida crediticia del sujeto.

**Código:** `src/spatial_model/05_xgboost_risk.py`

### 4.2 Las 13 Variables Topológicas (Node Embeddings)

Se extrajeron 13 features del grafo para cada estado usando NetworkX:

| # | Variable | Categoría | ¿Qué mide? |
|---|----------|-----------|-------------|
| 1 | `inventario_bovino` | Masa Biológica | Tamaño del hato estatal (SIAP 2023) |
| 2 | `degree_centrality` | Topología | ¿Con cuántos estados interactúa fuertemente? |
| 3 | `betweenness_centrality` | Topología | ¿Es un "puente" obligatorio en la red? |
| 4 | `closeness_centrality` | Topología | ¿Qué tan cerca está de todos los demás estados? |
| 5 | `pagerank` | Topología | Algoritmo de Google: importancia relativa en la red |
| 6 | `weighted_in_flux` | Flujo Gravitatorio | Suma total de atracción comercial entrante |
| 7 | `weighted_out_flux` | Flujo Gravitatorio | Suma total de riesgo exportado a otros |
| 8 | `max_in_prob` | Flujo Gravitatorio | La ruta singular más peligrosa de entrada |
| 9 | `max_out_prob` | Flujo Gravitatorio | La ruta singular más peligrosa de salida |
| 10 | `avg_dist_carretera` | Distancia | Promedio en km a todos los demás estados |
| 11 | `min_dist_carretera` | Distancia | Distancia al vecino más cercano |
| 12 | `lat` | Geográfica | Latitud del centroide |
| 13 | `lon` | Geográfica | Longitud del centroide |

### 4.3 Metodología de Entrenamiento

- **Técnica:** Leave-One-Out Cross-Validation (32 estados = 32 folds). Cada estado se predice habiendo entrenado con los otros 31.
- **Hiperparámetros:** `n_estimators=100`, `max_depth=4`, `learning_rate=0.1`, `subsample=0.8`.
- **Targets:** Se entrenaron dos modelos independientes:
  - **Target 1:** `dia_primera_infeccion` (¿cuándo llega el virus?)
  - **Target 2:** `pico_infectados` (¿cuántas cabezas se infectan en el peor momento?)

### 4.4 Resultados del XGBoost

| Target | R² (LOO-CV) | MAE | Interpretación |
|--------|-------------|-----|----------------|
| `pico_infectados` | **0.843** | ~200K cabezas | Excelente: la topología del grafo explica el 84.3% de la varianza en devastación |
| `dia_primera_infeccion` | ~0.0 | ~12 días | Pobre: el *momento* del contagio es estocástico (depende del azar de Monte Carlo) |

**Insight del Feature Importance:**

Las dos variables dominantes para predecir el pico de infectados son:

1. **`inventario_bovino`** — La "gasolina" para el fuego.
2. **`weighted_out_flux`** — La capacidad de exportar riesgo a otros estados.

**Conclusión epistémica:** Para que un estado sea un epicentro catastrófico, no basta con tener muchas vacas. Chiapas tiene más vacas que Michoacán pero está arrinconado geográficamente. **El peligro real reside en la combinación letal de alto inventario + alta centralidad de exportación.**

![Feature Importance XGBoost — Pico de Infectados](../../data/processed/spatial/charts/xgboost_importance_pico_infectados.png)

*Figura 4. Importancia de variables del XGBoost para predecir el pico de infectados. El inventario bovino y el flujo gravitatorio saliente dominan la predicción.*

![XGBoost vs SIR — Pico de Infectados](../../data/processed/spatial/charts/sir_vs_xgboost_pico_infectados.png)

*Figura 5. Validación cruzada: Predicción XGBoost (eje X) vs. Resultado real del SIR (eje Y). R² = 0.843. Los puntos cercanos a la diagonal indican alta precisión.*

### 4.5 Inmunización de Redes y Política Pública (Cerrar la Llave del Gas)

El modelo predictivo XGBoost y la simulación espacial demuestran que la contención epidemiológica tradicional es obsoleta. En lugar de una estrategia reactiva, proponemos un enfoque de **Inmunización de Redes (*Network Immunization*)** basado en la topología estructural del país.

#### A. La Analogía de la Válvula de Gas vs. el Extintor
*   **Estrategia tradicional (Apagar el fuego con extintor):** Esperar a que un estado reporte un brote para correr a establecer un cerco sanitario local. Esto es equivalente a intentar apagar el fuego con un extintor mientras la línea de suministro sigue abierta; la velocidad de dispersión inter-estatal supera cualquier capacidad de respuesta logística.
*   **Estrategia basada en Grafos (Cerrar la llave del gas):** Identificar y bloquear de forma proactiva los **hubs de intermediación y exportación de flujo**. Si se establecen puntos permanentes de inspección sanitaria y desinfección en las principales arterias de salida de los estados con mayor `weighted_out_flux` (Veracruz, Jalisco, Michoacán y Puebla), la red nacional se fragmenta en componentes aislados. El virus queda atrapado en su isla de origen, extinguiendo su capacidad de causar una pandemia nacional sin importar dónde haya iniciado el paciente cero.

#### B. Paradoja de la Masa Biológica frente a la Centralidad Estructural
*   **Masa Biológica (Inventario Bovino):** Representa la cantidad de "combustible" disponible localmente para alimentar el brote. Un estado como Chiapas tiene un inventario bovino masivo (~2.6M de cabezas), pero debido a su posición periférica en el extremo sur del país, tiene un bajo potencial de distribución sistémica.
*   **Flujo Gravitatorio Saliente (weighted_out_flux):** Mide la capacidad de inyectar riesgo comercial a las autopistas principales del país. Veracruz y Jalisco combinan alta masa biológica con una centralidad de exportación gigantesca. Bloquear o inmunizar estos nodos clave protege de forma indirecta a decenas de estados importadores netos que están a cientos de kilómetros de distancia.

---

### 4.6 Acordeón Conceptual de Inteligencia Artificial y Grafos

Para consolidar la defensa técnica del coloquio ante el sínodo y el docente Luis Gerardo Acuña, se presenta esta síntesis de la maquinaria lógica empleada:

#### 1. XGBoost Regressor (Aprendizaje Supervisado)
*   **¿Qué es?** Es un algoritmo de ensamble de árboles de decisión optimizado mediante *Gradient Boosting*. Construye árboles secuenciales donde cada nuevo árbol corrige los errores de predicción de los anteriores.
*   **¿Para qué sirve en el proyecto?** Actúa como un tasador de riesgo instantáneo (equivalente al *Credit Score* de FICO). En lugar de correr una simulación estocástica SIR de 180 días (que consume valiosos segundos de cómputo), el XGBoost lee las métricas topológicas de un estado y predice en milisegundos qué tan grande será su pico máximo de infectados.
*   **Validación Cruzada Leave-One-Out (LOO-CV):** Dado nuestro tamaño de muestra limitado (32 estados), la validación cruzada tradicional (como 5-fold) sufriría de alta varianza. LOO-CV entrena exactamente 32 modelos independientes; en cada iteración, el modelo se entrena con 31 estados y predice el riesgo del estado excluido. Esto asegura que la métrica de precisión R² = 0.843 sea robusta, honesta y no sufra de sobreajuste (*overfitting*).
*   **La paradoja de los Targets:**
    *   **Pico de Infectados (R² = 0.843):** Es un éxito rotundo porque la magnitud máxima de un brote es una propiedad puramente estructural del nodo (depende de su inventario y conectividad en carretera).
    *   **Día de Primera Infección (R² ~ 0.0):** El modelo no pudo predecirlo porque el momento exacto en que un camión infectado cruza una frontera es un evento puramente estocástico (azar de Monte Carlo), el cual no está determinado por la topología estática del grafo.

#### 2. Conceptos de Teoría de Grafos y Fricción Geoespacial
*   **Grafo Dirigido Ponderado:** Red de 32 nodos (estados) y 992 conexiones (aristas) donde las aristas tienen una dirección (el flujo comercial va de origen a destino) y un peso (`weighted_out_flux`) derivado de la atracción gravitatoria.
*   **Modelo de Gravedad de Huff/Stewart:** Adaptación de la ley de Newton a las ciencias sociales. El flujo comercial y de contagio entre el estado i y el estado j es proporcional a sus masas biológicas (inventarios bovinos) e inversamente proporcional al cuadrado de su distancia real por carretera asfáltica (calculada mediante la API OSRM).
*   **Centralidad de Intermediación (Betweenness Centrality):** Mide con qué frecuencia un nodo actúa como puente obligatorio en los caminos más cortos de la red. Bloquear un nodo con alto *Betweenness* divide físicamente el mapa nacional de carreteras.
*   **PageRank (Algoritmo de Google):** Mide la influencia recursiva de un nodo en la red. Un estado tiene un PageRank alto si está conectado a otros estados que a su vez son importadores o exportadores masivos de ganado.

![Feature Importance XGBoost — Día de Primera Infección](../../data/processed/spatial/charts/xgboost_importance_dia_primera_infeccion.png)

*Figura 6. Importancia de variables para predecir el día de primera infección. Este modelo tiene R² ~ 0 porque el momento del contagio es estocástico, no estructural.*

---

## 5. Visualizaciones e Impacto Económico Espacial

### 5.1 Animación Custom: Stacked Bar Chart Race

Se desarrolló un motor de renderizado custom (`04c_custom_stacked_race.py`) usando `matplotlib.animation.FuncAnimation` para superar la limitación de la librería `bar_chart_race`, que no soporta barras apiladas.

**Características técnicas:**

- 180 fotogramas a 3 FPS (~60 segundos de animación).
- Top 12 estados por ranking dinámico.
- Barras bicolor: **Rojo** = Infectados Activos, **Negro** = Sacrificados/Removidos.
- Dashboard superior con métricas nacionales en tiempo real (día, infectados, sacrificados).
- Exportación dual: MP4 (ffmpeg/x264) y GIF (Pillow).

**Archivos generados:**

- Video: `data/processed/spatial/charts/stacked_race_fmd.mp4`
- GIF: `data/processed/spatial/charts/stacked_race_fmd.gif`

### 5.2 Impacto Económico con el Modelo Espacial

**Código:** `src/models/fmd_finance_spatial.py`

Se realizó un fork de las proyecciones financieras del Segundo Avance, reemplazando el modelo SIR teórico (mezcla homogénea) por los datos reales del SIR Espacial Gravitatorio. El resultado confirma que, aunque la geografía aplaza el colapso (empujando la masacre del Mes 2 al Mes 3), **la pérdida acumulada a 150 días sigue siendo catastrófica: $52,796 Millones de USD.**

| Mes | Modelo Base (2° Avance) | Modelo Espacial (3° Avance) | Diferencia |
|-----|------------------------|----------------------------|-----------|
| Mes 1 | Explosión inmediata | Lento (fricción geográfica) | -85% sacrificados |
| Mes 2-3 | Pico y caída | **Pico retrasado al Mes 3** | +40% concentración |
| Total 5 meses | ~$52,800M USD | **~$52,796M USD** | Virtualmente igual |

![Flujo de Caja FMD — Modelo Espacial](../figures/flujo_caja_fmd_espacial.png)

*Figura 7. Flujo de caja mensual FMD con el Modelo Espacial Gravitatorio. La fricción geográfica redistribuye el colapso hacia los meses 3-4, pero la pérdida acumulada es idéntica.*

### 5.3 Inventario Completo de Artefactos Visuales

| # | Artefacto | Archivo | Tipo |
|---|-----------|---------|------|
| 1 | Mapa animado SIR (180 días) | `data/processed/spatial/fmd_spread_simulation_180d.gif` | GIF |
| 2 | Bar Chart Race (HTML interactivo) | `data/processed/spatial/bar_chart_race_180d.html` | HTML |
| 3 | **Stacked Race Chart (Custom bicolor)** | `data/processed/spatial/charts/stacked_race_fmd.mp4` | MP4 |
| 4 | Gráfica apilada nacional S-I-R | `data/processed/spatial/charts/sir_nacional_apilado.png` | PNG |
| 5 | Gráficas apiladas Top 8 estados | `data/processed/spatial/charts/sir_top8_estados_apilado.png` | PNG |
| 6 | Feature Importance (Pico) | `data/processed/spatial/charts/xgboost_importance_pico_infectados.png` | PNG |
| 7 | Feature Importance (Día) | `data/processed/spatial/charts/xgboost_importance_dia_primera_infeccion.png` | PNG |
| 8 | Scatter SIR vs XGBoost | `data/processed/spatial/charts/sir_vs_xgboost_pico_infectados.png` | PNG |
| 9 | Flujo de Caja Espacial | `docs/figures/flujo_caja_fmd_espacial.png` | PNG |
| 10 | Flujo de Caja Base (2° Avance) | `docs/figures/flujo_caja_fmd.png` | PNG |
| 11 | Contrafactual Detección FMD | `docs/figures/contrafactual_fmd.png` | PNG |

---

## 6. Pipeline Técnico Completo

### 6.1 Scripts del Pipeline (Orden de Ejecución)

```bash
cd src/spatial_model/
python3 01_data_prep.py          # Unión INEGI + SIAP → centroides
python3 01b_road_distances.py    # API OSRM → matriz de distancias
python3 02_gravity_model.py      # Modelo gravitatorio → 992 aristas
python3 03_spatial_sir.py        # Simulación SIR espacial → GIF + CSV
python3 03b_sir_full_history.py  # Re-simulación con S-I-R completo
python3 04_bar_chart_race.py     # Race chart HTML (45 días)
python3 04_bar_chart_race_180.py # Race chart HTML (180 días)
python3 04b_stacked_sir_charts.py # Gráficas apiladas (PNG)
python3 04c_custom_stacked_race.py # Animación custom bicolor (MP4+GIF)
python3 05_xgboost_risk.py       # XGBoost + Feature Importance
```

### 6.2 Fuentes de Datos

| Dataset | Fuente | Formato |
|---------|--------|---------|
| Polígonos Estatales | INEGI Marco Geoestadístico | GeoJSON |
| Inventario Bovino 2023 | SIAP / SADER | CSV, 32 registros |
| Distancias por Carretera | OSRM (Open Source Routing Machine) | API REST → CSV |
| Red de Caminos | OpenStreetMap vía OSRM | Implícita en routing |

### 6.3 Dependencias

```
geopandas, pandas, numpy, matplotlib, networkx, xgboost, scikit-learn,
requests, Pillow, bar_chart_race
```

---

## 7. Base de Datos NoSQL (MongoDB)

> 🟡 **Estado: En progreso.** Sección a cargo de [Compañero]. Esquema diseñado y aprobado; falta la implementación con datos reales.

### 7.1 Modelo Entidad-Relación (7 Colecciones)

```mermaid
erDiagram
    USUARIO ||--o{ REPORTE_SANITARIO : "Genera"
    USUARIO ||--o{ GRANJA : "Administra"
    GRANJA ||--o{ ANIMAL : "Alberga"
    GRANJA ||--o{ ZONA_CONTROL : "Pertenece a"
    ANIMAL ||--o{ MOVIMIENTO : "Registra"
    ANIMAL ||--o{ REPORTE_SANITARIO : "Sujeto de"
    MODELO_PREDICCION ||--o{ ZONA_CONTROL : "Calcula riesgo de"

    USUARIO {
        ObjectId _id PK
        string nombre_completo "Encriptado RSA"
        string rfc_curp "Encriptado RSA"
        string email "Encriptado RSA"
        string rol "Ganadero - Veterinario - CPA - Admin"
        string password_hash "bcrypt 12 rounds"
        date ultimo_acceso
    }

    GRANJA {
        ObjectId _id PK
        ObjectId owner_id FK
        string upp_id "Clave SINIIGA Unica"
        GeoJSON ubicacion "Point lat long"
        string estado "Jalisco - Veracruz - etc"
        int inventario_bovino "Cabezas actuales"
        int capacidad_maxima
        boolean cuarentena_activa
        float indice_riesgo "Score del modelo ML 0-1"
    }

    ANIMAL {
        ObjectId _id PK
        ObjectId granja_actual_id FK
        string siniiga_tag "Arete RFID"
        string especie "Bovino - Porcino - Caprino"
        string raza
        date fecha_nacimiento
        string estado_salud "Sano - Sospechoso - Infectado - Removido"
        date ultima_vacunacion
    }

    MOVIMIENTO {
        ObjectId _id PK
        ObjectId animal_id FK
        ObjectId granja_origen_id FK
        ObjectId granja_destino_id FK
        date fecha_transito
        string tipo "Comercial - Feria - Rastro TIF"
        string vehiculo_placas
        boolean guia_sanitaria_verificada
    }

    REPORTE_SANITARIO {
        ObjectId _id PK
        ObjectId animal_id FK
        ObjectId usuario_id FK
        ObjectId granja_id FK
        date fecha_reporte
        string sintomas "Lesiones vesiculares fiebre sialorrea"
        string diagnostico_presuntivo
        string metodo_diagnostico "Clinico - ELISA - RT-PCR"
        float probabilidad_riesgo "Score del modelo ML"
        string estatus "Pendiente - Confirmado - Descartado"
    }

    ZONA_CONTROL {
        ObjectId _id PK
        string estado
        GeoJSON perimetro "Polygon de 3km o 10km"
        string tipo "Foco - Perifocal - Vigilancia"
        float riesgo_gravitatorio "Indice calculado por el modelo"
        int granjas_afectadas
        date fecha_activacion
    }

    MODELO_PREDICCION {
        ObjectId _id PK
        date fecha_ejecucion
        string version_modelo "XGBoost v1.7 mas Gravity"
        object parametros "R0 gamma alpha beta"
        object resultados_por_estado "32 scores de riesgo"
        float accuracy "Precision del modelo"
    }
```

### 7.2 Ejemplo de Documento JSON (Reporte Sanitario)

```json
{
  "_id": "ObjectId('665a1b2c3d4e5f6a7b8c9d0e')",
  "granja_id": "ObjectId('665a1b2c3d4e5f6a7b8c9d0f')",
  "animal_id": "ObjectId('665a1b2c3d4e5f6a7b8c9d10')",
  "fecha_reporte": "2026-05-15T10:30:00Z",
  "sintomas": "Lesiones vesiculares en lengua y pezuñas, fiebre 40.5°C",
  "diagnostico_presuntivo": "Sospecha de FMD (Serotipo O)",
  "metodo_diagnostico": "ELISA NSP",
  "probabilidad_riesgo": 0.87,
  "estatus": "Pendiente confirmación RT-PCR"
}
```

### 7.3 Integración con el Motor Predictivo

El campo `indice_riesgo` (float 0.0–1.0) de las colecciones `GRANJA` y `ZONA_CONTROL` se alimenta directamente del output del XGBoost, basándose en las 13 variables topológicas del grafo. Esto permite a los veterinarios de la CPA priorizar inspecciones en estados con alto flujo gravitatorio saliente.

---

## 8. Criptografía y Seguridad

> 🟡 **Estado: En progreso.** Sección a cargo de [Compañero]. Esquema diseñado con los algoritmos vistos en clase.

### 8.1 Arquitectura de Seguridad (Basada en el temario del curso)

El sistema protege los datos sensibles de los ganaderos utilizando dos familias de algoritmos criptográficos:

| Capa | Algoritmo / Técnica | Propósito en la Aplicación |
|------|---------------------|---------------------------|
| **Passwords** | `bcrypt` (Función Hash con sal) | Las contraseñas nunca se almacenan en texto plano. Se aplica un Hash matemático irreversible para proteger contra hackeos de la base de datos. |
| **Datos Personales (PII)** | `RSA` (Cifrado Asimétrico) | Los nombres, correos y RFC de los ganaderos se encriptan con la Llave Pública al guardarlos en MongoDB. Solo la CPA tiene la Llave Privada para desencriptar. |
| **Tokens de Sesión** | `JWT` firmado con RSA | Al iniciar sesión, se entrega un token firmado criptográficamente para validar identidad sin retransmitir la contraseña. |

### 8.2 ¿Qué campos están encriptados?

| Tipo | Campos | Justificación |
|------|--------|---------------|
| 🔒 **Encriptados (RSA)** | `nombre_completo`, `rfc_curp`, `email`, `vehiculo_placas` | Datos personales identificables según la LFPDPPP |
| 🟢 **Texto Plano** | `estado_salud`, `ubicacion`, `inventario_bovino`, `indice_riesgo`, `fecha_reporte` | Necesarios para consultas geoespaciales y analíticas en tiempo real |

---

## 9. Estado de Avance por Materia

| Materia | Componente | Estado | Evidencia |
|---------|-----------|--------|-----------|
| **Ecuaciones Diferenciales** | Modelo SIR Dual + SIR Espacial Gravitatorio (180 días) | ✅ Completado | `src/spatial_model/03_spatial_sir.py` |
| **Bases de Datos NoSQL** | Esquema MongoDB 7 colecciones + Data Warehouse Pydantic | 🟡 Esquema aprobado, implementación pendiente | `docs/propuesta_app_db_cripto.md` |
| **Estadística Multivariada** | EDA + ANOVA + Correlación zoonótica | ✅ Completado | `notebooks/01-03` |
| **Inteligencia Artificial** | XGBoost Riesgo Topológico (13 Node Embeddings, R²=0.843) | ✅ Completado | `src/spatial_model/05_xgboost_risk.py` |
| **Criptografía** | Esquema Hash (bcrypt) + RSA para PII | 🟡 Diseño aprobado, código pendiente | `docs/propuesta_app_db_cripto.md` |
| **Finanzas Corporativas** | Impacto TB + FMD Base + FMD Espacial + Contrafactual | ✅ Completado | `src/models/fmd_finance_spatial.py` |
| **Innovación Social** | App Ganado Saludable + Dashboard + DINESA | ✅ Conceptualizado | Sección 7 del 2° Avance |

---

## 10. Próximos Pasos

| # | Tarea | Responsable | Estado |
|---|-------|-------------|--------|
| 1 | Implementar colecciones MongoDB con datos reales | Compañero | 🟡 Pendiente |
| 2 | Codificar esquema de encriptación Hash+RSA (demo funcional) | Compañero | 🟡 Pendiente |
| 3 | Generar documento DOCX final del Tercer Avance (JS) | Yo | 🟡 Esperando §7 y §8 |
| 4 | Preparar presentación oral (~15 diapositivas) con animaciones MP4 | Equipo | 🟡 Pendiente |

---

## 11. Bibliografía

- Anderson, I. (2002). *Foot and Mouth Disease 2001: Lessons to be Learned Inquiry Report.* The Stationery Office, London.
- Barlow, N.D. (1991). *A spatially aggregated disease/host model for bovine Tb in New Zealand possum populations.* Journal of Applied Ecology, 28(3), 777-793.
- Brauer, F., & Castillo-Chávez, C. (2012). *Mathematical Models in Population Biology and Epidemiology.* Springer.
- Kermack, W. O., & McKendrick, A. G. (1927). *A contribution to the mathematical theory of epidemics.* Proceedings of the Royal Society of London A, 115(772), 700-721.
- Knight-Jones, T.J.D. & Rushton, J. (2013). *The economic impacts of foot and mouth disease.* Preventive Veterinary Medicine, 112(3-4), 161-173.
- OIE. (2023). *Manual of Diagnostic Tests and Vaccines for Terrestrial Animals.* Chapter 3.1.8: Foot and Mouth Disease. WOAH.
- Rahman, M. A., & Samad, M. A. (2009). *Effect of bovine tuberculosis on milk production.* Bangladesh Journal of Veterinary Medicine, 7(2), 287-290.
- SIAP. (2024). *Panorama Agroalimentario 2024.* Servicio de Información Agroalimentaria y Pesquera, México.
- Tildesley, M. J. et al. (2006). *Optimal reactive vaccination strategies for a foot-and-mouth disease outbreak in the UK.* Nature, 440, 83-86.
- USDA ERS. (2024). *Mexico Livestock and Products Annual.* United States Department of Agriculture.
