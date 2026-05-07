"""
Finance Addendum v2 — FMD como protagonista, TB como proxy comparativo.

Genera:
  1. Tabla de Costos de Diagnóstico FMD (país libre → protocolo DINESA)
  2. Flujo de caja mensual FMD Escenario de Reintroducción (5 meses)
  3. Análisis contrafactual/sensibilidad: Día 3 vs Día 14 vs Día 30
  4. Gráficas storytelling estilo Big4

Fuentes citadas con DOI/institución en cada dato.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import json, os

# ── Paleta UNRC ──────────────────────────────────────────────
CARMESI = "#9C223F"
DORADO  = "#C9A84C"
DARK    = "#1A1A2E"
CREAM   = "#F8F4F0"
ALERT   = "#E74C3C"
GREEN   = "#27AE60"
BLUE    = "#2E86C1"

OUT = os.path.join(os.path.dirname(__file__), "../../docs/figures")
os.makedirs(OUT, exist_ok=True)

# ═══════════════════════════════════════════════════════════════
# 1. COSTOS DE DIAGNÓSTICO FMD — País libre, protocolo DINESA
# ═══════════════════════════════════════════════════════════════
# En México (país libre desde 1954), FMD es enfermedad exótica.
# El diagnóstico NO es servicio comercial — lo absorbe el Estado.
# Sin embargo, el COSTO existe para el presupuesto público.
#
# Fuentes:
#   - ELISA NSP (Non-Structural Protein): Detect Ab post-infection
#     Ref: OIE Manual Ch. 3.1.8; PrioCHECK FMDV NS kit ~$8-15/sample
#   - RT-PCR (Real-Time): Gold standard molecular, BSL-3
#     Ref: Reid et al. (2003), J. Virol. Methods; ~$25-50/sample
#   - Virus Isolation (Cell Culture): BSL-3/BSL-4 requerido
#     Ref: OIE Manual; ~$80-150/sample (incluye mantenimiento BSL-3)
#   - Inspección Clínica (Vesículas): Sin costo lab, solo veterinario
#     Ref: SENASICA / CPA; ~$0-10 por visita
#   - LAMP (Loop-mediated Amplification): Prueba de campo rápida
#     Ref: Dukes et al. (2006); ~$10-20/sample
#   - Secuenciación Genómica: Serotipado definitivo
#     Ref: Knowles & Samuel (2003); ~$100-300/sample

fmd_diagnostics = [
    {
        "method": "Inspección Clínica (Vesículas)",
        "cost_usd": "$0 – $10",
        "time": "Inmediato",
        "sensitivity": "~70%",
        "notes": "Primer filtro. Confusión con estomatitis vesicular.",
        "source": "SENASICA / CPA; OIE Manual 3.1.8"
    },
    {
        "method": "ELISA NSP (Anticuerpos No-Estructurales)",
        "cost_usd": "$8 – $15",
        "time": "4-6 horas",
        "sensitivity": "90-95%",
        "notes": "Distingue infección vs vacunación (DIVA). Screening masivo.",
        "source": "PrioCHECK FMDV NS; OIE Manual"
    },
    {
        "method": "RT-PCR Tiempo Real",
        "cost_usd": "$25 – $50",
        "time": "4-8 horas",
        "sensitivity": "95-99%",
        "notes": "Gold standard molecular. Requiere BSL-3.",
        "source": "Reid et al. (2003); PANAFTOSA"
    },
    {
        "method": "LAMP (Prueba de Campo Rápida)",
        "cost_usd": "$10 – $20",
        "time": "30-60 min",
        "sensitivity": "85-95%",
        "notes": "Portátil. Útil en zonas rurales sin laboratorio.",
        "source": "Dukes et al. (2006), J. Virol. Methods"
    },
    {
        "method": "Aislamiento Viral (Cultivo Celular)",
        "cost_usd": "$80 – $150",
        "time": "3-7 días",
        "sensitivity": "Gold Standard",
        "notes": "Confirmatorio definitivo. Solo en BSL-3/4.",
        "source": "OIE Manual 3.1.8; Pirbright Institute"
    },
    {
        "method": "Secuenciación Genómica (Serotipado)",
        "cost_usd": "$100 – $300",
        "time": "5-14 días",
        "sensitivity": "100%",
        "notes": "Identifica serotipo exacto (O, A, SAT1-3, Asia1, C).",
        "source": "Knowles & Samuel (2003); WRLFMD"
    },
]

# ═══════════════════════════════════════════════════════════════
# 2. PARÁMETROS ECONÓMICOS FMD — México
# ═══════════════════════════════════════════════════════════════
# Fuentes verificadas:
#   - Exportación ganado vivo 2024: $1,015M USD (GCMA/USDA, 1.25M cabezas)
#   - Exportación carne res 2024: $1,700M USD (USDA ERS)
#   - Total sector exportador: ~$3,000M USD/año ≈ $8.2M USD/día
#   - Valor cabeza en pie: $26,250 MXN (~$1,544 USD) (SNIIM 2024)
#   - UK 2001: £8B total, 6.5M animales sacrificados, £1.3B compensación
#     Ref: Anderson Report (2002); National Audit Office
#   - Pérdidas globales FMD endémica: $6.5-21B USD/año (Knight-Jones & Rushton, 2013)

N = 35_100_000
VALOR_CABEZA_USD = 1_544
EXPORT_DIARIO_USD = 8_200_000  # $3B/año ÷ 365
COSTO_SACRIFICIO_USD = 50  # logística por cabeza (Rifle Sanitario)

# ═══════════════════════════════════════════════════════════════
# 3. MODELO SIR FMD — Escenario de Reintroducción (5 meses)
# ═══════════════════════════════════════════════════════════════
R0_fmd = 6.0
gamma_fmd = 1 / 14  # días (enfermedad aguda)
beta_fmd = R0_fmd * gamma_fmd

def run_sir_fmd(days, detection_day=None, quarantine_effectiveness=0.85):
    """Simula SIR para FMD con detección opcional."""
    S, I, R = N - 1, 1, 0  # I₀ = 1 animal importado
    daily = []
    for d in range(days):
        if detection_day and d >= detection_day:
            eff_beta = beta_fmd * (1 - quarantine_effectiveness)
        else:
            eff_beta = beta_fmd
        dS = -eff_beta * S * I / N
        dI = eff_beta * S * I / N - gamma_fmd * I
        dR = gamma_fmd * I
        S += dS; I += dI; R += dR
        daily.append({"day": d+1, "S": S, "I": I, "R": R})
    return daily

# Sin detección (worst case)
baseline = run_sir_fmd(150)

# Flujo de caja mensual (5 meses = 150 días)
monthly_fmd = []
cumulative = 0
for month in range(1, 6):
    start_day = (month - 1) * 30
    end_day = month * 30
    
    # Animales sacrificados en el mes (nuevos R del SIR)
    r_start = baseline[start_day]["R"] if start_day > 0 else 0
    r_end = baseline[end_day - 1]["R"]
    sacrificed = int(r_end - r_start)
    
    # Pico de infectados en el mes
    peak_I = max(baseline[d]["I"] for d in range(start_day, end_day))
    
    # Costos
    sacrifice_cost = sacrificed * VALOR_CABEZA_USD
    export_loss = EXPORT_DIARIO_USD * 30  # Cierre total de fronteras
    diagnostic_cost = int(peak_I * 0.05) * 35  # 5% muestreados a $35 RT-PCR
    total_month = sacrifice_cost + export_loss + diagnostic_cost
    cumulative += total_month
    
    monthly_fmd.append({
        "month": month,
        "infected_peak": int(peak_I),
        "sacrificed": sacrificed,
        "sacrifice_cost_usd": sacrifice_cost,
        "export_loss_usd": export_loss,
        "diagnostic_cost_usd": diagnostic_cost,
        "total_month_usd": total_month,
        "cumulative_usd": cumulative,
    })

# ═══════════════════════════════════════════════════════════════
# 4. ANÁLISIS CONTRAFACTUAL / SENSIBILIDAD
# ═══════════════════════════════════════════════════════════════
# Escenarios: detección en Día 3, Día 14, Día 30, Sin detección
scenarios_fmd = {}
for label, det_day in [("Día 3 (ideal)", 3), ("Día 14 (realista)", 14), 
                        ("Día 30 (tardía)", 30), ("Sin detección", None)]:
    sim = run_sir_fmd(150, detection_day=det_day)
    total_removed = sim[-1]["R"]
    peak_infected = max(d["I"] for d in sim)
    
    # Costo total
    sacrifice = total_removed * VALOR_CABEZA_USD
    export = EXPORT_DIARIO_USD * 150  # 5 meses de bloqueo
    total = sacrifice + export
    
    scenarios_fmd[label] = {
        "detection_day": det_day if det_day else "Nunca",
        "total_removed": int(total_removed),
        "peak_infected": int(peak_infected),
        "sacrifice_cost_usd": int(sacrifice),
        "export_loss_usd": int(export),
        "total_cost_usd": int(total),
        "daily_data": sim
    }

# Calcular ahorros
baseline_cost = scenarios_fmd["Sin detección"]["total_cost_usd"]
for label in scenarios_fmd:
    s = scenarios_fmd[label]
    s["savings_usd"] = baseline_cost - s["total_cost_usd"]
    s["savings_pct"] = round(s["savings_usd"] / baseline_cost * 100, 1) if baseline_cost > 0 else 0

# ═══════════════════════════════════════════════════════════════
# GRÁFICA 1: Flujo de Caja Mensual FMD (Waterfall)
# ═══════════════════════════════════════════════════════════════
fig, ax1 = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor(CREAM)
ax1.set_facecolor(CREAM)

months = [m["month"] for m in monthly_fmd]
sacrifice_costs = [m["sacrifice_cost_usd"] / 1e9 for m in monthly_fmd]  # Billions
export_costs = [m["export_loss_usd"] / 1e9 for m in monthly_fmd]
cumul = [m["cumulative_usd"] / 1e9 for m in monthly_fmd]

x = np.arange(len(months))
w = 0.35

bars1 = ax1.bar(x - w/2, sacrifice_costs, w, color=CARMESI, alpha=0.9, 
                label="Sacrificio sanitario", zorder=3)
bars2 = ax1.bar(x + w/2, export_costs, w, color=DORADO, alpha=0.9,
                label="Cierre de exportaciones", zorder=3)

ax2 = ax1.twinx()
ax2.plot(x, cumul, color=ALERT, linewidth=3, marker='D', markersize=10,
         markerfacecolor='white', markeredgecolor=ALERT, markeredgewidth=2,
         label="Pérdida acumulada", zorder=4)
ax2.set_facecolor("none")

# Etiqueta final
ax2.annotate(f"${cumul[-1]:.1f}B", xy=(4, cumul[-1]),
             xytext=(3.2, cumul[-1] * 1.05),
             fontsize=13, fontweight='bold', color=ALERT,
             arrowprops=dict(arrowstyle='->', color=ALERT, lw=2))

ax1.set_xlabel("Mes desde I₀ = 1", fontsize=12, fontweight='bold', color=DARK)
ax1.set_ylabel("Pérdida Mensual (Billions USD)", fontsize=12, fontweight='bold', color=DARK)
ax2.set_ylabel("Pérdida Acumulada (Billions USD)", fontsize=12, fontweight='bold', color=ALERT)
ax1.set_xticks(x)
ax1.set_xticklabels([f"Mes {m}" for m in months])

ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:.1f}B"))
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:.1f}B"))

ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', framealpha=0.9)

fig.suptitle("Flujo de Caja: Escenario de Reintroducción de Fiebre Aftosa en México",
             fontsize=14, fontweight='bold', color=DARK, y=0.98)
ax1.set_title("Pérdida por sacrificio sanitario + cierre OMSA de exportaciones (R₀ = 6.0, Serotipo O)",
              fontsize=9, color='gray', style='italic', pad=10)

plt.tight_layout()
plt.savefig(os.path.join(OUT, "flujo_caja_fmd.png"), dpi=300, bbox_inches='tight')
print("✅ flujo_caja_fmd.png")

# ═══════════════════════════════════════════════════════════════
# GRÁFICA 2: Análisis Contrafactual / Sensibilidad FMD
# ═══════════════════════════════════════════════════════════════
fig2, ax3 = plt.subplots(figsize=(12, 6))
fig2.patch.set_facecolor(CREAM)
ax3.set_facecolor(CREAM)

colors_s = {
    "Día 3 (ideal)": GREEN,
    "Día 14 (realista)": BLUE,
    "Día 30 (tardía)": DORADO,
    "Sin detección": ALERT
}

for label, data in scenarios_fmd.items():
    days_range = range(1, 151)
    infected = [d["I"] for d in data["daily_data"]]
    ax3.plot(days_range, [i/1e6 for i in infected], 
             color=colors_s[label], linewidth=2.5,
             label=f"{label}: {data['total_removed']:,} sacrificados", zorder=3)

# Líneas verticales de detección
for day, color, lbl in [(3, GREEN, "D3"), (14, BLUE, "D14"), (30, DORADO, "D30")]:
    ax3.axvline(x=day, color=color, linestyle='--', alpha=0.4, linewidth=1)

ax3.set_xlabel("Días desde I₀ = 1", fontsize=12, fontweight='bold', color=DARK)
ax3.set_ylabel("Animales Infectados (Millones)", fontsize=12, fontweight='bold', color=DARK)
ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.1f}M"))

ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

fig2.suptitle("Análisis de Sensibilidad: Impacto del Momento de Detección en FMD",
              fontsize=14, fontweight='bold', color=DARK, y=0.98)
ax3.set_title("Curva de infectados según día de activación del DINESA (R₀ = 6.0, cuarentena 85%)",
              fontsize=9, color='gray', style='italic', pad=10)
ax3.legend(loc='upper left', framealpha=0.9, fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(OUT, "contrafactual_fmd.png"), dpi=300, bbox_inches='tight')
print("✅ contrafactual_fmd.png")

# ═══════════════════════════════════════════════════════════════
# EXPORTAR JSON
# ═══════════════════════════════════════════════════════════════
# Limpiar daily_data para JSON (muy grande)
export_scenarios = {}
for k, v in scenarios_fmd.items():
    export_scenarios[k] = {key: val for key, val in v.items() if key != "daily_data"}

output = {
    "fmd_diagnostics": fmd_diagnostics,
    "monthly_cashflow_fmd": monthly_fmd,
    "scenarios_fmd": export_scenarios,
    "mexico_export_data": {
        "live_cattle_2024_usd": 1_015_000_000,
        "beef_exports_2024_usd": 1_700_000_000,
        "total_sector_usd": 3_000_000_000,
        "daily_export_loss_usd": EXPORT_DIARIO_USD,
        "source": "USDA ERS / GCMA 2024"
    },
    "uk_2001_benchmark": {
        "total_cost_gbp": 8_000_000_000,
        "animals_slaughtered": 6_500_000,
        "compensation_gbp": 1_300_000_000,
        "source": "Anderson Report (2002); National Audit Office UK"
    },
}

json_path = os.path.join(OUT, "..", "Segundo_avance", "fmd_finance_data.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
print("✅ fmd_finance_data.json")

# ── Resumen ─────────────────────────────────────────
print("\n" + "="*65)
print("RESUMEN FINANCIERO FMD — ESCENARIO DE REINTRODUCCIÓN")
print("="*65)
print(f"\n📊 Valor por cabeza: ${VALOR_CABEZA_USD:,} USD")
print(f"📊 Exportaciones en riesgo: ${3_000_000_000:,} USD/año (${EXPORT_DIARIO_USD:,} USD/día)")
print(f"\n{'Escenario':<25} {'Sacrificados':>15} {'Costo Total':>18} {'Ahorro':>18}")
print("-"*76)
for label, data in export_scenarios.items():
    sav = f"${data['savings_usd']:,} ({data['savings_pct']}%)" if data['savings_usd'] > 0 else "—"
    print(f"{label:<25} {data['total_removed']:>15,} ${data['total_cost_usd']:>16,}  {sav}")
