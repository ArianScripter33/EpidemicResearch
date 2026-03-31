Esto es exactamente la pregunta que necesitas hacerte **antes** de codear cualquiera de estos módulos. Si no entiendes qué hace la herramienta, vas a generar gráficos bonitos que no puedes defender ante el jurado. Vamos uno por uno, con datos concretos de tu proyecto:

---

### 1. 🎭 Caras de Chernoff

**¿Qué es?** Una técnica de visualización inventada por Herman Chernoff (1973) que mapea variables numéricas a **rasgos faciales**. Explota un hack cognitivo: los humanos somos expertos en distinguir caras. Podemos detectar diferencias sutiles entre 32 caras más rápido que entre 32 filas de una tabla.

**¿Cómo funciona?** Cada variable controla un rasgo:

| Rasgo Facial | Variable de tu proyecto | Ejemplo |
|---|---|---|
| Ancho de cara | Densidad ganadera (cabezas/km²) | Cara ancha = estado con mucho ganado |
| Altura de ojos | Prevalencia TB bovina (%) | Ojos altos = mucha TB |
| Curvatura de boca | Clausuras por clembuterol (#) | Boca triste = muchas clausuras |
| Tamaño de nariz | Resistencia antimicrobiana (%) | Nariz grande = alta resistencia |
| Inclinación de cejas | Casos CIE-10 A05 per cápita | Cejas fruncidas = muchas intoxicaciones |

**¿Con qué datos?** Una tabla de 32 filas (estados) × 5-7 columnas (variables del warehouse). Cada estado = una cara.

**Interpretación potencial:** *"Las caras de Chihuahua, Durango y Jalisco se ven casi idénticas: cara ancha, ojos altos, boca triste. Esto revela visualmente que comparten el mismo perfil de riesgo: alta densidad ganadera + alta TB + muchas clausuras. En contraste, la cara de la CDMX es completamente diferente — cara delgada, ojos bajos — porque es consumidora, no productora."*

**¿Para qué materia?** Estadística Multivariada (requisito explícito del PP).

---

### 2. 〰️ Curvas de Andrews

**¿Qué es?** Otra técnica de visualización multivariada. Transforma cada observación (estado) en una **función de Fourier** que puedes graficar como una curva continua.

**¿Cómo funciona?** Cada estado se convierte en una curva:
```
f(t) = x1/√2 + x2·sin(t) + x3·cos(t) + x4·sin(2t) + x5·cos(2t) + ...
```
Donde x1, x2, x3... son las variables normalizadas de ese estado.

**¿Para qué sirve?** Para detectar **clusters** (grupos) visualmente. Si dos curvas se parecen, esos estados tienen perfiles similares. Si una curva se separa del grupo, es un **outlier**.

**¿Con qué datos?** La misma matriz de 32 estados × 5-7 variables.

**Interpretación potencial:** *"Las curvas de Andrews revelan 3 clusters naturales: (1) estados ganaderos del norte (Chihuahua, Sonora, Durango) con curvas de alta amplitud, (2) estados del sureste con producción extensiva (Veracruz, Chiapas) con oscilaciones medias, y (3) estados urbanos/consumidores (CDMX, Querétaro) con curvas planas. Un outlier podría ser Tabasco — baja densidad pero alta resistencia RAM."*

**¿Para qué materia?** Estadística Multivariada.

---

### 3. 📊 PCA (Principal Component Analysis) + Scree Plot + Biplot

**¿Qué es?** Un método matemático para **reducir dimensionalidad**. Si tienes 7 variables, PCA las comprime en 2-3 "super-variables" (componentes principales) que capturan la mayor parte de la información.

**¿Por qué lo necesitas?** Porque si intentas graficar 7 variables simultáneamente, es imposible. PCA te dice: *"Oye, el 78% de toda la variación en tus datos se explica con solo 2 ejes."*

**Los 3 outputs del PCA:**

| Output | ¿Qué muestra? | ¿Cómo se lee? |
|---|---|---|
| **Scree Plot** | Un gráfico de barras que muestra cuánta varianza explica cada componente | Si las primeras 2-3 barras son altas y el resto son planas, PCA funciona bien. El "codo" te dice cuántos componentes usar |
| **Biplot** | Un scatter plot 2D donde cada punto es un estado y las flechas son las variables originales | Estados cercanos son similares. Flechas que apuntan igual están correlacionadas. Flechas opuestas están inversamente correlacionadas |
| **Loadings** | Tabla numérica de cuánto contribuye cada variable a cada componente | Si PC1 tiene loadings altos en "densidad ganadera" y "clausuras", entonces PC1 = "presión ganadera" |

**¿Con qué datos?** La matriz 32 estados × 7 variables (densidad, prevalencia TB, resistencia RAM, clausuras clembuterol, casos A05, producción cárnica, infraestructura sanitaria).

**Interpretación potencial:** *"PC1 (45% de la varianza) está dominado por densidad ganadera y producción cárnica → lo llamamos 'presión productiva'. PC2 (23%) está dominado por resistencia antimicrobiana y clausuras → lo llamamos 'falla regulatoria'. El biplot muestra que Jalisco y Veracruz tienen alta presión productiva Y alta falla regulatoria simultáneamente — son los estados de mayor riesgo sistémico."*

**¿Para qué materia?** Estadística Multivariada.

---

### 4. 📈 ANOVA / MANOVA

**¿Qué es?** Un test estadístico para responder: **¿Hay diferencia SIGNIFICATIVA entre grupos, o es solo ruido?**

- **ANOVA** (Analysis of Variance): Compara las medias de una variable entre varios grupos.
- **MANOVA** (Multivariate ANOVA): Lo mismo, pero con varias variables a la vez.

**Tu caso concreto:** El V2.md reporta prevalencia de Salmonella en 4 canales de venta:

| Canal | Prevalencia |
|---|---|
| Supermercados | 1.3% |
| Carnicerías | 8.4% |
| Tianguis | 13.6% |
| Mercados Municipales | 22.3% |

La pregunta es: **¿Estas diferencias son reales o podrían ser casualidad?** ANOVA responde con un **p-value**.

**Interpretación potencial:** *"ANOVA arroja F = 14.3, p < 0.001. Rechazamos la hipótesis nula: la prevalencia de Salmonella NO es igual entre canales. El test post-hoc de Tukey confirma que la diferencia es significativa entre Supermercados y Mercados Municipales (p < 0.001), pero NO entre Carnicerías y Tianguis (p = 0.12). Esto implica que la intervención regulatoria debe focalizarse en los mercados municipales, no repartirse por igual."*

**¿Para qué materia?** Estadística Multivariada.

---

### 5. 📉 Regresión Lineal Múltiple

**¿Qué es?** Un modelo que dice: *"¿Cuánto influye cada variable independiente (X) en la variable dependiente (y)?"* y le asigna un **coeficiente numérico** a cada una.

```
Casos_A05 = β0 + β1·densidad_ganadera + β2·prevalencia_Salmonella + β3·clausuras + ε
```

**Diferencia con XGBoost:** La regresión te da **interpretabilidad** (puedes decir "por cada clausura adicional, los casos A05 suben en 2.3"). XGBoost te da **poder predictivo** pero es una caja negra (sin SHAP).

**¿Con qué datos?** Tabla 32 estados × año, con columnas: casos_A05, densidad_ganadera, prevalencia_Salmonella_canal, num_clausuras, porcentaje_resistencia_ampicilina.

**Interpretación potencial:** *"R² = 0.72 (el modelo explica el 72% de la variación en casos A05). El coeficiente de clausuras por clembuterol es β3 = 2.3 (p < 0.05), lo que significa que por cada clausura adicional en un estado, se esperan ~2.3 casos más de intoxicación alimentaria. La prevalencia de Salmonella en mercados tiene el coeficiente más alto (β2 = 8.1), confirmando que el canal de venta informal es el driver principal."*

**¿Para qué materia?** Estadística Multivariada + IA (complementa al XGBoost).

---

### 6. 🗺️ Mapas Coropléticos (Choropleth)

**¿Qué es?** Un mapa donde cada estado está **coloreado según una variable numérica**. Rojo = alto riesgo, verde = bajo riesgo. Es la versión geográfica de un heatmap.

**¿Con qué datos?** Necesitas dos cosas:
1. Un GeoJSON de los estados de México (polígonos geográficos) — disponibles públicamente.
2. Tu tabla de datos por estado (prevalencia TB, clausuras, riesgo predicho, etc.)

**Mapas que generaríamos:**

| Mapa | Variable | Colores |
|---|---|---|
| Mapa 1 | Prevalencia TB bovina por estado | Blanco → Rojo oscuro |
| Mapa 2 | Clausuras por clembuterol per cápita | Verde → Rojo |
| Mapa 3 | Riesgo A05 predicho por XGBoost (%) | Azul → Naranja → Rojo |
| Mapa 4 | Densidad ganadera (cabezas/km²) | Amarillo → Marrón |

**Interpretación potencial:** *"El mapa coroplético revela un 'cinturón de riesgo' que va de Jalisco a Veracruz pasando por Michoacán y Puebla — estados con alta densidad ganadera y baja cobertura de inspección COFEPRIS. Este patrón es invisible en una tabla pero inmediatamente obvio en el mapa."*

**¿Para qué materia?** IA (visualización de predicciones) + Innovación Social (hacer visibles las desigualdades geográficas).

---

### 7. 📐 SIR Phase Diagrams (Diagramas de Fase)

**¿Qué es?** Dos tipos de gráficas que salen del modelo SIR de Ecuaciones Diferenciales:

**Tipo A — Evolución Temporal:** Ejes X=tiempo (días), Y=número de animales. 3 curvas: S(t) baja, I(t) sube y luego baja, R(t) sube. Es la gráfica clásica de "aplanar la curva" que todos vimos durante COVID.

**Tipo B — Diagrama de Fase:** Ejes X=Susceptibles, Y=Infectados. Muestra la TRAYECTORIA del sistema — cómo se mueve el estado del rebaño en el tiempo. Es un "retrato" del comportamiento dinámico.

**¿Con qué datos?**
- **Modo TB:** S_0 = 35.1M, I_0 = datos de cuarentenas SENASICA, R0 = 1.8
- **Modo FMD:** S_0 = 35.1M, I_0 = 1 (un solo caso importado), R0 = 6.0

**La gráfica killer:** Poner **ambos modelos lado a lado**. TB a la izquierda (curva lenta, meseta suave en 5 años), FMD a la derecha (pico explosivo en 45 días). El contraste visual es devastador para la presentación.

**Interpretación potencial:** *"El diagrama de fase muestra que con R0 = 1.8 (TB), el sistema converge a un equilibrio endémico estable — hay infectados, pero son manejables. Con R0 = 6.0 (FMD), el sistema NO tiene equilibrio estable — la trayectoria va directamente al colapso. La única forma de evitarlo es reducir R0 por debajo de 1 mediante cuarentena+sacrificio masivo en las primeras 72 horas."*

**¿Para qué materia?** Ecuaciones Diferenciales Aplicadas.

---

### 8. 📊 Dashboard (Streamlit/Plotly)

**¿Qué es?** Una **aplicación web interactiva** que integra todas las visualizaciones anteriores en una sola pantalla. El usuario selecciona un estado, y el dashboard actualiza: el mapa, las curvas SIR, las métricas financieras y las predicciones XGBoost.

**Componentes:**
- Panel izquierdo: Mapa coroplético de México (click en estado para seleccionar)
- Panel central: Curvas SIR del estado seleccionado + métricas clave
- Panel derecho: Tabla financiera (VPN, ROI) + score de riesgo XGBoost
- Slider: R0 ajustable para simular escenarios en vivo

**¿Para qué materia?** Es el **prototipo** que pide el PP (*"al menos un prototipo: organizacional, visual, algorítmico"*). Es tu demo en vivo para el coloquio.

---

### 🧠 Resumen Visual (Cheat Sheet)

| Técnica | Pregunta que responde | Input | Output |
|---|---|---|---|
| **Chernoff** | ¿Qué estados se "parecen"? | Matriz estados × variables | 32 caritas |
| **Andrews** | ¿Hay clusters naturales? | Misma matriz | Curvas superpuestas |
| **PCA** | ¿Cuáles son los "super-factores"? | Misma matriz | 2-3 componentes |
| **Scree** | ¿Cuántos factores importan? | Eigenvalues del PCA | Gráfico de barras |
| **Biplot** | ¿Quién está cerca de quién y por qué? | PCA scores + loadings | Scatter + flechas |
| **ANOVA** | ¿Las diferencias son reales? | Grupos + variable | p-value |
| **Regresión** | ¿Cuánto influye cada variable? | X + y | Coeficientes + R² |
| **Choropleth** | ¿Dónde está el riesgo? | GeoJSON + datos | Mapa coloreado |
| **SIR Plots** | ¿Qué tan rápido se propaga? | S_0, I_0, β, γ | Curvas temporales |
| **Dashboard** | ¿Todo junto, interactivo? | Todo lo anterior | Web app |

¿Quedó claro? ¿Hay alguna técnica que quieras que profundicemos antes de pasar a la Fase 1? 🎯