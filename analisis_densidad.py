cortes = [0, 50, 75, 100] # 4 números, asegúrate de abarcar tu máximo
nombres_grupos = ['Baja Densidad', 'Media Densidad', 'Alta Densidad']

# Izquierda: Nombre de columna NUEVO | Derecha: Seleccionamos la columna ORIGINAL
df['Categoria_densidad'] = pd.cut(df['Densidad_Ganado'], bins=cortes, labels=nombres_grupos)

# Tu groupby original, pero agrupando por tu columna NUEVA
promedio_den = df.groupby('Categoria_densidad')['hectareas'].mean()