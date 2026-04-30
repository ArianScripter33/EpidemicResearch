const fs = require("fs");
const path = require("path");
const { Document, Packer, HeadingLevel, LevelFormat, AlignmentType } = require("docx");

const { headerFooter, img, imgCaption, spacer, C, D } = require("./docx_helpers");
const { buildCover, buildTOC, buildIntro } = require("./docx_part1_cover");
const { buildPipeline } = require("./docx_part2_pipeline");
const { buildEDA } = require("./docx_part3_eda");
const { buildStats } = require("./docx_part4_stats");
const { buildSIR } = require("./docx_part5_sir");
const { buildEconomics, buildOpsStatusBiblio } = require("./docx_part6_econ_ops");

async function main() {
  console.log("🔨 Generando Segundo Avance DOCX...");

  const kpiDash = [
    img("../figures/kpi_dashboard.png", 6.5, 2.5),
    imgCaption("Panel de Indicadores Clave del Proyecto Ganado Saludable."),
    spacer(10),
  ];

  const doc = new Document({
    styles: {
      default: { document: { run: { font: "Arial", size: 22 } } },
      paragraphStyles: [
        {
          id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 36, bold: true, font: "Arial", color: C },
          paragraph: { spacing: { before: 200, after: 160 }, outlineLevel: 0 }
        },
        {
          id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 28, bold: true, font: "Arial", color: D },
          paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 1 }
        },
        {
          id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 24, bold: true, font: "Arial", color: C },
          paragraph: { spacing: { before: 160, after: 80 }, outlineLevel: 2 }
        },
      ]
    },
    numbering: {
      config: [
        {
          reference: "bullets",
          levels: [{
            level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } }
          }]
        },
        {
          reference: "numbers",
          levels: [{
            level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } }
          }]
        },
      ]
    },
    sections: [{
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
        }
      },
      ...headerFooter(),
      children: [
        ...buildCover(),
        ...buildTOC(),
        ...kpiDash,
        ...buildIntro(),
        ...buildPipeline(),
        ...buildEDA(),
        ...buildStats(),
        ...buildSIR(),
        ...buildEconomics(),
        ...buildOpsStatusBiblio(),
      ]
    }]
  });

  const buffer = await Packer.toBuffer(doc);
  const outPath = path.join(__dirname, "Ganado_Saludable_Segundo_Avance.docx");
  fs.writeFileSync(outPath, buffer);
  console.log(`✅ Generado: ${outPath}`);
  console.log(`📦 Tamaño: ${(buffer.length / 1024).toFixed(1)} KB`);
}

main().catch(err => { console.error("❌ Error:", err); process.exit(1); });
