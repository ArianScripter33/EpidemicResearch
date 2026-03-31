# Data Acquisition Plan — Ganado Saludable MVP

> **Objetivo:** Obtener los datos con máximo retorno para la presentación (10-15 min, ~15-20 slides).
> **Principio:** Más datos = mejores insights, pero priorizamos por impacto directo en entregables.
> **Fecha:** 2026-03-31

---

## Estado Actual del Proyecto

**Phase 0 (Documentación):** ✅ 100% completa (~1,900 líneas de docs)
**Phase 1-7 (Ejecución):** ❌ 0% — cero código, cero datos, cero estructura

**Brecha crítica:** Ratio planning/execution = ∞. Es momento de invertirla.

---

## Diagnóstico de Fuentes de Datos (ROI por Slide)

### 🟥 WAVE 1 — Ship or Die (Alto ROI, endpoints estables)

| # | Fuente | URL | Formato | Qué alimenta | Slides |
|---|--------|-----|---------|---------------|--------|
| 1 | **SENASICA Hatos Libres TB** | `repodatos.atdt.gob.mx/.../hatos_libres_tuberculosis.csv` | CSV | SIR calibración + Mapa coroplético | 6, 7-8 |
| 2 | **DGE Anuarios Morbilidad** | `epidemiologia.salud.gob.mx/anuario/datos_abiertos/Anuario_{year}.zip` | ZIP→CSV | ANOVA + EDA + correlación TB animal↔humano | 9 |
| 3 | **Constantes de literatura** | V2.md + README.md (ya documentadas) | In-memory | SIR FMD (R0=6.0), ANOVA (prevalencias), Tabla financiera | 7-8, 9, 10 |

**¿Por qué Wave 1 primero?**
- El SIR Dual es THE MONEY SHOT (slides 7-8). Puede funcionar SOLO con constantes de literatura, pero calibrarlo con datos reales SENASICA lo hace 10x más creíble.
- El mapa coroplético (slide 6) necesita datos por estado → SENASICA CSV.
- El ANOVA (slide 9) puede correr con las prevalencias de V2.md (1.3% vs 22.3%) sin extracción, pero datos DGE añaden solidez.

**Fallback si Wave 1 falla:**
- SENASICA CSV → Usar constantes R0 de literatura directamente (Tildesley et al.)
- DGE Anuarios → Usar las cifras de V2.md para ANOVA (ya tenemos los 4 canales con prevalencias)

---

### 🟨 WAVE 2 — Enrich (Medio ROI, refuerza narrativa)

| # | Fuente | URL | Formato | Qué alimenta | Prioridad |
|---|--------|-----|---------|---------------|-----------|
| 4 | **openFMD CSV** | `openfmd.org/dashboard/fmdwatch/` (download button) | CSV | Series FMD internacionales → valida R0 → Chronos (Tier 2) | Alta |
| 5 | **SIAP/SADER** | Datos abiertos de producción pecuaria | CSV | Densidad ganadera por estado → choropleth + features XGBoost | Media |
| 6 | **PUCRA PDFs** | `puiree.cic.unam.mx/divulgacion/docs/pucra2024.pdf` | PDF→tablas | Tablas RAM → narrativa de resistencia antimicrobiana | Media |
| 7 | **WAHIS/WOAH** | `github.com/loicleray/WOAH_WAHIS.ReportRetriever` | API→CSV | Datos FMD contemporáneos Sudamérica | Baja |

**¿Cuándo ejecutar Wave 2?**
- Solo si Wave 1 está completa y los datos son insuficientes para la narrativa.
- openFMD es el de mayor ROI de Wave 2: le da profundidad internacional al proyecto.
- PUCRA es valioso narrativamente (94.7% resistencia ampicilina) pero los datos clave ya están en V2.md.

**Fallback si Wave 2 falla:**
- openFMD → Usar parámetros R0 de papers publicados (ya documentados en README)
- SIAP → Usar datos censales generales de biomasa (35.1M cabezas, V2.md)
- PUCRA → Las cifras de V2.md cubren el requisito narrativo

---

### 🟦 WAVE 3 — Flex Mode (Bajo ROI para MVP, alto riesgo técnico)

| # | Fuente | Método | Riesgo | Qué alimenta |
|---|--------|--------|--------|---------------|
| 8 | **SINAIS Cubos** | ViewState bypass (POST) | Alto — ActiveX/OWC11 | Validación cruzada DGE |
| 9 | **PNT/COFEPRIS** | Selenium headless | Alto — JS dinámico, CAPTCHAs | Proxy de Opacidad (clembuterol) |
| 10 | **Cuarentenas TB PDFs** | camelot/tabula (PDF parsing) | Medio — tablas escaneadas | Datos granulares de despoblación |

**Regla de oro Wave 3:** Solo si te sobran >3 días antes de la entrega Y las Waves 1-2 están completas.

---

## Plan de Ejecución: Scripts a Construir

### Bloque 0: Foundation (15 min)

```
Crear:
├── src/__init__.py
├── src/config.py          # URLs + constantes biológicas/financieras
├── src/base_extractor.py  # ABC con lineage metadata
├── requirements.txt       # Dependencias mínimas
├── data/raw/              # Datos crudos (gitignored)
└── data/processed/        # Datos limpios
```

**`requirements.txt` mínimo:**
```
pandas>=2.0
requests>=2.31
scipy>=1.11
matplotlib>=3.8
plotly>=5.18
pydantic>=2.0
```

**`src/config.py` contendrá:**
- Todas las URLs de M_doc.md refs [1]-[24]
- Constantes biológicas de V2.md (N_BIOMASA, R0_TB, R0_FMD, etc.)
- Constantes financieras (costos UK 2001, indemnizaciones)
- Prevalencias por canal (supermercados 1.3%, mercados 22.3%, etc.)

### Bloque 1: Wave 1 Extractors (1 hora)

**Script 1: `src/extractors/senasica_tb.py`**
- Download CSV directo desde `repodatos.atdt.gob.mx`
- Parse columnas: estado, tipo_produccion, num_hatos_libres
- Normalización de nombres de estados
- Guardar en `data/raw/senasica_hatos_libres.csv`
- Calcular: prevalencia_aproximada = 1 - (hatos_libres / hatos_totales)

**Script 2: `src/extractors/dge_morbilidad.py`**
- Download ZIPs de anuarios (2015-2022)
- Unzip → parse CSV con encoding `latin1`
- Filtrar por CIE-10: A15-A19 (TB), A05 (intoxicaciones alimentarias)
- Agregar por estado y año
- Guardar en `data/raw/dge_morbilidad_{year}.csv`

**Script 3: `src/extractors/openfmd.py`** (si Wave 1 exitosa, arrancamos)
- Navegar a openFMD dashboard y descargar CSV
- Parse: país, fecha, casos, serotipo
- Filtrar Americas
- Guardar en `data/raw/openfmd_americas.csv`

### Bloque 2: Core MVP Models (pueden correr en paralelo - 1.5 horas)

**Script 4: `src/models/sir_dual.py`** — LA PIEZA CENTRAL
- Implementar sistema SIR con scipy.odeint
- Modo 1: TB (R0≈1.8, γ=1/180)
- Modo 2: FMD (R0≈6.0, γ=1/14)
- 6 escenarios paramétricos
- Output: DataFrames S(t), I(t), R(t) + gráficas matplotlib

**Script 5: `src/models/stats_multivariate.py`**
- ANOVA de 4 canales de venta (scipy.stats.f_oneway)
- Si hay datos suficientes: PCA + scree plot
- Output: p-value, test statistic, interpretación

**Script 6: `src/models/financial_roi.py`**
- VPN comparativo: preventivo $5M vs reactivo $39M (TB) / $200B (FMD)
- ROI del primer año
- Output: tabla formateada para el artículo

**Script 7: `src/crypto/encryption.py`**
- César: encrypt/decrypt con desplazamiento n
- RSA: keygen, encrypt, decrypt (simplificado para demo)
- ~100 líneas

### Bloque 3: Visualización MVP (1 hora)

**Script 8: `src/visualization/choropleth_maps.py`**
- Mapa de México por estado con plotly.express
- Variable: prevalencia TB (datos SENASICA)
- GeoJSON de estados mexicanos

**Script 9: `src/visualization/sir_plots.py`**
- Curvas S(t), I(t), R(t) lado a lado: TB vs FMD
- Diagramas de fase
- THE MONEY SHOT para slides 7-8

---

## Estrategia de Datos Escasos

> Si una fuente no tiene datos suficientes, aquí está el árbol de decisión:

```
¿SENASICA CSV disponible?
├── Sí → Usar para calibrar SIR + choropleth
└── No → ¿API oculta funciona?
    ├── Sí → Usar JSON como fallback
    └── No → Usar constantes de literatura (R0=1.8 de papers)
              El SIR funciona SIN datos mexicanos reales.

¿DGE Anuarios descargables?
├── Sí → Filtrar CIE-10, agregar por estado
└── No → ¿Otro año disponible?
    ├── Sí → Usar ese año
    └── No → ANOVA con datos de V2.md (prevalencias hardcodeadas)
              Los 4 canales ya tienen valores publicados.

¿openFMD CSV disponible?
├── Sí → Enriquecer series temporales + validar R0
└── No → Usar R0 de Tildesley et al. directamente.
          El modelo SIR no depende de datos raw de FMD.

¿Datos insuficientes para XGBoost?
├── Sí → Degradar a Regresión Lineal Múltiple (funciona con 32 obs = estados)
└── No → Entrenar XGBoost + SHAP values (Tier 2)
```

**Principio:** Ningún componente MVP debe bloquearse por falta de datos. Cada uno tiene un fallback que funciona con las constantes ya documentadas.

---

## Orden de Ejecución Recomendado (Hoy)

1. ✅ **Foundation** → config.py, requirements.txt, estructura
2. ✅ **SENASICA extractor** → probar endpoint, descargar datos
3. ✅ **DGE extractor** → probar endpoint, descargar anuarios
4. ✅ **SIR Dual Model** → implementar con constantes (no depende de extractores)
5. ✅ **Choropleth** → si SENASICA da datos
6. ✅ **ANOVA** → con datos V2.md o DGE
7. ✅ **Crypto module** → independiente
8. ✅ **Financial table** → con constantes

> **Meta del día:** Tener los extractores Wave 1 corriendo + SIR Dual generando gráficas.
> Con eso tienes el 60% del MVP funcional.
