"""
Base Extractor — ABC for all data extraction modules
=====================================================
Provides: retry logic, lineage metadata injection, logging, and file persistence.
"""

import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.config import (
    HTTP_BACKOFF_FACTOR,
    HTTP_RETRIES,
    HTTP_TIMEOUT,
    RAW_DIR,
    USER_AGENT,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class BaseExtractor(ABC):
    """
    Abstract base class for all data extractors.

    Every extractor must implement:
    - extract() → raw DataFrame
    - transform(df) → cleaned DataFrame

    Provides for free:
    - Resilient HTTP session with retries + exponential backoff
    - Lineage metadata injection (fecha_extraccion_etl, fuente_origen, version_etl)
    - Persistence to data/raw/
    - Structured logging
    """

    VERSION = "1.0.0"

    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"extractor.{name}")
        self.session = self._build_session()

    def _build_session(self) -> requests.Session:
        """Build a resilient HTTP session with retries and backoff."""
        session = requests.Session()
        session.headers.update({"User-Agent": USER_AGENT})

        retry_strategy = Retry(
            total=HTTP_RETRIES,
            backoff_factor=HTTP_BACKOFF_FACTOR,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def download_file(self, url: str, filename: Optional[str] = None) -> Path:
        """Download a file from URL and save to data/raw/."""
        RAW_DIR.mkdir(parents=True, exist_ok=True)

        if filename is None:
            filename = url.split("/")[-1].split("?")[0]

        filepath = RAW_DIR / filename
        self.logger.info(f"Downloading: {url}")
        self.logger.info(f"  → Target: {filepath}")

        start = time.time()
        response = self.session.get(url, timeout=HTTP_TIMEOUT, stream=True)
        response.raise_for_status()

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        elapsed = time.time() - start
        size_mb = filepath.stat().st_size / (1024 * 1024)
        self.logger.info(f"  ✓ Downloaded {size_mb:.2f} MB in {elapsed:.1f}s")

        return filepath

    def download_csv(self, url: str, encoding: str = "utf-8", **kwargs) -> pd.DataFrame:
        """Download and parse a CSV directly into a DataFrame."""
        self.logger.info(f"Fetching CSV: {url}")
        start = time.time()

        response = self.session.get(url, timeout=HTTP_TIMEOUT)
        response.raise_for_status()

        from io import BytesIO
        df = pd.read_csv(BytesIO(response.content), encoding=encoding, **kwargs)

        elapsed = time.time() - start
        self.logger.info(f"  ✓ Parsed {len(df)} rows × {len(df.columns)} cols in {elapsed:.1f}s")

        return df

    def inject_lineage(self, df: pd.DataFrame, fuente: str) -> pd.DataFrame:
        """Add ETL lineage metadata to every DataFrame."""
        df = df.copy()
        df["fecha_extraccion_etl"] = datetime.now(timezone.utc).isoformat()
        df["fuente_origen"] = fuente
        df["version_etl"] = self.VERSION
        return df

    def save_raw(self, df: pd.DataFrame, filename: str) -> Path:
        """Persist DataFrame to data/raw/ as CSV."""
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        filepath = RAW_DIR / filename
        df.to_csv(filepath, index=False, encoding="utf-8")
        self.logger.info(f"  💾 Saved {len(df)} rows → {filepath}")
        return filepath

    def save_processed(self, df: pd.DataFrame, filename: str) -> Path:
        """Persist DataFrame to data/processed/ as CSV."""
        from src.config import PROCESSED_DIR
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        filepath = PROCESSED_DIR / filename
        df.to_csv(filepath, index=False, encoding="utf-8")
        self.logger.info(f"  💾 Saved {len(df)} rows → {filepath}")
        return filepath

    @abstractmethod
    def extract(self) -> pd.DataFrame:
        """Extract raw data from source. Must be implemented by subclass."""
        ...

    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and transform extracted data. Must be implemented by subclass."""
        ...

    def run(self) -> pd.DataFrame:
        """Full ETL pipeline: extract → lineage → transform → save."""
        self.logger.info(f"{'='*60}")
        self.logger.info(f"Starting extraction: {self.name}")
        self.logger.info(f"{'='*60}")

        try:
            # Extract
            raw_df = self.extract()
            if raw_df.empty:
                self.logger.warning("⚠ Extraction returned empty DataFrame")
                return raw_df

            # Save raw
            self.save_raw(raw_df, f"{self.name}_raw.csv")

            # Transform
            clean_df = self.transform(raw_df)

            # Inject lineage
            clean_df = self.inject_lineage(clean_df, self.name)

            # Save processed
            self.save_processed(clean_df, f"{self.name}_clean.csv")

            self.logger.info(f"✅ {self.name} complete: {len(clean_df)} clean rows")
            return clean_df

        except requests.exceptions.RequestException as e:
            self.logger.error(f"❌ Network error in {self.name}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"❌ Error in {self.name}: {e}")
            raise
