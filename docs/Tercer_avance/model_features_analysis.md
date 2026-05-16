# Análisis Profundo de Variables: Modelo SIR Espacial y XGBoost

Este documento detalla la arquitectura de features y decisiones de diseño detrás del modelado epidemiológico de FMD en México.

---

## Parte 1: El Modelo SIR Espacial (La Simulación Física)

A diferencia del primer modelo SIR ingenuo (que asumía que México era un solo campo gigante donde todas las vacas convivían), este nuevo modelo introduce una **Red Gravitatoria**. 

### Las Variables Base del SIR Espacial
El modelo se alimenta de la red generada en la Fase 2, la cual usa dos variables fundamentales bajo la fórmula de Gravedad Newtoniana ($F = M_1 * M_2 / D^2$):

1. **Masa ($M_i, M_j$): Inventario Bovino (SADER/SIAP)**
   * Representa la "atracción gravitatoria" de un estado. Estados con millones de vacas (Veracruz, Jalisco) son nodos masivos que "atraen" y "exportan" patógenos con mayor fuerza.
2. **Distancia ($D_{ij}$): Red Carretera (API OSRM)**
   * No usamos distancia en línea recta (Euclidiana), porque los camiones ganaderos no vuelan. Usamos la API de OSRM para trazar las rutas asfálticas reales. La cordillera de la Sierra Madre agrega "fricción" realista al comercio y a la propagación del virus.

### El Dilema de la Granularidad: ¿Centroides Estatales o Ubicación Exacta de Ranchos?
Hiciste una observación brillante: *"¿No sería más preciso usar la ubicación exacta del hato en lugar del centroide del estado?"*

**Tienes 100% de razón teórica.** Si tuviéramos las coordenadas (lat/lon) de cada rancho ganadero en México y simuláramos cómo interactúa el rancho A con el rancho B, tendríamos un modelo mucho más preciso llamado **Agent-Based Model (ABM)**. 

Sin embargo, tomamos la decisión arquitectónica de usar **Centroides Estatales** por tres razones:
1. **Privacidad y Disponibilidad de Datos:** El gobierno mexicano (SIAP/INEGI) publica datos agregados a nivel municipio o estado. Publicar la ubicación exacta de ranchos privados es riesgoso y raro.
2. **Carga Computacional:** Simular 32 nodos estatales con 992 aristas de carretera toma segundos. Simular 500,000 ranchos individuales requeriría una supercomputadora para calcular 250,000,000,000 de interacciones gravitatorias cada día.
3. **Heurística de Flujo Comercial:** A nivel macroeconómico, el ganado se concentra en rastros y centros de distribución cerca de las capitales. El "centroide" o la "capital" estatal funciona como un proxy estadísticamente válido para el Hub de exportación de ese estado.

---

## Parte 2: El Modelo XGBoost (La Predicción de Riesgo)

Si el SIR simula la "física", el XGBoost actúa como un tasador de riesgo. Le extrajimos al grafo 13 variables topológicas y le pedimos al modelo de Machine Learning que aprendiera a predecir qué estado sufriría la peor devastación.

### Análisis de las 13 Features del Grafo (Node Embeddings)

El XGBoost no ve "carreteras" ni "vacas"; ve números. Diseñamos estas features para representar la posición de cada estado en la red:

#### A. Features de "Masa" (Biológicas)
* **`inventario_bovino`:** La cantidad de ganado del estado. Es la "gasolina" para el fuego.

#### B. Features Gravitatorias (Comerciales)
* **`weighted_in_flux` / `weighted_out_flux`:** La suma total de atracción gravitatoria comercial que un estado recibe y emite. Un alto *out_flux* significa que este estado "exporta" mucho riesgo a otros.
* **`max_in_prob` / `max_out_prob`:** La conexión singular más peligrosa que tiene el estado. Ejemplo: la ruta individual de más alto riesgo de Tlaxcala.

#### C. Features de Distancia Pura
* **`avg_dist_carretera`:** Promedio en km para llegar a todos los demás estados. Penaliza a la península de Baja California.
* **`min_dist_carretera`:** Qué tan cerca está su vecino geográfico más próximo.

#### D. Features Topológicas Puras (Teoría de Grafos / Centralidad)
* **`degree_centrality`:** ¿Con cuántos estados interactúa de manera directa y fuerte?
* **`betweenness_centrality`:** (Centralidad de Intermediación). Si todo el ganado de México viajara por las rutas más cortas, ¿qué estado actuaría como "puente" obligatorio por el que pasan todos los camiones? (El Estado de México suele puntuar alto aquí).
* **`closeness_centrality`:** (Centralidad de Cercanía). ¿Qué estado tiene la distancia total más corta hacia TODOS los demás estados del país?
* **`pagerank`:** El algoritmo clásico de Google aplicado a FMD. No solo importa cuántos vecinos tienes, sino *qué tan importantes* son tus vecinos. Si estás conectado a Veracruz (nodo enorme), tu PageRank sube masivamente.

### Interpretación de los Resultados del XGBoost
El Feature Importance arrojó una gran revelación. La feature que más predice el nivel de devastación (Pico de Infectados) es el **`inventario_bovino`**, seguida inmediatamente por el **`weighted_out_flux`**.

**Conclusión Epistémica:**
Para que un estado cause o sufra una catástrofe epidémica, no basta con tener muchas vacas. Chiapas tiene más vacas que Michoacán, pero está arrinconado en el sur. **El peligro real reside en estados que combinan alto inventario con alta centralidad de flujo saliente.** 

Este es el tipo de "Insight accionable" que justifica usar Machine Learning sobre ecuaciones diferenciales: XGBoost nos dice exactamente dónde invertir el presupuesto de seguridad nacional (por ejemplo, blindar las carreteras de salida de los estados con alto *weighted_out_flux*).
