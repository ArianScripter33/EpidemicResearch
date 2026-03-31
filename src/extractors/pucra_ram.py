"""
PUCRA RAM Extractor — Wave 2 (PDF Parsing)
==========================================
Extracts antimicrobial resistance tables from PUCRA/UNAM annual reports.

Target bacteria: E. coli, Klebsiella pneumoniae, Salmonella spp., Acinetobacter baumannii
Feeds: AMR parameters for simulation and article.
"""

import pandas as pd
import pdfplumber
import re
from src.base_extractor import BaseExtractor
from src.config import PUCRA_URLS, RESISTENCIA_AMPICILINA

class PucraRAMExtractor(BaseExtractor):
    """
    Extractor for PUCRA RAM tables.
    Strategy:
    1. Download PDF reports for multiple years.
    2. Extract tables with resistance rates.
    3. Filter for specific bacteria and antibiotics.
    4. Cross-validate with hardcoded constants.
    """

    def __init__(self):
        super().__init__(name="pucra_ram")

    def extract(self) -> pd.DataFrame:
        """Download and parse PUCRA PDFs."""
        all_data = []
        for year, url in PUCRA_URLS.items():
            try:
                local_path = self.download_file(url)
                with pdfplumber.open(local_path) as pdf:
                    self.logger.info(f"Extracting tables from PUCRA {year} ({len(pdf.pages)} pages)...")
                    for i, page in enumerate(pdf.pages):
                        tables = page.extract_tables()
                        for table in tables:
                            if not table or len(table) < 2: continue

                            # Heuristic: resistance tables have certain headers
                            header = [str(c).replace('\n', ' ').strip().lower() for c in table[0]]
                            if any(k in header for k in ['antibiótico', 'antimicrobiano', 'bacteria', 'resistencia']):
                                df_table = pd.DataFrame(table[1:], columns=header)
                                # Clean potential empty headers/duplicates
                                df_table.columns = [f"col_{j}" if not c else c for j, c in enumerate(df_table.columns)]
                                df_table['year_report'] = year
                                df_table['source_url'] = url
                                df_table['page_num'] = i + 1
                                all_data.append(df_table)
            except Exception as e:
                self.logger.warning(f"Failed to process PUCRA {year}: {e}")

        if not all_data:
            return pd.DataFrame()

        combined_df = pd.concat(all_data, ignore_index=True)
        self.logger.info(f"Extracted {len(combined_df)} raw rows from PUCRA PDFs.")
        return combined_df

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and normalize RAM data."""
        if df.empty: return df

        clean = df.copy()

        # Target bacteria
        target_bacteria = [
            'E. COLI', 'ESCHERICHIA COLI',
            'KLEBSIELLA PNEUMONIAE',
            'SALMONELLA SPP.', 'SALMONELLA',
            'ACINETOBACTER BAUMANNII'
        ]

        # Identify relevant columns
        cols = clean.columns
        bacteria_col = next((c for c in cols if any(k in c.lower() for k in ['bacteria', 'organismo', 'especie'])), None)
        antibiotic_col = next((c for c in cols if any(k in c.lower() for k in ['antibiótico', 'antimicrobiano', 'antibiotico', 'fármaco', 'agente'])), None)
        resistance_col = next((c for c in cols if any(k in c.lower() for k in ['resistencia', 'pct', '%', 'porcentaje'])), None)
        n_col = next((c for c in cols if 'aislamientos' in c or 'n=' in c or 'total' in c), None)

        if not bacteria_col or not antibiotic_col:
            # Try to infer if not found by name
            self.logger.warning("Could not identify bacteria or antibiotic columns by name. Columns were: " + str(list(cols)))
            return clean # Or return empty if we want strict

        # Standardize names
        final_cols = {
            bacteria_col: 'bacteria',
            antibiotic_col: 'antibiotico',
            resistance_col: 'pct_resistencia' if resistance_col else 'raw_resistencia',
            n_col: 'n_aislamientos' if n_col else 'raw_n'
        }
        clean = clean.rename(columns={k: v for k, v in final_cols.items() if k})

        # Filtering
        # 1. Row filtering by bacteria (if it's per row) or table context?
        # Often tables have a single bacteria in the title, and then rows are antibiotics.
        # But some tables have bacteria in the first column.

        def is_target_bacteria(val):
            val = str(val).upper().strip()
            return any(b in val for b in target_bacteria)

        # Clean pct_resistencia
        if 'pct_resistencia' in clean.columns:
            clean['pct_resistencia'] = clean['pct_resistencia'].str.replace('%', '').str.replace(',', '.').str.strip()
            clean['pct_resistencia'] = pd.to_numeric(clean['pct_resistencia'], errors='coerce')

        # Validation with constants (e.g. Salmonella + Ampicilina ~ 94.7%)
        # Note: 94.7% in config is 0.947, so we check for ~94.7 in the PDF
        salmo_amp = clean[
            (clean['bacteria'].fillna('').str.upper().str.contains('SALMONELLA')) &
            (clean['antibiotico'].fillna('').str.upper().str.contains('AMPICILINA'))
        ]
        if not salmo_amp.empty:
            extracted_val = salmo_amp['pct_resistencia'].iloc[0]
            self.logger.info(f"Cross-validation: Extracted {extracted_val}% for Salmonella+Ampicilina. Config expects {RESISTENCIA_AMPICILINA*100}%.")

        return clean

if __name__ == "__main__":
    extractor = PucraRAMExtractor()
    result = extractor.run()
    if not result.empty:
        print(f"Extracted {len(result)} rows.")
        print(result.head())
    else:
        print("No data extracted.")
