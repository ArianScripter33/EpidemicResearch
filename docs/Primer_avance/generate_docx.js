// generate_docx.js — Ganado Saludable: Primer Avance
// Universidad Nacional "Rosario Castellanos" — Colores: Carmesí #9C223F | Dorado #C9A84C

const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, PageNumber, PageBreak, LevelFormat, TableOfContents,
  UnderlineType, VerticalAlign, convertInchesToTwip
} = require("docx");
const fs = require("fs");

// ─── Paleta UNRC ──────────────────────────────────────────────────────────────
const CRIMSON   = "9C223F";   // Pantone 7420 C — Rojo Carmesí oficial UNRC
const GOLD      = "C9A84C";   // Dorado universitario complementario
const GOLD_LIGHT= "F5E6C4";   // Dorado claro para fondos de tabla
const DARK      = "1A1A2E";   // Casi negro para texto
const WHITE     = "FFFFFF";
const GRAY_LIGHT= "F8F4F0";   // Fondo suave neutro

// ─── Helpers ──────────────────────────────────────────────────────────────────
const pageW = 11906; // A4 width in DXA
const contentW = pageW - 2 * 1440; // 1 inch margins each side → ~9026 DXA

const spacer = (pt = 6) =>
  new Paragraph({ spacing: { before: 0, after: pt * 20 } });

const hRule = () =>
  new Paragraph({
    spacing: { before: 80, after: 80 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: CRIMSON, space: 1 } },
    children: []
  });

const goldRule = () =>
  new Paragraph({
    spacing: { before: 40, after: 40 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: GOLD, space: 1 } },
    children: []
  });

const centeredText = (text, opts = {}) =>
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: opts.spaceBefore ?? 40, after: opts.spaceAfter ?? 40 },
    children: [new TextRun({ text, ...opts })]
  });

const bodyPara = (text, opts = {}) =>
  new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { before: 60, after: 120, line: 360, lineRule: "auto" },
    children: [new TextRun({ text, font: "Arial", size: 22, ...opts })]
  });

const bodyParaRuns = (runs) =>
  new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { before: 60, after: 120, line: 360, lineRule: "auto" },
    children: runs
  });

const run = (text, opts = {}) =>
  new TextRun({ text, font: "Arial", size: 22, ...opts });

const boldRun = (text, opts = {}) =>
  run(text, { bold: true, ...opts });

// ─── Bullet list helper ────────────────────────────────────────────────────────
const bullet = (text, level = 0) =>
  new Paragraph({
    numbering: { reference: "bullets", level },
    alignment: AlignmentType.JUSTIFIED,
    spacing: { before: 40, after: 60, line: 320, lineRule: "auto" },
    children: [new TextRun({ text, font: "Arial", size: 22 })]
  });

const numberedItem = (text, level = 0) =>
  new Paragraph({
    numbering: { reference: "numbers", level },
    alignment: AlignmentType.JUSTIFIED,
    spacing: { before: 40, after: 80, line: 320, lineRule: "auto" },
    children: [new TextRun({ text, font: "Arial", size: 22 })]
  });

// ─── Section heading ──────────────────────────────────────────────────────────
const h1 = (text) =>
  new Paragraph({
    heading: HeadingLevel.HEADING_1,
    pageBreakBefore: true,
    spacing: { before: 200, after: 160 },
    children: [new TextRun({ text, font: "Arial", size: 36, bold: true, color: CRIMSON })]
  });

const h2 = (text) =>
  new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 200, after: 100 },
    children: [new TextRun({ text, font: "Arial", size: 28, bold: true, color: DARK })]
  });

const h3 = (text) =>
  new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 160, after: 80 },
    children: [new TextRun({ text, font: "Arial", size: 24, bold: true, color: CRIMSON, italics: false })]
  });

// ─── Info table for carátula ──────────────────────────────────────────────────
const infoRow = (label, value) =>
  new TableRow({
    children: [
      new TableCell({
        width: { size: 3600, type: WidthType.DXA },
        shading: { fill: CRIMSON, type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 160, right: 160 },
        borders: {
          top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE },
          left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE }
        },
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [new TextRun({ text: label, font: "Arial", size: 20, bold: true, color: WHITE })]
        })]
      }),
      new TableCell({
        width: { size: 5426, type: WidthType.DXA },
        shading: { fill: GRAY_LIGHT, type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 160, right: 160 },
        borders: {
          top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE },
          left: { style: BorderStyle.SINGLE, size: 3, color: GOLD },
          right: { style: BorderStyle.NONE }
        },
        children: [new Paragraph({
          alignment: AlignmentType.LEFT,
          children: [new TextRun({ text: value, font: "Arial", size: 20, color: DARK })]
        })]
      })
    ]
  });

// ─── SECCIONES DEL DOCUMENTO ──────────────────────────────────────────────────

// ── SECCIÓN 1: CARÁTULA (sin header/footer) ──────────────────────────────────
const coverSection = {
  properties: {
    page: {
      size: { width: 11906, height: 16838 },
      margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
    }
  },
  headers: { default: new Header({ children: [new Paragraph("")] }) },
  footers: { default: new Footer({ children: [new Paragraph("")] }) },
  children: [
    // Banda superior carmesí
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 0 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 32, color: CRIMSON, space: 0 } },
      shading: { fill: CRIMSON, type: ShadingType.CLEAR },
      children: [new TextRun({ text: "  ", font: "Arial", size: 48 })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 0 },
      shading: { fill: GOLD, type: ShadingType.CLEAR },
      children: [new TextRun({ text: "  ", font: "Arial", size: 8 })]
    }),
    spacer(24),
    // Institución
    centeredText("Universidad Nacional", {
      font: "Arial", size: 32, bold: false, color: DARK,
      spaceBefore: 60, spaceAfter: 20
    }),
    centeredText('"Rosario Castellanos"', {
      font: "Arial", size: 36, bold: true, color: CRIMSON,
      spaceBefore: 20, spaceAfter: 60
    }),
    centeredText("Licenciatura en Ciencias de Datos para Negocios", {
      font: "Arial", size: 24, bold: false, color: DARK,
      spaceBefore: 20, spaceAfter: 20
    }),
    hRule(),
    spacer(20),
    // Título del proyecto
    centeredText("PROYECTO PROTOTÍPICO", {
      font: "Arial", size: 22, bold: false, color: GOLD,
      underline: { type: UnderlineType.SINGLE, color: GOLD },
      spaceBefore: 40, spaceAfter: 20
    }),
    centeredText("Ganado Saludable", {
      font: "Arial", size: 56, bold: true, color: CRIMSON,
      spaceBefore: 20, spaceAfter: 20
    }),
    centeredText("Primer Avance", {
      font: "Arial", size: 36, bold: true, color: DARK,
      spaceBefore: 20, spaceAfter: 60
    }),
    centeredText("Sistema Integral de Auditoría Epidemiológica Bovina", {
      font: "Arial", size: 24, bold: false, color: DARK, italics: true,
      spaceBefore: 20, spaceAfter: 40
    }),
    goldRule(),
    spacer(20),
    // Tabla de datos del proyecto
    new Table({
      width: { size: 9026, type: WidthType.DXA },
      columnWidths: [3600, 5426],
      rows: [
        infoRow("Fecha:", "26 de marzo de 2026"),
        infoRow("Semestre:", "4° — 2026-1"),
        infoRow("Docente:", "Víctor Hugo Reyes Anselmo"),
        infoRow("Enfermedad Asignada:", "Fiebre Aftosa (FMD) · Calibración: Tuberculosis Bovina"),
        infoRow("Estado de Avance:", "100% — Planificación estratégica y arquitectura ELT"),
      ]
    }),
    spacer(40),
    // Banda inferior dorada
    new Paragraph({
      alignment: AlignmentType.CENTER,
      shading: { fill: GOLD, type: ShadingType.CLEAR },
      children: [new TextRun({ text: "  ", font: "Arial", size: 8 })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      shading: { fill: CRIMSON, type: ShadingType.CLEAR },
      children: [new TextRun({ text: "  ", font: "Arial", size: 40 })]
    }),
  ]
};

// ── SECCIÓN 2: ÍNDICE ─────────────────────────────────────────────────────────
const tocSection = {
  properties: {
    page: {
      size: { width: 11906, height: 16838 },
      margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
    }
  },
  headers: {
    default: new Header({
      children: [
        new Paragraph({
          alignment: AlignmentType.RIGHT,
          border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: GOLD, space: 1 } },
          children: [
            new TextRun({ text: "Ganado Saludable — Primer Avance  |  UNRC 2026-1", font: "Arial", size: 18, color: CRIMSON, italics: true })
          ]
        })
      ]
    })
  },
  footers: {
    default: new Footer({
      children: [
        new Paragraph({
          alignment: AlignmentType.CENTER,
          border: { top: { style: BorderStyle.SINGLE, size: 4, color: CRIMSON, space: 1 } },
          children: [
            new TextRun({ text: "Página ", font: "Arial", size: 18, color: DARK }),
            new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: CRIMSON }),
            new TextRun({ text: " de ", font: "Arial", size: 18, color: DARK }),
            new TextRun({ children: [PageNumber.TOTAL_PAGES], font: "Arial", size: 18, color: DARK }),
          ]
        })
      ]
    })
  },
  children: [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 160 },
      children: [new TextRun({ text: "Índice de Contenidos", font: "Arial", size: 44, bold: true, color: CRIMSON })]
    }),
    goldRule(),
    spacer(8),
    new TableOfContents("", {
      hyperlink: true,
      headingStyleRange: "1-3",
      stylesWithLevels: []
    }),
  ]
};

// ── SECCIÓN 3: CUERPO DEL DOCUMENTO ──────────────────────────────────────────
const bodySection = {
  properties: {
    page: {
      size: { width: 11906, height: 16838 },
      margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
    }
  },
  headers: {
    default: new Header({
      children: [
        new Paragraph({
          alignment: AlignmentType.RIGHT,
          border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: GOLD, space: 1 } },
          children: [
            new TextRun({ text: "Ganado Saludable — Primer Avance  |  UNRC 2026-1", font: "Arial", size: 18, color: CRIMSON, italics: true })
          ]
        })
      ]
    })
  },
  footers: {
    default: new Footer({
      children: [
        new Paragraph({
          alignment: AlignmentType.CENTER,
          border: { top: { style: BorderStyle.SINGLE, size: 4, color: CRIMSON, space: 1 } },
          children: [
            new TextRun({ text: "Página ", font: "Arial", size: 18, color: DARK }),
            new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: CRIMSON }),
            new TextRun({ text: " de ", font: "Arial", size: 18, color: DARK }),
            new TextRun({ children: [PageNumber.TOTAL_PAGES], font: "Arial", size: 18, color: DARK }),
          ]
        })
      ]
    })
  },
  children: [

    // ── 1. INTRODUCCIÓN ──────────────────────────────────────────────────────
    h1("1. Introducción y Contexto"),
    bodyPara(
      "Este proyecto, titulado Ganado Saludable, propone una infraestructura de auditoría sistémica de " +
      "externalidades bovinas en México. Bajo el enfoque One Health (Una Sola Salud), se busca integrar " +
      "datos de sanidad animal, salud pública y finanzas para prevenir crisis epidemiológicas catastróficas."
    ),

    h2("1.1 Alerta Global 2026 — Actualización de Investigación"),
    bodyPara(
      "Nuestra investigación de campo y monitoreo de fuentes internacionales (FAO/WOAH) revela que en " +
      "marzo de 2026 se han confirmado brotes críticos de Fiebre Aftosa (FMD) en las siguientes regiones:"
    ),
    bullet("Chipre (Lárnaca): 49 unidades afectadas, más de 26,000 cabezas sacrificadas."),
    bullet("Grecia (Lesbos): primer brote detectado desde 2001."),
    bullet("Israel (Golán): identificación del serotipo SAT1."),
    spacer(6),
    bodyPara(
      "Esta coyuntura hace que nuestra enfermedad asignada —la Fiebre Aftosa— sea de máxima relevancia " +
      "para la seguridad nacional agropecuaria de México, país libre de la enfermedad desde 1954, pero " +
      "cuya vulnerabilidad ante una reintroducción es crítica."
    ),

    // ── 2. PLANTEAMIENTO ─────────────────────────────────────────────────────
    h1("2. Planteamiento del Problema"),
    bodyPara(
      "México posee una biomasa bovina de 35.1 millones de cabezas. Un brote de fiebre aftosa no " +
      "representaría solo una crisis sanitaria, sino un bloqueo comercial total de exportaciones de carne, " +
      "con un impacto económico proyectado de $200,000 millones de pesos (basado en la progresión del " +
      "brote del Reino Unido en 2001, ajustado a la biomasa mexicana)."
    ),

    h2("2.1 Incidentes Críticos Identificados"),
    numberedItem("Ciberseguridad: intercepción maliciosa de datos IoT para enmascarar brotes."),
    numberedItem("Incertidumbre Epidemiológica: incapacidad de predecir la velocidad de contagio (R0)."),
    numberedItem("Riesgo Financiero: subestimación del costo de reacción versus prevención primaria."),

    // ── 3. OBJETIVOS ─────────────────────────────────────────────────────────
    h1("3. Objetivos"),
    h2("3.1 Objetivo General"),
    bodyPara(
      "Diseñar e implementar un sistema integral de monitoreo y alerta temprana que utilice Ciencia de " +
      "Datos, IA y Modelado Matemático para anticipar el impacto de la Fiebre Aftosa en México, " +
      "utilizando la Tuberculosis Bovina como métrica de calibración."
    ),

    h2("3.2 Objetivos Específicos — Alineación con Materias"),

    h3("1. Inteligencia Artificial"),
    bodyPara(
      "Entrenar un modelo de machine learning (XGBoost Clasificador) diseñado para estimar la " +
      "probabilidad de brotes (identificados bajo CIE-10 A05). Las variables predictoras (features) " +
      "incluirán determinantes no convencionales como el volumen de alimento procesado y un innovador " +
      "\"Proxy de Opacidad\": el número de clausuras efectuadas por COFEPRIS debido a infracciones " +
      "vinculadas al clembuterol u otros LMR (Límites Máximos de Residuos)."
    ),

    h3("2. Estadística Multivariada"),
    bodyPara(
      "Implementar esquemas visuales para la identificación de perfiles de riesgo epidemiológico " +
      "(agrupaciones o clusters) a nivel estatal empleando Análisis de Componentes Principales (PCA) " +
      "para lidiar con altas dimensionalidades. Se reforzará con gráficos como las Curvas de Andrews " +
      "y representaciones antropomórficas como las Caras de Chernoff, con el objetivo de facilitar " +
      "el entendimiento de patrones geográficos donde se combinan variables críticas."
    ),

    h3("3. Ecuaciones Diferenciales"),
    bodyPara(
      "Traducir escenarios biológicos en la formulación de sistemas dinámicos tipo SIR " +
      "(Susceptibles-Infectados-Recuperados). La modelación se efectuará operando el sistema primero " +
      "en su fase pasiva-analítica con los ratios infecciosos de tuberculosis (calibración, R0 ≈ 1.8), " +
      "iterándolo mediante las derivadas aplicables al escenario prospectivo ante Fiebre Aftosa (R0 ≈ 6.0)."
    ),

    h3("4. Bases de Datos NoSQL"),
    bodyPara(
      "Migrar la administración de entidades de información altamente variopinta (PDFs crudos, datasets " +
      "del DGE/SINAIS) a colecciones soportadas mediante un clúster de bases documentales distribuidas, " +
      "específicamente MongoDB. Este sistema estructurará el DWH asimilando métricas procedentes de " +
      "los extractores generados bajo el modelo Star-Schema (estrella)."
    ),

    h3("5. Criptografía"),
    bodyPara(
      "Asegurar la trazabilidad mediante algoritmos para anonimizar los identificadores que viajen " +
      "hacia la analítica. Incorporará codificación en bloques (Cifrado César) a modo de ofuscación " +
      "de entidades (lotes de seguimiento), más criptosistemas de firma robusta de claves asimétricas " +
      "(RSA) como mecanismo que resista falsificaciones maliciosas contra ecosistemas IoT ganaderos."
    ),

    h3("6. Finanzas Corporativas"),
    bodyPara(
      "Justificar fiscal y corporativamente el costo del ecosistema al trazar los análisis determinantes " +
      "(TIR o VPN — Valor Presente Neto) como justificación. El fin será contraponer el desembolso por " +
      "la tecnología de monitorización versus los más de $200,000 millones probables extraídos del PIB " +
      "del país por la reintroducción de la Fiebre Aftosa (FMD)."
    ),

    h3("7. Innovación Social"),
    bodyPara(
      "Posibilitar que las analíticas generen intervenciones asertivas integrales basadas en el concepto " +
      "One Health, protegiendo la carga económica familiar desproporcionada que recae sobre las " +
      "poblaciones subrepresentadas de rastros y mercados en zonas endémicas por descuidos en " +
      "inocuidad alimentaria."
    ),

    // ── 4. MARCO TEÓRICO ─────────────────────────────────────────────────────
    h1("4. Marco Teórico y Avance de Investigación"),

    h2("4.1 Estrategia de Calibración — Proxy Epidemiológico"),
    bodyPara(
      "Dado que México ostenta el estatus de país libre de Fiebre Aftosa (FMD) sin vacunación desde 1954, " +
      "no resulta posible ingerir datos históricos locales provenientes de este patógeno para modelar su " +
      "propagación. La propuesta metodológica innovadora radica en utilizar a la Tuberculosis Bovina (TB) " +
      "—zoonosis grave con dinámica endémica en México a la cual se destinan hasta $300 millones de pesos " +
      "anuales dentro de la fiscalización del Estado— como entidad de calibración (Proxy Epidemiológico). " +
      "La mecánica transcurrirá con el siguiente orden:"
    ),
    numberedItem(
      "Calibración TB Bovina: la asimilación al sistema biológico con los datos empíricos procedentes " +
      "de las acciones de SENASICA producirán los determinantes para la función matemática con un índice " +
      "de propagación moderada estimada en R0 ≈ 1.8."
    ),
    numberedItem(
      "Transfer Learning Viral (FMD): una vez afinada la mecánica en México con datos de tuberculosis " +
      "en Python, las métricas predictivas recibirán un incremento (factor de aceleración exógena) basado " +
      "en cifras paramétricas de casos extremos extranjeros, situando la Fiebre Aftosa en R0 ≈ 6.0."
    ),
    numberedItem(
      "Replicabilidad Cuantitativa: la experimentación derivará simulaciones precisas sobre el efecto " +
      "destructivo de una reactivación epidemiológica generalizada de esta zoonosis foránea."
    ),

    h2("4.2 Fuentes de Datos Auditadas — Módulos ETL"),
    bodyPara(
      "El marco actual de fuentes estructuradas, a menudo albergadas de forma dispersa con esquemas " +
      "tecnológicos hostiles (como el control ActiveX del gobierno y sitios de dinámica JavaScript en " +
      "la Plataforma Nacional de Transparencia PNT), estipularon las vías siguientes como canales de " +
      "rastreo del data lake principal:"
    ),
    bullet(
      "SENASICA: monitoreo desde repositorios y la API encubierta (JSON/CSV) de las detecciones de hatos " +
      "en seguimiento o los PDFs con registros de cuarentenas ejecutadas."
    ),
    bullet(
      "Instituto Nacional DGE/SINAIS: captura tabulada desde Anuarios de salud oficial de incidencias de " +
      "zoonosis cruzadas y fallecimientos reportados bajo listados de morbilidad humana (CIE-10), mapeados " +
      "por correlación departamental/regional con eventos del animal."
    ),
    bullet(
      "OpenFMD / Institutos Internacionales: repositorios de datos con series de evolución viral " +
      "(brotes 2026 en Europa y Sudamérica), de extrema importancia para algoritmos de Series de Tiempo " +
      "como AWS Chronos."
    ),
    bullet(
      "PUCRA (UNAM): exposición de datos biológicos sobre RAM (Resistencia a Antimicrobianos) en PDFs; " +
      "como el 94% de insensibilidad del microbio a la ampicilina encontrado a nivel mercado comercial."
    ),
    bullet(
      "PNT / COFEPRIS (Scraping): generación de spiders/bots de web-scraping en navegador Headless " +
      "(Selenium) que identifique resoluciones coercitivas, determinando actas con detección de fallos " +
      "por presencia de clembuterol o niveles anómalos de salmonela."
    ),

    // ── 5. INSTRUMENTACIÓN ANALÍTICA ─────────────────────────────────────────
    h1("5. Instrumentación Analítica"),

    h2("5.1 Análisis de Componentes Principales (PCA)"),
    bodyPara(
      "Las variables de alta dimensionalidad —densidad ganadera, clausuras LMR, ventas clandestinas, " +
      "carga antibiótica en rastros— se sintetizan mediante PCA, explicando más del 70% de la varianza " +
      "en dos o tres componentes principales. Esto revela correlaciones latentes entre regiones como " +
      "Jalisco y Veracruz, no contiguas geográficamente pero sí operativamente en bioseguridad deficiente."
    ),

    h2("5.2 Visualizaciones Multivariadas"),
    bodyParaRuns([
      boldRun("Curvas de Andrews: "),
      run("cada entidad federativa se representa mediante transformaciones de la serie de Fourier, " +
          "graficadas como líneas de oscilación variable para localizar clusters de riesgo y outliers."),
    ]),
    spacer(4),
    bodyParaRuns([
      boldRun("Caras de Chernoff: "),
      run("variables complejas (ratios de prevalencia, RAM, infecciones A05) se traducen a rasgos " +
          "antropomórficos para facilitar la identificación facial de perfiles de riesgo en reportes " +
          "dirigidos a personal de políticas públicas sin formación en ML."),
    ]),

    h2("5.3 Modelo XGBoost Clasificador"),
    bodyParaRuns([
      boldRun("Input (Features): "),
      run("conteo de patógenos cruzados (Salmonelosis DGE/SINAIS), hatos libres detectados y el " +
          "Proxy de Opacidad de clausuras por clembuterol."),
    ]),
    spacer(4),
    bodyParaRuns([
      boldRun("Output (Target): "),
      run("métrica AUC de riesgo predicho para subidas de intoxicaciones alimentarias y diseminación " +
          "zoonótica. La interpretabilidad vía SHAP localiza las features de mayor peso predictivo."),
    ]),

    // ── 6. ARQUITECTURA ELT ───────────────────────────────────────────────────
    h1("6. Propuesta Metodológica — Arquitectura ELT"),
    bodyPara(
      "La instrumentación de software del proyecto recae sobre una infraestructura ELT " +
      "(Extract-Load-Transform) orquestada que materializa la visión de la Auditoría Sistémica. " +
      "La línea de procesamiento obedece al formato dimensional (Data Warehouse):"
    ),
    numberedItem(
      "Submódulo de Extracción Transaccional: programación dual de módulos Python (\"Arañas Asíncronas\" " +
      "basadas en Playwright headless) frente a interrupciones o modales interactivos en sitios como " +
      "la PNT. Estas se suman a conexiones por Requests que acceden a las APIs del SENASICA, vulnerando " +
      "las restricciones artificiales del gobierno que solo habilitan visores como OWC11 (Microsoft " +
      "ActiveX) de los años 90."
    ),
    numberedItem(
      "Capa Data Lake / Capa Oro NoSQL (MongoDB): todos los reportes PDF transcritos mediante metodologías " +
      "heurísticas OCR (Camelot / pdfplumber), junto con los datasets numéricos de APIs desofuscadas de " +
      "JSON, quedan anclados en un repositorio NoSQL normalizado según el modelo Star-Schema " +
      "(fact_tiempo, fact_geografia)."
    ),
    numberedItem(
      "Analíticas e Ingeniería Matemática (SciPy): diferentes pipelines emplearán la solución de " +
      "Runge-Kutta sobre scipy.integrate.odeint, derivando los puntos de corte en las curvas de " +
      "propagación SIR para estimar en modo predictivo el instante de un desbordamiento al brote " +
      "pandémico nacional."
    ),
    numberedItem(
      "Visor Diagnóstico Automatizado (Dashboard): las gráficas derivadas de Matplotlib/Plotly " +
      "mostrarán correlaciones sobre mapas coropléticos que permitirán a cualquier miembro calificador " +
      "del Coloquio constatar cómo una simulación financiera y biológica puede proteger el entorno nacional."
    ),

    // ── 7. BIBLIOGRAFÍA ────────────────────────────────────────────────────────
    h1("7. Bibliografía"),
    // APA 7: títulos de obras en itálica
    bodyParaRuns([
      run("FAO. (2026). "),
      run("Update on Foot-and-Mouth Disease outbreaks in Europe and the Near East", { italics: true }),
      run(". Organización de las Naciones Unidas para la Alimentación y la Agricultura."),
    ]),
    bodyParaRuns([
      run("WOAH. (2026). "),
      run("Emergence of FMD Serotype SAT1 in the Golan region: Regional implications", { italics: true }),
      run(". Organización Mundial de Sanidad Animal."),
    ]),
    bodyParaRuns([
      run("Brauer, F., & Castillo-Chávez, C. (2012). "),
      run("Mathematical Models in Population Biology and Epidemiology", { italics: true }),
      run(". Springer."),
    ]),
    bodyParaRuns([
      run("SENASICA. (2024). "),
      run("Boletín Trimestral de Cuarentenas de Tuberculosis Bovina", { italics: true }),
      run(". Servicio Nacional de Sanidad, Inocuidad y Calidad Agroalimentaria."),
    ]),
    bodyParaRuns([
      run("Russell, S., & Norvig, P. (2021). "),
      run("Artificial Intelligence: A Modern Approach", { italics: true }),
      run(" (4.ª ed.). Pearson."),
    ]),

    // ── 8. ENTREGABLES Y ESTRATEGIA MVP ──────────────────────────────────────
    h1("8. Entregables Finales — Estrategia MVP"),
    bodyPara(
      "Alineados con los requerimientos del Problema Prototípico, la ejecución opera bajo una estrategia " +
      "de Producto Mínimo Viable (MVP). Toda la infraestructura técnica es instrumental para los dos " +
      "entregables definitivos:"
    ),
    h2("8.1 Artículo de Divulgación Científica"),
    bodyPara(
      "Documento maestro de 15 a 25 páginas en formato APA 7 con mínimo 5 fuentes. Sintetizará el " +
      "cumplimiento de las 7 materias con énfasis en Innovación Social: test ANOVA demostrando " +
      "desigualdad estadística (prevalencia 22.3% en tianguis vs. 1.3% en supermercados corporativos)."
    ),
    h2("8.2 Exposición en Coloquio"),
    bodyPara(
      "Presentación digital de 15 a 20 diapositivas (Gamma / Genially) con Impacto Visual Base: " +
      "gráficas SIR comparativas TB vs. FMD, simplificando Ecuaciones Diferenciales para un jurado " +
      "multidisciplinario."
    ),

    // ── ESTADO DE AVANCE ─────────────────────────────────────────────────────
    spacer(20),
    hRule(),
    spacer(8),
    new Table({
      width: { size: 9026, type: WidthType.DXA },
      columnWidths: [4513, 4513],
      rows: [
        new TableRow({
          children: [
            new TableCell({
              columnSpan: 2,
              shading: { fill: CRIMSON, type: ShadingType.CLEAR },
              margins: { top: 100, bottom: 100, left: 200, right: 200 },
              borders: {
                top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE },
                left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE }
              },
              children: [new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [new TextRun({ text: "Estado de Avance del Proyecto", font: "Arial", size: 24, bold: true, color: WHITE })]
              })]
            })
          ]
        }),
        new TableRow({
          children: [
            new TableCell({
              width: { size: 4513, type: WidthType.DXA },
              shading: { fill: GOLD_LIGHT, type: ShadingType.CLEAR },
              margins: { top: 80, bottom: 80, left: 160, right: 160 },
              borders: {
                top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.SINGLE, size: 2, color: GOLD },
                left: { style: BorderStyle.NONE }, right: { style: BorderStyle.SINGLE, size: 2, color: GOLD }
              },
              children: [new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [new TextRun({ text: "Planificación Estratégica", font: "Arial", size: 22, bold: true, color: DARK })]
              })]
            }),
            new TableCell({
              width: { size: 4513, type: WidthType.DXA },
              shading: { fill: GOLD_LIGHT, type: ShadingType.CLEAR },
              margins: { top: 80, bottom: 80, left: 160, right: 160 },
              borders: {
                top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.SINGLE, size: 2, color: GOLD },
                left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE }
              },
              children: [new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [new TextRun({ text: "100% Completado ✓", font: "Arial", size: 22, bold: true, color: CRIMSON })]
              })]
            })
          ]
        }),
        new TableRow({
          children: [
            new TableCell({
              width: { size: 4513, type: WidthType.DXA },
              shading: { fill: GOLD_LIGHT, type: ShadingType.CLEAR },
              margins: { top: 80, bottom: 80, left: 160, right: 160 },
              borders: {
                top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE },
                left: { style: BorderStyle.NONE }, right: { style: BorderStyle.SINGLE, size: 2, color: GOLD }
              },
              children: [new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [new TextRun({ text: "Arquitectura ELT y Diseño", font: "Arial", size: 22, bold: true, color: DARK })]
              })]
            }),
            new TableCell({
              width: { size: 4513, type: WidthType.DXA },
              shading: { fill: GOLD_LIGHT, type: ShadingType.CLEAR },
              margins: { top: 80, bottom: 80, left: 160, right: 160 },
              borders: {
                top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE },
                left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE }
              },
              children: [new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [new TextRun({ text: "100% Completado ✓", font: "Arial", size: 22, bold: true, color: CRIMSON })]
              })]
            })
          ]
        })
      ]
    }),
    spacer(8),
    hRule(),
  ]
};

// ─── DOCUMENTO FINAL ──────────────────────────────────────────────────────────
const doc = new Document({
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "\u2022",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      },
      {
        reference: "numbers",
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: "%1.",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      }
    ]
  },
  styles: {
    default: {
      document: { run: { font: "Arial", size: 22 } }
    },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Arial", color: CRIMSON },
        paragraph: { spacing: { before: 200, after: 160 }, outlineLevel: 0 }
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: DARK },
        paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 1 }
      },
      {
        id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial", color: CRIMSON },
        paragraph: { spacing: { before: 160, after: 80 }, outlineLevel: 2 }
      }
    ]
  },
  sections: [coverSection, tocSection, bodySection]
});

// ─── OUTPUT ───────────────────────────────────────────────────────────────────
const outputPath = "docs/Ganado_Saludable_Primer_Avance.docx";
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(outputPath, buffer);
  console.log(`✅ DOCX generado: ${outputPath}`);
}).catch(err => {
  console.error("❌ Error:", err.message);
  process.exit(1);
});
