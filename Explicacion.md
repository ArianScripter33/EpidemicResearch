# Arquitectura de Datos — Ganado Saludable

> **Principio de Oro:** Cada dato que extraemos tiene que aparecer en un slide o en el artículo. Si no, no lo extraemos.
> Este documento es tu mapa de orientación. Si en algún momento no entiendes "¿para qué sirve X?", la respuesta está aquí.

---

## El Problema Central (Por Qué Todo Esto Existe)

Te asignaron **Fiebre Aftosa (FMD)** como enfermedad de estudio. El problema: **México está libre de FMD desde 1954**. No hay brotes locales, no hay datos mexicanos, no hay series temporales nacionales.

¿Opción A? Inventar datos. Rechazada. Es deshonesto académicamente.

¿Opción B? Usar un **Proxy Epidemiológico**. Esta es la solución.

**La estrategia:** Usamos **Tuberculosis Bovina (TB)** como sustituto de calibración. La TB SÍ existe en México, SENASICA SÍ tiene datos reales, y matemáticamente los modelos son intercambiables — solo cambian los parámetros (`R0`, duración infecciosa). Calibramos el modelo con TB real, luego "apretamos el botón" y simulamos lo que pasaría con FMD.

```
TB real (R0 = 1.8, datos SENASICA) ──calibra──► Modelo SIR
                                                      │
                                              cambia parámetros
                                                      │
FMD simulado (R0 = 6.0, literatura) ◄──simula──── Modelo SIR
```

---

## Mapa Completo: Dato → Modelo → Slide

Esta tabla es el corazón del proyecto. Te dice exactamente qué sirve para qué.

| Fuente de Datos | Vector Extraído | Modelo que lo usa | Slide en Presentación |
|---|---|---|---|
| **SENASICA** | Hatos certificados libres de TB por estado | SIR (calibración) + Mapa | Slide 6 (mapa), Slides 7-8 (SIR) |
| **DGE Anuarios** | Casos humanos TB (A15-A19) por estado | Correlación Cruzada | Slide 5 (puente animal-humano) |
| **DGE Anuarios** | Intoxicaciones alimentarias (A05) por estado | ANOVA | Slide 9 (canales de venta) |
| **Constantes Literatura** | R0_FMD = 6.0, periodo infeccioso = 14 días | SIR (simulación FMD) | Slides 7-8 (el "Money Shot") |
| **Constantes Literatura** | Costos UK 2001: ~$200B MXN | Modelo Financiero | Slide 10 (ROI/VPN) |
| **Constantes Literatura** | Resistencia Ampicilina 94.7% (PUCRA) | ANOVA + XGBoost | Slide 9, Artículo |
| **COFEPRIS Clausuras** | Establecimientos clausurados por Clenbuterol/LMR | XGBoost (feature) | Slide 11 (Proxy de Opacidad) |
| **openFMD / Literatura** | Brotes FMD internacionales, R0 por región | SIR validación, Chronos | Slide 4 (contexto global) |
| **SENASICA PDFs** | Cuarentenas trimestrales 2024 por estado | ANOVA + mapa granular | Artículo (sección resultados) |

---

## Las Fuentes de Datos (De Dónde Viene Todo)

### A. SENASICA — La Fuente Principal

**¿Qué es SENASICA?**
El Servicio Nacional de Sanidad, Inocuidad y Calidad Agroalimentaria. Es la DEA del ganado mexicano — vigila que los animales no estén enfermos antes de llegar al rastro.

**¿Qué datos exactos extraemos?**

1. **Hatos Libres de TB** (`hatos_libres_tuberculosis.csv`)
   - ¿Qué es un "hato"? Una unidad productiva ganadera (una granja básicamente).
   - ¿Qué es "libre"? Certificado oficialmente por SENASICA como sin TB activa.
   - **Columnas clave:** `entidad`, `constancias_emitidas_bovinos_carne`, `total_bovinos_constatados_libres`
   - **Lo que extraímos:** 64 filas — 32 estados × 2 fuentes CSV (los dos CSVs más recientes de SENASICA).

2. **Cuarentenas Trimestrales 2024** (PDFs — extracción con Jules)
   - Reportes PDF por trimestre con số de granjas en cuarentena y animales sacrificados.
   - **Columnas clave:** `estado`, `num_hatos_cuarentena`, `num_animales`, `tipo_medida`

**¿Por qué los hatos libres y no los infectados?**
Porque SENASICA no publica "hatos enfermos" directamente — publican los "libres". La lógica es:

```
Prevalencia_aproximada = 1 - (hatos_libres / hatos_totales)
```

Un estado con pocos hatos libres = alta prevalencia implícita.

---

### B. DGE — El Radar Humano

**¿Qué es la DGE?**
Dirección General de Epidemiología (SSalud). Publica los **Anuarios de Morbilidad** — básicamente el tablero de control de qué enfermedades están afectando a los mexicanos ese año.

**¿Qué datos exactos extraemos?**

Los **Anuarios** son ZIPs que contienen CSVs con miles de filas. Nosotros filtramos por **códigos CIE-10** (el estándar internacional de clasificación de enfermedades):

| Código CIE-10 | Enfermedad | ¿Para qué lo usamos? |
|---|---|---|
| `A15`, `A16` | TB pulmonar y bacteriológica | Correlación con TB animal SENASICA |
| `A17` | TB meníngea | TB total humana |
| `A18`, `A19` | TB de otros órganos | TB total humana |
| `A05` | Intoxicación alimentaria bacteriana | ANOVA por canal de venta |

**Lo que extraímos:** 384 filas (288 de TB + 96 de intoxicaciones) para los años 2015, 2016, 2017.

**¿Por qué solo 2015-2017?**
Esa es la única ventana donde la DGE publicó datos abiertos en formato CSV descargable directamente. De 2018 en adelante migraron a un sistema diferente. Por eso mandamos a Jules a buscar métodos alternativos para años más recientes.

**El "puente" más poderoso del proyecto:**
Cruzar datos de SENASICA (vacas enfermas, por estado) con DGE (humanos enfermos, por estado) para demostrar correlación geográfica. Si Chihuahua tiene alta prevalencia de TB bovina Y alta incidencia de TB humana, eso no es coincidencia — es zoonosis documentable.

---

### C. Constantes de la Literatura

**¿Qué son?**
Parámetros epidemiológicos y económicos validados y publicados en papers científicos peer-reviewed. Están compilados en tu `V2.md` y en el `Protocolo Investigación PDF`.

**¿Por qué esto es crítico?**
Porque hacen que tus modelos funcionen **sin importar si la red cae el día del coloquio**. No dependes de APIs externas para las gráficas más importantes.

**Los parámetros clave:**

```
Biológicos:
  N = 35,100,000       # Biomasa nacional (cabezas de ganado, SIAP)
  R0_TB  = 1.8         # Ritmo Básico de Reproducción — TB Bovina
  R0_FMD = 6.0         # R0 FMD (Tildesley et al., 2006, UK 2001)
  gamma_TB  = 1/180    # Un animal infeccioso por ~6 meses
  gamma_FMD = 1/14     # Un animal infeccioso por ~14 días

Resistencia Antimicrobiana (PUCRA/UNAM):
  ampicilina     = 94.7%   # Salmonella en carne molida
  carbenicilina  = 84.2%
  blaCTX-M (BLEE) = 23.5%

Financieros:
  Costo_UK_2001     = ~$200B MXN       # Brote FMD más costoso documentado
  Sistema_IoT_anual = ~$5M MXN         # Costo del sistema preventivo propuesto
  Tasa_descuento    = 12%              # Para cálculo de VPN
```

---

## Los Modelos (El Motor Científico)

Los datos crudos no impresionan a nadie. La magia está en lo que haces con ellos.

### 1. El Modelo SIR Dual — The Money Shot

**¿Qué es el modelo SIR?**
El modelo epidemiológico más usado en el mundo. Divide toda la población en 3 "cajas" y define reglas matemáticas de cómo los individuos pasan de una a otra:

```
S (Susceptibles) ──β·I──► I (Infectados) ──γ──► R (Recuperados/Removidos)
```

- **S = Susceptibles:** Animales que PUEDEN infectarse (no tienen inmunidad).
- **I = Infectados:** Animales enfermos ACTUALMENTE que contagian.
- **R = Removidos:** Animales que ya no contagian (se recuperaron, murieron, o fueron sacrificados).

**Los parámetros que controlan todo:**
- `beta (β)` = Tasa de contagio. Depende del R0 y de qué tan rápido se recuperan.
- `gamma (γ)` = Tasa de recuperación. = 1 / duración_infecciosa_en_días.
- Relación clave: `R0 = beta / gamma`

**El enfoque "Dual" — por qué es brillante:**

```
MODO 1 — Calibración con TB Bovina (datos REALES mexicanos):
  R0   = 1.8    → enfermedad lenta, curva casi plana
  gamma = 1/180  → un animal es infeccioso 6 meses
  Resultado: Curva suave. Muestra el "estado actual" de México.

MODO 2 — Simulación FMD (escenario de catástrofe):
  R0   = 6.0    → enfermedad explosiva, curva exponencial
  gamma = 1/14   → un animal es infeccioso 14 días
  Resultado: Colapso en semanas. Muestra "lo que podría pasar".
```

**El output visual (Slides 7-8):**
Dos gráficas de `S(t)`, `I(t)`, `R(t)` en el tiempo, lado a lado. La de la izquierda es la TB real, gradual. La de la derecha es el FMD simulado, vertical, catastrófico. Esa comparación visual, sin decir una palabra, justifica toda la inversión en prevención.

**6 escenarios que corremos:**
1. TB sin intervención (¿cuántos hatos se infectan en 5 años?)
2. TB con vacunación (R0 cae a 0.9 — control logrado)
3. TB con cuarentena estatal
4. FMD sin intervención (¿cuántos días hasta 50% infectado?)
5. FMD con cuarentena + sacrificio
6. FMD escenario UK 2001 (R0 = 8.0 — el peor caso)

---

### 2. ANOVA — El Juicio a los Canales de Venta

**¿Qué es ANOVA?**
Análisis de Varianza (Analysis of Variance). Responde a una pregunta específica:
> *"¿La diferencia entre estos grupos es real o es puro ruido estadístico?"*

**El setup:**
Tienes 4 canales de venta de carne, cada uno con una prevalencia conocida de Salmonella:

| Canal de Venta | Prevalencia Salmonella |
|---|---|
| Supermercados | 1.3% |
| Carnicerías | 8.4% |
| Tianguis | 13.6% |
| Mercados Municipales | 22.3% |

**La pregunta:** ¿Es esa diferencia (1.3% vs 22.3%) estadísticamente significativa o podría ser azar?

**El output:** Un `p-value`. Si p < 0.05, hay diferencia real entre canales. Ese número va directo al artículo y a la slide 9 como evidencia dura de que el canal de compra SÍ importa para tu salud.

---

### 3. El Modelo Financiero (ROI/VPN)

**El argumento más poderoso del proyecto no es biológico, es económico.**

La propuesta: implementar un sistema de trazabilidad con IoT y Criptografía cuesta ~$5M MXN/año.

Si no lo implementas y entra un brote de FMD como el UK 2001, el costo es ~$200B MXN (incluyendo comercio perdido, sacrificios, cuarentenas internacionales).

**El VPN (Valor Presente Neto) lo cuantifica:**
```
ROI = (Pérdida_evitada - Costo_sistema) / Costo_sistema
ROI = ($200B - $5M) / $5M = 39,999x
```

Eso no es un número de presentación — es el argumento con el que convences al gobierno de que vale la pena invertir.

---

### 4. Criptografía — El Módulo "One Health Digital"

**¿Por qué está esto en un proyecto de epidemiología?**
Porque es un requisito de la materia de Seguridad de Datos (una de las 7 materias que cubre el proyecto). Pero no es decorativo — tiene justificación real.

**El argumento:** Si usas IoT (sensores en los rastros, GPS en camiones de carne) para rastrear la cadena de frío y los movimientos del ganado, esos datos son **sensibles**. Un productor corrupto que acceda al sistema podría:
- Falsificar registros de temperatura.
- Ocultar el origen de animales enfermos.

**La solución que implementamos:**
- **Cifrado César:** Demo didáctico — desplaza letras N posiciones. Muestra el concepto básico de cifrado simétrico.
- **RSA:** El estándar de criptografía asimétrica real. Clave pública para encriptar, clave privada para desencriptar. Garantiza que solo el rastro autorizado puede leer los datos de identidad del animal.

**Output en el proyecto:** ~100 líneas de Python en `src/crypto/encryption.py` que demuestran ambos algoritmos funcionando.

---

## El Pipeline ELT (Cómo Fluyen los Datos)

```
FUENTES EXTERNAS
      │
      ▼
[EXTRACT] src/extractors/
  ├── senasica_tb.py        → CSV directo → 64 filas
  ├── dge_morbilidad.py     → ZIP → CSV → 384 filas (filtradas A05, A15-A19)
  ├── openfmd.py            → Intentos de API → fallback literatura
  └── (Jules) cofepris.py   → COFEPRIS clausuras (pendiente)
      │
      ▼
[LOAD] data/raw/            ← Datos crudos, sin tocar
      │
      ▼
[TRANSFORM] src/models/ y src/warehouse/
  ├── Normalización de nombres de estados
  ├── Injección de metadatos (fecha_etl, fuente_origen, version_etl)
  ├── Esquema estrella Pydantic (para MongoDB)
  └── Cálculo de prevalencias derivadas
      │
      ▼
[OUTPUT] data/processed/    ← Datos limpios listos para modelos
      │
      ▼
[MODELS]
  ├── SIR Dual (scipy.odeint)
  ├── ANOVA (scipy.stats.f_oneway)
  ├── ROI/VPN (cálculo financiero)
  └── Mapa Coroplético (plotly.express)
      │
      ▼
[SLIDES + ARTÍCULO]
  ├── Slide 6:  Mapa México por estado (datos SENASICA)
  ├── Slides 7-8: Curvas SIR TB vs FMD (The Money Shot)
  ├── Slide 9:  ANOVA canales de venta
  ├── Slide 10: Tabla ROI financiero
  └── Slide 11: Proxy de Opacidad (COFEPRIS + XGBoost)
```

---

## El Proxy de Opacidad — La Contribución Original del Proyecto

**¿Qué es?**
Una metodología inventada en este proyecto para medir indirectamente el abuso de antibióticos en la industria cárnica.

**El problema:** No hay datos públicos de "granjas que abusan de antibióticos". Es información que nadie reporta voluntariamente.

**La solución:** Usar las **clausuras de COFEPRIS** como proxy (indicador indirecto).

**La lógica (que va explícita en el artículo):**
1. El Clenbuterol es un anabólico ilegal fácil de detectar en pruebas de laboratorio.
2. COFEPRIS clausura establecimientos cuando lo detecta — eso SÍ es dato público.
3. Un productor dispuesto a inyectar Clenbuterol (riesgo legal alto, ganancia marginal) tiene alta probabilidad de también ignorar los tiempos de retiro de antibióticos (riesgo difícil de detectar, ganancia comparable).
4. **Resultado:** Las clausuras por Clenbuterol se convierten en un feature de XGBoost para predecir riesgo de residuos antibióticos por zona geográfica.

Mides A (Clenbuterol detectado) para inferir B (Abuso de antibióticos no detectado).

---

## La Anatomía de los Archivos `.md` del Proyecto

No son simples notas. Cada uno tiene un rol específico en la arquitectura del conocimiento:

| Archivo | Rol | Qué contiene |
|---|---|---|
| `M_doc.md` | **Source of Truth de Extracción** | 24 URLs verificadas, pseudocódigo de extracción, estrategias de fallback |
| `V2.md` | **Libro de Constantes** | R0, gamma, biomasa, prevalencias, resistencias — todos los números que no cambian |
| `implementation_plan.md` | **La Tubería (Pipeline)** | Arquitectura del ELT, esquema estrella MongoDB, dependencias técnicas |
| `presentation_script.md` | **El Destino Final** | Guión narrativo del coloquio, 4 actos, cada slide con su argumento |
| `mvp_strategy.md` | **El Anti-Overengineering** | Qué SÍ construir (Tier 1), qué es nice-to-have (Tier 2-3), regla de oro |
| `data_acquisition_plan.md` | **El Plan de Batalla de Datos** | Wave 1-3, ROI por fuente, árbol de decisión si una fuente falla |
| `Explicacion.md` | **Este archivo** | Mapa de orientación para entender el proyecto completo |

---

## Las Jules Issues — Por Qué las Mandamos

**¿Qué es Jules?**
Un agente de IA asíncrono de Google que corre en máquinas GCP efímeras, navega la web, escribe código y abre Pull Requests directamente en tu repositorio.

**¿Por qué lo usamos en lugar de hacerlo nosotros?**
Intentamos extraer datos de la DGE y openFMD con un navegador interno — el proceso fue lento, bloqueado por JavaScript y por endpoints que cambian sus URLs dinámicamente. Delegamos esas tareas "hostiles" a Jules y en paralelo seguimos construyendo el código del proyecto.

**Los 4 issues que lanzamos (en `docs/jules_issues/`):**

| Issue | Misión | Por qué importa |
|---|---|---|
| `issue_01_dge_2018_2024.md` | Encontrar CSVs de morbilidad DGE para años 2018-2024 | Tenemos solo 2015-2017, necesitamos más años para el análisis de tendencia |
| `issue_02_openfmd_kaggle.md` | Encontrar la URL real de descarga CSV de openFMD + Kaggle FMD dataset | Datos reales de brotes FMD internacionales para validar R0 |
| `issue_03_cofepris_pucra.md` | Clausuras COFEPRIS (CSV/PDF) + Tablas RAM de PDFs del PUCRA/UNAM | El Proxy de Opacidad + validar constantes de resistencia antimicrobiana |
| `issue_04_senasica_cuarentenas.md` | Parsear PDFs trimestrales de cuarentenas SENASICA 2023-2024 | Datos granulares de despoblaciones para calibrar el SIR con más fidelidad |

Cada issue tiene: contexto completo del proyecto, Google Dorks de búsqueda específicos, estrategias de fallback, y el schema exacto del archivo de salida que Jules debe generar.