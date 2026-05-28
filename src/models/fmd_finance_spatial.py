"""
fmd_finance_spatial.py
----------------------
Fork de fmd_finance_addendum.py que utiliza los resultados del Modelo Espacial
(sir_simulation_results_180d.csv) en lugar del modelo SIR teórico homogéneo.
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

# ── Paleta UNRC ──────────────────────────────────────────────
CARMESI = "#9C223F"
DORADO  = "#C9A84C"
DARK    = "#1A1A2E"
CREAM   = "#F8F4F0"

OUT = os.path.join(os.path.dirname(__file__), "../../docs/figures")
os.makedirs(OUT, exist_ok=True)
INPUT_CSV = os.path.join(os.path.dirname(__file__), "../../data/processed/spatial/sir_simulation_results_180d.csv")

VALOR_CABEZA_USD = 1_544
EXPORT_DIARIO_MAX = 8_200_000  # $3B/año ÷ 365 (100% cierre)

# ── Modelo escalonado de cierre de exportaciones ──────────────
def export_loss_day(day):
    if day <= 3: return 0
    elif day <= 7: return int(EXPORT_DIARIO_MAX * 0.90)
    elif day <= 14: return int(EXPORT_DIARIO_MAX * 0.98)
    else: return EXPORT_DIARIO_MAX

def export_loss_range(start_day, end_day):
    return sum(export_loss_day(d) for d in range(start_day + 1, end_day + 1))

def export_loss_total(days):
    return export_loss_range(0, days)

def main():
    print("Cargando datos del SIR Espacial...")
    df = pd.read_csv(INPUT_CSV)
    
    # Recortar a 150 días para hacer la comparación directa (5 meses)
    df_150 = df[df['dia'] <= 150].copy()
    
    # Flujo de caja mensual
    monthly_fmd = []
    cumulative = 0
    
    for month in range(1, 6):
        start_day = (month - 1) * 30
        end_day = month * 30
        
        # Filtro de días
        df_month = df_150[(df_150['dia'] > start_day) & (df_150['dia'] <= end_day)]
        if df_month.empty:
            continue
            
        r_start = df_150[df_150['dia'] == start_day]['removidos'].values[0] if start_day > 0 else 0
        r_end = df_month.iloc[-1]['removidos']
        sacrificed = int(r_end - r_start)
        
        peak_I = df_month['infectados'].max()
        
        sacrifice_cost = sacrificed * VALOR_CABEZA_USD
        export_loss = export_loss_range(start_day, end_day)
        total_month = sacrifice_cost + export_loss
        cumulative += total_month
        
        monthly_fmd.append({
            "month": month,
            "sacrifice_cost_usd": sacrifice_cost,
            "export_loss_usd": export_loss,
            "cumulative_usd": cumulative
        })
    
    # ── GRÁFICA: Flujo de Caja Mensual FMD Espacial ──────────────
    fig, ax1 = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor(CREAM)
    ax1.set_facecolor(CREAM)

    months = [m["month"] for m in monthly_fmd]
    sacrifice_costs = [m["sacrifice_cost_usd"] / 1e6 for m in monthly_fmd]
    cumul = [m["cumulative_usd"] / 1e6 for m in monthly_fmd]

    x = np.arange(len(months))

    bars = ax1.bar(x, sacrifice_costs, 0.6, color=CARMESI, alpha=0.9,
                   label="Sacrificio sanitario (por mes)", zorder=3)

    for bar, val in zip(bars, sacrifice_costs):
        if val > 500:
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000,
                     f"${val:,.0f}M", ha='center', va='bottom', fontsize=10,
                     color=DARK, fontweight='bold')

    ax2 = ax1.twinx()
    ax2.plot(x, cumul, color=DORADO, linewidth=3, marker='D', markersize=10,
             markerfacecolor='white', markeredgecolor=DORADO, markeredgewidth=2,
             label="Pérdida acumulada", zorder=4)
    ax2.set_facecolor("none")

    ax2.annotate(f"${cumul[-1]:,.0f}M", xy=(4, cumul[-1]),
                 xytext=(3.3, cumul[-1] * 0.90),
                 fontsize=13, fontweight='bold', color=DORADO,
                 arrowprops=dict(arrowstyle='->', color=DORADO, lw=2))

    export_total = export_loss_total(150) / 1e6
    ax1.text(0.02, 0.95,
             f"⚠ Cierre de Exportaciones:\n"
             f"Total 150 días: ${export_total:,.0f}M USD\n\n"
             f"Nota: El Modelo Espacial retrasa la masacre\nhacia los meses 3 y 4 debido a la fricción geográfica.",
             transform=ax1.transAxes, fontsize=10, ha='left', va='top',
             bbox=dict(boxstyle='round,pad=0.6', facecolor='white',
                       edgecolor=DORADO, alpha=0.95, linewidth=1.5),
             color=DARK)

    ax1.set_xlabel("Mes desde I₀ = 1", fontsize=12, fontweight='bold', color=DARK)
    ax1.set_ylabel("Costo Sacrificio Sanitario (Millones USD)", fontsize=12, fontweight='bold', color=CARMESI)
    ax2.set_ylabel("Pérdida Acumulada (Millones USD)", fontsize=12, fontweight='bold', color=DORADO)
    ax1.set_xticks(x)
    ax1.set_xticklabels([f"Mes {m}" for m in months])

    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}M"))
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}M"))

    ax1.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', framealpha=0.9)

    fig.suptitle("Flujo de Caja FMD: Modelo SIR ESPACIAL (Fricción Geográfica)",
                 fontsize=14, fontweight='bold', color=DARK, y=0.98)
    ax1.set_title("La geografía aplaza el colapso, pero la pérdida acumulada a 5 meses sigue superando los $51,000M USD.",
                  fontsize=10, color='gray', style='italic', pad=10)

    plt.tight_layout()
    out_img = os.path.join(OUT, "flujo_caja_fmd_espacial.png")
    plt.savefig(out_img, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfica generada: {out_img}")

    # Resumen
    total_sacrificados = df_150.iloc[-1]['removidos']
    costo_total = total_sacrificados * VALOR_CABEZA_USD + export_loss_total(150)
    print("\nRESUMEN FINANCIERO ESPACIAL (150 DÍAS):")
    print(f"Total Sacrificados: {total_sacrificados:,.0f}")
    print(f"Costo Total Estimado: ${costo_total:,.0f} USD")

if __name__ == '__main__':
    main()
