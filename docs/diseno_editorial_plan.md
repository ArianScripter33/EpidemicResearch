# 🎨 Plan de Diseño Editorial y Dirección de Arte — AftoSec Revista de Divulgación

Este documento establece las directrices estéticas, el mapa de maquetación y la estrategia de diseño gráfico para transformar el **Artículo de Divulgación Científica de AftoSec** de un documento plano de texto a una publicación premium con calidad de **Revista de Divulgación Científica Internacional**.

Nos inspiraremos en el estilo visual híbrido de **Nature Editorial** (rigor, autoridad, precisión y tablas densas) y **MIT Technology Review** (diseño tecnológico contemporáneo, tipografías geométricas, citas destacadas de alto impacto y paletas cromáticas profundas).

---

## 🎨 1. Eje Cromático y Paleta de Identidad UNRC

Para garantizar la coherencia visual con la Universidad Nacional "Rosario Castellanos" y un look premium de negocios pecuarios, utilizaremos la siguiente paleta cromática estructurada:

| Color | Token Hex | Rol en la Revista | Sensación Psicológica |
|---|---|---|---|
| **Fondo Crema** | `#F8F4F0` | Fondo principal de las páginas. Evita el "blanco de oficina" plano y da una textura cálida de papel editorial. | Elegancia, prestigio, lectura descansada. |
| **Gris Carbón** | `#1A1A2E` | Tipografía principal, títulos y bordes gruesos estructurales. | Rigor técnico, modernidad de datos. |
| **Carmesí UNRC** | `#9C223F` | Color de énfasis principal. Encabezados de sección, números de página, bordes de llamadas (*pull quotes*) y curvas clásicas. | Urgencia biológica, alerta epidemiológica. |
| **Dorado Arena** | `#C9A84C` | Destacados numéricos, curvas espaciales, KPIs financieros y bordes de infoboxes. | Valor comercial, riqueza del hato, precisión. |

---

## ✍️ 2. Tipografía y Jerarquía Visual

Para lograr el look híbrido entre ciencia y tecnología, utilizaremos una combinación de dos familias tipográficas:

1.  **Títulos y Subtítulos (Sans-Serif - Estilo MIT Tech Review):** `Inter`, `Outfit` o `Helvetica Neue`. Trazos gruesos, limpios y de alta legibilidad para dar un aspecto tecnológico e ingenieril.
2.  **Cuerpo del Texto (Serif - Estilo Nature):** `Georgia` o `Garamond`. Facilita la lectura de párrafos extensos y le da peso académico y formal a la redacción técnica.

### Jerarquía de Tamaños (Puntos):
*   **Título Principal (Portada):** 28pt | Semibold | Carbón
*   **Encabezados de Sección (§):** 18pt | Bold | Carmesí
*   **Subencabezados:** 14pt | Medium | Carbón
*   **Cuerpo del Texto:** 11pt | Regular | Carbón | Espaciado de línea: 1.15
*   **Llamadas y Citas Destacadas:** 13pt | Italic | Carmesí/Dorado
*   **Pies de Página / Citas en margen:** 8.5pt | Regular | Gris medio

---

## 🖼️ 3. Elementos Ornamentales y Funcionales (Maquetación)

Una revista de divulgación no es un informe aburrido; debe guiar el ojo del lector usando elementos gráficos que organicen la información:

### 3.1 Citas Destacadas (Pull Quotes)
Textos cortos y potentes flotando en la diagramación o centrados con bordes Carmesí de **3pt** a la izquierda.
*   *Destacado 1 (Sección §1):*
    > **"Un brote de Fiebre Aftosa en México no es una simple crisis de salud animal; es la parálisis instantánea de un motor exportador de 3,000 millones de dólares anuales."**
*   *Destacado 2 (Sección §5):*
    > **"La innovación social no es el algoritmo. Es el diseño criptográfico que neutraliza el temor del ganadero, convirtiendo el reporte temprano en un escudo colectivo."**

### 3.2 Cuadros de Información Técnica (Infoboxes / Sidebars)
Cajas de texto flotantes con fondo Dorado muy claro (`#FFFDF9`) y bordes dorados delgados (`1.5pt`), diseñadas para albergar tecnicismos que no deben interrumpir el flujo principal:
*   *Infobox Criptográfico:* Explicación matemática del paso Quarter-Round de **ChaCha20** (álgebra modular, sumas y rotaciones).
*   *Infobox de Machine Learning:* Detalle técnico de la regularización L1/L2 en **XGBoost** para combatir el sobreajuste de 13 variables.

### 3.3 Iconografía Minimalista
Utilizaremos iconos vectoriales elegantes (o caracteres Unicode premium) al inicio de cada sección:
*   🗺️ **§2. La Red Vial:** Un icono de nodos de red en dorado.
*   ☣️ **§3. La Simulación:** Un icono de alerta biológica o propagación de virus.
*   🤖 **§4. La Inteligencia Artificial:** Un icono de engranes o nodos neuronales en gris oscuro.
*   🔑 **§5. La Criptografía:** Un candado o llave en carmesí.
*   📈 **§6. La Modelación Financiera:** Una barra de flujo de caja en dorado.

---

## 📚 4. Mecanismo de Pies de Página (Footnotes Map)

Para materializar tu excelente propuesta de **Mapa de Respaldo Cita-Dato**, configuraremos la inyección en Word/PDF de forma que cada cita APA 7 en el texto tenga un pie de página aclaratorio que actúe como un "metadato explicativo":

```
[Texto en el Artículo] 
"...el hato pecuario nacional estimado en 35.1 millones de cabezas[1]..."

[Pie de Página Resultante]
1. SIAP/SADER (2023). Censo Pecuario Nacional de Bovinos. El dato representa la biomasa susceptible inicial utilizada como parámetro de población constante (N) en la formulación de los 32 nodos del modelo SIR.
```

### Mapa de Pies de Página Críticos:
1.  **Cita de Knight-Jones [5]** $\rightarrow$ *Pie de página:* Explica cómo el cálculo de pérdida de **$52,796 MDD** se deriva de la tasa diaria de pérdida por exportaciones de $8.2M USD y el costo de sacrificio sanitario.
2.  **Cita de ChaCha20 RFC 8439 [8]** $\rightarrow$ *Pie de página:* Explica que la elección del algoritmo de flujo se debe al bajo consumo de CPU en procesadores móviles antiguos en zonas rurales sin soporte criptográfico de hardware.
3.  **Cita de Tildesley [3]** $\rightarrow$ *Pie de página:* Justifica que la reducción a cercos quirúrgicos de 3 km mediante buffers GeoJSON evita la matanza masiva innecesaria de ganado y ahorra un 40% de carcasas biológicas frente al modelo estatal de la DINESA.

---

## 🎨 5. Plan de Generación de Ilustraciones Editoriales (IA Prompts)

Para evitar placeholders y dotar a la revista de imágenes realistas y soberbias, utilizaremos los siguientes prompts estructurados en el generador de imágenes:

### 🖼️ Ilustración 1: La Interfaz de la App en el Campo
*   **Prompt:** `Minimalist editorial UI mockup of a clean mobile application interface on a smartphone screen, held in a hand, showing veterinary diagnostic inputs and encrypted safety icons. Soft sunlight, Mexican cattle ranch background out of focus, professional corporate color palette (burgundy, cream, slate grey), high-end photography for Nature magazine, realistic, clean design, no text distortions --ar 16:9`

### 🖼️ Ilustración 2: El Grafo de Conectividad Nacional
*   **Prompt:** `High-tech minimal network graph visualization overlaying a abstract vector map of Mexico. Highway corridors highlighted as glowing thin lines, nodes representing major livestock hubs in Jalisco and Veracruz as elegant golden data points. Clean design, scientific infographic style, editorial layout, dark navy and crimson accents, premium Tech Review aesthetic --ar 16:9`

---

## 🛠️ 6. Próximo Paso en el Entregable Word/PDF

Utilizando tu script de Node.js `generate_docx_v2.js` y la **Skill de Docx**, aplicaremos este mapa de estilos inyectando:
1.  Bordes de párrafo de color Carmesí para las citas destacadas.
2.  Tabla estilizada de dos colores (crema y carmesí) para los benchmarks del XGBoost.
3.  Inyección de footnotes dinámicos mapeando las fuentes directamente desde `docs/bibliografia_maestra.md`.
