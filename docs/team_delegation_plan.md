# Plan de Delegación y Análisis Exploratorio (EDA)

## 1. Fase de Análisis Exploratorio Global (EDA)
**Responsables:** Arian & Antigravity (Core Team)
**Objetivo:** Consolidar, limpiar y descubrir *insights* en todos los datasets recuperados antes de pasarlos al equipo.

**Acciones a realizar en Jupyter Notebook (`01_eda_global.ipynb`):**
1. **DGE Morbilidad:** Graficar la serie de tiempo 2015-2024 para Tuberculosis (A15-A19) vs Intoxicaciones (A05) a nivel nacional.
2. **SENASICA:** Analizar la distribución de hatos libres vs cuarentenados. Evaluar cuánta biomasa está bajo riesgo en los 13 estados afectados.
3. **openFMD:** Filtrar brotes de Fiebre Aftosa (2000-2025) por continente. Identificar serotipos más comunes (O, A, SAT2) para justificar los parámetros de nuestro modelo SIR.
4. **COFEPRIS:** Mapear las 33 sanciones de laboratorios para establecer nuestro "proxy basal normativo" (la frecuencia con la que el gobierno inspecciona).

---

## 2. Alineación con Incidentes Críticos (Syllabus)
Las tareas delegadas deben cumplir con los requisitos académicos sin requerir conocimientos avanzados de modelado matemático o Machine Learning.

*   **Incidente Crítico 1 (Matemáticas Discretas / Criptografía):** Implementación de cifrado para proteger datos de granjas.
*   **Incidente Crítico 2 (Estadística Multivariada):** Análisis de varianza (ANOVA) y pruebas de hipótesis.
*   **Incidente Crítico 3 (Bases de Datos NoSQL):** Ingesta de JSONs a MongoDB.

---

## 3. Asignación de Tareas Específicas (Nivel: Analista Junior)

Estas tareas están diseñadas para ser **muy medibles, delimitadas y útiles**. Les dará el sentimiento de contribución real mientras nosotros construimos la arquitectura pesada.

### 👨‍💻 Miembro 1 del Equipo: Transformación a NoSQL y Criptografía Básica
**Perfil necesario:** Python básico, conocimientos de diccionarios, JSON.
**Tarea A:** Convertir el dataset `senasica_cuarentenas_clean.csv` en una estructura JSON anidada (por estado y trimestre) para simular la ingesta a MongoDB.
**Tarea B:** Programar una función en Python (Cifrado César o similar simple) que encripte la columna de `establecimiento` del dataset de COFEPRIS para "proteger datos sensibles" (Cumple con requisito de Matemáticas Discretas).
**Entregable:** Un script `crypto_mongo_prep.py` que genere los JSONs cifrados.

### 👨‍💻 Miembro 2 del Equipo: Estadística Descriptiva y Visualización (Plotly/Seaborn)
**Perfil necesario:** Manejo de Pandas básico, Matplotlib/Plotly.
**Tarea A:** Agrupar el dataset `openfmd_clean.csv` por continente (`un_region`) y año, y generar un gráfico de barras apiladas de los 10 países con más brotes de Fiebre Aftosa en los últimos 20 años.
**Tarea B:** Calcular la media, mediana y desviación estándar de los casos de morbilidad de Tuberculosis de nuestro dataset DGE 2015-2017 por estado, y preparar una tabla resumen.
**Entregable:** Un jupyter notebook `02_analisis_descriptivo.ipynb` con las 2 gráficas y la tabla resumen.

---

## 4. Flujo de Revisión (Code Review)
1. **Asignación:** Se les entrega a cada uno sus respectivos CSVs limpios y un archivo `.prompt` o `.md` con instrucciones paso a paso.
2. **Ejecución:** Ellos desarrollan sus scripts.
3. **Revisión:** Nosotros cruzamos sus gráficas y scripts con nuestro EDA global para verificar métricas, depuramos su código ("Insights") y lo integramos al reporte final.
