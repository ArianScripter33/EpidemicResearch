import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import os

# Parámetros básicos para la demostración
N = 35_100_000
I0 = 1
R0 = 0
S0 = N - I0
beta = 6.0 * (1.0/14.0)
gamma = 1.0 / 14.0

def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = (beta * S * I / N) - (gamma * I)
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

# 1. Simulación Perfecta Integrada con ODEINT (SciPy)
t_smooth = np.linspace(0, 50, 500)
ret_smooth = odeint(deriv, (S0, I0, R0), t_smooth, args=(N, beta, gamma))
I_smooth = ret_smooth.T[1]

# 2. Simulación Manual A Pasos (Simulando lo que haría la computadora a mano - Método de Euler)
dt_step = 4 # Saltos de 4 días para que se vea tosco y escalonado
t_steps = np.arange(0, 50, dt_step)
I_manual = [I0]
S_current = S0

for i in range(1, len(t_steps)):
    I_current = I_manual[-1]
    
    # a) Preguntarle a la Ecuación Diferencial cuál es la pendiente AHORA mismo
    dSdt = -beta * S_current * I_current / N
    dIdt = (beta * S_current * I_current / N) - (gamma * I_current)
    
    # b) El Integrador "Avanza" en el tiempo multiplicando la pendiente por el tamaño del paso
    I_next = I_current + (dIdt * dt_step)
    S_next = S_current + (dSdt * dt_step)
    
    I_manual.append(I_next)
    S_current = S_next

# Gráfica Explicativa
plt.style.use('seaborn-v0_8-white')
plt.figure(figsize=(10, 6))

plt.plot(t_smooth, I_smooth / 1e6, 'r-', linewidth=3, label='scipy.odeint (Magia Curva Runge-Kutta Continua)')
plt.step(t_steps, np.array(I_manual) / 1e6, 'k--o', where='post', alpha=0.7, 
         label=f'Cálculo Manual Escalonado a Pasos (dt={dt_step} días)')

plt.title("Disección de una ODE: Integración Continua vs Pasos Manuales", fontsize=16, pad=20)
plt.ylabel("Infectados (Millones)")
plt.xlabel("Días de Simulación")

# Anotaciones para explicar el "bucle" intermedio
plt.annotate("Día 0: Lee I0=1\nCalcula pendiente", xy=(0, 0), xytext=(5, 1), arrowprops=dict(arrowstyle="->", color='gray'))
plt.annotate(f"Día {dt_step}: Salta con\nla pendiente vieja", xy=(dt_step, I_manual[1]/1e6), xytext=(dt_step+2, (I_manual[1]/1e6)+2), arrowprops=dict(arrowstyle="->", color='gray'))

plt.legend()
plt.grid(axis='y', alpha=0.3)

os.makedirs('docs/figures', exist_ok=True)
out_path = 'docs/figures/ode_euler_vs_odeint.png'
plt.savefig(out_path, dpi=300, bbox_inches='tight')
print(f"Gráfica educativa generada en: {out_path}")
