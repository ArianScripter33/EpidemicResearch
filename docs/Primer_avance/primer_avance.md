# 🐄 Ganado Saludable: Primer Avance del Proyecto Prototípico

**Fecha:** 26 de marzo de 2026  
**Licenciatura:** Ciencias de Datos para Negocios  
**Semestre:** 4° (Semestre 2026-1)  
**Institución:** Universidad Nacional "Rosario Castellanos"  
**Docente:** Víctor Hugo Reyes Anselmo  

---

## 1. Introducción y Contexto (Audit de 2026)

Este proyecto, titulado **"Ganado Saludable"**, propone una infraestructura de auditoría sistémica de externalidades bovinas en México. Bajo el enfoque **"One Health"** (Una Sola Salud), se busca integrar datos de sanidad animal, salud pública y finanzas para prevenir crisis epidemiológicas catastróficas.

### ⚠️ Alerta Global 2026 (Actualización de Investigación)

Nuestra investigación de campo y monitoreo de fuentes internacionales (FAO/WOAH) revela que en **marzo de 2026** se han confirmado brotes críticos de **Fiebre Aftosa (FMD)** en:

* **Chipre (Lárnaca):** 49 unidades afectadas, >26,000 cabezas sacrificadas.
* **Grecia (Lesbos):** Primer brote detectado desde 2001.
* **Israel (Golan):** Identificación del serotipo SAT1.

Esta coyuntura hace que nuestra **enfermedad asignada (Fiebre Aftosa)** sea de máxima relevancia para la seguridad nacional agropecuaria de México, país que ha sido libre de la enfermedad desde 1954, pero cuya vulnerabilidad ante una reintroducción es crítica.

---

## 2. Planteamiento del Problema

México posee una biomasa bovina de **35.1 millones de cabezas**. Un brote de fiebre aftosa en el país no representaría solo una crisis sanitaria, sino un **bloqueo comercial total** de las exportaciones de carne, con un impacto económico proyectado de **$200,000 millones de pesos** (basado en la progresión del brote del Reino Unido en 2001, ajustado a la biomasa mexicana).

### Incidentes Críticos Identificados

1. **Ciberseguridad:** Intercepción maliciosa de datos IoT para enmascarar brotes.
2. **Incertidumbre Epidemiológica:** Incapacidad de predecir la velocidad de contagio (R0).
3. **Riesgo Financiero:** Subestimación del costo de reacción vs. prevención primaria.

---

## 3. Objetivos

### Objetivo General

Diseñar e implementar un sistema integral de monitoreo y alerta temprana que utilice **Ciencia de Datos, IA y Modelado Matemático** para anticipar el impacto de la Fiebre Aftosa en México, utilizando la Tuberculosis Bovina como métrica de calibración.

### Objetivos Específicos y Alineación Académica (Integración de Materias)

1. **Inteligencia Artificial:** Entrenar un modelo de machine learning (XGBoost Clasicador) diseñado para estimar la probabilidad de brotes (identificados bajo CIE-10 A05). Las variables predictoras (features) de este modelo incluirán determinantes que no son convencionales, tales como el volumen de alimento procesado y un innovador "Proxy de Opacidad": el número de clausuras efectuadas por COFEPRIS debido a infracciones vinculadas al clembuterol u otros LMR (Límites Máximos de Residuos).
2. **Estadística Multivariada:** Implementar esquemas visuales para la identificación de perfiles de riesgo epidemiológico (agrupaciones o clusters) a nivel estatal empleando **Análisis de Componentes Principales (PCA)** para lidiar con altas dimensionalidades. Se reforzará con gráficos como las **Curvas de Andrews** y representaciones antropomórficas como las **Caras de Chernoff**, con el objetivo de facilitar el entendimiento de patrones geográficos donde se combinan variables críticas.
3. **Ecuaciones Diferenciales:** Traducir escenarios biológicos en la formulación de **sistemas dinámicos tipo SIR** (Susceptibles-Infectados-Recuperados). La modelación se efectuará operando el sistema primero en su fase pasiva-analítica con los ratios infecciosos de tuberculosis (calibración), iterándolo mediante las derivadas aplicables al escenario prospectivo ante Fiebre Aftosa.
4. **Bases de Datos NoSQL:** Migrar la administración de entidades de información altamente variopinta y esquemática (PDFs crudos, datasets del DGE/SINAIS) a colecciones soportadas mediante el uso de un clúster de bases documentales distribuidas, específicamente **MongoDB**. Este sistema estructurará el DWH asimilando métricas procedentes de los extractores generados.
5. **Criptografía:** Asegurar la trazabilidad mediante algoritmos para anonimizar los identificadores que viajen hacia la analítica. Incorporará **codificación en bloques (Cifrado César)** a modo de ofuscación de entidades (lotes de seguimiento) más **criptosistemas de firma robusta de claves asimétricas (RSA)**, como mecanismo que resista falsificaciones maliciosas contra ecosistemas de tipo IoT incrustados en sistemas ganaderos.
6. **Finanzas Corporativas:** Justificar fiscal y corporativamente el costo del ecosistema al trazar los análisis determinantes (TIR o **VPN**) como justificación. El fin será contraponer el desembolso por la tecnología de monitorización versus los más de \$200,000 millones probables extraídos del PIB del país por la reintroducción de la Fiebre Aftosa (FMD).
7. **Innovación Social:** Posibilitar que tales analíticas generen intervenciones asertivas integrales basadas en el concepto *One Health*, protegiendo la carga económica familiar desproporcionada que resuena hacia las poblaciones subrepresentadas de rastros y mercados en zonas endémicas por descuidos en inocuidad alimentaria.

---

## 4. Marco Teórico y Avance de Investigación Sustancial

### 4.1 La Estrategia de Calibración (Proxy Epidemiológico y Riesgo Zoonótico)

Dado que México ostenta el estatus de país libre de Fiebre Aftosa (FMD) sin vacunación desde 1954, no resulta posible ingerir datos históricos locales provenientes de este patógeno para modelar su propagación. La propuesta metodológica innovadora radica en utilizar a la **Tuberculosis Bovina (TB)** —zoonosis grave con dinámica endémica en México de las cuales se destinan hasta \$300 millones de pesos anuales dentro de la fiscalización del Estado— como **entidad de calibración (Proxy Epidemiológico)**. La mecánica transcurrirá con el siguiente orden:

1. **Calibración TB Bovina:** La asimilación al sistema biológico con los datos empíricos procedentes de las acciones de SENASICA producirán los determinantes para la función matemática con un índice de propagación moderada estimada en un $R_0 \approx 1.8$.
2. **Transfer Learning Viral (FMD):** Una vez afinada la mecánica en México con datos de la tuberculosis en Python, las métricas predictivas (mediante uso de derivadas) recibirán un incremento (factor de aceleración exógena) basado en cifras paramétricas importadas de casos extremos extranjeros y estudios prospectivos que infieren las reproducciones al salto catastrófico situando a la Fiebre Aftosa en un nivel de $R_0 \approx 6.0$.
3. **Replicabilidad Cuantitativa:** La experimentación y modelación derivará simulaciones precisas sobre el efecto destructivo de una reactivación epidemiológica generalizada de esta zoonosis foránea.

### 4.2 Fuentes de Datos Auditadas para Extracción Masiva (Módulos ETL)

El marco actual de fuentes estructuradas, a menudo albergadas de forma dispersa con esquemas tecnológicos "hostiles" (como el control ActiveX del gobierno y sitios de dinámica JavaScript en la Plataforma Nacional de Transparencia PNT) estipularon las vías siguientes como canales de rastreo de nuestra data lake principal:

* **Ministerio/SENASICA:** Monitoreo desde repositorios y la API encubierta (JSON/CSV) de las detecciones de hatos en seguimiento o los PDFs con registros de cuarentenas ejecutadas.
* **Instituto Nacional DGE/SINAIS:** Captura tabulada desde Anuarios de salud oficial de incidencias de zoonosis cruzadas y fallecimientos reportados bajo listados de morbilidad humana (CIE-10). Todo mapeado por correlación departamental/regional con eventos del animal.
* **OpenFMD / Institutos Aprobados Internacionales:** Repositorios de datos que incluyen series de evolución actual de virus reportados a lo largo del hemisferio (brotes del inicio del año 2026 y reportes en Sudamérica) de extrema importancia para algoritmos de Series de Tiempo del AWS Chronos.
* **PUCRA (UNAM):** Exposición de datos biológicos sobre una variable alarmante de RAM (Resistencia a Antimicrobianos) expresados en PDFs; como lo es el 94% de insensibilidad del microbio a la ampicilina encontrado a nivel mercado comercial.
* **Inspección e infranormatividad (PNT / COFEPRIS):** Generación de "Spiders/Bots" de web-scraping en un navegador automatizado Headless (Selenium) que identifique resoluciones coercitivas, determinando actas con detección de fallos por presencia del componente anabólico (Clembuterol) o niveles anéticos de salmonela.

---

## 5. Instrumentación Analítica Específica (Innovación en IA y Estadística)

La arquitectura analítica del proyecto no solo recaba información, sino que despliega técnicas avanzadas de ciencia de datos para encontrar la señal entre el ruido estadístico de la vigilancia agropecuaria:

### 5.1 Análisis de Componentes Principales (PCA)

Las variables extraídas de la locación endémica (como densidad de poblaciones ganaderas por estado, la recurrencia de clausuras ante LMR, ventas clandestinas en tianguis o la carga antibiótica en los rastros) generan una matriz de muy alta dimensionalidad. El modelo asimilará estas variables empleando PCA.
* **Propósito:** Condensar la "presión ganadera" o la "degradación en sanidad" como componentes en dos o tres ejes rectores, explicando más del 70% de la varianza del fenómeno en vectores interpretables (Componentes Principales 1 y 2). Esto evidenciará empíricamente correlaciones latentes (ej. la similitud de ecosistemas de bioseguridad deficiente entre regiones no contiguas geográfica, pero sí operativamente como Jalisco y Veracruz).

### 5.2 Visualizaciones Multivariadas (Curvas de Andrews y Caras de Chernoff)

Con las dimensiones de riesgo sintetizadas, convertiremos la tabla cruda de 32 estados de México en visualizaciones diseñadas para la cognición humana inmediata:

* **Curvas de Andrews:** Representaremos cada entidad federativa mediante transformaciones de la serie de Fourier, graficándolas como líneas de oscilación variable. Ello facilitará la localización expedita de clusters/agrupaciones de riesgo subyacentes o de outliers y comportamientos discrepantes.
* **Caras de Chernoff:** Traduciremos variables complejas (ratios de prevalencia, RAM e infecciones A05) a rasgos antropomórficos (curvatura de boca, tamaño de los ojos). Detectar de forma facial los perfiles de los estados en riesgo de un impacto inminente provee un poderoso puente de Innovación Social en reportes técnicos dirigidos a personal de políticas públicas no entrenado en ML.

### 5.3 Inteligencia Artificial (Modelo XGBoost Clásico)

Dejando de lado la predicción con el modelo SIR, que trabaja asumiendo poblaciones generales, implementaremos algoritmos de reforzamiento por gradiente (Extreme Gradient Boosting C).

* **Input (Features):** La ingesta asimilará el recuento de los patógenos cruzados (Salmonelosis desde la DGE/SINAIS) con predictores que el modelo considerará de bioseguridad, tales como el número de "Hatos Libres" detectados o el "Proxy de Opacidad" generado al contabilizar localizaciones recabadas por scraping (clausuras locales debidas a excesos de clembuterol en rastros).
* **Output (Target):** El sistema asignará una métrica o AUC de riesgo predicho que estimará probables subidas en incidentes de intoxicaciones alimentarias y problemas de diseminación zoonótica. A diferencia de un simple cálculo R0 generalizado del modelo SIR, la predicción XGBoost provee interpretabilidad al localizar las *features* de mayor peso (e.g. clausuras sanitarias pasadas auguran brotes futuros mejor que las simples variables climáticas).

---

## 6. Propuesta Metodológica y Diseño de Ingeniería de Software (Arquitectura ELT)

La instrumentación de software del proyecto recae sobre una infraestructura ELT (Extract-Load-Transform) orquestada que materializa la visión de la Auditoría Sistémica. La línea de procesamiento obedece al formato dimensional (Data Warehouse):

1. **Submódulo de Extracción Transaccional:** Programación dual de módulos Python ("Arañas Asíncronas" basadas en framework Headless/Playwriight) frente a interrupciones o modales interactivos en sitios como la PNT. Estas se suman a conexiones por Requests que acceden sigilosamente a las APIs inexpresivas del SENASICA, vulnerando las restricciones artificiales del gobierno que solo habilitan visores como OWC11 (Microsoft ActiveX) de los años 90.
2. **Capa Data Lake / Capa Oro NoSQL (MongoDB):** Todos los reportes PDF transcritos mediante metodologías heurísticas OCR (utilizando Camelot / Pdfplumber), junto con los dataset numéricos de APIs desofuscadas de JSON, quedan anclados en un repositorio NoSQL. Estarán normalizados según el modelo transaccional Star-Schema (estrella), que correlaciona de manera escalable y eficiente las propiedades temporales (fact_tiempo, fact_geografia) contra la métrica estadística del riesgo sanitario.
3. **Analíticas e Ingeniería Matemática (Integración SciPy):** Con los datos unificados, diferentes pipelines emplearán la solución de Runge-Kutta sobre *scipy.integrate.odeint* que derivarán los puntos de corte en las simuladas curvas de propagación SIR para estimar en modo predictivo el instante de un desbordamiento o salto al brote pandémico nacional.
4. **Visor Diagnóstico Automatizado (Dashboard):** Para culminar la evidencia, se desplegarán las lógicas y perfiles descriptivos en librerías reactivas analíticas. Las gráficas derivadas de Matplotlib/Plotly mostrarán correlaciones sobre mapas coropléticos a color que permitirán a cualquier miembro calificador del Coloquio constatar de primera mano cómo una simulación financiera y biológica puede proteger nuestro entorno nacional.

---

## 7. Bibliografía (APA 7)

* FAO. (2026). *Update on Foot-and-Mouth Disease outbreaks in Europe and the Near East*.
* WOAH. (2026). *Emergence of FMD Serotype SAT1 in the Golan region: Regional implications*.
* Brauer, F., & Castillo-Chávez, C. (2012). *Mathematical Models in Population Biology and Epidemiology*. Springer.
* SENASICA. (2024). *Boletín Trimestral de Cuarentenas de Tuberculosis Bovina*.
* Russell, S., & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach*. Pearson.

---

## 8. Entregables Finales y Estrategia de Ejecución (MVP)

Alineación estricta con los requerimientos de evaluación del Problema Prototípico exige evitar el sobre-desarrollo tecnológico (*overengineering*). Por consiguiente, la ejecución del proyecto operará bajo una estrategia de **Producto Mínimo Viable (MVP)**. Toda la infraestructura de extracción de datos, bases de datos NoSQL y el entrenamiento de modelos de Inteligencia Artificial fungirán como "herramientas instrumentales" con el único fin de materializar los dos **entregables definitivos**:

1. **Artículo de Divulgación Científica:** Documento maestro (15 a 25 páginas, formato APA 7, 5+ fuentes). Sintetizará el cumplimiento de las 7 materias, destacando fuertemente el componente de **Innovación Social**: utilizando un test de varianza ANOVA, demostraremos estadísticamente cómo la desigualdad recae sobre las subpoblaciones consumidoras de mercados y tianguis locales (prevalencia de patógenos del 22.3% frente a un 1.3% en supermercados corporativos).
2. **Exposición en Coloquio (Presentación Digital):** Apoyo visual de entre 15 y 20 diapositivas desarrolladas en plataformas en nube (Gamma / Genially). La presentación culminará con nuestro "Impacto Visual Base" (Gráficas SIR comparativas entre la lenta TB frente a la FMD), simplificando Ecuaciones Diferenciales para un jurado multidisciplinario.

---
> **Estado de avance:** 100% de la planificación estratégica, justificación epidemiológica/académica y definición de la arquitectura de extracción de datos (ELT) completadas con éxito.
