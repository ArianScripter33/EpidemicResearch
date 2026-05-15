"""
04c_custom_stacked_race.py
--------------------------
Genera un "Bar Chart Race" personalizado utilizando Matplotlib FuncAnimation.
A diferencia de la librería bar_chart_race, este script permite barras APILADAS,
mostrando simultáneamente los Infectados Activos (rojo) y los Sacrificados (negro)
por estado a lo largo del tiempo.
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

INPUT_CSV = '../../data/processed/spatial/sir_full_state_history_180d.csv'
OUT_DIR = '../../data/processed/spatial/charts/'
OUT_GIF = os.path.join(OUT_DIR, 'stacked_race_fmd.gif')
OUT_MP4 = os.path.join(OUT_DIR, 'stacked_race_fmd.mp4')

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print("Cargando datos S-I-R...")
    df = pd.read_csv(INPUT_CSV)
    
    # Pre-calcular Total Afectados para ordenar el ranking
    df['Afectados'] = df['I'] + df['R']
    
    # Configurar la figura
    fig, ax = plt.subplots(figsize=(14, 8))
    plt.subplots_adjust(left=0.15, right=0.9, top=0.85, bottom=0.1)
    
    dias = sorted(df['dia'].unique())
    max_x = df['Afectados'].max() * 1.05
    
    def format_millions(x, pos):
        return f'{x/1e6:.1f}M'
    
    def update(frame):
        ax.clear()
        
        dia = dias[frame]
        df_dia = df[df['dia'] == dia].copy()
        
        # Mantener solo el Top 12 de afectados ese día
        df_dia = df_dia.sort_values('Afectados', ascending=True).tail(12)
        
        estados = df_dia['estado'].values
        R_vals = df_dia['R'].values
        I_vals = df_dia['I'].values
        Afectados_vals = df_dia['Afectados'].values
        
        y_pos = range(len(estados))
        
        # Dibujar barra de Sacrificados (Base)
        ax.barh(y_pos, R_vals, color='#2c2c2c', label='Removidos (Sacrificados)')
        
        # Dibujar barra de Infectados (Apilada sobre la base)
        ax.barh(y_pos, I_vals, left=R_vals, color='#e63946', label='Infectados Activos')
        
        # Anotaciones de valor
        for i, (af, iv) in enumerate(zip(Afectados_vals, I_vals)):
            if af > 10000:
                ax.text(af + (max_x * 0.01), i, f'{af/1e6:.2f}M', 
                        va='center', fontsize=11, fontweight='bold', color='black')
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(estados, fontsize=12, fontweight='bold')
        ax.set_xlim(0, max_x)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(format_millions))
        
        # Títulos Dinámicos
        total_sacrificados = df_dia['R'].sum()
        total_infectados = df_dia['I'].sum()
        
        ax.set_title('Colapso del Hato Nacional — Propagación FMD (SIR)', 
                     fontsize=18, fontweight='bold', pad=30)
        
        # Caja de texto informativa superior
        info_text = (f" Día: {dia:03d} / 180  |  "
                     f"Infectados Activos Nacional: {total_infectados/1e6:.2f}M  |  "
                     f"Sacrificados Nacional: {total_sacrificados/1e6:.2f}M")
        
        ax.text(0.5, 1.05, info_text, transform=ax.transAxes, ha='center', 
                fontsize=14, fontweight='bold',
                bbox=dict(facecolor='#f1faee', edgecolor='black', boxstyle='round,pad=0.5'))
        
        ax.grid(axis='x', linestyle='--', alpha=0.4)
        ax.legend(loc='lower right', fontsize=12)

    print("Generando fotogramas y compilando animación (Esto tomará ~20 segundos)...")
    anim = animation.FuncAnimation(fig, update, frames=len(dias), interval=100)
    
    # Intentar guardar como MP4 (requiere ffmpeg)
    try:
        anim.save(OUT_MP4, fps=10, extra_args=['-vcodec', 'libx264'])
        print(f"✅ Animación MP4 generada exitosamente: {OUT_MP4}")
    except Exception as e:
        print(f"⚠️ No se pudo guardar MP4 (quizás no hay ffmpeg). Error: {e}")
    
    # Guardar siempre como GIF
    print("Compilando GIF de respaldo...")
    anim.save(OUT_GIF, writer='pillow', fps=10)
    print(f"✅ Animación GIF generada exitosamente: {OUT_GIF}")

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    main()
