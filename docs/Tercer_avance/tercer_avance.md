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

### 4.5 Implicaciones para Política Pública: ¿Dónde Intervenir?

El XGBoost revela que la intervención óptima **no depende de dónde inicie la infección**, sino de la **estructura del grafo**:

- **Estrategia tradicional (Reactiva):** Esperar al brote → cerco sanitario → perseguir el fuego.
- **Estrategia basada en grafos (Proactiva):** Instalar puntos de inspección sanitaria permanentes en las carreteras de mayor `weighted_out_flux` que salen de Jalisco, Veracruz y Estado de México. Al asfixiar estos "súper-nodos distribuidores", se fragmenta la red nacional en islas seguras, sin importar dónde haya iniciado el brote.

---

## 5. Visualizaciones Generadas

### 5.1 Inventario de Artefactos Visuales

| Artefacto | Archivo | Descripción |
|-----------|---------|-------------|
| Mapa Animado SIR (180 días) | `fmd_spread_simulation_180d.gif` | Propagación geográfica sobre mapa de México |
| Bar Chart Race (HTML) | `bar_chart_race_180d.html` | Competencia animada de infectados por estado |
| **Stacked Race Chart (Custom)** | `stacked_race_fmd.mp4` / `.gif` | Barras bicolor (Infectados rojo + Sacrificados negro) con ranking dinámico |
| Gráfica Apilada Nacional | `sir_nacional_apilado.png` | Área chart S-I-R completo del hato nacional |
| Gráficas Apiladas Top 8 | `sir_top8_estados_apilado.png` | S-I-R individual de los 8 estados más afectados |
| Feature Importance XGBoost | `xgboost_importance_pico_infectados.png` | Variables más predictivas del pico de infección |
| SIR vs XGBoost Scatter | `sir_vs_xgboost_pico_infectados.png` | Validación cruzada: predicción vs realidad |

### 5.2 Animación Custom: Stacked Bar Chart Race

Se desarrolló un motor de renderizado custom (`04c_custom_stacked_race.py`) usando `matplotlib.animation.FuncAnimation` para superar la limitación de la librería `bar_chart_race`, que no soporta barras apiladas.

**Características técnicas:**
- 180 fotogramas a 10 FPS (18 segundos de animación).
- Top 12 estados por ranking dinámico.
- Barras bicolor: **Rojo** = Infectados Activos, **Negro** = Sacrificados/Removidos.
- Dashboard superior con métricas nacionales en tiempo real (día, infectados, sacrificados).
- Exportación dual: MP4 (ffmpeg/x264) y GIF (Pillow).

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

> 🟡 **Estado: En progreso.** Sección a cargo de [Compañero]. Se espera la implementación de las colecciones `GRANJA`, `ANIMAL`, `MOVIMIENTO`, `REPORTE_SANITARIO` y `ZONA_CONTROL` conforme al esquema definido en `docs/propuesta_app_db_cripto.md`.

### 7.1 Esquema Aprobado

El modelo Entidad-Relación define 7 colecciones principales:

- **USUARIO:** Ganaderos, veterinarios y administradores (PII encriptada con FLE).
- **GRANJA:** Unidades de producción con ubicación GeoJSON y score de riesgo ML.
- **ANIMAL:** Trazabilidad individual con arete SINIIGA y estado de salud S-I-R.
- **MOVIMIENTO:** Registro de tránsito comercial entre granjas (vector de contagio).
- **REPORTE_SANITARIO:** Denuncias con probabilidad de riesgo del modelo ML.
- **ZONA_CONTROL:** Perímetros de cuarentena (Foco, Perifocal, Vigilancia).
- **MODELO_PREDICCION:** Registro de ejecuciones del XGBoost con parámetros y scores.

### 7.2 Integración con el Motor Predictivo

El campo `indice_riesgo` (float 0.0–1.0) de las colecciones `GRANJA` y `ZONA_CONTROL` se alimenta directamente del output del XGBoost, basándose en las 13 variables topológicas del grafo.

---

## 8. Criptografía y Seguridad

> 🟡 **Estado: En progreso.** Sección a cargo de [Compañero]. Se espera la implementación del esquema de seguridad de tres capas conforme a `docs/propuesta_app_db_cripto.md`.

### 8.1 Arquitectura de Seguridad Aprobada (Tres Capas)

| Capa | Estándar | Algoritmo |
|------|----------|-----------|
| En Tránsito | TLS 1.3 | ECDHE_RSA_WITH_AES_256_GCM_SHA384 |
| En Reposo | AES-256 | AES-256-CBC (MongoDB WiredTiger) |
| A Nivel de Campo (FLE) | AEAD | AES-256-CBC + HMAC-SHA-512 |
| Passwords | bcrypt | 12 rounds de sal |
| Tokens de Sesión | JWT | RS256 (RSA 2048-bit) |

### 8.2 Campos Protegidos (Criterio LFPDPPP)

- **Encriptados (FLE):** `nombre_completo`, `rfc_curp`, `email`, `vehiculo_placas`.
- **Texto Plano:** `estado_salud`, `ubicacion`, `inventario_bovino`, `indice_riesgo`, `fecha_reporte` (requeridos para consultas geoespaciales y analíticas en tiempo real).

---

## 9. Estado de Avance por Materia

| Materia | Componente | Estado | Evidencia |
|---------|-----------|--------|-----------|
| **Ecuaciones Diferenciales** | Modelo SIR Dual + SIR Espacial Gravitatorio | ✅ Completado | `src/spatial_model/` |
| **Bases de Datos NoSQL** | Esquema MongoDB + Data Warehouse Pydantic | 🟡 Esquema aprobado, implementación pendiente | `docs/propuesta_app_db_cripto.md` |
| **Estadística Multivariada** | EDA + ANOVA + Correlación zoonótica | ✅ Completado | `notebooks/01-03` |
| **Inteligencia Artificial** | XGBoost Riesgo Topológico (13 Node Embeddings) | ✅ Completado (R²=0.843) | `src/spatial_model/05_xgboost_risk.py` |
| **Criptografía** | Esquema FLE + TLS 1.3 + bcrypt | 🟡 Diseño aprobado, código pendiente | `docs/propuesta_app_db_cripto.md` |
| **Finanzas Corporativas** | Modelos de impacto TB + FMD + Contrafactual | ✅ Completado | `src/models/fmd_finance_addendum.py` |
| **Innovación Social** | App Ganado Saludable + Dashboard + DINESA | ✅ Conceptualizado | Sección 7 del 2° Avance |

---

## 10. Próximos Pasos

| # | Tarea | Responsable | Estado |
|---|-------|-------------|--------|
| 1 | Implementar colecciones MongoDB con datos reales | Compañero | 🟡 Pendiente |
| 2 | Codificar esquema de encriptación FLE (demo funcional) | Compañero | 🟡 Pendiente |
| 3 | Generar documento DOCX final del Tercer Avance | Yo | 🟡 Esperando §7 y §8 |
| 4 | Preparar presentación oral con animaciones MP4 | Equipo | 🟡 Pendiente |
| 5 | Análisis de sensibilidad: "Blindaje" de súper-nodos | Yo (opcional) | ⚪ Futuro |

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
