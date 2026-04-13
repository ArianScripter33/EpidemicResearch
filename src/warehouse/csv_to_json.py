import csv
import json
from collections import defaultdict
import os

def main():
    # Rutas relativas asumiendo que se ejecuta desde la raíz del proyecto o desde src/warehouse
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    input_file = os.path.join(base_dir, 'data', 'processed', 'senasica_cuarentenas_clean.csv')
    output_file = os.path.join(base_dir, 'data', 'processed', 'cuarentenas.json')

    # Diccionario anidado
    data = defaultdict(dict)
    
    total_animales = 0

    with open(input_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            estado = row['estado']
            trimestre = f"Q{row['trimestre']}_{row['anio']}"
            hatos = int(row['num_hatos_cuarentena'])
            animales = int(row['num_animales'])
            
            if trimestre not in data[estado]:
                data[estado][trimestre] = {'hatos': 0, 'animales': 0}
            
            data[estado][trimestre]['hatos'] += hatos
            data[estado][trimestre]['animales'] += animales
            total_animales += animales

    with open(output_file, mode='w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Transformación completa. Archivo guardado en: {output_file}")
    print(f"✅ Total estados en JSON: {len(data.keys())} (Se esperan 27)")
    print(f"✅ Suma de animales total: {total_animales} (Se esperan 7558)")

if __name__ == "__main__":
    main()
