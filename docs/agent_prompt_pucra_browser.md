# PROMPT: Descargar PDF de PUCRA (UNAM) con Browser Real

## EL PROBLEMA

El servidor `puiree.cic.unam.mx` ha estado dando timeout consistentemente cuando intentamos descargar los PDFs del PUCRA (Plan Universitario de Control de Resistencia Antimicrobiana) por `requests` de Python. La conexión se cuelga después de 60 segundos.

Necesitamos que TÚ, con un browser real, navegues al portal de la UNAM y descargues manualmente el PDF.

## TU MISIÓN

### Paso 1: Intentar la ruta directa

Abre un navegador y navega a estas URLs en orden. Si alguna carga, descarga el PDF:

```
https://puiree.cic.unam.mx/divulgacion/docs/pucra2025.pdf
https://puiree.cic.unam.mx/divulgacion/docs/pucra2024.pdf
https://puiree.cic.unam.mx/divulgacion/docs/pucra23.pdf
```

Si alguno descarga exitosamente, guárdalo como:
- `data/raw/pucra2024.pdf` (o el año que corresponda)

### Paso 2: Si la ruta directa falla, navegar el portal

1. Navega a `https://puiree.cic.unam.mx/divulgacion/`
2. Busca enlaces a los informes anuales PUCRA
3. Si el sitio tiene otra estructura, explora y encuentra los PDFs

### Paso 3: Si el portal UNAM está completamente caído, buscar alternativas

Google searches:

```
"PUCRA" "resistencia antimicrobiana" 2024 filetype:pdf
"Plan Universitario" "resistencia antimicrobiana" UNAM 2024 filetype:pdf
site:unam.mx PUCRA 2024
site:cic.unam.mx pucra
"pucra" antimicrobial resistance Mexico 2024
```

También busca en:
- Google Scholar: `PUCRA antimicrobial resistance Mexico`
- ResearchGate: `PUCRA UNAM resistencia`
- Repositorio institucional UNAM: `https://repositorio.unam.mx/` buscando "PUCRA"

### Paso 4: Si encuentras CUALQUIER PDF de PUCRA

1. Descárgalo a `data/raw/pucra2024.pdf` (o `pucra2025.pdf`, etc.)
2. Ejecuta el extractor que ya está listo:
   ```bash
   python -m src.extractors.pucra_ram
   ```
3. Verifica que genera `data/processed/pucra_ram_clean.csv`

### Paso 5: Validar los datos extraídos

Si el extractor produce resultados, valida contra estas constantes conocidas de `src/config.py`:

| Bacteria | Antibiótico | Valor esperado |
|----------|-------------|----------------|
| Salmonella spp. | Ampicilina | ~94.7% resistencia |
| Salmonella spp. | Carbenicilina | ~84.2% |
| Salmonella spp. | Tetraciclina | ~68.4% |
| Salmonella spp. | TMP-SMX | ~68.4% |
| E. coli | BLACTx-M | ~23.5% prevalencia |

Si los valores extraídos del PDF están dentro de ±10% de estos rangos, la extracción es correcta.

## ARCHIVOS RELEVANTES

| Archivo | Propósito |
|---------|-----------|
| `src/extractors/pucra_ram.py` | Extractor ya funcional. Acepta PDF local en `data/raw/` |
| `src/config.py` líneas 121-128 | Constantes de resistencia antimicrobiana para cross-validation |

## QUÉ HAY DENTRO DEL PDF (Para que sepas qué buscar)

El PDF PUCRA es un informe anual de la UNAM que contiene:
- Tablas de % de resistencia bacteriana a diferentes antibióticos
- Datos de aislados clínicos de hospitales mexicanos
- Las bacterias principales: E. coli, Klebsiella pneumoniae, Salmonella spp., Acinetobacter baumannii
- Los antibióticos: Ampicilina, Carbenicilina, Tetraciclina, TMP-SMX, Carbapenémicos, etc.

Las tablas típicamente tienen este formato:
```
| Bacteria | Antibiótico | n (aislados) | % Resistencia | % Sensible |
```

El extractor `pucra_ram.py` busca tablas con headers que contengan las palabras "antibiótico", "antimicrobiano", "bacteria", "resistencia".

## CONTEXTO

Estos datos sirven para:
1. **Validar** que nuestras constantes hardcodeadas (94.7% Ampicilina) son correctas
2. **Fortalecer la narrativa** del artículo científico sobre Resistencia Antimicrobiana
3. **Demostrar** que el consumo de carne con residuos de antibióticos (detectado en canales informales como tianguis) genera presión selectiva para bacterias resistentes

## ENTREGABLES

- `data/raw/pucra2024.pdf` (o cualquier año reciente)
- `data/processed/pucra_ram_clean.csv` (output del extractor)
- Documentar en `docs/wave2_recovery_results.md` si tuvo éxito o no
