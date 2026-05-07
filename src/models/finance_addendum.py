"""
Finance Addendum — Respuesta al feedback del profesor de Finanzas Empresariales.

Genera:
  1. Tabla de Costos de Diagnóstico por método
  2. Flujo de caja mensual (12 meses) para TB Bovina
  3. Análisis contrafactual: Detección Temprana vs Tardía
  4. 2 gráficas storytelling estilo Big4/SWD

Fuentes citadas en cada dato.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import json
import os

# ── Paleta UNRC ──────────────────────────────────────────────
CARMESI = "#9C223F"
DORADO  = "#C9A84C"
DARK    = "#1A1A2E"
CREAM   = "#F8F4F0"
ALERT   = "#E74C3C"
GREEN   = "#27AE60"

OUT_DIR = os.path.join(os.path.dirname(__file__), "../../docs/figures")
os.makedirs(OUT_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════════════════
# 1. COSTOS DE DIAGNÓSTICO — Datos respaldados por literatura
# ═══════════════════════════════════════════════════════════════
# Fuentes:
#   - Tuberculina PPD: PRONABIVE México (productor nacional), ~$2-4 USD/dosis
#     Ref: SENASICA, NOM-031-ZOO-1995 y Acuerdo DOF 30-dic-2024
#   - Honorarios veterinarios: CFPP Chihuahua, ~$5-15 USD/visita dependiendo de
#     tamaño de hato. Incluye inyección + lectura 72h (2 visitas)
#   - Gamma-Interferón (BOVIGAM™): Thermo Fisher, ~$15-25 USD/muestra
#     Ref: Bezos et al. (2014), Veterinary Microbiology
#   - ELISA (IDVet): ~$8-12 USD/muestra
#     Ref: Casal et al. (2017), Prev. Vet. Medicine
#   - PCR (IS6110): Labs universitarios UNAM/INIFAP, ~$20-35 USD
#     Ref: Pérez-Guerrero et al. (2008), Veterinary Microbiology
#   - Cultivo bacteriológico: 4-8 semanas, ~$40-60 USD
#     Ref: OIE Manual of Diagnostic Tests, Ch. 3.4.6
#   - Inspección post-mortem: Costo absorbido en rastro TIF
#     Ref: NOM-033-ZOO-1995

diagnostics = [
    {
        "method": "Tuberculina Intradérmica (PPD)",
        "cost_usd_min": 3, "cost_usd_max": 8,
        "cost_mxn_min": 51, "cost_mxn_max": 136,
        "time": "72 horas",
        "sensitivity": "80-90%",
        "specificity": "95-99%",
        "notes": "Requiere 2 visitas. Gold standard OIE para screening.",
        "source": "SENASICA / NOM-031-ZOO; PRONABIVE"
    },
    {
        "method": "Gamma-Interferón (BOVIGAM™)",
        "cost_usd_min": 15, "cost_usd_max": 25,
        "cost_mxn_min": 255, "cost_mxn_max": 425,
        "time": "24-48 horas",
        "sensitivity": "85-95%",
        "specificity": "90-97%",
        "notes": "Muestra sanguínea. Mayor sensibilidad en etapas tempranas.",
        "source": "Bezos et al. (2014); Thermo Fisher"
    },
    {
        "method": "ELISA (Anticuerpos)",
        "cost_usd_min": 8, "cost_usd_max": 12,
        "cost_mxn_min": 136, "cost_mxn_max": 204,
        "time": "24-48 horas",
        "sensitivity": "60-80%",
        "specificity": "90-95%",
        "notes": "Útil para screening masivo. Detecta fases avanzadas.",
        "source": "Casal et al. (2017)"
    },
    {
        "method": "PCR (IS6110/IS1081)",
        "cost_usd_min": 20, "cost_usd_max": 35,
        "cost_mxn_min": 340, "cost_mxn_max": 595,
        "time": "5-7 días",
        "sensitivity": "95-99%",
        "specificity": "98-100%",
        "notes": "Alta precisión. Requiere laboratorio equipado.",
        "source": "Pérez-Guerrero et al. (2008); UNAM/INIFAP"
    },
    {
        "method": "Cultivo Bacteriológico",
        "cost_usd_min": 40, "cost_usd_max": 60,
        "cost_mxn_min": 680, "cost_mxn_max": 1020,
        "time": "4-8 semanas",
        "sensitivity": "Gold Standard",
        "specificity": "100%",
        "notes": "Confirmatorio definitivo. Lento pero irrefutable.",
        "source": "OIE Manual, Ch. 3.4.6"
    },
    {
        "method": "Inspección Post-mortem (Rastro TIF)",
        "cost_usd_min": 0, "cost_usd_max": 0,
        "cost_mxn_min": 0, "cost_mxn_max": 0,
        "time": "Inmediato",
        "sensitivity": "50-60%",
        "specificity": "95%",
        "notes": "Sin costo adicional (absorbido por rastro). Baja sensibilidad.",
        "source": "NOM-033-ZOO-1995; SENASICA"
    },
]

# ═══════════════════════════════════════════════════════════════
# 2. FLUJO DE CAJA MENSUAL TB BOVINA (12 meses) — Modelo SIR
# ═══════════════════════════════════════════════════════════════
# Parámetros del SIR ya calibrado en sir_dual.py:
#   N = 35,100,000 | I0 = 7,558 | R0_tb = 1.8 | gamma = 1/180

N = 35_100_000
I0 = 7_558
R0_tb = 1.8
gamma_tb = 1 / 180  # días
beta_tb = R0_tb * gamma_tb

# Resolver SIR simplificado mes a mes (30 días por mes, Euler)
S, I, R = N - I0, I0, 0
monthly_data = []

for month in range(1, 13):
    month_start_I = I
    for day in range(30):
        dS = -beta_tb * S * I / N
        dI = beta_tb * S * I / N - gamma_tb * I
        dR = gamma_tb * I
        S += dS
        I += dI
        R += dR
    
    # Económicos por mes (Rahman & Samad, 2009 + SIAP 2024)
    avg_infected = (month_start_I + I) / 2
    liters_lost_per_cow_day = 18 * 0.17  # 3.06 L/día
    price_per_liter = 6.50  # MXN (SIAP 2024)
    monthly_loss_mxn = avg_infected * liters_lost_per_cow_day * price_per_liter * 30
    monthly_loss_usd = monthly_loss_mxn / 17  # TC ~17 MXN/USD (2024)
    
    # Valor de cabeza perdida (sacrificio sanitario)
    # Precio promedio en pie: $50-55 MXN/kg × 500 kg = ~$25,000-27,500 MXN
    # Fuente: SNIIM 2024, bovinos para abasto
    valor_cabeza_mxn = 26_250  # promedio
    valor_cabeza_usd = valor_cabeza_mxn / 17
    
    # Diagnóstico: Tuberculina a todo el hato afectado + 10% del hato cercano
    diagnostic_heads = int(avg_infected * 1.1)
    diagnostic_cost_usd = diagnostic_heads * 5.5  # promedio tuberculina
    
    monthly_data.append({
        "month": month,
        "infected_start": int(month_start_I),
        "infected_end": int(I),
        "avg_infected": int(avg_infected),
        "liters_lost_total": int(avg_infected * liters_lost_per_cow_day * 30),
        "production_loss_mxn": round(monthly_loss_mxn),
        "production_loss_usd": round(monthly_loss_usd),
        "diagnostic_cost_usd": round(diagnostic_cost_usd),
        "cumulative_loss_usd": 0  # se calcula abajo
    })

# Calcular acumulado
cumulative = 0
for m in monthly_data:
    cumulative += m["production_loss_usd"] + m["diagnostic_cost_usd"]
    m["cumulative_loss_usd"] = round(cumulative)

# ═══════════════════════════════════════════════════════════════
# 3. ANÁLISIS CONTRAFACTUAL: Detección Temprana vs Tardía
# ═══════════════════════════════════════════════════════════════
# Escenario A: Detección en Mes 2 → cuarentena inmediata, I se estabiliza
# Escenario B: Detección en Mes 6 → 6 meses de propagación libre
# Escenario C: Sin detección (status quo) → 12 meses completos

scenarios = {}
for label, detection_month in [("Temprana (Mes 2)", 2), ("Tardía (Mes 6)", 6), ("Sin detección", 13)]:
    S_s, I_s, R_s = N - I0, I0, 0
    total_loss = 0
    monthly_losses = []
    
    for month in range(1, 13):
        month_start_I = I_s
        for day in range(30):
            if month >= detection_month:
                # Post-detección: cuarentena reduce beta un 70%
                effective_beta = beta_tb * 0.3
            else:
                effective_beta = beta_tb
            dS = -effective_beta * S_s * I_s / N
            dI = effective_beta * S_s * I_s / N - gamma_tb * I_s
            dR = gamma_tb * I_s
            S_s += dS
            I_s += dI
            R_s += dR
        
        avg_I = (month_start_I + I_s) / 2
        loss = avg_I * 3.06 * 6.50 * 30 / 17
        total_loss += loss
        monthly_losses.append(round(loss))
    
    scenarios[label] = {
        "total_12m_usd": round(total_loss),
        "final_infected": int(I_s),
        "monthly_losses": monthly_losses
    }

# Calcular ahorro
savings_early = scenarios["Sin detección"]["total_12m_usd"] - scenarios["Temprana (Mes 2)"]["total_12m_usd"]
savings_late = scenarios["Sin detección"]["total_12m_usd"] - scenarios["Tardía (Mes 6)"]["total_12m_usd"]

# ═══════════════════════════════════════════════════════════════
# GRÁFICA 1: Flujo de Caja Mensual (Waterfall / SWD style)
# ═══════════════════════════════════════════════════════════════
fig, ax1 = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor(CREAM)
ax1.set_facecolor(CREAM)

months = [m["month"] for m in monthly_data]
monthly_losses_usd = [m["production_loss_usd"] for m in monthly_data]
cumulative_losses = [m["cumulative_loss_usd"] for m in monthly_data]

# Barras mensuales
bars = ax1.bar(months, monthly_losses_usd, color=CARMESI, alpha=0.85, width=0.6, 
               label="Pérdida mensual (USD)", zorder=3)

# Línea acumulada
ax2 = ax1.twinx()
ax2.plot(months, cumulative_losses, color=DORADO, linewidth=3, marker='o', 
         markersize=8, markerfacecolor=DORADO, markeredgecolor=DARK, 
         label="Pérdida acumulada (USD)", zorder=4)
ax2.set_facecolor("none")

# Etiquetas en barras
for bar, val in zip(bars, monthly_losses_usd):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2000, 
             f"${val:,.0f}", ha='center', va='bottom', fontsize=8, 
             color=DARK, fontweight='bold')

# Etiqueta final acumulada
ax2.annotate(f"${cumulative_losses[-1]:,.0f}", 
             xy=(12, cumulative_losses[-1]),
             xytext=(10.5, cumulative_losses[-1] * 1.08),
             fontsize=11, fontweight='bold', color=DORADO,
             arrowprops=dict(arrowstyle='->', color=DORADO, lw=1.5))

ax1.set_xlabel("Mes", fontsize=12, fontweight='bold', color=DARK)
ax1.set_ylabel("Pérdida Mensual (USD)", fontsize=12, fontweight='bold', color=CARMESI)
ax2.set_ylabel("Pérdida Acumulada (USD)", fontsize=12, fontweight='bold', color=DORADO)
ax1.set_xticks(months)
ax1.set_xticklabels([f"Mes {m}" for m in months], rotation=45, ha='right')

ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)

fig.suptitle("Flujo de Caja: Impacto Económico Mensual de TB Bovina", 
             fontsize=14, fontweight='bold', color=DARK, y=0.98)
ax1.set_title("Pérdida en producción lechera por animales infectados (modelo SIR × costos SIAP 2024)", 
              fontsize=10, color='gray', style='italic', pad=10)

# Leyendas combinadas
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', framealpha=0.9)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "flujo_caja_mensual_tb.png"), dpi=300, bbox_inches='tight')
print("✅ flujo_caja_mensual_tb.png")

# ═══════════════════════════════════════════════════════════════
# GRÁFICA 2: Análisis Contrafactual (SWD slope chart)
# ═══════════════════════════════════════════════════════════════
fig2, ax3 = plt.subplots(figsize=(12, 6))
fig2.patch.set_facecolor(CREAM)
ax3.set_facecolor(CREAM)

colors = {
    "Temprana (Mes 2)": GREEN,
    "Tardía (Mes 6)": DORADO,
    "Sin detección": ALERT
}
linewidths = {"Temprana (Mes 2)": 3, "Tardía (Mes 6)": 2.5, "Sin detección": 2}

for label, data in scenarios.items():
    cumul = np.cumsum(data["monthly_losses"])
    ax3.plot(range(1, 13), cumul, color=colors[label], linewidth=linewidths[label],
             marker='o', markersize=6, label=f"{label}: ${data['total_12m_usd']:,.0f} USD total",
             zorder=3)

# Zona de ahorro (sombreada)
cumul_sin = np.cumsum(scenarios["Sin detección"]["monthly_losses"])
cumul_early = np.cumsum(scenarios["Temprana (Mes 2)"]["monthly_losses"])
ax3.fill_between(range(1, 13), cumul_early, cumul_sin, alpha=0.15, color=GREEN, 
                 label=f"Ahorro det. temprana: ${savings_early:,.0f} USD")

# Anotación de ahorro
ax3.annotate(f"Ahorro:\n${savings_early:,.0f} USD\n({savings_early/scenarios['Sin detección']['total_12m_usd']*100:.1f}%)", 
             xy=(9, (cumul_sin[8] + cumul_early[8])/2),
             fontsize=10, fontweight='bold', color=GREEN, ha='center',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=GREEN, alpha=0.9))

ax3.set_xlabel("Mes", fontsize=12, fontweight='bold', color=DARK)
ax3.set_ylabel("Pérdida Acumulada (USD)", fontsize=12, fontweight='bold', color=DARK)
ax3.set_xticks(range(1, 13))
ax3.set_xticklabels([f"Mes {m}" for m in range(1, 13)], rotation=45, ha='right')
ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

# Líneas verticales de detección
ax3.axvline(x=2, color=GREEN, linestyle='--', alpha=0.5, linewidth=1)
ax3.axvline(x=6, color=DORADO, linestyle='--', alpha=0.5, linewidth=1)
ax3.text(2.1, ax3.get_ylim()[1]*0.3, "Detección\ntemprana", fontsize=8, color=GREEN, alpha=0.7)
ax3.text(6.1, ax3.get_ylim()[1]*0.3, "Detección\ntardía", fontsize=8, color=DORADO, alpha=0.7)

ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

fig2.suptitle("Análisis Contrafactual: ROI de la Detección Temprana", 
              fontsize=14, fontweight='bold', color=DARK, y=0.98)
ax3.set_title("Pérdida acumulada por TB Bovina según momento de detección y cuarentena", 
              fontsize=10, color='gray', style='italic', pad=10)
ax3.legend(loc='upper left', framealpha=0.9, fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "contrafactual_deteccion_tb.png"), dpi=300, bbox_inches='tight')
print("✅ contrafactual_deteccion_tb.png")

# ═══════════════════════════════════════════════════════════════
# EXPORTAR DATOS PARA EL MARKDOWN
# ═══════════════════════════════════════════════════════════════
output = {
    "diagnostics": diagnostics,
    "monthly_cashflow": monthly_data,
    "scenarios": scenarios,
    "savings": {
        "early_vs_none_usd": savings_early,
        "late_vs_none_usd": savings_late,
        "early_pct": round(savings_early/scenarios["Sin detección"]["total_12m_usd"]*100, 1),
        "late_pct": round(savings_late/scenarios["Sin detección"]["total_12m_usd"]*100, 1),
    },
    "unit_economics": {
        "valor_cabeza_mxn": 26_250,
        "valor_cabeza_usd": round(26_250/17),
        "valor_100_cabezas_usd": round(26_250*100/17),
        "loss_per_cow_per_day_mxn": round(3.06 * 6.50, 2),
        "loss_per_cow_per_day_usd": round(3.06 * 6.50 / 17, 2),
        "loss_per_cow_per_month_usd": round(3.06 * 6.50 * 30 / 17, 2),
    }
}

json_path = os.path.join(OUT_DIR, "..", "Segundo_avance", "finance_addendum_data.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
print(f"✅ finance_addendum_data.json")

# ── Imprimir resumen ─────────────────────────────────────────
print("\n" + "="*60)
print("RESUMEN FINANCIERO — ADDENDUM")
print("="*60)
print(f"\n📊 Valor por cabeza: ${output['unit_economics']['valor_cabeza_usd']:,} USD ({output['unit_economics']['valor_cabeza_mxn']:,} MXN)")
print(f"📊 Valor 100 cabezas: ${output['unit_economics']['valor_100_cabezas_usd']:,} USD")
print(f"📊 Pérdida/vaca/día: ${output['unit_economics']['loss_per_cow_per_day_usd']} USD")
print(f"📊 Pérdida/vaca/mes: ${output['unit_economics']['loss_per_cow_per_month_usd']} USD")
print(f"\n💰 Pérdida 12 meses sin detección: ${scenarios['Sin detección']['total_12m_usd']:,} USD")
print(f"💰 Pérdida 12 meses det. temprana: ${scenarios['Temprana (Mes 2)']['total_12m_usd']:,} USD")
print(f"💰 Pérdida 12 meses det. tardía:   ${scenarios['Tardía (Mes 6)']['total_12m_usd']:,} USD")
print(f"\n🏆 Ahorro detección temprana: ${savings_early:,} USD ({output['savings']['early_pct']}%)")
print(f"🏆 Ahorro detección tardía:   ${savings_late:,} USD ({output['savings']['late_pct']}%)")
