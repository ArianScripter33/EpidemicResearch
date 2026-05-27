# 👥 Estructura de Contribuciones y Roles de Desarrollo — Proyecto AftoSec

Este documento detalla los roles de desarrollo, la autoría del código y las contribuciones individuales de cada miembro del equipo para el Problema Prototípico de 4° Semestre. 

El objetivo es garantizar la transparencia y la trazabilidad de la autoría ante los evaluadores académicos.

---

## 🛠️ Matriz de Contribuciones y Roles Técnicos

### 1. Arian Pedroza Celis (`ArianScripter33`)
*   **Rol Principal:** Arquitecto de Datos y Modelación Matemática.
*   **Contribuciones Técnicas (Código y Análisis):**
    *   **Modelo SIR Espacial Gravitatorio:** Integración de la API OSRM para distancias carreteras de los 32 estados y simulación epidemiológica estocástica (`src/spatial_model/01_data_prep.py`, `02_gravity_model.py`, `03_spatial_sir.py`).
    *   **Machine Learning:** Entrenamiento del modelo predictivo de riesgo mediante **XGBoost Regressor** con validación LOOCV y análisis de importancia de características topológicas en grafos (`src/spatial_model/05_xgboost_risk.py`).
    *   **Visualización Científica:** Animación en video/GIF del Bar Chart Race de la propagación del virus y gráficas dinámicas nacionales (`src/spatial_model/04_bar_chart_race.py`, `04b_stacked_sir_charts.py`).
*   **Documentación Principal:**
    *   `docs/Tercer_avance/tercer_avance.md` (Secciones 1, 2, 3, 4, 5.1, 5.2, 6, 7).

### 2. Victoria Montserrat Enriquez (`monenri9-svg`)
*   **Rol Principal:** Analista de Cálculo Multivariable y Proyección Financiera.
*   **Contribuciones Técnicas (Código y Análisis):**
    *   **Modelación Financiera Multivariable:** Diseño e implementación de las funciones de flujo de caja y simulación de pérdidas monetarias comparativas entre el modelo clásico y el espacial (`src/models/fmd_finance_comparison.py`, `src/models/fmd_finance_spatial.py`).
    *   **Visualización Comparativa:** Generación de gráficas de la curva diaria de infectados activos y costos mensuales acumulados analizando el aplanamiento de curvas por fricción geográfica (`docs/figures/fmd_comparativa_diaria.png`, `docs/figures/fmd_comparativa_mensual.png`).
*   **Documentación Principal:**
    *   `docs/Segundo_avance/fmd_finance_data_spatial.json` (Parámetros y amortizaciones mensuales).
    *   `docs/Tercer_avance/tercer_avance.md` (Sección 5.3 - Comparativa Homogénea vs Espacial).
    *   `docs/Tercer_avance/Propuesta_innovacionSocial/Actividad_Innovacion_Social_Ganado_Saludable.md` (Línea narrativa y ODS).

### 3. Axel (`Miembro 1 - Crypto/NoSQL`)
*   **Rol Principal:** Ingeniero de Ciberseguridad y Modelado NoSQL.
*   **Contribuciones Técnicas (Código y Análisis):**
    *   **Criptografía Móvil (FLE):** Diseño e implementación del cifrado de datos personales a nivel de campo (Field-Level Encryption) utilizando el cifrado de flujo **ChaCha20-Poly1305** en dispositivos clientes (`src/crypto/mock_mobile_app.py`).
    *   **Modelado NoSQL:** Diseño y simulación del esquema de colecciones flexibles de MongoDB que aíslan la identidad del ganadero pero permiten la consulta de variables epidemiológicas en texto plano (`data/nosql/registroGanado.json`, `ejemplo_reporte_cifrado.json`).
*   **Documentación Principal:**
    *   `docs/explicacion_matematica_chacha20.md` (Fundamentos de álgebra modular, Quarter-Round y estructura ARX de ChaCha20).
    *   `docs/Tercer_avance/tercer_avance.md` (Sección 8.3 - Simulador de App Móvil).

---

## 🔍 Trazabilidad en el Historial de Git
Para auditar la veracidad del historial de commits sin mezclar ni sobrescribir el trabajo, el desarrollo se segmentó de la siguiente forma:

1.  **Integración limpia en `main`:** Cada miembro desarrolló en sus respectivas ramas de features (`feature/miembro1-crypto-nosql` y `feature/analisis-morbilidad`).
2.  **Autoría explícita:** Los desarrollos fueron incorporados al tronco principal a través de commits con firmas cruzadas (`Co-authored-by`), asegurando que la autoría de Axel y Victoria aparezca registrada de manera indeleble en el log oficial de GitHub.
