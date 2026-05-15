"""
03b_sir_full_history.py
-----------------------
Re-corre la simulación SIR espacial de 180 días pero guarda los 3 compartimentos
(S, I, R) por estado por día. Esto alimenta:
  - La gráfica apilada S-I-R
  - El modelo XGBoost (features de grafo + SIR)
"""
import geopandas as gpd
import pandas as pd
import numpy as np
import os

# Rutas
GEOJSON_PATH = '../../data/processed/spatial/nodos_estados.geojson'
MATRIX_PATH = '../../data/processed/spatial/matriz_gravedad.csv'
OUT_FULL = '../../data/processed/spatial/sir_full_state_history_180d.csv'

# Parámetros (idénticos al 03_spatial_sir.py para reproducibilidad)
BETA = 0.6
GAMMA = 0.1
SPATIAL_BETA = 0.8
DIAS_SIMULACION = 180
ESTADO_PACIENTE_CERO = 'Veracruz'

def main():
    print("=== Fase 3b: Generación de Historial Completo S-I-R por Estado ===")
    
    gdf = gpd.read_file(GEOJSON_PATH)
    matriz = pd.read_csv(MATRIX_PATH)
    
    gdf['S'] = gdf['inventario_bovino_2023'].astype(float)
    gdf['I'] = 0.0
    gdf['R'] = 0.0
    
    idx_zero = gdf.index[gdf['estado'] == ESTADO_PACIENTE_CERO].tolist()[0]
    gdf.at[idx_zero, 'I'] = 100.0
    gdf.at[idx_zero, 'S'] -= 100.0
    
    spatial_probs = {}
    for _, row in matriz.iterrows():
        o, d = row['origen'], row['destino']
        if o not in spatial_probs:
            spatial_probs[o] = {}
        spatial_probs[o][d] = row['probabilidad_contagio_base']
    
    registros = []
    np.random.seed(42)
    
    for t in range(DIAS_SIMULACION):
        # Guardar snapshot de los 3 compartimentos
        for _, row in gdf.iterrows():
            registros.append({
                'dia': t,
                'estado': row['estado'],
                'S': int(row['S']),
                'I': int(row['I']),
                'R': int(row['R']),
                'N': int(row['inventario_bovino_2023']),
                'I_perc': row['I'] / row['inventario_bovino_2023'] if row['inventario_bovino_2023'] > 0 else 0,
                'R_perc': row['R'] / row['inventario_bovino_2023'] if row['inventario_bovino_2023'] > 0 else 0,
            })
        
        if t % 30 == 0:
            total_I = gdf['I'].sum()
            total_R = gdf['R'].sum()
            n_afectados = len(gdf[gdf['I'] >= 1])
            print(f"  Día {t:3d} | I: {int(total_I):>12,} | R (Sacrificados): {int(total_R):>12,} | Estados: {n_afectados}")
        
        # --- MATEMÁTICA SIR (idéntica al 03) ---
        nuevos_I = np.zeros(len(gdf))
        nuevos_R = np.zeros(len(gdf))
        
        for i, row in gdf.iterrows():
            if row['I'] > 0:
                S, I, N = row['S'], row['I'], row['inventario_bovino_2023']
                nuevos_I[i] += min(S, BETA * S * I / N)
                nuevos_R[i] += min(I, GAMMA * I)
        
        estados_infectados = gdf[gdf['I'] >= 1]['estado'].tolist()
        estados_sanos = gdf[gdf['I'] < 1]['estado'].tolist()
        
        for e_inf in estados_infectados:
            idx_inf = gdf.index[gdf['estado'] == e_inf][0]
            prevalencia = gdf.at[idx_inf, 'I'] / gdf.at[idx_inf, 'inventario_bovino_2023']
            for e_sano in estados_sanos:
                if e_inf in spatial_probs and e_sano in spatial_probs[e_inf]:
                    prob_base = spatial_probs[e_inf][e_sano]
                    if np.random.random() < prob_base * prevalencia * SPATIAL_BETA:
                        idx_sano = gdf.index[gdf['estado'] == e_sano][0]
                        nuevos_I[idx_sano] += 50.0
        
        gdf['I'] += nuevos_I - nuevos_R
        gdf['S'] -= nuevos_I
        gdf['R'] += nuevos_R
        gdf['S'] = gdf['S'].clip(lower=0)
        gdf['I'] = gdf['I'].clip(lower=0)
    
    df = pd.DataFrame(registros)
    os.makedirs(os.path.dirname(OUT_FULL), exist_ok=True)
    df.to_csv(OUT_FULL, index=False)
    print(f"\n✅ Historial completo S-I-R guardado: {OUT_FULL}")
    print(f"   {len(df)} registros ({DIAS_SIMULACION} días x {len(gdf)} estados)")
    
    # Resumen final
    dia_final = df[df['dia'] == DIAS_SIMULACION - 1]
    print(f"\n--- Resumen Día {DIAS_SIMULACION - 1} ---")
    print(f"   Susceptibles restantes:  {dia_final['S'].sum():>12,}")
    print(f"   Infectados activos:      {dia_final['I'].sum():>12,}")
    print(f"   Removidos (Sacrificados):{dia_final['R'].sum():>12,}")

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    main()
