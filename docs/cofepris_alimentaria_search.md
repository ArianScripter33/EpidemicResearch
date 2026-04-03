# COFEPRIS Alimentaria Search Log

Fecha de corte: 2026-04-03

## Objetivo

Encontrar `clausuras alimentarias reales` de COFEPRIS, idealmente relacionadas con:

- `clenbuterol`
- `salmonella`
- `LMR`
- `rastros`
- `mataderos`
- `plantas procesadoras de carne`

## URLs Visitadas

Portales oficiales intentados:

- `https://www.gob.mx/cofepris/documentos/lista-de-establecimientos-clausurados?state=published`
- `https://www.gob.mx/cofepris/acciones-y-programas/acciones-sanitarias`
- `https://www.gob.mx/cofepris/acciones-y-programas/listado-de-visitas-de-verificacion`
- `https://www.gob.mx/cofepris/prensa`
- `https://www.gob.mx/cofepris/acciones-y-programas/resoluciones-y-sanciones`

Buscadores y búsqueda dirigida:

- `site:gob.mx/cofepris clausura rastro clenbuterol filetype:pdf`
- `site:gob.mx/cofepris "establecimientos clausurados" alimentos filetype:pdf`
- `site:gob.mx/cofepris clenbuterol clausura 2024`
- `site:gob.mx/cofepris "acta de clausura" carne rastro`
- `site:datos.gob.mx cofepris clausura alimentos`
- `site:plataformadetransparencia.org.mx COFEPRIS clausura establecimientos alimentarios 2024`

## Hallazgos

### 1. El portal normal de COFEPRIS está protegido por anti-bot

Los endpoints HTML principales devolvieron `Challenge Validation` por `requests`.

Resultado:
- no fue viable usar scraping HTTP directo sobre las páginas normales
- tampoco aparecieron tablas alimentarias en los PDFs locales de `Listado_de_Establecimientos_Verificados__2023/2024`

### 2. Los PDFs locales ya presentes no sirven para el caso alimentario

Archivos revisados:

- `data/raw/Listado_de_Establecimientos_Verificados__2023.pdf`
- `data/raw/Listado_de_Establecimientos_Verificados__2024.pdf`

Conclusión:
- producen verificaciones principalmente farmacéuticas
- sesgo fuerte a `laboratorios` y `fábricas de medicamentos`
- no contienen el objetivo `rastro/clenbuterol/salmonella`

### 3. La mejor fuente oficial recuperable fue `Resoluciones y sanciones`

Se localizaron y descargaron estos PDFs oficiales por URL directa:

- `https://www.gob.mx/cms/uploads/attachment/file/937536/Resoluciones_y_sanciones_septiembre_2023_COS.pdf`
- `https://www.gob.mx/cms/uploads/attachment/file/937538/Resoluciones_y_sanciones_diciembre_2023_COS.pdf`
- `https://www.gob.mx/cms/uploads/attachment/file/982366/Resoluciones_y_sanciones_diciembre_2024_COS_a.pdf`

Archivos guardados:

- `data/raw/cofepris_resoluciones_sanciones_sep_2023.pdf`
- `data/raw/cofepris_resoluciones_sanciones_dic_2023.pdf`
- `data/raw/cofepris_resoluciones_sanciones_dic_2024.pdf`

## Qué Se Encontró En Esos PDFs

No se encontraron menciones explícitas a:

- `clenbuterol`
- `clembuterol`
- `salmonella`
- `LMR`
- `rastro`
- `matanza`

Sí se encontraron establecimientos y empresas alimentarias/cárnicas oficiales, por ejemplo:

- `CARNES SELECTAS ALI, S.A. DE C.V.`
- `GRUPO COMERCIAL ML BACHOCO / GRUPO COMERCIAL DE POLLO Y CARNES`
- `ALMACENES Y FRIGORIFICOS AMERIBEN, S.A. DE C.V.`
- `CARNES SELECTAS EXPRESS DEL SUR`
- `CARNICERIA EL GRILLO`
- `QUALTIA ALIMENTOS OPERACIONES, S. DE R.L. DE C.V.`

## Resultado Operativo

Se generó un dataset alternativo:

- `data/processed/cofepris_clausuras_alimentarias_clean.csv`

Contenido:
- `12` registros oficiales alimentarios/cárnicos
- `7` registros marcados como `meat_related = true`

Limitación crítica:
- son `procedimientos de sanción` oficiales
- no son `clausuras cárnicas con contaminante explícito`
- por tanto, funcionan como `proxy regulatorio alimentario alternativo`, no como prueba directa de clenbuterol o salmonella

## Conclusión

Conclusión honesta de esta búsqueda:

1. No se encontró en esta pasada un PDF federal de COFEPRIS que documente explícitamente `clausura de rastro/carnicería/planta cárnica` por `clenbuterol`, `salmonella` o `LMR`.
2. Sí se encontró una señal oficial alternativa de establecimientos alimentarios/cárnicos sancionados por COFEPRIS.
3. Para el proyecto, este hallazgo puede usarse como una versión conservadora del `Proxy de Opacidad`.

## Siguiente Paso Recomendado

Si se quiere ir más allá del hallazgo actual, las rutas con mejor expectativa son:

1. `PNT` con solicitudes o búsquedas por expediente, no solo búsqueda pública rápida.
2. Comunicados estatales de `COEPRIS` y secretarías sanitarias locales.
3. Cruce con nombres de establecimientos cárnicos ya identificados en estos PDFs de sanción.
