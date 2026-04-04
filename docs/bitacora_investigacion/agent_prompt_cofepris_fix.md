# PROMPT: Encontrar y Extraer las Clausuras ALIMENTARIAS Reales de COFEPRIS

## EL PROBLEMA

El extractor actual (`src/extractors/cofepris_clausuras.py`) parsea correctamente los PDFs, pero las 33 filas que produce son **TODAS** de `giro_actividad = "LABORATORIO O FÁBRICA DE MEDICAMENTOS"`. Son verificaciones de empresas farmacéuticas (Laboratorios PISA, Grossman, etc.), NO clausuras de establecimientos alimentarios.

Para nuestro proyecto necesitamos clausuras de **rastros, mataderos, plantas procesadoras de carne, empacadoras** donde COFEPRIS haya encontrado **Clenbuterol, Salmonella, violaciones de LMR (Límites Máximos de Residuos)**, o cualquier infracción alimentaria relacionada con la cadena cárnica.

## TU MISIÓN

### Paso 1: Navegar COFEPRIS con browser real

Abre un navegador y navega a estos portales en orden:

1. **Portal principal de clausuras:**
   `https://www.gob.mx/cofepris/documentos/lista-de-establecimientos-clausurados?state=published`
   
2. **Acciones sanitarias:**
   `https://www.gob.mx/cofepris/acciones-y-programas/acciones-sanitarias`

3. **Verificaciones sanitarias (alimentos):**
   `https://www.gob.mx/cofepris/acciones-y-programas/listado-de-visitas-de-verificacion`

4. **Google site search:**
   ```
   site:gob.mx/cofepris clausura rastro clenbuterol filetype:pdf
   site:gob.mx/cofepris "establecimientos clausurados" alimentos filetype:pdf
   site:gob.mx/cofepris clenbuterol clausura 2024
   site:gob.mx/cofepris "acta de clausura" carne rastro
   site:cofepris.gob.mx clausura alimentos
   ```

5. **Datos abiertos:**
   `https://datos.gob.mx/busca/dataset?q=cofepris+clausura`
   `https://datos.gob.mx/busca/dataset?q=cofepris+clenbuterol`

6. **Comunicados de prensa COFEPRIS (a menudo tienen listas de clausurados):**
   `https://www.gob.mx/cofepris/prensa`
   Busca comunicados que mencionen: "clausura", "rastro", "clenbuterol", "carne", "inocuidad"

### Paso 2: Identificar los PDFs correctos

Lo que buscamos son PDFs que contengan tablas con columnas como:
- Nombre del establecimiento (ej: "Rastro Municipal de Toluca")
- Motivo de clausura (ej: "Presencia de Clenbuterol", "Violación LMR", "Condiciones insalubres")
- Ubicación/Estado
- Fecha de clausura
- Agente encontrado (Clenbuterol, Salmonella, etc.)

**NO nos sirven:**
- Verificaciones de laboratorios farmacéuticos (eso es lo que ya tenemos)
- Listas de farmacias clausuradas
- Verificaciones de dispositivos médicos

### Paso 3: Descargar y parsear

Si encuentras PDFs correctos:
1. Descárgalos a `data/raw/cofepris_clausuras_alimentos_YYYY.pdf`
2. Parsea con `pdfplumber` (ya está instalado)
3. Filtra por keywords: `CLENBUTEROL`, `CLEMBUTEROL`, `SALMONELLA`, `LMR`, `RASTRO`, `MATANZA`, `CARNE`, `POLLO`, `ALIMENT`, `BOVIN`, `AVICOLA`
4. Guarda resultado en `data/processed/cofepris_clausuras_alimentarias_clean.csv`

### Paso 4: Si NO encuentras PDFs de clausuras alimentarias

Esto es posible. COFEPRIS es notoriamente opaco. Si no encuentras los PDFs:

1. **Documenta** exactamente qué URLs visitaste y qué encontraste
2. **Busca comunicados de prensa** como alternativa — a menudo COFEPRIS anuncia clausuras en notas de prensa con datos parciales
3. **Intenta la PNT (Plataforma Nacional de Transparencia):**
   `https://www.plataformadetransparencia.org.mx/`
   Busca: "COFEPRIS clausura establecimientos alimentarios 2023 2024"
4. Crea `docs/cofepris_alimentaria_search.md` documentando todos los intentos

## ARCHIVOS RELEVANTES DEL REPO

| Archivo | Propósito |
|---------|-----------|
| `src/extractors/cofepris_clausuras.py` | Parser actual (funciona bien, el problema es la fuente) |
| `src/config.py` | `COFEPRIS_CLAUSURAS` URL, `ESTADOS_MEXICO` para normalización |
| `data/raw/Listado_de_Establecimientos_Verificados__2023.pdf` | PDF INCORRECTO (farmacias) |
| `data/raw/Listado_de_Establecimientos_Verificados__2024.pdf` | PDF INCORRECTO (farmacias) |
| `data/processed/cofepris_clausuras_clean.csv` | Output actual: 33 filas de farmacias (INÚTIL) |

## CONTEXTO DEL PROYECTO

Esto alimenta el **"Proxy de Opacidad"** del proyecto Ganado Saludable. La hipótesis es: si COFEPRIS clausura frecuentemente rastros por Clenbuterol/Salmonella en ciertos estados, esos estados tienen mayor riesgo epidemiológico. Es una variable latente para XGBoost que mide "qué tan descontrolada está la cadena cárnica".

## ENTREGABLE

- `data/processed/cofepris_clausuras_alimentarias_clean.csv` (si encuentras los PDFs)
- `docs/cofepris_alimentaria_search.md` (documentación de búsqueda, siempre)
