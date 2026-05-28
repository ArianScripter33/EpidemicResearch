import geopandas as gpd
import pandas as pd
import json
import os

# Configuración de rutas
RAW_GEO_PATH = '../../data/raw/inegi/estados_mexico.geojson'
RAW_SIAP_PATH = '../../data/raw/siap/inventario_bovino_2023.csv'
OUT_GEO_PATH = '../../data/processed/spatial/nodos_estados.geojson'
OUT_CSV_PATH = '../../data/processed/spatial/nodos_estados.csv'

def normalize_state_name(name):
    """Normaliza los nombres de los estados para evitar errores en el join."""
    mapping = {
        'Estado de México': 'México',
        'Coahuila de Zaragoza': 'Coahuila',
        'Michoacán de Ocampo': 'Michoacán',
        'Veracruz de Ignacio de la Llave': 'Veracruz',
        'Ciudad de México': 'Ciudad de México'
    }
    return mapping.get(name, name)

def main():
    print("=== Fase 1: Extracción y Preprocesamiento ===")
    
    # 1. Cargar datos geográficos
    print(f"Cargando shapefile: {RAW_GEO_PATH}")
    gdf = gpd.read_file(RAW_GEO_PATH)
    
    # 2. Cargar inventario bovino
    print(f"Cargando inventario: {RAW_SIAP_PATH}")
    siap_df = pd.read_csv(RAW_SIAP_PATH)
    siap_df['name'] = siap_df['estado'].apply(normalize_state_name)
    
    # 3. Unir datos (Merge)
    print("Uniendo datos espaciales y tabulares...")
    merged_gdf = gdf.merge(siap_df, on='name', how='left')
    
    # Verificar si hubo estados que no hicieron match
    missing = merged_gdf[merged_gdf['inventario_bovino_2023'].isna()]['name'].tolist()
    if missing:
        print(f"⚠️ ADVERTENCIA: No hubo match para: {missing}")
    
    # 4. Calcular centroides (Proyectar a EPSG:6372 - Mexico LCC para calcular distancias métricas correctas)
    print("Proyectando a EPSG:6372 y calculando centroides...")
    # CRS 6372 es la proyección Cónica Conforme de Lambert para México (mide en metros)
    merged_gdf_proj = merged_gdf.to_crs(epsg=6372)
    merged_gdf_proj['centroid'] = merged_gdf_proj.geometry.centroid
    
    # Extraer coordenadas X e Y del centroide (en metros)
    merged_gdf['centroid_x_m'] = merged_gdf_proj['centroid'].x
    merged_gdf['centroid_y_m'] = merged_gdf_proj['centroid'].y
    
    # Extraer también la latitud y longitud (útiles para web maps/JSON)
    centroids_wgs84 = merged_gdf_proj['centroid'].to_crs(epsg=4326)
    merged_gdf['lon'] = centroids_wgs84.x
    merged_gdf['lat'] = centroids_wgs84.y
    
    # 5. Limpieza final de columnas
    final_gdf = merged_gdf[['name', 'clave', 'inventario_bovino_2023', 'lon', 'lat', 'centroid_x_m', 'centroid_y_m', 'geometry']]
    final_gdf = final_gdf.rename(columns={'name': 'estado'})
    
    # 6. Guardar resultados
    os.makedirs(os.path.dirname(OUT_GEO_PATH), exist_ok=True)
    
    # Guardar como GeoJSON (solo permite una columna geométrica, que será el polígono)
    final_gdf.to_file(OUT_GEO_PATH, driver='GeoJSON')
    print(f"✅ Guardado GeoJSON: {OUT_GEO_PATH}")
    
    # Guardar como CSV (tiramos la geometría pesada, ideal para el modelo Gravity/ML)
    df_csv = pd.DataFrame(final_gdf.drop(columns=['geometry']))
    df_csv.to_csv(OUT_CSV_PATH, index=False)
    print(f"✅ Guardado CSV: {OUT_CSV_PATH}")
    
    print("\nResumen del dataset procesado:")
    print(df_csv[['estado', 'inventario_bovino_2023', 'lon', 'lat']].head())

if __name__ == '__main__':
    # Cambiar el working directory al directorio del script para que las rutas relativas funcionen
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    main()
