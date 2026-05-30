# AftoSec: Vigilancia Epidemiológica de Precisión para la Ganadería Mexicana
## Artículo de Divulgación Científica — Proyecto "Ganado Saludable"

> **Universidad Nacional "Rosario Castellanos"** | Licenciatura en Ciencias de Datos para Negocios
> **Semestre 2026-1** | Problema Prototípico — 4° Semestre
> **Autores:** Arian Pedroza Celis · Kevin Axel Acosta Ayala · Victoria [Apellido]

---

## 🗺️ GUÍA DE CONTRIBUCIÓN — LEER ANTES DE EDITAR

Este documento está dividido en secciones. Cada sección tiene un **responsable** y una etiqueta de estado:

- `✅ COMPLETADO` — Ya redactado, no modificar sin avisar
- `🔵 PENDIENTE — AXEL` — Tu sección, Axel. Instrucciones abajo del título
- `🟣 PENDIENTE — VICTORIA` — Tu sección, Victoria. Instrucciones abajo del título
- `🔄 REVISIÓN CONJUNTA` — Entre todos al final

**Objetivo:** Tener un borrador completo para el **28 o 29 de mayo**. La presentación es el **6 de junio**.

**¿Dónde encontrar información?**
- Documento técnico principal: `docs/Tercer_avance/tercer_avance.md`
- Innovación Social: `docs/Tercer_avance/Propuesta_innovacionSocial/Actividad_Innovacion_Social_Ganado_Saludable.md`
- Figuras generadas: `docs/figures/` y `data/processed/spatial/charts/`

---

## Resumen Ejecutivo ✅ COMPLETADO

¿Cómo viajan las pandemias animales en un país de 2 millones de kilómetros cuadrados? Esta pregunta guió el desarrollo de **AftoSec**, un sistema integrado que combina ecuaciones diferenciales espaciales, modelos gravitatorios de transporte terrestre, Inteligencia Artificial sobre grafos de carretera y cifrado asimétrico de grado militar para modelar, predecir y contener brotes de Fiebre Aftosa (FMD) en México sin comprometer la privacidad ni el sustento económico de los productores ganaderos.

El resultado: un motor predictivo con R² = 0.8924 que, con solo 13 variables topológicas de la red vial nacional, predice la severidad de un brote en cualquier estado antes de que el primer camión infectado cruce una frontera estatal.

---

## §1. El Problema: Una Bomba de Tiempo de 35 Millones de Cabezas ✅ COMPLETADO — AXEL

Imagina un patógeno tan voraz que puede propagarse con el simple roce del viento o una mota de polvo, infectando hatos enteros en cuestión de horas. Esa es la Fiebre Aftosa (FMD): una de las enfermedades animales más temidas del planeta. En México, este enemigo invisible acecha una de nuestras mayores riquezas nacionales: un hato ganadero que supera las 35.1 millones de cabezas de ganado bovino (según datos oficiales del SIAP 2023). Este gigantesco motor pecuario no solo alimenta a millones de familias, sino que posiciona a nuestro país como uno de los líderes globales en exportación de carne. 

Sin embargo, esta enorme escala nos convierte también en un blanco sumamente vulnerable. No tenemos que adivinar qué pasaría si un brote ingresa a territorio nacional; la historia ya nos ha entregado advertencias devastadoras. El precedente del Reino Unido en 2001 es escalofriante: un brote descontrolado costó más de 8,000 millones de libras esterlinas y obligó a realizar el sacrificio masivo y doloroso de 6 millones de animales, cuyas imágenes de piras de fuego conmocionaron al mundo. 

Para México, la irrupción de la Fiebre Aftosa desataría una catástrofe financiera inmediata. En cuestión de minutos, las fronteras se cerrarían y se decretaría la suspensión absoluta de nuestras exportaciones de carne y ganado en pie hacia mercados clave como Estados Unidos, Japón y la Unión Europea. Las consecuencias económicas se propagarían más rápido que el propio virus, estimando pérdidas globales de hasta $52,800 millones de dólares en solo 150 días. Pero la verdadera tragedia no reside en las frías cifras macroeconómicas, sino en el impacto social. Para el pequeño y mediano ganadero de estados como Jalisco o Veracruz, el cierre del mercado y las medidas sanitarias drásticas se traducirían en una quiebra absoluta e inevitable en un plazo menor a 90 días. En este escenario, la ganadería nacional no solo perdería cabezas de ganado, sino su sustento intergeneracional, su patrimonio y su viabilidad económica en el mediano plazo.

---

## §2. La Física del Contagio: Por Qué los Virus Viajan en Camiones ✅ COMPLETADO

Las vacas no vuelan. En México, el virus de la Fiebre Aftosa no se mueve por el aire entre estados — se mueve a bordo de tráileres ganaderos que recorren las carreteras federales. Para modelar este flujo sin datos privados de facturación, adaptamos la **Ley de Gravitación Universal de Newton** a la economía del transporte pecuario:

```
F_ij = K × (P_i × P_j) / d_ij²
```

Donde el flujo comercial de ganado entre el estado `i` y el estado `j` es proporcional a los inventarios bovinos de ambos estados e inversamente proporcional al cuadrado de la distancia real por carretera — calculada mediante la API pública OSRM (Open Source Routing Machine) para los 32 × 32 = 1,024 pares de estados.

El resultado es un **grafo dirigido** de 32 nodos (estados) y 992 aristas (rutas de comercio) donde cada conexión tiene un peso que representa la probabilidad de que un camión infectado cruce esa frontera estatal. Este mapa de riesgo tiene una precisión que ninguna tabla de Excel podría replicar: captura que Veracruz y Jalisco son "superconectores" no por capricho, sino porque su combinación de masa ganadera gigante y conectividad carretera central los convierte en los multiplicadores sistémicos del riesgo epidémico.

**El hallazgo más contraintuitivo:** el estado más peligroso no es necesariamente el que tiene más vacas. Es el que más *exporta* — el que tiene el mayor `weighted_out_flux`. Un estado como Chiapas, con 2.6M de cabezas, está arrinconado geográficamente y tiene bajo potencial de distribución nacional. Veracruz, con inventario similar, tiene la red vial más conectada del Golfo y puede contaminar al país en 12 días.

---

## §3. La Simulación: 180 Días de Caos Controlado ✅ COMPLETADO

Sobre este grafo de carreteras ejecutamos una **simulación estocástica SIR** (Susceptibles-Infectados-Removidos) durante 180 días. A diferencia del modelo clásico que asume que todas las vacas del país conviven en el mismo campo virtual, nuestro modelo impone fricción geográfica: el virus tiene que "viajar" por las aristas del grafo ponderado por el flujo gravitatorio.

**Diseño Visual de la Epidemia (Estilo *Plague Inc.*):**
El mapa coroplético de la simulación (`data/processed/spatial/fmd_spread_simulation_180d.gif`) traduce el desastre sanitario en colores directos:
*   **Gris Claro (`#e0e0e0`):** Representa las zonas sanas, susceptibles de infección.
*   **Rojo Brillante (`#FF1E1E`):** Marca la irrupción inmediata del brote.
*   **Rojo-Negro Oscuro (`#5C0505`):** Denota la fase avanzada de la epidemia local y el inicio del rifle sanitario constante.
*   **Negro Carbón (`#111111`):** Simboliza que el hato ha sido completamente despoblado o extinguido (pérdidas mayores al 90%).
*   **Marcador Biohazard ☣️:** En el momento exacto en que entra el virus a un estado, aparece y pulsa dinámicamente el icono de peligro biológico en su centroide durante los primeros 6 días del brote local. Veracruz inicia con este marcador en el Día 0, y Jalisco o Puebla lo encienden en cuanto el virus arriba por carretera.

Los resultados desafiaron la intuición inicial:

| Métrica | Modelo Clásico | Modelo Espacial AftoSec | Diferencia |
|---------|---------------|------------------------|------------|
| Pico nacional de infectados | ~17,500,000 | **10,200,000** | -41.7% |
| Día del pico | Día 45 | **Día 58** | +13 días |
| Sacrificio total (Día 180) | N/A | **33,421,804 (96.9%)** | — |
| Estados que sobreviven | 0 de 32 | **5 de 32** | — |

**El dato más valioso** no es el pico reducido: son los **+13 días adicionales** de ventana de contención. La fricción geográfica real da tiempo para intervenir antes del colapso. Esos 13 días son la diferencia entre contener el brote en un estado (costo: ~$2,000M MXN) o enfrentar una pandemia nacional (costo: ~$200,000M MXN).

Además, simulamos tres escenarios de paciente cero para entender cómo el origen del brote cambia el patrón de propagación:

- **Veracruz (El Emisor Masivo):** Explosión sur→norte en 12 días. El peor escenario epidemiológico.
- **Sonora (El Hub Exportador):** Propagación lenta hacia el sur, pero cierre de fronteras con EE.UU. el Día 1. El peor escenario financiero.
- **Puebla (El Puente Topológico):** Distribución radial eficiente en todas direcciones gracias a su altísima centralidad de intermediación en la red vial.

---

## §4. La Inteligencia Artificial: Un FICO Score para el Ganado ✅ COMPLETADO

Correr una simulación de 180 días toma varios segundos de cómputo. En producción, necesitamos una respuesta en milisegundos. Para esto entrenamos un **XGBoost Regressor** — el mismo algoritmo que usan los bancos para evaluar riesgo de crédito, aplicado aquí para evaluar riesgo epidémico.

El modelo toma 13 características topológicas de cada estado en el grafo (PageRank, Betweenness Centrality, flujos gravitatorios, distancias) y predice el pico máximo de infectados sin ejecutar ninguna simulación. Resultado: **R² = 0.8924** en Leave-One-Out Cross-Validation — la metodología más exigente posible para un dataset de 32 muestras.

Benchmarkeamos el modelo contra tres alternativas:

| Modelo | R² (LOOCV) | Veredicto |
|--------|------------|-----------|
| Regresión Lineal Múltiple | 1.0000 | ⚠️ Overfitting severo — memoriza ruido |
| Árbol de Decisión | 0.7601 | Alta varianza, poco confiable |
| Random Forest | 0.8396 | Sólido, pero superable |
| **XGBoost** | **0.8924** | ✅ Ganador: mejor R² y MAE más bajo |

La Regresión Lineal con R² = 1.0 es una trampa clásica: con 13 variables y solo 27 muestras de entrenamiento, el modelo memoriza los datos en lugar de aprender. XGBoost, con su regularización L1/L2, evita este problema.

---

## §5. La Criptografía: El Escudo que Hace Posible el Reporte ✅ COMPLETADO — AXEL

Detrás de cualquier catástrofe epidemiológica casi siempre existe una barrera social invisible: el miedo. Ante una sospecha de Fiebre Aftosa, el ganadero se enfrenta a un dilema ético perverso. Si reporta de inmediato, teme que su predio sea inmediatamente cuarentenado, sus animales sacrificados y su sustento de vida destruido por completo. El resultado histórico de este temor es el silencio absoluto, lo que termina por convertir un brote aislado en una epidemia de proporciones nacionales. 

Para romper este círculo vicioso, en AftoSec diseñamos un escudo de privacidad criptográfico de dos capas que trabaja en conjunto para proteger la identidad del productor, permitiéndole reportar de manera totalmente segura y confidencial. 

La primera capa opera directamente en su teléfono celular mediante una aplicación móvil que utiliza el algoritmo **ChaCha20-Poly1305**. Este módulo actúa como una 'caja fuerte en la palma de la mano': cifra los datos personales (nombre, teléfono y ubicación GPS exacta) *antes* de que la información salga del dispositivo hacia la red. Elegimos ChaCha20 porque es el estándar moderno y ultrarrápido que protege los chats de WhatsApp y la navegación web segura TLS 1.3, funcionando perfectamente incluso en dispositivos de bajo costo en zonas rurales que carecen de chips criptográficos dedicados.

La segunda capa asegura el servidor utilizando la robusta criptografía asimétrica **RSA-2048**. La información viaja encriptada y se almacena en contenedores inescrutables en la base de datos pecuaria, jamás en texto plano. Solo la Comisión oficial (CPA/SENASICA) posee la llave privada exclusiva para abrir esta 'caja fuerte' y descifrar la identidad del ganadero únicamente cuando es indispensable enviar ayuda veterinaria y vacunas al predio. 

Al erradicar el miedo al reporte con matemáticas aplicadas, habilitamos un flujo seguro de alerta temprana. El ganadero reporta sin temores, nuestra inteligencia artificial procesa el riesgo en milisegundos y el hato nacional se salva de una despoblación devastadora.

---

## §6. Innovación Social y Modelación Financiera: Cuando la Tecnología Cambia los Incentivos
### 🟣 PENDIENTE — VICTORIA | Extensión objetivo: ~450 palabras

**Instrucciones para Victoria:**

Esta sección explica el impacto humano, social y financiero-cuantitativo del proyecto. Tú programaste las gráficas comparativas mensuales y diarias, así que en esta sección debes lucir ese análisis que une el **cálculo multivariable/epidemiológico** con las **proyecciones de negocio**.

**Puntos que DEBES cubrir (en orden):**
1. **El dilema ético del ganadero:** ¿reportar o no reportar? Explica el dilema como si fuera una decisión de negocios bajo incertidumbre (miedo a perder su hato por cuarentenas estatales ineficientes).
2. **Las curvas de infectados diarios (Cálculo Multivariable):** Explica la comparación de la **Figura 8** (`docs/figures/fmd_comparativa_diaria.png`). ¿Por qué el modelo clásico homogéneo muestra una explosión exponencial irreal y por qué el modelo espacial gravitatorio aplana la curva? (La geografía actúa como un freno físico/fricción al transporte).
3. **El Flujo de Caja Mensual Acumulado (Proyecciones):** Explica la comparación de la **Figura 9** (`docs/figures/fmd_comparativa_mensual.png`). ¿Por qué en el Mes 1 y 2 el modelo espacial simula pérdidas mucho menores (retraso geográfico) pero al Mes 5 ambos convergen en una catástrofe de **$52,796 MDD**? (El virus eventualmente llega a los nodos superconectores Veracruz/Jalisco si no se contiene a tiempo).
4. **El modelo de adopción y mitigación ambiental:** El modelo en 3 fases para implantar la app y cómo las cuarentenas quirúrgicas de 3 km (en vez del sacrificio masivo) reducen el impacto ambiental.

**¿De dónde sacar la info?**
- Lee completo el documento que tú trabajaste: `src/models/fmd_finance_comparison.py` (tus ecuaciones de flujo de caja).
- Lee la Sección **5.3** de `docs/Tercer_avance/tercer_avance.md` — ahí redacté la explicación de tus dos gráficas para la parte técnica.
- Lee `docs/Tercer_avance/Propuesta_innovacionSocial/Actividad_Innovacion_Social_Ganado_Saludable.md` Secciones 2 y 6 para la parte de dilema ético e impacto ambiental.

**Tono:** Profesional, combinando negocios y modelación cuantitativa.

```
[ESCRIBE AQUÍ — ~450 palabras]
```

---

## §7. Conclusión: Datos que Salvan Industrias
### 🔄 REVISIÓN CONJUNTA — Un párrafo de cada quien

**Instrucciones:** Cada miembro del equipo escribe 2–3 oraciones respondiendo: *"¿Qué aprendiste de este proyecto que no sabías antes?"* Sé honesto, no tiene que ser técnico.

**Arian:**
```
[Tu cierre aquí]
```

**Axel:**
```
Este proyecto me demostró que la seguridad de los datos no es un concepto puramente matemático u abstracto, sino una herramienta fundamental para construir confianza humana en el mundo real. Al aplicar criptografía simétrica y asimétrica de vanguardia en el sector pecuario, entendí cómo la privacidad puede transformar el temor de un ganadero en colaboración activa, logrando así que toda la modelación epidemiológica y de inteligencia artificial sea viable y efectiva para proteger nuestra economía nacional.
```

**Victoria:**
```
[Tu cierre aquí — 2-3 oraciones. Enfoque: Qué aprendiste sobre modelación financiera y cómo el modelado estocástico espacial multivariable en grafos cambia por completo las proyecciones estáticas del segundo avance.]
```

*Cierre editorial (a completar entre todos después de leer los tres):*
```
[Párrafo de cierre unificado — lo redactamos juntos en el meet]
```

---

## §8. Referencias (Formato APA 7) ✅ COMPLETADO

- Anderson, I. (2002). *Foot and Mouth Disease 2001: Lessons to be Learned Inquiry Report*. The Stationery Office.
- Brauer, F., & Castillo-Chávez, C. (2012). *Mathematical Models in Population Biology and Epidemiology* (2nd ed.). Springer. https://doi.org/10.1007/978-1-4614-1686-9
- Kermack, W. O., & McKendrick, A. G. (1927). A contribution to the mathematical theory of epidemics. *Proceedings of the Royal Society of London A, 115*(772), 700–721. https://doi.org/10.1098/rspa.1927.0118
- Knight-Jones, T. J. D., & Rushton, J. (2013). The economic impacts of foot and mouth disease. *Preventive Veterinary Medicine, 112*(3–4), 161–173. https://doi.org/10.1016/j.prevetmed.2013.06.013
- OIE/WOAH. (2023). *Manual of Diagnostic Tests and Vaccines for Terrestrial Animals — Chapter 3.1.8: Foot and Mouth Disease*. World Organisation for Animal Health.
- SIAP. (2024). *Panorama Agroalimentario 2024*. Servicio de Información Agroalimentaria y Pesquera, SADER. https://www.gob.mx/siap
- Tildesley, M. J., Savill, N. J., Shaw, D. J., Deardon, R., Brooks, S. P., Woolhouse, M. E. J., Grenfell, B. T., & Keeling, M. J. (2006). Optimal reactive vaccination strategies for a foot-and-mouth outbreak in the UK. *Nature, 440*(7080), 83–86. https://doi.org/10.1038/nature04324
- USDA ERS. (2024). *Mexico Livestock and Products Annual*. United States Department of Agriculture. https://fas.usda.gov/data/mexico-livestock-and-products-annual-2024

---

| Sección | Responsable | Estado | Fecha límite |
|---------|-------------|--------|-------------|
| §1 El Problema | **Axel** | ✅ Listo | — |
| §2 La Red Vial | Arian | ✅ Listo | — |
| §3 La Simulación | Arian | ✅ Listo | — |
| §4 La IA y Benchmark | Arian | ✅ Listo | — |
| §5 La Criptografía | **Axel** | ✅ Listo | — |
| §6 Innovación Social | **Victoria** | ⬜ Pendiente | 29/05 |
| §7 Conclusión (c/u) | **Todos** | ⏳ En curso | 29/05 |
| §8 Referencias | Arian | ✅ Listo | — |
| Revisión final | Arian | ⬜ 30/05 | 30/05 |

---

## 🔧 GUÍA DE SINCRONIZACIÓN GIT (Axel y Victoria: leer esto antes de editar)

Antes de ponerte a escribir tu sección, sincroniza tu copia local con los avances que ya subimos. Son 2 comandos:

```bash
# 1. Baja los últimos cambios del repo (incluyendo el trabajo de tu simulación de app, Axel)
git pull origin main

# 2. Verifica que tienes los archivos nuevos
git log --oneline -5
```

Si ves el commit `feat(crypto): integrate ChaCha20-Poly1305 mobile simulator` en el log, estás al día.

**¿Qué leer según tu sección?**

| Quién | Archivos que TE conciernen | Qué ignorar |
|-------|---------------------------|-------------|
| **Axel (§1 + §5)** | `docs/Tercer_avance/tercer_avance.md` Secc. 2.1, 5.2, 8, 9.1 · `src/crypto/mock_mobile_app.py` · `docs/explicacion_matematica_chacha20.md` | Todo `src/spatial_model/`, todo `src/models/`, los notebooks |
| **Victoria (§6)** | `docs/Tercer_avance/Propuesta_innovacionSocial/Actividad_Innovacion_Social_Ganado_Saludable.md` (completo) · Secc. 5.3 y 9.3 de `tercer_avance.md` · `src/models/fmd_finance_comparison.py` | Todo el código de machine learning / XGBoost y notebooks |

**Para subir tu borrador:**
```bash
# Cuando termines de escribir en este archivo, sólo haz:
git add docs/articulo_divulgacion_final.md
git commit -m "docs(articulo): borrador §[TU NUMERO] — [tu nombre]"
git push origin main
```

Si hay conflicto (poco probable pero posible si los dos editan al mismo tiempo), avisen a Arian por WhatsApp antes de hacer push.

---

## ⚖️ §9. Propiedad Intelectual y Cláusula de Licencia

Este desarrollo (código fuente de la simulación, modelos de machine learning XGBoost, algoritmos de ruteo y fricción vial OSRM, simuladores de criptografía ChaCha20/RSA y documentación asociada) es propiedad intelectual colectiva de sus autores bajo la legislación mexicana vigente de derechos de autor (Ley Federal del Derecho de Autor - LFDA).

Se prohíbe la reproducción parcial o total, distribución comercial, ingeniería inversa o uso de la metodología para proyectos ajenos a esta institución sin el consentimiento expreso y por escrito de los titulares de la autoría.
© 2026 Arian Pedroza Celis, Kevin Axel Acosta Ayala, Victoria Montserrat Enriquez. Todos los derechos reservados.
