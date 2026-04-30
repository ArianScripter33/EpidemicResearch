const { spacer, body, bodyRuns, r, b, bullet, numbered, h1, h2, h3, makeTable, img, imgCaption } = require("./docx_helpers");

function buildEconomics() {
  return [
    h1("6. Análisis de Impacto Económico"),

    h2("6.1 TB Bovina: El \"Cáncer Financiero\" del Ganadero"),
    bodyRuns([b("Código: "), r("src/models/tb_storytelling_plot.py")]),
    body("Dado que la curva de infectados de TB es estable (~14K animales) pero persistente durante años, el daño real es acumulativo. Se construyó un modelo económico basado en literatura científica:"),
    spacer(2),
    bullet("Caída en Producción: Rahman & Samad (2009) reporta una caída del -17% en producción de leche por vaca infectada."),
    bullet("Precio de la Leche (SIAP México, 2024): $6.50 MXN/litro."),
    bullet("Producción Estándar: 18 litros/día por vaca (SAGARPA, 2023)."),
    bullet("Derivación: 18 L × 17% = 3.06 L perdidos → 3.06 × $6.50 = $19.89 MXN ≈ $1.10 USD diarios por vaca."),
    spacer(2),
    bodyRuns([b("Resultado: "), r("Integrando el costo sobre 36 meses, la pérdida nacional asciende a $17.3 Millones de USD exclusivamente por caída en producción lechera.")]),
    img("../figures/tb_impacto_financiero.png", 6.2, 4.0),
    imgCaption("Figura 10. Impacto financiero acumulado de la Tuberculosis Bovina ($17.3M USD en 36 meses)."),

    h2("6.2 Fiebre Aftosa: La Quiebra Automática"),
    bodyRuns([b("Código: "), r("src/models/fmd_storytelling_plot.py")]),
    body("A diferencia de la TB, la Fiebre Aftosa desencadena un colapso instantáneo:"),
    spacer(2),
    bullet("Pérdida Biológica: 500 kg en pie × $50 MXN = $25,000 MXN ≈ $1,250 USD por cabeza sacrificada (Fuente: SNIIM / Uniones Ganaderas)."),
    bullet("Cierre de Fronteras: Al declararse I₀=1, se activa un bloqueo OMSA a los $3,000 Millones USD anuales de exportación cárnica (pérdida de ~$8.2 Millones USD diarios)."),
    spacer(2),
    bodyRuns([b("Resultado: "), r("En menos de 150 días, la pérdida acumulada alcanza $22.8 Billones de Dólares (Billions USD).")]),
    img("../figures/fmd_impacto_nuclear.png", 6.2, 4.0),
    imgCaption("Figura 11. Colapso financiero catastrófico por Fiebre Aftosa ($22.8B USD en 150 días)."),
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
        ["Finanzas Corporativas", "Modelos impacto TB + FMD", "✅ Completado", "storytelling_plot.py"],
        ["Innovación Social", "App + Dashboard + DINESA", "✅ Conceptualizado", "Sección 7"],
      ],
      [2200, 2400, 1800, 2626]
    ),

    h1("9. Bibliografía"),
    body("Barlow, N.D. (1991). A spatially aggregated disease/host model for bovine Tb in New Zealand possum populations. Journal of Applied Ecology, 28(3), 777-793."),
    body("Brauer, F., & Castillo-Chávez, C. (2012). Mathematical Models in Population Biology and Epidemiology. Springer."),
    body("FAO. (2026). Update on Foot-and-Mouth Disease outbreaks in Europe and the Near East. Organización de las Naciones Unidas para la Alimentación y la Agricultura."),
    body("Kermack, W. O., & McKendrick, A. G. (1927). A contribution to the mathematical theory of epidemics. Proceedings of the Royal Society of London A, 115(772), 700-721."),
    body("Rahman, M. A., & Samad, M. A. (2009). Effect of bovine tuberculosis on milk production. Bangladesh Journal of Veterinary Medicine, 7(2), 287-290."),
    body("SENASICA. (2024). Boletín Trimestral de Cuarentenas de Tuberculosis Bovina. Servicio Nacional de Sanidad, Inocuidad y Calidad Agroalimentaria."),
    body("SIAP. (2024). Panorama Agroalimentario 2024. Servicio de Información Agroalimentaria y Pesquera, México."),
    body("Tildesley, M. J. et al. (2006). Optimal reactive vaccination strategies for a foot-and-mouth disease outbreak in the UK. Nature, 440, 83-86."),
    body("WOAH. (2026). Emergence of FMD Serotype SAT1 in the Golan region: Regional implications. Organización Mundial de Sanidad Animal."),
    body("WRLFMD / openFMD. (2025). World Reference Laboratory for Foot-and-Mouth Disease — Open Data Portal. The Pirbright Institute."),
  ];
}

module.exports = { buildEconomics, buildOpsStatusBiblio };
