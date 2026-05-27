import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Rutas de entrada (rutas relativas corregidas para ejecución desde src/spatial_model)
GEOJSON_PATH = '../../data/processed/spatial/nodos_estados.geojson'
MATRIX_PATH = '../../data/processed/spatial/matriz_gravedad.csv'

# Parámetros Epidémicos (FMD)
BETA = 0.6
GAMMA = 0.1
SPATIAL_BETA = 0.8
DIAS_SIMULACION = 180
ESTADO_PACIENTE_CERO = 'Veracruz'

def run_simulation(gdf_base, spatial_probs, use_lockdown=False, lockdown_day=12):
    gdf = gdf_base.copy()
    
    # Inicializar columnas SIR
    gdf['S'] = gdf['inventario_bovino_2023'].astype(float)
    gdf['I'] = 0.0
    gdf['R'] = 0.0
    
    # Inyectar Paciente Cero
    idx_zero = gdf.index[gdf['estado'] == ESTADO_PACIENTE_CERO].tolist()[0]
    gdf.at[idx_zero, 'I'] = 100.0
    gdf.at[idx_zero, 'S'] -= 100.0
    
    historial = []
    np.random.seed(42)  # Mantener consistencia
    
    for t in range(DIAS_SIMULACION):
        total_I = gdf['I'].sum()
        total_R = gdf['R'].sum()
        historial.append({'dia': t, 'infectados': total_I, 'removidos': total_R})
        
        nuevos_I = np.zeros(len(gdf))
        nuevos_R = np.zeros(len(gdf))
        
        # a) Propagación Local (Euler)
        for i, row in gdf.iterrows():
            if row['I'] > 0:
                S = row['S']
                I = row['I']
                N = row['inventario_bovino_2023']
                
                delta_I = min(S, BETA * S * I / N)
                delta_R = min(I, GAMMA * I)
                
                nuevos_I[i] += delta_I
                nuevos_R[i] += delta_R
                
        # b) Propagación Espacial (Nodos interactuando)
        estados_infectados = gdf[gdf['I'] >= 1]['estado'].tolist()
        estados_sanos = gdf[gdf['I'] < 1]['estado'].tolist()
        
        # Lista de estados a bloquear en caso de cuarentena
        estados_bloqueados = ['Veracruz', 'Tabasco', 'Puebla', 'Oaxaca']
        
        for e_inf in estados_infectados:
            idx_inf = gdf.index[gdf['estado'] == e_inf][0]
            prevalencia = gdf.at[idx_inf, 'I'] / gdf.at[idx_inf, 'inventario_bovino_2023']
            
            for e_sano in estados_sanos:
                # Si hay cuarentena activa y involucra a Veracruz o colindantes bloqueados, cortar la ruta a 0
                if use_lockdown and t >= lockdown_day:
                    if e_inf in estados_bloqueados or e_sano in estados_bloqueados:
                        continue  # Se bloquea el transporte comercial de ganado
                
                if e_inf in spatial_probs and e_sano in spatial_probs[e_inf]:
                    prob_base = spatial_probs[e_inf][e_sano]
                    prob_base_calibrada = max(0.015, prob_base)
                    
                    prob_infeccion = prob_base_calibrada * prevalencia * SPATIAL_BETA
                    
                    if np.random.random() < prob_infeccion:
                        idx_sano = gdf.index[gdf['estado'] == e_sano][0]
                        if gdf.at[idx_sano, 'S'] > 50.0:
                            nuevos_I[idx_sano] += 50.0
                            
        # c) Actualizar valores
        gdf['I'] += nuevos_I - nuevos_R
        gdf['S'] -= nuevos_I
        gdf['R'] += nuevos_R
        
        gdf['S'] = gdf['S'].clip(lower=0)
        gdf['I'] = gdf['I'].clip(lower=0)
        
    return pd.DataFrame(historial)

def main():
    print("=== Simulación de Cerco Sanitario (Lockdown) en Veracruz ===")
    
    # 1. Cargar Datos
    gdf = gpd.read_file(GEOJSON_PATH)
    matriz = pd.read_csv(MATRIX_PATH)
    
    spatial_probs = {}
    for _, row in matriz.iterrows():
        o = row['origen']
        d = row['destino']
        if o not in spatial_probs:
            spatial_probs[o] = {}
        spatial_probs[o][d] = row['probabilidad_contagio_base']
        
    # 2. Correr simulaciones
    print("Corriendo Escenario 1: Libre propagación espacial...")
    df_base = run_simulation(gdf, spatial_probs, use_lockdown=False)
    
    # Simular bloqueo en el Día 12 (cuando se detecta el brote en Veracruz con la App Criptográfica)
    lockdown_day = 12
    print(f"Corriendo Escenario 2: Cuarentena y Cierre de rutas de Veracruz y colindantes (Puebla, Oaxaca, Tabasco) en el Día {lockdown_day}...")
    df_lockdown = run_simulation(gdf, spatial_probs, use_lockdown=True, lockdown_day=lockdown_day)
    
    # 3. Graficar comparativa
    CARMESI = '#900C3F'
    DORADO = '#D4AF37'
    DARK = '#2C3E50'
    CREAM = '#FDFBF7'
    VERDE_SANIDAD = '#2E7D32'
    
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)
    
    # Curvas
    ax.plot(df_base['dia'], df_base['infectados'] / 1e6, color=CARMESI, linewidth=3,
             label="Escenario Libre (Sin restricción de tránsito)", zorder=3)
    ax.plot(df_lockdown['dia'], df_lockdown['infectados'] / 1e6, color=VERDE_SANIDAD, linewidth=3,
             label=f"Escenario de Cerco Sanitario (Lockdown Día {lockdown_day})", zorder=3)
    
    # Resaltar picos
    peak_base = df_base['infectados'].max() / 1e6
    peak_base_day = df_base['infectados'].idxmax()
    
    peak_lock = df_lockdown['infectados'].max() / 1e6
    peak_lock_day = df_lockdown['infectados'].idxmax()
    
    ax.scatter(peak_base_day, peak_base, color=CARMESI, s=100, edgecolor='black', zorder=4)
    ax.annotate(f"Pico Libre: {peak_base:.1f}M\n(Día {peak_base_day})", 
                 xy=(peak_base_day, peak_base), xytext=(peak_base_day - 45, peak_base - 3),
                 fontweight='bold', fontsize=9.5, color=CARMESI,
                 arrowprops=dict(arrowstyle='->', color=CARMESI, lw=1.5))
                  
    ax.scatter(peak_lock_day, peak_lock, color=VERDE_SANIDAD, s=100, edgecolor='black', zorder=4)
    ax.annotate(f"Pico Cuarentena: {peak_lock:.2f}M\n(Día {peak_lock_day})", 
                 xy=(peak_lock_day, peak_lock), xytext=(peak_lock_day + 15, peak_lock + 1.5),
                 fontweight='bold', fontsize=9.5, color=VERDE_SANIDAD,
                 arrowprops=dict(arrowstyle='->', color=VERDE_SANIDAD, lw=1.5))
    
    # Sombra del área salvada
    ax.fill_between(df_base['dia'], df_lockdown['infectados'] / 1e6, df_base['infectados'] / 1e6,
                    color=VERDE_SANIDAD, alpha=0.15, label="Ganado Salvado por Intervención", zorder=2)
    
    # Línea vertical del bloqueo
    ax.axvline(x=lockdown_day, color='#7F8C8D', linestyle='--', alpha=0.8, zorder=1)
    ax.text(lockdown_day + 2, 8, "Cierre de Canales\n(Veracruz + Vecinos)", color='#7F8C8D', fontsize=9, fontweight='bold')

    # Títulos y formato
    ax.set_title("Efecto de Intervención: Cierre de Canales de Veracruz y Colindantes", fontsize=13, fontweight='bold', color=DARK, pad=15)
    ax.set_xlabel("Días desde el Caso Cero", fontsize=11, fontweight='bold', color=DARK)
    ax.set_ylabel("Animales Infectados Activos (Millones)", fontsize=11, fontweight='bold', color=DARK)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.1f}M"))
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(DARK)
    ax.spines['bottom'].set_color(DARK)
    
    ax.grid(True, linestyle='--', alpha=0.4, color='#BDC3C7')
    ax.legend(loc="upper right", framealpha=0.9, fontsize=10)
    
    plt.tight_layout()
    os.makedirs('../../docs/figures', exist_ok=True)
    img_out = '../../docs/figures/fmd_lockdown_comparison.png'
    plt.savefig(img_out, dpi=300, bbox_inches='tight')
    print(f"[OK] Gráfica de intervención de cerco sanitario generada en: {img_out}")
    plt.close()

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    main()
