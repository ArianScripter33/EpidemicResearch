import csv
import json
import os
from pydantic import BaseModel

# 1. Definimos nuestro modelo
class CuarentenaRecord(BaseModel):
    estado: str
    num_animales: int
    trimestre: int
    num_hatos_cuarentena: int
    anio: int

def main():
    # Detectamos la ruta automáticamente para que funcione donde sea
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ruta_csv = os.path.join(base_dir, 'data', 'processed', 'senasica_cuarentenas_clean.csv')
    ruta_json = os.path.join(base_dir, 'data', 'processed', 'cuarentenas.json')
    
    # Aquí organizaremos nuestros datos
    datos_agrupados = {}

    with open(ruta_csv, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        
        for fila in lector:
            # 2. Validación de Tipos (Lo vuelve Python object)
            registro = CuarentenaRecord(**fila)
            
            # 3. Concatenamos para crear la llave del Trimestre Ej. "Q4_2024"
            llave_trimestre = f"Q{registro.trimestre}_{registro.anio}"

            # 4. Construcción del Árbol de Diccionarios (Anidación)
            # Primero: Si el Estado no existe, le creamos su espacio vacío
            if registro.estado not in datos_agrupados:
                datos_agrupados[registro.estado] = {}
            
            # Segundo: Si dentro de ese Estado, el trimestre no existe, arrancamos en ceros
            if llave_trimestre not in datos_agrupados[registro.estado]:
                datos_agrupados[registro.estado][llave_trimestre] = {"hatos": 0, "animales": 0}
                
            # 5. La Sumatoria Acumulada
            # Aquí ocurre la magia matemática (+="agrega esto al valor actual")
            datos_agrupados[registro.estado][llave_trimestre]["hatos"] += registro.num_hatos_cuarentena
            datos_agrupados[registro.estado][llave_trimestre]["animales"] += registro.num_animales

    # 6. Escribimos y exportamos todo al disco duro
    with open(ruta_json, mode='w', encoding='utf-8') as archivo_json:
        json.dump(datos_agrupados, archivo_json, ensure_ascii=False, indent=2)
        
    print(f"✅ ¡Transformación completada!")
    print(f"Se procesaron los datos a formato JSON y puedes verlos en data/processed/cuarentenas.json")

if __name__ == '__main__':
    main()
