# JULES ISSUE 4 — SENASICA: More Granular TB Data (Quarantines + API)

## Priority: MEDIUM | Label: `jules` | Wave: 1.5

---

## Project Context

**Project:** Ganado Saludable — Academic epidemic research (UNRC, 4° Semestre).

**What we have now:** 64 rows from SENASICA CSVs — hatos certificados como libres de TB bovina, broken down by state and type of cattle (carne, leche, doble propósito). Successfully downloaded from:
- `https://repodatos.atdt.gob.mx/api_update/senasica/constatacion_hatos_libres_tuberculosis_bovina/hatos_libres_tuberculosis.csv`

**The gap:** The current data is aggregate constancias (certifications of freedom). For calibrating our SIR model we also need:
- **Cuarentenas** (quarantines) — number of farms under quarantine, animals affected, per state
- **Despoblaciones** (depopulations/sacrifices) — number of animals killed per state per year
- **Prevalencia temporal** — ideally multiple years to see trend

---

## Task for Jules

### Step 1: Web Search for more SENASICA datasets
Search the web for:
1. `site:datos.gob.mx SENASICA tuberculosis bovina cuarentenas CSV`
2. `datos.gob.mx SENASICA tuberculosis bovina 2020 2021 2022 2023 descarga`
3. `SENASICA datos abiertos hatos tuberculosis bovina por estado multi-año CSV`
4. `"senasica" "tuberculosis bovina" "datos abiertos" API JSON endpoint`

### Step 2: Check datos.gob.mx for more SENASICA datasets
Navigate to `https://www.datos.gob.mx/busca/?q=tuberculosis+bovina+senasica`
- List ALL datasets available, not just the one we already downloaded
- Note any with multiple years, quarantine data, or more granular breakdown

Also check:
- `https://www.datos.gob.mx/busca/?q=SENASICA+bovinos`
- `https://www.datos.gob.mx/busca/?q=senasica+cuarentena`

### Step 3: Download Quarantine PDFs and parse
SENASICA publishes quarterly quarantine reports as PDFs at:
- Q4 2024: `https://www.gob.mx/cms/uploads/attachment/file/979992/1._Cuarentenas_Tb_4to_tmt.pdf`
- Q3 2024: `https://www.gob.mx/cms/uploads/attachment/file/958502/1_Cuarentenas_Tercer_2024.pdf`
- Q2 2024: `https://www.gob.mx/cms/uploads/attachment/file/935619/1_CUARENTENAS_2DO_TRIMESTRE_2024.pdf`
- Q1 2024: `https://www.gob.mx/cms/uploads/attachment/file/914491/1_CUARENTENAS_Primer_2024.pdf`

Use pdfplumber to extract tables with columns:
- estado, num_hatos_cuarentena, num_animales, tipo_medida (cuarentena/despoblación), fecha

Also search for 2022 and 2023 quarterlies on the same page:
`https://www.gob.mx/senasica/documentos/cuarentenas-tuberculosis-bovina-2024?state=published`
(change 2024 to 2022, 2023 to find older reports)

### Step 4: Try SENASICA hidden API
The research protocol PDF documents an undisclosed REST API:
`https://dj.senasica.gob.mx/sias/api/Statistics/SaludAnimal/TuberculosisBovina/ObtenerDatos`

Try both GET and POST, with headers:
```python
headers = {
    'Accept': 'application/json',
    'Referer': 'https://dj.senasica.gob.mx/sias/',
}
```
Also try inspecting network requests on:
`https://dj.senasica.gob.mx/sias/` (the SIAS portal)

---

## Expected Output

1. Download and parse all 4 quarterly PDFs (Q1-Q4 2024) into a unified CSV
2. Write `src/extractors/senasica_cuarentenas.py` that:
   - Downloads quarterly PDFs for 2023 and 2024
   - Extracts quarantine tables using pdfplumber
   - Outputs `data/processed/senasica_cuarentenas_clean.csv`
3. Document any additional SENASICA CSV datasets found on datos.gob.mx
4. Note if the hidden API is accessible

---

## Files Already in Repo

- `src/extractors/senasica_tb.py` — existing CSV extractor (64 rows, 32 states)
- `src/config.py` — has `SENASICA_CUARENTENAS_PDFS` and `SENASICA_API_OCULTA` constants
- `data/processed/senasica_tb_clean.csv` — the current 64 rows
- `requirements.txt` — `pdfplumber>=0.10` already installed
