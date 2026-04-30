const { spacer, hRule, goldRule, centered, body, bodyRuns, r, b, bullet, h1, h2, h3, C, G, D, W, GR, GL, infoRow, noBorders } = require("./docx_helpers");
const { Paragraph, TextRun, Table, TableRow, TableCell, AlignmentType, HeadingLevel, BorderStyle, WidthType, ShadingType, TableOfContents, PageBreak } = require("docx");

function buildCover() {
  return [
    spacer(80),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 0 }, border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: C, space: 1 } }, children: [] }),
    spacer(20),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 200, after: 80 }, children: [new TextRun({ text: "GANADO SALUDABLE", font: "Arial", size: 52, bold: true, color: C })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 40 }, children: [new TextRun({ text: "Sistema Integral de Auditoría Epidemiológica Bovina", font: "Arial", size: 28, color: D })] }),
    spacer(10),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 0 }, border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: G, space: 1 } }, children: [] }),
    spacer(20),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 80, after: 200 }, children: [new TextRun({ text: "SEGUNDO AVANCE — REPORTE DE EJECUCIÓN", font: "Arial", size: 32, bold: true, color: G })] }),
    spacer(20),
    new Table({
      width: { size: 9026, type: WidthType.DXA }, columnWidths: [3600, 5426],
      rows: [
        infoRow("Universidad", "Universidad Nacional \"Rosario Castellanos\""),
        infoRow("Carrera", "Licenciatura en Ciencias de Datos para Negocios"),
        infoRow("Semestre", "4° — 2026-1"),
        infoRow("Enfermedad", "Fiebre Aftosa (FMD) | Proxy: Tuberculosis Bovina"),
        infoRow("Fecha", "30 de abril de 2026"),
      ]
    }),
    spacer(40),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 200 }, border: { top: { style: BorderStyle.SINGLE, size: 4, color: G, space: 1 } }, children: [] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 80 }, children: [new TextRun({ text: "Documento generado programáticamente con docx-js", font: "Arial", size: 16, italics: true, color: "999999" })] }),
  ];
}

function buildTOC() {
  return [
    new Paragraph({ children: [new PageBreak()] }),
    new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 200, after: 200 }, children: [new TextRun({ text: "Tabla de Contenidos", font: "Arial", size: 36, bold: true, color: C })] }),
    new TableOfContents("Tabla de Contenidos", { hyperlink: true, headingStyleRange: "1-3" }),
  ];
}

function buildIntro() {
  return [
    h1("1. Introducción"),
    h2("1.1 Resumen del Primer Avance"),
    body("En el Primer Avance se presentó la arquitectura estratégica del proyecto \"Ganado Saludable\": un sistema integral de auditoría epidemiológica que utiliza la Tuberculosis Bovina (endémica en México) como proxy de calibración para modelar el impacto catastrófico de una reintroducción de Fiebre Aftosa (FMD), enfermedad de la cual México ha sido declarado libre desde 1954."),
    body("Se definió la alineación con las 7 materias del semestre, se diseñó la arquitectura ELT (Extract-Load-Transform), y se identificaron las fuentes de datos gubernamentales e internacionales necesarias."),
    h2("1.2 Qué se ha ejecutado desde entonces"),
    body("Este Segundo Avance documenta la ejecución completa de la primera mitad del proyecto:"),
    spacer(4),
    bullet("Pipeline ELT multi-fuente operativo (~29,200 registros limpios desde 6 fuentes)"),
    bullet("Análisis Exploratorio de Datos (EDA) con 8 hallazgos cuantificados"),
    bullet("Análisis Descriptivo de brotes en África (Top 5 países FMD)"),
    bullet("Análisis Inferencial: correlación zoonótica TB bovina↔humana y ANOVA de canales de venta"),
    bullet("Data Warehouse: transformación estructurada CSV→JSON con validación Pydantic"),
    bullet("Modelo matemático SIR dual (TB Bovina vs. FMD) mediante integración numérica de EDOs"),
    bullet("Cuantificación del impacto económico con modelos basados en literatura científica"),
    bullet("Arquitectura operativa de despliegue en campo (App + Dashboard NoSQL)"),
  ];
}

module.exports = { buildCover, buildTOC, buildIntro };
