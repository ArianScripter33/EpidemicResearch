# Ganado Saludable — ELT Pipeline & Data Warehouse

> **Enfermedad asignada: Fiebre Aftosa (FMD)** | TB Bovina = Proxy de calibración

> **Última actualización:** 2026-04-03 (Post Wave 2 Recovery)

## Phase 0: Research & Audit

- [x] Read V2.md (epidemiological context, 35.1M biomass, RAM prevalence)
- [x] Read M_doc.md (extraction protocol, 24 refs, endpoints, star schema)
- [x] Read PROBLEMA PROTOTIPICO PDF (7-subject university requirements)
- [x] Read Protocolo Investigación Zoonótica PDF (advanced extraction, hacker vectors)
- [x] Audit v1 plan vs v2 plan → produce definitive v3 merge
- [x] Write implementation plan v3 (dual-path extraction, full URL table, all schemas)
- [x] Reframe project: FMD = assigned disease, TB = calibration proxy
- [x] Update to V4: SIR dual-mode, FMD constants, UK 2001 reference, WRLFMD/PANAFTOSA sources
- [x] Create README.md with 7-subject coverage map and potential findings
- [x] Create presentation_script.md (guion narrativo para coloquio)
- [x] Add Component 5 (visualization + stats multivariate) to implementation plan
- [x] Add "Proxy de Opacidad" (clembuterol) to XGBoost features and PNT extractor
- [x] Create docs/mvp_strategy.md (priorización + anti-overengineering)
- [x] Create docs/data_acquisition_plan.md (plan de adquisición de datos Wave 1-3)

## Phase 1: Core Infra & Security

- [x] Create directory structure (src/, extractors/, warehouse/, models/, crypto/, visualization/, tests/)
- [x] Create `src/config.py` (all URLs from M_doc [1]-[24], V2.md constants, FMD constants, SIR scenarios)
- [x] Create `src/base_extractor.py` (ABC with lineage: fecha_extraccion_etl, fuente_origen, version_etl)
- [x] Create `requirements.txt`
- [x] Update `.gitignore`
- [ ] Create `src/crypto/encryption.py` (César + RSA — Problema Prototípico §Criptografía)

## Phase 2: Extraction Modules (Module 1) — Wave-Based

### Wave 1 (Stable Endpoints) ✅

- [x] **SENASICA TB:** CSV hatos libres → **64 rows, 32 estados** — proxy calibración
- [x] **DGE Morbilidad:** Anuarios 2015-2017 ZIP→CSV → **384 rows** (288 TB + 96 A05)
  - Nota: Anuarios 2018+ no disponibles en formato CSV (404). 2015-2017 tienen datos por estado/edad/mes/institución.
- [x] **DGE Morbilidad 2018-2024:** PDFs parseados con pdfplumber → **28 filas nacionales** + serie consolidada 2015-2024 (40 filas)
  - Nota: Solo nivel nacional (no estatal). CSV estatal legado 2015-2017 preservado intacto.

### Wave 2 (International + FMD Data)

- [x] **openFMD:** Browser-assisted Playwright export → **28,585 filas reales** (123 países, serotipos, coordenadas GPS, 2001-2025)
- [x] **Kaggle FMD:** Extractor `kaggle_fmd.py` listo (necesita API key)
- [x] **PUCRA RAM PDFs:** Extractor `pucra_ram.py` endurecido. Host UNAM sigue caído. Acepta PDF local en `data/raw/pucra2024.pdf`.
- [x] **COFEPRIS clausuras:** Parser reparado → **33 filas tidy**. ⚠️ PROBLEMA: PDFs son de "Establecimientos Verificados" (laboratorios farmacéuticos), NO de clausuras de rastros/mataderos. Necesita nuevas fuentes PDF con clausuras alimentarias reales.
- [x] **SENASICA Cuarentenas:** Extractor `senasica_cuarentenas.py` → **108 filas** 2024 PDFs (API oculta = 404).

### Wave 3 (Hostile Extraction — Solo si sobra tiempo)

- [ ] **SINAIS Cubos:** ViewState bypass (tokens + POST) OR Anuarios fallback
- [ ] **PNT/COFEPRIS:** Selenium headless — clausuras (clembuterol, LMR, Salmonella) + Proxy de Opacidad

## Phase 3: Data Warehouse & NoSQL (Module 2)

- [ ] Pydantic dimension models (6: Tiempo, Geografia, Patogeno, Antimicrobiano, Establecimiento, Especie)
- [ ] Pydantic fact models (7: HatosTB, CuarentenasTB, MorbilidadHumana, IndemnizacionTB, FMDCasos, RAM, Clausura)
- [ ] Star schema assembler (joins, keys geográficas)
- [ ] MongoDB adapter (nosql_client.py — requisito académico NoSQL)
- [ ] Docker `mongo:latest` levantado + colecciones creadas

## Phase 4: Model Preparation & Financials (Module 3)

- [ ] **SIR DUAL MODE:** Calibración TB (R0≈1.8, γ=1/180d) → Simulación FMD (R0≈6.0, γ=1/14d) — 6 escenarios
- [ ] **Stats Multivariate:** ANOVA canales de venta (con datos V2.md), PCA (si datos suficientes), Regresión Múltiple
- [ ] **Financial ROI:** VPN, ROI, tabla comparativa preventivo vs reactivo
- [ ] XGBoost feature engineering (Tier 2 — si datos suficientes)
- [ ] Chronos time-series formatter (Tier 2 — si openFMD data obtenida)

## Phase 5: Visualization & Dashboard (Module 4)

- [ ] **Mapa coroplético:** México por estado con datos SENASICA (plotly.express)
- [ ] **SIR Plots:** Curvas S(t), I(t), R(t) comparativas TB vs FMD + diagramas de fase
- [ ] **Tabla financiera:** Visualización ROI preventivo vs reactivo
- [ ] Caras de Chernoff (Tier 2 — si datos multivariados suficientes)
- [ ] Curvas de Andrews (Tier 2)
- [ ] Dashboard interactivo Streamlit (Tier 3)

## Phase 6: Notebooks EDA ✅

- [x] `01_eda_global.ipynb` — EDA maestro que consolida SENASICA (32 estados), DGE (TB + A05), openFMD y COFEPRIS.
- [ ] `02_analisis_descriptivo.ipynb` — Análisis de varianza (DGE) y Top países África (TBD - delegado).
- [ ] `03_multivariate_analysis.ipynb` — PCA, ANOVA, Chernoff
- [ ] `04_sir_simulation.ipynb` — Simulación SIR dual interactiva
- [ ] `05_financial_analysis.ipynb` — VPN, ROI, escenarios

## Phase 7: Verification & Delivery

- [ ] Unit tests (mock HTTP, Pydantic validation, César/RSA bidireccional)
- [x] Smoke test SENASICA CSV (endpoint alive, 64 rows downloaded)
- [x] Smoke test DGE Anuarios (2015-2017 alive, 384 filtered rows)
- [x] Smoke test openFMD (API no accesible, fallback a literatura OK)
- [ ] SIR dual validation (gráfica comparativa TB vs FMD side-by-side)
- [ ] Artículo de divulgación (15-25 páginas, APA 7, min 5 fuentes)
- [ ] Presentación digital (Gamma/Genially/Prezi)

---

## Data Inventory (as of 2026-04-03)

| Dataset | Source | Rows | Status | Key columns |
|---------|--------|------|--------|-------------|
| SENASICA TB | CSV datos abiertos | 64 | ✅ Ready | entidad, constancias, bovinos_libres |
| SENASICA Cuarentenas | PDFs trimestrales 2024 | 108 | ✅ Ready | estado, cuarentena, animales_sacrificados |
| DGE Morbilidad (estatal) | Anuarios ZIP 2015-2017 | 384 | ✅ Ready | estado, CIE-10, acumulado, edad, mes, institución |
| DGE Morbilidad (nacional) | PDFs 2018-2024 | 28 | ✅ Ready | year, cve_cie10, acumulado_nacional |
| DGE Consolidado Nacional | Unión 2015-2024 | 40 | ✅ Ready | year, cve_cie10, acumulado_nacional |
| openFMD (real data) | Browser export WRLFMD | 28,585 | ✅ Ready | country, date, serotype, topotype, lineage |
| COFEPRIS Alimentaria | gob.mx PDFs | 12 | ✅ Proxy regulatory | Sanciones a empresas cárnicas (Bachoco, Qualtia) |
| PUCRA RAM | PDFs UNAM | — | ❌ Host caído | Esperando PDF local en data/raw/pucra2024.pdf |

**Total filas limpias:** ~29,242
