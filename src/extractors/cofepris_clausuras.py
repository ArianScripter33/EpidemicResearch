"""
COFEPRIS Clausuras Extractor — Wave 3 (Hostile Extraction)
=========================================================
Extracts data from COFEPRIS closure lists (establecimientos clausurados).
Specifically targets meat processing plants with clenbuterol or salmonella.

Feeds: Proxy de Opacidad (XGBoost feature)
"""

import pandas as pd
import pdfplumber
import re
from typing import Optional
from src.base_extractor import BaseExtractor
from src.config import COFEPRIS_CLAUSURAS, ESTADOS_MEXICO

class CofeprisClausurasExtractor(BaseExtractor):
    """
    Extractor for COFEPRIS closure lists.
    Strategy:
    1. Scrape the documents page to find the latest PDF link.
    2. Download the PDF.
    3. Extract tables using pdfplumber.
    4. Filter by meat-related keywords and contaminants.
    """

    def __init__(self):
        super().__init__(name="cofepris_clausuras")
        self.base_url = "https://www.gob.mx"

    def extract(self) -> pd.DataFrame:
        """Find and download the latest PDF, then extract tables."""
        self.logger.info("Finding latest PDF closure lists...")

        # Search for multiple sources as the first one might only be clinics
        urls_to_check = [COFEPRIS_CLAUSURAS, "https://www.gob.mx/cofepris/acciones-y-programas/listado-de-visitas-de-verificacion"]
        all_pdfs = []

        for url in urls_to_check:
            resp = self.session.get(url)
            html = resp.text
            matches = re.findall(r'href="([^"]*?\.pdf)"', html, re.IGNORECASE)
            for m in matches:
                full_url = m if m.startswith('http') else self.base_url + m
                if full_url not in all_pdfs:
                    all_pdfs.append(full_url)

        if not all_pdfs:
            self.logger.error("Could not find any PDF links in the COFEPRIS pages.")
            return pd.DataFrame()

        self.logger.info(f"Found {len(all_pdfs)} PDF candidates.")

        # In a real scenario, we might want to filter PDFs by name (e.g. including 'Establecimientos')
        # For now, let's try the ones that look most promising
        target_pdfs = [p for p in all_pdfs if 'Establecimientos' in p or 'clausuradas' in p]
        if not target_pdfs: target_pdfs = all_pdfs[:3] # Fallback to first few

        all_data = []
        for pdf_url in target_pdfs:
            try:
                local_path = self.download_file(pdf_url)
                with pdfplumber.open(local_path) as pdf:
                    self.logger.info(f"Extracting tables from {pdf_url} ({len(pdf.pages)} pages)...")
                    for i, page in enumerate(pdf.pages):
                        table = page.extract_table()
                        if table:
                            # Use first row as header, but handle cases where it might not be perfect
                            header = [str(c).replace('\n', ' ').strip() for c in table[0]]
                            # Ensure unique headers by appending suffix if duplicate
                            seen = {}
                            unique_header = []
                            for h in header:
                                if h in seen:
                                    seen[h] += 1
                                    unique_header.append(f"{h}_{seen[h]}")
                                else:
                                    seen[h] = 0
                                    unique_header.append(h)

                            df_page = pd.DataFrame(table[1:], columns=unique_header)
                            df_page['source_pdf'] = pdf_url
                            all_data.append(df_page)
            except Exception as e:
                self.logger.warning(f"Failed to process {pdf_url}: {e}")

        if not all_data:
            self.logger.warning("No tables found in the PDF.")
            return pd.DataFrame()

        combined_df = pd.concat(all_data, ignore_index=True)
        self.logger.info(f"Extracted {len(combined_df)} raw rows from PDF.")
        return combined_df

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean data, filter by keywords, and normalize states."""
        if df.empty:
            return df

        clean = df.copy()

        # Normalize columns
        clean.columns = [
            str(c).lower().strip()
            .replace('\n', ' ')
            .replace(' ', '_')
            .replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
            for c in clean.columns
        ]

        # Identify columns
        # Expected: establecimiento, estado, motivo, fecha, agente_detectado
        # But may vary by PDF version
        self.logger.info(f"Available columns: {list(clean.columns)}")

        # Mapping to target columns if they exist under different names
        col_mapping = {
            'nombre_del_establecimiento': 'establecimiento',
            'razon_social': 'establecimiento',
            'entidad_federativa': 'estado',
            'causa_de_la_sancion': 'motivo',
            'fecha_de_clausura': 'fecha',
            'irregularidades_detectadas': 'motivo',
            'giro': 'motivo'
        }

        for old, new in col_mapping.items():
            if old in clean.columns and new not in clean.columns:
                clean[new] = clean[old]

        # Filter by keywords
        keywords = ["CLENBUTEROL", "CLEMBUTEROL", "LMR", "SALMONELLA", "RASTRO", "CARNICERIA", "MATANZA", "POLLO", "CARNE", "ALIMENT"]
        pattern = '|'.join(keywords)

        # Look for keywords in all string columns (mostly 'motivo' or 'irregularidades')
        mask = clean.apply(lambda row: row.astype(str).str.contains(pattern, case=False, na=False).any(), axis=1)

        filtered = clean[mask].copy()
        self.logger.info(f"Filtered to {len(filtered)} rows matching keywords: {keywords}")

        # Normalize states
        if 'estado' in filtered.columns:
            # Simple normalization for exact matches in the dictionary
            # Reverse map for normalization? Actually ESTADOS_MEXICO is code -> full_name
            inv_estados = {v.upper(): k for k, v in ESTADOS_MEXICO.items()}

            def normalize_state(s):
                s = str(s).strip().upper()
                # Remove accents
                s = s.replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U')
                if s in inv_estados:
                    return s # or inv_estados[s] if we want the code
                # Try partial match or special cases
                if 'MEXICO' in s and 'CIUDAD' not in s: return 'MEXICO'
                if 'DISTRITO FEDERAL' in s: return 'CIUDAD DE MEXICO'
                return s

            filtered['estado_norm'] = filtered['estado'].apply(normalize_state)

        return filtered

if __name__ == "__main__":
    extractor = CofeprisClausurasExtractor()
    result = extractor.run()
    if not result.empty:
        print(f"Extracted {len(result)} rows.")
        print(result.head())
    else:
        print("No data extracted.")
