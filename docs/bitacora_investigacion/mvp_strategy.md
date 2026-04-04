# Ganado Saludable — Execution Strategy & MVP Definition

> **Documento de referencia clave para evitar overengineering.**
> Si pierdes contexto con el agente, este doc tiene todo lo que necesitas para retomar.
> Última actualización: 2025-03-25

---

## ⚠️ Regla de Oro

> **El implementation_plan.md es un MENÚ de opciones, NO un checklist.**
> No necesitas construir todo lo que está documentado.
> Ejecuta el Tier 1 primero. Solo avanza a Tier 2/3 si te sobra tiempo.

---

## El Entregable Real (Lo que el profesor espera)

| Constraint | Valor |
|---|---|
| Presentación oral | 10-15 minutos, ~15-20 slides |
| Formato | Gamma, Genially o Prezi |
| Artículo de divulgación | 15-25 páginas, APA 7, min 5 fuentes |
| Participación | Equitativa entre todos los miembros |
| Prototipo | Al menos 1 (organizacional, visual, algorítmico o educativo) |
| Reflexión | Impacto ambiental, social y económico |

**Todo lo demás (pipeline, MongoDB, dashboard, XGBoost) son HERRAMIENTAS para generar los datos y gráficos que irán en el artículo y la presentación. No son entregables en sí mismos.**

---

## Enfermedad Asignada y Estrategia Metodológica

- **Enfermedad asignada por el profesor:** Fiebre Aftosa (FMD)
- **Problema:** México es libre de FMD desde 1954 → no hay datos nacionales de brotes
- **Solución:** Usar TB Bovina como proxy de calibración (datos reales de SENASICA) y transferir parámetros al escenario FMD
- **Concepto clave:** "Transfer Learning epidemiológico" — calibrar con R0_tb ≈ 1.8, simular con R0_fmd ≈ 6.0
- **Contribución original:** "Proxy de Opacidad" — clausuras por clembuterol como indicador de abuso antibiótico

---

## Sistema de Tiers (Priorización)

### 🟥 TIER 1 — MVP (Ship or Die)

**Meta:** Cubrir las 7 materias con el mínimo esfuerzo viable. Con SOLO esto ya tienes un proyecto entregable y defendible.

| # | Componente | Materia(s) que cubre | Esfuerzo | Notas |
|---|---|---|---|---|
| 1 | **SENASICA CSV extractor** (hatos libres TB) | — | Medio | Primary path: CSV directo. Sin API interception. |
| 2 | **DGE Anuarios extractor** (ZIP→CSV, CIE-10 A05/A15-A19) | — | Medio | Download + unzip + filter. latin1 encoding. |
| 3 | **Modelo SIR dual** (TB calibración → FMD simulación) | EDOs | Bajo | scipy.odeint. 3-6 escenarios. LA PIEZA CENTRAL. |
| 4 | **Gráficas SIR** (curvas S/I/R + comparativa TB vs FMD) | EDOs | Bajo | matplotlib. Máximo impacto visual. |
| 5 | **1 mapa coroplético** (prevalencia TB por estado) | IA / Innov. Social | Bajo | plotly.express con GeoJSON de México. |
| 6 | **Módulo crypto** (César + RSA demo funcional) | Criptografía | Bajo | encrypt/decrypt/keygen. ~100 líneas. |
| 7 | **MongoDB** con 2-3 colecciones + Pydantic models | NoSQL | Bajo | Docker mongo:latest. Insert + query básico. |
| 8 | **1 tabla financiera** (ROI/VPN preventivo vs reactivo) | Finanzas | Bajo | Puede ser un cálculo en notebook, no necesita motor. |
| 9 | **1 test estadístico** (ANOVA canales de venta Salmonella) | Estadística Multi. | Bajo | scipy.stats.f_oneway. 4 grupos, 1 resultado. |
| 10 | **Artículo** (15-25 págs) + **Presentación** (15-20 slides) | TODAS | Alto | El entregable real. Todo lo demás alimenta esto. |

**Tiempo estimado Tier 1:** 1-2 semanas de trabajo enfocado.

---

### 🟨 TIER 2 — Nice to Have (Si te sobra tiempo)

| # | Componente | Qué añade | Esfuerzo |
|---|---|---|---|
| 11 | **XGBoost** con SHAP values | IA más impresionante que solo EDA | Medio |
| 12 | **Caras de Chernoff** (5-8 estados clave, NO 32) | Wow factor Estadística Multivariada | Medio |
| 13 | **PCA** + scree plot + biplot | Complementa Chernoff, fácil con sklearn | Bajo |
| 14 | **openFMD extractor** | Datos internacionales FMD para reforzar narrativa | Bajo |
| 15 | **Regresión lineal múltiple** | Interpretabilidad: coeficientes con p-values | Bajo |
| 16 | **Clembuterol como feature** en XGBoost | "Proxy de Opacidad" funcional | Bajo (si PNT funciona) |
| 17 | **Más mapas coropléticos** (clausuras, riesgo predicho) | Más visuales para el artículo | Bajo |

---

### 🟦 TIER 3 — Flex Mode (Solo si quieres impresionar o tienes semanas extra)

| # | Componente | Qué añade | Esfuerzo |
|---|---|---|---|
| 18 | **Dashboard Streamlit** | Demo en vivo en coloquio — efecto WOW máximo | Alto |
| 19 | **Curvas de Andrews** | Sofisticación estadística extra | Medio |
| 20 | **SINAIS ViewState bypass** | Técnicamente cool pero frágil | Alto |
| 21 | **PNT Selenium** (clausuras COFEPRIS) | El extractor más complejo, alto riesgo de fallo | Alto |
| 22 | **Chronos time series** | Predicción de trayectorias, requiere openFMD | Medio |
| 23 | **SENASICA API interception** | Hacker mode, innecesario si CSV funciona | Alto |
| 24 | **MANOVA** | Overkill estadístico, ANOVA basta | Bajo |

---

## Qué técnica usar si los datos son escasos

**Si un extractor falla o los datos son insuficientes, aquí está el fallback:**

| Si falla... | Usa en su lugar... | ¿Por qué? |
|---|---|---|
| SENASICA API (datos granulares) | SENASICA CSV (datos agregados) | CSV siempre disponible en datos abiertos |
| XGBoost (necesita muchos datos) | Regresión lineal múltiple | Funciona con 32 observaciones (estados) |
| Chernoff (32 estados con 7 variables) | Choropleth map | Solo necesita 1 variable por estado |
| PNT Selenium (JS dinámico, CAPTCHAs) | Búsqueda manual + descarga de PDFs | Semi-manual pero funcional |
| SINAIS cubos (ActiveX/OWC11) | DGE Anuarios ZIP→CSV | Mismos datos, diferente fuente |
| openFMD (datos FMD internacionales) | Parámetros R0 de literatura (Tildesley et al.) | No necesitas datos raw si usas R0 publicados |
| Dashboard Streamlit | Screenshots de matplotlib en slides | Mismo resultado visual, sin infraestructura |

---

## Cobertura de las 7 Materias — Versión MVP

| Materia | MVP (mínimo para aprobar) | Con qué se entrega |
|---|---|---|
| **Criptografía** | Demo César ("LOTE"→"ORWH") + RSA keygen/encrypt/decrypt | Código + sección artículo |
| **Estadística Multi.** | ANOVA de canales de venta (p-value) + 1 mapa coroplético | Tabla + gráfico artículo |
| **IA** | EDA + mapa coroplético con datos cruzados | Notebook + gráficos |
| **NoSQL** | MongoDB Docker con 2 colecciones + justificación de elección | Diagrama + sección artículo |
| **EDOs** | SIR dual (TB vs FMD) con 3-6 escenarios + curvas | Gráficas + sección artículo |
| **Finanzas** | 1 tabla de ROI/VPN (preventivo $5M vs reactivo $39M/$200B) | Tabla + sección artículo |
| **Innov. Social** | Enfoque One Health + mapa de actores + reflexión inequidad | Sección artículo |

---

## Estructura de la Presentación (10-15 min)

| Slide | Contenido | Tiempo |
|---|---|---|
| 1 | Título + equipo | 15s |
| 2-3 | El problema: "México libre de FMD pero ciego" + datos de impacto | 1.5 min |
| 4 | Enfoque One Health (diagrama animal↔humano↔finanzas) | 1 min |
| 5 | Metodología: proxy TB + transfer learning | 1 min |
| 6 | Mapa coroplético (prevalencia TB por estado) | 1 min |
| 7-8 | Modelo SIR: curvas TB vs FMD lado a lado (THE MONEY SHOT) | 2 min |
| 9 | ANOVA: canales de venta Salmonella (p-value) | 1 min |
| 10 | Tabla financiera: $5M prevención vs $200B catástrofe | 1 min |
| 11 | Criptografía: demo César + RSA (por qué importa para IoT) | 1 min |
| 12 | MongoDB: esquema de colecciones (por qué NoSQL) | 1 min |
| 13 | Innovación social: inequidad geográfica + tianguis | 1 min |
| 14 | Conclusión + cita de cierre | 1 min |
| 15 | Q&A | Resto |

**Slides opcionales (Tier 2):** Chernoff faces, SHAP values, PCA biplot, dashboard demo.

---

## Documentos del Proyecto

| Archivo | Propósito | ¿Cuándo leerlo? |
|---|---|---|
| **docs/mvp_strategy.md** | **ESTE DOCUMENTO.** Priorización y anti-overengineering | Siempre que dudes qué hacer primero |
| `docs/implementation_plan.md` | Arquitectura técnica completa (menú de opciones) | Cuando necesites detalle de un componente |
| `docs/task.md` | Checklist de todas las tareas | Para tracking de progreso |
| `docs/presentation_script.md` | Guion narrativo para coloquio (4 actos) | Cuando prepares la presentación |
| `README.md` | Documentación pública + cobertura de 7 materias | Para entender el proyecto completo |
| `V2.md` | Datos epidemiológicos clave | Para constantes y cifras |
| `M_doc.md` | Protocolo de extracción con URLs | Para implementar extractores |

---

## Instrucciones para un Agente Nuevo

> Si estás leyendo esto como un agente de IA que retoma la conversación:
>
> 1. **Lee este documento primero.** Define el MVP y los tiers.
> 2. **Lee `docs/implementation_plan.md`** para la arquitectura completa.
> 3. **Lee `docs/task.md`** para ver qué está hecho y qué falta.
> 4. **NO construyas todo el plan.** Ejecuta solo el Tier donde el usuario esté.
> 5. **La enfermedad asignada es Fiebre Aftosa (FMD).** TB Bovina es el proxy.
> 6. **El entregable real es un artículo de 15-25 págs + presentación de 15 min.**
> 7. **Evita overengineering.** Pregunta: "¿Esto va a aparecer en una slide o en el artículo? Si no, no lo construyas."
