import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import os
from PIL import Image
import io

# Rutas de entrada
GEOJSON_PATH = '../../data/processed/spatial/nodos_estados.geojson'
MATRIX_PATH = '../../data/processed/spatial/matriz_gravedad.csv'
ICON_PATH = '../../data/resources/IconInfected.png'

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
    
    # Intentar pre-cargar el icono de Plague Inc. personalizado
    has_icon = os.path.exists(ICON_PATH)
    icon_img = None
    if has_icon:
        try:
            icon_img = mpimg.imread(ICON_PATH)
            print(f"✅ Icono personalizado cargado correctamente: {ICON_PATH}")
        except Exception as e:
            print(f"⚠️ Error cargando icono en {ICON_PATH}: {e}. Se usará fallback unicode.")
            has_icon = False
    else:
        print(f"ℹ️ No se encontró el icono en {ICON_PATH}. Se usará fallback de texto unicode ☣️.")
    
    # Inicializar columnas SIR en el GeoDataFrame
    gdf['S'] = gdf['inventario_bovino_2023']
    gdf['I'] = 0.0
    gdf['R'] = 0.0
    gdf['dias_infectado'] = 0  # Para la animación estilo Plague Inc.
    
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
    
    # 2. Bucle de Simulación
    np.random.seed(42) # Reproducibilidad
    
    for t in range(DIAS_SIMULACION):
        # 2a. Construir colores dinámicos por estado
        colores = []
        for idx, row in gdf.iterrows():
            total = row['inventario_bovino_2023']
            i_perc = row['I'] / total
            r_perc = row['R'] / total
            
            if row['I'] < 1.0 and row['R'] < 100.0:
                # Sano: Gris claro
                colores.append('#e0e0e0')
            elif r_perc >= 0.90:
                # Extinto / Despoblado por rifle sanitario: Negro
                colores.append('#111111')
            else:
                # Activo. Transiciona de Rojo brillante a Rojo oscuro-negro según los removidos (r_perc)
                factor_rojo = min(1.0, i_perc / 0.3)
                factor_oscuro = min(1.0, r_perc / 0.90)
                
                # Interpolación RGB: disminuye intensidad y brillo conforme sube factor_oscuro
                r = 1.0 - (factor_oscuro * 0.85)
                g = 0.08 * (1.0 - factor_oscuro)
                b = 0.08 * (1.0 - factor_oscuro)
                
                colores.append(mcolors.to_hex((r, g, b)))
        
        gdf['color_actual'] = colores
        
        # Renderear Frame del mapa
        fig, ax = plt.subplots(1, 1, figsize=(11, 8), facecolor='#F8F4F0')
        ax.set_facecolor('#F8F4F0')
        ax.axis('off')
        
        # Título estilo Plague Inc.
        ax.text(0.5, 0.96, f"AftoSec: Vigilancia Epidemiológica Nacional", 
                transform=ax.transAxes, fontsize=15, fontweight='bold', color='#1A1A2E', ha='center')
        ax.text(0.5, 0.92, f"Simulación de Brote de Fiebre Aftosa (FMD) — Día {t}", 
                transform=ax.transAxes, fontsize=12, fontweight='medium', color='#7F8C8D', ha='center')
        
        # Pintar el mapa base usando nuestros colores calculados
        gdf.plot(ax=ax, color=gdf['color_actual'], edgecolor='#2c3e50', linewidth=0.4)
        
        # 2b. Efecto Plague Inc: Dibujar el icono custom apuntando al centroide (arriba de él)
        for idx, row in gdf.iterrows():
            if 0 < row['dias_infectado'] <= 6:
                # Obtener centroide para posicionar el icono
                centroide = row['geometry'].centroid
                
                if has_icon and icon_img is not None:
                    # Escalamos el icono a un tamaño elegante (unas 12-15 veces más pequeño que el original)
                    zoom_factor = 0.018 + (t % 3) * 0.003
                    
                    imagebox = OffsetImage(icon_img, zoom=zoom_factor)
                    # box_alignment=(0.5, 0.0) alinea la base central del icono con el punto (queda directamente ARRIBA del centroide)
                    ab = AnnotationBbox(imagebox, (centroide.x, centroide.y),
                                        xycoords='data',
                                        box_alignment=(0.5, 0.0),
                                        pad=0.0,
                                        frameon=False,
                                        zorder=5)
                    ax.add_artist(ab)
                    
                    # Dibujar círculo de advertencia rojo suave justo en el centroide como base del impacto
                    ax.plot(centroide.x, centroide.y, marker='o', color='#E74C3C', 
                            markersize=4 + (t % 3) * 1.5, alpha=0.3, zorder=4)
                else:
                    # Fallback al símbolo unicode si no se encuentra o falla el archivo de imagen
                    size_pulse = 14 + (t % 3) * 2
                    ax.plot(centroide.x, centroide.y, marker='o', color='#E74C3C', 
                            markersize=size_pulse + 5, alpha=0.3, zorder=4)
                    ax.text(centroide.x, centroide.y, "☣️", fontsize=size_pulse, 
                            color='#E74C3C', ha='center', va='center', fontweight='bold', zorder=5)
        
        # 2c. Leyenda explicativa personalizada
        leyenda_elementos = [
            plt.Line2D([0], [0], marker='s', color='w', label='🟢 Susceptible (Sano)', 
                       markerfacecolor='#e0e0e0', markersize=12, markeredgecolor='black'),
            plt.Line2D([0], [0], marker='s', color='w', label='🔴 Brote Activo Inicial', 
                       markerfacecolor='#FF1E1E', markersize=12, markeredgecolor='black'),
            plt.Line2D([0], [0], marker='s', color='w', label='🟤 Epidemia Avanzada', 
                       markerfacecolor='#5C0505', markersize=12, markeredgecolor='black'),
            plt.Line2D([0], [0], marker='s', color='w', label='⚫ Extinto / Despoblado por Rifle Sanitario', 
                       markerfacecolor='#111111', markersize=12, markeredgecolor='black'),
            plt.Line2D([0], [0], marker='None', color='w', label='📍  Alerta de Brote Pecuario Reciente', 
                       markerfacecolor='none', markersize=10, markeredgewidth=0)
        ]
        
        ax.legend(handles=leyenda_elementos, loc="lower left", framealpha=0.9, 
                  facecolor='#FFFFFF', edgecolor='#BDC3C7', fontsize=9.5, 
                  title="Estado del Hato Bovino", title_fontsize=10.5)
        
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
        
        print(f"Día {t} | Infectados: {int(total_I):,} | Despoblados: {len(gdf[gdf['R']/gdf['inventario_bovino_2023'] >= 0.90])} | Activos ☣️: {len(gdf[gdf['dias_infectado'] > 0])}")
        
        # --- MATEMÁTICA SIR ---
        nuevos_I = np.zeros(len(gdf))
        nuevos_R = np.zeros(len(gdf))
        
        # Incrementar contador de días infectado para los estados activos
        for idx, row in gdf.iterrows():
            if row['I'] >= 1.0:
                gdf.at[idx, 'dias_infectado'] += 1
            else:
                gdf.at[idx, 'dias_infectado'] = 0
        
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
                    
                    # Añadimos un piso mínimo (epsilon de 0.015) para evitar que el decaimiento por distancia
                    # deje permanentemente inmunes a estados remotos (Bajas y Quintana Roo)
                    prob_base_calibrada = max(0.015, prob_base)
                    
                    # La probabilidad final depende de la prevalencia en origen y la fuerza gravitatoria
                    prob_infeccion = prob_base_calibrada * prevalencia * SPATIAL_BETA
                    
                    # Lanzar el dado
                    if np.random.random() < prob_infeccion:
                        # ¡CHISPAZO! Entra el virus al nuevo estado
                        idx_sano = gdf.index[gdf['estado'] == e_sano][0]
                        # Solo se infecta si no ha sido ya devastado
                        if gdf.at[idx_sano, 'S'] > 50.0:
                            nuevos_I[idx_sano] += 50.0 # 50 vacas infectadas iniciales por el embarque
                            gdf.at[idx_sano, 'dias_infectado'] = 1 # Empieza contador
        
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
