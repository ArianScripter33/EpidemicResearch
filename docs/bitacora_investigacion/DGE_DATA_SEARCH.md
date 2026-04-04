# DGE Morbilidad 2018-2024 Data Search Summary

## Objective
Find and extract CSV morbidity data for Mexico (DGE) for the years 2018-2024, filtering for CIE-10 codes A15-A19 and A05.

## Findings

### 1. Interactive Portal
The portal at [https://epidemiologia.salud.gob.mx/anuario/html/morbilidad_nacional.html](https://epidemiologia.salud.gob.mx/anuario/html/morbilidad_nacional.html) contains data for 2018-2024, but it is rendered via JavaScript and points to **PDF files**, not CSVs.

**PDF URL Pattern:**
`https://epidemiologia.salud.gob.mx/anuario/{year}/morbilidad/nacional/{report_name}.pdf`

**Verified Reports (2018-2024):**
- `distribucion_casos_nuevos_enfermedad_fuente_notificacion.pdf`
- `distribucion_casos_nuevos_enfermedad_grupo_edad.pdf`

### 2. Attempted CSV/ZIP URLs (All 404)
The following patterns were tested for years 2018-2024 and returned 404 Not Found:
- `https://epidemiologia.salud.gob.mx/anuario/datos_abiertos/Anuario_{year}.zip` (Worked for 2015-2017)
- `https://epidemiologia.salud.gob.mx/anuario/{year}/datos_abiertos/Anuario_{year}.zip`
- `https://epidemiologia.salud.gob.mx/anuario/{year}/morbilidad/nacional/datos_abiertos.zip`
- `https://epidemiologia.salud.gob.mx/anuario/datos_abiertos/t{year}.csv`
- `https://epidemiologia.salud.gob.mx/anuario/{year}/morbilidad/nacional/t{year}.csv`

### 3. Alternative Portals
- **datos.gob.mx**: No "Anuario de Morbilidad" datasets found for years beyond 2017.
- **DGE Datos Abiertos**: The main page [https://www.gob.mx/salud/documentos/datos-abiertos-152127](https://www.gob.mx/salud/documentos/datos-abiertos-152127) only links to 2015-2017 ZIPs.

## Conclusion
The DGE does not currently provide the full morbidity microdata (Datos Abiertos) in ZIP/CSV format for 2018-2024 in the expected locations. To obtain this data, a PDF scraper for the national and state reports may be required, or a direct request to the DGE via the Platform for Transparency.

## Recommended Next Steps
1. Implement a PDF extractor using `pdfplumber` or `camelot` to parse the identified PDF reports.
2. Check [SINAIS Cubos Dinámicos](http://www.dgis.salud.gob.mx/contenidos/basesdedatos/BD_Cubos_gobmx.html) as an alternative source for tabular data, although it often requires manual interaction or complex scraping.
