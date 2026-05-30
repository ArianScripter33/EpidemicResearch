# 📝 Plan de Trabajo y TODOs — AftoSec (Entrega Final y Diseño Editorial)

> **Enfermedad Asignada:** Fiebre Aftosa (FMD) | **Proxy de Calibración:** TB Bovina
> **Fase del Proyecto:** Auditoría de Calidad, Consolidación Bibliográfica y Diseño Editorial Premium

---

## 🛠️ Phase 1: Auditoría Técnica y Consolidación (En Curso) 🔄

- [x] **Auditoría de Hallazgos y Alucinaciones:**
  - [x] Corregir la alucinación de Diana Victoria en la Sección §6 respecto al comportamiento inicial de los flujos de caja en Veracruz.
  - [x] Sincronizar y auditar el término "Cifrado Híbrido" (Hybrid Encryption) en la sección §5 de Axel.
  - [x] Actualizar y validar los nombres completos de los autores (Diana Victoria Hernandez Monroy).
- [x] **Consolidación Bibliográfica (APA 7):**
  - [x] Crear el documento de referencia `docs/bibliografia_maestra.md` que mapea cada fuente del semestre completo con los datos específicos del modelo SIR y finanzas.
- [ ] **Sincronización de Referencias Cruzadas:**
  - [ ] Unificar la bibliografía final en `docs/articulo_divulgacion_final.md` (Sección §8).
  - [ ] Unificar la bibliografía final en `docs/Tercer_avance/tercer_avance.md` (Sección de Bibliografía).

---

## 🎨 Phase 2: Diseño Editorial y Dirección de Arte ⏳

- [x] **Planificación del Diseño Editorial:**
  - [x] Crear el archivo `docs/diseno_editorial_plan.md` con los lineamientos estéticos (Estilo Híbrido Nature / MIT Tech Review, paleta UNRC, jerarquías tipográficas, citas destacadas e infoboxes).
- [ ] **Generación de Ilustraciones con IA:**
  - [ ] Generar la ilustración conceptual de la interfaz de la App en el campo (Ganadero/Vacas).
  - [ ] Generar la ilustración del Grafo de Conectividad Vial Nacional de Veracruz y Jalisco.
  - [ ] Mapear las rutas de las imágenes en los documentos `tercer_avance.md` y `articulo_divulgacion_final.md`.
- [ ] **Maquetación Docx/PDF de Alta Calidad (Skill Docx):**
  - [ ] Configurar el archivo de generación del documento Word para aplicar la paleta UNRC (`#9C223F`, `#C9A84C`, `#F8F4F0`).
  - [ ] Inyectar las citas destacadas con bordes carmesí gruesos.
  - [ ] Diseñar las tablas comparativas de benchmark del XGBoost en dos colores.
  - [ ] Programar e inyectar el mapa de pies de página explicativos (Footnotes) vinculados a la bibliografía maestra.

---

## 🧪 Phase 3: Verificación de Scripts de Producción

- [ ] **Smoke Tests de Ecuaciones Financieras:**
  - [ ] Verificar consistencia del valor de cabeza bovina (`1544 USD`) y pérdida máxima por cierre de exportaciones (`8.2M USD`) en `fmd_finance_spatial.py` y `fmd_finance_comparison.py`.
- [ ] **Smoke Tests de Ciberseguridad:**
  - [ ] Correr `mock_mobile_app.py` para asegurar que el cifrado y descifrado de ChaCha20 y el tag AEAD se validen sin errores.
- [ ] **Verificación de Data Warehouse:**
  - [ ] Asegurar que el conversor `csv_to_json.py` con validación Pydantic guarde correctamente `cuarentenas.json` sin discrepancias de tipos.

---

## 📦 Phase 4: Sincronización y Cierre

- [ ] **Revisión Conjunta de Conclusiones:**
  - [ ] Dejar listos los placeholders para las firmas de conclusiones de Arian, Axel y Diana Victoria.
  - [ ] Commit y Push final en GitHub de todos los entregables.
