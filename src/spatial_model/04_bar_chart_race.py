import pandas as pd
import bar_chart_race as bcr
import os

INPUT_CSV = '../../data/processed/spatial/sir_state_history.csv'
OUT_HTML = '../../data/processed/spatial/bar_chart_race.html'

def main():
    print("=== Generando Animación Bar Chart Race ===")
    
    # Cargar historial
    df = pd.read_csv(INPUT_CSV)
    
    # Bar Chart Race requiere que el índice sea el tiempo y las columnas las categorías
    df = df.set_index('dia')
    
    # Quedarnos solo con los estados que tuvieron al menos 1 infectado para limpiar el gráfico
    max_infectados = df.max()
    estados_afectados = max_infectados[max_infectados > 0].index
    df = df[estados_afectados]
    
    print(f"Creando animación para {len(estados_afectados)} estados afectados...")
    
    # Generar el HTML (no requiere ffmpeg como el mp4)
    html_str = bcr.bar_chart_race(
        df=df,
        filename=None, # Si es None, devuelve HTML (o podemos exportar a .mp4 si tenemos ffmpeg)
        orientation='h',
        sort='desc',
        n_bars=10, # Top 10 estados
        fixed_order=False,
        fixed_max=True,
        steps_per_period=10,
        interpolate_period=False,
        label_bars=True,
        bar_size=.95,
        period_label={'x': .99, 'y': .25, 'ha': 'right', 'va': 'center', 'size': 18},
        period_fmt='Día {x:.0f}',
        period_summary_func=lambda v, r: {'x': .99, 'y': .18, 's': f'Total Infecciones: {v.nlargest(32).sum():,.0f}', 'ha': 'right', 'size': 11},
        title='Evolución de Casos FMD por Estado',
        title_size=16,
        bar_label_size=10,
        tick_label_size=10,
        shared_fontdict=None,
        scale='linear',
        writer=None,
        fig=None,
        dpi=144,
        bar_kwargs={'alpha': .8},
        filter_column_colors=False
    )
    
    # Guardar a disco
    with open(OUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_str)
        
    print(f"✅ Bar Chart Race HTML guardado en: {OUT_HTML}")
    print("Abre este archivo en tu navegador para ver la animación interactiva.")

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    main()
