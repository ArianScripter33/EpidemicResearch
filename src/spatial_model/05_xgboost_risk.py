"""
05_xgboost_risk.py
------------------
Entrena un XGBoost Regressor para predecir el "Índice de Riesgo Sistémico"
de cada estado, usando features derivados del modelo gravitatorio y la 
topología de la red.

Features por estado:
  - inventario_bovino_2023 (Masa)
  - degree_centrality (¿Cuántas conexiones fuertes tiene?)
  - betweenness_centrality (¿Qué tan "puente" es en la red?)
  - closeness_centrality (¿Qué tan cerca está de todos los demás?)
  - weighted_in_flux (Suma de flujos gravitatorios entrantes)
  - weighted_out_flux (Suma de flujos gravitatorios salientes)
  - avg_dist_carretera (Distancia promedio por carretera a los demás)
  - min_dist_carretera (Distancia mínima al vecino más cercano)

Target:
  - dia_primera_infeccion (Inversa del riesgo: más temprano = más riesgo)
  - pct_sacrificado_dia_60 (% del hato perdido al día 60)
"""
import pandas as pd
import numpy as np
import networkx as nx
import xgboost as xgb
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import os

# Rutas
NODOS_CSV = '../../data/processed/spatial/nodos_estados.csv'
MATRIX_CSV = '../../data/processed/spatial/matriz_gravedad.csv'
DISTANCES_CSV = '../../data/processed/spatial/distancias_carretera.csv'
SIR_FULL = '../../data/processed/spatial/sir_full_state_history_180d.csv'
OUT_DIR = '../../data/processed/spatial/charts/'
OUT_FEATURES = '../../data/processed/spatial/xgboost_features.csv'
OUT_COMPARISON = '../../data/processed/spatial/sir_vs_xgboost_comparison.csv'

def build_graph_features(nodos_df, matrix_df, dist_df):
    """Construye features de grafo para cada estado."""
    print("  Construyendo grafo de NetworkX...")
    
    # Crear grafo dirigido ponderado
    G = nx.DiGraph()
    for _, row in nodos_df.iterrows():
        G.add_node(row['estado'], inventario=row['inventario_bovino_2023'])
    
    for _, row in matrix_df.iterrows():
        G.add_edge(row['origen'], row['destino'], 
                   weight=row['probabilidad_contagio_base'],
                   flujo=row['flujo_gravedad'])
    
    # Calcular métricas de centralidad
    degree_c = nx.degree_centrality(G)
    betweenness_c = nx.betweenness_centrality(G, weight='weight')
    closeness_c = nx.closeness_centrality(G, distance=None)  # Usando peso
    pagerank = nx.pagerank(G, weight='weight')
    
    # Features por estado
    features = []
    for _, node_row in nodos_df.iterrows():
        estado = node_row['estado']
        
        # Flujos gravitatorios
        in_edges = matrix_df[matrix_df['destino'] == estado]
        out_edges = matrix_df[matrix_df['origen'] == estado]
        
        # Distancias por carretera
        dists = dist_df[dist_df['origen'] == estado]['distancia_carretera_km']
        
        features.append({
            'estado': estado,
            'inventario_bovino': node_row['inventario_bovino_2023'],
            'lon': node_row['lon'],
            'lat': node_row['lat'],
            # Centralidades de grafo
            'degree_centrality': degree_c.get(estado, 0),
            'betweenness_centrality': betweenness_c.get(estado, 0),
            'closeness_centrality': closeness_c.get(estado, 0),
            'pagerank': pagerank.get(estado, 0),
            # Flujos
            'weighted_in_flux': in_edges['flujo_gravedad'].sum(),
            'weighted_out_flux': out_edges['flujo_gravedad'].sum(),
            'max_in_prob': in_edges['probabilidad_contagio_base'].max() if len(in_edges) > 0 else 0,
            'max_out_prob': out_edges['probabilidad_contagio_base'].max() if len(out_edges) > 0 else 0,
            # Distancias
            'avg_dist_carretera': dists.mean() if len(dists) > 0 else 0,
            'min_dist_carretera': dists.min() if len(dists) > 0 else 0,
        })
    
    return pd.DataFrame(features)

def build_targets(sir_df):
    """Extrae targets del modelo SIR para cada estado."""
    targets = []
    
    for estado in sir_df['estado'].unique():
        estado_df = sir_df[sir_df['estado'] == estado].sort_values('dia')
        
        # Día de primera infección
        infectado = estado_df[estado_df['I'] >= 1]
        dia_infeccion = infectado['dia'].min() if len(infectado) > 0 else 999
        
        # % sacrificado al día 60
        dia60 = estado_df[estado_df['dia'] == 60]
        if len(dia60) > 0:
            N = dia60.iloc[0]['N']
            R60 = dia60.iloc[0]['R']
            pct_r60 = (R60 / N * 100) if N > 0 else 0
        else:
            pct_r60 = 0
        
        # Pico de infección
        pico_I = estado_df['I'].max()
        dia_pico = estado_df.loc[estado_df['I'].idxmax(), 'dia']
        
        targets.append({
            'estado': estado,
            'dia_primera_infeccion': dia_infeccion,
            'pct_sacrificado_dia_60': round(pct_r60, 2),
            'pico_infectados': int(pico_I),
            'dia_pico': int(dia_pico),
        })
    
    return pd.DataFrame(targets)

def train_xgboost(features_df, target_col, feature_cols):
    """Entrena XGBoost con Leave-One-Out (32 estados = 32 folds)."""
    X = features_df[feature_cols].values
    y = features_df[target_col].values
    
    loo = LeaveOneOut()
    predictions = np.zeros(len(y))
    
    for train_idx, test_idx in loo.split(X):
        model = xgb.XGBRegressor(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            verbosity=0
        )
        model.fit(X[train_idx], y[train_idx])
        predictions[test_idx] = model.predict(X[test_idx])
    
    # Entrenar modelo final para feature importance
    final_model = xgb.XGBRegressor(
        n_estimators=100, max_depth=4, learning_rate=0.1,
        subsample=0.8, colsample_bytree=0.8, random_state=42, verbosity=0
    )
    final_model.fit(X, y)
    
    mae = mean_absolute_error(y, predictions)
    r2 = r2_score(y, predictions)
    
    return predictions, final_model, mae, r2

def plot_feature_importance(model, feature_cols, target_name):
    """Gráfica de importancia de features."""
    importances = model.feature_importances_
    sorted_idx = np.argsort(importances)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(range(len(sorted_idx)), importances[sorted_idx], color='#e63946', alpha=0.8)
    ax.set_yticks(range(len(sorted_idx)))
    ax.set_yticklabels([feature_cols[i] for i in sorted_idx], fontsize=10)
    ax.set_xlabel('Importancia (Gain)', fontsize=12)
    ax.set_title(f'XGBoost Feature Importance — Target: {target_name}',
                 fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, f'xgboost_importance_{target_name}.png'), dpi=150, bbox_inches='tight')
    plt.close()

def plot_comparison(features_df, target_col, predictions, target_name):
    """SIR real vs XGBoost predicción."""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    y_real = features_df[target_col].values
    estados = features_df['estado'].values
    
    ax.scatter(y_real, predictions, s=80, color='#e63946', alpha=0.7, edgecolors='black', linewidths=0.5)
    
    # Línea perfecta
    lim_min = min(min(y_real), min(predictions)) * 0.9
    lim_max = max(max(y_real), max(predictions)) * 1.1
    ax.plot([lim_min, lim_max], [lim_min, lim_max], 'k--', alpha=0.5, label='Predicción Perfecta')
    
    # Etiquetar los estados outliers (top 5 con mayor error)
    errors = np.abs(y_real - predictions)
    top_outliers = np.argsort(errors)[-5:]
    for idx in top_outliers:
        ax.annotate(estados[idx], (y_real[idx], predictions[idx]),
                    fontsize=8, fontweight='bold',
                    xytext=(5, 5), textcoords='offset points')
    
    r2 = r2_score(y_real, predictions)
    mae = mean_absolute_error(y_real, predictions)
    ax.set_title(f'SIR Simulación vs XGBoost Predicción\n{target_name} | R²={r2:.3f} | MAE={mae:.2f}',
                 fontsize=14, fontweight='bold')
    ax.set_xlabel(f'{target_name} (SIR Simulación)', fontsize=12)
    ax.set_ylabel(f'{target_name} (XGBoost Predicción)', fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, f'sir_vs_xgboost_{target_name}.png'), dpi=150, bbox_inches='tight')
    plt.close()

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print("=== Fase 5: XGBoost Risk Model con Features de Grafo ===\n")
    
    # 1. Cargar datos
    nodos = pd.read_csv(NODOS_CSV)
    matrix = pd.read_csv(MATRIX_CSV)
    dists = pd.read_csv(DISTANCES_CSV)
    sir = pd.read_csv(SIR_FULL)
    
    # 2. Construir features
    print("Paso 1: Construyendo features de grafo...")
    features_df = build_graph_features(nodos, matrix, dists)
    print(f"  {len(features_df)} estados, {len(features_df.columns)-1} features")
    
    # 3. Construir targets
    print("Paso 2: Extrayendo targets del modelo SIR...")
    targets_df = build_targets(sir)
    
    # 4. Merge
    full_df = features_df.merge(targets_df, on='estado')
    full_df.to_csv(OUT_FEATURES, index=False)
    print(f"  Dataset completo guardado: {OUT_FEATURES}")
    
    # 5. Entrenar modelos
    feature_cols = [
        'inventario_bovino', 'degree_centrality', 'betweenness_centrality',
        'closeness_centrality', 'pagerank', 'weighted_in_flux', 'weighted_out_flux',
        'max_in_prob', 'max_out_prob', 'avg_dist_carretera', 'min_dist_carretera',
        'lat', 'lon'
    ]
    
    # Target 1: Día de primera infección
    print("\nPaso 3: Entrenando XGBoost — Target: dia_primera_infeccion")
    # Filtrar estados no infectados
    df_infected = full_df[full_df['dia_primera_infeccion'] < 999].copy()
    
    preds_dia, model_dia, mae_dia, r2_dia = train_xgboost(
        df_infected, 'dia_primera_infeccion', feature_cols
    )
    print(f"  R² = {r2_dia:.3f} | MAE = {mae_dia:.2f} días")
    
    plot_feature_importance(model_dia, feature_cols, 'dia_primera_infeccion')
    plot_comparison(df_infected, 'dia_primera_infeccion', preds_dia, 'dia_primera_infeccion')
    
    # Target 2: Pico de infectados
    print("\nPaso 4: Entrenando XGBoost — Target: pico_infectados")
    preds_pico, model_pico, mae_pico, r2_pico = train_xgboost(
        df_infected, 'pico_infectados', feature_cols
    )
    print(f"  R² = {r2_pico:.3f} | MAE = {mae_pico:,.0f} cabezas")
    
    plot_feature_importance(model_pico, feature_cols, 'pico_infectados')
    plot_comparison(df_infected, 'pico_infectados', preds_pico, 'pico_infectados')
    
    # 6. Tabla comparativa SIR vs XGBoost
    df_infected['xgb_pred_dia'] = preds_dia.round(1)
    df_infected['xgb_pred_pico'] = preds_pico.astype(int)
    
    comparison = df_infected[['estado', 'dia_primera_infeccion', 'xgb_pred_dia',
                              'pico_infectados', 'xgb_pred_pico', 'pct_sacrificado_dia_60']].copy()
    comparison.columns = ['Estado', 'SIR Día Infección', 'XGB Pred Día', 
                          'SIR Pico I', 'XGB Pred Pico', '% Sacrificado Día 60']
    comparison = comparison.sort_values('SIR Día Infección')
    comparison.to_csv(OUT_COMPARISON, index=False)
    
    print(f"\n{'='*80}")
    print("TABLA COMPARATIVA: SIR vs XGBoost")
    print(f"{'='*80}")
    print(comparison.to_string(index=False))
    
    print(f"\n✅ Todos los artefactos guardados en {OUT_DIR}")
    print(f"✅ Features exportados: {OUT_FEATURES}")
    print(f"✅ Comparación: {OUT_COMPARISON}")

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    main()
