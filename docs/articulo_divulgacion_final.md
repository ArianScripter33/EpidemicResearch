# AftoSec: Vigilancia Epidemiológica de Precisión para la Ganadería Mexicana
## Artículo de Divulgación Científica — Proyecto "Ganado Saludable"

> **Universidad Nacional "Rosario Castellanos"** | Licenciatura en Ciencias de Datos para Negocios
> **Semestre 2026-1** | Problema Prototípico — 4° Semestre
> **Autores:** Arian Pedroza Celis · Axel [Apellido] · Victoria [Apellido]

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

## §1. El Problema: Una Bomba de Tiempo de 35 Millones de Cabezas
### 🔵 PENDIENTE — AXEL | Extensión objetivo: ~350 palabras

**Instrucciones para Axel:**

Redacta esta sección explicando el problema de la Fiebre Aftosa en México para un lector que no sabe nada del tema. Tu objetivo es que al terminar de leer, el lector entienda POR QUÉ esto es urgente.

**Puntos que DEBES cubrir (en este orden):**
1. ¿Qué es la Fiebre Aftosa y por qué es tan contagiosa? (Una oración poderosa de apertura)
2. El tamaño del hato nacional: 35.1 millones de cabezas bovinas (fuente: SIAP 2023)
3. El precedente histórico: el brote del Reino Unido en 2001 costó más de 8,000 millones de libras y el sacrificio de 6 millones de animales
4. El riesgo para México: cierre inmediato de exportaciones a EE.UU., Japón y la UE
5. El impacto en el pequeño ganadero: quiebra en menos de 90 días

**¿De dónde sacar la info?**
- Lee la Sección 2.1 de `docs/Tercer_avance/tercer_avance.md` — ahí está el contexto del modelo base
- El dato de impacto económico de $52,800M USD está en la Sección 5.2
- Para el contexto de FMD global: busca "FMD 2001 UK outbreak economic impact" en Google

**Tono:** Periodístico, como un artículo de Expansión o El Financiero. Primera persona del plural ("encontramos", "nuestro sistema").

```
[ESCRIBE AQUÍ — ~350 palabras]
```

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

Los resultados desafiaron la intuición inicial:

| Métrica | Modelo Clásico | Modelo Espacial AftoSec | Diferencia |
|---------|---------------|------------------------|------------|
| Pico nacional de infectados | ~17,000,000 | **10,200,000** | -40% |
| Día del pico | ~45 | **58** | +13 días |
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

## §5. La Criptografía: El Escudo que Hace Posible el Reporte
### 🔵 PENDIENTE — AXEL | Extensión objetivo: ~300 palabras

**Instrucciones para Axel:**

Esta sección es tuya porque tú trabajaste en los dos módulos de encriptación. Explícale a alguien que nunca ha escuchado de criptografía cómo funciona nuestro sistema y POR QUÉ es necesario.

**Puntos que DEBES cubrir:**
1. El problema: ¿por qué el ganadero NO reporta? (Miedo a perder su rancho)
2. La solución: **dos capas de cifrado** que trabajan en conjunto:
   - **App móvil (tu trabajo → ChaCha20-Poly1305):** El formulario del ganadero cifra sus datos personales en el teléfono *antes* de mandarlo al servidor. Usa análoga de "caja fuerte en la palma de la mano". Menciona que usaste ChaCha20 porque es el cifrado que usa WhatsApp y TLS 1.3 en dispositivos sin chip especializado.
   - **Servidor (RSA-2048 + bcrypt):** Los datos viajan cifrados y nunca se guardan en texto plano. Solo la CPA tiene la llave para descifrarlos.
3. El resultado: el ganadero reporta sin miedo → la IA recibe el dato → salva el hato nacional

**IMPORTANTE:** NO menciones el cifrado César en la redacción final del artículo. Nuestro sistema de producción usa ChaCha20 (móvil) + RSA-2048 (servidor), que son los estándares de la industria.

**¿De dónde sacar la info?**
- Sección **8.3** de `docs/Tercer_avance/tercer_avance.md` — la tabla de ChaCha20 vs RSA es tuya
- Sección 9.1 del mismo documento (el Dilema Ético del ganadero)
- Tu script `src/crypto/mock_mobile_app.py` — ya lo integramos a `main`, úsalo como referencia de lo que hiciste

**Tono:** Claro, accesible. Usa analogías del mundo físico (candados, cajas fuertes, llaves).

```
[ESCRIBE AQUÍ — ~300 palabras]
```

---

## §6. Innovación Social: Cuando la Tecnología Cambia los Incentivos
### 🟣 PENDIENTE — VICTORIA | Extensión objetivo: ~350 palabras

**Instrucciones para Victoria:**

Esta sección explica el impacto humano y social del proyecto. NO necesitas entender código para escribirla — es la más cercana a ciencias sociales y negocios.

**Puntos que DEBES cubrir (en orden):**
1. El dilema ético del ganadero: ¿reportar o no reportar? Explica el dilema como si fuera una decisión de negocios bajo incertidumbre
2. Quiénes son los beneficiados directos e indirectos (usa la tabla de actores)
3. El modelo de adopción en 3 fases (Piloto → Regional → Nacional)
4. El impacto ambiental: cuarentenas quirúrgicas de 3 km vs. sacrificio estatal masivo → -40% de carcasas
5. Cierra con por qué esto conecta con ODS 2 (Hambre Cero) y ODS 3 (Salud)

**¿De dónde sacar la info?**
- Lee COMPLETO: `docs/Tercer_avance/Propuesta_innovacionSocial/Actividad_Innovacion_Social_Ganado_Saludable.md`
- Enfócate en las secciones 2, 6 y 8 de ese documento
- La tabla de actores está en la Sección 9.3 de `tercer_avance.md`

**Tono:** Empático y orientado a personas. Habla del "ganadero Don Aurelio" como personaje (ya está en el código del demo). Conecta la tecnología con el impacto humano real.

```
[ESCRIBE AQUÍ — ~350 palabras]
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
[Tu cierre aquí — 2-3 oraciones]
```

**Victoria:**
```
[Tu cierre aquí — 2-3 oraciones]
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

## ✅ Checklist de Entrega

| Sección | Responsable | Estado | Fecha límite |
|---------|-------------|--------|-------------|
| §1 El Problema | **Axel** | ⬜ Pendiente | 28/05 |
| §2 La Red Vial | Arian | ✅ Listo | — |
| §3 La Simulación | Arian | ✅ Listo | — |
| §4 La IA y Benchmark | Arian | ✅ Listo | — |
| §5 La Criptografía | **Axel** | ⬜ Pendiente | 28/05 |
| §6 Innovación Social | **Victoria** | ⬜ Pendiente | 29/05 |
| §7 Conclusión (c/u) | **Todos** | ⬜ Pendiente | 29/05 |
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
| **Victoria (§6)** | `docs/Tercer_avance/Propuesta_innovacionSocial/Actividad_Innovacion_Social_Ganado_Saludable.md` (completo) · Secc. 9.3 de `tercer_avance.md` | Todo el código Python, los JSON, los CSV |

**Para subir tu borrador:**
```bash
# Cuando termines de escribir en este archivo, sólo haz:
git add docs/articulo_divulgacion_final.md
git commit -m "docs(articulo): borrador §[TU NUMERO] — [tu nombre]"
git push origin main
```

Si hay conflicto (poco probable pero posible si los dos editan al mismo tiempo), avisen a Arian por WhatsApp antes de hacer push.
