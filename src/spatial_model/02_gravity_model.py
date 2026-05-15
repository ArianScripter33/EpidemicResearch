import pandas as pd
import numpy as np
import json
import os

# Configuración de rutas
INPUT_CSV = '../../data/processed/spatial/nodos_estados.csv'
OUT_MATRIX_CSV = '../../data/processed/spatial/matriz_gravedad.csv'
OUT_EDGES_JSON = '../../data/processed/spatial/edges_gravedad.json'
INPUT_DISTANCES_CSV = '../../data/processed/spatial/distancias_carretera.csv'

# Parámetros del Modelo Gravitatorio
# F_ij = k * (P_i^alpha * P_j^beta) / d_ij^gamma
ALPHA = 1.0  # Peso del inventario de origen
BETA = 1.0   # Peso del inventario de destino
GAMMA = 2.0  # Decaimiento por distancia (al cuadrado, ley de gravedad de Newton)
K_SCALAR = 1e-6 # Escalar para evitar números inmensos (puede ajustarse para calibrar)

def main():
    print("=== Fase 2: Modelo Gravitatorio (Cálculo de Flujos) ===")
    
    # 1. Cargar Nodos
    df = pd.read_csv(INPUT_CSV)
    df_dist = pd.read_csv(INPUT_DISTANCES_CSV)
    
    estados = df['estado'].tolist()
    n = len(estados)
    print(f"Calculando red para {n} nodos (estados) usando distancias reales por carretera...")
    
    edges = []
    
    # 2. Generar Matriz NxN
    for i in range(n):
        for j in range(n):
            if i == j:
                continue # No calculamos auto-flujo
                
            est_o = df.iloc[i]
            est_d = df.iloc[j]
            
            # Poblaciones (Masas)
            P_i = est_o['inventario_bovino_2023']
            P_j = est_d['inventario_bovino_2023']
            
            # Buscar distancia real por carretera
            dist_row = df_dist[(df_dist['origen'] == est_o['estado']) & (df_dist['destino'] == est_d['estado'])]
            if not dist_row.empty:
                d_ij = dist_row.iloc[0]['distancia_carretera_km']
            else:
                # Fallback de seguridad (no debería ocurrir)
                d_ij = 100.0 
                
            # Para evitar división por 0 o distancias irreales (<1km entre estados)
            if d_ij < 1.0: 
                d_ij = 1.0
                
            # Fórmula Gravitatoria
            F_ij = K_SCALAR * ((P_i**ALPHA * P_j**BETA) / (d_ij**GAMMA))
            
            edges.append({
                'origen': est_o['estado'],
                'destino': est_d['estado'],
                'distancia_km': round(d_ij, 2),
                'flujo_gravedad': F_ij,
                # Para XGBoost o análisis de red, guardamos los id:
                'origen_id': est_o['clave'],
                'destino_id': est_d['clave']
            })
            
    # 3. Guardar en formato DataFrame (Edge List)
    edges_df = pd.DataFrame(edges)
    
    # Normalizar los flujos entre 0 y 1 para tener "Probabilidades de Contagio Relativas"
    max_flujo = edges_df['flujo_gravedad'].max()
    edges_df['probabilidad_contagio_base'] = edges_df['flujo_gravedad'] / max_flujo
    
    # 4. Guardar a Disco
    edges_df.to_csv(OUT_MATRIX_CSV, index=False)
    print(f"✅ Guardada matriz CSV: {OUT_MATRIX_CSV} ({len(edges_df)} conexiones posibles)")
    
    # También guardamos como JSON para fácil lectura en D3.js, React o la Web App
    edges_json = edges_df.to_dict(orient='records')
    with open(OUT_EDGES_JSON, 'w', encoding='utf-8') as f:
        json.dump(edges_json, f, ensure_ascii=False, indent=2)
    print(f"✅ Guardado JSON: {OUT_EDGES_JSON}")
    
    # Mostrar las rutas más peligrosas (top 5)
    print("\n🔥 TOP 5 RUTAS DE MAYOR RIESGO EPIDEMIOLÓGICO (Más flujo esperado):")
    top_rutas = edges_df.sort_values(by='flujo_gravedad', ascending=False).head(5)
    print(top_rutas[['origen', 'destino', 'distancia_km', 'probabilidad_contagio_base']].to_string(index=False))

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    main()
