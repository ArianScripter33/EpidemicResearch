# Wave 2 Recovery Plan — Agent-Assisted Data Extraction

> **Fecha:** 2026-04-02
> **Contexto:** Post-Jules audit. Evaluación de calidad + plan de recuperación con agente web-capable.
> **Objetivo:** Maximizar filas de datos reales extraídas antes de pasar a modelado (Phase 4).

---

## 1. Auditoría de Calidad: Resultados de Jules (4 Issues)

### Scorecard General

| Issue | Tarea | Resultado | Calidad | Filas | Veredicto |
|-------|-------|-----------|---------|-------|-----------|
| #4 | SENASICA Cuarentenas PDF + API | ✅ Éxito total | 🟢 Excelente | 108 | Dual-mode parser (tabla + regex fallback). API cerrada documentada. |
| #3 | COFEPRIS Clausuras + PUCRA RAM | ⚠️ Parcial | 🟡 Bueno | 2 (COFEPRIS) + 0 (PUCRA timeout) | COFEPRIS filtró correctamente. PUCRA bloqueado por timeout UNAM. |
| #1 | DGE Morbilidad 2018-2024 | ❌ Bloqueado | 🟢 Bien documentado | 0 | Investigación exhaustiva. CSVs no existen post-2017. PDFs sí disponibles. |
| #2 | openFMD + Kaggle FMD | ⚠️ Parcial | 🟡 Bueno | 0 (Kaggle needs creds) + 6 (literatura) | Shiny WebSocket bloqueó descarga. Kaggle extractor listo pero sin API key. WAHIS deprecated. |

### Calificación Global: **7/10**

**Lo bueno:**
- Arquitectura impecable (herencia de BaseExtractor, logging, retry, lineage metadata)
- Documentación de vías muertas (API 404, WAHIS Cloudflare, DGE sin CSVs)
- Scripts reutilizables y resilientes

**Lo mejorable:**
- Jules NO puede navegar la web como un browser real (no tiene Playwright/Selenium en su sandbox)
- No intentó parsear los PDFs de la DGE 2018-2024 (se rindió al no encontrar CSVs)
- PUCRA falló por timeout sin fallback local

---

## 2. Brechas Recuperables (Qué nos falta y cómo atacarlo)

### 🔴 BRECHA 1: DGE Morbilidad 2018-2024 (ALTA PRIORIDAD)

**Estado actual:** 0 filas. Solo tenemos 2015-2017 (384 filas).

**Por qué importa:** Con 7 años más de datos (2018-2024), el ANOVA y la correlación TB animal↔humano pasan de "interesante" a "estadísticamente irrefutable". Es la diferencia entre 3 puntos de datos y 10 puntos en una regresión temporal.

**URLs verificadas de los PDFs (Jules las confirmó):**
```
https://epidemiologia.salud.gob.mx/anuario/{year}/morbilidad/nacional/distribucion_casos_nuevos_enfermedad_fuente_notificacion.pdf
https://epidemiologia.salud.gob.mx/anuario/{year}/morbilidad/nacional/distribucion_casos_nuevos_enfermedad_grupo_edad.pdf
```
Donde `{year}` = 2018, 2019, 2020, 2021, 2022, 2023, 2024

**Estrategia de recuperación:**

1. **Docling/Marker → Markdown:** Convertir cada PDF a Markdown estructurado
   - `pip install docling` o `pip install marker-pdf`
   - Ambas librerías preservan estructura de tablas
   - Output: archivos `.md` con tablas en formato Markdown

2. **Exploración con head/tail:** Una vez en Markdown, hacer `grep -i "tuberculosis\|A15\|A16\|A17\|A18\|A19\|A05"` para localizar las filas relevantes

3. **Script de extracción:** Diseñar un parser que:
   - Abra cada `.md` convertido
   - Identifique las tablas de morbilidad por estado
   - Filtre por códigos CIE-10: A15-A19 (TB), A05 (intoxicaciones)
   - Normalice nombres de estados con `ESTADOS_MEXICO` de `config.py`
   - Genere CSV con columnas: `estado, year, cie10, casos_totales, tasa_por_100k`

4. **Alternativa LLM Vision:** Si docling no parsea bien las tablas:
   - Subir las páginas relevantes del PDF a un LLM con visión
   - Pedirle que extraiga la tabla en formato CSV
   - Validar con cross-check manual de 2-3 estados

**Archivos relevantes:**
- `src/extractors/dge_2018_2024.py` — Placeholder actual, reemplazar con parser real
- `src/extractors/dge_morbilidad.py` — Extractor funcional 2015-2017 (usar como template)
- `src/config.py` — CIE10_TARGET_ALL, DGE_ANUARIO_URL_TEMPLATE
- `docs/DGE_DATA_SEARCH.md` — Investigación completa de Jules

---

### 🟡 BRECHA 2: PUCRA RAM (MEDIA PRIORIDAD)

**Estado actual:** Script listo (`pucra_ram.py`), pero servidores UNAM timeout.

**Por qué importa:** Validar que nuestras constantes hardcodeadas (94.7% resistencia Ampicilina) coinciden con los reportes PDF oficiales. Fortalece la sección de RAM del artículo.

**Estrategia de recuperación:**

1. **Retry con agente web:** El agente navega a `https://puiree.cic.unam.mx/divulgacion/` y descarga los PDFs manualmente
2. **Docling → tablas:** Convertir `pucra2024.pdf` o `pucra2025.pdf` a Markdown
3. **Fuzzy matching:** Buscar "Ampicilina", "E. coli", "Salmonella", "Klebsiella" en el Markdown
4. **Extraer porcentajes:** Regex `\d+\.?\d*%` cerca de las keywords
5. **Cross-validate:** Comparar valores extraídos con `RESISTENCIA_AMPICILINA = 0.947` en `config.py`

**Archivos relevantes:**
- `src/extractors/pucra_ram.py` — Extractor existente (ya tiene lógica de cross-validation)
- `src/config.py` — Constantes RAM (líneas 121-128)

---

### 🟡 BRECHA 3: openFMD Real Data (MEDIA PRIORIDAD)

**Estado actual:** 6 filas de literatura (hardcodeadas). Shiny dashboard bloqueó descarga automática.

**Por qué importa:** Datos reales de brotes FMD por país/fecha darían profundidad internacional al proyecto. Alimentaría Chronos time-series (Tier 2).

**Estrategia de recuperación:**

1. **Agente web con browser real:** Navegar a `https://openfmd.org/dashboard/fmdwatch/`
   - Interactuar con el dashboard Shiny
   - Seleccionar filtros (Americas, 2020-2025)
   - Hacer click en "Download CSV"
   - Capturar el blob descargado

2. **Alternativa Kaggle:** Configurar `~/.kaggle/kaggle.json` y ejecutar `kaggle_fmd.py`
   - Dataset: `wasimfaraz/fmd-cattle-dataset`
   - El extractor ya está listo, solo necesita credenciales

3. **WAHIS Manual Export:** El agente navega a `https://wahis.woah.org/#/dashboards/qd-dashboard`
   - Filtra por "Foot and mouth disease"
   - Exporta CSV manualmente (Cloudflare permite browsers reales)

**Archivos relevantes:**
- `src/extractors/openfmd.py` — Extractor con 3 fallbacks
- `src/extractors/kaggle_fmd.py` — Listo, necesita API key
- `src/config.py` — OPENFMD_DASHBOARD, KAGGLE_FMD_DATASET

---

### 🟢 BRECHA 4: COFEPRIS Clausuras Expandidas (BAJA PRIORIDAD)

**Estado actual:** 2 filas ultra-filtradas. Suficiente para el proxy, pero más datos = mejor feature engineering.

**Estrategia de recuperación:**

1. **Expandir keywords:** Añadir "ANTIBIOTICO", "PENICILINA", "TETRACICLINA", "AVICOLA" al filtro
2. **Más años:** Buscar reportes 2019-2023 en `https://www.gob.mx/cofepris/documentos/`
3. **Agente web:** Navegar la página de COFEPRIS que tiene JS rendering y encontrar más PDFs

**Archivos relevantes:**
- `src/extractors/cofepris_clausuras.py` — Extractor funcional

---

## 3. Herramientas para PDF → Datos Tabulares

### Pipeline Propuesto: PDF → MD → CSV

```
PDF (gobierno)
    │
    ├── docling (IBM) ──→ Markdown con tablas preservadas
    ├── marker-pdf ──────→ Markdown con layout detection (ML-based)
    ├── pdfplumber ──────→ Tablas directas (ya lo usamos)
    │
    ▼
Markdown / JSON estructurado
    │
    ├── grep / fuzzy search ──→ Localizar filas por keyword
    ├── pandas.read_csv(StringIO) → DataFrame
    ├── LLM Vision (si tabla rota) → CSV text output
    │
    ▼
CSV limpio → data/processed/
```

### Comparativa de Herramientas

| Herramienta | Fortaleza | Debilidad | Usar para |
|-------------|-----------|-----------|-----------|
| `docling` | Preserva estructura, tablas complejas | Pesado (IBM Watson deps) | DGE PDFs (tablas multi-página) |
| `marker-pdf` | ML-based layout detection, rápido | Menos preciso en tablas gubernamentales | PUCRA PDFs |
| `pdfplumber` | Ya lo usamos, ligero | Falla con tablas rotadas o merged cells | COFEPRIS (ya funciona) |
| `camelot` | Excelente para tablas con líneas | Requiere Ghostscript | Alternativa a pdfplumber |
| LLM Vision | Entiende contexto, fuzzy matching | Rate limits, costo, alucinaciones numéricas | Validación / tablas imposibles |

---

## 4. Orden de Ejecución por ROI

1. **DGE 2018-2024 (docling → CSV)** — Mayor impacto: +7 años de datos epidemiológicos
2. **openFMD (browser download)** — Datos FMD reales internacionales
3. **PUCRA (retry download + docling)** — Validación de constantes RAM
4. **COFEPRIS expandido** — Más filas para proxy de opacidad

---

## 5. Archivos del Repositorio (Mapa de Referencia)

```
EpidemicResearch/
├── src/
│   ├── config.py                    # URLs, constantes biológicas/financieras, CIE-10
│   ├── base_extractor.py            # ABC con retry, logging, lineage
│   └── extractors/
│       ├── senasica_tb.py           # ✅ 64 filas
│       ├── senasica_cuarentenas.py  # ✅ 108 filas
│       ├── dge_morbilidad.py        # ✅ 384 filas (2015-2017)
│       ├── dge_2018_2024.py         # ❌ PLACEHOLDER — necesita reemplazo
│       ├── cofepris_clausuras.py    # ✅ 2 filas
│       ├── pucra_ram.py             # ⚠️ Script OK, servidor UNAM caído
│       ├── openfmd.py               # ⚠️ Fallback a literatura (6 filas)
│       └── kaggle_fmd.py            # ⚠️ Necesita ~/.kaggle/kaggle.json
├── data/
│   ├── raw/                         # PDFs descargados + CSVs crudos
│   └── processed/                   # CSVs limpios listos para modelos
├── docs/
│   ├── task.md                      # Checklist maestro del proyecto
│   ├── data_acquisition_plan.md     # Plan Wave 1-3 con status actualizado
│   ├── DGE_DATA_SEARCH.md           # Investigación exhaustiva de Jules sobre DGE
│   ├── senasica_api_findings.md     # API SENASICA = 404 documentado
│   ├── senasica_datasets.md         # URLs de PDFs trimestrales
│   ├── implementation_plan.md       # Arquitectura completa del proyecto
│   ├── mvp_strategy.md              # Priorización anti-overengineering
│   └── jules_issues/               
│       ├── issue_01_dge_2018_2024.md
│       ├── issue_02_openfmd_kaggle.md
│       ├── issue_03_cofepris_pucra.md
│       └── issue_04_senasica_cuarentenas.md
├── Explicacion.md                   # Mapa arquitectural completo
├── M_doc.md                         # Protocolos de extracción y refs
└── V2.md                            # Constantes epidemiológicas y financieras
```
