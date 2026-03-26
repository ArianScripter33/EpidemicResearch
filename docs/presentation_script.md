# 🐄 Ganado Saludable: Guion de Presentación (Coloquio)

> **Bioseguridad Inteligente frente al Bioterrorismo Corporativo**
> Detección Temprana, Ciencia de Datos y el Paradigma "One Health"

---

## ACTO I: El Espejismo de la Seguridad y los "Reactores Biológicos" (El Gancho)

**Narrativa:**
México ha estado libre de la Fiebre Aftosa (FMD) desde 1954. Esta aparente victoria nos ha vuelto ciegos ante un peligro inminente. Hoy en día, los 2.8 millones de bovinos que ingresan anualmente a los corrales de engorda intensiva (CAFOs) en nuestro país ya no son solo centros de producción de carne; se han convertido en auténticos **"vasos de mezcla" o reactores biológicos**.

Las condiciones de hacinamiento extremo, el amoníaco que quema los tractos respiratorios y el abuso de antibióticos obligan a virus y bacterias a mutar violentamente. El Dr. Michael Greger advierte que estas instalaciones son fábricas de patógenos letales, comparables con agentes de **bioterrorismo** (como ocurrió con el virus Nipah en granjas de cerdos). Sin embargo, la industria mantiene esto oculto mediante un **"corporativismo defensivo"**, negándose a revelar qué y cuánto inyectan a los animales para evitar sanciones comerciales.

**El Problema Prototípico:** ¿Cómo podemos, como científicos de datos, penetrar esta barrera de opacidad y crear un sistema de alerta temprana que proteja las 35.1 millones de cabezas de ganado en México y, en consecuencia, la salud humana y la economía nacional?

---

## ACTO II: La Estrategia del "Proxy" (Explicación Metodológica)

**Narrativa Didáctica:**
Como no tenemos datos recientes de Fiebre Aftosa en México, los algoritmos estarían "ciegos". Para resolverlo, diseñamos una arquitectura **Dual-Path** usando *Transfer Learning* y *Proxies*:

1. **El Proxy Epidemiológico (Tuberculosis Bovina):** Calibraremos nuestros modelos con los datos reales de cuarentenas y gasto estatal del SENASICA para Tuberculosis Bovina (una enfermedad endémica y crónica con R0 ≈ 1.8), y luego transferimos esos parámetros al escenario catastrófico de FMD (R0 ≈ 6.0).

2. **El Proxy de Opacidad (Clenbuterol como indicador de abuso antibiótico):** Como la industria oculta el abuso de antibióticos, haremos minería de datos en la Plataforma Nacional de Transparencia (PNT/INAI) buscando clausuras por *Clenbuterol* y *Límites Máximos de Residuos (LMR)*. **Quien viola la ley usando Clenbuterol tiene una probabilidad casi absoluta de abusar de antibióticos** — el clembuterol es la punta visible del iceberg de la opacidad.

> **Nota:** Este concepto de "Proxy de Opacidad" es una contribución original del equipo. Las clausuras por clembuterol son datos públicos (PNT); el abuso de antibióticos no lo es. Al usar uno como predictor del otro, estamos haciendo ingeniería de features con creatividad metodológica.

---

## ACTO III: Arquitectura de la Solución (Integración de las 7 Asignaturas)

*Aquí demostramos al jurado cómo se resuelve el Problema Prototípico aplicando cada materia.*

### 1. 🔐 Fundamentos de Criptografía: Blindando la Verdad

* **El Reto:** Un competidor desleal interviene nuestros sensores IoT para inyectar datos falsos de temperatura, buscando enmascarar un brote y arruinar a "Carnes Selectas Mexicanas".
* **El Método:** Aplicaremos **Cifrado César** (ej. "LOTE" → "ORWH" con desplazamiento 3) para ofuscar identificadores rápidos, pero el núcleo será la **criptografía asimétrica (RSA)** con funciones *hash* (SHA-256).
* **Resultado:** Cada sensor firmará digitalmente su lectura. La manipulación de datos se vuelve criptográficamente imposible de ocultar.
* **Entregable:** `src/crypto/encryption.py` — código funcional con demo interactiva.

### 2. 🗄️ Bases de Datos NoSQL: Escalabilidad ante el Caos

* **El Reto:** Un brote explosivo genera un tsunami de datos: lecturas IoT por segundo mezcladas con PDFs de cuarentenas del gobierno no estructurados.
* **El Método:** Implementaremos **MongoDB** con un diseño *Star Schema* adaptado a documentos BSON (embedding de dimensiones frecuentes).
* **Resultado:** Consultas geoespaciales complejas (estado → hatos → casos humanos) optimizadas. Almacenamiento de datos no estructurados (actas PNT en texto libre) con índices de texto completo.
* **Entregable:** `src/warehouse/nosql_client.py` + colecciones MongoDB documentadas.

### 3. 📊 Estadística Multivariada: El Rostro de la Crisis

* **El Reto:** Comprender la correlación entre decenas de variables (clima, densidad de ganado, clausuras y prevalencia de patógenos).
* **El Método:** **PCA** para reducir dimensionalidad + **Caras de Chernoff** para mapear visualmente el perfil de riesgo de los 32 estados + **ANOVA** para probar diferencia estadística entre canales de venta.
* **Resultado:** Demostraremos que comprar carne en un mercado municipal (22.3% de contaminación por *Salmonella*) tiene un riesgo estadísticamente superior al supermercado (1.3%).
* **Entregable:** Notebooks con 32 Caras de Chernoff + Curvas de Andrews + tablas PCA.

### 4. 🤖 Inteligencia Artificial: El Oráculo Predictivo

* **El Reto:** Predecir un brote antes de que haya síntomas clínicos o decomisos masivos.
* **El Método:** **XGBoost Classifier** entrenado con datos ruidosos y desbalanceados (SMOTE). Target: casos CIE-10 A05 (intoxicación alimentaria). Features incluyen el **proxy de clembuterol** como indicador de bioseguridad deficiente.
* **Resultado:** Sistema de alerta temprana. SHAP values revelarán que la falla en bioseguridad en rastros es el factor predictivo #1.
* **Entregable:** `src/models/xgboost_prep.py` + modelo entrenado + métricas AUC-ROC.

### 5. 📐 Ecuaciones Diferenciales Aplicadas: Modelando la Catástrofe

* **El Reto:** Cuantificar el impacto temporal de la Fiebre Aftosa frente a una respuesta gubernamental lenta.
* **El Método:** **Sistema SIR dual** (Susceptibles, Infectados, Recuperados) de EDOs resuelto con Runge-Kutta (`scipy.integrate.odeint`).
* **Resultado:** Las curvas de fase prueban que mientras la TB (R0=1.8) infecta al 12% del hato en 5 años, la FMD (R0=6.0) infectaría al **80% del hato nacional en solo 45 días**. Retrasar la cuarentena 48 horas = perder el control del país.
* **Entregable:** `src/models/sir_prep.py` + 6 escenarios + gráficas comparativas TB vs FMD.

### 6. 💰 Finanzas Corporativas: El Valor Presente de la Supervivencia

* **El Reto:** Convencer a la junta directiva de que el sistema IoT no es un gasto, sino un escudo financiero.
* **El Método:** Análisis de **VPN** y **ROI**. Análisis DuPont. Razones financieras.
* **Resultado:** $5M MXN de sistema preventivo vs $200B MXN de un brote FMD tipo UK 2001. El ROI de la prevención es infinito cuando se trata de evitar la quiebra.
* **Entregable:** `src/models/financial_roi.py` + tabla comparativa TB crónico vs FMD catastrófico.

### 7. 🌍 Laboratorio de Innovación Social: *One Health*

* **El Reto:** Evaluar el impacto ético y social de la propuesta.
* **El Método:** Paradigma "Una Sola Salud" (*One Health*) de la OMS/FAO/WOAH. Mapa de stakeholders. Análisis de inequidad.
* **Resultado:** Las superbacterias (94.7% resistencia a ampicilina) forjadas en corrales industriales terminan en los tianguis de comunidades rurales marginadas. Nuestro proyecto democratiza la bioseguridad.
* **Entregable:** Diagrama sistémico + mapa de actores + sección de impacto social en el artículo.

---

## ACTO IV: Conclusión y Entregables (El Cierre)

**Narrativa:**
Nuestro artículo de divulgación y los dashboards interactivos probarán una premisa innegable que cumple con el objetivo de nuestra Licenciatura en Ciencias de Datos para Negocios:

> **"En la era de los virus pandémicos y la resistencia a los antibióticos, la verdadera innovación no es simplemente poner sensores en las vacas. Es utilizar las matemáticas, la criptografía y la inteligencia artificial para hacer visibles las cadenas de transmisión que un sistema fragmentado y corporativo intenta ocultar."**

La bioseguridad basada en datos no es un lujo; es nuestra única estrategia de supervivencia económica y sanitaria.

---

## Notas de Diseño para la Presentación

- **Formato sugerido:** Gamma o Genially (requerido por PP)
- **Duración:** Asignada por el comité organizador
- **Requisitos PP:**
  - Participación equitativa de todas las personas del equipo
  - Lenguaje claro, inclusivo y con argumentos sólidos
  - Apoyo visual mediante la presentación digital
  - Conexión explícita entre la propuesta y los incidentes críticos del semestre
- **Fuentes:** Mínimo 5, citadas en formato APA 7
