"""
fmd_finance_comparison.py
-------------------------
Genera gráficas comparativas estilizadas (estilo Big4 / UNRC) entre el modelo
clásico homogéneo y el nuevo modelo espacial gravitatorio:
1. Comparación mensual del Flujo de Caja Acumulado (USD).
2. Comparación diaria de la Curva Epidémica de Infectados Activos.
"""

import pandas as pd
import numpy as np
import json
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── Paleta de Colores UNRC ────────────────────────────────────
CARMESI = "#9C223F"  # Modelo Homogéneo
DORADO  = "#C9A84C"  # Modelo Espacial
DARK    = "#1A1A2E"
CREAM   = "#F8F4F0"
WHITE   = "#FFFFFF"
GRAY    = "#7F8C8D"

OUT_DIR = os.path.join(os.path.dirname(__file__), "../../docs/figures")
os.makedirs(OUT_DIR, exist_ok=True)

JSON_HOMOG = os.path.join(os.path.dirname(__file__), "../../docs/Segundo_avance/fmd_finance_data.json")
JSON_SPATIAL = os.path.join(os.path.dirname(__file__), "../../docs/Segundo_avance/fmd_finance_data_spatial.json")
CSV_SPATIAL = os.path.join(os.path.dirname(__file__), "../../data/processed/spatial/sir_simulation_results_180d.csv")

def run_homogeneous_sir(days=150):
    """Simula el SIR homogéneo diario para graficar la curva de infectados activos."""
    N = 35_100_000
    S = N - 1
    I = 1.0
    R = 0.0
    R0 = 6.0
    gamma = 1 / 14
    beta = R0 * gamma
    
    daily_I = [I]
    for _ in range(days):
        dS = -beta * S * I / N
        dI = beta * S * I / N - gamma * I
        dR = gamma * I
        S += dS
        I += dI
        R += dR
        daily_I.append(I)
    return daily_I

def main():
    print("=== Generador de Gráficas Comparativas Homogéneo vs. Espacial ===")
    
    # ── 1. CARGAR DATOS MENSUALES ───────────────────────────────
    with open(JSON_HOMOG, "r", encoding="utf-8") as f:
        data_h = json.load(f)
    with open(JSON_SPATIAL, "r", encoding="utf-8") as f:
        data_s = json.load(f)
        
    months = [1, 2, 3, 4, 5]
    cum_h = [m["cumulative_usd"] / 1e9 for m in data_h["monthly_cashflow_fmd"]]
    cum_s = [m["cumulative_usd"] / 1e9 for m in data_s["fmd_diagnostics_spatial"]]
    
    # ── GRÁFICA 1: COMPARATIVA MENSUAL DE COSTOS ACUMULADOS ───────
    fig1, ax = plt.subplots(figsize=(10, 6))
    fig1.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)
    
    # Dibujar líneas comparativas
    ax.plot(months, cum_h, color=CARMESI, linewidth=3, marker='o', markersize=8,
            label="Modelo Homogéneo ($I_0 = 1$)", zorder=3)
    ax.plot(months, cum_s, color=DORADO, linewidth=3, marker='s', markersize=8,
            label="Modelo Espacial Gravitatorio ($I_0 = 100$ en Veracruz)", zorder=3)
    
    # Anotaciones de valores clave
    for m, val_h, val_s in zip(months, cum_h, cum_s):
        # Para el mes 1, 3 y 5
        if m in [1, 3, 5]:
            ax.annotate(f"${val_h:.1f} mil M", xy=(m, val_h), xytext=(-25, 8 if val_h > val_s else -15),
                        textcoords='offset points', color=CARMESI, fontweight='bold', fontsize=9,
                        bbox=dict(boxstyle='round,pad=0.2', facecolor=WHITE, edgecolor=CARMESI, alpha=0.8))
            ax.annotate(f"${val_s:.1f} mil M", xy=(m, val_s), xytext=(10, 8 if val_s >= val_h else -15),
                        textcoords='offset points', color=DORADO, fontweight='bold', fontsize=9,
                        bbox=dict(boxstyle='round,pad=0.2', facecolor=WHITE, edgecolor=DORADO, alpha=0.8))

    # Títulos y etiquetas
    ax.set_title("Comparativa de Costo Acumulado: Homogéneo vs. Espacial", fontsize=14, fontweight='bold', color=DARK, pad=15)
    ax.set_xlabel("Mes de Epidemia", fontsize=11, fontweight='bold', color=DARK)
    ax.set_ylabel("Pérdida Acumulada (Miles de Millones de USD)", fontsize=11, fontweight='bold', color=DARK)
    ax.set_xticks(months)
    ax.set_xticklabels([f"Mes {m}" for m in months])
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:.0f} mil M"))
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(DARK)
    ax.spines['bottom'].set_color(DARK)
    
    ax.grid(True, linestyle='--', alpha=0.4, color='#BDC3C7')
    ax.legend(loc="upper left", framealpha=0.9, fontsize=10)
    
    plt.tight_layout()
    img_mensual = os.path.join(OUT_DIR, "fmd_comparativa_mensual.png")
    plt.savefig(img_mensual, dpi=300, bbox_inches='tight')
    print(f"[OK] Gráfica mensual generada: {img_mensual}")
    plt.close()

    # ── 2. CARGAR Y SIMULAR DATOS DIARIOS ───────────────────────
    df_sp = pd.read_csv(CSV_SPATIAL)
    df_sp_150 = df_sp[df_sp['dia'] <= 150].copy()
    
    daily_spatial_I = df_sp_150['infectados'].tolist()
    daily_homog_I = run_homogeneous_sir(150)
    days = df_sp_150['dia'].tolist()
    
    # ── GRÁFICA 2: COMPARATIVA DIARIA DE CURVAS EPIDÉMICAS ────────
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    fig2.patch.set_facecolor(CREAM)
    ax2.set_facecolor(CREAM)
    
    # Curvas
    ax2.plot(days, [i / 1e6 for i in daily_homog_I], color=CARMESI, linewidth=3,
             label="Homogéneo ($I_0 = 1$, Mezcla Perfecta)", zorder=3)
    ax2.plot(days, [i / 1e6 for i in daily_spatial_I], color=DORADO, linewidth=3,
             label="Espacial ($I_0 = 100$ en Veracruz, Fricción Vial)", zorder=3)
    
    # Resaltar picos
    peak_h = max(daily_homog_I) / 1e6
    peak_h_day = np.argmax(daily_homog_I) + 1
    
    peak_s = max(daily_spatial_I) / 1e6
    peak_s_day = np.argmax(daily_spatial_I) + 1
    
    ax2.scatter(peak_h_day, peak_h, color=CARMESI, s=100, edgecolor='black', zorder=4)
    ax2.annotate(f"Pico Homogéneo: {peak_h:.1f}M\n(Día {peak_h_day})", 
                 xy=(peak_h_day, peak_h), xytext=(peak_h_day - 45, peak_h - 4),
                 fontweight='bold', fontsize=9.5, color=CARMESI,
                 arrowprops=dict(arrowstyle='->', color=CARMESI, lw=1.5))
                 
    ax2.scatter(peak_s_day, peak_s, color=DORADO, s=100, edgecolor='black', zorder=4)
    ax2.annotate(f"Pico Espacial: {peak_s:.1f}M\n(Día {peak_s_day})", 
                 xy=(peak_s_day, peak_s), xytext=(peak_s_day + 15, peak_s + 2),
                 fontweight='bold', fontsize=9.5, color=DORADO,
                 arrowprops=dict(arrowstyle='->', color=DORADO, lw=1.5))

    # Títulos y formato
    ax2.set_title("Dinámica de Infección Diaria: Homogéneo vs. Espacial", fontsize=14, fontweight='bold', color=DARK, pad=15)
    ax2.set_xlabel("Días desde el Caso Cero", fontsize=11, fontweight='bold', color=DARK)
    ax2.set_ylabel("Animales Infectados Activos (Millones)", fontsize=11, fontweight='bold', color=DARK)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.1f}M"))
    
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_color(DARK)
    ax2.spines['bottom'].set_color(DARK)
    
    ax2.grid(True, linestyle='--', alpha=0.4, color='#BDC3C7')
    ax2.legend(loc="upper right", framealpha=0.9, fontsize=10)
    
    plt.tight_layout()
    img_diaria = os.path.join(OUT_DIR, "fmd_comparativa_diaria.png")
    plt.savefig(img_diaria, dpi=300, bbox_inches='tight')
    print(f"[OK] Gráfica diaria generada: {img_diaria}")
    plt.close()

if __name__ == '__main__':
    main()
