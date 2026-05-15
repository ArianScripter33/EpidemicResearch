import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os
from PIL import Image
import io

# Rutas de entrada
GEOJSON_PATH = '../../data/processed/spatial/nodos_estados.geojson'
MATRIX_PATH = '../../data/processed/spatial/matriz_gravedad.csv'
# Rutas de salida
OUT_DIR = '../../data/processed/spatial/frames/'
OUT_GIF = '../../data/processed/spatial/fmd_spread_simulation_180d.gif'
OUT_CSV = '../../data/processed/spatial/sir_simulation_results_180d.csv'
OUT_STATE_HISTORY = '../../data/processed/spatial/sir_state_history_180d.csv'

# Parámetros Epidémicos (FMD)
BETA = 0.6      # Tasa de contagio local muy alta
GAMMA = 0.1     # Tasa de sacrificio/remoción (10 días)
SPATIAL_BETA = 0.8 # Fuerza del contagio entre estados (rutas comerciales)
DIAS_SIMULACION = 180
ESTADO_PACIENTE_CERO = 'Veracruz'

def main():
    print("=== Fase 3: Simulación Espacial SIR y Generación de Animación ===")
    os.makedirs(OUT_DIR, exist_ok=True)
    
    # 1. Cargar Datos
    print("Cargando mapa y red gravitatoria...")
    gdf = gpd.read_file(GEOJSON_PATH)
    matriz = pd.read_csv(MATRIX_PATH)
    
    # Inicializar columnas SIR en el GeoDataFrame
    gdf['S'] = gdf['inventario_bovino_2023']
    gdf['I'] = 0.0
    gdf['R'] = 0.0
    
    # Inyectar Paciente Cero
    idx_zero = gdf.index[gdf['estado'] == ESTADO_PACIENTE_CERO].tolist()[0]
    gdf.at[idx_zero, 'I'] = 100.0  # 100 vacas infectadas inicialmente
    gdf.at[idx_zero, 'S'] -= 100.0
    
    # Crear diccionario de probabilidades espaciales rápido
    # format: {origen: {destino: prob_base}}
    spatial_probs = {}
    for _, row in matriz.iterrows():
        o = row['origen']
        d = row['destino']
        if o not in spatial_probs:
            spatial_probs[o] = {}
        spatial_probs[o][d] = row['probabilidad_contagio_base']
        
    historial = []
    historial_estados = []
    frames = []
    
    print(f"Iniciando simulación de {DIAS_SIMULACION} días...")
    
    # Configuración de mapa
    cmap = plt.cm.Reds
    norm = mcolors.Normalize(vmin=0, vmax=0.3) # Max 30% del hato infectado para saturar el color rojo
    
    # 2. Bucle de Simulación
    np.random.seed(42) # Reproducibilidad
    
    for t in range(DIAS_SIMULACION):
        # Guardar estado actual
        gdf['I_perc'] = gdf['I'] / gdf['inventario_bovino_2023']
        
        # Renderear Frame del mapa
        fig, ax = plt.subplots(1, 1, figsize=(10, 7))
        ax.axis('off')
        ax.set_title(f"Fiebre Aftosa en México - Propagación\nDía {t}", fontsize=16, fontweight='bold')
        
        # Pintar el mapa: gris claro si I_perc == 0, rojo si I_perc > 0
        # Reemplazar NaN o ceros por un valor muy bajo para que cmap funcione, o pintar manual
        gdf.plot(column='I_perc', ax=ax, cmap=cmap, norm=norm, 
                 edgecolor='black', linewidth=0.3,
                 missing_kwds={'color': '#f0f0f0'}) # Fondo gris para sanos
                 
        # Poner los estados con 0 infecciones explícitamente en gris claro
        gdf[gdf['I'] < 1].plot(ax=ax, color='#e0e0e0', edgecolor='black', linewidth=0.3)
        
        # Guardar frame en memoria (sin escribir al disco para ser más rápido)
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        frames.append(Image.open(buf))
        plt.close(fig)
        
        # Registrar métricas globales
        total_I = gdf['I'].sum()
        total_R = gdf['R'].sum()
        historial.append({'dia': t, 'infectados': total_I, 'removidos': total_R})
        
        # Registrar métricas por estado para el Bar Chart Race
        fila_estados = {'dia': t}
        for _, row in gdf.iterrows():
            fila_estados[row['estado']] = int(row['I'])
        historial_estados.append(fila_estados)
        
        print(f"Día {t} | Infectados Totales: {int(total_I):,} | Estados Afectados: {len(gdf[gdf['I'] >= 1])}")
        
        # --- MATEMÁTICA SIR ---
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
        
        for e_inf in estados_infectados:
            idx_inf = gdf.index[gdf['estado'] == e_inf][0]
            prevalencia = gdf.at[idx_inf, 'I'] / gdf.at[idx_inf, 'inventario_bovino_2023']
            
            for e_sano in estados_sanos:
                # Si existe conexión comercial en la matriz gravitatoria
                if e_inf in spatial_probs and e_sano in spatial_probs[e_inf]:
                    prob_base = spatial_probs[e_inf][e_sano]
                    
                    # La probabilidad final depende de la prevalencia en origen y la fuerza gravitatoria
                    prob_infeccion = prob_base * prevalencia * SPATIAL_BETA
                    
                    # Lanzar el dado
                    if np.random.random() < prob_infeccion:
                        # ¡CHISPAZO! Entra el virus al nuevo estado
                        idx_sano = gdf.index[gdf['estado'] == e_sano][0]
                        nuevos_I[idx_sano] += 50.0 # 50 vacas infectadas iniciales por el embarque
        
        # c) Actualizar valores
        gdf['I'] += nuevos_I - nuevos_R
        gdf['S'] -= nuevos_I
        gdf['R'] += nuevos_R
        
        # Evitar negativos por errores de redondeo
        gdf['S'] = gdf['S'].clip(lower=0)
        gdf['I'] = gdf['I'].clip(lower=0)

    # 3. Exportar GIF y Datos
    print("\nGenerando GIF...")
    frames[0].save(OUT_GIF, format='GIF', append_images=frames[1:], save_all=True, duration=200, loop=0)
    print(f"✅ GIF Guardado: {OUT_GIF}")
    
    df_historial = pd.DataFrame(historial)
    df_historial.to_csv(OUT_CSV, index=False)
    print(f"✅ Historial CSV Guardado: {OUT_CSV}")
    
    df_historial_estados = pd.DataFrame(historial_estados)
    df_historial_estados.to_csv(OUT_STATE_HISTORY, index=False)
    print(f"✅ Historial por Estado (Para Bar Chart) Guardado: {OUT_STATE_HISTORY}")
    
if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    main()
