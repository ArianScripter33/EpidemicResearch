const {
  Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, PageNumber, LevelFormat, TableOfContents
} = require("docx");
const fs = require("fs");
const path = require("path");

const C = "#9C223F", G = "#C9A84C", GL = "#F5E6C4", D = "1A1A2E", W = "FFFFFF", GR = "F8F4F0";

const spacer = (pt = 6) => new Paragraph({ spacing: { before: 0, after: pt * 20 } });

const hRule = () => new Paragraph({
  spacing: { before: 80, after: 80 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: C, space: 1 } }, children: []
});

const goldRule = () => new Paragraph({
  spacing: { before: 40, after: 40 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: G, space: 1 } }, children: []
});

const centered = (text, opts = {}) => new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: opts.spaceBefore ?? 40, after: opts.spaceAfter ?? 40 },
  children: [new TextRun({ text, font: "Arial", size: 22, ...opts })]
});

const body = (text, opts = {}) => new Paragraph({
  alignment: AlignmentType.JUSTIFIED,
  spacing: { before: 60, after: 120, line: 360, lineRule: "auto" },
  children: [new TextRun({ text, font: "Arial", size: 22, ...opts })]
});

const bodyRuns = (runs) => new Paragraph({
  alignment: AlignmentType.JUSTIFIED,
  spacing: { before: 60, after: 120, line: 360, lineRule: "auto" },
  children: runs
});

const r = (text, opts = {}) => new TextRun({ text, font: "Arial", size: 22, ...opts });
const b = (text, opts = {}) => r(text, { bold: true, ...opts });

const bullet = (text, level = 0) => new Paragraph({
  numbering: { reference: "bullets", level },
  alignment: AlignmentType.JUSTIFIED,
  spacing: { before: 40, after: 60, line: 320, lineRule: "auto" },
  children: [r(text)]
});

const numbered = (text, level = 0) => new Paragraph({
  numbering: { reference: "numbers", level },
  alignment: AlignmentType.JUSTIFIED,
  spacing: { before: 40, after: 80, line: 320, lineRule: "auto" },
  children: [r(text)]
});

const h1 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_1, pageBreakBefore: true,
  spacing: { before: 200, after: 160 },
  children: [new TextRun({ text, font: "Arial", size: 36, bold: true, color: C })]
});

const h2 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_2,
  spacing: { before: 200, after: 100 },
  children: [new TextRun({ text, font: "Arial", size: 28, bold: true, color: D })]
});

const h3 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_3,
  spacing: { before: 160, after: 80 },
  children: [new TextRun({ text, font: "Arial", size: 24, bold: true, color: C })]
});

const bdr = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: bdr, bottom: bdr, left: bdr, right: bdr };
const noBorders = { top: {style:BorderStyle.NONE}, bottom: {style:BorderStyle.NONE}, left: {style:BorderStyle.NONE}, right: {style:BorderStyle.NONE} };
const cellMargins = { top: 80, bottom: 80, left: 120, right: 120 };

function makeTable(headers, rows, colWidths) {
  const totalW = colWidths.reduce((a, b) => a + b, 0);
  const headerRow = new TableRow({
    children: headers.map((h, i) => new TableCell({
      width: { size: colWidths[i], type: WidthType.DXA }, borders, margins: cellMargins,
      shading: { fill: C, type: ShadingType.CLEAR },
      children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: h, font: "Arial", size: 20, bold: true, color: W })] })]
    }))
  });
  const dataRows = rows.map((row, ri) => new TableRow({
    children: row.map((cell, ci) => new TableCell({
      width: { size: colWidths[ci], type: WidthType.DXA }, borders, margins: cellMargins,
      shading: { fill: ri % 2 === 0 ? GR : W, type: ShadingType.CLEAR },
      children: [new Paragraph({ children: [new TextRun({ text: String(cell), font: "Arial", size: 20 })] })]
    }))
  }));
  return new Table({ width: { size: totalW, type: WidthType.DXA }, columnWidths: colWidths, rows: [headerRow, ...dataRows] });
}

function img(filePath, widthInches, heightInches) {
  const absPath = path.resolve(__dirname, filePath);
  if (!fs.existsSync(absPath)) { return body(`[Imagen no encontrada: ${filePath}]`, { italics: true, color: "999999" }); }
  const ext = path.extname(absPath).slice(1).toLowerCase();
  return new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { before: 120, after: 120 },
    children: [new ImageRun({
      type: ext === "jpg" ? "jpeg" : ext, data: fs.readFileSync(absPath),
      transformation: { width: widthInches * 72, height: heightInches * 72 },
      altText: { title: path.basename(absPath), description: path.basename(absPath), name: path.basename(absPath) }
    })]
  });
}

function imgCaption(text) {
  return new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { before: 40, after: 160 },
    children: [new TextRun({ text, font: "Arial", size: 18, italics: true, color: "666666" })]
  });
}

const infoRow = (label, value) => new TableRow({
  children: [
    new TableCell({
      width: { size: 3600, type: WidthType.DXA },
      shading: { fill: C, type: ShadingType.CLEAR }, margins: { top: 80, bottom: 80, left: 160, right: 160 }, borders: noBorders,
      children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: label, font: "Arial", size: 20, bold: true, color: W })] })]
    }),
    new TableCell({
      width: { size: 5426, type: WidthType.DXA },
      shading: { fill: GR, type: ShadingType.CLEAR }, margins: { top: 80, bottom: 80, left: 160, right: 160 },
      borders: { ...noBorders, left: { style: BorderStyle.SINGLE, size: 3, color: G } },
      children: [new Paragraph({ children: [new TextRun({ text: value, font: "Arial", size: 20, color: D })] })]
    })
  ]
});

const headerFooter = () => ({
  headers: { default: new Header({ children: [new Paragraph({
    alignment: AlignmentType.RIGHT,
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: G, space: 1 } },
    children: [new TextRun({ text: "Ganado Saludable — Segundo Avance  |  UNRC 2026-1", font: "Arial", size: 18, color: C, italics: true })]
  })] }) },
  footers: { default: new Footer({ children: [new Paragraph({
    alignment: AlignmentType.CENTER,
    border: { top: { style: BorderStyle.SINGLE, size: 4, color: C, space: 1 } },
    children: [
      new TextRun({ text: "Página ", font: "Arial", size: 18, color: D }),
      new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: C }),
      new TextRun({ text: " de ", font: "Arial", size: 18, color: D }),
      new TextRun({ children: [PageNumber.TOTAL_PAGES], font: "Arial", size: 18, color: D }),
    ]
  })] }) }
});

module.exports = { C, G, GL, D, W, GR, spacer, hRule, goldRule, centered, body, bodyRuns, r, b, bullet, numbered, h1, h2, h3, makeTable, img, imgCaption, infoRow, headerFooter, noBorders };
