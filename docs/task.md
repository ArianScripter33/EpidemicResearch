# Ganado Saludable — ELT Pipeline & Data Warehouse

> **Enfermedad asignada: Fiebre Aftosa (FMD)** | TB Bovina = Proxy de calibración

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
- [ ] Get user approval on plan + answers to 5 open questions

## Phase 1: Core Infra & Security

- [ ] Create directory structure (src/, extractors/, warehouse/, models/, crypto/, visualization/, tests/)
- [ ] Create `src/config.py` (all URLs from M_doc [1]-[24], V2.md constants, **FMD constants**)
- [ ] Create `src/base_extractor.py` (ABC with lineage: fecha_extraccion_etl, fuente_origen)
- [ ] Create `src/crypto/encryption.py` (César + RSA — Problema Prototípico §Criptografía)
- [ ] Create `requirements.txt`, `.gitignore`

## Phase 2: Extraction Modules (Module 1) — Wave-Based

### Wave 1 (Stable Endpoints)

- [ ] **SENASICA TB:** CSV hatos libres + API oculta fallback + Cuarentenas PDF (camelot) — **proxy calibración**
- [ ] **DGE Morbilidad:** Anuarios ZIP→CSV, CIE-10 filter (A15-A19, A05), latin1 encoding

### Wave 2 (International + PDF Parsing — **FMD Data**)

- [ ] **openFMD:** FMD global CSV — **datos primarios para la enfermedad asignada** + Chronos training
- [ ] **WRLFMD/PANAFTOSA:** Reportes regionales Sudamérica (serotipos, R0 estimados)
- [ ] **Manuales CPA:** KPIs de capacidad de respuesta (t_detección, t_cuarentena, brigadas)
- [ ] **PUCRA RAM:** PDF table extraction (E. coli, K. pneumoniae resistance rates)

### Wave 3 (Hostile Extraction)

- [ ] **SINAIS Cubos:** ViewState bypass (tokens + POST) OR Anuarios fallback
- [ ] **PNT/COFEPRIS:** Selenium headless — clausuras (clembuterol, LMR, Salmonella) + **Proxy de Opacidad**

## Phase 3: Data Warehouse & NoSQL (Module 2)

- [ ] Pydantic dimension models (6: Tiempo, Geografia, Patogeno, Antimicrobiano, Establecimiento, Especie)
- [ ] Pydantic fact models (7: HatosTB, CuarentenasTB, MorbilidadHumana, IndemnizacionTB, FMDCasos, RAM, Clausura)
- [ ] Star schema assembler (joins, keys geográficas)
- [ ] MongoDB adapter (nosql_client.py — requisito académico NoSQL)
- [ ] Docker `mongo:latest` levantado + colecciones creadas

## Phase 4: Model Preparation & Financials (Module 3)

- [ ] **SIR DUAL MODE:** Calibración TB (R0≈1.8, γ=1/180d) → Simulación FMD (R0≈6.0, γ=1/14d) — 6 escenarios
- [ ] XGBoost feature engineering (+ **proxy clembuterol** como feature de bioseguridad → target A05)
- [ ] **Stats Multivariate:** PCA + scree/biplot, ANOVA canales de venta, Regresión Múltiple → R²
- [ ] Chronos time-series formatter — **FMD series como principal**, TB series como calibración
- [ ] Financial ROI engine (VPN, ROI, Apalancamiento — **dual: TB crónico $39M vs FMD catastrófico $200B**)

## Phase 5: Visualization & Dashboard (Module 4)

- [ ] **Caras de Chernoff:** 32 caras (una por estado), rasgos = prevalencia TB, RAM, clausuras, densidad
- [ ] **Curvas de Andrews:** series de Fourier para clusters de estados epidemiológicamente similares
- [ ] **Mapas coropléticos:** mapa de México por estado con prevalencia TB, densidad, clausuras clembuterol
- [ ] **SIR Plots:** curvas S(t), I(t), R(t) comparativas TB vs FMD + diagramas de fase
- [ ] **Dashboard interactivo (Streamlit/Plotly Dash):** mapa + selector de estado + SIR + financiero

## Phase 6: Notebooks EDA

- [ ] `01_eda_senasica.ipynb` — Exploración datos SENASICA
- [ ] `02_eda_morbilidad.ipynb` — Exploración datos DGE/SINAIS
- [ ] `03_multivariate_analysis.ipynb` — PCA, Chernoff, Andrews, ANOVA
- [ ] `04_sir_simulation.ipynb` — Simulación SIR dual interactiva
- [ ] `05_xgboost_training.ipynb` — Entrenamiento + SHAP values
- [ ] `06_financial_analysis.ipynb` — VPN, ROI, escenarios

## Phase 7: Verification & Delivery

- [ ] Unit tests (mock HTTP, Pydantic validation, César/RSA bidireccional)
- [ ] Smoke test (download real SENASICA CSV, confirm endpoint alive)
- [ ] Local E2E with Docker MongoDB (pipeline: extract → ingest → model prep)
- [ ] Lineage audit (confirm fecha_extraccion_etl in all collections)
- [ ] SIR dual validation (gráfica comparativa TB vs FMD side-by-side)
- [ ] Artículo de divulgación (15-25 páginas, APA 7, min 5 fuentes)
- [ ] Presentación digital (Gamma/Genially/Prezi)
