**ACTIVIDAD DE INNOVACIÓN SOCIAL**

*Proyecto Prototípico — Ganado Saludable:*
*AftoSec: Vigilancia Epidemiológica de Precisión ante Fiebre Aftosa*

---

| Campo | Detalle |
|-------|---------|
| **Nombre del proyecto** | Ganado Saludable — AftoSec: Sistema Geoespacial de Detección Temprana de Fiebre Aftosa |
| **Alumno** | Arian Pedroza Celis |
| **Grupo / Carrera** | 4° Semestre / Licenciatura en Ciencias de Datos para Negocios |
| **Fecha** | Mayo 2026 |
| **Docente** | Luis Gerardo Acuña Quintero |
| **Comunidad / Sector de impacto** | Pequeños y medianos productores ganaderos, inspectores sanitarios de la CPA/SENASICA, consumidores finales, transportistas pecuarios y el hato nacional bovino (35.1M cabezas). |

---

# 2. Identificación de la Problemática

**• ¿Qué problema social identificaron?**

El verdadero obstáculo de la vigilancia epidemiológica en México no es la falta de tecnología, sino una **asimetría perversa de incentivos**: el ganadero que detecta síntomas de Fiebre Aftosa (FMD) en su hato sabe que reportar oficialmente implica el **sacrificio total de su inventario**, la pérdida inmediata de su fuente de ingreso y la quiebra en menos de 90 días. Ante este miedo racional, el productor oculta el brote, generando una propagación silenciosa y descontrolada que termina siendo exponencialmente más costosa para todos los actores del sistema.

Este dilema ético —entre el interés individual del ganadero y el bien colectivo de la bioseguridad nacional— es la causa raíz del fallo sistémico. La Fiebre Aftosa (FMD) se clasifica como una **enfermedad exótica de notificación obligatoria** (OIE/WOAH), pero la obligatoriedad sin un sistema de protección económica para el productor convierte la transparencia en una amenaza para el ganadero, no en un recurso.

**• ¿Quiénes son las personas afectadas?**

- **Productores primarios:** Pequeños y medianos ganaderos con hatos de 50–500 cabezas, cuya actividad representa el 100% de su ingreso familiar. Un brote sin detección temprana los condena a la quiebra.
- **Trabajadores de rastros y transporte:** El sacrificio masivo y el cierre de fronteras sanitarias destruye el empleo en toda la cadena logística.
- **Consumidores finales:** La interrupción de la cadena de suministro cárnica eleva los precios y reduce la disponibilidad de proteína animal.
- **El hato nacional:** 35.1 millones de cabezas bovinas vulnerables a una enfermedad con potencial de devastar el 96% del inventario nacional en 180 días según nuestras simulaciones.

**• ¿Dónde ocurre?**

A nivel nacional, con focos de máxima vulnerabilidad estructural en los estados con mayor inventario bovino y alta conectividad carretera: **Veracruz** (epicentro más peligroso por flujo gravitatorio saliente), **Jalisco** (mayor masa individual), **Chiapas**, **Michoacán** y **Puebla** (nodo-puente de intermediación). El riesgo no es geográfico-estático; es dinámico y se propaga a través de la red vial nacional como un flujo comercial de ganado.

**• ¿Cuáles son las causas principales?**

1. **El incentivo perverso al silencio:** No existe un mecanismo de reporte anónimo que desacople la identidad del productor de la alerta epidemiológica, eliminando el miedo a la sanción económica inmediata.
2. **La opacidad institucional:** Los datos de cuarentenas y movimientos de ganado de SENASICA no se publican en formatos computacionalmente accesibles, generando silos de información que impiden la vigilancia predictiva.
3. **La falta de modelado espacial:** Las autoridades no disponen de herramientas para estimar con precisión cómo se propagaría un brote a través de la red de carreteras, impidiendo la priorización inteligente de recursos de inspección.
4. **La ausencia de trazabilidad digital:** Menos del 15% del hato nacional cuenta con trazabilidad electrónica activa, imposibilitando el rastreo de contactos post-brote.

**• ¿Qué consecuencias genera?**

- Pérdidas económicas catastróficas estimadas en **$52,800 millones de USD** en 150 días si un brote de FMD no se contiene a tiempo (análisis de flujo de caja del sistema).
- Cierre inmediato de fronteras de exportación (México es un exportador neto de carne bovina) por parte de EE.UU., Japón y la UE.
- Sacrificio masivo innecesario por falta de zonificación de riesgo: sin detección temprana, se sacrifica más ganado del estrictamente necesario.
- Ruptura de la cadena alimentaria nacional con impacto desproporcionado en las comunidades rurales dependientes de la ganadería de subsistencia.

---

# 3. Relación con los Objetivos de Desarrollo Sostenible (ODS)

**• ODS relacionados:**

- **ODS 2: Hambre Cero** — La seguridad del suministro de proteína animal nacional.
- **ODS 3: Salud y Bienestar** — Bajo el enfoque *One Health*, la FMD tiene implicaciones en la salud pública al interrumpir cadenas alimentarias.
- **ODS 9: Industria, Innovación e Infraestructura** — Digitalización de la cadena de valor ganadera.
- **ODS 17: Alianzas para lograr los Objetivos** — Colaboración entre gobierno (SENASICA), academia (URC) y sector privado (ganaderos).

**• Justificación:**

AftoSec actúa como infraestructura de bien público que protege simultáneamente la seguridad alimentaria (ODS 2), la salud animal como componente de la salud pública (ODS 3), y la digitalización del sector primario (ODS 9). La criptografía Zero-Knowledge es el habilitador técnico que hace posible la alianza de datos entre actores que históricamente no han confiado entre sí (ODS 17).

**• Meta específica que se busca impactar:**

> *Meta 3.d: Reforzar la capacidad de todos los países en materia de alerta temprana, reducción de riesgos y gestión de los riesgos para la salud nacional y mundial.*

---

# 4. Diagnóstico del Contexto

**• Contexto social — El Dilema Ético del Ganadero:**

El sistema de bioseguridad actual penaliza al ganadero honesto. Un productor con 200 cabezas que reporta una sospecha de FMD enfrenta el sacrificio de la totalidad de su hato, con indemnizaciones gubernamentales que en el mejor de los casos cubren el 40–60% del valor comercial. Esto crea una dinámica de *juego de gallina* entre el interés individual y el colectivo: el ganadero que reporta tarde pero no reporta gana tiempo, pero arrastra a toda la comunidad al desastre.

AftoSec resuelve esto con **criptografía Zero-Knowledge**: el productor reporta síntomas desde una app móvil sin revelar su identidad. Sus datos personales (Nombre, RFC, coordenadas exactas del rancho) se cifran localmente con RSA-2048 antes de transmitirse. El sistema de IA puede generar alertas epidemiológicas anónimas sin saber quién reportó. Solo cuando la probabilidad de brote supera un umbral crítico (≥ 0.85) y se activa el protocolo oficial de cuarentena, la CPA puede usar su llave privada para revelar la identidad del productor y coordinar el apoyo financiero de contingencia.

**Este es el corazón de la innovación social: convertir la transparencia epidemiológica en un activo, no en una amenaza.**

**• Contexto económico:**

El sector ganadero bovino aporta aproximadamente el 1.2% del PIB nacional. Un brote masivo de FMD no contenido provocaría:
- Pérdida directa de $52,800M USD en valor del hato sacrificado.
- Cierre de fronteras de exportación por mínimo 3–5 años.
- Colapso de la cadena de valor que emplea a más de 1.2 millones de personas.
- Presión inflacionaria en alimentos básicos (carne y leche) de hasta 35%.

La inversión en AftoSec —sensores, software, infraestructura de datos— representa menos del 0.001% de este riesgo catastrófico, generando un **ROI documentado superior al 340%** bajo el escenario de detección temprana de 48 horas.

**• Contexto ambiental:**

La FMD y las respuestas mal coordinadas a ella tienen un impacto ambiental directo:
1. **El sacrificio masivo innecesario:** El protocolo estándar de "cuarentena y sacrificio total" en zonas amplias destruye miles de cabezas sanas. AftoSec permite zonificación precisa (GeoJSON buffers de 3 km), reduciendo el radio de sacrificio al mínimo epidemiológicamente necesario.
2. **Residuos biológicos del sacrificio:** La gestión inadecuada de carcasas genera contaminación de mantos freáticos y suelos. La detección temprana reduce la masa de residuos biológicos.
3. **Huella de carbono:** El ciclo de sacrificio-repoblación masiva tiene una huella de carbono enorme (transporte, procesamiento, crianza de reemplazos). Prevenir el brote es ambientalmente superior a responder a él.

**• Contexto cultural:**

La cultura ganadera en México, especialmente en regiones como Jalisco, Chiapas, Sonora y Veracruz, tiene una fuerte identidad comunitaria y desconfianza histórica hacia la intervención gubernamental en la inspección de ganado. El ganadero percibe al inspector sanitario como un agente de confiscación, no de apoyo. AftoSec invierte este paradigma:

- El productor controla qué información comparte y cuándo.
- La criptografía le garantiza que sus datos no serán usados para fines fiscales o de confiscación arbitraria.
- El sistema funciona como un **escudo económico**, no como una herramienta de vigilancia.

**• Actores involucrados (Mapa de Stakeholders):**

| Actor | Rol | Incentivo para participar |
|-------|-----|--------------------------|
| **Ganadero / Productor** | Reportante de síntomas | Protección de identidad, acceso a indemnizaciones más rápidas |
| **Veterinario de campo** | Validador clínico de alertas | Herramienta de apoyo diagnóstico en zonas remotas |
| **SENASICA / CPA** | Autoridad epidemiológica | Datos en tiempo real para respuesta oportuna |
| **SADER** | Coordinación de programas de apoyo | Focalización eficiente de subsidios de contingencia |
| **Transportistas pecuarios** | Nodo de transmisión en red vial | Rutas seguras, evitar cierres imprevistos de carreteras |
| **Universidad (URC)** | Desarrollo tecnológico y validación | Investigación aplicada y generación de conocimiento |
| **Consumidores finales** | Beneficiarios de cadena alimentaria segura | Disponibilidad y precio estable de carne |

---

# 5. Investigación y Recolección de Información

**• Fuentes documentales:**

- SIAP/SADER (2023): Inventario Bovino Nacional — 35.1M cabezas por estado.
- SENASICA (2024): Reportes de cuarentenas activas y estatus zoosanitario.
- OSRM/OpenStreetMap: Matriz de distancias reales por carretera (32×32 estados).
- OIE/WOAH (2023): Manual de diagnóstico de FMD — Capítulo 3.1.8.
- Knight-Jones & Rushton (2013): Impacto económico de la FMD, Preventive Veterinary Medicine.
- Tildesley et al. (2006): Estrategias óptimas de vacunación reactiva, Nature.
- Anderson (2002): Reporte de la epidemia FMD 2001 en Reino Unido.

**• Metodología de recolección:**

- Pipeline ELT automatizado con validación Pydantic sobre datos del SIAP.
- Consulta a API OSRM para obtención de la matriz de distancias terrestres reales.
- Construcción de grafo dirigido ponderado (32 nodos × 992 aristas) con NetworkX.
- Simulación Monte Carlo SIR Espacial sobre 180 días, semilla reproducible (seed=42).

**• Hallazgos principales:**

1. **El epicentro no es donde más vacas hay, sino donde más exporta:** La variable más predictiva del colapso de un estado es el `weighted_out_flux` (flujo gravitatorio saliente), no el inventario bovino absoluto.
2. **La geografía retrasa pero no evita el colapso:** El modelo espacial redujo el pico nacional de ~17M a **10.2M infectados simultáneos** (+13 días al pico), demostrando que la fricción geográfica da una ventana de intervención real de 13 días.
3. **La ventana crítica de contención:** Bloqueando selectivamente menos del 5% de las aristas del grafo vial (puntos de inspección en estados de alta intermediación), se puede salvar hasta el **40% del hato nacional** mediante Network Extinction.
4. **El análisis de 3 escenarios (Veracruz, Sonora, Puebla)** demuestra que la topología del origen define la velocidad y el patrón de propagación, no solo la magnitud.

---

# 6. Diseño de la Propuesta de Innovación Social

**• Nombre de la propuesta:**

**AftoSec** — Sistema Integral de Vigilancia Epidemiológica de Precisión con Criptografía Zero-Knowledge para la Detección Temprana de Fiebre Aftosa en México.

**• Descripción de la solución:**

AftoSec es un sistema integrado de tres capas que resuelve el dilema ético del ganadero y la asimetría de información del sistema epidemiológico:

**Capa 1 — Reporte Anónimo (App Móvil):**
El productor reporta síntomas desde una app con interfaz simplificada. Sus datos personales se cifran localmente con RSA-2048+OAEP antes de transmitirse. El servidor solo recibe texto cifrado ilegible. La geolocalización se transmite como polígono de área (no punto exacto) para proteger la privacidad predial.

**Capa 2 — Inteligencia Espacial (Motor XGBoost + SIR):**
El motor de IA evalúa el riesgo en función de la topología del grafo de transporte. Si la alerta supera el umbral de riesgo (≥ 0.85), el sistema genera automáticamente:
- Un polígono GeoJSON de cuarentena de 3 km.
- Una estimación del pico de infectados esperado en los estados conectados.
- Un ranking de los 5 estados en mayor riesgo de contagio en los próximos 30 días.

**Capa 3 — Desencriptación Autorizada (CPA/SENASICA):**
Solo ante un brote confirmado por RT-PCR, la autoridad usa su llave privada RSA para revelar la identidad del productor y activar el protocolo de indemnización. Este mecanismo convierte el reporte temprano en un **activo financiero** para el ganadero, no en una sentencia.

**• ¿Qué hace innovadora la propuesta?**

La innovación no es el algoritmo de IA ni el modelo epidemiológico —estas son herramientas bien conocidas. La innovación es el **diseño de incentivos**:

1. *Criptografía como instrumento de política pública:* La privacidad tecnológica rompe el dilema ético y convierte al ganadero de actor pasivo-resistente en colaborador activo.
2. *Network Extinction como política de salud:* Reemplaza la vacunación masiva reactiva por una estrategia de contención dirigida, 10 veces más eficiente por peso invertido.
3. *Datos del productor como capital, no como pasivo:* Al garantizar que el dato no será usado para fines punitivos, se genera un sistema de reporte voluntario que funciona sin coerción.

**• Modelo de Adopción y Escalabilidad:**

```
FASE 1 — Piloto (Meses 1-6):
  • 50 ganaderos voluntarios en Veracruz y Jalisco
  • App móvil + backend MongoDB local
  • Validación del modelo XGBoost con datos reales

FASE 2 — Expansión Regional (Meses 7-18):
  • Alianza con asociaciones ganaderas estatales (UGRVJ, UGRAM)
  • Integración con SENASICA vía API
  • Entrenamiento de inspectores veterinarios como operadores del sistema

FASE 3 — Escala Nacional (Mes 19+):
  • Despliegue en los 32 estados
  • Dashboard público de riesgo epidémico (datos anonimizados)
  • Integración con la Campaña Nacional Zoosanitaria
```

**• Beneficiarios directos:**
- Productores ganaderos con hatos de 50–2,000 cabezas que hoy no tienen acceso a herramientas de gestión de riesgo epidémico.
- Inspectores sanitarios de SENASICA y veterinarios de campo.

**• Beneficiarios indirectos:**
- Consumidores de carne bovina en México (~130M personas).
- Transportistas pecuarios que evitan cierres imprevistos de rutas.
- El gobierno federal al reducir el pasivo contingente de indemnizaciones masivas.

---

# 7. Planeación de Actividades

**• Actividades completadas en Semestre 2026-1:**

| Semana | Actividad | Logro | Evidencia |
|--------|-----------|-------|-----------|
| 1–4 | Ingeniería de Datos (ELT) | Pipeline de 6 fuentes, 29,200+ registros | `src/warehouse/mongodb_loader.py` |
| 5–8 | Modelo Gravitatorio + Red Vial | Grafo 32×992, API OSRM | `src/spatial_model/02_gravity_model.py` |
| 9–12 | SIR Espacial (180 días) | GIF + CSV + figuras (pico 10.2M) | `src/spatial_model/03_spatial_sir.py` |
| 13–16 | XGBoost Risk Scoring | R²=0.8924, 13 features | `src/spatial_model/05_xgboost_risk.py` |
| 17–18 | Criptografía RSA-2048 + Bcrypt | Demo funcional de encriptación PII | `src/crypto/encryption.py` |
| 19–20 | Benchmark 4 modelos (LOOCV) | XGBoost supera a RF, DT, RLM | `src/spatial_model/08_model_benchmark.py` |
| 21 | Análisis de Sensibilidad | 3 escenarios (Veracruz, Sonora, Puebla) | Documentado en tercer_avance.md |
| 22 | Documentación integral | Artículo + Diapositivas + Cumplimiento PP | Docs en `/docs/Tercer_avance/` |

**• Responsable:** Arian Pedroza Celis (Líder de Ciencia de Datos y Arquitectura de Software)

**• Recursos utilizados:**
- Repositorio GitHub: `EpidemicResearch`
- Entorno de cómputo: Apple Silicon (M-series), Python 3.11+
- Stack técnico: `geopandas`, `networkx`, `xgboost`, `scikit-learn`, `pymongo`, `cryptography`, `scipy`, `matplotlib`
- APIs: OSRM (routing), SIAP/SADER (inventarios bovinos)

---

# 8. Impacto Esperado

**• Impacto social — Resolución del Dilema Ético:**

Al garantizar el anonimato criptográfico del reportante, AftoSec transforma la estructura de incentivos del ganadero:

- **Antes de AftoSec:** Reportar = arriesgar la quiebra → incentivo a ocultar.
- **Con AftoSec:** Reportar anónimamente = acceder a indemnización rápida + proteger a los vecinos → incentivo a cooperar.

Esta inversión del incentivo es el mecanismo de innovación social más poderoso del sistema, porque hace que el bien individual y el bien colectivo converjan por primera vez.

**• Impacto ambiental:**

| Indicador | Sin AftoSec | Con AftoSec | Mejora |
|-----------|-------------|-------------|--------|
| Cabezas sacrificadas (180 días) | 33.4M (96.9% del hato) | ~20M (con Network Extinction) | -40% |
| Residuos biológicos generados | ~5M toneladas de carcasas | ~3M toneladas | -40% |
| Huella de carbono (sacrificio + repoblación) | Máxima | Reducida por zonificación | -30–40% |
| Radio de cuarentena | Estatal (miles de km²) | Buffer GeoJSON de 3 km | -99% en área |

La zonificación de riesgo mediante GeoJSON permite cuarentenas quirúrgicas que minimizan el daño ambiental del sacrificio masivo.

**• Impacto económico:**

Un análisis contrafactual documenta que la inversión en detección temprana de 48 horas genera:
- **ROI > 340%** al reducir el número de animales sacrificados.
- Diferencia entre $2,000M MXN (contención en un estado) vs $200,000M MXN (propagación nacional).
- Preservación del estatus de exportación ante EE.UU. (mercado valorado en $800M USD/año).

**• Indicadores de éxito:**

1. **R² del modelo XGBoost ≥ 0.89** en predicción del pico de infectados por estado (✅ Logrado: 0.8924).
2. **Tiempo de procesamiento del alerta < 15 segundos** desde el reporte del ganadero hasta la generación del polígono GeoJSON de cuarentena.
3. **Tasa de adopción voluntaria ≥ 30%** en pilotos de zonas de alto riesgo (Veracruz, Jalisco) en los primeros 6 meses.
4. **Reducción del radio de sacrificio en ≥ 60%** vs el protocolo estándar de cuarentena estatal.

---

# 9. Reflexión Final

**• ¿Qué aprendieron durante el proceso?**

La lección más profunda de este proyecto no es técnica: es que **el peor problema de diseño en sistemas de información de salud pública no es la falta de datos, sino la falta de confianza**. Todas las herramientas algorítmicas del mundo (SIR, XGBoost, grafos, APIs) son inútiles si el actor humano clave —el ganadero— no reporta porque le da miedo. Diseñar el sistema criptográfico como un mecanismo de construcción de confianza fue la decisión de ingeniería social más importante del proyecto, no la elección del modelo de IA.

La segunda lección es que la geografía importa: un modelo de mezcla homogénea que ignora las carreteras no solo es matemáticamente incorrecto, sino que genera políticas de respuesta equivocadas. La fricción espacial da tiempo —13 días adicionales de ventana de contención— y esos 13 días son la diferencia entre salvar el 40% del hato o perder el 97%.

**• ¿Qué dificultades encontraron?**

- La opacidad de los datos gubernamentales (SENASICA publica en PDFs no estructurados) obligó a desarrollar técnicas avanzadas de web scraping forense.
- La limitación de muestra (N=32 estados) impone restricciones estadísticas reales: la Regresión Lineal Múltiple no es viable con 13 features y 27 muestras (identificamos overfitting con R²=1.0 como síntoma), lo que justificó la elección de XGBoost con regularización.
- Construir el argumento de Network Extinction (fragmentación de grafos para contención epidémica) requirió integrar conceptos de tres disciplinas simultáneamente: epidemiología, teoría de grafos y política pública.

**• ¿Cómo mejorarían la propuesta?**

1. **Sensores IoT en puntos de entrada/salida de camiones ganaderos:** Lectores RFID en casetas de inspección de carretera que registren automáticamente los movimientos de ganado y alimenten el grafo en tiempo real.
2. **Integración con SINIIGA (Sistema Nacional de Identificación Individual de Ganado):** Conectar el modelo de riesgo con el arete electrónico para trazabilidad individual, no solo estatal.
3. **Panel de riesgo público anonimizado:** Un dashboard accesible para productores y veterinarios que muestre el nivel de alerta en tiempo real por región, incentivando la vigilancia distribuida.
4. **Modelo de aprendizaje federado:** Entrenar XGBoost de forma distribuida con datos de cada rancho sin que el dato abandone el dispositivo local del productor, maximizando privacidad y volumen de entrenamiento simultáneamente.

---

# Formato de Seguimiento Semanal (Actualizado)

| Semana | Actividad realizada | Avances | Dificultades | Acciones siguientes |
|--------|---------------------|---------|--------------|---------------------|
| **1–4** | Pipeline ELT + Minería de Datos | 6 fuentes integradas, 29,200+ registros en MongoDB. Modelo SIR base calibrado. | PDFs no estructurados de SENASICA, scraping forense. | Construcción del grafo vial y modelo gravitatorio. |
| **5–8** | Modelo Gravitatorio + Red Vial OSRM | Grafo dirigido 32×992 aristas. Matriz de distancias reales por carretera. | Latencia de la API OSRM en consultas masivas (32×32). | Simulación SIR Espacial sobre el grafo. |
| **9–12** | SIR Espacial (180 días) + Visualizaciones | GIF animado de propagación. Pico reducido a 10.2M. Stacked Race Chart MP4. | Parametrización del acoplamiento espacial (β_spatial). | XGBoost Risk Scoring sobre las 13 features topológicas. |
| **13–16** | XGBoost + Feature Importance + Criptografía | R²=0.8924. Encriptación RSA-2048 funcional. MongoDB con 7 colecciones. | Overfitting de RLM (R²=1.0) que requirió explicación epistémica. | Benchmarking formal y análisis de sensibilidad. |
| **17–20** | Benchmark 4 modelos + Análisis Sensibilidad | 3 escenarios (Veracruz, Sonora, Puebla) documentados. XGBoost validado como el mejor modelo. | Varianza alta en predicción de "día de infección" (target débil). | Documentación final, presentación y coloquio. |
