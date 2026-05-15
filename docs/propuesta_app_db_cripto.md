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

Dado que manejamos datos sensibles (ubicación de granjas, identidad de ganaderos y estatus sanitario que puede afectar mercados internacionales de $3,000M USD anuales), implementamos un modelo de **seguridad de tres capas**.

```mermaid
flowchart TD
    subgraph Cliente ["Dispositivo del Ganadero / Veterinario"]
        A["App Móvil / Web\n(React Native / Next.js)"]
    end

    subgraph Red ["Tránsito de Datos"]
        B(("🔒 TLS 1.3\nECDHE + AES-256-GCM\nPerfect Forward Secrecy"))
    end

    subgraph Servidor ["Backend (Node.js / Python)"]
        C["API Gateway\n+ Rate Limiting"]
        D["Lógica de Negocio\n+ Autenticación JWT"]
        E{"🔑 Motor FLE\nClient-Side\nField-Level Encryption"}
    end

    subgraph KMS ["Gestión de Llaves"]
        K["AWS KMS / GCP KMS\nLlave Maestra (CMK)\nRotación cada 90 días"]
    end

    subgraph BaseDatos ["MongoDB Atlas"]
        F[("MongoDB\n🔒 AES-256-CBC\nEncryption at Rest\n+ Audit Logging")]
    end

    A <-->|Canal Seguro HTTPS| B
    B <--> C
    C <--> D
    D <-->|"Cifrado en Memoria\n(antes de escribir a DB)"| E
    E <-->|"Datos PII cifrados\n(campos individuales)"| F
    K -.->|"Provee Data Encryption Keys\n(DEKs)"| E
```

### Especificaciones Técnicas de Criptografía

| Capa | Estándar | Algoritmo | Detalle Técnico |
|------|----------|-----------|-----------------|
| **En Tránsito** | TLS 1.3 | `ECDHE_RSA_WITH_AES_256_GCM_SHA384` | Perfect Forward Secrecy: si roban la llave hoy, no desencriptan datos de ayer. Cada sesión genera una llave efímera Diffie-Hellman sobre curva elíptica. |
| **En Reposo** | AES-256 | `AES-256-CBC` (MongoDB WiredTiger) | Todo el volumen de disco está cifrado de forma transparente. Si roban el disco físico, los datos son ilegibles sin la llave maestra. |
| **A Nivel de Campo (FLE)** | AEAD | `AES-256-CBC + HMAC-SHA-512` | Los campos PII (`nombre_completo`, `rfc_curp`, `email`) se cifran **antes de salir del servidor** hacia la base de datos. Ni el DBA puede leerlos sin la Data Encryption Key (DEK) gestionada por el KMS externo. |
| **Passwords** | bcrypt | `bcrypt` con 12 rounds de sal | Las contraseñas nunca se almacenan en texto plano. bcrypt es resistente a ataques de GPU por diseño (memory-hard). |
| **Tokens de Sesión** | JWT | `RS256` (RSA 2048-bit) | Los tokens de autenticación se firman asimétricamente. El servidor solo necesita la llave pública para verificar, reduciendo la superficie de ataque. |

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

El modelo XGBoost calcula un **Índice de Riesgo Sistémico (0.0 a 1.0)** para cada estado, basado en:
- Inventario bovino (masa gravitatoria)
- Centralidad en la red de movimiento de ganado
- Distancia a los estados más conectados
- Número de rastros TIF
- Valor de exportaciones

Este score se inyecta automáticamente en el campo `indice_riesgo` de las colecciones `GRANJA` y `ZONA_CONTROL`, permitiendo a los veterinarios de la CPA priorizar las inspecciones.

---

## 4. Próximos Pasos (To-Do para el Equipo)

| # | Tarea | Responsable | Entregable |
|---|-------|-------------|------------|
| 1 | Revisar diagramas de BD y aprobar colecciones | Compañero | Feedback en PR |
| 2 | Descargar Shapefile INEGI + CSV SIAP | Equipo | Archivos en `data/raw/` |
| 3 | Programar `gravity_network.py` | Yo | Script + gráfica de la red |
| 4 | Generar animación de propagación (GIF/MP4) | Yo | Archivo para la presentación |
| 5 | Entrenar XGBoost y generar mapa de riesgo | Yo | Mapa coroplético + métricas |
| 6 | Diseñar slides de arquitectura y seguridad | Compañero | Diapositivas con los diagramas de este doc |
