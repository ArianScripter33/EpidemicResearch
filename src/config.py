"""
Ganado Saludable — Central Configuration
=========================================
All URLs, biological constants, and financial parameters.
Sources: M_doc.md refs [1]-[24], V2.md, README.md, Protocolo PDF
"""

from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# PROJECT PATHS
# ═══════════════════════════════════════════════════════════════
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# ═══════════════════════════════════════════════════════════════
# EXTRACTION URLs — Verified from M_doc.md
# ═══════════════════════════════════════════════════════════════

# --- Wave 1: Stable Endpoints ---

SENASICA_URLS = {
    # [1] Hatos libres TB bovina — CSV directo
    "hatos_libres_dic_2025": "https://repodatos.atdt.gob.mx/api_update/senasica/constatacion_hatos_libres_tuberculosis_bovina/hatos_libres_tuberculosis.csv",
    "hatos_libres_jun_2025": "https://repodatos.atdt.gob.mx/api_update/senasica/constatacion_hatos_libres_tuberculosis_bovina/47_tuberculosis-bovina.csv",
    # Ficha del dataset
    "dataset_page": "https://www.datos.gob.mx/dataset/constatacion_hatos_libres_tuberculosis_bovina",
}

# [2] Cuarentenas TB 2024 (PDFs)
SENASICA_CUARENTENAS_PDFS = {
    "q4_2024": "https://www.gob.mx/cms/uploads/attachment/file/979992/1._Cuarentenas_Tb_4to_tmt.pdf",
    "q3_2024": "https://www.gob.mx/cms/uploads/attachment/file/958502/1_Cuarentenas_Tercer_2024.pdf",
    "q2_2024": "https://www.gob.mx/cms/uploads/attachment/file/935619/1_CUARENTENAS_2DO_TRIMESTRE_2024.pdf",
    "q1_2024": "https://www.gob.mx/cms/uploads/attachment/file/914491/1_CUARENTENAS_Primer_2024.pdf",
}

# [3] DGE Anuarios de Morbilidad (ZIP → CSV)
DGE_ANUARIO_URL_TEMPLATE = "https://epidemiologia.salud.gob.mx/anuario/datos_abiertos/Anuario_{year}.zip"
DGE_YEARS = list(range(2015, 2023))  # 2015–2022
DGE_PDF_YEARS = list(range(2018, 2025))  # 2018–2024
DGE_NATIONAL_REPORT_NAME = "distribucion_casos_nuevos_enfermedad_fuente_notificacion"
DGE_NATIONAL_PDF_URL_TEMPLATE = (
    "https://epidemiologia.salud.gob.mx/anuario/{year}/morbilidad/nacional/{report_name}.pdf"
)

# API oculta SENASICA (secondary path — Doc A / Protocolo PDF)
SENASICA_API_OCULTA = "https://dj.senasica.gob.mx/sias/api/Statistics/SaludAnimal/TuberculosisBovina/ObtenerDatos"

# --- Wave 2: International + PDF Parsing ---

# [14] openFMD Dashboard — CSV global de brotes FMD
OPENFMD_DASHBOARD = "https://openfmd.org/dashboard/fmdwatch/"

# [17] WRLFMD — World Reference Lab reportes por región
WRLFMD_SUDAMERICA = "https://www.wrlfmd.org/country-reports/south-america"

# PANAFTOSA/OPS
PANAFTOSA_URL = "https://www.paho.org/en/panaftosa"

# [19]-[21] PUCRA — Resistencia Antimicrobiana (PDFs)
PUCRA_URLS = {
    "2025": "https://puiree.cic.unam.mx/divulgacion/docs/pucra2025.pdf",
    "2024": "https://puiree.cic.unam.mx/divulgacion/docs/pucra2024.pdf",
    "2023": "https://puiree.cic.unam.mx/divulgacion/docs/pucra23.pdf",
}

# WAHIS — WOAH reports retriever (GitHub tool)
WAHIS_RETRIEVER_REPO = "https://github.com/loicleray/WOAH_WAHIS.ReportRetriever"
# Note: Broken as of March 2026 due to Cloudflare protection.

# Kaggle FMD Dataset
KAGGLE_FMD_DATASET = "wasimfaraz/fmd-cattle-dataset"

# --- Wave 3: Hostile Extraction ---

# [4] SINAIS Cubos Dinámicos
SINAIS_CUBOS = "http://www.dgis.salud.gob.mx/contenidos/basesdedatos/BD_Cubos_gobmx.html"

# [24] PNT — Plataforma Nacional de Transparencia
PNT_URL = "https://www.plataformadetransparencia.org.mx/"

# COFEPRIS clausuras
COFEPRIS_CLAUSURAS = "https://www.gob.mx/cofepris/documentos/lista-de-establecimientos-clausurados?state=published"
COFEPRIS_VERIFICACIONES = "https://www.gob.mx/cofepris/acciones-y-programas/listado-de-visitas-de-verificacion"

# --- Documentos de Referencia (PDFs) ---

# [11] Plan de Acción Inmediata FMD
PAI_FMD_PDF = "https://dj.senasica.gob.mx/Contenido/files/2021/julio/PAIFiebreAftosa07-06-21_e83a982d-b6b5-40b0-a3ae-41321c88bbfa.pdf"

# [12] Manuales CPA
MANUALES_CPA = "https://www.gob.mx/senasica/documentos/manuales-cpa?state=published"

# [7] Acuerdo TB DOF
ACUERDO_TB_DOF = "https://www.gob.mx/cms/uploads/attachment/file/964169/2024_12_30_MAT_sader_-_Acuerdo_TB.pdf"

# ═══════════════════════════════════════════════════════════════
# BIOLOGICAL CONSTANTS — from V2.md + README.md + Literature
# ═══════════════════════════════════════════════════════════════

# --- Biomasa Nacional ---
N_BIOMASA_TOTAL = 35_100_000        # 35.1M cabezas (SIAP)
N_BIOMASA_CARNE = 32_600_000        # 32.6M para carne
N_BIOMASA_LECHE = 2_500_000         # 2.5M lecheras
CONFINAMIENTO_ANUAL = 2_800_000     # Cabezas/año en CAFOs

# --- Tuberculosis Bovina (Proxy de Calibración) ---
R0_TB_LOW = 1.5
R0_TB_MID = 1.8                     # Valor central para simulación
R0_TB_HIGH = 2.0
PERIODO_INFECCIOSO_TB_DIAS = 180    # ~6 meses
GAMMA_TB = 1 / PERIODO_INFECCIOSO_TB_DIAS
BETA_TB = R0_TB_MID * GAMMA_TB

# --- Fiebre Aftosa (Enfermedad Asignada) ---
R0_FMD_LOW = 4.0                    # Estimación conservadora
R0_FMD_MID = 6.0                    # Valor central (Tildesley et al.)
R0_FMD_HIGH = 8.0                   # Escenario UK 2001
PERIODO_INFECCIOSO_FMD_DIAS = 14    # ~2 semanas
GAMMA_FMD = 1 / PERIODO_INFECCIOSO_FMD_DIAS
BETA_FMD = R0_FMD_MID * GAMMA_FMD

# --- Resistencia Antimicrobiana (V2.md §3-4) ---
RESISTENCIA_AMPICILINA = 0.947      # 94.7% de Salmonella en carne molida
RESISTENCIA_CARBENICILINA = 0.842
RESISTENCIA_TETRACICLINA = 0.684
RESISTENCIA_TMP_SMX = 0.684
PREVALENCIA_BLACTX_M = 0.235       # 23.5% (BLEE)
PREVALENCIA_BLATEM = 0.150
ECOLI_O157_PIEL = 0.909            # 90.9% en hisopados pre-evisceración

# --- Prevalencia Salmonella por Canal de Venta (V2.md §3) ---
PREVALENCIA_SALMONELLA = {
    "supermercados": 0.013,          # 1.3%
    "carnicerias": 0.084,            # 8.4%
    "tianguis": 0.136,               # 13.6%
    "mercados_municipales": 0.223,   # 22.3%
}

# ═══════════════════════════════════════════════════════════════
# FINANCIAL CONSTANTS — from M_doc.md §1.3 + README + Literature
# ═══════════════════════════════════════════════════════════════

# TB Bovina (crónico, endémico)
PRESUPUESTO_CAMPAÑA_TB_MXN = 300_000_000        # >300M MXN/año (SENASICA)
DESPOBLACION_MAX_CABEZAS = 1_951                 # Máximo registrado (Chihuahua)
COSTO_BROTE_TB_MXN = 39_000_000                  # ~$39M MXN por brote
INDEMNIZACION_PCT = 0.85                          # ~85% del valor del animal
PRECIO_UA_MXN = 20_000                            # Precio por Unidad Animal (estimado)

# FMD (catastrófico)
COSTO_UK_2001_GBP = 8_000_000_000                # ~£8B
COSTO_UK_2001_MXN = 200_000_000_000              # ~$200B MXN
ANIMALES_SACRIFICADOS_UK_2001 = 6_000_000
COSTO_SISTEMA_IOT_ANUAL_MXN = 5_000_000          # $5M MXN

# Tasa de descuento para VPN
TASA_DESCUENTO = 0.12                             # TIIE + prima de riesgo

# ═══════════════════════════════════════════════════════════════
# CIE-10 CODES — for DGE filtering
# ═══════════════════════════════════════════════════════════════

CIE10_TB_RESPIRATORIA = ["A15", "A16"]
CIE10_TB_OTRAS = ["A17", "A18", "A19"]
CIE10_TB_ALL = CIE10_TB_RESPIRATORIA + CIE10_TB_OTRAS
CIE10_INTOXICACION_ALIMENTARIA = ["A05"]
CIE10_TARGET_ALL = CIE10_TB_ALL + CIE10_INTOXICACION_ALIMENTARIA

# ═══════════════════════════════════════════════════════════════
# EXTRACTION CONFIG
# ═══════════════════════════════════════════════════════════════

HTTP_TIMEOUT = 60           # seconds
HTTP_RETRIES = 3
HTTP_BACKOFF_FACTOR = 2     # exponential backoff
USER_AGENT = "GanadoSaludable-EpidemicResearch/1.0 (Academic Project)"

# ═══════════════════════════════════════════════════════════════
# SIR MODEL SCENARIOS — 6 escenarios definidos en implementation_plan
# ═══════════════════════════════════════════════════════════════

SIR_SCENARIOS = [
    {
        "id": 1,
        "name": "TB — Sin intervención",
        "disease": "TB",
        "R0": R0_TB_MID,
        "gamma": GAMMA_TB,
        "N": N_BIOMASA_TOTAL,
        "t_days": 365 * 5,  # 5 años
        "description": "¿Cuántos hatos se infectan en 1 año? (Validación vs datos SENASICA)",
    },
    {
        "id": 2,
        "name": "TB — Con vacunación",
        "disease": "TB",
        "R0": 0.9,           # Vacunación reduce R0 < 1
        "gamma": GAMMA_TB,
        "N": N_BIOMASA_TOTAL,
        "t_days": 365 * 5,
        "description": "¿Cuánto debe reducirse β para control?",
    },
    {
        "id": 3,
        "name": "TB — Con cuarentena estatal",
        "disease": "TB",
        "R0": 0.9,           # Cuarentena reduce R0
        "gamma": GAMMA_TB,
        "N": N_BIOMASA_TOTAL,
        "t_days": 365 * 5,
        "description": "Efecto de aislar Chihuahua/Durango",
    },
    {
        "id": 4,
        "name": "FMD — Sin intervención",
        "disease": "FMD",
        "R0": R0_FMD_MID,    # R0 = 6.0
        "gamma": GAMMA_FMD,
        "N": N_BIOMASA_TOTAL,
        "t_days": 180,       # 6 meses
        "description": "¿Cuántos días hasta infectar >50% del hato nacional?",
    },
    {
        "id": 5,
        "name": "FMD — Con cuarentena + sacrificio",
        "disease": "FMD",
        "R0": 2.0,           # Intervención reduce R0 de 6.0 a 2.0
        "gamma": GAMMA_FMD,
        "N": N_BIOMASA_TOTAL,
        "t_days": 180,
        "description": "¿Es suficiente la capacidad de respuesta CPA?",
    },
    {
        "id": 6,
        "name": "FMD — Escenario UK 2001",
        "disease": "FMD",
        "R0": R0_FMD_HIGH,   # R0 = 8.0
        "gamma": GAMMA_FMD,
        "N": N_BIOMASA_TOTAL,
        "t_days": 180,
        "description": "¿Cuántas cabezas se sacrificarían? ¿Cuál es el costo?",
    },
]

# ═══════════════════════════════════════════════════════════════
# ESTADOS DE MÉXICO — for geographic normalization
# ═══════════════════════════════════════════════════════════════

ESTADOS_MEXICO = {
    "AGS": "Aguascalientes", "BC": "Baja California", "BCS": "Baja California Sur",
    "CAM": "Campeche", "COAH": "Coahuila", "COL": "Colima",
    "CHIS": "Chiapas", "CHIH": "Chihuahua", "CDMX": "Ciudad de México",
    "DGO": "Durango", "GTO": "Guanajuato", "GRO": "Guerrero",
    "HGO": "Hidalgo", "JAL": "Jalisco", "MEX": "Estado de México",
    "MICH": "Michoacán", "MOR": "Morelos", "NAY": "Nayarit",
    "NL": "Nuevo León", "OAX": "Oaxaca", "PUE": "Puebla",
    "QRO": "Querétaro", "QROO": "Quintana Roo", "SLP": "San Luis Potosí",
    "SIN": "Sinaloa", "SON": "Sonora", "TAB": "Tabasco",
    "TAM": "Tamaulipas", "TLAX": "Tlaxcala", "VER": "Veracruz",
    "YUC": "Yucatán", "ZAC": "Zacatecas",
}
