const { spacer, body, bodyRuns, r, b, bullet, h1, h2, h3, makeTable, img, imgCaption } = require("./docx_helpers");

function buildSIR() {
  return [
    h1("5. Modelado Matemático SIR"),

    h2("5.1 Fundamentos Teóricos"),
    body("El modelo SIR (Susceptibles-Infectados-Recuperados), propuesto por Kermack y McKendrick en 1927, divide a la población en tres compartimentos que fluyen como líquidos en tuberías. Se implementó como un sistema de Ecuaciones Diferenciales Ordinarias (ODEs) resuelto mediante integración numérica (scipy.integrate.odeint), que utiliza internamente métodos de Runge-Kutta para garantizar precisión."),
    spacer(4),
    bodyRuns([b("Las ecuaciones del sistema son:")]),
    bullet("dS/dt = −β · S · I / N   (tasa de contagio)"),
    bullet("dI/dt = β · S · I / N − γ · I   (balance neto de infectados)"),
    bullet("dR/dt = γ · I   (acumulación de removidos)"),

    h2("5.2 Simulación Dual: TB Bovina vs. Fiebre Aftosa"),
    bodyRuns([b("Código: "), r("src/models/sir_dual.py")]),
    spacer(4),
    makeTable(
      ["Parámetro", "TB Bovina (Endémica)", "Fiebre Aftosa (Shock Exótico)"],
      [
        ["I₀ inicial", "7,558 animales (SENASICA 2024)", "1 animal (importación)"],
        ["R₀ estimado", "1.8 (Barlow, 1991)", "6.0 (Tildesley et al., 2006)"],
        ["Duración (1/γ)", "180 días (crónica)", "14 días (aguda)"],
        ["Pico de I a 150 días", "14,711 animales", "18,752,410 animales"],
        ["Interpretación", "Sangrado silencioso", "Colapso exponencial catastrófico"],
      ],
      [2400, 3300, 3326]
    ),
    spacer(4),
    bodyRuns([b("Hallazgo Clave: "), r("Un único animal importado con Serotipo O puede incendiar más del 53% del hato nacional (18.7M de 35.1M) antes del día 150.")]),
    img("../figures/sir_comparativo.png", 6.2, 4.0),
    imgCaption("Figura 9. Simulación SIR dual: Tuberculosis Bovina endémica vs. Fiebre Aftosa exótica."),
  ];
}

module.exports = { buildSIR };
