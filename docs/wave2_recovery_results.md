# Wave 2 Recovery Results

Fecha de corte: 2026-04-03

## Resumen Ejecutivo

La fase de recuperación de `Wave 2` quedó funcional en los componentes de mayor valor para el proyecto:

- `DGE 2018-2024` quedó recuperado con extracción real desde PDF nacional.
- `DGE nacional 2015-2024` quedó consolidado sin alterar el CSV estatal legado.
- `openFMD` quedó resuelto con adquisición browser-assisted real desde el dashboard Shiny y normalización local en el repo.
- `COFEPRIS` quedó reparado a un esquema tidy estable sobre los PDFs locales `2023/2024`.
- `COFEPRIS alimentario` quedó recuperado de forma parcial mediante PDFs oficiales de `Resoluciones y sanciones`, con 12 registros alimentarios/cárnicos utilizables como proxy alternativo.
- `PUCRA` quedó endurecido, pero su adquisición local sigue dependiendo de disponibilidad externa o de un PDF manual.

## Estado Por Fuente

| Fuente | Estado | Evidencia | Archivo principal |
| --- | --- | --- | --- |
| DGE nacional `2018-2024` | Recuperado | 28 filas, años `2018-2024`, `0` duplicados | `data/processed/dge_morbilidad_2018_2024_clean.csv` |
| DGE nacional consolidado `2015-2024` | Recuperado | 40 filas, años `2015-2024`, `0` duplicados | `data/processed/dge_morbilidad_nacional_2015_2024_clean.csv` |
| openFMD / FMDwatch | Recuperado | 28,585 filas crudas/limpias desde navegador real | `data/raw/openfmd_fmdwatch_export.csv` |
| COFEPRIS `2023/2024` | Recuperado | 33 filas limpias, esquema tidy | `data/processed/cofepris_clausuras_clean.csv` |
| COFEPRIS alimentario alternativo | Recuperado parcialmente | 12 registros oficiales alimentarios/cárnicos desde `Resoluciones y sanciones`; sin detalle de contaminante | `data/processed/cofepris_clausuras_alimentarias_clean.csv` |
| PUCRA `2024` | Preparado, sin adquisición local concluida | El PDF oficial fue verificable por navegador/web, pero no se logró persistir localmente desde shell/red | Espera `data/raw/pucra2024.pdf` |

## Resultados Recuperados

### 1. DGE 2018-2024

Extractor: `python -m src.extractors.dge_2018_2024`

Salida limpia:
- `data/processed/dge_morbilidad_2018_2024_clean.csv`

Esquema:
- `year_anuario`
- `report_name`
- `cve_cie10`
- `des_diagno`
- `acumulado_nacional`
- `source_pdf`
- `source_page`
- `extraction_method`

Resultado validado:
- 28 filas
- años `2018-2024`
- presencia de `A05`
- presencia de tuberculosis (`A15-A16`, `A17.0`, `A17.1, A17.8, A17.9, A18-A19`)
- `0` duplicados por `year_anuario + cve_cie10 + report_name`

### 2. DGE Nacional 2015-2024

Consolidación: `python -m src.extractors.dge_2018_2024`

Salida limpia:
- `data/processed/dge_morbilidad_nacional_2015_2024_clean.csv`

Lógica:
- `2015-2017` se agrega a nivel país desde `data/processed/dge_morbilidad_clean.csv`
- `2018-2024` se integra desde el nuevo extractor PDF nacional

Resultado validado:
- 40 filas
- años `2015-2024`
- `0` duplicados

### 3. openFMD / FMDwatch

Adquisición real:
- se abrió el dashboard `https://www.openfmd.org/dashboard/fmdwatch/`
- se navegó a la pestaña `Data table`
- se esperó a que el anchor `#loc_data_table-download_csv` recibiera `href`
- el CSV se obtuvo leyendo el endpoint dentro de la misma sesión Shiny viva

Comando de adquisición:

```bash
python -m src.extractors.openfmd_playwright_export
```

Comando de normalización:

```bash
python -m src.extractors.openfmd
```

Archivos:
- `data/raw/openfmd_fmdwatch_export.csv`
- `data/raw/openfmd_raw.csv`
- `data/processed/openfmd_clean.csv`

Resultado validado:
- 28,585 filas
- 28 columnas crudas del dashboard
- 33 columnas limpias incluyendo linaje ETL
- 123 países

Sanity check útil para modelado:
- si se filtran fechas válidas `2000-2025`, quedan 17,264 filas
- la fuente válida observada en ese rango fue `WRLFMD`
- serotipos dominantes: `O`, `A`, `SAT2`, `UNTYPED`, `Asia1`

Notas:
- el dashboard a veces devuelve HTML si se intenta descargar demasiado pronto o fuera de la sesión correcta
- el helper ya rechaza esos falsos CSV y los mueve a `data/raw/debug/` si vuelve a ocurrir

### 4. COFEPRIS

Comando:

```bash
python -m src.extractors.cofepris_clausuras
```

Salida limpia:
- `data/processed/cofepris_clausuras_clean.csv`

Resultado validado:
- 33 filas
- parseo estable sobre los PDFs locales:
  - `data/raw/Listado_de_Establecimientos_Verificados__2023.pdf`
  - `data/raw/Listado_de_Establecimientos_Verificados__2024.pdf`

Campos principales:
- `establecimiento`
- `domicilio`
- `orden_verificacion`
- `fecha_inicio_visita`
- `fecha_termino_visita`
- `giro_actividad`
- `motivo_visita`
- `estado_norm`

### 4.1 COFEPRIS alimentario alternativo

Ruta:
- `data/processed/cofepris_clausuras_alimentarias_clean.csv`

Fuentes oficiales usadas:
- `data/raw/cofepris_resoluciones_sanciones_sep_2023.pdf`
- `data/raw/cofepris_resoluciones_sanciones_dic_2023.pdf`
- `data/raw/cofepris_resoluciones_sanciones_dic_2024.pdf`

Resultado validado:
- 12 registros alimentarios/cárnicos
- 7 registros con `meat_related = true`
- 0 registros con `closure_explicit = true`
- 0 registros con `contaminant_explicit = true`

Lectura correcta del hallazgo:
- sí existe una señal oficial alimentaria útil para proxy regulatorio
- no se encontraron en esta pasada menciones explícitas a `clenbuterol`, `salmonella`, `LMR`, `rastro` o `matanza`
- por eso este archivo debe usarse como `proxy regulatorio alimentario alternativo`, no como evidencia directa de contaminantes cárnicos

### 5. PUCRA

Comando:

```bash
python -m src.extractors.pucra_ram
```

Estado:
- el extractor ya está listo para trabajar con una sola fuente viva `2024`
- el host `puiree.cic.unam.mx` sigue fallando cuando intentamos persistir el PDF localmente desde shell/red
- el flujo quedó degradado de forma limpia: si el host no responde, el extractor no rompe el pipeline
- el PDF oficial `pucra2024.pdf` sí fue verificable por navegador/web y corresponde al reporte `Resistencia antimicrobiana en México 2017 a 2023`

Ruta operativa recomendada:
- guardar manualmente el PDF como `data/raw/pucra2024.pdf`
- volver a correr `python -m src.extractors.pucra_ram`

Salida esperada:
- `data/processed/pucra_ram_clean.csv`

## Cómo Usar Cada Fuente En El Pipeline

### Flujo recomendado

```bash
python -m src.extractors.dge_2018_2024
python -m src.extractors.openfmd_playwright_export
python -m src.extractors.openfmd
python -m src.extractors.cofepris_clausuras
python -m src.extractors.pucra_ram
```

## Uso Analítico Recomendado

### DGE

Usar:
- `data/processed/dge_morbilidad_nacional_2015_2024_clean.csv`

Propósito:
- serie longitudinal mexicana para `A05` y grupos de tuberculosis
- baseline nacional para calibración y contraste temporal

### openFMD

Usar:
- `data/processed/openfmd_clean.csv`

Columnas recomendadas para análisis:
- `country`
- `date_sampling`
- `fmdv_serotype`
- `fmdv_topotype`
- `fmdv_lineage`
- `host`
- `data_source`
- `report_url`

Filtros recomendados:
- `date_sampling` entre `2000-01-01` y `2025-12-31`
- `fmdv_positive == "Yes"`
- `country != "Mexico"` cuando el objetivo sea modelar riesgo exógeno moderno

Uso:
- caracterizar diversidad viral
- identificar serotipos y regiones recientes
- alimentar narrativa y variables exógenas para escenarios FMD

### COFEPRIS

Usar:
- `data/processed/cofepris_clausuras_alimentarias_clean.csv`

Uso:
- proxy de opacidad regulatoria
- señal de riesgo alimentario oficial
- fallback cuando no existan clausuras cárnicas explícitas con contaminante
- features regulatorias para XGBoost

Notas:
- `data/processed/cofepris_clausuras_clean.csv` sigue existiendo, pero estaba sesgado a verificaciones farmacéuticas y no debe ser la primera opción para el proxy alimentario

### PUCRA

Usar:
- `data/processed/pucra_ram_clean.csv` cuando exista

Uso:
- soporte para narrativa RAM
- comparación con constantes ya definidas en `src/config.py`
- evidencia para exposición y discusión teórica

## Limitaciones Conocidas

1. `openFMD` requiere navegador real o Playwright; no es una fuente confiable por `requests` directos.
2. `PUCRA` sigue sin una ruta de descarga local persistente desde shell/red, aunque el PDF oficial sí pudo verificarse en navegador/web.
3. `openFMD` contiene registros históricos muy antiguos; para análisis epidemiológico reciente conviene filtrar por ventana temporal.
4. `DGE 2018-2024` se recuperó a nivel nacional, no estatal.
5. `COFEPRIS` no entregó en esta pasada un PDF federal con motivo explícito `clenbuterol/salmonella/LMR`; el mejor hallazgo fue un conjunto de sanciones alimentarias oficiales.

## Archivos Clave

- `src/extractors/dge_2018_2024.py`
- `src/extractors/openfmd.py`
- `src/extractors/openfmd_playwright_export.py`
- `src/extractors/cofepris_clausuras.py`
- `src/extractors/pucra_ram.py`
- `tests/test_wave2_recovery.py`

## Verificación Ejecutada

```bash
python -m unittest tests.test_wave2_recovery
```

Resultado:
- `8` pruebas
- `OK`
