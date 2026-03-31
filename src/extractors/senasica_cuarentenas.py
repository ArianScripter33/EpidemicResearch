"""
SENASICA Quarantine Extractor — Wave 1.5
=========================================
Extracts quarterly quarantine data from SENASICA PDFs (2023-2024).

Source: https://www.gob.mx/senasica/documentos/cuarentenas-tuberculosis-bovina-2024?state=published
Output: data/processed/senasica_cuarentenas_clean.csv
"""

import re
from pathlib import Path
from typing import List, Optional

import pandas as pd
import pdfplumber

from src.base_extractor import BaseExtractor
from src.config import (
    SENASICA_CUARENTENAS_PDFS,
    ESTADOS_MEXICO,
)


class SenasicaCuarentenasExtractor(BaseExtractor):
    """
    Extractor for SENASICA Tuberculosis Bovina quarantine reports.
    Parses quarterly PDFs using pdfplumber.
    """

    def __init__(self):
        super().__init__(name="senasica_cuarentenas")
        # Add 2023 URLs (inferred/found)
        self.urls_2023 = {
            "q4_2023": "https://www.gob.mx/cms/uploads/attachment/file/890479/1_CUARENTENAS_CUARTO_2023.pdf",
            "q3_2023": "https://www.gob.mx/cms/uploads/attachment/file/868285/1_CUARENTENAS_TERCER_2023.pdf",
            "q2_2023": "https://www.gob.mx/cms/uploads/attachment/file/845453/1_CUARENTENAS_SEGUNDO_2023.pdf",
            "q1_2023": "https://www.gob.mx/cms/uploads/attachment/file/817234/1_CUARENTENAS_Primer_2023.pdf",
        }

    def extract(self) -> pd.DataFrame:
        """
        Download and parse all quarterly PDFs.
        """
        all_data = []

        # Process 2024 (from config)
        for q, url in SENASICA_CUARENTENAS_PDFS.items():
            year = 2024
            quarter = int(q[1])
            df = self._process_pdf(url, year, quarter)
            if not df.empty:
                all_data.append(df)

        # Process 2023
        for q, url in self.urls_2023.items():
            year = 2023
            quarter = int(q[1])
            try:
                df = self._process_pdf(url, year, quarter)
                if not df.empty:
                    all_data.append(df)
            except Exception as e:
                self.logger.warning(f"Could not process {q}: {e}")

        if not all_data:
            return pd.DataFrame()

        return pd.concat(all_data, ignore_index=True)

    def _process_pdf(self, url: str, year: int, quarter: int) -> pd.DataFrame:
        """Download and parse a single PDF."""
        self.logger.info(f"Processing {year} Q{quarter}: {url}")

        try:
            pdf_path = self.download_file(url)
        except Exception as e:
            self.logger.error(f"Failed to download {url}: {e}")
            return pd.DataFrame()

        raw_rows = self._parse_tables(pdf_path)

        if not raw_rows:
            self.logger.warning(f"No table data found in {pdf_path}")
            return pd.DataFrame()

        df = pd.DataFrame(raw_rows)
        # Add temporal metadata
        df["anio"] = year
        df["trimestre"] = quarter
        df["fecha"] = f"{year}-Q{quarter}"
        df["source_url"] = url

        return df

    def _parse_tables(self, pdf_path: Path) -> List[dict]:
        """
        Extract quarantine data rows from PDF.
        Targets tables with state-level metrics.
        """
        extracted_rows = []

        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if not text: continue

                # Try table extraction first
                tables = page.extract_tables()
                if tables:
                    for table in tables:
                        if not table or len(table) < 2: continue
                        headers = None
                        start_idx = 0
                        for row_idx, row in enumerate(table):
                            potential_headers = [str(c).strip().upper() for c in row if c]
                            if any("ESTADO" in h or "ENTIDAD" in h for h in potential_headers) and \
                               any("HATO" in h or "CUARENTENA" in h for h in potential_headers):
                                headers = [str(c).strip().upper() if c else "" for c in row]
                                start_idx = row_idx + 1
                                break

                        if headers:
                            self.logger.info(f"  Found table on page {i+1}")
                            for row in table[start_idx:]:
                                clean_row = [str(c).strip() if c else "" for c in row]
                                if not any(clean_row) or "TOTAL" in clean_row[0].upper(): continue
                                entry = self._map_row_to_schema(clean_row, headers)
                                if entry: extracted_rows.append(entry)
                            return extracted_rows # Found it

                # Fallback to regex text parsing if table extraction fails or is messy
                # Looking for: State [Zone] Hatos Preventivas Despoblación
                self.logger.info(f"  Attempting regex parsing on page {i+1}")
                lines = text.split('\n')
                current_state = None
                for line in lines:
                    line = line.strip()
                    if not line or "TOTAL" in line.upper() or "PERIODO" in line.upper(): continue

                    # Pattern for state names (usually start with uppercase)
                    state_match = re.match(r'^([A-Z][a-zñáéíóú\s]+(?:\sLagunera)?)\s*(?:[AB][123]?)?\s+([\d,]+\s+[\d,]+\s+[\d,]+.*)', line)
                    if state_match:
                        state_name = state_match.group(1).strip()
                        data_part = state_match.group(2).strip().split()

                        entry = {
                            "estado": state_name,
                            "num_hatos_cuarentena": data_part[0] if len(data_part) > 0 else "0",
                            "num_animales": data_part[3] if len(data_part) > 3 else "0", # Based on 2024 PDF structure
                            "tipo_medida": "Cuarentena",
                        }
                        extracted_rows.append(entry)
                    elif re.match(r'^[A-Z][a-zñáéíóú\s]+(?:\sLagunera)?$', line):
                        current_state = line
                    elif current_state and re.match(r'^[AB][123]?\s+([\d,]+\s+[\d,]+\s+[\d,]+.*)', line):
                        data_part = line.split()[1:]
                        entry = {
                            "estado": current_state,
                            "num_hatos_cuarentena": data_part[0] if len(data_part) > 0 else "0",
                            "num_animales": data_part[3] if len(data_part) > 3 else "0",
                            "tipo_medida": "Cuarentena",
                        }
                        extracted_rows.append(entry)

        return extracted_rows

    def _map_row_to_schema(self, row: List[str], headers: List[str]) -> Optional[dict]:
        """Maps raw table row to standard schema."""
        entry = {
            "estado": "",
            "num_hatos_cuarentena": "0",
            "num_animales": "0",
            "tipo_medida": "Cuarentena",
        }

        for i, val in enumerate(row):
            if i >= len(headers): break
            h = headers[i]

            if not h: continue

            if "ESTADO" in h or "ENTIDAD" in h:
                entry["estado"] = val
            elif "HATO" in h:
                entry["num_hatos_cuarentena"] = val
            elif "ANIMAL" in h or "CABEZA" in h:
                entry["num_animales"] = val
            elif "MEDIDA" in h or "TIPO" in h:
                entry["tipo_medida"] = val

        if not entry["estado"] or "ESTADO" in entry["estado"].upper() or "TOTAL" in entry["estado"].upper():
            return None

        return entry

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and normalize extracted quarantine data.
        """
        if df.empty:
            return df

        clean = df.copy()

        # 1. Normalize State Names
        clean["estado"] = clean["estado"].str.strip().str.upper()

        # Reverse mapping for ESTADOS_MEXICO to match names
        name_to_abbr = {v.upper(): k for k, v in ESTADOS_MEXICO.items()}

        def normalize_state(name):
            name = name.replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U")
            name = name.replace("Ñ", "N")

            # Try direct match
            if name in name_to_abbr:
                return ESTADOS_MEXICO[name_to_abbr[name]]
            # Try fuzzy match (contained)
            for std_name in name_to_abbr.keys():
                # Remove accents from std_name too just in case
                std_clean = std_name.replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U").replace("Ñ", "N")
                if std_clean in name or name in std_clean:
                    return ESTADOS_MEXICO[name_to_abbr[std_name]]
            return name.title()

        clean["estado"] = clean["estado"].apply(normalize_state)

        # 2. Clean numeric columns
        for col in ["num_hatos_cuarentena", "num_animales"]:
            clean[col] = (
                clean[col]
                .astype(str)
                .str.replace(",", "")
                .str.replace(r"[^\d]", "", regex=True)
            )
            clean[col] = pd.to_numeric(clean[col], errors="coerce").fillna(0).astype(int)

        # 3. Handle duplicates (if multiple tables per PDF)
        clean = clean.drop_duplicates(subset=["estado", "anio", "trimestre", "tipo_medida"])

        return clean


if __name__ == "__main__":
    extractor = SenasicaCuarentenasExtractor()
    result = extractor.run()

    if not result.empty:
        print(f"\nExtracted {len(result)} rows of quarantine data.")
        print(result.head())
    else:
        print("Extraction failed or no data found.")
