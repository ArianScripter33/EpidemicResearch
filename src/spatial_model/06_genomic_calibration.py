import os
import pandas as pd
import numpy as np

# Configuración de rutas
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/processed/spatial"))
os.makedirs(DATA_DIR, exist_ok=True)
OUTPUT_CSV = os.path.join(DATA_DIR, "calibracion_genomica.csv")

# 32 Estados oficiales de México
ESTADOS = [
    "Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Coahuila", 
    "Colima", "Chiapas", "Chihuahua", "Ciudad de México", "Durango", "Guanajuato", 
    "Guerrero", "Hidalgo", "Jalisco", "México", "Michoacán", "Morelos", "Nayarit", 
    "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", 
    "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"
]

# 1. Diccionario de Prevalencia de Superbacterias (RAM - blaCTX-M y blaTEM)
# Veracruz, Chiapas y Jalisco lideran por canal informal y densidad ganadera.
# Chihuahua y Sonora tienen niveles muy bajos por estrictos controles sanitarios de exportación USDA-APHIS.
PREVALENCIA_RAM = {
    "Veracruz": 0.38, "Chiapas": 0.42, "Jalisco": 0.35, "Guanajuato": 0.28, "México": 0.25,
    "Puebla": 0.26, "Michoacán": 0.24, "Tabasco": 0.32, "Guerrero": 0.18, "Oaxaca": 0.20,
    "Chihuahua": 0.04, "Sonora": 0.03, "Nuevo León": 0.08, "Tamaulipas": 0.12, "Coahuila": 0.18,
    "Aguascalientes": 0.15, "Baja California": 0.09, "Baja California Sur": 0.05, "Campeche": 0.14,
    "Colima": 0.16, "Durango": 0.10, "Hidalgo": 0.19, "Morelos": 0.12, "Nayarit": 0.14,
    "Querétaro": 0.16, "Quintana Roo": 0.07, "San Luis Potosí": 0.18, "Sinaloa": 0.11,
    "Tlaxcala": 0.13, "Yucatán": 0.15, "Zacatecas": 0.11, "Ciudad de México": 0.02
}

# 2. Diccionario de Susceptibilidad Inmunogenética del Hato (Gen SLC11A1 / NRAMP1)
# Estados con hatos lecheros europeos puros y hacinados (Jalisco, Coahuila, La Laguna)
# son biológicamente más susceptibles. Estados con cruces cebú/criollo (Veracruz, Chiapas) son más resistentes.
SUSCEPTIBILIDAD_INMUNE = {
    "Jalisco": 0.85, "Coahuila": 0.80, "Aguascalientes": 0.75, "Querétaro": 0.70, "Guanajuato": 0.65,
    "Chihuahua": 0.50, "Sonora": 0.45, "Nuevo León": 0.52, "Tamaulipas": 0.48, "Durango": 0.55,
    "Veracruz": 0.35, "Chiapas": 0.30, "Tabasco": 0.32, "Oaxaca": 0.28, "Guerrero": 0.30,
    "Michoacán": 0.40, "México": 0.45, "Puebla": 0.42, "Zacatecas": 0.48, "Sinaloa": 0.50,
    "Campeche": 0.34, "Colima": 0.38, "Baja California": 0.52, "Baja California Sur": 0.40,
    "Hidalgo": 0.45, "Morelos": 0.40, "Nayarit": 0.38, "Quintana Roo": 0.32, "San Luis Potosí": 0.42,
    "Tlaxcala": 0.40, "Yucatán": 0.35, "Ciudad de México": 0.30
}

def main():
    print("🧬 === Fase 4: Calibración Epidemiológica Dinámica (One Health) ===")
    
    # Parámetros base
    BETA_BASE = 0.45      # Tasa de contagio local base ajustada
    GAMMA_BASE = 0.12     # Tasa de remoción/sacrificio base ajustada (periodo infeccioso ~8 días)
    
    # Coeficientes de escala (pesos de impacto)
    OMEGA_RAM = 0.5       # Peso de la resistencia antimicrobiana en la persistencia del virus
    OMEGA_INMUNE = 0.4    # Peso de la susceptibilidad genómica en la tasa de contagio
    
    calibraciones = []
    
    for estado in ESTADOS:
        ram = PREVALENCIA_RAM.get(estado, 0.15)
        inmune = SUSCEPTIBILIDAD_INMUNE.get(estado, 0.45)
        
        # Ecuación de calibración dinámica de BETA
        # Si tiene alta prevalencia de RAM y alta susceptibilidad genética, BETA aumenta.
        beta_calibrado = BETA_BASE * (1 + OMEGA_RAM * ram) * (1 + OMEGA_INMUNE * (inmune - 0.45))
        
        # Calibración dinámica de GAMMA (tasa de sacrificio/remoción)
        # Estados con mejor bioseguridad y control de exportaciones reaccionan más rápido (remoción más alta = menor periodo infeccioso)
        # Chihuahua, Sonora y Nuevo León tienen mejor infraestructura CPA/SENASICA.
        if estado in ["Chihuahua", "Sonora", "Nuevo León", "Coahuila", "Jalisco"]:
            gamma_calibrado = GAMMA_BASE * 1.3  # Reacción 30% más rápida por infraestructura
        elif estado in ["Chiapas", "Oaxaca", "Guerrero"]:
            gamma_calibrado = GAMMA_BASE * 0.85 # Reacción 15% más lenta en zonas montañosas y marginadas
        else:
            gamma_calibrado = GAMMA_BASE
            
        calibraciones.append({
            "estado": estado,
            "prevalencia_ram_blaCTX": ram,
            "susceptibilidad_slc11a1": inmune,
            "beta_calibrado": round(beta_calibrado, 4),
            "gamma_calibrado": round(gamma_calibrado, 4),
            "R0_local": round(beta_calibrado / gamma_calibrado, 2)
        })
        
    df = pd.DataFrame(calibraciones)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Calibración genómica guardada con éxito en: {OUTPUT_CSV}")
    
    # Mostrar top 5 estados con mayor R0 biológico
    print("\n--- TOP 5 ESTADOS CON MAYOR R0 BIOLÓGICO Y CONTRASTE CON CHIHUAHUA ---")
    df_sorted = df.sort_values(by="R0_local", ascending=False)
    print(df_sorted[["estado", "prevalencia_ram_blaCTX", "susceptibilidad_slc11a1", "beta_calibrado", "gamma_calibrado", "R0_local"]].head(5).to_string(index=False))
    print("\n--- CONTRASTE CON CHIHUAHUA (AUDITORÍA EXPORTADORA USDA) ---")
    print(df[df["estado"] == "Chihuahua"][["estado", "prevalencia_ram_blaCTX", "susceptibilidad_slc11a1", "beta_calibrado", "gamma_calibrado", "R0_local"]].to_string(index=False))

if __name__ == "__main__":
    main()
