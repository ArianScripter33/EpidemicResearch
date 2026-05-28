import pandas as pd
import requests
import time
import os

INPUT_CSV = '../../data/processed/spatial/nodos_estados.csv'
OUT_DISTANCES = '../../data/processed/spatial/distancias_carretera.csv'

def main():
    print("=== Extracción de Distancias Reales por Carretera ===")
    
    # 1. Cargar Nodos
    df = pd.read_csv(INPUT_CSV)
    
    # Validar que existan lat/lon
    if 'lon' not in df.columns or 'lat' not in df.columns:
        raise ValueError("El archivo de nodos no tiene columnas 'lon' y 'lat'")
    
    # 2. Formatear coordenadas para OSRM
    # OSRM espera: lon,lat;lon,lat;...
    coords = ";".join([f"{row['lon']},{row['lat']}" for _, row in df.iterrows()])
    
    # 3. Llamar a la API pública de OSRM (Open Source Routing Machine)
    # Usamos el servicio 'table' para obtener la matriz NxN de distancias y duraciones
    print(f"Llamando a la API de OSRM para {len(df)} estados...")
    url = f"http://router.project-osrm.org/table/v1/driving/{coords}?annotations=distance"
    
    try:
        # Añadir un User-Agent amable (política de OSRM)
        headers = {'User-Agent': 'EpidemicResearch_GravityModel/1.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if data['code'] != 'Ok':
            raise ValueError(f"Error en OSRM: {data['code']}")
            
        distances_m = data['distances'] # Matriz NxN en metros
        
        # 4. Construir el Edge List
        edges = []
        estados = df['estado'].tolist()
        
        for i, origen in enumerate(estados):
            for j, destino in enumerate(estados):
                if i != j:
                    dist_km = distances_m[i][j] / 1000.0
                    edges.append({
                        'origen': origen,
                        'destino': destino,
                        'distancia_carretera_km': round(dist_km, 2)
                    })
                    
        edges_df = pd.DataFrame(edges)
        
        # 5. Guardar a Disco
        os.makedirs(os.path.dirname(OUT_DISTANCES), exist_ok=True)
        edges_df.to_csv(OUT_DISTANCES, index=False)
        print(f"✅ Matriz de distancias por carretera guardada: {OUT_DISTANCES}")
        
        print("\nTop 5 rutas más largas por carretera:")
        print(edges_df.sort_values('distancia_carretera_km', ascending=False).head().to_string(index=False))
        
    except Exception as e:
        print(f"❌ Error al obtener rutas: {e}")

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    main()
