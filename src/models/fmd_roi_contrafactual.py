import matplotlib.pyplot as plt
import numpy as np
import os

# Colores institucionales
CARMESI = '#900C3F'
DORADO = '#D4AF37'
DARK = '#2C3E50'
CREAM = '#FDFBF7'

def plot_contrafactual():
    # Datos de sacrificios por día de detección
    dias = ['Día 3\n(Detección Inmediata)', 'Día 14\n(Detección Retrasada)', 'Día 30\n(Brote Descontrolado)', 'Día 60\n(Colapso Nacional)']
    sacrificados = [16, 461, 56000, 10200000]
    
    # Costo base por animal (Valor cabeza + logística cuarentena + pérdida comercial)
    COSTO_UNITARIO_USD = 1544 
    costos_usd = [s * COSTO_UNITARIO_USD for s in sacrificados]
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(CREAM)
    ax1.set_facecolor(CREAM)
    
    # Eje 1: Barras de Costo Financiero (Escala Logarítmica para poder ver la monstruosa diferencia)
    x = np.arange(len(dias))
    bars = ax1.bar(x, costos_usd, color=CARMESI, alpha=0.85, width=0.6, edgecolor='black')
    
    # Formato eje Y (Logarítmico)
    ax1.set_yscale('log')
    ax1.set_ylabel("Costo Total Acumulado (USD) - Escala Logarítmica", fontsize=11, fontweight='bold', color=DARK)
    ax1.set_ylim(1e4, 1e11)
    
    # Etiquetas en la parte superior de las barras
    for i, bar in enumerate(bars):
        costo = costos_usd[i]
        if costo < 1e6:
            texto = f"${costo/1e3:.1f}k"
        elif costo < 1e9:
            texto = f"${costo/1e6:.1f}M"
        else:
            texto = f"${costo/1e9:.1f} mil M"
            
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.5, 
                 f"{texto}\n({sacrificados[i]:,} cabezas)", 
                 ha='center', va='bottom', fontsize=10, fontweight='bold', color=DARK)
    
    ax1.set_xticks(x)
    ax1.set_xticklabels(dias, fontsize=10, fontweight='bold')
    ax1.set_title("Análisis Contrafactual: Costo de Retraso en Detección (Fiebre Aftosa)", fontsize=14, fontweight='bold', color=DARK, pad=20)
    
    # Quitar bordes
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_color(DARK)
    ax1.spines['bottom'].set_color(DARK)
    
    ax1.grid(True, axis='y', linestyle='--', alpha=0.4, color='#BDC3C7')
    
    # Añadir texto explicativo de ROI
    ahorro_3_vs_30 = costos_usd[2] - costos_usd[0]
    ax1.text(0.5, 0.85, f"ROI App (Día 3 vs Día 30):\n¡Ahorro de ${ahorro_3_vs_30/1e6:.1f} Millones USD!", 
             transform=ax1.transAxes, ha='center', va='center', 
             bbox=dict(facecolor=DORADO, alpha=0.2, edgecolor=DORADO, boxstyle='round,pad=1'),
             fontsize=11, fontweight='bold', color=DARK)
             
    plt.tight_layout()
    os.makedirs('docs/figures', exist_ok=True)
    out_path = 'docs/figures/fmd_roi_contrafactual.png'
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfica Contrafactual ROI generada: {out_path}")

if __name__ == '__main__':
    plot_contrafactual()
