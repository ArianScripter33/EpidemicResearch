const { spacer, body, bodyRuns, r, b, bullet, h1, h2, h3, makeTable, img, imgCaption } = require("./docx_helpers");

function buildEDA() {
  return [
    h1("3. Hallazgos del Análisis Exploratorio (EDA)"),
    bodyRuns([b("Notebook de referencia: "), r("notebooks/01_eda_global.ipynb")]),

    h2("3.1 COVID-19 validó la hipótesis de canales de venta"),
    body("La serie temporal DGE 2015-2024 revela una anomalía natural que funciona como grupo de control involuntario:"),
    makeTable(
      ["Año", "Intoxicaciones Alimentarias (A05)", "Tuberculosis (A15-A19)"],
      [["2019", "31,916", "22,283"], ["2020", "18,667 (−41.5%)", "16,747 (−24.8%)"], ["2024", "25,259", "25,980"]],
      [1800, 3800, 3426]
    ),
    spacer(4),
    body("Cuando México cerró tianguis, mercados informales y cadenas de comida callejera durante 2020, las intoxicaciones alimentarias colapsaron un 41.5%. La tuberculosis cayó solo un 24.8% (transmisión respiratoria). Esto demuestra que los canales de venta informales son el vector primario de contagio alimentario."),
    img("../../data/processed/eda_charts/dge_tendencia_temporal.png", 6.2, 3.8),
    imgCaption("Figura 1. Serie temporal DGE 2015-2024 con banda COVID-19."),

    h2("3.2 Cobertura del programa TB Bovina: Solo el 1.2%"),
    body("El programa SENASICA ha certificado 420,171 bovinos como libres de tuberculosis, de una biomasa nacional de 35,100,000. Cobertura: 1.20%. El 98.8% del hato opera en oscuridad estadística."),
    img("../../data/processed/eda_charts/senasica_hatos_libres.png", 6.2, 3.8),
    imgCaption("Figura 2. Top 15 estados por bovinos certificados libres de TB."),

    h2("3.3 Cuarentenas SENASICA 2024: Jalisco concentra el 66.6%"),
    body("27 de 32 estados tienen hatos bajo cuarentena activa: 856 hatos y 7,558 animales afectados. Jalisco concentra el 66.6% de los animales afectados (5,035) con solo el 15.8% de los hatos, sugiriendo concentración en unidades de producción grandes."),
    img("../../data/processed/eda_charts/senasica_cuarentenas_estado.png", 6.2, 3.8),
    imgCaption("Figura 3. Hatos y animales cuarentenados por estado (SENASICA 2024)."),

    h2("3.4 Las Américas: Inmunológicamente vírgenes a FMD"),
    body("De 16,540 eventos FMD positivos globalmente (2000-2025), las Américas representan solo el 2.7%. México, libre desde 1954, tiene una biomasa 100% susceptible."),
    img("../../data/processed/eda_charts/openfmd_region_serotipos.png", 6.2, 3.8),
    imgCaption("Figura 4. Distribución global de brotes FMD por región y serotipo."),

    h2("3.5 Serotipo O domina el 55% de las epidemias globales"),
    body("El serotipo O (9,072 eventos, 54.9% del total) es el mismo que devastó al Reino Unido en 2001. Esto parametriza nuestro modelo SIR con R₀ = 6.0."),
    img("../../data/processed/eda_charts/openfmd_serotipos_pie.png", 4.5, 3.5),
    imgCaption("Figura 5. Distribución de serotipos FMD a nivel global."),

    h2("3.6 Opacidad regulatoria como indicador de riesgo"),
    body("COFEPRIS no publica datos granulares sobre clausuras alimentarias con detalle de contaminantes. Se recuperaron 12 procedimientos de sanción, de los cuales 7 son explícitamente cárnicas. Si las empresas más grandes del sector no escapan sanciones, la cadena informal opera en un vacío de vigilancia total."),
  ];
}

module.exports = { buildEDA };
