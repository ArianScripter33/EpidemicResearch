# 📚 Bibliografía Maestra y Mapa de Linaje Cita-Dato — AftoSec

Este documento constituye la **fuente única de verdad bibliográfica (APA 7ª edición)** para el proyecto **AftoSec (Ganado Saludable)** a lo largo de todo el semestre (Avances 1, 2 y 3). 

Asocia cada referencia teórica y oficial con los datos específicos, constantes financieras o lógicas matemáticas que respaldan dentro de los entregables y scripts de producción.

---

## 🌎 1. Eje: Epidemiología Matemática y Simulación SIR

### [1] Kermack, W. O., & McKendrick, A. G. (1927). A contribution to the mathematical theory of epidemics. *Proceedings of the Royal Society of London A*, 115(772), 700–721. https://doi.org/10.1098/rspa.1927.0118
*   **Dato/Parámetro que respalda:** Ecuaciones diferenciales continuas del modelo SIR base:
    $$\frac{dS}{dt} = -\beta \frac{S I}{N}, \quad \frac{dI}{dt} = \beta \frac{S I}{N} - \gamma I, \quad \frac{dR}{dt} = \gamma I$$
*   **Uso en el Proyecto:** Base matemática para la simulación del modelo homogéneo clásico.
*   **Uso en Código:** `src/models/sir_dual.py` (Líneas 35-52) y `src/models/fmd_finance_comparison.py` (Líneas 34-53).

### [2] Brauer, F., & Castillo-Chávez, C. (2012). *Mathematical Models in Population Biology and Epidemiology* (2nd ed.). Springer. https://doi.org/10.1007/978-1-4614-1686-9
*   **Dato/Parámetro que respalda:** Definición matemática de la Razón Reproductiva Básica ($R_0$) y el umbral de inmunidad de hato ($H_I = 1 - 1/R_0$).
*   **Uso en el Proyecto:** Justificación teórica de por qué la Tuberculosis Bovina tiene un $R_0 \approx 1.8$ (baja velocidad, endémica) y la Fiebre Aftosa un $R_0 \approx 6.0$ (explosión epidémica).
*   **Uso en Documento:** `docs/Tercer_avance/tercer_avance.md` (Sección 2.1 - Fundamento Biológico).

### [3] Tildesley, M. J., Savill, N. J., Shaw, D. J., Deardon, R., Brooks, S. P., Woolhouse, M. E. J., Grenfell, B. T., & Keeling, M. J. (2006). Optimal reactive vaccination strategies for a foot-and-mouth outbreak in the UK. *Nature*, 440(7080), 83–86. https://doi.org/10.1038/nature04324
*   **Dato/Parámetro que respalda:** Eficacia de las cuarentenas y cercos sanitarios reactivos limitados. Justifica el **buffer circular de 3 km de radio** para contener brotes localizados de Fiebre Aftosa.
*   **Uso en el Proyecto:** Soporte para la propuesta de Innovación Social y Mitigación Ambiental (cuarentenas quirúrgicas vs. sacrificios masivos estatales).
*   **Uso en Documento:** `docs/Tercer_avance/Propuesta_innovacionSocial/Actividad_Innovacion_Social_Ganado_Saludable.md` (Sección 3 - Mitigación).

### [4] Barlow, N. D. (1991). A spatially aggregated disease/host model for bovine Tb in New Zealand possum populations. *Journal of Applied Ecology*, 28(3), 777–793. https://doi.org/10.2307/2404221
*   **Dato/Parámetro que respalda:** Dinámica de agregación espacial y uso de la Tuberculosis Bovina (TB) como un proxy de calibración biológica lenta.
*   **Uso en el Proyecto:** Justifica metodológicamente el uso de una enfermedad endémica local en México para calibrar el software antes de simular una enfermedad exótica (FMD).
*   **Uso en Documento:** `docs/Segundo_avance/teoria_modelo_sir.md`.

---

## 💸 2. Eje: Economía y Finanzas Pecuarias

### [5] Knight-Jones, T. J. D., & Rushton, J. (2013). The economic impacts of foot and mouth disease. *Preventive Veterinary Medicine*, 112(3–4), 161–173. https://doi.org/10.1016/j.prevetmed.2013.06.013
*   **Dato/Parámetro que respalda:** La pérdida promedio mundial por el cierre inmediato de exportaciones en países libres de vacunación y el costo global estimado de **$52,800 millones de USD** en un brote nacional en México.
*   **Uso en el Proyecto:** Soporte macroeconómico de las proyecciones a 150 días en el modelo financiero espacial.
*   **Uso en Documento:** `docs/Tercer_avance/tercer_avance.md` (Sección 6.2) y `docs/articulo_divulgacion_final.md` (§6).
*   **Uso en Código:** `src/models/fmd_finance_spatial.py` (Línea 27: `EXPORT_DIARIO_MAX = 8_200_000`).

### [6] Anderson, I. (2002). *Foot and Mouth Disease 2001: Lessons to be Learned Inquiry Report*. The Stationery Office.
*   **Dato/Parámetro que respalda:** Precedente histórico del brote del Reino Unido en 2001: pérdida de **8,000 millones de libras esterlinas** y el sacrificio obligatorio de **6 millones de cabezas de ganado**.
*   **Uso en el Proyecto:** Justificación del riesgo por inacción y calibración del costo de detección tardía en el análisis de ROI contrafactual.
*   **Uso en Documento:** `docs/articulo_divulgacion_final.md` (§1. El Problema).

### [7] Rahman, M. A., & Samad, M. A. (2009). Effect of bovine tuberculosis on milk production. *Bangladesh Journal of Veterinary Medicine*, 7(2), 287–290. https://doi.org/10.3329/bjvm.v7i2.5615
*   **Dato/Parámetro que respalda:** Disminución del 10–20% en la producción láctea y pérdida de peso del 15% en ganado bovino afectado crónicamente por TB.
*   **Uso en el Proyecto:** Sustento económico del impacto silencioso pero constante de la Tuberculosis Bovina como patógeno calibrador en el Avance 2.
*   **Uso en Documento:** `docs/Segundo_avance/segundo_avance.md` (Sección 4).

---

## 🔒 3. Eje: Criptografía y Ciberseguridad

### [8] Nir, Y., & Langley, A. (2018). *ChaCha20 and Poly1305 for IETF Protocols* (RFC 8439). Internet Engineering Task Force (IETF). https://tools.ietf.org/html/rfc8439
*   **Dato/Parámetro que respalda:** La estructura algebraica modular, las operaciones ARX (Add-Rotate-XOR) y el desempeño en software del algoritmo de cifrado simétrico por flujo ChaCha20.
*   **Uso en el Proyecto:** Justificación del uso de ChaCha20 en dispositivos móviles de bajo costo en zonas rurales de Chiapas y Veracruz que carecen de chips criptográficos dedicados (AES-NI).
*   **Uso en Documento:** `docs/explicacion_matematica_chacha20.md` y `docs/articulo_divulgacion_final.md` (§5).
*   **Uso en Código:** `src/crypto/encryption.py` y `src/crypto/mock_mobile_app.py`.

### [9] Jonsson, J., & Kaliski, B. (2003). *Public-Key Cryptography Standards (PKCS) #1: RSA Cryptography Specifications Version 2.1* (RFC 3447). IETF. https://tools.ietf.org/html/rfc3447
*   **Dato/Parámetro que respalda:** Especificaciones del cifrado asimétrico RSA-2048 con esquema de relleno OAEP (Optimal Asymmetric Encryption Padding).
*   **Uso en el Proyecto:** Soporte para el esquema de **Cifrado Híbrido (Hybrid Encryption)** implementado para proteger las credenciales e identidad del ganadero en el servidor de SENASICA.
*   **Uso en Documento:** `docs/articulo_divulgacion_final.md` (§5).

---

## 🇲🇽 4. Eje: Censos y Datos Gubernamentales (México)

### [10] SIAP / SADER. (2023). *Cierre de la Producción Pecuaria 2023 (Inventario de Población Ganadera Bovinos)*. Servicio de Información Agroalimentaria y Pesquera, Secretaría de Agricultura y Desarrollo Rural, Gobierno de México. https://www.gob.mx/siap
*   **Dato/Parámetro que respalda:** Inventario nacional ganadero de **35.1 millones de cabezas de bovinos** y la distribución exacta por cada una de las 32 entidades federativas.
*   **Uso en el Proyecto:** Población susceptible inicial ($N$) por cada nodo del Grafo Nacional.
*   **Uso en Código:** `src/spatial_model/01_data_prep.py` (Ingesta del censo) y `src/models/fmd_finance_comparison.py` (Línea 36: `N = 35_100_000`).

### [11] INEGI. (2023). *Marco Geoestadístico Nacional 2023*. Instituto Nacional de Estadística y Geografía. https://www.inegi.org.mx
*   **Dato/Parámetro que respalda:** Polígonos geoespaciales y centroides geográficos de las 32 entidades federativas de México.
*   **Uso en el Proyecto:** Coordenadas latitud/longitud de los centroides de población para la formulación de los flujos gravitatorios interestatales.
*   **Uso en Código:** `src/spatial_model/01_data_prep.py` y `src/spatial_model/02_gravity_model.py`.

### [12] SENASICA. (2024). *Boletín Trimestral de Cuarentenas de Tuberculosis Bovina e Hatos Libres*. Servicio Nacional de Sanidad, Inocuidad y Calidad Agroalimentaria, Gobierno de México.
*   **Dato/Parámetro que respalda:** Registros estatales de prevalencia de TB, cuarentenas activas y hatos acreditados como libres de la enfermedad.
*   **Uso en el Proyecto:** Calibración empírica del proxy SIR de Tuberculosis Bovina a nivel nacional.
*   **Uso en Código:** `src/warehouse/csv_to_json.py` (Validador Pydantic del dataset de cuarentenas).

### [13] SNIIM. (2024). *Cuadro Comparativo Anual Nacional — Bovinos en Pie*. Sistema Nacional de Información e Integración de Mercados, Secretaría de Economía, Gobierno de México.
*   **Dato/Parámetro que respalda:** El valor comercial promedio en pie de un bovino de engorda en México, tasado en **$26,248 MXN** (aproximadamente **$1,544 USD** por cabeza de ganado).
*   **Uso en el Proyecto:** Constante de costo directo por animal sacrificado ante protocolos sanitarios ($P_{\text{sacrificio}}$).
*   **Uso en Código:** `src/models/fmd_finance_spatial.py` (Línea 26: `VALOR_CABEZA_USD = 1_544`).

### [14] USDA ERS. (2024). *Mexico Livestock and Products Annual — Live Cattle and Beef Trade Statistics*. United States Department of Agriculture, Economic Research Service.
*   **Dato/Parámetro que respalda:** Límite máximo de exportación de carne y ganado en pie de México hacia Estados Unidos, tasado en **$3,000 millones de USD anuales**.
*   **Uso en el Proyecto:** Cálculo de la pérdida diaria máxima por cierre absoluto de fronteras pecuarias.
*   **Uso en Código:** `src/models/fmd_finance_spatial.py` (Línea 27: `EXPORT_DIARIO_MAX = 8_200_000` derivado de $\frac{\$3,000,000,000 \text{ USD}}{365 \text{ días}} \approx \$8.21 \text{M USD}$).
