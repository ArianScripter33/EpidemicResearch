# 🐄 Ganado Saludable: Guion de Presentación (Coloquio)

> **Bioseguridad Inteligente frente al Bioterrorismo Corporativo**
> Detección Temprana, Ciencia de Datos y el Paradigma "One Health"

---

## 📋 Guía Rápida de Prioridad

Antes de leer el guion completo, tengan claro esto:

| Etiqueta | Significado | ¿Qué hacer? |
|---|---|---|
| 🟥 **MVP** | Obligatorio para entregar y presentar | Hacerlo primero. Sin esto no hay proyecto. |
| 🟨 **NICE TO HAVE** | Opcional. Añade puntos extra si tenemos tiempo y datos | Hacerlo solo si el MVP está completo. |

**El entregable real:**
- Presentación oral: **10-15 min**, ~15-20 slides
- Artículo de divulgación: **15-25 páginas**, APA 7, mínimo 5 fuentes
- Al menos 1 prototipo (visual, algorítmico u organizacional)

**Todo lo demás (pipeline, MongoDB, dashboard, XGBoost) son HERRAMIENTAS para generar los datos y gráficos que van en el artículo y la presentación. No son entregables en sí mismos.**

> Para más detalle sobre la priorización, ver `docs/mvp_strategy.md`.

---

## ACTO I: El Espejismo de la Seguridad y los "Reactores Biológicos" (El Gancho)

> 🟥 **MVP** — Este acto es el gancho narrativo. Va sí o sí en las primeras 2-3 slides.

**Narrativa:**
México ha estado libre de la Fiebre Aftosa (FMD) desde 1954. Esta aparente victoria nos ha vuelto ciegos ante un peligro inminente. Hoy en día, los 2.8 millones de bovinos que ingresan anualmente a los corrales de engorda intensiva (CAFOs) en nuestro país ya no son solo centros de producción de carne; se han convertido en auténticos **"vasos de mezcla" o reactores biológicos**.

Las condiciones de hacinamiento extremo, el amoníaco que quema los tractos respiratorios y el abuso de antibióticos obligan a virus y bacterias a mutar violentamente. El Dr. Michael Greger advierte que estas instalaciones son fábricas de patógenos letales, comparables con agentes de **bioterrorismo** (como ocurrió con el virus Nipah en granjas de cerdos). Sin embargo, la industria mantiene esto oculto mediante un **"corporativismo defensivo"**, negándose a revelar qué y cuánto inyectan a los animales para evitar sanciones comerciales.

**El Problema Prototípico:** ¿Cómo podemos, como científicos de datos, penetrar esta barrera de opacidad y crear un sistema de alerta temprana que proteja las 35.1 millones de cabezas de ganado en México y, en consecuencia, la salud humana y la economía nacional?

---

## ACTO II: La Estrategia del "Proxy" (Explicación Metodológica)

> 🟥 **MVP** — La explicación de por qué usamos TB como proxy es obligatoria. El jurado necesita entender que FMD no tiene datos en México.

**Narrativa Didáctica:**
Como no tenemos datos recientes de Fiebre Aftosa en México, los algoritmos estarían "ciegos". Para resolverlo, diseñamos una arquitectura **Dual-Path** usando *Transfer Learning* y *Proxies*:

1. 🟥 **MVP — El Proxy Epidemiológico (Tuberculosis Bovina):** Calibraremos nuestros modelos con los datos reales de cuarentenas y gasto estatal del SENASICA para Tuberculosis Bovina (una enfermedad endémica y crónica con R0 ≈ 1.8), y luego transferimos esos parámetros al escenario catastrófico de FMD (R0 ≈ 6.0).

2. 🟨 **NICE TO HAVE — El Proxy de Opacidad (Clenbuterol como indicador de abuso antibiótico):** Como la industria oculta el abuso de antibióticos, haremos minería de datos en la Plataforma Nacional de Transparencia (PNT/INAI) buscando clausuras por *Clenbuterol* y *LMR*. **Quien viola la ley usando Clenbuterol tiene una probabilidad casi absoluta de abusar de antibióticos.**

> **Nota para el equipo:** El Proxy de Opacidad es una contribución original nuestra y es muy poderoso narrativamente. Sin embargo, depende de que logremos extraer datos de la PNT con Selenium (técnicamente complejo). Si no lo logramos, el proyecto funciona perfecto solo con el Proxy Epidemiológico (TB).

---

## ACTO III: Arquitectura de la Solución (Integración de las 7 Asignaturas)

*Aquí demostramos al jurado cómo se resuelve el Problema Prototípico aplicando cada materia.*

---

### 1. 🔐 Fundamentos de Criptografía: Blindando la Verdad

> 🟥 **MVP** — Código funcional de César + RSA. ~100 líneas de Python.

* **El Reto:** Un competidor desleal interviene nuestros sensores IoT para inyectar datos falsos de temperatura, buscando enmascarar un brote y arruinar a "Carnes Selectas Mexicanas".
* **El Método:** Aplicaremos **Cifrado César** (ej. "LOTE" → "ORWH" con desplazamiento 3) para ofuscar identificadores rápidos, pero el núcleo será la **criptografía asimétrica (RSA)** con funciones *hash* (SHA-256).
* **Resultado:** Cada sensor firmará digitalmente su lectura. La manipulación de datos se vuelve criptográficamente imposible de ocultar.
* **Entregable MVP:** `src/crypto/encryption.py` — código funcional con demo interactiva.

---

### 2. 🗄️ Bases de Datos NoSQL: Escalabilidad ante el Caos

> 🟥 **MVP** — MongoDB Docker con 2-3 colecciones + justificación de por qué NoSQL y no SQL.

* **El Reto:** Un brote explosivo genera un tsunami de datos: lecturas IoT por segundo mezcladas con PDFs de cuarentenas del gobierno no estructurados.
* **El Método:** Implementaremos **MongoDB** con un diseño *Star Schema* adaptado a documentos BSON (embedding de dimensiones frecuentes).
* **Resultado MVP:** Modelo de datos documentado + insert/query funcionando. Almacenamiento de datos no estructurados (actas de clausura en texto libre).
* **Entregable MVP:** `src/warehouse/nosql_client.py` + colecciones MongoDB documentadas.

> 🟨 *NICE TO HAVE: Optimización de consultas geoespaciales, índices de texto completo, benchmarks de performance.*

---

### 3. 📊 Estadística Multivariada: El Rostro de la Crisis

> 🟥 **MVP mínimo:** ANOVA de canales de venta Salmonella (1 test, 1 p-value, 1 conclusión contundente).

* **El Reto:** Comprender la correlación entre decenas de variables (clima, densidad de ganado, clausuras y prevalencia de patógenos).
* **El Método MVP:** **ANOVA** para probar diferencia estadística entre canales de venta (supermercado 1.3% vs mercados 22.3%).
* **Resultado MVP:** Demostraremos que comprar carne en un mercado municipal tiene un riesgo estadísticamente superior al supermercado, con p-value para respaldarlo.
* **Entregable MVP:** Resultado del test ANOVA + 1 mapa coroplético de prevalencia por estado.

> 🟨 *NICE TO HAVE: PCA + scree plot + biplot, Caras de Chernoff (5-8 estados clave), Curvas de Andrews, Regresión Lineal Múltiple. Estas técnicas son más sofisticadas pero requieren más datos. Si los conseguimos, las añadimos; si no, ANOVA basta para cubrir la materia.*

---

### 4. 🤖 Inteligencia Artificial: El Oráculo Predictivo

> 🟥 **MVP mínimo:** EDA (Exploratory Data Analysis) + mapa coroplético con datos cruzados + narrativa de hallazgos.

* **El Reto:** Predecir un brote antes de que haya síntomas clínicos o decomisos masivos.
* **El Método MVP:** Análisis exploratorio de los datos extraídos (SENASICA + DGE) cruzados geográficamente. Visualización en mapa coroplético. Conclusiones descriptivas.
* **Entregable MVP:** Notebooks de EDA + gráficos descriptivos para el artículo.

> 🟨 *NICE TO HAVE: XGBoost Classifier con SMOTE + SHAP values. Esto es mucho más impresionante pero necesita suficientes datos limpios y features bien construidas. Si logramos el proxy de clembuterol + datos de SENASICA + DGE, lo intentamos. Si no, la EDA descriptiva cubre el requisito de IA.*

---

### 5. 📐 Ecuaciones Diferenciales Aplicadas: Modelando la Catástrofe

> 🟥 **MVP — LA PIEZA CENTRAL DEL PROYECTO.** Es lo más impactante visualmente y lo más sólido académicamente. Prioridad máxima.

* **El Reto:** Cuantificar el impacto temporal de la Fiebre Aftosa frente a una respuesta gubernamental lenta.
* **El Método:** **Sistema SIR dual** (Susceptibles, Infectados, Recuperados) de EDOs resuelto con Runge-Kutta (`scipy.integrate.odeint`).
  * **Modo 1 (TB calibración):** R0 ≈ 1.8, γ = 1/180 días
  * **Modo 2 (FMD simulación):** R0 ≈ 6.0, γ = 1/14 días
* **Resultado:** Las curvas de fase prueban que mientras la TB (R0=1.8) infecta al 12% del hato en 5 años, la FMD (R0=6.0) infectaría al **80% del hato nacional en solo 45 días**. Retrasar la cuarentena 48 horas = perder el control del país.
* **Entregable MVP:** `src/models/sir_prep.py` + 3-6 escenarios + gráficas comparativas TB vs FMD lado a lado.

> **Nota para el equipo:** Esta gráfica comparativa (TB lenta a la izquierda, FMD explosiva a la derecha) es "THE MONEY SHOT" de la presentación. Si solo pudiéramos mostrar 1 cosa, sería esta.

---

### 6. 💰 Finanzas Corporativas: El Valor Presente de la Supervivencia

> 🟥 **MVP** — 1 tabla comparativa de ROI/VPN. Puede ser un cálculo simple en un notebook.

* **El Reto:** Convencer a la junta directiva de que el sistema IoT no es un gasto, sino un escudo financiero.
* **El Método MVP:** Tabla de **VPN** y **ROI** comparando prevención vs reacción.
* **Resultado MVP:** $5M MXN de sistema preventivo vs $200B MXN de un brote FMD tipo UK 2001. El ROI de la prevención es infinito cuando se trata de evitar la quiebra.
* **Entregable MVP:** 1 tabla en el artículo con los números. No necesita un motor financiero completo.

> 🟨 *NICE TO HAVE: Motor financiero automatizado (`financial_roi.py`), Análisis DuPont completo, sensibilidad de escenarios, gráfico de flujos descontados.*

---

### 7. 🌍 Laboratorio de Innovación Social: *One Health*

> 🟥 **MVP** — Sección en el artículo + diagrama sistémico. No requiere código.

* **El Reto:** Evaluar el impacto ético y social de la propuesta.
* **El Método:** Paradigma "Una Sola Salud" (*One Health*) de la OMS/FAO/WOAH. Mapa de stakeholders. Análisis de inequidad.
* **Resultado:** Las superbacterias (94.7% resistencia a ampicilina) forjadas en corrales industriales terminan en los tianguis de comunidades rurales marginadas. Nuestro proyecto democratiza la bioseguridad.
* **Entregable MVP:** Diagrama sistémico (animal ↔ humano ↔ finanzas) + reflexión de impacto social en el artículo.

---

## ACTO IV: Conclusión y Entregables (El Cierre)

> 🟥 **MVP** — La conclusión y la cita de cierre van en la última slide.

**Narrativa:**
Nuestro artículo de divulgación y las visualizaciones probarán una premisa innegable que cumple con el objetivo de nuestra Licenciatura en Ciencias de Datos para Negocios:

> **"En la era de los virus pandémicos y la resistencia a los antibióticos, la verdadera innovación no es simplemente poner sensores en las vacas. Es utilizar las matemáticas, la criptografía y la inteligencia artificial para hacer visibles las cadenas de transmisión que un sistema fragmentado y corporativo intenta ocultar."**

La bioseguridad basada en datos no es un lujo; es nuestra única estrategia de supervivencia económica y sanitaria.

---

## Resumen de Prioridades para el Equipo

### Lo que DEBEMOS tener listo (🟥 MVP)

1. ✅ Datos extraídos de SENASICA (CSV) y DGE (Anuarios)
2. ✅ Modelo SIR dual con gráfica TB vs FMD (LA pieza central)
3. ✅ 1 mapa coroplético de México por estado
4. ✅ Módulo crypto funcional (César + RSA demo)
5. ✅ MongoDB con 2-3 colecciones
6. ✅ 1 tabla financiera (ROI prevención vs catástrofe)
7. ✅ ANOVA de canales de venta Salmonella
8. ✅ Sección One Health en el artículo
9. ✅ Artículo (15-25 págs) + Presentación (15-20 slides)

### Lo que PODRÍAMOS añadir si da tiempo (🟨 Nice to Have)

- XGBoost con SHAP values
- Caras de Chernoff (5-8 estados, no 32)
- PCA + scree plot
- Proxy de Opacidad (clembuterol via PNT)
- Dashboard Streamlit para demo en vivo
- Curvas de Andrews
- Regresión lineal múltiple
- Chronos time series

> **Regla para decidir:** ¿Esto va a aparecer en una slide o en el artículo? Si la respuesta es no, no lo construyas.

---

## Notas de Diseño para la Presentación

- **Formato sugerido:** Gamma o Genially (requerido por PP)
- **Duración:** 10-15 minutos (asignada por el comité)
- **Slides estimadas:** 15-20 máximo
- **Requisitos PP:**
  - Participación equitativa de todas las personas del equipo
  - Lenguaje claro, inclusivo y con argumentos sólidos
  - Apoyo visual mediante la presentación digital
  - Conexión explícita entre la propuesta y los incidentes críticos del semestre
- **Fuentes:** Mínimo 5, citadas en formato APA 7

---

## Documentos del Proyecto (Referencia Rápida)

| Archivo | Para qué sirve |
|---|---|
| `docs/mvp_strategy.md` | Priorización detallada y tabla de fallbacks |
| `docs/implementation_plan.md` | Arquitectura técnica completa (menú de opciones) |
| `docs/task.md` | Checklist de todas las tareas |
| `README.md` | Documentación pública + cobertura de 7 materias |
| `V2.md` | Datos epidemiológicos clave (cifras y constantes) |
| `M_doc.md` | Protocolo de extracción con URLs verificadas |
