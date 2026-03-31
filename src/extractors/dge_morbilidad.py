"""
DGE Morbilidad Extractor — Wave 1 (Stable endpoint)
====================================================
Descarga anuarios de morbilidad de la Dirección General de Epidemiología.

Source: epidemiologia.salud.gob.mx/anuario/datos_abiertos/Anuario_{year}.zip
Format: ZIP → CSV (encoding: latin1)
Filter: CIE-10 codes A15-A19 (TB) + A05 (intoxicaciones alimentarias)

Output: DataFrame con casos de morbilidad filtrados por CIE-10
Feeds: ANOVA (slide 9) + EDA + correlación TB animal↔humano
"""

import io
import zipfile
from pathlib import Path
from typing import List, Optional

import pandas as pd

from src.base_extractor import BaseExtractor
from src.config import (
    CIE10_TARGET_ALL,
    CIE10_TB_ALL,
    CIE10_INTOXICACION_ALIMENTARIA,
    DGE_ANUARIO_URL_TEMPLATE,
    DGE_YEARS,
    HTTP_TIMEOUT,
    RAW_DIR,
)


class DGEMorbilidadExtractor(BaseExtractor):
    """
    Extrae datos de morbilidad humana de los Anuarios de la DGE.

    Strategy:
    1. Download ZIP for each year (2015-2022)
    2. Extract CSV(s) from each ZIP
    3. Filter by CIE-10 codes: TB (A15-A19) + Intoxicaciones (A05)
    4. Aggregate by state and year
    """

    def __init__(self, years: Optional[List[int]] = None):
        super().__init__(name="dge_morbilidad")
        self.years = years or DGE_YEARS

    def extract(self) -> pd.DataFrame:
        """
        Download and parse anuarios for all configured years.
        Continues even if some years fail.
        """
        all_frames = []
        successful_years = []
        failed_years = []

        for year in self.years:
            try:
                df = self._extract_year(year)
                if df is not None and not df.empty:
                    df["year_anuario"] = year
                    all_frames.append(df)
                    successful_years.append(year)
                    self.logger.info(f"  ✓ {year}: {len(df)} rows")
                else:
                    failed_years.append(year)
                    self.logger.warning(f"  ⚠ {year}: Empty or unparseable")
            except Exception as e:
                failed_years.append(year)
                self.logger.warning(f"  ⚠ {year} failed: {e}")
                continue

        self.logger.info(f"\nSummary: {len(successful_years)} years OK, {len(failed_years)} failed")
        if failed_years:
            self.logger.info(f"Failed years: {failed_years}")

        if all_frames:
            combined = pd.concat(all_frames, ignore_index=True)
            self.logger.info(f"Total rows extracted: {len(combined)}")
            return combined

        self.logger.warning("No data extracted from any year.")
        return pd.DataFrame()

    def _extract_year(self, year: int) -> Optional[pd.DataFrame]:
        """Download and parse a single anuario year."""
        url = DGE_ANUARIO_URL_TEMPLATE.format(year=year)
        self.logger.info(f"Fetching anuario {year}: {url}")

        response = self.session.get(url, timeout=HTTP_TIMEOUT)
        response.raise_for_status()

        # Save raw ZIP
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        zip_path = RAW_DIR / f"Anuario_{year}.zip"
        with open(zip_path, "wb") as f:
            f.write(response.content)

        # Extract CSVs from ZIP
        frames = []
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            csv_files = [f for f in z.namelist() if f.lower().endswith(".csv")]
            self.logger.info(f"  ZIP contains: {csv_files}")

            for csv_name in csv_files:
                try:
                    df = self._parse_csv_from_zip(z, csv_name)
                    if df is not None and not df.empty:
                        frames.append(df)
                except Exception as e:
                    self.logger.warning(f"  Could not parse {csv_name}: {e}")
                    continue

        if frames:
            return pd.concat(frames, ignore_index=True)
        return None

    def _parse_csv_from_zip(self, z: zipfile.ZipFile, csv_name: str) -> Optional[pd.DataFrame]:
        """Parse a CSV file from within a ZIP archive."""
        with z.open(csv_name) as f:
            content = f.read()

        # Try multiple encodings
        for encoding in ["latin1", "iso-8859-1", "cp1252", "utf-8"]:
            try:
                df = pd.read_csv(
                    io.BytesIO(content),
                    encoding=encoding,
                    low_memory=False,
                    on_bad_lines="skip",
                )
                if len(df) > 0:
                    df["source_file"] = csv_name
                    return df
            except (UnicodeDecodeError, pd.errors.ParserError):
                continue

        return None

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean, normalize, and filter DGE morbidity data.

        Steps:
        1. Normalize column names
        2. Identify CIE-10 column
        3. Filter by target codes (TB + intoxicaciones)
        4. Aggregate by state and year
        """
        if df.empty:
            return df

        clean = df.copy()

        # Normalize column names
        clean.columns = (
            clean.columns.str.strip()
            .str.lower()
            .str.replace(r"\s+", "_", regex=True)
        )

        self.logger.info(f"Columns available: {list(clean.columns)}")

        # Try to find the CIE-10 column
        cie_col = self._find_column(clean, ["cie10", "cie_10", "clave_cie", "diagnostico", "clave", "cve_diag", "clues"])

        if cie_col is None:
            self.logger.warning("Could not find CIE-10 column. Returning all data.")
            self.logger.info(f"Available columns: {list(clean.columns)}")
            return clean

        self.logger.info(f"CIE-10 column identified: '{cie_col}'")

        # Ensure CIE column is string
        clean[cie_col] = clean[cie_col].astype(str).str.strip().str.upper()

        # Filter by target CIE-10 codes
        mask = clean[cie_col].apply(
            lambda x: any(x.startswith(code) for code in CIE10_TARGET_ALL)
        )

        filtered = clean[mask].copy()
        self.logger.info(f"Filtered to {len(filtered)} rows matching CIE-10 targets")

        if not filtered.empty:
            # Tag disease category
            filtered["disease_category"] = filtered[cie_col].apply(self._categorize_cie10)

            # Summary
            for cat in filtered["disease_category"].unique():
                count = len(filtered[filtered["disease_category"] == cat])
                self.logger.info(f"  {cat}: {count} rows")

        return filtered

    @staticmethod
    def _find_column(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
        """Find the first matching column from a list of candidates."""
        for candidate in candidates:
            for col in df.columns:
                if candidate in col.lower():
                    return col
        return None

    @staticmethod
    def _categorize_cie10(code: str) -> str:
        """Categorize a CIE-10 code into disease group."""
        if any(code.startswith(c) for c in CIE10_TB_ALL):
            return "tuberculosis"
        elif any(code.startswith(c) for c in CIE10_INTOXICACION_ALIMENTARIA):
            return "intoxicacion_alimentaria"
        else:
            return "other"


# ═══════════════════════════════════════════════════
# CLI entry point
# ═══════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    # Allow specifying specific years from command line
    # Usage: python -m src.extractors.dge_morbilidad 2020 2021 2022
    if len(sys.argv) > 1:
        years = [int(y) for y in sys.argv[1:]]
    else:
        # Default: start with just 2022 for speed, expand later
        years = [2022]
        print("Tip: Using only 2022. Run with specific years for more data:")
        print("  python -m src.extractors.dge_morbilidad 2018 2019 2020 2021 2022")

    extractor = DGEMorbilidadExtractor(years=years)
    result = extractor.run()

    if not result.empty:
        print(f"\n{'='*60}")
        print(f"DGE Morbilidad — Extraction Complete")
        print(f"{'='*60}")
        print(f"Rows: {len(result)}")
        print(f"Columns: {list(result.columns)}")
        print(f"\nDisease categories:")
        if "disease_category" in result.columns:
            print(result["disease_category"].value_counts())
        print(f"\nData saved to: data/raw/ and data/processed/")
    else:
        print("\n⚠ No morbidity data extracted.")
        print("Fallback: Use prevalence values from V2.md for ANOVA (already hardcoded in config.py)")
