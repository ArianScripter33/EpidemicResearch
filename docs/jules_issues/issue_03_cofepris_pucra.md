# JULES ISSUE 3 — COFEPRIS Clausuras + PUCRA RAM: Get Structured Data

## Priority: MEDIUM | Label: `jules` | Wave: 2

---

## Project Context

**Project:** Ganado Saludable — Academic epidemic research (UNRC, 4° Semestre).

**What we need:** Two datasets that feed our antimicrobial resistance and food safety analysis:

### Dataset A: COFEPRIS Clausuras (Clenbuterol + LMR + Salmonella)
These are government closures of meat processing plants (rastros) and distributors caught with:
- Clenbuterol (illegal growth promoter)
- LMR (Límites Máximos de Residuos) violations — antibiotic residues
- Salmonella contamination

**Why it matters:** We call this the "Proxy de Opacidad" — companies caught with clenbuterol violations almost certainly also abuse antibiotics. This is an original methodological contribution of our project and feeds as a feature in our XGBoost model.

**Needed:** A table with columns: `establecimiento`, `estado`, `motivo`, `fecha`, `agente_detectado`

### Dataset B: PUCRA — Antimicrobial Resistance Rates
The Plan Universitario de Control de la Resistencia Antimicrobiana (PUCRA/UNAM) publishes annual reports with resistance rates table by bacteria/antibiotic.

**Key numbers already documented in our config** (from V2.md literature):
- Ampicilina: 94.7% resistance in Salmonella from ground beef
- Carbenicilina: 84.2%
- blaCTX-M gene: 23.5%

But we need the full table from the PDF for our article.

---

## Task A: COFEPRIS Clausuras

### Step 1: Web Search
Search for:
1. `COFEPRIS clausuras clembuterol datos CSV descarga 2020 2021 2022 2023`
2. `site:gob.mx COFEPRIS establecimientos clausurados excel download`
3. `COFEPRIS rastros clausurados listado excel 2024`

### Step 2: Navigate COFEPRIS pages
1. Go to `https://www.gob.mx/cofepris/documentos/lista-de-establecimientos-clausurados?state=published`
   - Does clicking any document give a CSV/Excel file or only PDF?
   - Note the most recent document URL and file format
2. Go to `https://www.gob.mx/cofepris/acciones-y-programas/resoluciones-y-sanciones`
   - Is there structured data here?
3. Go to `https://www.gob.mx/cofepris/acciones-y-programas/listado-de-visitas-de-verificacion`
   - Is this an Excel/CSV download?

### Step 3: Write extractor
If data is accessible (CSV/Excel):
- Write `src/extractors/cofepris_clausuras.py`
- Filter for keywords in `motivo`: "CLENBUTEROL", "LMR", "SALMONELLA", "CLEMBUTEROL"
- Group by state (`estado`) and count closures per state

If only PDFs: write a parser using `pdfplumber` to extract tables from the latest closure list PDF.

---

## Task B: PUCRA RAM Tables

### Step 1: Download and parse
The PDF is at: `https://puiree.cic.unam.mx/divulgacion/docs/pucra2024.pdf`

Use Python + pdfplumber to:
1. Extract all tables from the PDF
2. Find tables with columns: bacteria, antimicrobiano, porcentaje_resistencia, n_aislamientos
3. Focus on: E. coli, Klebsiella pneumoniae, Salmonella spp., Acinetobacter baumannii

### Step 2: Also check 2025 version
`https://puiree.cic.unam.mx/divulgacion/docs/pucra2025.pdf`

### Step 3: Write extractor + save
Write `src/extractors/pucra_ram.py` that:
1. Downloads the PDF
2. Extracts resistance rate tables using pdfplumber
3. Outputs a clean CSV to `data/processed/pucra_ram_clean.csv`
4. Key columns: `bacteria`, `antibiotico`, `pct_resistencia`, `year_report`, `source`

---

## Known Data (already hardcoded in config.py — for cross-validation)

```python
RESISTENCIA_AMPICILINA = 0.947    # 94.7% Salmonella en carne molida
RESISTENCIA_CARBENICILINA = 0.842
PREVALENCIA_BLACTX_M = 0.235     # 23.5% BLEE
ECOLI_O157_PIEL = 0.909          # 90.9% hisopados pre-evisceración
```

These should match what the PUCRA PDF says — if the PDF extraction yields the same numbers, our data pipeline is validated.

---

## Files Already in Repo

- `src/config.py` — has `PUCRA_URLS`, `COFEPRIS_CLAUSURAS` constants
- `src/base_extractor.py` — ABC base class to inherit from
- `requirements.txt` — `pdfplumber` already installed
