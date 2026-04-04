# MEGA-PROMPT: Wave 2 Data Recovery Agent

> **Instrucción:** Copia TODO este documento como prompt para tu agente con capacidad de navegación web.
> **Longitud estimada:** ~4,000 tokens de contexto puro.

---

## TU MISIÓN

Eres un agente de datos senior trabajando en el proyecto académico **"Ganado Saludable" (EpidemicResearch)**. Tu trabajo es **recuperar datos que un agente anterior (Jules) no pudo extraer** porque no tenía capacidad de navegar la web como un browser real.

Tienes acceso a un browser. Puedes navegar, hacer click, descargar archivos, y ejecutar código Python.

El repositorio está en: `/Users/arianstoned/Developer/uni_semestre_4/EpidemicResearch`

---

## CONTEXTO DEL PROYECTO

Este es un proyecto universitario de investigación epidemiológica sobre Fiebre Aftosa (FMD) en ganado bovino mexicano. Usamos Tuberculosis Bovina como proxy de calibración porque México no tiene FMD activa.

**Fase actual:** Acabamos de terminar la Fase 1 (Adquisición de Datos) con un agente asíncrono (Jules). Jules logró extraer algunos datasets pero **falló en otros** porque no podía navegar la web. Tú SÍ puedes.

**Stack técnico:**
- Python 3.x + pandas + pdfplumber
- Todos los extractores heredan de `BaseExtractor` (en `src/base_extractor.py`)
- Los datos crudos van a `data/raw/`, los limpios a `data/processed/`
- La configuración central está en `src/config.py`

---

## TAREAS PRIORITARIAS (Ordenadas por ROI)

### TAREA 1 (ALTA PRIORIDAD): Extraer DGE Morbilidad 2018-2024 de PDFs

**Contexto completo:** La Dirección General de Epidemiología (DGE) de México publicaba anuarios de morbilidad como CSVs hasta 2017. A partir de 2018, SOLO están disponibles como PDFs. Jules confirmó esto exhaustivamente (ver `docs/DGE_DATA_SEARCH.md`). Ya tenemos datos de 2015-2017 (384 filas) extraídos del CSV, necesitamos 2018-2024 para completar la serie temporal.

**URLs verificadas de los PDFs (todas confirmadas activas por Jules):**
```
https://epidemiologia.salud.gob.mx/anuario/2018/morbilidad/nacional/distribucion_casos_nuevos_enfermedad_fuente_notificacion.pdf
https://epidemiologia.salud.gob.mx/anuario/2019/morbilidad/nacional/distribucion_casos_nuevos_enfermedad_fuente_notificacion.pdf
https://epidemiologia.salud.gob.mx/anuario/2020/morbilidad/nacional/distribucion_casos_nuevos_enfermedad_fuente_notificacion.pdf
https://epidemiologia.salud.gob.mx/anuario/2021/morbilidad/nacional/distribucion_casos_nuevos_enfermedad_fuente_notificacion.pdf
https://epidemiologia.salud.gob.mx/anuario/2022/morbilidad/nacional/distribucion_casos_nuevos_enfermedad_fuente_notificacion.pdf
https://epidemiologia.salud.gob.mx/anuario/2023/morbilidad/nacional/distribucion_casos_nuevos_enfermedad_fuente_notificacion.pdf
https://epidemiologia.salud.gob.mx/anuario/2024/morbilidad/nacional/distribucion_casos_nuevos_enfermedad_fuente_notificacion.pdf
```

**También hay versión por grupo de edad:**
```
https://epidemiologia.salud.gob.mx/anuario/{year}/morbilidad/nacional/distribucion_casos_nuevos_enfermedad_grupo_edad.pdf
```

**Qué extraer de cada PDF:**
- Filas que contengan enfermedades con códigos CIE-10: **A15, A16, A17, A18, A19** (Tuberculosis) y **A05** (Intoxicaciones alimentarias bacterianas)
- Columnas típicas: Enfermedad, CIE-10, Total Nacional, y desglose por estado si está disponible
- Normalizar nombres de estados usando el diccionario `ESTADOS_MEXICO` en `src/config.py`

**Método recomendado:**
1. Descarga cada PDF a `data/raw/dge_{year}_morbilidad.pdf`
2. Usa `docling` (`pip install docling`) o `marker-pdf` para convertir PDF → Markdown
3. Si docling no está disponible, usa `pdfplumber` directamente para extraer tablas
4. Busca en el output las filas que contienen "Tuberculosis", "A15", "A16", "A17", "A18", "A19", "A05", "Intoxicaciones"
5. Parsea esas filas en un DataFrame con columnas: `year, cie10_code, enfermedad, casos_totales, tasa_por_100k`
6. Guarda resultado en `data/processed/dge_morbilidad_2018_2024.csv`
7. Actualiza `src/extractors/dge_2018_2024.py` reemplazando el placeholder actual con el extractor real

**Referencia del extractor que ya funciona para 2015-2017:** `src/extractors/dge_morbilidad.py`

**Portal interactivo (para exploración adicional):** `https://epidemiologia.salud.gob.mx/anuario/html/morbilidad_nacional.html` — Es una página JavaScript/HTML que renderiza menús. Puedes navegar ahí para encontrar más datos o explorar la estructura.

---

### TAREA 2 (MEDIA PRIORIDAD): Descargar datos openFMD del dashboard Shiny

**Contexto:** El dashboard de openFMD (`https://openfmd.org/dashboard/fmdwatch/`) es una app R Shiny. El botón "Download CSV" genera un archivo dinámicamente via WebSocket, no tiene URL estática.

**Lo que necesitamos:**
- Navega a `https://openfmd.org/dashboard/fmdwatch/`
- Interactúa con los filtros del dashboard (selecciona region = Americas si es posible)
- Haz click en el botón "Download" o "Export CSV"
- Guarda el archivo descargado en `data/raw/openfmd_fmdwatch.csv`
- Parsea: país, fecha del brote, serotipo, número de casos, animales sacrificados
- Guarda limpio en `data/processed/openfmd_clean.csv`

**Si el dashboard no funciona o no tiene datos de Americas:**
- Navega a `https://wahis.woah.org/#/dashboards/qd-dashboard`
- Filtra por "Foot and mouth disease"
- Exporta/descarga los datos que aparezcan
- Nota: WAHIS usa Cloudflare pero un browser real PUEDE pasar

**Extractor existente como referencia:** `src/extractors/openfmd.py` (ver los campos esperados en `_generate_literature_reference()`)

---

### TAREA 3 (MEDIA PRIORIDAD): Reintentar descarga PUCRA RAM

**Contexto:** Los servidores de la UNAM (`puiree.cic.unam.mx`) estaban dando timeout. El script `src/extractors/pucra_ram.py` es funcional pero no pudo conectar.

**URLs a intentar:**
```
https://puiree.cic.unam.mx/divulgacion/docs/pucra2025.pdf
https://puiree.cic.unam.mx/divulgacion/docs/pucra2024.pdf
https://puiree.cic.unam.mx/divulgacion/docs/pucra23.pdf
```

**Alternativa si los servidores siguen caídos:**
- Busca en Google: `site:unam.mx PUCRA resistencia antimicrobiana 2024 filetype:pdf`
- Busca en Google: `"Plan Universitario de Control de Resistencia Antimicrobiana" 2024`
- Descarga cualquier PDF que encuentres con tablas de resistencia

**Qué extraer:**
- Tablas de % de resistencia por bacteria y antibiótico
- Bacterias target: E. coli, Klebsiella pneumoniae, Salmonella spp., Acinetobacter baumannii
- Antibióticos target: Ampicilina, Carbenicilina, Tetraciclina, TMP-SMX

**Cross-validación:** Compara el % extraído de Salmonella + Ampicilina contra el valor 94.7% que tenemos en `src/config.py` línea 122 (`RESISTENCIA_AMPICILINA = 0.947`)

---

### TAREA 4 (BAJA PRIORIDAD): Expandir COFEPRIS clausuras

**Contexto:** Ya tenemos 2 filas extraídas de establecimientos clausurados. Queremos más.

**Portal principal:** `https://www.gob.mx/cofepris/documentos/lista-de-establecimientos-clausurados?state=published`

**Lo que necesitamos:**
- Navega a la página de COFEPRIS
- Busca todos los PDFs de "Listado de Establecimientos Verificados" de 2019 a 2024
- Descárgalos a `data/raw/`
- Ejecuta `python -m src.extractors.cofepris_clausuras` después de la descarga
- Si el filtro actual es muy restrictivo, prueba expandir las keywords en el script

**Keywords actuales del filtro (en `cofepris_clausuras.py`):**
```python
['CLENBUTEROL', 'CLEMBUTEROL', 'LMR', 'SALMONELLA', 'RASTRO', 'CARNICERIA', 'MATANZA', 'POLLO', 'CARNE', 'ALIMENT']
```

---

## REGLAS DE OPERACIÓN

1. **Hereda de BaseExtractor** si creas nuevos scripts. Lee `src/base_extractor.py` primero.
2. **Normaliza estados** con `ESTADOS_MEXICO` de `src/config.py`.
3. **No subas datos a Git.** `data/raw/` y `data/processed/` están en `.gitignore`.
4. **Documenta hallazgos** en `docs/wave2_recovery_results.md`.
5. **Si una fuente falla**, documenta POR QUÉ y qué intentaste. No te rindas silenciosamente.
6. **Prioridad:** Tarea 1 > Tarea 2 > Tarea 3 > Tarea 4.

## ARCHIVOS CLAVE QUE DEBES LEER ANTES DE EMPEZAR

| Archivo | Por qué |
|---------|---------|
| `src/config.py` | URLs, constantes, CIE-10 codes, estados |
| `src/base_extractor.py` | ABC para heredar |
| `src/extractors/dge_morbilidad.py` | Template funcional para DGE 2015-2017 |
| `src/extractors/dge_2018_2024.py` | Placeholder a reemplazar |
| `docs/DGE_DATA_SEARCH.md` | Investigación completa de vías muertas |
| `docs/wave2_recovery_plan.md` | Plan estratégico completo |
| `docs/task.md` | Checklist maestro |
| `Explicacion.md` | Arquitectura del proyecto completa |

## ENTREGABLES ESPERADOS

Al terminar, deberías haber generado:

1. `data/processed/dge_morbilidad_2018_2024.csv` — Con al menos las filas de TB y A05 por año
2. `data/processed/openfmd_clean.csv` — Datos reales de brotes FMD (si el dashboard coopera)
3. `data/processed/pucra_ram_clean.csv` — Tablas RAM validadas contra config.py
4. `src/extractors/dge_2018_2024.py` — Extractor real (no placeholder)
5. `docs/wave2_recovery_results.md` — Resumen de hallazgos y limitaciones
