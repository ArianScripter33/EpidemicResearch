# 📊 Trazabilidad de Datos, Linaje y Calibración de Figuras — AftoSec

Este documento detalla el **Data Lineage (Linaje de Datos)**, la procedencia oficial de las variables y la justificación metodológica de los parámetros para las 13 figuras generadas a lo largo de los tres avances del proyecto **AftoSec (Problema Prototípico: Ganado Saludable)**.

Este registro sirve de garantía de transparencia técnica y académica para el sínodo evaluador de la Universidad Nacional "Rosario Castellanos".

---

## 🌎 1. Catálogo Oficial de Fuentes de Datos (Data Catalog)

Para evitar la improvisación de variables o la invención de escenarios en una enfermedad exótica ausente en México desde 1954 (Fiebre Aftosa / FMD), el sistema fue calibrado con datos institucionales reales de las siguientes dependencias de gobierno y organismos internacionales:

1.  **Secretaría de Agricultura y Desarrollo Rural (SADER) / Servicio de Información Agroalimentaria y Pesquera (SIAP):**
    *   *Dataset:* **Cierre de la Producción Pecuaria 2023 (Inventario de Población Ganadera Bovinos)**.
    *   *Uso:* Determina la población inicial susceptible por nodo ($P_i$, $P_j$) desagregada a nivel de las 32 entidades federativas.
2.  **Instituto Nacional de Estadística y Geografía (INEGI):**
    *   *Dataset:* **Marco Geoestadístico Nacional 2023** (Polígonos vectoriales en formato GeoJSON para los 32 estados de la República).
    *   *Uso:* Renderización cartográfica y cálculo georreferenciado de centroides de población ganadera.
3.  **Open Source Routing Machine (OSRM) / OpenStreetMap (OSM):**
    *   *Dataset:* **Red Vial Digital Púbica de México**.
    *   *Uso:* Ruteador terrestre que calcula la distancia de conducción terrestre real en carretera asfáltica entre los centroides de cada par de estados ($d_{ij}$ real) mediante consultas a la API de OSRM, superando la limitación de la distancia euclidiana (línea recta) del modelo gravitatorio clásico.
4.  **Organización Mundial de Sanidad Animal (OMSA / WOAH):**
    *   *Dataset:* Sistema Mundial de Información Zoosanitaria (**WAHIS**), bases de datos globales de brotes de Fiebre Aftosa (Serotipo O).
    *   *Uso:* Calibración biológica de los parámetros del virus (Tasa de ataque $\beta = 0.6$, Tasa de remoción por rifle sanitario $\gamma = 0.1$, lo que modela un periodo infeccioso promedio de 10-14 días).
5.  **Sistema Nacional de Información e Integración de Mercados (SNIIM) / SADER:**
    *   *Dataset:* Cotizaciones promedio de bovinos en pie para abasto nacional (2024).
    *   *Uso:* Costo promedio por cabeza fijado en **$1,544 USD** ($26,250 MXN) para modelar la pérdida de capital biológico por rifle sanitario.
6.  **Secretaría de Salud / Dirección General de Epidemiología (DGE):**
    *   *Dataset:* Boletines Epidemiológicos Anuales de Morbilidad por Zoonosis (2018-2024).
    *   *Uso:* Calibración de la regresión lineal inicial y ANOVA de Tuberculosis Bovina (TB) como proxy epidemiológico nacional en los Avances 1 y 2.

---

## 📊 2. Inventario Riguroso y Pies de Imagen Formulares

### 🎬 Figura 1: Mapa Animado de la Propagación de FMD sobre México (180 días)
*   **Archivo en Repositorio:** `data/processed/spatial/fmd_spread_simulation_180d.gif` (GIF)
*   **Script Generador:** `src/spatial_model/03_spatial_sir.py`
*   **Pie de Imagen Riguroso:** 
    > *Figura 1. Simulación espacial estocástica de la propagación de Fiebre Aftosa (FMD, Serotipo O) en el rebaño bovino mexicano sobre un horizonte de 180 días, utilizando un modelo de acoplamiento gravitatorio sobre la red vial federal de transporte pecuario. El sombreado rojo representa la prevalencia de hato en fase de infección activa y el gris representa las zonas susceptibles. Elaboración propia a partir de datos del Marco Geoestadístico del INEGI (2023), los inventarios estatales de ganado del SIAP (2023), y matrices de ruteo por carretera asfáltica obtenidas vía la API de OSRM.*

### 📊 Figura 2: Bar Chart Race Interactivo (180 días)
*   **Archivo en Repositorio:** `data/processed/spatial/bar_chart_race_180d.html` (HTML interactivo)
*   **Script Generador:** `src/spatial_model/04_bar_chart_race_180.py`
*   **Pie de Imagen Riguroso:**
    > *Figura 2. Evolución cronológica interactiva del volumen acumulado de cabezas bovinas infectadas activas (Bar Chart Race) en los 12 estados más vulnerables de la República Mexicana. Elaboración propia con base en el motor de simulación geoespacial AftoSec, calibrado con los censos agropecuarios del SIAP (2023) y modelado mediante fricción de transporte vial por carreteras federales de la API de OSRM.*

### 🎥 Figura 3: Stacked Bar Chart Race Animado Bicolor (FMD Epidemic Evolution)
*   **Archivo en Repositorio:** `data/processed/spatial/charts/stacked_race_fmd.gif` y `stacked_race_fmd.mp4` (GIF/MP4)
*   **Script Generador:** `src/spatial_model/04c_custom_stacked_race.py`
*   **Pie de Imagen Riguroso:**
    > *Figura 3. Simulación animada bicolor de la carrera de barras apiladas (Stacked Bar Chart Race) mostrando la destrucción del hato ganadero en las 12 entidades más afectadas. El color rojo representa las cabezas de ganado con infección activa y el color negro representa la biomasa pecuaria sacrificada ("Removida") bajo el protocolo internacional del rifle sanitario. Elaboración propia basada en integraciones numéricas del modelo estocástico de grafos acoplados AftoSec, empleando datos censales del SIAP (2023) y matrices de ruteo vial de OSRM.*

### 📈 Figura 4: Gráfica Apilada Nacional S-I-R
*   **Archivo en Repositorio:** `data/processed/spatial/charts/sir_nacional_apilado.png` (PNG)
*   **Script Generador:** `src/spatial_model/04b_stacked_sir_charts.py`
*   **Pie de Imagen Riguroso:**
    > *Figura 4. Evolución de la dinámica epidemiológica compartimental S-I-R (Susceptibles, Infectados Activos, Removidos/Sacrificados) a nivel nacional durante una ventana epidémica de 180 días. El modelo geoespacial revela que el pico nacional de contagios simultáneos se reduce a 10.2 millones de cabezas en el Día 58 debido a la fricción de distancia en la red vial. Elaboración propia con base en el motor de simulación espacial AftoSec y datos del inventario pecuario nacional del SIAP (2023).*

### 📈 Figura 5: Gráficas Apiladas Top 8 Estados Más Afectados
*   **Archivo en Repositorio:** `data/processed/spatial/charts/sir_top8_estados_apilado.png` (PNG)
*   **Script Generador:** `src/spatial_model/04b_stacked_sir_charts.py`
*   **Pie de Imagen Riguroso:**
    > *Figura 5. Dinámicas compartimentales S-I-R individuales para las ocho entidades con mayor devastación pecuaria acumulada en México. Se demuestran visualmente los "picos desfasados" (staggered peaks), lo que representa la fricción geográfica terrestre que impide un brote explosivo simultáneo. Elaboración propia a partir del historial del modelo de dispersión espacial AftoSec con datos iniciales del SIAP (2023) y distancias de transporte terrestre de OSRM.*

### 📊 Figura 6: Feature Importance XGBoost (Pico de Infectados)
*   **Archivo en Repositorio:** `data/processed/spatial/charts/xgboost_importance_pico_infectados.png` (PNG)
*   **Script Generador:** `src/spatial_model/05_xgboost_risk.py`
*   **Pie de Imagen Riguroso:**
    > *Figura 6. Importancia relativa de las variables topológicas y biológicas del grafo nacional de transporte pecuario para predecir la magnitud del pico de infectados por estado (métrica de ganancia - Gain de XGBoost). Elaboración propia aplicando el algoritmo de aprendizaje supervisado XGBoost Regressor en validación cruzada Leave-One-Out (LOOCV), utilizando métricas estructurales de red de NetworkX y censos de ganado del SIAP (2023).*

### 📊 Figura 7: Feature Importance XGBoost (Día de Primera Infección)
*   **Archivo en Repositorio:** `data/processed/spatial/charts/xgboost_importance_dia_primera_infeccion.png` (PNG)
*   **Script Generador:** `src/spatial_model/05_xgboost_risk.py`
*   **Pie de Imagen Riguroso:**
    > *Figura 7. Importancia relativa de variables topológicas para predecir el día de arribo del primer brote viral a cada entidad federal. La nula predictibilidad del modelo (R² ~ 0) demuestra estadísticamente que el chispazo de contagio inicial es un evento puramente estocástico de Monte Carlo vial, no determinado por la estructura estática del grafo. Elaboración propia basada en modelos de regresión XGBoost y simulaciones estocásticas.*

### 📉 Figura 8: Scatter Plot de Validación Cruzada LOOCV (XGBoost vs. SIR real)
*   **Archivo en Repositorio:** `data/processed/spatial/charts/sir_vs_xgboost_pico_infectados.png` (PNG)
*   **Script Generador:** `src/spatial_model/05_xgboost_risk.py`
*   **Pie de Imagen Riguroso:**
    > *Figura 8. Validación cruzada Leave-One-Out (LOOCV) del modelo XGBoost Regressor para la predicción de la biomasa bovina infectada en el pico de la epidemia por estado. La alta correlación (R² = 0.843, MAE = ~200k cabezas) valida la viabilidad del aprendizaje automático como un Credit Score de riesgo estructural instantáneo sin necesidad de cómputos estocásticos dinámicos. Elaboración propia a partir de datos estructurales y simulaciones.*

### 💸 Figura 9: Flujo de Caja Mensual FMD (Modelo SIR Espacial)
*   **Archivo en Repositorio:** `docs/figures/flujo_caja_fmd_espacial.png` (PNG)
*   **Script Generador:** `src/models/fmd_finance_spatial.py`
*   **Pie de Imagen Riguroso:**
    > *Figura 9. Proyección del flujo de caja negativo mensual y pérdidas acumuladas del sector pecuario nacional por Fiebre Aftosa (FMD) bajo el modelo geoespacial AftoSec. Integra las pérdidas de biomasa por sacrificio sanitario ($1,544 USD/cabeza) y las pérdidas por bloqueo comercial de exportación de la OMSA ($8.2 millones de USD diarios de pérdida constante). Elaboración propia con base en el historial de simulación espacial SIR y parámetros financieros del SNIIM (2024) y el SIAP.*

### 💸 Figura 10: Flujo de Caja Mensual FMD (Modelo SIR Base Homogéneo - 2° Avance)
*   **Archivo en Repositorio:** `docs/figures/flujo_caja_fmd.png` (PNG)
*   **Script Generador:** `src/models/finance_addendum.py`
*   **Pie de Imagen Riguroso:**
    > *Figura 10. Proyección del colapso financiero mensual acumulado por Fiebre Aftosa (FMD) bajo la premisa de una mezcla homogénea clásica del hato (sin fricción espacial ni geografía vial), mostrando la ruina sectorial inmediata. Elaboración propia basada en la integración de ecuaciones diferenciales ordinarias SIR y cotizaciones comerciales del SIAP y el SNIIM.*

### 📈 Figura 11: Gráfica de Análisis Contrafactual de Alerta Temprana (Inacción vs. AftoSec)
*   **Archivo en Repositorio:** `docs/figures/contrafactual_fmd.png` (PNG)
*   **Script Generador:** `src/models/finance_addendum.py` (2° Avance)
*   **Pie de Imagen Riguroso:**
    > *Figura 11. Análisis contrafactual y retorno de inversión (ROI) social de la implementación del sistema digital preventivo de trazabilidad de precisión AftoSec, confrontando el costo por inacción epidemiológica frente al cerco sanitario georreferenciado e inmediato en fases tempranas. Elaboración propia basada en análisis de sensibilidad y modelos financieros preventivos.*

### 📈 Figura 12: Comparativa Diaria de Curvas Epidémicas (Clásico Homogéneo vs. Espacial Gravitatorio)
*   **Archivo en Repositorio:** `docs/figures/fmd_comparativa_diaria.png` (PNG)
*   **Script Generador:** `src/models/fmd_finance_comparison.py`
*   **Pie de Imagen Riguroso:**
    > *Figura 12. Comparativa diaria de la curva de infectados activos (Mezcla Homogénea vs. Espacial Gravitatorio). La fricción espacial carretera en el modelo acoplado reduce el pico máximo un ~41.7% (de 17.5M a 10.2M) y retrasa el día del pico al Día 58 (frente al Día 45 del modelo clásico), generando una ventana de control crítico de 13 días. El efecto ocurre a pesar de una semilla inicial 100 veces mayor ($I_0 = 100$ en Veracruz vs. $I_0 = 1$). Elaboración propia a partir de simulaciones en Python e integraciones de flujos de acoplamiento espacial por carretera.*

### 📈 Figura 13: Comparativa Mensual de Pérdidas Financieras Acumuladas (USD)
*   **Archivo en Repositorio:** `docs/figures/fmd_comparativa_mensual.png` (PNG)
*   **Script Generador:** `src/models/fmd_finance_comparison.py`
*   **Pie de Imagen Riguroso:**
    > *Figura 13. Comparativa del impacto financiero mensual acumulado (en billones de USD) por el brote de Fiebre Aftosa. Se observa que la fricción geográfica terrestre aplaza las pérdidas catastróficas en los meses 1 y 2, pero al mes 5 ambos modelos convergen inevitablemente en un colapso financiero idéntico de $52,796 millones de USD. Elaboración propia con base en modelos financieros y comerciales de exportación pecuaria nacional del SIAP y el SNIIM (2024).*

---

## 🏆 3. Selección Crítica de las 4 Figuras para el Artículo de Divulgación Final

Para evitar la saturación cognitiva del lector no técnico, se ha definido que el borrador final del **Artículo de Divulgación Científica** integrará únicamente las siguientes **4 figuras definitivas** en sus respectivas secciones:

1.  **Figura 1 (Propagación Espacial SIR):** Plasmada en la **§3 (La Simulación)** como una secuencia estática de 3 paneles temporales (Día 15, Día 45, Día 90). Es la representación geográfica visual de la dispersión de la Fiebre Aftosa en el territorio mexicano.
2.  **Figura 12 (Comparación de Curvas Diarias):** Plasmada en la **§6 (Innovación y Finanzas)**. Demuestra la evidencia empírica-matemática del aplanamiento de curva por fricción geográfica terrestre.
3.  **Figura 13 (Comparación de Flujo Mensual):** Plasmada en la **§6 (Innovación y Finanzas)**. Valúa financieramente el impacto y evidencia la ventana de contención económica y el retorno de inversión del sistema AftoSec.
4.  **Figura 8 (Validación Cruzada LOOCV de XGBoost):** Plasmada en la **§4 (Inteligencia Artificial)**. Es la validación matemática de MLOps que demuestra la capacidad predictiva instantánea de nuestro XGBoost Regressor en milisegundos con solo 13 métricas de grafos.
