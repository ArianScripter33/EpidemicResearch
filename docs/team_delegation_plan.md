# Plan de Delegación de Tareas al Equipo

> **Última actualización:** 2026-04-03 (Post EDA Global)  
> **Hallazgos de referencia:** `docs/hallazgos_fase1_eda.md`  
> **Notebook de referencia:** `notebooks/01_eda_global.ipynb`

---

## 1. Onboarding: Lo Que Todo El Equipo Debe Saber

Antes de asignar tareas, cada miembro del equipo debe:

1. **Leer** `docs/hallazgos_fase1_eda.md` — Resumen completo de qué datos tenemos, de dónde salieron, y qué descubrimos.
2. **Ejecutar** `notebooks/01_eda_global.ipynb` — Correr el notebook celda por celda para familiarizarse con los datasets y las gráficas.
3. **Entender los números clave:**
   - México tiene **35.1 millones** de cabezas de ganado bovino
   - Solo **1.2%** está certificado como libre de tuberculosis
   - **27 de 32 estados** tienen cuarentenas activas por TB bovina
   - Jalisco concentra **66.6%** de los animales afectados
   - Las Américas solo representan **2.7%** de los brotes globales de Fiebre Aftosa
   - COVID-2020 redujo intoxicaciones alimentarias en **41.5%** (al cerrar canales informales)

---

## 2. Alineación con Incidentes Críticos del Syllabus

| Incidente Crítico | Materia | Tarea Asociada | Asignado a |
|-------------------|---------|----------------|------------|
| IC1: Criptografía | Matemáticas Discretas | Cifrado César/RSA sobre datos sensibles | Miembro 1 |
| IC2: Estadística | Estadística Multivariada | Cálculos descriptivos + gráficas | Miembro 2 |
| IC3: NoSQL | Bases de Datos | Transformación CSV → JSON → MongoDB | Miembro 1 |
| IC4: Modelado SIR | Modelado Matemático | `scipy.odeint` (Core Team) | Arian |
| IC5: Visualización | Herramientas Computacionales | Mapa coroplético, gráficas SIR | Core Team + Miembro 2 |

---

## 3. Asignación de Tareas Concretas

### 👨‍💻 Miembro 1: Transformación a NoSQL y Criptografía

**Perfil necesario:** Python básico, manejo de diccionarios y JSON.

**Tarea A — Transformación NoSQL**
- **Input:** `data/processed/senasica_cuarentenas_clean.csv` (108 filas, 11 columnas)
- **Acción:** Convertir el CSV en una estructura JSON anidada por estado y trimestre. Ejemplo:
```json
{
  "Jalisco": {
    "Q1_2024": {"hatos": 30, "animales": 1200},
    "Q2_2024": {"hatos": 35, "animales": 1350}
  }
}
```
- **Entregable:** Script `src/warehouse/csv_to_json.py` + archivo `data/processed/cuarentenas.json`
- **Verificación:** El JSON debe tener 27 estados (coincide con EDA) y el total de animales debe sumar 7,558.

**Tarea B — Criptografía Básica**
- **Input:** `data/processed/cofepris_clausuras_alimentarias_clean.csv` (12 filas)
- **Acción:** Implementar una función de Cifrado César que encripte la columna `establecimiento` con una clave k=7. Implementar la función inversa (descifrado). Demostrar bidireccionalidad.
- **Entregable:** Script `src/crypto/encryption.py` con funciones `cifrar_cesar(texto, k)` y `descifrar_cesar(texto, k)`
- **Verificación:** `descifrar_cesar(cifrar_cesar("Bachoco", 7), 7)` debe retornar `"Bachoco"`.

**Tiempo estimado:** 3-4 horas total.

---

### 👨‍💻 Miembro 2: Estadística Descriptiva y Visualización

**Perfil necesario:** Pandas básico, Matplotlib o Seaborn.

**Tarea A — Top 5 Países FMD (África)**
- **Input:** `data/processed/openfmd_clean.csv` (28,585 filas)
- **Filtro obligatorio:** Continente africano (`un_region == "Africa"`), `fmdv_positive == "Yes"`, y `date_sampling` entre 2000 y 2025.
- **Acción:** Agrupar por `country`, contar eventos, graficar un barplot de los 5 países africanos con más brotes.
- **Resultado esperado:** Egipto (651), Kenia (645), Nigeria (552), Etiopía (505), Sudán (288).
- **Entregable:** Notebook `notebooks/02_analisis_descriptivo.ipynb` con la gráfica y 2 párrafos de interpretación.

**Tarea B — Estadísticos de TB Humana por Estado**
- **Input:** `data/processed/dge_morbilidad_clean.csv` (384 filas, dataset estatal 2015-2017)
- **Acción:** Filtrar filas donde CIE-10 sea "A15" o "A16" (tuberculosis respiratoria). Agrupar por estado. Calcular: media, mediana, desviación estándar y coeficiente de variación de los casos acumulados.
- **Entregable:** En el mismo notebook, una tabla resumen con los 32 estados + breve análisis de cuáles estados tienen mayor variabilidad.

**Tarea C (Opcional) — Interpretación del Efecto COVID**
- **Input:** La gráfica `dge_tendencia_temporal.png` generada por el notebook del EDA Global.
- **Acción:** Escribir 2 párrafos explicando por qué las intoxicaciones alimentarias cayeron 41.5% en 2020 pero la tuberculosis solo cayó 24.8%. ¿Qué dice esto sobre los mecanismos de transmisión de cada enfermedad?
- **Entregable:** Texto en Markdown al final de su notebook.

### 👨‍💻 Arian (Core Team)

**Perfil necesario:** Machine Learning, Ecuaciones Diferenciales, Orquestación de Repositorios.

**Tarea A — Modelado SIR Dual (FMD vs TB)**
- **Acción:** Implementar sistemas de ecuaciones diferenciales ordinarias (ODEs) con `scipy.odeint` para el Incidente de Modelado Matemático. 
- **Entregable:** Script `src/models/sir_dual.py` con 3 escenarios paramétricos calibrados con los R0 de la literatura.

**Tarea B — Estadística Inferencial (ANOVA)**
- **Acción:** Desarrollar el análisis de varianza para probar hipótesis sobre la contaminación estacional cruzada con factores de puntos de venta (Incidente de Estadística Multivariada).
- **Entregable:** Script `src/models/stats_multivariate.py`.

**Tarea C — Arquitectura y Review**
- **Acción:** Orquestar el entorno en GitHub, consolidar todos los análisis del equipo en un documento científico uniforme, y realizar validación cruzada y optimización de sus rutinas de código.

---

## 4. Nota Sobre Uso de Herramientas IA

Los miembros del equipo tienen acceso a agentes de inteligencia artificial (Gemini, ChatGPT, Copilot, etc.) para asistirles en la ejecución de sus tareas. **Esto es aceptable y recomendado**, siempre que:

1. **Entiendan** lo que el agente genera (no copy-paste ciego)
2. **Verifiquen** que los números coincidan con los datasets reales
3. **Documenten** qué herramientas usaron en sus notebooks (buenas prácticas de reproducibilidad)

Las tareas están diseñadas para ser simples en scope pero requieren comprensión del dominio epidemiológico. Si usan IA correctamente, pueden terminar más rápido y con mejor calidad — pero **el Core Team validará todo** en la fase de revisión.

---

## 5. Lo Que NO Deben Tocar

- `src/config.py` — Fuente de verdad. Solo lectura.
- `src/base_extractor.py` — Infraestructura interna.
- `src/extractors/*` — Los extractores ya están validados.
- `notebooks/01_eda_global.ipynb` — Nuestro notebook maestro SI pueden hacer una copia hacer merge.

---

## 6. Revisión y Optimización por Core Team

### 6.1 Checklist de Revisión (Por Tarea)

Cuando cada miembro entregue su trabajo, el Core Team (Arian) ejecutará esta revisión:

**Para Miembro 1 (NoSQL + Criptografía):**

| Criterio | Verificación | Acción si falla |
|----------|-------------|-----------------|
| JSON bien formado | `json.load()` no lanza error | Devolver con instrucciones de fix |
| Suma de animales = 7,558 | `sum(all_animales) == 7558` | Revisar agrupación por estado |
| 27 estados en JSON | `len(json.keys()) == 27` | Verificar filtro de estados |
| Cifrado bidireccional | `descifrar(cifrar("Bachoco", 7), 7) == "Bachoco"` | Revisar lógica de módulo |
| Manejo de caracteres especiales | Cifrar "S.A. DE C.V." no rompe | Agregar guard para no-alfabéticos |

**Para Miembro 2 (Stats + Viz):**

| Criterio | Verificación | Acción si falla |
|----------|-------------|-----------------|
| Filtro FMD correcto | Solo `fmdv_positive == "Yes"` y año >= 2000 | Devolver — datos sin filtrar son inútiles |
| Top 10 coincide con EDA | India ≈ 1,506, Pakistán ≈ 1,455 | Cruzar contra `01_eda_global.ipynb` |
| Stats TB por estado completos | 32 estados presentes | Verificar que no hicieron `dropna()` |
| Interpretación COVID coherente | Menciona cierre de tianguis/canales informales | Guiar si es superficial |

### 6.2 Optimización de Algoritmos

Si el código de los miembros funciona pero es ineficiente o poco elegante, el Core Team tiene permiso de:

1. **Refactorizar** sus scripts manteniendo la lógica original (no reescribir desde cero)
2. **Documentar** las optimizaciones como comentarios inline (`# Optimizado por Core Team: ...`)
3. **Agregar type hints** y docstrings si faltan
4. **Limpiar** outputs de notebook (quitar celdas de debug, ordenar visualizaciones)

**Regla de oro:** Si el miembro hizo el 80% correcto, el Core Team completa el 20% restante. Si hizo menos del 50% correcto, se le devuelve con feedback específico para rehacerlo.

### 6.3 Sesión de Feedback (30 min por miembro)

Después de la revisión técnica, el Core Team conduce una mini-sesión donde:

1. **Se muestra** su trabajo integrado en el notebook global — que vean cómo su gráfica encaja en la narrativa completa
2. **Se explican** las optimizaciones hechas — que aprendan del refactor, no solo reciban el código limpio
3. **Se validan** sus interpretaciones — si escribieron "India tiene más brotes porque tiene más vacas", se les desafía: "¿Es por la densidad ganadera, la falta de vacunación, o ambas?"
4. **Se documenta** la contribución de cada miembro para el reporte final

### 6.4 Criterio de Integración al Reporte

El trabajo de los miembros se integra al artículo final **solo si:**

- [ ] Pasa todos los criterios del checklist (sección 6.1)
- [ ] Las gráficas tienen títulos, ejes etiquetados y fuentes citadas
- [ ] Las interpretaciones son coherentes con los hallazgos del EDA global
- [ ] El código corre sin errores en el entorno del proyecto (`requirements.txt`)

---

## 7. Flujo de Revisión Completo

```
1. Onboarding (Lectura)      →  Cada miembro lee hallazgos_fase1_eda.md
2. Asignación (CSVs + .md)   →  Se les entrega los CSVs y este plan
3. Ejecución (3-5 horas)     →  Desarrollan scripts/notebooks (pueden usar IA)
4. Entrega (Pull Request)    →  Suben su rama al repo
5. Revisión (Checklist 6.1)  →  Core Team valida contra EDA global
6. Optimización (6.2)        →  Core Team refactoriza si necesario
7. Feedback (6.3)            →  Sesión de 30 min por miembro
8. Integración (6.4)         →  Se incorpora al reporte final
```

---

## 8. Calendario Sugerido

| Día | Miembro 1 | Miembro 2 | Core Team |
|-----|-----------|-----------|-----------|
| Día 1 | Onboarding + Tarea A (JSON) | Onboarding + Tarea A (Top 10 FMD) | Modelo SIR Dual |
| Día 2 | Tarea B (Criptografía) | Tarea B (Stats TB por estado) | ANOVA + Financiero |
| Día 3 | — | Tarea C (Interpretación COVID) | Mapa coroplético |
| Día 4 | Code Review conjunto | Code Review conjunto | Integración al artículo |
