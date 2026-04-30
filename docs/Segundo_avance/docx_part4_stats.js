const { spacer, body, bodyRuns, r, b, bullet, h1, h2, h3, makeTable, img, imgCaption } = require("./docx_helpers");

function buildStats() {
  return [
    h1("4. Análisis Estadístico del Equipo"),

    h2("4.1 Análisis Descriptivo: Top 5 Países FMD en África"),
    bodyRuns([b("Notebook: "), r("notebooks/02_analisis_descriptivo.ipynb — Aporte de la Miembro 2 del equipo (Victoria).")]),
    body("Se filtraron 10,606 eventos FMD positivos confirmados en la región africana (2000-2025) del dataset openFMD, aplicando técnicas de Data Binning por décadas y generando estadísticas descriptivas."),
    spacer(4),
    makeTable(
      ["#", "País", "Brotes FMD Confirmados"],
      [["1", "Algeria", "1,308"], ["2", "Zimbabwe", "1,061"], ["3", "Sudáfrica", "971"], ["4", "Kenya", "914"], ["5", "Egipto", "765"]],
      [800, 4200, 4026]
    ),
    spacer(6),
    bodyRuns([b("Data Binning por Décadas:")]),
    makeTable(
      ["Década", "Brotes en África"],
      [["2000s", "1,208"], ["2010s", "3,154"], ["2020s", "762"]],
      [4500, 4526]
    ),
    spacer(4),
    bodyRuns([b("Hallazgo clave: "), r("Los brotes en la década de los 2010s fueron 2.6 veces mayores que en los 2000s. La aparente caída en los 2020s responde al fenómeno de Right-Censoring (rezago de reporte del WRLFMD), no a una mejora epidemiológica real.")]),
    img("../figures/top5_africa_fmd.png", 6.2, 3.8),
    imgCaption("Figura 6. Top 5 países de África con mayor incidencia de Fiebre Aftosa (2000-2025)."),

    h2("4.2 Análisis Inferencial: Correlación Zoonótica y ANOVA"),
    bodyRuns([b("Notebook: "), r("notebooks/03_analisis_inferencial.ipynb — Aporte de la Miembro 2 del equipo (Victoria).")]),
    body("Se realizaron dos pruebas inferenciales:"),

    h3("A. Correlación cruzada TB Bovina ↔ TB Humana"),
    body("Se cruzaron los datos de animales en cuarentena por TB bovina (SENASICA, n=26 estados) con los casos acumulados de tuberculosis humana (DGE, CIE-10 A15-A19, 2015-2017)."),
    spacer(2),
    bullet("Coeficiente de Pearson: r = 0.222"),
    bullet("P-value: p = 0.275 (no significativo a α = 0.05)"),
    spacer(2),
    bodyRuns([b("Interpretación: "), r("La correlación lineal directa entre TB bovina y TB humana a nivel estatal no resultó estadísticamente significativa. Esto no invalida la relación zoonótica, sino que sugiere que la transmisión TB animal→humano opera a través de intermediarios complejos (leche no pasteurizada, contacto directo) que no se capturan con una simple correlación geográfica. Los estados con mayor carga de TB humana (Veracruz: 6,524 casos, Baja California: 6,038) no necesariamente coinciden con los de mayor cuarentena bovina (Jalisco: 5,035 animales), porque la TB humana en México tiene también un fuerte componente de transmisión persona-persona.")]),
    img("../figures/correlacion_tb_zoonotica.png", 5.8, 4.2),
    imgCaption("Figura 7. Correlación zoonótica TB Bovina ↔ TB Humana (r = 0.222, p = 0.275)."),

    h3("B. ANOVA — Riesgo de Salmonella según canal de venta"),
    body("Se simularon 1,000 muestras por canal utilizando distribuciones binomiales basadas en las prevalencias documentadas en la literatura:"),
    makeTable(
      ["Canal de Venta", "Prevalencia Esperada", "Prevalencia Simulada"],
      [["Supermercados", "1.3%", "0.8%"], ["Carnicerías", "8.4%", "9.1%"], ["Tianguis", "13.6%", "13.7%"], ["Mercados Municipales", "22.3%", "21.4%"]],
      [3200, 3000, 2826]
    ),
    spacer(4),
    bullet("F-statistic: 78.72"),
    bullet("P-value: 1.80 × 10⁻⁴⁹ (altamente significativo)"),
    spacer(2),
    bodyRuns([b("Hallazgo: "), r("La diferencia entre canales es abrumadoramente significativa (p < 0.001). Un consumidor que compra carne en un mercado municipal tiene 26 veces más probabilidad de encontrar Salmonella que uno que compra en un supermercado (21.4% vs 0.8%). Esto valida cuantitativamente el argumento de que el canal de distribución informal es el principal vector de riesgo alimentario.")]),
    img("../figures/anova_canales_venta.png", 6.2, 3.8),
    imgCaption("Figura 8. ANOVA: Riesgo sanitario por canal de venta (F = 78.72, p < 0.001)."),
  ];
}

module.exports = { buildStats };
