"""
DGE Morbilidad 2018-2024 Extractor — National PDF Recovery
===========================================================
Recovers national morbidity rows for A05 and tuberculosis codes from the
post-2017 DGE PDF reports and consolidates them with the pre-2018 state CSVs.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import pandas as pd
import pdfplumber

from src.base_extractor import BaseExtractor
from src.config import (
    DGE_NATIONAL_PDF_URL_TEMPLATE,
    DGE_NATIONAL_REPORT_NAME,
    DGE_PDF_YEARS,
    PROCESSED_DIR,
    RAW_DIR,
)


TARGET_TOKEN_PATTERN = re.compile(r"\bA(?:05|1[5-9])(?:\.\d+)?(?:-A?(?:05|1[5-9])(?:\.\d+)?)?\b")
CIE_CAPTURE_PATTERN = re.compile(
    r"(?P<cie>A(?:05|1[5-9])(?:\.\d+)?(?:-A?(?:05|1[5-9])(?:\.\d+)?)?"
    r"(?:,\s*A(?:05|1[5-9])(?:\.\d+)?(?:-A?(?:05|1[5-9])(?:\.\d+)?)?)*)"
)
NUMBER_BLOCK_PATTERN = re.compile(r"\d[\d ]*")


class DGEMorbilidad20182024Extractor(BaseExtractor):
    """
    Extract national DGE morbidity rows from PDF reports for 2018-2024.

    Output schema:
    - year_anuario
    - report_name
    - cve_cie10
    - des_diagno
    - acumulado_nacional
    - source_pdf
    - source_page
    - extraction_method
    """

    REPORT_NAME = DGE_NATIONAL_REPORT_NAME

    def __init__(self, years: Optional[Iterable[int]] = None):
        super().__init__(name="dge_morbilidad_2018_2024")
        self.years = list(years or DGE_PDF_YEARS)

    def extract(self) -> pd.DataFrame:
        frames: List[pd.DataFrame] = []

        for year in self.years:
            pdf_path = self._ensure_local_pdf(year)
            records = self._extract_year(year, pdf_path)
            if records:
                frame = pd.DataFrame(records)
                frames.append(frame)
                self.logger.info(f"  ✓ {year}: {len(frame)} target rows")
            else:
                self.logger.warning(f"  ⚠ {year}: No target rows found")

        if not frames:
            return pd.DataFrame()

        return pd.concat(frames, ignore_index=True)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df

        clean = df.copy()
        clean["year_anuario"] = pd.to_numeric(clean["year_anuario"], errors="coerce").astype("Int64")
        clean["acumulado_nacional"] = pd.to_numeric(clean["acumulado_nacional"], errors="coerce").astype("Int64")
        clean["source_page"] = pd.to_numeric(clean["source_page"], errors="coerce").astype("Int64")
        clean["cve_cie10"] = clean["cve_cie10"].astype(str).str.replace(r"\s+", " ", regex=True).str.strip()
        clean["des_diagno"] = clean["des_diagno"].astype(str).str.replace(r"\s+", " ", regex=True).str.strip()
        clean["report_name"] = clean["report_name"].fillna(self.REPORT_NAME)
        clean["extraction_method"] = clean["extraction_method"].fillna("pdfplumber_text")
        clean = clean.drop_duplicates(
            subset=["year_anuario", "report_name", "cve_cie10", "des_diagno"]
        )
        clean = clean.sort_values(["year_anuario", "cve_cie10", "des_diagno"]).reset_index(drop=True)
        return clean

    def _ensure_local_pdf(self, year: int) -> Path:
        filename = f"dge_{year}_{self.REPORT_NAME}.pdf"
        pdf_path = RAW_DIR / filename
        if pdf_path.exists() and pdf_path.stat().st_size > 0:
            return pdf_path

        url = DGE_NATIONAL_PDF_URL_TEMPLATE.format(year=year, report_name=self.REPORT_NAME)
        return self.download_file(url, filename=filename)

    def _extract_year(self, year: int, pdf_path: Path) -> List[Dict[str, object]]:
        records = self._extract_with_pdfplumber(year, pdf_path)
        if records:
            return records

        self.logger.info(f"  Trying docling fallback for {year}")
        return self._extract_with_docling(year, pdf_path)

    def _extract_with_pdfplumber(self, year: int, pdf_path: Path) -> List[Dict[str, object]]:
        records: List[Dict[str, object]] = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                words = page.extract_words(use_text_flow=True, keep_blank_chars=False)
                if words:
                    for row_words in self._group_words_by_row(words):
                        parsed = self._parse_pdfplumber_row(row_words)
                        if not parsed:
                            continue
                        parsed.update(
                            {
                                "year_anuario": year,
                                "report_name": self.REPORT_NAME,
                                "source_pdf": pdf_path.name,
                                "source_page": page_num,
                                "extraction_method": "pdfplumber_words",
                            }
                        )
                        records.append(parsed)
                    continue

                text = page.extract_text() or ""
                records.extend(
                    self._parse_text_lines(
                        text.splitlines(),
                        year=year,
                        source_pdf=pdf_path.name,
                        source_page=page_num,
                        extraction_method="pdfplumber_text",
                    )
                )
        return records

    def _extract_with_docling(self, year: int, pdf_path: Path) -> List[Dict[str, object]]:
        try:
            from docling.document_converter import DocumentConverter
        except Exception as exc:
            self.logger.warning(f"  docling unavailable: {exc}")
            return []

        try:
            result = DocumentConverter().convert(str(pdf_path))
            markdown = result.document.export_to_markdown()
        except Exception as exc:
            self.logger.warning(f"  docling failed for {pdf_path.name}: {exc}")
            return []

        return self._parse_text_lines(
            markdown.splitlines(),
            year=year,
            source_pdf=pdf_path.name,
            source_page=None,
            extraction_method="docling_markdown",
        )

    def _parse_text_lines(
        self,
        lines: Iterable[str],
        year: int,
        source_pdf: str,
        source_page: Optional[int],
        extraction_method: str,
    ) -> List[Dict[str, object]]:
        records: List[Dict[str, object]] = []
        previous_line = ""

        for raw_line in lines:
            line = self._normalize_line(raw_line)
            if not line:
                continue

            candidates = [line]
            if previous_line:
                candidates.append(f"{previous_line} {line}")

            parsed = None
            for candidate in candidates:
                parsed = self._parse_target_line(candidate)
                if parsed:
                    break

            if parsed:
                parsed.update(
                    {
                        "year_anuario": year,
                        "report_name": self.REPORT_NAME,
                        "source_pdf": source_pdf,
                        "source_page": source_page,
                        "extraction_method": extraction_method,
                    }
                )
                records.append(parsed)

            previous_line = line

        return records

    @staticmethod
    def _normalize_line(line: str) -> str:
        return re.sub(r"\s+", " ", line or "").strip()

    @classmethod
    def _parse_target_line(cls, line: str) -> Optional[Dict[str, object]]:
        if not TARGET_TOKEN_PATTERN.search(line):
            return None

        cie_match = CIE_CAPTURE_PATTERN.search(line)
        if not cie_match:
            return None

        diagnosis = cls._normalize_line(line[: cie_match.start()])
        remainder = cls._normalize_line(line[cie_match.end() :])
        numeric_tokens = re.findall(r"\d{1,3}", remainder)
        if not diagnosis or not numeric_tokens:
            return None

        acumulado = cls._parse_first_numeric_value(numeric_tokens)
        return {
            "cve_cie10": cls._normalize_line(cie_match.group("cie")),
            "des_diagno": diagnosis,
            "acumulado_nacional": acumulado,
        }

    @staticmethod
    def _parse_first_numeric_value(tokens: List[str]) -> int:
        if len(tokens) >= 2 and len(tokens[0]) < 3 and len(tokens[1]) == 3:
            return int(tokens[0] + tokens[1])
        return int(tokens[0])

    @staticmethod
    def _group_words_by_row(words: List[Dict[str, object]], tolerance: float = 2.5) -> List[List[Dict[str, object]]]:
        rows: List[List[Dict[str, object]]] = []
        for word in sorted(words, key=lambda item: (item["top"], item["x0"])):
            if not rows or abs(rows[-1][0]["top"] - word["top"]) > tolerance:
                rows.append([word])
            else:
                rows[-1].append(word)
        return rows

    @classmethod
    def _parse_pdfplumber_row(cls, row_words: List[Dict[str, object]]) -> Optional[Dict[str, object]]:
        sorted_words = sorted(row_words, key=lambda item: item["x0"])
        texts = [cls._normalize_line(word["text"]) for word in sorted_words]
        if not any(TARGET_TOKEN_PATTERN.search(text) for text in texts):
            return None

        first_code_idx = next((idx for idx, text in enumerate(texts) if TARGET_TOKEN_PATTERN.search(text)), None)
        if first_code_idx is None or first_code_idx == 0:
            return None

        code_tokens: List[str] = []
        numeric_words: List[Dict[str, object]] = []
        for word in sorted_words[first_code_idx:]:
            text = cls._normalize_line(word["text"])
            if re.fullmatch(r"\d{1,3}", text):
                numeric_words.append(word)
            elif numeric_words:
                break
            else:
                code_tokens.append(text)

        if not code_tokens or not numeric_words:
            return None

        diagnosis = cls._normalize_line(" ".join(texts[:first_code_idx]))
        cie_code = cls._normalize_line(" ".join(code_tokens))
        first_numeric_group = cls._group_adjacent_numeric_words(numeric_words)[0]
        acumulado = int("".join(first_numeric_group))

        return {
            "cve_cie10": cie_code,
            "des_diagno": diagnosis,
            "acumulado_nacional": acumulado,
        }

    @staticmethod
    def _group_adjacent_numeric_words(
        numeric_words: List[Dict[str, object]],
        max_gap: float = 8.0,
    ) -> List[List[str]]:
        groups: List[List[str]] = []
        current: List[str] = []
        previous_x1: Optional[float] = None

        for word in sorted(numeric_words, key=lambda item: item["x0"]):
            text = str(word["text"])
            if previous_x1 is None or float(word["x0"]) - previous_x1 <= max_gap:
                current.append(text)
            else:
                groups.append(current)
                current = [text]
            previous_x1 = float(word["x1"])

        if current:
            groups.append(current)

        return groups


class DGENationalSeriesConsolidator(BaseExtractor):
    """
    Build a single national 2015-2024 series without mutating the existing state CSV.
    """

    def __init__(self):
        super().__init__(name="dge_morbilidad_nacional_2015_2024")

    def extract(self) -> pd.DataFrame:
        pre_2018_path = PROCESSED_DIR / "dge_morbilidad_clean.csv"
        post_2017_path = PROCESSED_DIR / "dge_morbilidad_2018_2024_clean.csv"

        if not pre_2018_path.exists():
            raise FileNotFoundError(f"Missing pre-2018 dataset: {pre_2018_path}")

        if not post_2017_path.exists():
            self.logger.info("Post-2017 national file not found. Running DGE 2018-2024 extractor first.")
            DGEMorbilidad20182024Extractor().run()

        pre_df = pd.read_csv(pre_2018_path)
        post_df = pd.read_csv(post_2017_path)
        return self.build_national_from_frames(pre_df, post_df)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df

        clean = df.copy()
        clean["year_anuario"] = pd.to_numeric(clean["year_anuario"], errors="coerce").astype("Int64")
        clean["acumulado_nacional"] = pd.to_numeric(clean["acumulado_nacional"], errors="coerce").astype("Int64")
        clean = clean.drop_duplicates(subset=["year_anuario", "cve_cie10", "des_diagno", "report_name"])
        clean = clean.sort_values(["year_anuario", "cve_cie10", "des_diagno"]).reset_index(drop=True)
        return clean

    @staticmethod
    def build_national_from_frames(pre_2018: pd.DataFrame, post_2017: pd.DataFrame) -> pd.DataFrame:
        pre = pre_2018.copy()
        pre["year_anuario"] = pd.to_numeric(pre["year_anuario"], errors="coerce")
        pre["acumulado"] = pd.to_numeric(pre["acumulado"], errors="coerce")
        pre = (
            pre.groupby(["year_anuario", "cve_cie10", "des_diagno"], as_index=False)["acumulado"]
            .sum()
            .rename(columns={"acumulado": "acumulado_nacional"})
        )
        pre["report_name"] = "state_aggregate_from_csv"
        pre["source_pdf"] = "dge_morbilidad_clean.csv"
        pre["source_page"] = pd.NA
        pre["extraction_method"] = "state_csv_aggregate"

        post = post_2017[
            [
                "year_anuario",
                "report_name",
                "cve_cie10",
                "des_diagno",
                "acumulado_nacional",
                "source_pdf",
                "source_page",
                "extraction_method",
            ]
        ].copy()

        combined = pd.concat([pre, post], ignore_index=True, sort=False)
        ordered_columns = [
            "year_anuario",
            "report_name",
            "cve_cie10",
            "des_diagno",
            "acumulado_nacional",
            "source_pdf",
            "source_page",
            "extraction_method",
        ]
        return combined[ordered_columns]


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Recover DGE national morbidity data from PDFs.")
    parser.add_argument("--years", nargs="*", type=int, help="Specific years to process, e.g. 2018 2019 2024")
    parser.add_argument(
        "--skip-consolidation",
        action="store_true",
        help="Run only the national PDF extractor and skip the 2015-2024 consolidation step.",
    )
    return parser


if __name__ == "__main__":
    args = _build_arg_parser().parse_args()
    extractor = DGEMorbilidad20182024Extractor(years=args.years)
    national_result = extractor.run()

    if national_result.empty:
        print("No national DGE rows extracted from the PDFs.")
    else:
        print(f"Recovered {len(national_result)} national DGE rows.")

    if not args.skip_consolidation:
        consolidated = DGENationalSeriesConsolidator().run()
        if consolidated.empty:
            print("National 2015-2024 consolidation returned no rows.")
        else:
            print(f"Built national 2015-2024 series with {len(consolidated)} rows.")
