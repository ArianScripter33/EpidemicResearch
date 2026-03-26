# 🐄 Ganado Saludable: Auditoría Sistémica de Externalidades Bovinas en México

> **Proyecto Prototípico · 4° Semestre · Lic. Ciencias de Datos para Negocios**
> Universidad Nacional "Rosario Castellanos" — Semestre 2026-1

---

## 📌 ¿Qué es este proyecto?

**Ganado Saludable** no es solo una plataforma de monitoreo de vacas enfermas. Es una **infraestructura de auditoría de salud pública** que conecta tres mundos que el gobierno mexicano trata como silos independientes:

```
🐮 Sanidad Animal     ←→     🏥 Salud Humana     ←→     💰 Finanzas Públicas
   (SENASICA)                    (SINAIS/DGE)              (SHCP/Indemnizaciones)
```

Bajo el enfoque **"One Health" (Una Sola Salud)** de la OMS, la FAO y la WOAH, este proyecto demuestra que **la fiebre aftosa, la tuberculosis bovina, la resistencia antimicrobiana y las intoxicaciones alimentarias no son problemas aislados**, sino eslabones de una misma cadena que termina costándole al erario público miles de millones de pesos en el peor escenario.

> **🎯 Enfermedad Asignada: Fiebre Aftosa (FMD)**
> 
> Nuestra enfermedad objetivo asignada por la cátedra es la **Fiebre Aftosa**. Sin embargo, México es oficialmente **libre de fiebre aftosa desde 1954**, por lo que no existen datos de brotes nacionales para modelar. Nuestra solución metodológica es usar **Tuberculosis Bovina** — una zoonosis endémica con datos reales en México — como **proxy de calibración** para nuestros modelos epidemiológicos, y luego transferir esos parámetros al escenario catastrófico de una reintroducción hipotética de FMD. Esto es análogo al concepto de *transfer learning* en Machine Learning.

---

## 🧠 La Tesis Central (El "So What?")

> **"México es libre de fiebre aftosa desde hace 70 años, pero nunca ha probado sus planes de contingencia bajo estrés real. Usando datos reales de tuberculosis bovina como proxy de calibración epidemiológica, este proyecto simula qué pasaría si la FMD re-ingresara — y demuestra que la prevención primaria es 100x más barata que la reacción tardía."**

### Las 3 preguntas que respondemos con datos:

1. **¿Cuánto perdería México si la fiebre aftosa re-ingresara?** → Simulación SIR calibrada con datos reales. Referencia: UK 2001 perdió ~£8 mil millones (~$200B MXN). Con 35.1M de cabezas en México, el impacto proyectado es catastrófico.
2. **¿Se puede anticipar la velocidad de propagación?** → Modelo SIR dual: calibrado con TB bovina (R0 ≈ 1.8), transferido a FMD (R0 ≈ 6.0). XGBoost para detectar señales tempranas de bioseguridad deficiente.
3. **¿Qué tan preparado está México?** → Cruce de datos de capacidad de respuesta (manuales CPA) vs velocidad de propagación simulada. Análisis de brecha: tiempos teóricos de cuarentena vs tiempo real que tomaría aislar 35.1M de cabezas.

---

## 🔬 Los 3 Vectores Analíticos

### Vector 1 — 🔴 Fiebre Aftosa (Enfermedad Asignada — Shock Exógeno Catastrófico)

> **Este es el vector principal del proyecto.** La Fiebre Aftosa (FMD) es la enfermedad más temida de la ganadería mundial, con capacidad de paralizar la economía agropecuaria de un país entero en semanas. En enero de 2025, la FAO emitió una alerta global por brotes en Europa y Cercano Oriente, recordando que **ningún país libre está verdaderamente a salvo**.

| Componente | Fuente de Datos | Hallazgo Esperado |
|---|---|---|
| **Internacional** | openFMD (CSV global de brotes) | Series de tiempo de brotes por país/fecha para entrenar modelos Chronos. R0 estimado del brote UK 2001 (R0 ≈ 4.0–8.0) |
| **Sudamérica** | WRLFMD + PANAFTOSA/OPS (reportes por país) | Serotipos circulantes, última epidemia por país. Datos de Argentina, Colombia, Venezuela como referencia regional |
| **Nacional — Preparedness** | Manuales CPA/SENASICA (PDFs) | KPIs de capacidad de respuesta: t_detección, t_notificación, t_cuarentena, brigadas disponibles, capacidad de sacrificio/día, laboratorios de diagnóstico |
| **Nacional — Simulación** | Modelo SIR dual (calibrado con TB → transferido a FMD) | Escenarios de propagación: ¿Cuántas cabezas se infectan en 30/60/90 días? ¿Cuántos estados se afectan? ¿Cuál es el punto de no retorno? |
| **Financiero** | Referencia UK 2001 + extrapolación a México | Costo estimado de una incursión: pérdida directa (sacrificio) + indirecta (embargo comercial, cierre de exportaciones, desempleo rural) |

**¿Por qué la FMD es diferente a cualquier otra enfermedad bovina?**

| Característica | Tuberculosis Bovina | Fiebre Aftosa |
|---|---|---|
| **Status en México** | Endémica (presente, controlable) | Exótica (libre desde 1954) |
| **R0 estimado** | ~1.5 – 2.0 | **~4.0 – 8.0** (3-5x más contagiosa) |
| **Velocidad de propagación** | Meses a años | **Días a semanas** |
| **Mortalidad animal** | Baja en adultos, crónica | Baja, pero la morbilidad es devastadora |
| **Impacto económico principal** | Despoblación selectiva + indemnización | **Embargo comercial total** — cierre de exportaciones |
| **Mecanismo de transmisión** | Contacto directo, leche, aerosol cercano | **Aerosol a distancia**, fómites, vehículos, personas, viento |
| **Referencia de costo** | ~$39M MXN/brote (Chihuahua) | **~£8B ($200B MXN)** — brote UK 2001 |

**Datos Clave de la FMD (del Problema Prototípico + FAO 2025):**
- La FAO advirtió en enero 2025 sobre brotes activos en **Europa y Cercano Oriente** — la enfermedad no es historia, es actualidad.
- Afecta a **todos los animales de pezuña partida**: bovinos, porcinos, ovinos, caprinos, búfalos.
- Se transmite por **contacto directo, aerosol, objetos contaminados** e incluso por **personas** (en su ropa/calzado).
- Causa **vesículas y aftas** en boca, lengua, pezuñas y ubres → los animales no comen, no caminan, no producen leche.
- El impacto real no es la mortalidad (que es baja en adultos), sino la **parálisis comercial**: un solo caso confirmado puede cerrar las exportaciones de carne de TODO México.
- México mantiene un estatus **"Libre sin vacunación"** ante la OIE/WOAH, lo que paradójicamente lo hace más vulnerable: no hay inmunidad de rebaño.

**Dato Impactante:** En el brote de UK 2001, se sacrificaron **más de 6 millones de animales** y el costo total superó los **£8 mil millones** (~$200B MXN). México tiene una biomasa bovina de 35.1M de cabezas — casi 6x la que tenía UK. Un brote aquí sería la mayor crisis agropecuaria de la historia de Latinoamérica.

---

### Vector 2 — Tuberculosis Bovina (Proxy de Calibración Epidemiológica)

> **TB Bovina no es la enfermedad asignada, pero es nuestra arma secreta.** Tiene datos reales, granulares, descargables de SENASICA y DGE. La usamos para calibrar los modelos SIR con parámetros mexicanos reales, y luego transferimos esos parámetros (ajustando R0) al escenario de FMD.

| Componente | Fuente de Datos | Hallazgo Esperado |
|---|---|---|
| **Animal** | API oculta SENASICA + CSVs hatos libres | Mapa estatal de prevalencia TB. Calibración de β y γ con datos reales de cuarentenas y despoblaciones |
| **Humano** | Anuarios DGE (CIE-10 A15-A19) + Cubos SINAIS | Correlación geográfica: estados con más TB bovina → más TB humana extrapulmonar |
| **Económico** | DOF + Seguros pecuarios | Costo estimado por Unidad Animal despoblada (~85% del valor de mercado). Gasto público anual en campaña nacional: >300M MXN |
| **Transfer Learning** | Parámetros calibrados | β_tb → β_fmd (multiplicar por factor R0_fmd/R0_tb ≈ 3.3x), luego simular el escenario FMD |

**Dato Impactante:** La degradación sanitaria de Tamaulipas por APHIS-USDA en 2020 causó parálisis comercial — y eso fue solo por TB. Un evento de FMD activaría consecuencias 100x más severas.

### Vector 3 — Resistencia Antimicrobiana (La Crisis Silente)

| Componente | Fuente de Datos | Hallazgo Esperado |
|---|---|---|
| **Clínico** | PUCRA/UNAM (PDFs 2022-2025) | Tasas de resistencia hospitalaria por E. coli y K. pneumoniae. Correlación con regiones ganaderas |
| **Alimentario** | PNT/COFEPRIS (Selenium scraping) | Número de clausuras por clembuterol/LMR por estado. Rastros reincidentes |
| **Genómico** | V2.md (literatura secundaria) | Prevalencia de genes blaCTX-M (23.5%), blaTEM (15%), bombas de eflujo tet(A/B) |

**Dato Impactante:** El 94.7% de las cepas de Salmonella en carne molida mexicana son resistentes a ampicilina. Esto convierte una intoxicación alimentaria "simple" en una emergencia hospitalaria que consume antibióticos de último recurso.

---

## 🎓 Cobertura de las 7 Materias (Incidentes Críticos)

Esta es la sección que más importa para la evaluación: cómo cada materia del semestre se integra de manera **funcional y no decorativa** en el proyecto.

### 1. 🔐 Fundamentos de Criptografía

**Incidente Crítico:** *"Competencia desleal: intercepción y manipulación de datos en la nube"*

| Requisito del PP | Nuestra Implementación | Entregable |
|---|---|---|
| Selección de técnica de cifrado más adecuado | Análisis comparativo César vs Hill vs RSA para proteger IDs de lotes y datos IoT | Tabla comparativa con pros/contras |
| Cifrado César con desplazamiento n | `src/crypto/encryption.py` — `caesar_encrypt("LOTE", 3)` → `"ORWH"` | Código funcional + demo interactiva |
| Cifrado RSA (asimétrico) | Generación de par de llaves RSA para firmar payloads de sensores IoT | Código funcional + diagrama de flujo |
| Integridad de datos IoT ante inyección maliciosa | Hash SHA-256 + firma digital para verificar que los datos no fueron alterados en tránsito | Protocolo documentado |

**Hallazgo Potencial para el artículo:**
> *"En un escenario donde un competidor inyecta datos falsos de temperatura para enmascarar un brote de fiebre aftosa, el cifrado César solo ofusca el identificador del lote, pero NO garantiza integridad. Se requiere RSA + hashing para firmar digitalmente cada lectura del sensor, convirtiendo la manipulación de datos en un acto criptográficamente detectable."*

---

### 2. 📊 Estadística Multivariada

**Incidente Crítico:** *"Estadística Multivariada en Sanidad Bovina"*

| Requisito del PP | Nuestra Implementación | Entregable |
|---|---|---|
| Representación gráfica de datos multivariados | Visualizaciones EDA sobre las variables cruzadas (prevalencia, clima, densidad) | Notebooks con gráficos |
| Caras de Chernoff | Cada estado de México representado como una "cara" donde los rasgos codifican: prevalencia TB, resistencia RAM, clausuras, producción | Gráfico de 32 caras |
| Curvas de Andrews | Series de Fourier para visualizar clusters de estados con perfiles epidemiológicos similares | Gráfico multidimensional |
| Regresión lineal múltiple | Modelo de regresión: variable dependiente = casos A05, independientes = densidad ganadera, prevalencia Salmonella, clausuras | Tabla de coeficientes + R² |
| ANOVA / MANOVA | Test: ¿Hay diferencia significativa en la prevalencia de Salmonella entre los 4 canales de comercialización? (Supermercados 1.3% vs Tianguis 13.6% vs Mercados 22.3%) | p-value + interpretación |
| Análisis de Componentes Principales (PCA) | Reducción dimensional de las variables ganaderas para identificar los factores latentes que mejor explican la varianza epidemiológica | Scree plot + biplot |

**Hallazgo Potencial:**
> *"El análisis PCA revela que el 78% de la varianza en morbilidad humana por intoxicaciones alimentarias se explica por solo 3 componentes principales: (1) densidad ganadera estatal, (2) porcentaje de comercialización informal (tianguis), y (3) número de clausuras por LMR. Las Caras de Chernoff muestran que Veracruz, Jalisco y Chiapas — los 3 estados con mayor población bovina — comparten perfiles epidemiológicos casi idénticos."*

---

### 3. 🤖 Inteligencia Artificial

**Incidente Crítico:** *"Sistema de alerta temprana mediante IA"*

| Requisito del PP | Nuestra Implementación | Entregable |
|---|---|---|
| Análisis e interpretación de datos relevantes | EDA sobre datasets cruzados SENASICA × DGE × PNT | Notebooks exploratorios |
| Diseño de solución basada en IA | **XGBoost Classifier:** Predice probabilidad de brote de intoxicación A05 por estado/trimestre | Modelo entrenado + métricas |
| Evaluación de factibilidad | Análisis de costo computacional, disponibilidad de datos y tiempo de inferencia | Sección del artículo |
| Manejo de datos con ruido, incompletos y desbalanceados | SMOTE para desbalanceo, imputación por mediana, feature scaling robusto | Pipeline documentado |

**Features del modelo XGBoost:**

| Feature (X) | Fuente | Tipo |
|---|---|---|
| Prevalencia Salmonella por canal | V2.md | Numérica (%) |
| Densidad ganadera estatal | SIAP/SADER | Numérica (cabezas/km²) |
| Clausuras COFEPRIS por estado | PNT (Selenium) | Conteo |
| % Resistencia antimicrobiana (ampicilina) | PUCRA | Numérica (%) |
| Volumen de faenamiento | SIAP | Numérica (toneladas) |
| **Target (y)** | **Casos CIE-10 A05 por estado/año** | **SINAIS/DGE** |

**Hallazgo Potencial:**
> *"El modelo XGBoost alcanza un AUC-ROC de 0.87 en la predicción de brotes de intoxicación alimentaria (A05). Las 3 features más importantes (SHAP values) son: (1) volumen de faenamiento estatal, (2) número de clausuras COFEPRIS, y (3) prevalencia de Salmonella en mercados municipales. Esto confirma que la bioseguridad en rastros — no el consumo per cápita — es el driver principal del riesgo."*

---

### 4. 🗄️ Bases de Datos NoSQL

**Incidente Crítico:** *"Crisis en la escalabilidad: Posible brote de fiebre aftosa"*

| Requisito del PP | Nuestra Implementación | Entregable |
|---|---|---|
| Selección del tipo de BDD NoSQL | **MongoDB (Documentos)** — Ideal para datos heterogéneos: CSVs estructurados + PDFs semi-estructurados + actas de clausura en texto libre | Justificación técnica |
| Modelado de datos NoSQL | Star Schema adaptado a colecciones: dimensiones como documentos referenciados, hechos como documentos embebidos | Diagrama de colecciones |
| Escalabilidad ante crisis | Simulación: ¿Qué pasa si entran 10,000 registros/hora durante un brote? MongoDB con sharding horizontal | Análisis de carga |

**Estructura de Colecciones MongoDB:**

```
ganado_saludable_db/
├── dim_geografia          # { estado_id, nombre, region, es_frontera }
├── dim_tiempo             # { fecha, año, trimestre, mes }
├── dim_patogeno           # { nombre, tipo, gen_resistencia }
├── fact_hatos_tb          # { estado_id, fecha_id, num_hatos_libres, ... }
├── fact_morbilidad_humana # { estado_id, fecha_id, cie10, num_casos, ... }
├── fact_clausuras         # { establecimiento, motivo, agente_detectado, ... }
└── fact_ram               # { bacteria, antibiotico, pct_resistencia, ... }
```

**Hallazgo Potencial:**
> *"La migración del Star Schema relacional a MongoDB redujo el tiempo de consulta de cruces geográficos (estado → hatos → casos humanos) de 4.2s a 0.3s gracias al embedding de dimensiones frecuentes. Sin embargo, las consultas ad-hoc de texto libre sobre actas de clausura COFEPRIS solo son viables con índices de texto completo ($text search), validando que NoSQL no es 'mejor' que SQL, sino complementario."*

---

### 5. 📐 Ecuaciones Diferenciales Aplicadas

**Incidente Crítico:** *"Modelación de la propagación de enfermedades mediante ecuaciones diferenciales"*

| Requisito del PP | Nuestra Implementación | Entregable |
|---|---|---|
| Formulación del modelo SIR | Sistema de 3 EDOs operando en **modo dual**: calibración TB + simulación FMD | Ecuaciones + código |
| Análisis e interpretación de resultados | Curvas S(t), I(t), R(t) bajo 6 escenarios de β y γ (3 TB + 3 FMD) | Gráficas de fase |
| Representación gráfica del sistema | Evolución temporal + diagramas de fase (S vs I) + **gráfica comparativa TB vs FMD** | Matplotlib/Plotly |
| Métodos numéricos | `scipy.integrate.odeint` (Runge-Kutta adaptivo) | Código documentado |
| Estrategias de control | Simulación de vacunación, cuarentena y sacrificio masivo → efecto en las curvas | Gráficas comparativas |

**El Modelo SIR Dual (TB Calibración → FMD Simulación):**

```
dS/dt = -β × S × I / N          (Susceptibles que se infectan)
dI/dt =  β × S × I / N  - γ × I  (Nuevos infectados - recuperados)
dR/dt =  γ × I                    (Infectados que se recuperan)

Donde:
  N   = 35,100,000 (biomasa bovina total, V2.md)
  β   = tasa de transmisión
  γ   = tasa de recuperación (inverso del período infeccioso)
  R0  = β / γ (número reproductivo básico)

── MODO 1: CALIBRACIÓN (TB Bovina) ──────────────
  R0_tb  ≈ 1.5 – 2.0  (calibrado con cuarentenas SENASICA 2024)
  γ_tb   ≈ 1/180 días (período infeccioso ~6 meses)
  β_tb   = R0_tb × γ_tb

── MODO 2: SIMULACIÓN (Fiebre Aftosa) ──────────
  R0_fmd ≈ 4.0 – 8.0  (literatura: UK 2001, Tildesley et al.)
  γ_fmd  ≈ 1/14 días  (período infeccioso ~2 semanas)
  β_fmd  = R0_fmd × γ_fmd
  Factor de transferencia: β_fmd / β_tb ≈ 3.3x – 5x
```

**Los 6 Escenarios a Simular:**

| # | Enfermedad | Escenario | R0 | Pregunta |
|---|---|---|---|---|
| 1 | TB Bovina | Sin intervención | 1.8 | ¿Cuántos hatos se infectan en 1 año? (Validación vs datos reales SENASICA) |
| 2 | TB Bovina | Con vacunación | <1.0 | ¿Cuánto debe reducirse β para control? |
| 3 | TB Bovina | Con cuarentena estatal | 1.8→0.9 | Efecto de aislar Chihuahua/Durango |
| 4 | **FMD** | **Sin intervención** | **6.0** | **¿Cuántos días hasta infectar >50% del hato nacional?** |
| 5 | **FMD** | **Con cuarentena + sacrificio** | **6.0→2.0** | **¿Es suficiente la capacidad de respuesta de los manuales CPA?** |
| 6 | **FMD** | **Escenario UK 2001 en México** | **8.0** | **¿Cuántas cabezas se sacrificarían? ¿Cuál es el costo?** |

**Hallazgo Potencial:**
> *"La simulación SIR dual revela un contraste brutal: con R0_tb = 1.8, la tuberculosis bovina infecta 12% del hato nacional en 5 años (progresión lenta, manejable). Con R0_fmd = 6.0, la fiebre aftosa infectaría el 80% del hato en apenas 45 días. Los manuales CPA de SENASICA asumen que pueden activar brigadas de sacrificio en 72 horas — pero la simulación muestra que para ese momento, el virus ya habría cruzado 8 estados por transmisión aerosol. La brecha entre la velocidad del virus y la velocidad del gobierno es el verdadero riesgo."*

---

### 6. 💰 Finanzas Corporativas

**Incidente Crítico:** *"Subestimación de costos y mala evaluación del riesgo financiero"*

| Requisito del PP | Nuestra Implementación | Entregable |
|---|---|---|
| Costo total del proyecto | Presupuesto del sistema IoT + pipeline de datos + licencias | Tabla de costos |
| Beneficio económico estimado | Ahorro por detección temprana (evitar despoblaciones de 1,951 cabezas/brote) | Proyección a 5 años |
| Retorno de inversión (ROI) | `ROI = (Beneficio Neto / Inversión Inicial) × 100` | Cálculo con datos reales |
| Valor Presente Neto (VPN) | Flujos de ahorro descontados a tasa TIIE + prima de riesgo | Análisis NPV |
| Razones financieras (Rentabilidad, Apalancamiento, Liquidez) | Análisis DuPont aplicado a la empresa ganadera modelo "Carnes Selectas Mexicanas" | Tabla de razones |
| Regresión predictiva | Modelo de regresión: gasto veterinario ~ f(prevalencia, densidad, clima) | Coeficientes + R² |

**Modelo Financiero de Prevención vs. Reacción (Dual: TB crónico + FMD catastrófico):**

| Escenario | Costo Estimado |
|---|---|
| **TB Reactivo:** Despoblación de 1 brote (endémico) | ~$39M MXN (1,951 × 1.0 UA × $20,000/UA × 100%) |
| **FMD Catastrófico:** Brote masivo (referencia UK 2001) | **~$200B MXN** (sacrificio masivo + embargo comercial + desempleo rural) |
| **Preventivo (IoT + IA):** Sistema de monitoreo anual | ~$5M MXN (hardware + cloud + mantenimiento) |
| **Ahorro neto por brote TB evitado** | ~$34M MXN |
| **Ahorro neto si FMD se detecta 48h antes** | **Potencialmente miles de millones** (contención antes de salto inter-estatal) |
| **ROI del primer año (TB)** | ~680% (si se evita un solo brote) |

**Hallazgo Potencial:**
> *"El análisis VPN a 5 años con tasa de descuento del 12% muestra que el sistema de detección temprana genera un valor presente neto de $127M MXN para brotes de TB endémica. Pero el verdadero valor del sistema está en el escenario de FMD: si el sistema de monitoreo IoT con IA detectara un caso sospechoso de fiebre aftosa 48 horas antes que la inspección visual tradicional, el modelo SIR muestra que esas 48 horas son la diferencia entre contener el brote en 1 estado ($2B MXN) o perder el control nacional ($200B MXN). La inversión de $5M/año se justifica solo con la probabilidad >0.1% de un evento FMD."*

---

### 7. 🌍 Laboratorio de Innovación Social

**Incidente Crítico:** *"Diagnóstico e innovación para una empresa cárnica en crisis"*

| Requisito del PP | Nuestra Implementación | Entregable |
|---|---|---|
| Diferencias entre innovación tecnológica, empresarial y social | La detección temprana es innovación tecnológica; la transparencia de datos es innovación social | Sección del artículo |
| Problemas sociales complejos y enfoque sistémico | **One Health como framework sistémico:** la bioseguridad no es un problema de veterinarios, es un problema de salud pública, economía y justicia social | Diagrama sistémico |
| Identificación de necesidades y actores | Mapa de stakeholders: ganaderos, SENASICA, COFEPRIS, hospitales, consumidores, comunidades rurales | Mapa de actores |
| Impacto en poblaciones vulnerables | La falta de bioseguridad castiga desproporcionadamente a: trabajadores de rastro, comunidades inmunodeprimidas (VIH + M. bovis), y consumidores de tianguis | Análisis de inequidad |

**Hallazgo Potencial:**
> *"El cruce de datos SENASICA × SINAIS × CONEVAL revela que los 5 estados con mayor prevalencia de TB bovina (Chihuahua, Durango, Jalisco, Veracruz, Chiapas) coinciden con estados de alta marginación rural. La probabilidad de morir por tuberculosis zoonótica es 3.2x mayor si el paciente vive en un municipio donde el 60%+ de la carne se comercializa en tianguis. La innovación social no es poner sensores en las vacas — es hacer visibles las cadenas de transmisión que el sistema de salud fragmentado oculta."*

---

## 🏗️ Arquitectura Técnica

```
                    ┌────────────────────────────────────┐
                    │     FUENTES GUBERNAMENTALES         │
                    │  SENASICA · SINAIS · PNT · DGE     │
                    │  openFMD · PUCRA/UNAM               │
                    └───────────────┬────────────────────┘
                                    │
                    ┌───────────────▼────────────────────┐
                    │       MÓDULO DE EXTRACCIÓN          │
                    │  API Intercept · ViewState Bypass   │
                    │  CSV Download · Selenium · Camelot  │
                    │  + Data Lineage (metadatos ETL)     │
                    └───────────────┬────────────────────┘
                                    │
                    ┌───────────────▼────────────────────┐
                    │       DATA WAREHOUSE (MongoDB)      │
                    │  Star Schema: 6 dims + 7 facts     │
                    │  Pydantic validation · NoSQL store  │
                    └───────────────┬────────────────────┘
                                    │
                    ┌───────────────▼────────────────────┐
                    │       MODELOS ANALÍTICOS            │
                    │  SIR (EDOs) · XGBoost · Chronos    │
                    │  Financial ROI · Multivariada       │
                    └───────────────┬────────────────────┘
                                    │
                    ┌───────────────▼────────────────────┐
                    │       CAPA DE SEGURIDAD             │
                    │  César · RSA · SHA-256 · Firmas     │
                    └───────────────┬────────────────────┘
                                    │
                    ┌───────────────▼────────────────────┐
                    │       ENTREGABLES                   │
                    │  📄 Artículo (15-25 págs)           │
                    │  📊 Presentación (Gamma/Genially)   │
                    │  🎤 Coloquio oral                   │
                    └────────────────────────────────────┘
```

---

## 📊 Datos Clave para el Artículo (Cifras de Impacto)

| Indicador | Valor | Fuente |
|---|---|---|
| Biomasa bovina total México | **35.1 millones** de cabezas | V2.md (SIAP) |
| Confinamiento anual | **2.8 millones** cabezas/año | V2.md |
| México libre de FMD desde | **1954** (72 años) | SENASICA/WOAH |
| R0 estimado FMD | **4.0 – 8.0** | Literatura (Tildesley et al.) |
| Costo brote FMD UK 2001 | **~£8B (~$200B MXN)** | DEFRA |
| Animales sacrificados UK 2001 | **>6 millones** | DEFRA |
| R0 estimado TB bovina | **~1.5 – 2.0** | Calibración SENASICA |
| Resistencia a Ampicilina | **94.7%** de Salmonella en carne molida | V2.md (literatura) |
| Prevalencia blaCTX-M (BLEE) | **23.5%** | V2.md (genómica) |
| E. coli O157 pre-evisceración | **90.9%** en hisopados de piel | V2.md |
| Presupuesto campaña TB bovina | **>300M MXN/año** | V2.md (SENASICA) |
| Despoblación máxima registrada | **1,951 cabezas** en un brote (Chihuahua) | V2.md |
| Prevalencia Salmonella en mercados | **22.3%** (vs 1.3% en supermercados) | V2.md |
| Alerta FAO fiebre aftosa | **Enero 2025** — brotes en Europa y Cercano Oriente | FAO 2025 |
| Ciberataques a México (Q1 2025) | **35,200 millones** | PP §Criptografía |

---

## 🚀 Ejecución

```bash
# Clonar e instalar
git clone https://github.com/[tu-repo]/EpidemicResearch.git
cd EpidemicResearch
pip install -r requirements.txt

# Ejecutar extractor SENASICA (validar endpoint)
python -m src.extractors.senasica_tb

# Ejecutar modelo SIR
python -m src.models.sir_prep

# Correr tests
python -m pytest tests/ -v
```

---

## 📚 Referencias Principales

- OMS/FAO/WOAH. (2024). *One Health Joint Plan of Action*.
- FAO. (2025). *La FAO advierte: es necesario incrementar la concienciación y las medidas ante los brotes de fiebre aftosa en Europa y el Cercano Oriente*. https://www.fao.org/newsroom/detail/fao-warns--enhanced-awareness-and-action-needed-amid-foot-and-mouth-disease-outbreaks-in-europe-and-the-near-east/es
- WOAH. (2025). *Fiebre aftosa: gestionar la respuesta en medio del caos durante su resurgimiento*. https://www.woah.org/es/articulo/fiebre-aftosa-gestionar-la-respuesta-en-medio-del-caos-durante-su-resurgimiento/
- Tildesley, M. J. et al. (2006). *Optimal reactive vaccination strategies for a foot-and-mouth disease epidemic*. Nature, 440, 83–86.
- Brauer, F., & Castillo-Chávez, C. (2012). *Mathematical Models in Population Biology and Epidemiology*. Springer.
- Hethcote, H. W. (2000). *The Mathematics of Infectious Diseases*. SIAM Review, 42(4).
- Neethirajan, S. (2020). *The role of sensors, big data and machine learning in modern animal farming*. Sensing and Bio-Sensing Research.
- Wolfert, S. et al. (2017). *Big data in smart farming: A review*. Agricultural Systems.
- Russell, S., & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
- Gitman, L. J., & Zutter, C. J. (2016). *Principios de administración financiera* (14.ª ed.). Pearson.
- Kreyszig, E. (2011). *Advanced Engineering Mathematics* (10th ed.). Wiley.

---

> **"La verdadera innovación no es poner sensores en las vacas. Es hacer visibles las cadenas de transmisión que un sistema de salud fragmentado oculta."**
