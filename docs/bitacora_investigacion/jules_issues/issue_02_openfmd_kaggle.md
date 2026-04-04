# JULES ISSUE 2 — openFMD: Find real CSV download URL + Kaggle FMD Dataset

## Priority: HIGH | Label: `jules` | Wave: 2

---

## Project Context

**Project:** Ganado Saludable — Academic epidemic research project (UNRC, 4° Semestre).

**Disease assigned:** Fiebre Aftosa (FMD). We need historical FMD outbreak data to:
1. Validate our R0 estimates (currently using literature: R0 = 4.0–8.0 from Tildesley et al. 2006)
2. Show international FMD series for the presentation narrative (FAO Jan 2025 alert: active outbreaks in Europe and Near East)
3. (Optional) Train Chronos time-series model on FMD outbreak sequences

**What we have now:** A 6-row literature reference table (hardcoded) with R0 estimates for: UK 2001, Argentina 2001, Colombia 2017, Germany 2025, Turkey 2024, Brazil 2006.

**What we need:** Actual tabular FMD data — dates, countries, case counts, serotypes.

---

## The Problem

The openFMD dashboard at `https://openfmd.org/dashboard/fmdwatch/` has a "Download CSV" button but the actual download URL is not visible from simple HTTP requests. The URL renders via JavaScript.

We tried several guessed URLs — all returned 404 or non-CSV content:
- `https://openfmd.org/api/fmdwatch/export/csv` → failed
- `https://openfmd.org/dashboard/fmdwatch/download` → failed
- `https://openfmd.org/fmdwatch/data/export.csv` → failed

WAHIS (WOAH) API at `https://wahis.woah.org/api/v1/...` also did not return accessible data.

---

## Task for Jules

### Step 1: Web Search for openFMD CSV URL
Search the web for:
1. `site:openfmd.org download csv fmdwatch`
2. `openfmd.org API endpoint CSV download fmd data`
3. `openFMD FMDwatch data download python script github`
4. `WOAH WAHIS FMD data download API python 2024`

### Step 2: Navigate openFMD dashboard
Go to `https://openfmd.org/dashboard/fmdwatch/`
- Click the download/export button (if it exists)
- Inspect the network request to find the actual API endpoint URL
- Note any filters applied (region, year, serotype)
- Copy the exact download URL

### Step 3: Kaggle FMD Dataset
Search for and download:
- `https://www.kaggle.com/datasets/wasimfaraz/fmd-cattle-dataset` (referenced in our research protocol PDF)
- Note: Kaggle may require auth. If so, document how to set up kaggle API key.

### Step 4: Alternative sources
Search for:
1. `PANAFTOSA PAHO FMD data download Americas 2010-2024 CSV`
2. `WOAH_WAHIS.ReportRetriever python pip install usage example`
   - GitHub: `https://github.com/loicleray/WOAH_WAHIS.ReportRetriever`
   - Check if this tool works and how to install + run it for FMD data Americas region
3. GitHub datasets for FMD: search `"foot and mouth disease" dataset CSV site:github.com`

---

## Expected Output

1. Write/update `src/extractors/openfmd.py` with the real download URL (replace the hardcoded fallback if a real URL is found)
2. If Kaggle dataset is accessible: add a `src/extractors/kaggle_fmd.py` script that downloads it
3. If WOAH_WAHIS tool works: add installation + usage notes to `docs/data_acquisition_plan.md`

---

## Files Already in Repo

- `src/extractors/openfmd.py` — existing extractor with literature fallback
- `src/config.py` — has `OPENFMD_DASHBOARD`, `WAHIS_RETRIEVER_REPO` constants
- `data/processed/openfmd_clean.csv` — the 6-row literature reference we currently have
