const { spacer, body, bodyRuns, r, b, bullet, numbered, h1, h2, h3, makeTable, img, imgCaption } = require("./docx_helpers");

function buildEconomics() {
  return [
    h1("6. Análisis de Impacto Económico"),

    h2("6.1 TB Bovina: El \"Cáncer Financiero\" del Ganadero (Proxy de Calibración)"),
    bodyRuns([b("Código: "), r("src/models/tb_storytelling_plot.py")]),
    body("Dado que la curva de infectados de TB es estable (~14K animales) pero persistente durante años, el daño real es acumulativo. Se construyó un modelo económico basado en literatura científica para calibrar la metodología antes de aplicarla a FMD:"),
    spacer(2),
    bullet("Caída en Producción: Rahman & Samad (2009) reporta una caída del -17% en producción de leche por vaca infectada."),
    bullet("Precio de la Leche (SIAP México, 2024): $6.50 MXN/litro."),
    bullet("Producción Estándar: 18 litros/día por vaca (SAGARPA, 2023)."),
    bullet("Derivación: 18 L × 17% = 3.06 L perdidos → 3.06 × $6.50 = $19.89 MXN ≈ $1.10 USD diarios por vaca."),
    spacer(2),
    bodyRuns([b("Resultado: "), r("Integrando el costo sobre 36 meses, la pérdida nacional asciende a $17.3 Millones de USD exclusivamente por caída en producción lechera. Este valor sirve como escenario base para comparar con la magnitud 7,000x mayor de FMD.")]),
    img("../figures/tb_impacto_financiero.png", 6.2, 4.0),
    imgCaption("Figura 10. Impacto financiero acumulado de la Tuberculosis Bovina ($17.3M USD en 36 meses) — Proxy de calibración."),

    h2("6.2 Fiebre Aftosa: La Quiebra Automática"),
    bodyRuns([b("Código: "), r("src/models/fmd_finance_addendum.py")]),
    body("A diferencia de la TB, la Fiebre Aftosa desencadena un colapso instantáneo:"),
    spacer(2),
    bullet("Pérdida Biológica: 500 kg en pie × $52.5 MXN/kg = $26,250 MXN ≈ $1,544 USD por cabeza sacrificada (Fuente: SNIIM 2024 / Uniones Ganaderas)."),
    bullet("Cierre de Fronteras: Al declararse I₀=1, se activa un bloqueo OMSA a los $3,000 Millones USD anuales de exportación cárnica (pérdida de ~$8.2 Millones USD diarios)."),
    spacer(2),
    bodyRuns([b("Resultado: "), r("En menos de 150 días, la pérdida acumulada alcanza $52.8 Billion USD, equivalente al 4% del PIB de México.")]),
    img("../figures/fmd_impacto_nuclear.png", 6.2, 4.0),
    imgCaption("Figura 11. Colapso financiero catastrófico por Fiebre Aftosa ($52.8B USD en 150 días)."),

    // ═══════════════════════════════════════════════════════
    // §6.3 — COSTOS DE DIAGNÓSTICO FMD
    // ═══════════════════════════════════════════════════════
    h2("6.3 Costos de Diagnóstico FMD: ¿Cuánto cuesta detectar la enfermedad?"),
    body("En México, la Fiebre Aftosa es una enfermedad exótica (libre desde 1954). El diagnóstico ante sospecha es responsabilidad del Estado a través de la CPA y laboratorios BSL-3 de SENASICA. Sin embargo, el costo presupuestario existe y es cuantificable:"),
    spacer(4),

    // Tabla de diagnósticos
    makeTable(
      ["Método Diagnóstico FMD", "Costo/muestra (USD)", "Tiempo", "Sensibilidad", "Fuente"],
      [
        ["Inspección Clínica (Vesículas)", "$0 – $10", "Inmediato", "~70%", "SENASICA / CPA; OIE 3.1.8"],
        ["ELISA NSP (Anticuerpos No-Estructurales)", "$8 – $15", "4-6 horas", "90-95%", "PrioCHECK FMDV NS; OIE"],
        ["RT-PCR Tiempo Real", "$25 – $50", "4-8 horas", "95-99%", "Reid et al. (2003); PANAFTOSA"],
        ["LAMP (Prueba de Campo Rápida)", "$10 – $20", "30-60 min", "85-95%", "Dukes et al. (2006)"],
        ["Aislamiento Viral (Cultivo Celular)", "$80 – $150", "3-7 días", "Gold Standard", "OIE Manual 3.1.8; Pirbright"],
        ["Secuenciación Genómica (Serotipado)", "$100 – $300", "5-14 días", "100%", "Knowles & Samuel (2003)"],
      ],
      [2600, 1400, 1200, 1100, 2726]
    ),
    spacer(4),

    body("A diferencia de la Tuberculosis Bovina (donde el productor paga la tuberculina), en FMD el diagnóstico es absorbido íntegramente por el Estado como parte del protocolo DINESA. La prueba ELISA NSP es particularmente importante porque permite distinguir animales infectados de animales vacunados (capacidad DIVA), crucial para mantener el estatus de país libre ante la OMSA."),

    h3("¿Cuánto representa una cabeza o un centenar en riesgo de FMD?"),

    makeTable(
      ["Concepto", "Por cabeza", "Por 100 cabezas"],
      [
        ["Valor de mercado en pie (500 kg × $52.5 MXN/kg)", "$26,250 MXN ($1,544 USD)", "$2,625,000 MXN ($154,412 USD)"],
        ["Pérdida por sacrificio sanitario (Rifle Sanitario)", "$1,544 USD (valor total)", "$154,412 USD"],
        ["Pérdida diaria de exportaciones (cierre OMSA)", "$8,200,000 USD/día (todo el sector)", "$3,000,000,000 USD/año"],
        ["Costo diagnóstico RT-PCR", "$37.50 USD promedio", "$3,750 USD"],
      ],
      [3600, 2700, 2726]
    ),
    spacer(4),
    bodyRuns([b("Fuentes: "), r("Precio ganado en pie: SNIIM 2024. Exportaciones: USDA ERS 2024 ($1,015M ganado vivo + $1,700M carne = ~$3,000M/año).")]),

    // ═══════════════════════════════════════════════════════
    // §6.4 — FLUJO DE CAJA MENSUAL FMD
    // ═══════════════════════════════════════════════════════
    h2("6.4 Flujo de Caja: Escenario de Reintroducción de FMD (5 meses)"),
    bodyRuns([b("Código: "), r("src/models/fmd_finance_addendum.py")]),
    body("Se proyectó el impacto económico mensual de un escenario donde 1 solo animal infectado con Serotipo O ingresa al hato nacional de 35.1 millones, utilizando el modelo SIR (R₀ = 6.0) y dos componentes de costo: el sacrificio sanitario (valor de mercado de cada animal removido) y el cierre de exportaciones bovinas por la OMSA."),
    spacer(2),

    bodyRuns([b("Modelo de cierre de exportaciones: "), r("El bloqueo comercial no es instantáneo. Se implementó un modelo escalonado basado en los tiempos de reacción documentados de los socios comerciales:")]),
    spacer(2),

    // Tabla de fases de cierre
    makeTable(
      ["Fase", "Días", "% Cerrado", "Pérdida/día", "Fuente"],
      [
        ["Sospecha", "1-3", "0%", "$0", "Protocolo DINESA (SENASICA); OIE Manual 3.1.8"],
        ["Confirmación + EE.UU.", "4-7", "90%", "$7.4M", "WOAH TAHC Art. 1.1.3; UK 2001 (Anderson Report)"],
        ["Reacción global", "8-14", "98%", "$8.0M", "MAFF Japan FMD contingency; CFIA Canada"],
        ["Cierre total", "15+", "100%", "$8.2M", "WOAH TAHC Ch. 8.8"],
      ],
      [1800, 800, 1000, 1100, 4326]
    ),
    spacer(2),
    body("Fuente del mercado: Exportaciones bovinas de México: $1,015M (ganado vivo, ~100% a EE.UU.) + $1,700M (carne de res, ~86% a EE.UU.) + ~$285M (subproductos) = ~$3,000M USD/año (USDA FAS GATS 2024; AHDB 2024). EE.UU. = ~90% del mercado combinado bovino."),
    spacer(2),
    bodyRuns([b("Metodología de Cálculo: "), r("La pérdida se estima como L = (V_anual / 365) * %_Fase. Con un V_anual de $3,000M USD, la pérdida máxima es de $8.22M USD/día. El costo de $1,201M USD en los escenarios es la sumatoria de estas pérdidas diarias a 150 días, integrando el ramp-up de los primeros 14 días.")]),
    spacer(4),

    // Tabla de flujo de caja mensual
    makeTable(
      ["Mes", "Infectados (pico)", "Sacrificados", "Sacrificio (USD)", "Cierre Export. (USD)", "Pérdida Acumulada"],
      [
        ["1", "9,520", "1,904", "$2,939,776", "$216,972,000", "$219,928,436"],
        ["2", "19,423,405", "8,720,482", "$13,464,424,208", "$246,000,000", "$13,964,343,594"],
        ["3", "19,685,118", "21,706,241", "$33,514,436,104", "$246,000,000", "$47,759,228,623"],
        ["4", "2,966,841", "2,644,549", "$4,083,183,656", "$246,000,000", "$52,093,604,249"],
        ["5", "329,660", "293,158", "$452,635,952", "$246,000,000", "$52,792,817,106"],
      ],
      [800, 1400, 1400, 1600, 1600, 2226]
    ),
    spacer(4),

    bodyRuns([b("Hallazgo: "), r("Con R₀ = 6.0, la FMD no es lineal — es una detonación nuclear biológica. En el Mes 1 parece controlable (1,904 sacrificados), pero en el Mes 2 ya son 8.7 millones y en el Mes 3, 21.7 millones. El Mes 1 muestra un cierre de exportaciones menor ($217M vs $246M) debido al modelo escalonado. A 5 meses, la pérdida acumulada alcanza $52.8 Billion USD — equivalente al 4% del PIB de México.")]),

    bodyRuns([b("Benchmark internacional: "), r("El brote de FMD en Reino Unido (2001) costó £8B (~$12B USD), con 6.5 millones de animales sacrificados y £1.3B en compensaciones directas (Anderson Report, 2002). México, con un hato 5.4x mayor, enfrentaría pérdidas proporcionalmente mayores.")]),

    img("../figures/flujo_caja_fmd.png", 6.5, 3.0),
    imgCaption("Figura 12. Flujo de caja mensual FMD — Costo del sacrificio sanitario derivado del modelo SIR (R₀ = 6.0). Cierre de exportaciones con modelo escalonado de 4 fases."),

    // ═══════════════════════════════════════════════════════
    // §6.5 — ANÁLISIS DE SENSIBILIDAD / CONTRAFACTUAL
    // ═══════════════════════════════════════════════════════
    h2("6.5 Análisis de Sensibilidad: Impacto del Momento de Detección"),
    body("¿Qué se gana al detectar la FMD a tiempo? Este análisis de sensibilidad varía una sola variable — el día de activación del DINESA — y mide el impacto en animales sacrificados y costo total a 150 días. Se asume que la cuarentena (cierre de movimientos + anillo sanitario 3 km) reduce la tasa de contagio un 85% (Tildesley et al., 2006):"),
    spacer(4),

    // Tabla contrafactual
    makeTable(
      ["Escenario", "Día", "Sacrificados", "Costo Sacrificio", "Cierre Export.", "Costo Total", "Ahorro vs. sin detección"],
      [
        ["Detección Ideal", "Día 3", "16", "$0.03M", "$1,201M", "$1,201M", "$54.05B (97.8%)"],
        ["Detección Realista", "Día 14", "461", "$0.71M", "$1,201M", "$1,202M", "$54.05B (97.8%)"],
        ["Detección Tardía", "Día 30", "56,674", "$87.5M", "$1,201M", "$1,288M", "$53.96B (97.7%)"],
        ["Sin detección", "Nunca", "35,007,684", "$54,052M", "$1,201M", "$55,253M", "—"],
      ],
      [1400, 900, 1200, 1200, 1100, 1100, 2126]
    ),
    spacer(4),

    body("Nota metodológica: El cierre de exportaciones ($1,201M) se modela con un ramp-up escalonado de 4 fases basado en market shares verificados (USDA FAS GATS 2024: EE.UU. = ~90% del mercado bovino). Es un costo constante entre escenarios porque se activa con I₀ = 1. La columna 'Costo Sacrificio' es el verdadero costo variable. El horizonte de 150 días subestima el impacto real: la OMSA requiere 6-24 meses post-erradicación para recuperar estatus libre (Anderson, 2002)."),
    spacer(4),

    bodyRuns([b("Hallazgos clave y Justificación Matemática:")]),
    spacer(2),
    numbered("Cada día cuenta exponencialmente (Crecimiento Viral): La diferencia entre detectar en el Día 3 (16 animales sacrificados) vs. el Día 30 (56,674) es de una magnitud de 3,542x. Esto ocurre porque la curva de contagio inicial sigue la ecuación I(t) = I_0 * e^((R_0 - 1)*gamma*t). Con un R_0 = 6.0, el crecimiento no es lineal, es una explosión demográfica exponencial. A pesar de esto, 56 mil animales sigue siendo manejable comparado con la catástrofe de no detectar (35 millones)."),
    numbered("El ROI de la vigilancia es astronómico (2,700:1): Calculamos el Retorno de Inversión (ROI) del sistema de vigilancia de la CPA (~$20M USD anuales). ROI = (Costo Sin Detección - Costo Detección Ideal) / Costo de Vigilancia = ($55.25B - $1.20B) / $20M = 2,702. Por cada dólar invertido en vigilancia activa, México ahorra $2,700 dólares en mitigación de crisis."),
    numbered("El cierre de exportaciones domina el costo en escenarios controlados: Incluso con detección en el Día 3, el costo del sacrificio es insignificante (16 * $1,544 = $24,704 USD), pero el costo por cierre de exportaciones es de $1.20B USD. El ratio de daño colateral es de 48,615x. El daño comercial colateral es casi 50 mil veces mayor que el daño biológico directo. Este costo es inevitable una vez declarado el caso I_0 = 1. La FMD es un virus económico."),
    spacer(4),

    bodyRuns([b("Proxy comparativo con TB Bovina (7,089x): "), r("Para validar el modelo, comparamos la FMD con la Tuberculosis Bovina (endémica). La TB (R_0 = 1.8) es de progresión lenta y genera pérdidas directas de ~$7.8M USD a 12 meses sin detección. La FMD (R_0 = 6.0) genera $55.3B USD en 5 meses. El ratio de severidad es de 55.3B / 7.8M = 7,089x. Esto valida que un modelo capaz de mapear la TB, es indispensable para la FMD.")]),

    img("../figures/contrafactual_fmd.png", 6.5, 2.8),
    imgCaption("Figura 13. Análisis de sensibilidad — Impacto del momento de detección en FMD (panel dual: escala completa + escala logarítmica)."),
  ];
}

function buildOpsStatusBiblio() {
  return [
    h1("7. Arquitectura Operativa Propuesta"),

    h2("7.1 Protocolo SENASICA Actual (DINESA)"),
    body("Cuando existe sospecha de FMD, la CPA (Comisión México-Estados Unidos para la Prevención de la Fiebre Aftosa) coordina la respuesta:"),
    spacer(2),
    numbered("Veterinarios oficiales inspeccionan las lesiones."),
    numbered("Se extraen muestras para un Laboratorio Nivel 3."),
    numbered("Si positivo, se detona el DINESA (Dispositivo Nacional de Emergencia de Sanidad Animal)."),
    numbered("El Ejército y la Guardia Nacional clausuran fronteras estatales (Rifle Sanitario)."),

    h2("7.2 El Cuello de Botella: El Productor Informal"),
    body("El problema no son los corporativos (SuKarne, Lala), sino los productores de traspatio. Ante el miedo al Rifle Sanitario y la burocracia de indemnización, el ganadero informal evade reportar e intenta vender vacas enfermas en tianguis y mercados negros. Este ocultamiento es el vector que habilita el R₀ = 6.0."),

    h2("7.3 Propuesta: Sistema de Inteligencia Epidémica Basado en Incentivos"),
    h3("Para el Ganadero (App Móvil)"),
    body("Una aplicación cuyo gancho de entrada (Wedge) sean los precios diarios del mercado ganadero. Si una vaca presenta anomalías, la app ofrece un \"Botón de Pánico\" que captura coordenadas GeoJSON y detona un proceso de Indemnización Acelerada (pago en 72 horas). Esto destruye el incentivo del mercado negro."),
    h3("Para la Autoridad (Dashboard NoSQL)"),
    body("La CPA visualiza un panel basado en MongoDB. Si tres productores denuncian anomalías en un radio de 50 km en menos de 2 horas, el sistema dispara una Alerta Espacial de Enjambre y corre la simulación SIR en tiempo real para informar al Ejército en qué casetas deben plantarse."),

    h1("8. Estado de Avance por Materia"),
    makeTable(
      ["Materia", "Componente", "Estado", "Evidencia"],
      [
        ["Ecuaciones Diferenciales", "Modelo SIR Dual (TB vs FMD)", "✅ Completado", "sir_dual.py"],
        ["Bases de Datos NoSQL", "Data Warehouse CSV→JSON + Pydantic", "✅ Completado", "csv_to_json.py"],
        ["Estadística Multivariada", "EDA + ANOVA + Correlación", "✅ Completado", "notebooks/01-03"],
        ["Inteligencia Artificial", "XGBoost Clasificador", "🟡 En diseño", "Features definidas"],
        ["Criptografía", "Cifrado César + RSA", "🟡 En progreso", "Tarea delegada"],
        ["Finanzas Corporativas", "Modelos impacto TB + FMD + Contrafactual", "✅ Completado", "fmd_finance_addendum.py"],
        ["Innovación Social", "App + Dashboard + DINESA", "✅ Conceptualizado", "Sección 7"],
      ],
      [2200, 2400, 1800, 2626]
    ),

    h1("9. Bibliografía"),
    body("Anderson, I. (2002). Foot and Mouth Disease 2001: Lessons to be Learned Inquiry Report. The Stationery Office, London."),
    body("Barlow, N.D. (1991). A spatially aggregated disease/host model for bovine Tb in New Zealand possum populations. Journal of Applied Ecology, 28(3), 777-793."),
    body("Brauer, F., & Castillo-Chávez, C. (2012). Mathematical Models in Population Biology and Epidemiology. Springer."),
    body("Dukes, J.P. et al. (2006). A reverse-transcription loop-mediated isothermal amplification (RT-LAMP) assay for the detection of foot-and-mouth disease virus. Journal of Virological Methods, 138(1-2), 18-26."),
    body("FAO. (2026). Update on Foot-and-Mouth Disease outbreaks in Europe and the Near East. Organización de las Naciones Unidas para la Alimentación y la Agricultura."),
    body("Kermack, W. O., & McKendrick, A. G. (1927). A contribution to the mathematical theory of epidemics. Proceedings of the Royal Society of London A, 115(772), 700-721."),
    body("Knight-Jones, T.J.D. & Rushton, J. (2013). The economic impacts of foot and mouth disease — What are they, how big, and where do they occur? Preventive Veterinary Medicine, 112(3-4), 161-173."),
    body("Knowles, N. J. & Samuel, A. R. (2003). Molecular epidemiology of foot-and-mouth disease virus. Virus Research, 91(1), 65-80."),
    body("OIE. (2023). Manual of Diagnostic Tests and Vaccines for Terrestrial Animals, Chapter 3.1.8: Foot and Mouth Disease; Chapter 3.4.6: Bovine Tuberculosis. World Organisation for Animal Health."),
    body("PANAFTOSA / OPS. (2024). Centro Panamericano de Fiebre Aftosa y Salud Pública Veterinaria — Materiales de Referencia. Organización Panamericana de la Salud."),
    body("Rahman, M. A., & Samad, M. A. (2009). Effect of bovine tuberculosis on milk production. Bangladesh Journal of Veterinary Medicine, 7(2), 287-290."),
    body("Reid, S. M. et al. (2003). Detection of all seven serotypes of foot-and-mouth disease virus by real-time, fluorogenic reverse transcription polymerase chain reaction assay. Journal of Virological Methods, 105(1), 67-80."),
    body("SENASICA. (2024). Boletín Trimestral de Cuarentenas de Tuberculosis Bovina. Servicio Nacional de Sanidad, Inocuidad y Calidad Agroalimentaria."),
    body("SIAP. (2024). Panorama Agroalimentario 2024. Servicio de Información Agroalimentaria y Pesquera, México."),
    body("SNIIM. (2024). Cuadro Comparativo Anual Nacional — Bovinos en Pie. Sistema Nacional de Información e Integración de Mercados, Secretaría de Economía."),
    body("Tildesley, M. J. et al. (2006). Optimal reactive vaccination strategies for a foot-and-mouth disease outbreak in the UK. Nature, 440, 83-86."),
    body("USDA ERS. (2024). Mexico Livestock and Products Annual — Live Cattle and Beef Trade Statistics. United States Department of Agriculture, Economic Research Service."),
    body("WOAH. (2026). Emergence of FMD Serotype SAT1 in the Golan region: Regional implications. Organización Mundial de Sanidad Animal."),
    body("WRLFMD / openFMD. (2025). World Reference Laboratory for Foot-and-Mouth Disease — Open Data Portal. The Pirbright Institute."),
  ];
}

module.exports = { buildEconomics, buildOpsStatusBiblio };
