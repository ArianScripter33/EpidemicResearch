import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

# ==========================================
# PARÁMETROS EMPÍRICOS FMD
# ==========================================
N = 35_100_000 
I0_FMD = 1 
R0_FMD = 0
S0_FMD = N - I0_FMD - R0_FMD

R0_val_FMD = 6.0 # Choque exótico altísima transmisión
gamma_FMD = 1.0 / 14.0  # Duración aguda: 14 días
beta_FMD = R0_val_FMD * gamma_FMD

t = np.linspace(0, 150, 500)

def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = (beta * S * I / N) - (gamma * I)
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

y0_FMD = S0_FMD, I0_FMD, R0_FMD
ret_FMD = odeint(deriv, y0_FMD, t, args=(N, beta_FMD, gamma_FMD))
S_FMD, I_FMD, R_FMD = ret_FMD.T

# ==========================================
# MODELO ECONÓMICO (Nuclear) - FMD
# ==========================================
# Si un animal tiene FMD, no disminuye su producción: Mueren o el ejército ejecuta el "Rifle Sanitario".
# El valor total del animal se pierde instantáneamente al ser Removido/Recuperado (R_FMD).
# 1. Pérdida del valor Biológico: ~25,000 MXN por cabeza ( ~$1,250 USD)
# 2. Bloqueo Comercial OMSA: Las exportaciones se detienen en el día 1. 
#    México exporta ~$3,000 Millones USD en carne al año = ~$8.2 Millones USD de pérdida DIARIA constante.

costo_por_cabeza_usd = 1250
bloqueo_comercial_diario_usd = 8_200_000

# El animal es rematado, por lo que el costo biológico obedece a los "Removidos / R" acumulados:
perdida_biologica = R_FMD * costo_por_cabeza_usd

# El impacto de las exportaciones es un daño constante desde el día 0:
perdida_exportaciones = t * bloqueo_comercial_diario_usd

perdida_total = perdida_biologica + perdida_exportaciones

# ==========================================
# VISUALIZACIÓN ELITE (McKinsey Style)
# ==========================================
plt.style.use('seaborn-v0_8-white')
fig, ax1 = plt.subplots(figsize=(11, 6.5))

color_shock = '#1A1A1A' # Negro apocalíptico
color_fondo = '#F8F9FA'
fig.patch.set_facecolor(color_fondo)
ax1.set_facecolor(color_fondo)

# Curva principal: Destrucción Total Financiera
ax1.plot(t, perdida_total / 1e9, color=color_shock, linewidth=4)
ax1.fill_between(t, 0, perdida_total / 1e9, color=color_shock, alpha=0.15)

# Remover Chartjunk
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.spines['bottom'].set_color('#CCCCCC')
ax1.grid(axis='y', linestyle='--', alpha=0.4)

# Títulos absolutos
fig.suptitle("Fiebre Aftosa (FMD): La Ruina Automática del Sector Agropecuario", 
             fontsize=18, fontweight='bold', x=0.1, y=0.96, ha='left', color='#e74c3c')

fig.text(0.1, 0.86, "Modelo de colapso: Valuación por sacrificio forzoso ($1,250 USD/cabeza) y Bloqueo de Exportación de la OMSA.\nUn solo infectado ($I_0=1$) cuesta más de $22 Billones de dólares en menos de 5 meses.", 
         fontsize=12, color='#7F8C8D', linespacing=1.5)

# Asegurar límites del gráfico
ax1.set_xlim(0, 155)

# Formateo Ejes
ax1.set_xlabel('Días post-Infección Cero (I0=1)', fontsize=12, color='#7F8C8D', labelpad=10)
ax1.set_ylabel('Pérdida Financiera (Miles de Millones / Billions USD)', fontsize=12, color='#7F8C8D', labelpad=15)
ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter('$%1.0fB USD'))

# Callout Anotación
end_loss_b = perdida_total[-1] / 1e9
max_dia = t[-1]
ax1.plot(max_dia, end_loss_b, marker='o', markersize=10, color=color_shock)
ax1.annotate(f'Quiebre Nacional:\n${end_loss_b:,.1f} Billones USD\n(en {int(max_dia)} días)', 
             xy=(max_dia, end_loss_b), xytext=(-15, 0), textcoords='offset points',
             fontsize=11, fontweight='bold', color='#c0392b', ha='right', va='center')

# Eje secundario discreto (Para la aceleración del sacrificio)
ax2 = ax1.twinx()
ax2.plot(t, R_FMD / 1e6, color='#c0392b', linewidth=2, linestyle=':', alpha=0.9)
ax2.spines['top'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.set_ylabel('Animales Muertos/Sacrificados (Millones)', fontsize=11, color='#c0392b', rotation=270, labelpad=25)
ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}M'))

plt.subplots_adjust(top=0.76, bottom=0.15, right=0.88, left=0.1)
os.makedirs('docs/figures', exist_ok=True)
out_path = 'docs/figures/fmd_impacto_nuclear.png'
plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
print(f"✅ Gráfica Nuclear de FMD generada: {out_path}")
