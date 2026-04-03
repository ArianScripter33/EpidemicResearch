"""
Kaggle FMD Dataset Extractor — Wave 2
====================================
Downloads cattle disease datasets from Kaggle.
Primary target: wasimfaraz/fmd-cattle-dataset

Setup:
1. Create a Kaggle account
2. Go to 'My Account' -> 'Create New API Token'
3. Save 'kaggle.json' to ~/.kaggle/kaggle.json
4. chmod 600 ~/.kaggle/kaggle.json
"""

import os
import pandas as pd
from pathlib import Path

from src.base_extractor import BaseExtractor
from src.config import (
    RAW_DIR,
    KAGGLE_FMD_DATASET,
)


class KaggleFMDExtractor(BaseExtractor):
    """
    Extrae datos de Fiebre Aftosa desde Kaggle.
    """

    DATASET_PATH = KAGGLE_FMD_DATASET

    def __init__(self):
        super().__init__(name="kaggle_fmd")

    def extract(self) -> pd.DataFrame:
        """
        Download dataset from Kaggle using the kaggle-api.
        """
        try:
            import kaggle
        except ImportError:
            self.logger.error("kaggle library not installed. Run: pip install kaggle")
            return pd.DataFrame()

        # Ensure .kaggle/kaggle.json exists
        kaggle_config = Path.home() / ".kaggle" / "kaggle.json"
        if not kaggle_config.exists() and "KAGGLE_USERNAME" not in os.environ:
            self.logger.warning("Kaggle API credentials not found. Set KAGGLE_USERNAME/KAGGLE_KEY or ~/.kaggle/kaggle.json")
            return pd.DataFrame()

        try:
            self.logger.info(f"Downloading Kaggle dataset: {self.DATASET_PATH}")
            # This downloads and unzips to data/raw/kaggle_fmd
            target_dir = RAW_DIR / "kaggle_fmd"
            target_dir.mkdir(parents=True, exist_ok=True)

            kaggle.api.dataset_download_files(
                self.DATASET_PATH,
                path=str(target_dir),
                unzip=True
            )

            # Find the largest CSV in the downloaded files
            csv_files = list(target_dir.glob("*.csv"))
            if not csv_files:
                self.logger.warning(f"No CSV files found in Kaggle dataset {self.DATASET_PATH}")
                return pd.DataFrame()

            # Use the largest CSV (often the main data file)
            main_csv = max(csv_files, key=lambda f: f.stat().st_size)
            self.logger.info(f"Loading CSV: {main_csv.name}")
            return pd.read_csv(main_csv)

        except Exception as e:
            self.logger.error(f"Kaggle download failed: {e}")
            return pd.DataFrame()

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standard transformation for FMD data."""
        if df.empty:
            return df

        clean = df.copy()
        clean.columns = [c.lower().replace(" ", "_") for c in clean.columns]
        return clean


if __name__ == "__main__":
    extractor = KaggleFMDExtractor()
    result = extractor.run()
    if not result.empty:
        print(f"Kaggle extraction successful: {len(result)} rows")
    else:
        print("Kaggle extraction failed or credentials missing.")
