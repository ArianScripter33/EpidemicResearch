"""
04b_stacked_sir_charts.py
--------------------------
Genera gráficas apiladas S-I-R por estado y a nivel nacional.
Visualizaciones:
  1. Gráfica apilada nacional (S + I + R = N total)
  2. Gráficas individuales de los top 8 estados más afectados
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

INPUT_CSV = '../../data/processed/spatial/sir_full_state_history_180d.csv'
OUT_DIR = '../../data/processed/spatial/charts/'

def format_millions(x, pos):
    return f'{x/1e6:.1f}M'

def plot_national(df):
    """Gráfica apilada nacional: todo México S-I-R"""
    nacional = df.groupby('dia')[['S','I','R']].sum()
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    ax.stackplot(
        nacional.index,
        nacional['R'], nacional['I'], nacional['S'],
        labels=['Removidos (Sacrificados)', 'Infectados Activos', 'Susceptibles'],
        colors=['#2c2c2c', '#e63946', '#a8dadc'],
        alpha=0.85
    )
    
    ax.set_title('Modelo SIR Espacial — Hato Nacional de México (34.5M cabezas)',
                 fontsize=16, fontweight='bold', pad=15)
    ax.set_xlabel('Día de Simulación', fontsize=12)
    ax.set_ylabel('Cabezas de Ganado', fontsize=12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_millions))
    ax.legend(loc='center right', fontsize=11, framealpha=0.9)
    ax.set_xlim(0, 179)
    
    # Marcar el pico de infección
    pico_dia = nacional['I'].idxmax()
    pico_val = nacional['I'].max()
    ax.axvline(x=pico_dia, color='yellow', linestyle='--', linewidth=1.5, alpha=0.8)
    ax.annotate(f'Pico: Día {pico_dia}\n{pico_val/1e6:.1f}M infectados',
                xy=(pico_dia, nacional['R'].iloc[pico_dia] + pico_val),
                xytext=(pico_dia + 15, pico_val + nacional['R'].iloc[pico_dia] + 2e6),
                fontsize=10, fontweight='bold', color='yellow',
                arrowprops=dict(arrowstyle='->', color='yellow', lw=1.5),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7))
    
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'sir_nacional_apilado.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Gráfica nacional apilada guardada")

def plot_top_states(df, top_n=8):
    """Gráficas individuales de los top N estados más devastados"""
    # Determinar los estados con más R (sacrificados) al final
    dia_final = df[df['dia'] == df['dia'].max()]
    top_estados = dia_final.nlargest(top_n, 'R')['estado'].tolist()
    
    fig, axes = plt.subplots(2, 4, figsize=(20, 10), sharex=True)
    axes = axes.flatten()
    
    for idx, estado in enumerate(top_estados):
        ax = axes[idx]
        estado_df = df[df['estado'] == estado].set_index('dia')
        
        ax.stackplot(
            estado_df.index,
            estado_df['R'], estado_df['I'], estado_df['S'],
            colors=['#2c2c2c', '#e63946', '#a8dadc'],
            alpha=0.85
        )
        
        # Título con el total de sacrificados
        total_R = estado_df['R'].iloc[-1]
        total_N = estado_df['S'].iloc[0] + estado_df['I'].iloc[0] + estado_df['R'].iloc[0]
        pct_lost = (total_R / total_N * 100) if total_N > 0 else 0
        
        ax.set_title(f'{estado}\n{total_R/1e6:.2f}M sacrificados ({pct_lost:.0f}%)',
                     fontsize=10, fontweight='bold')
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_millions))
        ax.set_xlim(0, 179)
        ax.grid(axis='y', alpha=0.2)
        
        if idx >= 4:
            ax.set_xlabel('Día', fontsize=9)
    
    fig.suptitle('Dinámica SIR por Estado — Top 8 Más Devastados',
                 fontsize=16, fontweight='bold', y=1.02)
    
    # Leyenda compartida
    fig.legend(['Removidos (Sacrificados)', 'Infectados Activos', 'Susceptibles'],
               loc='lower center', ncol=3, fontsize=11, framealpha=0.9,
               bbox_to_anchor=(0.5, -0.02))
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'sir_top8_estados_apilado.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ Gráficas de top {top_n} estados guardadas")

def plot_day_of_infection_table(df):
    """Genera tabla de cuándo fue infectado cada estado y qué porcentaje perdió"""
    # Primer día con I >= 1 para cada estado
    infectados = df[df['I'] >= 1].groupby('estado')['dia'].min().reset_index()
    infectados.columns = ['estado', 'dia_primera_infeccion']
    
    # Pérdida total al día 179
    dia_final = df[df['dia'] == df['dia'].max()][['estado', 'R', 'N']]
    dia_final['pct_sacrificado'] = (dia_final['R'] / dia_final['N'] * 100).round(1)
    
    tabla = infectados.merge(dia_final[['estado', 'R', 'N', 'pct_sacrificado']], on='estado')
    tabla = tabla.sort_values('dia_primera_infeccion')
    tabla.columns = ['Estado', 'Día Infección', 'Sacrificados', 'Inventario', '% Perdido']
    
    tabla.to_csv(os.path.join(OUT_DIR, 'tabla_cronologia_infeccion.csv'), index=False)
    print("✅ Tabla cronológica de infección guardada")
    print(tabla.to_string(index=False))

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print("=== Generando Visualizaciones Apiladas S-I-R ===\n")
    
    df = pd.read_csv(INPUT_CSV)
    
    plot_national(df)
    plot_top_states(df)
    plot_day_of_infection_table(df)

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    main()
