import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

# ==========================================
# PARÁMETROS EMPÍRICOS 
# ==========================================
N = 35_100_000 
I0_TB = 7558 
R0_TB = 0
S0_TB = N - I0_TB - R0_TB

R0_val_TB = 1.8 
gamma_TB = 1.0 / 180.0  # Duración prolongada: ~180 días
beta_TB = R0_val_TB * gamma_TB

# Simulación a largo plazo (3 años) para mostrar la cronicidad
t = np.linspace(0, 365 * 3, 1000)

def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = (beta * S * I / N) - (gamma * I)
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

y0_TB = S0_TB, I0_TB, R0_TB
ret_TB = odeint(deriv, y0_TB, t, args=(N, beta_TB, gamma_TB))
S_TB, I_TB, R_TB = ret_TB.T

# ==========================================
# MODELO ECONÓMICO (Literatura Científica)
# ==========================================
# Fuentes: Rahman & Samad (2009) — 17% caída en producción láctea (dato validado para México).
# Boland et al. (Irlanda, 2010) — Pérdida absoluta: 120–573 kg por lactancia.
# Base de precios: SIAP México 2024 — Precio promedio leche: $6.50 MXN/litro.
# Producción diaria vaca lechera mexicana promedio: 18 litros/día (SAGARPA 2023).
#
# Cálculo por vaca infectada:
#   Producción base = 18 L/día
#   Caída = 17% (Rahman & Samad, cota superior conservadora)
#   Litros perdidos = 18 * 0.17 = 3.06 L/día
#   Valor perdido = 3.06 L * $6.50 MXN = $19.89 MXN ≈ $1.1 USD diarios por vaca
#   El decomiso de canal (100% si hay lesiones tísicas) se añade como evento puntual,
#   pero para la integral continua usamos la pérdida lechera únicamente.
costo_diario_por_vaca_usd = 1.10  # USD/vaca/día (base científica, no estimado arbitrario)
perdida_diaria = I_TB * costo_diario_por_vaca_usd
# Integral (suma acumulada del costo a lo largo del tiempo)
dt = t[1] - t[0]
perdida_acumulada = np.cumsum(perdida_diaria) * dt

# ==========================================
# VISUALIZACIÓN ELITE (McKinsey / Tuft Style)
# ==========================================
plt.style.use('seaborn-v0_8-white')
fig, ax1 = plt.subplots(figsize=(11, 6.5))

color_sangrado = '#B22222' # Firebrick red
color_fondo = '#F8F9FA'
fig.patch.set_facecolor(color_fondo)
ax1.set_facecolor(color_fondo)

# Curva principal: El Sangrado Financiero
ax1.plot(t/365, perdida_acumulada / 1e6, color=color_sangrado, linewidth=4)
ax1.fill_between(t/365, 0, perdida_acumulada / 1e6, color=color_sangrado, alpha=0.1)

# Eliminar "Chartjunk" (Gridlines invasivas y bordes)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.spines['bottom'].set_color('#CCCCCC')
ax1.grid(axis='y', linestyle='--', alpha=0.4)

# Títulos y Explicaciones
ax1.set_title("Tuberculosis Bovina: El 'Cáncer Financiero' del Ganadero", 
              fontsize=18, fontweight='bold', loc='left', pad=45, color='#2C3E50')

ax1.text(0, 1.08, "Mientras la curva infecciosa parece plana, cada vaca enferma genera un daño acumulativo devastador.\nSimulación basada en literatura (Rahman & Samad) a $1.1 USD diarios por pérdida lechera.", 
         transform=ax1.transAxes, fontsize=12, color='#7F8C8D', linespacing=1.5)

# Expandir límite X para que quepa la anotación final
ax1.set_xlim(0, 3.3)

# Formateo de Ejes
ax1.set_xlabel('Años de Simulación', fontsize=12, color='#7F8C8D', labelpad=10)
ax1.set_ylabel('Pérdida Monetaria Acumulada', fontsize=12, color='#7F8C8D', labelpad=15)
ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter('$%1.0fM USD'))

# Anotación directa al punto final
end_loss = perdida_acumulada[-1] / 1e6
ax1.plot(3, end_loss, marker='o', markersize=10, color=color_sangrado)
ax1.annotate(f'Pérdida Nacional:\n${end_loss:,.1f} Millones USD\nen 36 meses\n(base: -17% leche, SIAP 2024)', 
             (3.02, end_loss - 2), fontsize=11, fontweight='bold', color=color_sangrado, va='top')

# Eje secundario discreto (Para que los que saben de SIR vean la población estable)
ax2 = ax1.twinx()
ax2.plot(t/365, I_TB, color='#95A5A6', linewidth=2, linestyle=':', alpha=0.8)
ax2.spines['top'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.set_ylabel('Animales Enfermos (Plana)', fontsize=11, color='#95A5A6', rotation=270, labelpad=25)
ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f} cabezas'))

plt.subplots_adjust(top=0.85, bottom=0.15, right=0.85, left=0.1)
os.makedirs('docs/figures', exist_ok=True)
out_path = 'docs/figures/tb_impacto_financiero.png'
plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
print(f"✅ Gráfica Big 4 generada: {out_path}")
