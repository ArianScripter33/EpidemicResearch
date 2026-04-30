import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# ==========================================
# PARÁMETROS EMPÍRICOS (Base: EDA Fase 1)
# ==========================================
N = 35_100_000  # Biomasa bovina nacional (cabezas)

# --- Enfermedad 1: Tuberculosis Bovina (Endémica) ---
I0_TB = 7558    # Animales actualmente en cuarentenas SENASICA 2024
R0_TB = 1.0     # (Inicialmente 0 = recuperados)
S0_TB = N - I0_TB - R0_TB

R0_val_TB = 1.8 # R0 estimado en literatura para TB bovina
gamma_TB = 1.0 / 180.0  # Duración prolongada: ~180 días
beta_TB = R0_val_TB * gamma_TB

# --- Enfermedad 2: Fiebre Aftosa / FMD (Brote Exótico) ---
# Justificación I0=1: Modelo de Gravedad Espacial (Riesgo de Importación constante)
I0_FMD = 1      
R0_FMD = 0      
S0_FMD = N - I0_FMD - R0_FMD

R0_val_FMD = 6.0 # R0 estimado epidemia UK 2001 (Serotipo O)
gamma_FMD = 1.0 / 14.0  # Duración aguda: ~14 días
beta_FMD = R0_val_FMD * gamma_FMD

# Rango temporal de simulación: 150 días
t = np.linspace(0, 150, 150)

# ==========================================
# SISTEMA DE ECUACIONES DIFERENCIALES (ODEs)
# ==========================================
def deriv(y, t, N, beta, gamma):
    """
    Motor ODE del Modelo SIR.
    y: vector de estado [S, I, R]
    t: tiempo actual (día)
    N: Población total
    """
    S, I, R = y
    
    # 1. Agotamiento de Susceptibles (Flujo de entrada a I)
    dSdt = -beta * S * I / N
    
    # 2. Crecimiento de Infectados
    dIdt = (beta * S * I / N) - (gamma * I)
    
    # 3. Acumulación de Recuperados/Removidos
    dRdt = gamma * I
    
    return dSdt, dIdt, dRdt

import os

# ==========================================
# INTEGRACIÓN NUMÉRICA (Simulación)
# ==========================================
def run_simulation():
    print(f"Iniciando simulación SIR Dual sobre {N:,.0f} animales...")
    
    # Vectores de estado inicial
    y0_TB = S0_TB, I0_TB, R0_TB
    y0_FMD = S0_FMD, I0_FMD, R0_FMD
    
    # Solucionador algorítmico (Runge-Kutta subyacente en LSODA)
    ret_TB = odeint(deriv, y0_TB, t, args=(N, beta_TB, gamma_TB))
    ret_FMD = odeint(deriv, y0_FMD, t, args=(N, beta_FMD, gamma_FMD))
    
    S_TB, I_TB, R_TB = ret_TB.T
    S_FMD, I_FMD, R_FMD = ret_FMD.T
    
    print("\n--- Resultados a 150 días ---")
    print(f"TB (Endémica):  Pico máximo de infectados: {int(max(I_TB)):,}")
    print(f"FMD (Exótica):  Pico máximo de infectados: {int(max(I_FMD)):,}")
    
    # ==========================================
    # VISUALIZACIÓN GRÁFICA (Matplotlib)
    # ==========================================
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Gráfica 1: Tuberculosis Bovina
    ax1.plot(t, S_TB / 1e6, 'b', alpha=0.7, linewidth=2, label='Susceptibles')
    ax1.plot(t, I_TB / 1e6, 'r', alpha=0.7, linewidth=2, label='Infectados')
    ax1.plot(t, R_TB / 1e6, 'g', alpha=0.7, linewidth=2, label='Recuperados/Removidos')
    ax1.set_title("TB Bovina (Epidemia Lenta / Endémica)\nI0=7,558 | R0=1.8")
    ax1.set_xlabel('Días')
    ax1.set_ylabel('Población Bovinos (Millones)')
    ax1.grid(visible=True, which='major', c='#dddddd', lw=1, alpha=0.8)
    ax1.legend(loc='center right')
    
    # Gráfica 2: Fiebre Aftosa (FMD)
    ax2.plot(t, S_FMD / 1e6, 'b', alpha=0.7, linewidth=2, label='Susceptibles')
    ax2.plot(t, I_FMD / 1e6, 'r', alpha=0.7, linewidth=2, label='Infectados')
    ax2.plot(t, R_FMD / 1e6, 'g', alpha=0.7, linewidth=2, label='Recuperados/Removidos')
    ax2.set_title("Fiebre Aftosa (Choque Exponencial Exótico)\nI0=1 | R0=6.0")
    ax2.set_xlabel('Días')
    ax2.grid(visible=True, which='major', c='#dddddd', lw=1, alpha=0.8)
    ax2.legend(loc='center right')
    
    plt.tight_layout()
    
    # Crear directorio si no existe y guardar
    os.makedirs('docs/figures', exist_ok=True)
    out_path = 'docs/figures/sir_comparativo.png'
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"\n✅ Gráfica generada y guardada en: {out_path}")
    
    return t, (S_TB, I_TB, R_TB), (S_FMD, I_FMD, R_FMD)

if __name__ == "__main__":
    run_simulation()
