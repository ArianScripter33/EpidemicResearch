"""
COFEPRIS Clausuras Extractor — Wave 3 (Tidy repair)
===================================================
Repairs the parsing of the already-downloaded 2023/2024 verification PDFs.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Iterable, List

import pandas as pd
import pdfplumber

from src.base_extractor import BaseExtractor
from src.config import COFEPRIS_CLAUSURAS, ESTADOS_MEXICO, RAW_DIR


EXPECTED_COLUMNS = [
    "no",
    "establecimiento",
    "domicilio",
    "orden_verificacion",
    "fecha_inicio_visita",
    "fecha_termino_visita",
    "giro_actividad",
    "motivo_visita",
]


class CofeprisClausurasExtractor(BaseExtractor):
    """
    Parse the local 2023/2024 PDFs into a stable eight-column schema and then
    filter rows useful for the project proxy.
    """

    KEYWORDS = [
        "CLENBUTEROL",
        "CLEMBUTEROL",
        "LMR",
        "SALMONELLA",
        "RASTRO",
        "CARNICERIA",
        "MATANZA",
        "POLLO",
        "CARNE",
        "ALIMENT",
        "RES",
        "BOVIN",
        "AVICOLA",
    ]

    def __init__(self):
        super().__init__(name="cofepris_clausuras")

    def extract(self) -> pd.DataFrame:
        pdf_paths = self._resolve_pdf_paths()
        all_rows: List[Dict[str, object]] = []

        for pdf_path in pdf_paths:
            all_rows.extend(self._extract_pdf_rows(pdf_path))

        if not all_rows:
            return pd.DataFrame()

        return pd.DataFrame(all_rows)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df

        clean = df.copy()
        for column in EXPECTED_COLUMNS:
            clean[column] = clean[column].astype(str).str.replace(r"\s+", " ", regex=True).str.strip()

        keyword_pattern = "|".join(self.KEYWORDS)
        mask = clean[["establecimiento", "domicilio", "giro_actividad", "motivo_visita"]].apply(
            lambda column: column.str.contains(keyword_pattern, case=False, na=False)
        ).any(axis=1)

        filtered = clean[mask].copy()
        filtered["estado_norm"] = filtered["domicilio"].apply(self._extract_state_from_address)
        filtered = filtered.drop_duplicates(subset=["source_pdf", "orden_verificacion"])
        filtered = filtered.sort_values(["source_pdf", "no"]).reset_index(drop=True)
        return filtered

    def _resolve_pdf_paths(self) -> List[Path]:
        preferred = [
            RAW_DIR / "Listado_de_Establecimientos_Verificados__2024.pdf",
            RAW_DIR / "Listado_de_Establecimientos_Verificados__2023.pdf",
        ]
        existing = [path for path in preferred if path.exists()]
        if existing:
            return existing

        self.logger.info("No local COFEPRIS PDFs found. Falling back to remote discovery.")
        return [self.download_file(url, filename=url.split("/")[-1]) for url in self._discover_remote_pdfs()]

    def _discover_remote_pdfs(self) -> List[str]:
        response = self.session.get(COFEPRIS_CLAUSURAS, timeout=30)
        response.raise_for_status()
        html = response.text
        urls = sorted(
            {
                url if url.startswith("http") else f"https://www.gob.mx{url}"
                for url in re.findall(r'href="([^"]+Listado_de_Establecimientos_Verificados[^"]+\.pdf)"', html)
            }
        )
        return urls[:2]

    def _extract_pdf_rows(self, pdf_path: Path) -> List[Dict[str, object]]:
        rows: List[Dict[str, object]] = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                tables = page.extract_tables()
                if not tables:
                    continue

                for table in tables:
                    rows.extend(self._extract_table_rows(table, pdf_path.name, page_num))

        self.logger.info(f"Parsed {len(rows)} tidy COFEPRIS rows from {pdf_path.name}")
        return rows

    def _extract_table_rows(self, table: List[List[str]], source_pdf: str, page_num: int) -> List[Dict[str, object]]:
        rows: List[Dict[str, object]] = []
        if not table:
            return rows

        start_idx = 0
        if len(table) > 1 and self._looks_like_header_banner(table[0]):
            start_idx = 2

        for raw_row in table[start_idx:]:
            normalized = [self._normalize_cell(cell) for cell in raw_row[: len(EXPECTED_COLUMNS)]]
            if len(normalized) < len(EXPECTED_COLUMNS):
                continue
            if not self._looks_like_data_row(normalized):
                continue

            record = dict(zip(EXPECTED_COLUMNS, normalized))
            record["source_pdf"] = source_pdf
            record["page_num"] = page_num
            rows.append(record)

        return rows

    @staticmethod
    def _normalize_cell(cell: object) -> str:
        return re.sub(r"\s+", " ", str(cell or "")).strip()

    @staticmethod
    def _looks_like_header_banner(row: List[str]) -> bool:
        joined = " ".join(str(cell or "") for cell in row).upper()
        return "LICENCIA SANITARIA" in joined or "MOTIVO DE VISITA" in joined

    @staticmethod
    def _looks_like_data_row(row: List[str]) -> bool:
        return (
            len(row) == len(EXPECTED_COLUMNS)
            and row[0].isdigit()
            and row[1].upper() != "ESTABLECIMIENTO"
            and bool(re.search(r"\d{2}-MF-", row[3]))
            and bool(re.search(r"\d{2}/\d{2}/\d{4}", row[4]))
        )

    @staticmethod
    def _extract_state_from_address(address: str) -> str:
        normalized = (
            address.upper()
            .replace("Á", "A")
            .replace("É", "E")
            .replace("Í", "I")
            .replace("Ó", "O")
            .replace("Ú", "U")
        )
        state_names = {value.upper(): value for value in ESTADOS_MEXICO.values()}
        for state_upper, canonical in state_names.items():
            if state_upper.upper() in normalized:
                return canonical
        if "CIUDAD DE MEXICO" in normalized:
            return "Ciudad de México"
        if re.search(r"\bMEXICO\b", normalized):
            return "Estado de México"
        return "SIN_ESTADO"


if __name__ == "__main__":
    extractor = CofeprisClausurasExtractor()
    result = extractor.run()
    if not result.empty:
        print(f"Extracted {len(result)} tidy COFEPRIS rows.")
        print(result.head().to_string(index=False))
    else:
        print("No COFEPRIS rows extracted.")
