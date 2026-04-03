"""
openFMD Extractor — Wave 2 (International FMD data)
====================================================
Descarga datos globales de brotes de Fiebre Aftosa desde openFMD/FMDwatch.

Source: openfmd.org/dashboard/fmdwatch/
Format: CSV (download button on dashboard)

This extractor also includes a fallback to WAHIS/WOAH data via the
community-maintained ReportRetriever.

Output: DataFrame con brotes FMD por país/fecha
Feeds: Validación de R0 + Series temporales para Chronos (Tier 2)
"""

from pathlib import Path

import pandas as pd

from src.base_extractor import BaseExtractor
from src.config import (
    KAGGLE_FMD_DATASET,
    OPENFMD_DASHBOARD,
    RAW_DIR,
)


class OpenFMDExtractor(BaseExtractor):
    """
    Extrae datos de brotes de Fiebre Aftosa a nivel global.

    Strategy:
    1. Normalize a browser-assisted export already saved in data/raw/
    2. If unavailable, use Kaggle only when credentials are configured
    3. If both fail, fall back to a literature reference dataset
    """

    def __init__(self):
        super().__init__(name="openfmd")

    def extract(self) -> pd.DataFrame:
        """
        Normalize real exports first, then fall back to literature.
        """
        try:
            df = self._load_local_browser_export()
            if df is not None and not df.empty:
                self.logger.info(f"Loaded {len(df)} rows from a local openFMD export")
                return df
        except Exception as e:
            self.logger.warning(f"Local openFMD export failed: {e}")

        try:
            df = self._try_kaggle_dataset()
            if df is not None and not df.empty:
                self.logger.info(f"Loaded {len(df)} rows from Kaggle dataset {KAGGLE_FMD_DATASET}")
                return df
        except Exception as e:
            self.logger.warning(f"Kaggle fallback failed: {e}")

        self.logger.info("All sources failed. Generating reference data from literature.")
        return self._generate_literature_reference()

    def _load_local_browser_export(self) -> pd.DataFrame | None:
        """
        Prefer browser-assisted CSV exports already saved in data/raw/.
        """
        patterns = ("*openfmd*.csv", "*fmdwatch*.csv", "*wahis*.csv")
        candidates: list[Path] = []
        for pattern in patterns:
            candidates.extend(RAW_DIR.glob(pattern))

        candidates = [
            path for path in candidates
            if path.name not in {"openfmd_raw.csv", "openfmd_clean.csv"}
        ]
        candidates = sorted(set(candidates), key=lambda p: p.stat().st_mtime, reverse=True)

        for path in candidates:
            if self._looks_like_html(path):
                self.logger.warning(f"Skipping {path.name}: downloaded artifact is HTML, not CSV")
                continue
            df = self._read_csv_with_fallbacks(path)
            if df is not None and not df.empty:
                if len(df.columns) == 1 and "<!doctype html" in str(df.columns[0]).lower():
                    self.logger.warning(f"Skipping {path.name}: parsed as a single HTML column")
                    continue
                df["source_file"] = path.name
                if "data_type" not in df.columns:
                    df["data_type"] = "browser_export"
                return df

        return None

    @staticmethod
    def _looks_like_html(path: Path) -> bool:
        try:
            sample = path.read_text(encoding="utf-8", errors="ignore")[:2048].lower()
        except Exception:
            return False
        return "<!doctype html" in sample or "<html" in sample

    @staticmethod
    def _read_csv_with_fallbacks(path: Path) -> pd.DataFrame | None:
        for kwargs in (
            {"sep": None, "engine": "python"},
            {"sep": ","},
            {"sep": ";"},
            {"sep": "\t"},
        ):
            try:
                df = pd.read_csv(path, **kwargs)
                if not df.empty:
                    return df
            except Exception:
                continue
        return None

    def _try_kaggle_dataset(self) -> pd.DataFrame | None:
        """
        Use Kaggle only if credentials are already configured.
        """
        try:
            from src.extractors.kaggle_fmd import KaggleFMDExtractor
        except Exception:
            return None

        df = KaggleFMDExtractor().extract()
        if df is not None and not df.empty:
            df["source_file"] = f"kaggle:{KAGGLE_FMD_DATASET}"
            if "data_type" not in df.columns:
                df["data_type"] = "kaggle_dataset"
        return df

    def _generate_literature_reference(self) -> pd.DataFrame:
        """
        Generate a reference DataFrame from published literature.
        This is NOT real data — it's a structured summary of known R0 estimates
        and outbreak parameters for FMD from peer-reviewed sources.

        Used when we can't access live data sources.
        """
        self.logger.info("Generating reference dataset from literature...")

        reference_data = [
            # UK 2001 outbreak
            {
                "country": "United Kingdom",
                "region": "Europe",
                "year": 2001,
                "outbreak_name": "UK 2001 Epidemic",
                "R0_estimate": 6.0,
                "R0_range_low": 4.0,
                "R0_range_high": 8.0,
                "total_cases_farms": 2026,
                "animals_culled": 6_000_000,
                "duration_days": 221,
                "cost_usd_billions": 16.0,
                "source": "Tildesley et al. (2006), DEFRA",
            },
            # Argentina 2001
            {
                "country": "Argentina",
                "region": "Americas",
                "year": 2001,
                "outbreak_name": "Argentina 2001",
                "R0_estimate": 5.5,
                "R0_range_low": 3.0,
                "R0_range_high": 7.0,
                "total_cases_farms": None,
                "animals_culled": None,
                "duration_days": None,
                "cost_usd_billions": None,
                "source": "PANAFTOSA/OPS",
            },
            # Colombia 2017 (last major Americas event)
            {
                "country": "Colombia",
                "region": "Americas",
                "year": 2017,
                "outbreak_name": "Colombia 2017 (Serotype O)",
                "R0_estimate": 4.5,
                "R0_range_low": 3.0,
                "R0_range_high": 6.0,
                "total_cases_farms": None,
                "animals_culled": None,
                "duration_days": None,
                "cost_usd_billions": None,
                "source": "WOAH WAHIS Reports",
            },
            # Europe 2023-2025 (recent outbreaks, FAO alert Jan 2025)
            {
                "country": "Germany",
                "region": "Europe",
                "year": 2025,
                "outbreak_name": "Germany 2025 (Serotype O)",
                "R0_estimate": 5.0,
                "R0_range_low": 3.5,
                "R0_range_high": 7.0,
                "total_cases_farms": None,
                "animals_culled": None,
                "duration_days": None,
                "cost_usd_billions": None,
                "source": "FAO Alert Jan 2025, WOAH",
            },
            # Turkey/Near East 2024-2025
            {
                "country": "Turkey",
                "region": "Near East",
                "year": 2024,
                "outbreak_name": "Turkey 2024-2025 (Ongoing)",
                "R0_estimate": 5.5,
                "R0_range_low": 4.0,
                "R0_range_high": 8.0,
                "total_cases_farms": None,
                "animals_culled": None,
                "duration_days": None,
                "cost_usd_billions": None,
                "source": "FAO Alert Jan 2025",
            },
            # Historical South America — successful eradication benchmark
            {
                "country": "Brazil",
                "region": "Americas",
                "year": 2006,
                "outbreak_name": "Last major SA outbreak (Mato Grosso do Sul)",
                "R0_estimate": 4.0,
                "R0_range_low": 2.5,
                "R0_range_high": 5.5,
                "total_cases_farms": None,
                "animals_culled": 30_000,
                "duration_days": 90,
                "cost_usd_billions": 1.5,
                "source": "PMC3720049",
            },
        ]

        df = pd.DataFrame(reference_data)
        df["data_type"] = "literature_reference"
        self.logger.info(f"Generated {len(df)} literature reference entries")
        return df

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and normalize FMD data."""
        if df.empty:
            return df

        clean = df.copy()

        clean.columns = (
            clean.columns.str.strip()
            .str.lower()
            .str.replace(r"\s+", "_", regex=True)
        )

        alias_map = {
            "country_name": "country",
            "country/territory": "country",
            "country_or_territory": "country",
            "event_date": "date",
            "outbreak_date": "date",
            "date_of_outbreak": "date",
            "serotype/strain": "serotype",
            "number_of_cases": "cases",
            "cases_count": "cases",
            "animals_destroyed": "animals_culled",
            "number_destroyed": "animals_culled",
        }
        clean = clean.rename(columns={old: new for old, new in alias_map.items() if old in clean.columns})

        for col in clean.columns:
            if any(token in col for token in ["r0", "cases", "culled", "year", "duration", "cost"]):
                clean[col] = pd.to_numeric(clean[col], errors="coerce")

        if "data_type" not in clean.columns:
            clean["data_type"] = "browser_export"

        self.logger.info(f"Transformed: {len(clean)} rows, {len(clean.columns)} columns")
        return clean


# ═══════════════════════════════════════════════════
# CLI entry point
# ═══════════════════════════════════════════════════

if __name__ == "__main__":
    extractor = OpenFMDExtractor()
    result = extractor.run()

    if not result.empty:
        print(f"\n{'='*60}")
        print(f"openFMD — Extraction Complete")
        print(f"{'='*60}")
        print(f"Rows: {len(result)}")
        print(f"Columns: {list(result.columns)}")
        print(f"\nData preview:")
        print(result.to_string(index=False))
        print(f"\nData saved to: data/raw/ and data/processed/")
    else:
        print("\n⚠ No FMD data obtained.")
