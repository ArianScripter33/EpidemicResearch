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

# Rutas de salida para el escenario de cuarentena
OUT_DIR = '../../data/processed/spatial/frames_lockdown/'
OUT_GIF = '../../data/processed/spatial/fmd_lockdown_simulation_180d.gif'

# Parámetros Epidémicos (FMD)
BETA = 0.6
GAMMA = 0.1
SPATIAL_BETA = 0.8
DIAS_SIMULACION = 180
ESTADO_PACIENTE_CERO = 'Veracruz'
LOCKDOWN_DAY = 12

def main():
    print("=== Generando Mapa Animado con Cerco Sanitario (Lockdown) ===")
    os.makedirs(OUT_DIR, exist_ok=True)
    
    # 1. Cargar Datos
    gdf = gpd.read_file(GEOJSON_PATH)
    matriz = pd.read_csv(MATRIX_PATH)
    
    has_icon = os.path.exists(ICON_PATH)
    icon_img = None
    if has_icon:
        try:
            icon_img = mpimg.imread(ICON_PATH)
            print(f"✅ Icono cargado: {ICON_PATH}")
        except:
            has_icon = False
            
    # Inicializar columnas SIR
    gdf['S'] = gdf['inventario_bovino_2023'].astype(float)
    gdf['I'] = 0.0
    gdf['R'] = 0.0
    gdf['dias_infectado'] = 0
    
    # Inyectar Paciente Cero
    idx_zero = gdf.index[gdf['estado'] == ESTADO_PACIENTE_CERO].tolist()[0]
    gdf.at[idx_zero, 'I'] = 100.0
    gdf.at[idx_zero, 'S'] -= 100.0
    
    spatial_probs = {}
    for _, row in matriz.iterrows():
        o = row['origen']
        d = row['destino']
        if o not in spatial_probs:
            spatial_probs[o] = {}
        spatial_probs[o][d] = row['probabilidad_contagio_base']
        
    frames = []
    np.random.seed(42)
    
    estados_bloqueados = ['Veracruz', 'Tabasco', 'Puebla', 'Oaxaca']
    
    for t in range(DIAS_SIMULACION):
        # Construir colores dinámicos
        colores = []
        for idx, row in gdf.iterrows():
            total = row['inventario_bovino_2023']
            i_perc = row['I'] / total
            r_perc = row['R'] / total
            
            if row['I'] < 1.0 and row['R'] < 100.0:
                colores.append('#e0e0e0')  # Sano
            elif r_perc >= 0.90:
                colores.append('#111111')  # Despoblado
            else:
                # Transición de rojo según avance
                factor_rojo = min(1.0, i_perc / 0.3)
                factor_oscuro = min(1.0, r_perc / 0.90)
                r = 1.0 - (factor_oscuro * 0.85)
                g = 0.08 * (1.0 - factor_oscuro)
                b = 0.08 * (1.0 - factor_oscuro)
                colores.append(mcolors.to_hex((r, g, b)))
                
        gdf['color_actual'] = colores
        
        # Iniciar figura
        fig, ax = plt.subplots(1, 1, figsize=(11, 8), facecolor='#F8F4F0')
        ax.set_facecolor('#F8F4F0')
        ax.axis('off')
        
        # Títulos dinámicos según estado de cuarentena
        if t >= LOCKDOWN_DAY:
            ax.text(0.5, 0.96, f"AftoSec: Vigilancia Epidemiológica Nacional", 
                    transform=ax.transAxes, fontsize=15, fontweight='bold', color='#1A1A2E', ha='center')
            ax.text(0.5, 0.92, f"🔴 CERCO SANITARIO ACTIVO (Día {LOCKDOWN_DAY}) | Cierre Comercial Golfo-Sur", 
                    transform=ax.transAxes, fontsize=12, fontweight='bold', color='#C0392B', ha='center')
        else:
            ax.text(0.5, 0.96, f"AftoSec: Vigilancia Epidemiológica Nacional", 
                    transform=ax.transAxes, fontsize=15, fontweight='bold', color='#1A1A2E', ha='center')
            ax.text(0.5, 0.92, f"Simulación de Brote de Fiebre Aftosa (FMD) — Día {t}", 
                    transform=ax.transAxes, fontsize=12, fontweight='medium', color='#7F8C8D', ha='center')
            
        # Pintar estados
        gdf.plot(ax=ax, color=gdf['color_actual'], edgecolor='#2c3e50', linewidth=0.4)
        
        # Dibujar cerco sanitario visual grueso (Línea naranja discontinua) en los estados bloqueados
        if t >= LOCKDOWN_DAY:
            gdf[gdf['estado'].isin(estados_bloqueados)].plot(
                ax=ax, facecolor='none', edgecolor='#E67E22', linewidth=1.5, linestyle='--', zorder=3
            )
            # Agregar indicador textual en el Golfo
            ax.text(gdf[gdf['estado'] == 'Veracruz'].geometry.centroid.x.values[0] - 1.0,
                    gdf[gdf['estado'] == 'Veracruz'].geometry.centroid.y.values[0] + 1.2,
                    "⚠️ Bloqueo Vial", color='#E67E22', fontsize=9.5, fontweight='bold',
                    bbox=dict(facecolor='white', alpha=0.8, edgecolor='#E67E22', boxstyle='round,pad=0.3'))
            
        # Dibujar iconos de infección Plague Inc.
        for idx, row in gdf.iterrows():
            if 0 < row['dias_infectado'] <= 6:
                centroide = row['geometry'].centroid
                if has_icon and icon_img is not None:
                    zoom_factor = 0.018 + (t % 3) * 0.003
                    imagebox = OffsetImage(icon_img, zoom=zoom_factor)
                    ab = AnnotationBbox(imagebox, (centroide.x, centroide.y),
                                        xycoords='data', box_alignment=(0.5, 0.0),
                                        pad=0.0, frameon=False, zorder=5)
                    ax.add_artist(ab)
                    ax.plot(centroide.x, centroide.y, marker='o', color='#E74C3C', 
                            markersize=4 + (t % 3) * 1.5, alpha=0.3, zorder=4)
                else:
                    size_pulse = 14 + (t % 3) * 2
                    ax.plot(centroide.x, centroide.y, marker='o', color='#E74C3C', 
                            markersize=size_pulse + 5, alpha=0.3, zorder=4)
                    ax.text(centroide.x, centroide.y, "☣️", fontsize=size_pulse, 
                            color='#E74C3C', ha='center', va='center', fontweight='bold', zorder=5)
                    
        # Leyenda
        leyenda_elementos = [
            plt.Line2D([0], [0], marker='s', color='w', label='🟢 Susceptible (Sano)', 
                       markerfacecolor='#e0e0e0', markersize=12, markeredgecolor='black'),
            plt.Line2D([0], [0], marker='s', color='w', label='🔴 Brote Activo Inicial', 
                       markerfacecolor='#FF1E1E', markersize=12, markeredgecolor='black'),
            plt.Line2D([0], [0], marker='s', color='w', label='⚫ Despoblado por Control', 
                       markerfacecolor='#111111', markersize=12, markeredgecolor='black'),
            plt.Line2D([0], [0], color='#E67E22', linestyle='--', label='🟠 Límite de Cerco Sanitario', 
                       linewidth=2)
        ]
        
        ax.legend(handles=leyenda_elementos, loc="lower left", framealpha=0.9, 
                  facecolor='#FFFFFF', edgecolor='#BDC3C7', fontsize=9.5, 
                  title="Estado de Contención", title_fontsize=10.5)
        
        # Guardar en memoria
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        frames.append(Image.open(buf))
        plt.close(fig)
        
        # --- MATEMÁTICA SIR CON LOCKDOWN ---
        nuevos_I = np.zeros(len(gdf))
        nuevos_R = np.zeros(len(gdf))
        
        for idx, row in gdf.iterrows():
            if row['I'] >= 1.0:
                gdf.at[idx, 'dias_infectado'] += 1
            else:
                gdf.at[idx, 'dias_infectado'] = 0
                
        # a) Propagación Local
        for i, row in gdf.iterrows():
            if row['I'] > 0:
                S = row['S']
                I = row['I']
                N = row['inventario_bovino_2023']
                delta_I = min(S, BETA * S * I / N)
                delta_R = min(I, GAMMA * I)
                nuevos_I[i] += delta_I
                nuevos_R[i] += delta_R
                
        # b) Propagación Espacial con Bloqueo
        estados_infectados = gdf[gdf['I'] >= 1]['estado'].tolist()
        estados_sanos = gdf[gdf['I'] < 1]['estado'].tolist()
        
        for e_inf in estados_infectados:
            idx_inf = gdf.index[gdf['estado'] == e_inf][0]
            prevalencia = gdf.at[idx_inf, 'I'] / gdf.at[idx_inf, 'inventario_bovino_2023']
            
            for e_sano in estados_sanos:
                # Interrupción de transporte en red
                if t >= LOCKDOWN_DAY:
                    if e_inf in estados_bloqueados or e_sano in estados_bloqueados:
                        continue
                        
                if e_inf in spatial_probs and e_sano in spatial_probs[e_inf]:
                    prob_base = spatial_probs[e_inf][e_sano]
                    prob_base_calibrada = max(0.015, prob_base)
                    
                    prob_infeccion = prob_base_calibrada * prevalencia * SPATIAL_BETA
                    
                    if np.random.random() < prob_infeccion:
                        idx_sano = gdf.index[gdf['estado'] == e_sano][0]
                        if gdf.at[idx_sano, 'S'] > 50.0:
                            nuevos_I[idx_sano] += 50.0
                            gdf.at[idx_sano, 'dias_infectado'] = 1
                            
        # c) Actualizar
        gdf['I'] += nuevos_I - nuevos_R
        gdf['S'] -= nuevos_I
        gdf['R'] += nuevos_R
        
        gdf['S'] = gdf['S'].clip(lower=0)
        gdf['I'] = gdf['I'].clip(lower=0)
        
        print(f"Cuarentena Día {t} | Infectados: {int(gdf['I'].sum()):,} | Cerco: {'ACTIVO' if t >= LOCKDOWN_DAY else 'Inactivo'}")
        
    print("\nGenerando GIF de Cuarentena...")
    frames[0].save(OUT_GIF, format='GIF', append_images=frames[1:], save_all=True, duration=200, loop=0)
    print(f"✅ GIF de Cuarentena Guardado: {OUT_GIF}")

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    main()
