# Segundo Avance: Reporte de Ejecución

> **Proyecto:** Ganado Saludable — Sistema Integral de Auditoría Epidemiológica Bovina
> **Universidad Nacional "Rosario Castellanos"** — Licenciatura en Ciencias de Datos para Negocios
> **Enfermedad asignada:** Fiebre Aftosa (FMD) | Proxy de calibración: Tuberculosis Bovina
> **Fecha:** 30 de abril de 2026
> **Semestre:** 4° — 2026-1

---

## 1. Introducción

### 1.1 Resumen del Primer Avance

En el Primer Avance se presentó la arquitectura estratégica del proyecto "Ganado Saludable": un sistema integral de auditoría epidemiológica que utiliza la Tuberculosis Bovina (endémica en México) como proxy de calibración para modelar el impacto catastrófico de una reintroducción de Fiebre Aftosa (FMD), enfermedad de la cual México ha sido declarado libre desde 1954.

Se definió la alineación con las 7 materias del semestre, se diseñó la arquitectura ELT (Extract-Load-Transform), y se identificaron las fuentes de datos gubernamentales e internacionales necesarias.

### 1.2 Qué se ha ejecutado desde entonces

Este Segundo Avance documenta la **ejecución completa** de la primera mitad del proyecto:

- Pipeline ELT multi-fuente operativo (~29,200 registros limpios desde 6 fuentes)
- Análisis Exploratorio de Datos (EDA) con 8 hallazgos cuantificados
- Análisis Descriptivo de brotes en África (Top 5 países FMD)
- Análisis Inferencial: correlación zoonótica TB bovina↔humana y ANOVA de canales de venta
- Data Warehouse: transformación estructurada CSV→JSON con validación Pydantic
- Modelo matemático SIR dual (TB Bovina vs. FMD) mediante integración numérica de EDOs
- Cuantificación del impacto económico con modelos basados en literatura científica
- Arquitectura operativa de despliegue en campo (App + Dashboard NoSQL)

---

## 2. Pipeline de Datos: Adquisición y Transformación

### 2.1 El Problema de los Datos en México

Los datos sobre enfermedades animales en México **no están en un repositorio centralizado**. El ecosistema opera con PDFs gubernamentales sin versión tabular (SENASICA, DGE post-2017, COFEPRIS), APIs no documentadas que retornan 404, dashboards internacionales que generan archivos vía WebSocket (openFMD) y servidores universitarios inestables (UNAM/PUCRA).

### 2.2 Estrategia ELT Multi-Fuente

Para resolver esta fragmentación, se diseñó un pipeline de Extracción-Carga-Transformación (ELT) resiliente con tres capas:

- **Capa 1 — Extracción directa:** Fuentes estables con CSV/ZIP accesibles por HTTP (SENASICA hatos libres, DGE 2015-2017).
- **Capa 2 — Parsing de PDFs:** Reportes trimestrales SENASICA, anuarios DGE 2018-2024 y resoluciones COFEPRIS procesados con `pdfplumber`.
- **Capa 3 — Navegador automatizado:** Dashboard interactivo openFMD (R/Shiny) y servidores inestables UNAM, automatizados con Playwright.

### 2.3 Inventario de Datasets Recuperados

| Dataset | Archivo | Filas | Método | Estado |
|---------|---------|-------|--------|--------|
| SENASICA TB (hatos libres) | `senasica_tb_clean.csv` | 64 | CSV directo | ✅ 32 estados |
| SENASICA Cuarentenas 2024 | `senasica_cuarentenas_clean.csv` | 108 | PDF parsing | ✅ 4 trimestres |
| DGE Morbilidad Estatal 2015-2017 | `dge_morbilidad_clean.csv` | 384 | ZIP → CSV | ✅ |
| DGE Morbilidad Nacional 2018-2024 | `dge_morbilidad_2018_2024_clean.csv` | 28 | PDF parsing | ✅ |
| DGE Consolidado Nacional 2015-2024 | `dge_morbilidad_nacional_2015_2024_clean.csv` | 40 | Unión automatizada | ✅ Serie 10 años |
| openFMD Global (WRLFMD) | `openfmd_clean.csv` | 28,585 | Playwright export | ✅ 103 países |
| COFEPRIS Sanciones Alimentarias | `cofepris_clausuras_alimentarias_clean.csv` | 12 | PDF parsing | ✅ 7 empresas cárnicas |

**Total:** ~29,200 registros limpios desde 6 fuentes distintas.

### 2.4 Data Warehouse: Transformación CSV→JSON con Pydantic

**Código:** `src/warehouse/csv_to_json.py` — Aporte del Miembro 1 del equipo (Axel).

Se implementó un script de transformación que convierte los datos tabulares de cuarentenas (CSV) a un formato JSON jerárquico optimizado para MongoDB, utilizando **Pydantic** como capa de validación de tipos:

```python
class CuarentenaRecord(BaseModel):
    estado: str
    num_animales: int
    trimestre: int
    num_hatos_cuarentena: int
    anio: int
```

Este modelo garantiza que si un dato del CSV viene mal formado (ej. un string donde debe haber un entero), el sistema lance un error antes de contaminar la base de datos NoSQL. Los datos se agrupan jerárquicamente por Estado → Trimestre, generando el archivo `data/processed/cuarentenas.json`.

---

## 3. Hallazgos del Análisis Exploratorio (EDA)

**Notebook de referencia:** `notebooks/01_eda_global.ipynb`

### 3.1 COVID-19 validó la hipótesis de canales de venta

La serie temporal DGE 2015-2024 revela una anomalía natural que funciona como grupo de control involuntario:

| Año | Intoxicaciones Alimentarias (A05) | Tuberculosis (A15-A19) |
|-----|-----------------------------------|------------------------|
| 2019 | 31,916 | 22,283 |
| **2020** | **18,667 (−41.5%)** | **16,747 (−24.8%)** |
| 2024 | 25,259 | 25,980 |

Cuando México cerró tianguis, mercados informales y cadenas de comida callejera durante 2020, las intoxicaciones alimentarias colapsaron un **41.5%**. La tuberculosis cayó solo un 24.8% (transmisión respiratoria). Esto demuestra que los **canales de venta informales** son el vector primario de contagio alimentario.

### 3.2 Cobertura del programa TB Bovina: Solo el 1.2%

El programa SENASICA ha certificado **420,171 bovinos** como libres de tuberculosis, de una biomasa nacional de 35,100,000. Cobertura: **1.20%**. El 98.8% del hato opera en oscuridad estadística.

### 3.3 Cuarentenas SENASICA 2024: Jalisco concentra el 66.6%

**27 de 32 estados** tienen hatos bajo cuarentena activa: **856 hatos** y **7,558 animales** afectados. Jalisco concentra el 66.6% de los animales afectados (5,035) con solo el 15.8% de los hatos, sugiriendo concentración en unidades de producción grandes.

### 3.4 Las Américas: Inmunológicamente vírgenes a FMD

De **16,540 eventos FMD positivos** globalmente (2000-2025), las Américas representan solo el **2.7%**. México, libre desde 1954, tiene una biomasa 100% susceptible.

### 3.5 Serotipo O domina el 55% de las epidemias globales

El serotipo O (9,072 eventos, 54.9% del total) es el mismo que devastó al Reino Unido en 2001. Esto parametriza nuestro modelo SIR con R₀ = 6.0.

### 3.6 Opacidad regulatoria como indicador de riesgo

COFEPRIS no publica datos granulares sobre clausuras alimentarias con detalle de contaminantes. Se recuperaron 12 procedimientos de sanción, de los cuales 7 son explícitamente cárnicas. Si las empresas más grandes del sector no escapan sanciones, la cadena informal opera en un vacío de vigilancia total.

---

## 4. Análisis Estadístico del Equipo

### 4.1 Análisis Descriptivo: Top 5 Países FMD en África

**Notebook:** `notebooks/02_analisis_descriptivo.ipynb` — Aporte de la Miembro 2 del equipo (Victoria).

Se filtraron los eventos FMD positivos confirmados en la región africana (2000-2025) del dataset openFMD, aplicando técnicas de *Data Binning* por décadas y generando estadísticas descriptivas (media, mediana, desviación estándar del año de muestreo). Se identificó el Top 5 de países africanos con mayor incidencia.

**Hallazgo clave:** Se confirmó que los brotes en África no muestran tendencia a la baja, reforzando la hipótesis de que la FMD sigue siendo una amenaza activa a nivel global y que el sub-reporte del WRLFMD (Right-Censoring) enmascara la magnitud real del problema.

### 4.2 Análisis Inferencial: Correlación Zoonótica y ANOVA

**Notebook:** `notebooks/03_analisis_inferencial.ipynb` — Aporte de la Miembro 2 del equipo (Victoria).

Se realizaron dos pruebas inferenciales:

**A. Correlación cruzada TB Bovina ↔ TB Humana:**
Se calculó el coeficiente de correlación de Pearson entre los animales en cuarentena por TB bovina (SENASICA) y los casos de tuberculosis humana (DGE) agrupados por estado. El objetivo es demostrar estadísticamente que los estados con mayor carga animal presentan mayor morbilidad humana.

**B. ANOVA — Riesgo de Salmonella según canal de venta:**
Se simularon 1,000 muestras por canal utilizando distribuciones binomiales basadas en las prevalencias documentadas en la literatura:

| Canal de Venta | Prevalencia Salmonella |
|----------------|----------------------|
| Supermercados | 1.3% |
| Carnicerías | 8.4% |
| Tianguis | 13.6% |
| Mercados Municipales | 22.3% |

El test ANOVA evalúa si la diferencia entre canales es estadísticamente significativa (p < 0.05), confirmando cuantitativamente que el canal de distribución es un determinante del riesgo sanitario.

---

## 5. Modelado Matemático SIR

### 5.1 Fundamentos Teóricos

El modelo SIR (Susceptibles-Infectados-Recuperados), propuesto por Kermack y McKendrick en 1927, divide a la población en tres compartimentos que fluyen como líquidos en tuberías. Se implementó como un sistema de Ecuaciones Diferenciales Ordinarias (ODEs) resuelto mediante integración numérica (`scipy.integrate.odeint`), que utiliza internamente métodos de Runge-Kutta para garantizar precisión.

Las ecuaciones del sistema son:
- dS/dt = −β · S · I / N  (tasa de contagio)
- dI/dt = β · S · I / N − γ · I  (balance neto de infectados)
- dR/dt = γ · I  (acumulación de removidos)

### 5.2 Simulación Dual: TB Bovina vs. Fiebre Aftosa

**Código:** `src/models/sir_dual.py` | **Figura:** `docs/figures/sir_comparativo.png`

| Parámetro | TB Bovina (Endémica) | Fiebre Aftosa FMD (Shock Exótico) |
|-----------|---------------------|-----------------------------------|
| I₀ inicial | 7,558 animales (datos SENASICA 2024) | 1 animal (riesgo de importación) |
| R₀ estimado | 1.8 (Barlow, 1991) | 6.0 (Tildesley et al., 2006) |
| Duración (1/γ) | 180 días (crónica) | 14 días (aguda) |
| Pico de I a 150 días | **14,711 animales** | **18,752,410 animales** |
| Interpretación | Sangrado silencioso | Colapso exponencial catastrófico |

**Hallazgo Clave:** Un único animal importado con Serotipo O puede incendiar más del **53% del hato nacional** (18.7M de 35.1M) antes del día 150.

![Gráfico: Tuberculosis Endémica vs Fiebre Aftosa Exótica](../figures/sir_comparativo.png)

---

## 6. Análisis de Impacto Económico

### 6.1 TB Bovina: El "Cáncer Financiero" del Ganadero

**Código:** `src/models/tb_storytelling_plot.py`

Dado que la curva de infectados de TB es estable (~14K animales) pero persistente durante años, el daño real es acumulativo. Se construyó un modelo económico basado en literatura científica:

- **Caída en Producción:** Rahman & Samad (2009) reporta una caída del **-17%** en producción de leche por vaca infectada.
- **Precio de la Leche (SIAP México, 2024):** $6.50 MXN/litro.
- **Producción Estándar:** 18 litros/día por vaca (SAGARPA, 2023).
- **Derivación:** 18 L × 17% = 3.06 L perdidos → 3.06 × $6.50 = $19.89 MXN ≈ **$1.10 USD diarios por vaca**.

**Resultado:** Integrando el costo sobre 36 meses, la pérdida nacional asciende a **$17.3 Millones de USD** exclusivamente por caída en producción lechera.

![Impacto Financiero — Tuberculosis Bovina](../figures/tb_impacto_financiero.png)

### 6.2 Fiebre Aftosa: La Quiebra Automática

**Código:** `src/models/fmd_storytelling_plot.py`

A diferencia de la TB, la Fiebre Aftosa desencadena un colapso instantáneo:

- **Pérdida Biológica:** 500 kg en pie × $50 MXN = $25,000 MXN ≈ **$1,250 USD** por cabeza sacrificada (Fuente: SNIIM / Uniones Ganaderas).
- **Cierre de Fronteras:** Al declararse I₀=1, se activa un bloqueo OMSA a los $3,000 Millones USD anuales de exportación cárnica (pérdida de ~$8.2 Millones USD diarios).

**Resultado:** En menos de 150 días, la pérdida acumulada alcanza **$22.8 Billones de Dólares (Billions USD)**.

![Colapso Financiero — Fiebre Aftosa](../figures/fmd_impacto_nuclear.png)

---

## 7. Arquitectura Operativa Propuesta

### 7.1 Protocolo SENASICA Actual (DINESA)

Cuando existe sospecha de FMD, la CPA (Comisión México-Estados Unidos para la Prevención de la Fiebre Aftosa) coordina la respuesta:
1. Veterinarios oficiales inspeccionan las lesiones.
2. Se extraen muestras para un Laboratorio Nivel 3.
3. Si positivo, se detona el **DINESA** (Dispositivo Nacional de Emergencia de Sanidad Animal).
4. El Ejército y la Guardia Nacional clausuran fronteras estatales (Rifle Sanitario).

### 7.2 El Cuello de Botella: El Productor Informal

El problema no son los corporativos (SuKarne, Lala), sino los **productores de traspatio**. Ante el miedo al Rifle Sanitario y la burocracia de indemnización, el ganadero informal **evade reportar** e intenta vender vacas enfermas en tianguis y mercados negros. Este ocultamiento es el vector que habilita el R₀ = 6.0.

### 7.3 Propuesta: Sistema de Inteligencia Epidémica Basado en Incentivos

**Para el Ganadero (App Móvil):**
Una aplicación cuyo gancho de entrada (*Wedge*) sean los precios diarios del mercado ganadero. Si una vaca presenta anomalías, la app ofrece un "Botón de Pánico" que captura coordenadas GeoJSON y detona un proceso de **Indemnización Acelerada** (pago en 72 horas). Esto destruye el incentivo del mercado negro.

**Para la Autoridad (Dashboard NoSQL):**
La CPA visualiza un panel basado en MongoDB. Si tres productores denuncian anomalías en un radio de 50 km en menos de 2 horas, el sistema dispara una **Alerta Espacial de Enjambre** y corre la simulación SIR en tiempo real para informar al Ejército en qué casetas deben plantarse.

---

## 8. Estado de Avance por Materia

| Materia | Componente | Estado | Evidencia |
|---------|-----------|--------|-----------|
| **Ecuaciones Diferenciales** | Modelo SIR Dual (TB vs FMD) | ✅ Completado | `src/models/sir_dual.py` |
| **Bases de Datos NoSQL** | Data Warehouse CSV→JSON + Pydantic | ✅ Completado | `src/warehouse/csv_to_json.py` |
| **Estadística Multivariada** | EDA + ANOVA canales + Correlación zoonótica | ✅ Completado | `notebooks/01-03` |
| **Inteligencia Artificial** | XGBoost Clasificador (pendiente) | 🟡 En diseño | Features definidas |
| **Criptografía** | Cifrado César + RSA | 🟡 En progreso | Tarea delegada |
| **Finanzas Corporativas** | Modelos de impacto económico TB + FMD | ✅ Completado | `tb_storytelling_plot.py`, `fmd_storytelling_plot.py` |
| **Innovación Social** | Arquitectura App + Dashboard + DINESA | ✅ Conceptualizado | Sección 7 de este documento |

---

## 9. Bibliografía

- Barlow, N.D. (1991). *A spatially aggregated disease/host model for bovine Tb in New Zealand possum populations.* Journal of Applied Ecology, 28(3), 777-793.
- Brauer, F., & Castillo-Chávez, C. (2012). *Mathematical Models in Population Biology and Epidemiology.* Springer.
- FAO. (2026). *Update on Foot-and-Mouth Disease outbreaks in Europe and the Near East.* Organización de las Naciones Unidas para la Alimentación y la Agricultura.
- Kermack, W. O., & McKendrick, A. G. (1927). *A contribution to the mathematical theory of epidemics.* Proceedings of the Royal Society of London A, 115(772), 700-721.
- Rahman, M. A., & Samad, M. A. (2009). *Effect of bovine tuberculosis on milk production.* Bangladesh Journal of Veterinary Medicine, 7(2), 287-290.
- SENASICA. (2024). *Boletín Trimestral de Cuarentenas de Tuberculosis Bovina.* Servicio Nacional de Sanidad, Inocuidad y Calidad Agroalimentaria.
- SIAP. (2024). *Panorama Agroalimentario 2024.* Servicio de Información Agroalimentaria y Pesquera, México.
- Tildesley, M. J. et al. (2006). *Optimal reactive vaccination strategies for a foot-and-mouth disease outbreak in the UK.* Nature, 440, 83-86.
- WOAH. (2026). *Emergence of FMD Serotype SAT1 in the Golan region: Regional implications.* Organización Mundial de Sanidad Animal.
- WRLFMD / openFMD. (2025). *World Reference Laboratory for Foot-and-Mouth Disease — Open Data Portal.* The Pirbright Institute.
