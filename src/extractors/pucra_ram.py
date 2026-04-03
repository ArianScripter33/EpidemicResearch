"""
PUCRA RAM Extractor — Wave 2 (Single-source hardening)
======================================================
Parses the 2024 PUCRA PDF into a tidy resistance table with one row per
organism, antibiotic, and period.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import pandas as pd
import pdfplumber
import requests

from src.base_extractor import BaseExtractor
from src.config import PUCRA_URLS, RAW_DIR, RESISTENCIA_AMPICILINA


class PucraRAMExtractor(BaseExtractor):
    """
    Strategy:
    1. Work against a single live source first (2024 report).
    2. Parse table text into tidy rows.
    3. Accept a manually downloaded local PDF when the host is unavailable.
    4. Keep exact source/page metadata for auditing.
    """

    TARGET_ORGANISMS = {
        re.compile(r"\b(?:Escherichia coli|E\. coli)\b", re.IGNORECASE): "Escherichia coli",
        re.compile(r"\b(?:Klebsiella pneumoniae|K\. pneumoniae)\b", re.IGNORECASE): "Klebsiella pneumoniae",
        re.compile(r"\bSalmonella(?: spp\.)?\b", re.IGNORECASE): "Salmonella spp.",
        re.compile(r"\b(?:Acinetobacter baumannii|A\. baumannii)\b", re.IGNORECASE): "Acinetobacter baumannii",
    }
    TARGET_ANTIBIOTICS = {
        re.compile(r"^Ampicilina\b", re.IGNORECASE): "Ampicilina",
        re.compile(r"^Carbenicilina\b", re.IGNORECASE): "Carbenicilina",
        re.compile(r"^Tetraciclina\b", re.IGNORECASE): "Tetraciclina",
        re.compile(r"^(?:TMP[-/ ]?SMX|Trimetoprim/?Sulfametoxazol)\b", re.IGNORECASE): "TMP-SMX",
        re.compile(r"^SAM\b", re.IGNORECASE): "Ampicilina/Sulbactam",
    }

    def __init__(self, years: Optional[Iterable[str]] = None):
        super().__init__(name="pucra_ram")
        self.years = list(years or ["2024"])

    def extract(self) -> pd.DataFrame:
        all_records: List[Dict[str, object]] = []

        for year in self.years:
            url = PUCRA_URLS.get(str(year))
            if not url:
                self.logger.warning(f"PUCRA source not configured for {year}")
                continue

            try:
                pdf_path = self._ensure_local_pdf(url)
            except Exception as exc:
                self.logger.warning(f"Skipping PUCRA {year}: {exc}")
                continue
            all_records.extend(self._extract_pdf_rows(pdf_path, year=str(year), source_url=url))

        if not all_records:
            return pd.DataFrame()

        return pd.DataFrame(all_records)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df

        clean = df.copy()
        clean["pct_resistencia"] = pd.to_numeric(clean["pct_resistencia"], errors="coerce")
        clean = clean.dropna(subset=["organismo", "antibiotico", "periodo"])
        clean = clean.drop_duplicates(
            subset=["source_report_year", "organismo", "antibiotico", "periodo", "page_num"]
        )
        clean = clean.sort_values(
            ["source_report_year", "organismo", "antibiotico", "periodo"]
        ).reset_index(drop=True)

        salmo_amp = clean[
            (clean["organismo"].str.contains("Salmonella", case=False, na=False))
            & (clean["antibiotico"].str.contains("Ampicilina", case=False, na=False))
        ]
        if not salmo_amp.empty:
            extracted_val = salmo_amp["pct_resistencia"].iloc[0]
            self.logger.info(
                "Cross-validation: Salmonella + Ampicilina = %.2f%% vs config %.2f%%",
                extracted_val,
                RESISTENCIA_AMPICILINA * 100,
            )

        return clean

    def _ensure_local_pdf(self, url: str) -> Path:
        filename = url.split("/")[-1]
        pdf_path = RAW_DIR / filename
        if pdf_path.exists() and pdf_path.stat().st_size > 0:
            return pdf_path

        candidate_paths = self._find_local_pdf_candidates(filename)
        if candidate_paths:
            chosen = candidate_paths[0]
            self.logger.info(f"Using existing local PUCRA PDF: {chosen.name}")
            return chosen

        RAW_DIR.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Downloading: {url}")
        self.logger.info(f"  → Target: {pdf_path}")
        try:
            response = requests.get(
                url,
                headers=dict(self.session.headers),
                timeout=(15, 30),
                stream=False,
            )
            response.raise_for_status()
            pdf_path.write_bytes(response.content)
            return pdf_path
        except Exception as exc:
            raise RuntimeError(
                "PUCRA host unavailable. Save the report manually under "
                f"{RAW_DIR / filename} or any matching pucra*.pdf file in data/raw/ and rerun."
            ) from exc

    def _find_local_pdf_candidates(self, filename: str) -> List[Path]:
        stem = Path(filename).stem
        patterns = [
            f"{filename}",
            f"*{stem}*.pdf",
            "*pucra*.pdf",
            "*PUCRA*.pdf",
            "*resistencia*antimicrobiana*.pdf",
            "*RAM*.pdf",
        ]

        matches: List[Path] = []
        for pattern in patterns:
            matches.extend(path for path in RAW_DIR.glob(pattern) if path.is_file() and path.stat().st_size > 0)

        unique_matches = list({path.resolve(): path for path in matches}.values())
        return sorted(
            unique_matches,
            key=lambda path: (
                0 if path.name == filename else 1,
                -path.stat().st_mtime,
                -path.stat().st_size,
            ),
        )

    def _extract_pdf_rows(self, pdf_path: Path, year: str, source_url: str) -> List[Dict[str, object]]:
        records: List[Dict[str, object]] = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                if not text.strip():
                    continue

                lines = [self._normalize_line(line) for line in text.splitlines() if self._normalize_line(line)]
                for organism, section_lines in self._split_page_sections(lines):
                    periods = self._extract_periods(section_lines)
                    for line in section_lines:
                        parsed_row = self._parse_antibiotic_row(line, periods)
                        if not parsed_row:
                            continue

                        for periodo, value in zip(parsed_row["periodos"], parsed_row["values"]):
                            if value == "ND":
                                continue
                            records.append(
                                {
                                    "source_report_year": year,
                                    "organismo": organism,
                                    "antibiotico": parsed_row["antibiotico"],
                                    "periodo": periodo,
                                    "pct_resistencia": value,
                                    "source_pdf": pdf_path.name,
                                    "page_num": page_num,
                                    "source_url": source_url,
                                    "raw_line": line,
                                }
                            )

        self.logger.info(f"Extracted {len(records)} tidy rows from {pdf_path.name}")
        return records

    @staticmethod
    def _normalize_line(line: str) -> str:
        return re.sub(r"\s+", " ", line or "").strip()

    def _match_organism(self, line: str) -> Optional[str]:
        for pattern, canonical in self.TARGET_ORGANISMS.items():
            if pattern.search(line):
                return canonical
        return None

    def _split_page_sections(self, lines: List[str]) -> List[Tuple[str, List[str]]]:
        sections: List[Tuple[str, List[str]]] = []
        current_organism: Optional[str] = None
        current_lines: List[str] = []

        for line in lines:
            matched_organism = self._match_organism(line)
            if matched_organism:
                if matched_organism == current_organism and current_lines:
                    current_lines.append(line)
                    continue
                if current_organism and current_lines:
                    sections.append((current_organism, current_lines))
                current_organism = matched_organism
                current_lines = [line]
                continue

            if current_organism:
                current_lines.append(line)

        if current_organism and current_lines:
            sections.append((current_organism, current_lines))

        return sections

    @staticmethod
    def _extract_periods(lines: List[str]) -> List[str]:
        ordered_periods: List[str] = []
        for line in lines:
            for year in re.findall(r"\b20\d{2}\b", line):
                if year not in ordered_periods:
                    ordered_periods.append(year)
            if "Promedio" in line and "Promedio" not in ordered_periods:
                ordered_periods.append("Promedio")
        return ordered_periods

    def _parse_antibiotic_row(self, line: str, periods: List[str]) -> Optional[Dict[str, object]]:
        for pattern, canonical in self.TARGET_ANTIBIOTICS.items():
            if not pattern.search(line):
                continue

            remainder = pattern.sub("", line, count=1).strip()
            values = re.findall(r"\b(?:ND|\d{1,3})\b", remainder)
            if not values:
                return None

            candidate_periods = periods[-len(values):] if periods and len(values) <= len(periods) else periods
            if not candidate_periods or len(candidate_periods) != len(values):
                candidate_periods = [f"value_{idx + 1}" for idx in range(len(values))]

            return {
                "antibiotico": canonical,
                "periodos": candidate_periods,
                "values": values,
            }

        return None


if __name__ == "__main__":
    extractor = PucraRAMExtractor()
    result = extractor.run()
    if not result.empty:
        print(f"Extracted {len(result)} tidy RAM rows.")
        print(result.head().to_string(index=False))
    else:
        print("No PUCRA rows extracted.")
