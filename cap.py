import numpy as np
import matplotlib.pyplot as plt

# Parámetros
capital_inicial = 100
p_ganar = 0.56
n_operaciones = 500  # Reducido a 500 para ver mejor la curva
kelly_full = 0.12

# Estrategias y sus colores asignados
estrategias = {
    "Kelly Quarter (3%)": {"frac": kelly_full * 0.25, "color": "green"},
    "Half Kelly (6%)": {"frac": kelly_full * 0.50, "color": "blue"},
    "Full Kelly (12%)": {"frac": kelly_full, "color": "orange"},
    "Overbet (50%)": {"frac": 0.50, "color": "red"}
}

plt.figure(figsize=(12, 7))

# Diccionario para guardar resultados estadísticos
resultados_ruina = {}

# 1. CORREMOS EL ANÁLISIS ESTADÍSTICO (1000 veces cada una)
for nombre, datos in estrategias.items():
    colapsos = 0
    for _ in range(1000):
        cap = capital_inicial
        for _ in range(n_operaciones):
            if np.random.random() < p_ganar:
                cap += cap * datos["frac"]
            else:
                cap -= cap * datos["frac"]
            if cap < 0.1:
                colapsos += 1
                break
    resultados_ruina[nombre] = (colapsos / 1000) * 100

# 2. GENERAMOS LA GRÁFICA (Solo 1 camino por estrategia)
for nombre, datos in estrategias.items():
    capital = capital_inicial
    historial = [capital]
    
    for _ in range(n_operaciones):
        if np.random.random() < p_ganar:
            capital += capital * datos["frac"]
        else:
            capital -= capital * datos["frac"]
        
        if capital < 0.1:
            capital = 0
            break
        historial.append(capital)
    
    # Rellenar con ceros si colapsó
    if len(historial) < n_operaciones + 1:
        historial.extend([0] * (n_operaciones + 1 - len(historial)))
        
    plt.plot(historial, label=f"{nombre} (Ruina: {resultados_ruina[nombre]:.1f}%)", 
             color=datos["color"], linewidth=2)

plt.yscale('log') 
plt.title(f"Comparativa de Estrategias (Prob. Ganancia: {p_ganar*100}%)", fontsize=14)
plt.xlabel("Número de Operaciones")
plt.ylabel("Capital (Escala Logarítmica)")
plt.legend()
plt.grid(True, which="both", ls="-", alpha=0.3)
plt.axhline(y=capital_inicial, color='black', linestyle='--', label="Capital Inicial")
plt.show()