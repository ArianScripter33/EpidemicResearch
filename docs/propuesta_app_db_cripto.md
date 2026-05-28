# Propuesta de Arquitectura: App Ganado Saludable (v2)

Este documento define la arquitectura teórica de la aplicación de trazabilidad y vigilancia epidemiológica, detallando:

1. El **esquema de base de datos** NoSQL (MongoDB).
2. El **flujo de encriptación** de datos sensibles.
3. La integración con el **motor de predicción** (Modelo Gravitatorio + XGBoost).

> **Decisión Estratégica (Mockup vs. Desarrollo Completo):**
> Para la presentación, el esfuerzo se enfoca en *demostrar el diseño conceptual y la viabilidad técnica* (diagramas, esquemas y resultados del modelo matemático) en lugar de programar el backend completo. Esto maximiza el impacto visual con mínima fricción técnica.

---

## 1. Esquema de Base de Datos (MongoDB)

Al ser una base de datos orientada a documentos (NoSQL), no tenemos "tablas" rígidas, sino **colecciones** de documentos JSON. A continuación se presenta el modelo Entidad-Relación de las colecciones principales:

```mermaid
erDiagram
    USUARIO ||--o{ REPORTE_SANITARIO : "Genera"
    USUARIO ||--o{ GRANJA : "Administra"
    GRANJA ||--o{ ANIMAL : "Alberga"
    GRANJA ||--o{ ZONA_CONTROL : "Pertenece a"
    ANIMAL ||--o{ MOVIMIENTO : "Registra"
    ANIMAL ||--o{ REPORTE_SANITARIO : "Sujeto de"
    MODELO_PREDICCION ||--o{ ZONA_CONTROL : "Calcula riesgo de"

    USUARIO {
        ObjectId _id PK
        string nombre_completo "🔒 Encriptado (FLE)"
        string rfc_curp "🔒 Encriptado (FLE)"
        string email "🔒 Encriptado (FLE)"
        string rol "Ganadero | Veterinario | CPA | Admin"
        string password_hash "bcrypt 12 rounds"
        date ultimo_acceso
    }

    GRANJA {
        ObjectId _id PK
        ObjectId owner_id FK
        string upp_id "Clave SINIIGA Única"
        GeoJSON ubicacion "Point(lat, long)"
        string estado "Jalisco | Veracruz | ..."
        int inventario_bovino "Cabezas actuales"
        int capacidad_maxima
        boolean cuarentena_activa
        float indice_riesgo "Score del modelo ML (0.0-1.0)"
    }

    ANIMAL {
        ObjectId _id PK
        ObjectId granja_actual_id FK
        string siniiga_tag "Arete RFID de identificación"
        string especie "Bovino | Porcino | Caprino"
        string raza
        date fecha_nacimiento
        string estado_salud "Sano | Sospechoso | Infectado | Removido"
        date ultima_vacunacion
    }

    MOVIMIENTO {
        ObjectId _id PK
        ObjectId animal_id FK
        ObjectId granja_origen_id FK
        ObjectId granja_destino_id FK
        date fecha_transito
        string tipo "Comercial | Feria | Rastro TIF"
        string vehiculo_placas
        boolean guia_sanitaria_verificada
    }

    REPORTE_SANITARIO {
        ObjectId _id PK
        ObjectId animal_id FK
        ObjectId usuario_id FK
        ObjectId granja_id FK
        date fecha_reporte
        string sintomas "Lesiones vesiculares, fiebre, sialorrea"
        string diagnostico_presuntivo
        string metodo_diagnostico "Clínico | ELISA | RT-PCR"
        float probabilidad_riesgo "Score del modelo ML"
        string estatus "Pendiente | Confirmado | Descartado"
    }

    ZONA_CONTROL {
        ObjectId _id PK
        string estado
        GeoJSON perimetro "Polygon de 3km/10km"
        string tipo "Foco | Perifocal | Vigilancia"
        float riesgo_gravitatorio "Índice calculado por el modelo"
        int granjas_afectadas
        date fecha_activacion
    }

    MODELO_PREDICCION {
        ObjectId _id PK
        date fecha_ejecucion
        string version_modelo "XGBoost v1.7 + Gravity"
        object parametros "R0, gamma, alpha, beta"
        object resultados_por_estado "32 scores de riesgo"
        float accuracy "Precisión del modelo"
    }
```

### Ejemplo de Documento JSON (MongoDB)

```json
{
  "_id": "ObjectId('665a1b2c3d4e5f6a7b8c9d0e')",
  "granja_id": "ObjectId('665a1b2c3d4e5f6a7b8c9d0f')",
  "animal_id": "ObjectId('665a1b2c3d4e5f6a7b8c9d10')",
  "fecha_reporte": "2026-05-15T10:30:00Z",
  "sintomas": "Lesiones vesiculares en lengua y pezuñas, fiebre 40.5°C",
  "diagnostico_presuntivo": "Sospecha de FMD (Serotipo O)",
  "metodo_diagnostico": "ELISA NSP",
  "probabilidad_riesgo": 0.87,
  "estatus": "Pendiente confirmación RT-PCR"
}
```

---

## 2. Esquema de Encriptación y Seguridad (Criptografía)

Dado que manejamos datos sensibles (ubicación de granjas y la identidad de los ganaderos), el sistema implementa una arquitectura de seguridad basada en los algoritmos vistos en clase: **Funciones Hash** y **Cifrado Asimétrico (RSA)**.

### Especificaciones Técnicas de Criptografía

| Capa | Algoritmo / Técnica | Propósito en la Aplicación |
|------|---------------------|---------------------------|
| **Passwords de Usuarios** | `bcrypt` (Función Hash con sal) | Las contraseñas de los ganaderos nunca se almacenan en texto plano. Se usa `bcrypt` para aplicar un Hash matemático irreversible, protegiéndolos contra hackeos de la base de datos. |
| **Datos Personales (PII)** | `RSA` (Cifrado Asimétrico) | Para proteger el nombre y correo del ganadero en la base de datos, usamos la Llave Pública (RSA) para encriptar la información al guardarla. Solo la autoridad (CPA) tiene la Llave Privada para desencriptarla cuando se requiere. |
| **Tokens de Sesión** | `JWT` firmado con RSA | Cuando el usuario inicia sesión en la App, se le entrega un token firmado criptográficamente para validar su identidad sin tener que mandar la contraseña en cada petición. |

### ¿Qué campos están encriptados?

```mermaid
flowchart LR
    subgraph Campos_Abiertos ["Campos en Texto Plano (Consultas rápidas)"]
        A1["estado_salud"]
        A2["ubicacion (GeoJSON)"]
        A3["inventario_bovino"]
        A4["indice_riesgo"]
        A5["fecha_reporte"]
    end

    subgraph Campos_FLE ["🔒 Campos con Field-Level Encryption"]
        B1["nombre_completo"]
        B2["rfc_curp"]
        B3["email"]
        B4["vehiculo_placas"]
    end

    subgraph Justificacion ["Criterio de Decisión"]
        C["¿Identifica a una persona física?\n→ SÍ = Encriptar (Ley Federal de\nProtección de Datos Personales)"]
    end

    Campos_Abiertos -.-> Justificacion
    Campos_FLE -.-> Justificacion
```

> **Principio rector:** Se encripta todo lo que la *Ley Federal de Protección de Datos Personales en Posesión de Particulares (LFPDPPP)* clasifica como dato personal identificable. Los datos epidemiológicos (estado_salud, ubicación, inventario) se mantienen en texto plano para permitir consultas geoespaciales y analíticas en tiempo real sin penalización de rendimiento.

---

## 3. Integración con el Motor de Predicción

La app no opera de forma aislada. Se alimenta del pipeline de Machine Learning:

```mermaid
flowchart LR
    subgraph Datos_Reales ["Datos Públicos (SIAP, INEGI)"]
        A["Inventario Bovino\npor Estado"]
        B["Shapefile\nMéxico"]
    end

    subgraph Motor ["Motor Predictivo (Python)"]
        C["Modelo Gravitatorio\nF_ij = k * P_i * P_j / d_ij^2"]
        D["SIR sobre Grafo\n(NetworkX)"]
        E["XGBoost Regressor\n(Índice de Riesgo)"]
    end

    subgraph App ["App Ganado Saludable"]
        F["MongoDB:\ncolección ZONA_CONTROL"]
        G["Dashboard:\nMapa de Riesgo"]
    end

    A --> C
    B --> C
    C --> D
    D --> E
    E -->|"Scores 0.0-1.0\npor estado"| F
    F --> G
```

El modelo XGBoost calcula un **Índice de Riesgo Sistémico (0.0 a 1.0)** para cada estado, basado en 13 variables de Teoría de Grafos:
- **Masa Biológica:** Inventario bovino actual.
- **Topología de Red:** Centralidad de Intermediación (Betweenness), PageRank, Cercanía.
- **Vectores de Infección:** Flujo Gravitatorio Saliente (weighted_out_flux) y Entrante (weighted_in_flux).
- **Fricción Geográfica:** Distancia asfáltica promedio al resto del país.

Este score predictivo se inyecta automáticamente en el campo `indice_riesgo` de las colecciones `GRANJA` y `ZONA_CONTROL`, permitiendo a los veterinarios de la CPA priorizar inspecciones estructurales (ej. blindar las granjas en estados con alto *flujo gravitatorio saliente*, independientemente de dónde haya iniciado un brote).

---

## 4. Próximos Pasos (To-Do para el Equipo)

| # | Tarea | Responsable | Entregable |
|---|-------|-------------|------------|
| 1 | Revisar diagramas de BD y aprobar colecciones | Compañero | Feedback en PR |
| 2 | Descargar Shapefile INEGI + CSV SIAP | Equipo | ✅ Completado |
| 3 | Programar Modelo Espacial (`02_gravity_model.py`, `03_spatial_sir.py`) | Yo | ✅ Completado |
| 4 | Generar animaciones S-I-R (Race Chart + Stacked) | Yo | ✅ Completado |
| 5 | Entrenar XGBoost y derivar Node Embeddings | Yo | ✅ Completado (R²=0.843) |
| 6 | Diseñar slides de arquitectura y seguridad | Compañero | Diapositivas con los diagramas de este doc |
