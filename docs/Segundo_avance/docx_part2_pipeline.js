const { spacer, body, bodyRuns, r, b, bullet, h1, h2, h3, makeTable, goldRule } = require("./docx_helpers");

function buildPipeline() {
  return [
    h1("2. Pipeline de Datos: Adquisición y Transformación"),

    h2("2.1 El Problema de los Datos en México"),
    body("Los datos sobre enfermedades animales en México no están en un repositorio centralizado. El ecosistema opera con PDFs gubernamentales sin versión tabular (SENASICA, DGE post-2017, COFEPRIS), APIs no documentadas que retornan 404, dashboards internacionales que generan archivos vía WebSocket (openFMD) y servidores universitarios inestables (UNAM/PUCRA)."),

    h2("2.2 Estrategia ELT Multi-Fuente"),
    body("Para resolver esta fragmentación, se diseñó un pipeline de Extracción-Carga-Transformación (ELT) resiliente con tres capas:"),
    spacer(4),
    bodyRuns([b("Capa 1 — Extracción directa: "), r("Fuentes estables con CSV/ZIP accesibles por HTTP (SENASICA hatos libres, DGE 2015-2017).")]),
    bodyRuns([b("Capa 2 — Parsing de PDFs: "), r("Reportes trimestrales SENASICA, anuarios DGE 2018-2024 y resoluciones COFEPRIS procesados con pdfplumber.")]),
    bodyRuns([b("Capa 3 — Navegador automatizado: "), r("Dashboard interactivo openFMD (R/Shiny) y servidores inestables UNAM, automatizados con Playwright.")]),

    h2("2.3 Inventario de Datasets Recuperados"),
    makeTable(
      ["Dataset", "Archivo", "Filas", "Método", "Estado"],
      [
        ["SENASICA TB (hatos libres)", "senasica_tb_clean.csv", "64", "CSV directo", "✅ 32 estados"],
        ["SENASICA Cuarentenas 2024", "senasica_cuarentenas_clean.csv", "108", "PDF parsing", "✅ 4 trimestres"],
        ["DGE Morbilidad Estatal 2015-2017", "dge_morbilidad_clean.csv", "384", "ZIP → CSV", "✅"],
        ["DGE Morbilidad Nacional 2018-2024", "dge_morbilidad_2018_2024_clean.csv", "28", "PDF parsing", "✅"],
        ["DGE Consolidado 2015-2024", "dge_morbilidad_nacional_2015_2024_clean.csv", "40", "Unión", "✅ Serie 10 años"],
        ["openFMD Global (WRLFMD)", "openfmd_clean.csv", "28,585", "Playwright", "✅ 103 países"],
        ["COFEPRIS Sanciones", "cofepris_clausuras_alimentarias_clean.csv", "12", "PDF parsing", "✅ 7 empresas"],
      ],
      [2400, 2200, 700, 1400, 2326]
    ),
    spacer(6),
    bodyRuns([b("Total: "), r("~29,200 registros limpios desde 6 fuentes distintas.")]),

    h2("2.4 Data Warehouse: Transformación CSV→JSON con Pydantic"),
    bodyRuns([b("Código: "), r("src/warehouse/csv_to_json.py — Aporte del Miembro 1 del equipo (Axel).")]),
    body("Se implementó un script de transformación que convierte los datos tabulares de cuarentenas (CSV) a un formato JSON jerárquico optimizado para MongoDB, utilizando Pydantic como capa de validación de tipos."),
    body("El modelo CuarentenaRecord valida campos: estado (str), num_animales (int), trimestre (int), num_hatos_cuarentena (int), anio (int). Si un dato del CSV viene mal formado, el sistema lanza un error antes de contaminar la base de datos NoSQL. Los datos se agrupan jerárquicamente por Estado → Trimestre."),
  ];
}

module.exports = { buildPipeline };
