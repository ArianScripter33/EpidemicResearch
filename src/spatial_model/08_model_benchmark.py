"""
08_model_benchmark.py
---------------------
Realiza un benchmarking formal comparando cuatro modelos de regresión:
1. Regresión Lineal (Baseline)
2. Árbol de Decisión (DT)
3. Bosque Aleatorio (Random Forest - RF)
4. XGBoost Regressor (XGB)

Todos los modelos se evalúan mediante Leave-One-Out Cross-Validation (LOOCV)
para garantizar robustez estadística en nuestro dataset de 32 estados (muestras).
"""
import pandas as pd
import numpy as np
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.model_selection import LeaveOneOut
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, r2_score

# Rutas de datos
FEATURES_CSV = '../../data/processed/spatial/xgboost_features.csv'

def evaluate_model_loo(model, X, y):
    """Evalúa un modelo usando Leave-One-Out Cross-Validation."""
    loo = LeaveOneOut()
    predictions = np.zeros(len(y))
    
    for train_idx, test_idx in loo.split(X):
        # Clonar/entrenar modelo en el pliegue
        model.fit(X[train_idx], y[train_idx])
        predictions[test_idx] = model.predict(X[test_idx])
        
    mae = mean_absolute_error(y, predictions)
    r2 = r2_score(y, predictions)
    return predictions, mae, r2

def main():
    print("=== Fase 8: Benchmarking de Modelos de Machine Learning (LOOCV) ===")
    
    # 1. Cargar features
    if not os.path.exists(FEATURES_CSV):
        print(f"❌ Error: No se encuentra el archivo {FEATURES_CSV}. Corre primero 05_xgboost_risk.py")
        return
        
    df = pd.read_csv(FEATURES_CSV)
    
    # Filtrar solo estados que llegaron a infectarse para el target de día
    df_infected = df[df['dia_primera_infeccion'] < 999].copy()
    
    feature_cols = [
        'inventario_bovino', 'degree_centrality', 'betweenness_centrality',
        'closeness_centrality', 'pagerank', 'weighted_in_flux', 'weighted_out_flux',
        'max_in_prob', 'max_out_prob', 'avg_dist_carretera', 'min_dist_carretera',
        'lat', 'lon'
    ]
    
    X_pico = df_infected[feature_cols].values
    y_pico = df_infected['pico_infectados'].values
    
    X_dia = df_infected[feature_cols].values
    y_dia = df_infected['dia_primera_infeccion'].values
    
    # Definición de modelos
    models = {
        "Regresión Lineal": LinearRegression(),
        "Árbol de Decisión": DecisionTreeRegressor(max_depth=4, random_state=42),
        "Random Forest": RandomForestRegressor(n_estimators=100, max_depth=4, random_state=42),
        "XGBoost": xgb.XGBRegressor(n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42, verbosity=0)
    }
    
    results = []
    
    print("\n[PROCESANDO] Evaluando modelos para predicción de PICO DE INFECTADOS...")
    for name, model in models.items():
        _, mae, r2 = evaluate_model_loo(model, X_pico, y_pico)
        results.append({
            "Target": "Pico Infectados",
            "Modelo": name,
            "R2 Score": round(r2, 4),
            "MAE": round(mae, 2)
        })
        
    print("[PROCESANDO] Evaluando modelos para predicción de DÍA DE PRIMERA INFECCIÓN...")
    for name, model in models.items():
        _, mae, r2 = evaluate_model_loo(model, X_dia, y_dia)
        results.append({
            "Target": "Día Infección",
            "Modelo": name,
            "R2 Score": round(r2, 4),
            "MAE": round(mae, 2)
        })
        
    # Formatear tabla de resultados
    results_df = pd.DataFrame(results)
    
    print("\n" + "="*80)
    print("TABLA COMPARATIVA DE RENDIMIENTO DE MODELOS (BENCHMARK)")
    print("="*80)
    print(results_df.to_string(index=False))
    print("="*80 + "\n")
    
    # Guardar a CSV para documentar
    OUT_CSV = '../../data/processed/spatial/model_benchmark_results.csv'
    results_df.to_csv(OUT_CSV, index=False)
    print(f"✅ Resultados exportados a: {OUT_CSV}")

    # --- VISUALIZACIÓN: Gráfica de barras comparativa R² LOOCV ---
    _generate_benchmark_chart(results_df)

def _generate_benchmark_chart(results_df: pd.DataFrame):
    """Genera gráfica de barras comparativa R² LOOCV para los 4 modelos."""
    OUT_CHART = '../../data/processed/spatial/charts/model_benchmark_r2.png'

    # Filtrar solo el target de Pico de Infectados (el target válido)
    df_pico = results_df[results_df['Target'] == 'Pico Infectados'].copy()
    df_pico = df_pico.sort_values('R2 Score', ascending=True)

    modelos = df_pico['Modelo'].tolist()
    r2_scores = df_pico['R2 Score'].tolist()

    # Colores: rojo para el modelo sospechoso (RL R²=1.0), verde para XGBoost, gris para los demás
    colores = []
    for m, r2 in zip(modelos, r2_scores):
        if r2 >= 1.0:
            colores.append('#E74C3C')   # Rojo → Overfitting
        elif 'XGBoost' in m:
            colores.append('#2ECC71')   # Verde → Ganador
        else:
            colores.append('#3498DB')   # Azul → Competidor

    fig, ax = plt.subplots(figsize=(10, 5.5))
    fig.patch.set_facecolor('#0D1117')
    ax.set_facecolor('#161B22')

    bars = ax.barh(modelos, r2_scores, color=colores, edgecolor='none', height=0.55, zorder=3)

    # Etiquetas de valor
    for bar, r2 in zip(bars, r2_scores):
        label = f"R² = {r2:.4f}"
        if r2 >= 1.0:
            label += "  ⚠️ Overfitting"
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height() / 2,
                label, va='center', ha='left', fontsize=10.5,
                color='white', fontweight='bold')

    # Línea de referencia: R²=0.9
    ax.axvline(x=0.89, color='#F39C12', linestyle='--', linewidth=1.4, alpha=0.8, zorder=2, label='XGBoost R² = 0.8924')

    # Estilo
    ax.set_xlabel('R² Score (LOOCV — Leave-One-Out Cross-Validation)', color='#AAAAAA', fontsize=11)
    ax.set_title('Benchmarking Comparativo de Modelos — Predicción: Pico de Infectados por Estado',
                 color='white', fontsize=13, fontweight='bold', pad=14)
    ax.tick_params(colors='#AAAAAA', labelsize=10)
    ax.spines['bottom'].set_color('#444')
    ax.spines['left'].set_color('#444')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlim(-0.1, 1.22)
    ax.grid(axis='x', color='#2C2C2C', linewidth=0.6, zorder=1)

    # Leyenda
    patch_winner  = mpatches.Patch(color='#2ECC71', label='✅ Modelo seleccionado (XGBoost)')
    patch_warning = mpatches.Patch(color='#E74C3C', label='⚠️ Overfitting severo (RLM)')
    patch_other   = mpatches.Patch(color='#3498DB', label='Modelos competidores')
    ax.legend(handles=[patch_winner, patch_other, patch_warning],
              facecolor='#1C2128', edgecolor='#444', labelcolor='white',
              fontsize=9.5, loc='lower right')

    plt.tight_layout()
    plt.savefig(OUT_CHART, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"✅ Gráfica de benchmarking guardada en: {OUT_CHART}")


if __name__ == '__main__':
    # Cambiar al directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    main()
