"""
SENASICA TB Extractor — Wave 1 (Stable endpoint)
=================================================
Descarga datos de hatos libres de tuberculosis bovina.

Primary path: CSV directo desde datos abiertos (repodatos.atdt.gob.mx)
Secondary path: API REST oculta de SENASICA (fallback)

Output: DataFrame con prevalencia TB por estado
Feeds: SIR calibración + Mapa Coroplético (slides 6, 7-8)
"""

import pandas as pd

from src.base_extractor import BaseExtractor
from src.config import (
    SENASICA_API_OCULTA,
    SENASICA_URLS,
    HTTP_TIMEOUT,
)


class SenasicaTBExtractor(BaseExtractor):
    """
    Extrae datos de hatos certificados como libres de TB bovina.

    Strategy:
    1. Try CSV directo (primary) — dos URLs conocidas
    2. If fails → try API oculta (secondary)
    3. Normalize: nombres de estados, columnas numéricas
    4. Calculate: prevalencia_aproximada = 1 - (hatos_libres / hatos_totales) [si hay dato]
    """

    def __init__(self):
        super().__init__(name="senasica_tb")

    def extract(self) -> pd.DataFrame:
        """
        Download SENASICA TB data.
        Tries multiple CSV URLs, falls back to hidden API.
        """
        # --- Primary path: CSV directo ---
        csv_urls = [
            SENASICA_URLS["hatos_libres_dic_2025"],
            SENASICA_URLS["hatos_libres_jun_2025"],
        ]

        frames = []
        for url in csv_urls:
            try:
                df = self._try_csv_download(url)
                if df is not None and not df.empty:
                    df["source_url"] = url
                    frames.append(df)
                    self.logger.info(f"  ✓ CSV exitoso: {len(df)} rows from {url.split('/')[-1]}")
            except Exception as e:
                self.logger.warning(f"  ⚠ CSV falló ({url.split('/')[-1]}): {e}")
                continue

        if frames:
            combined = pd.concat(frames, ignore_index=True)
            self.logger.info(f"Primary path OK: {len(combined)} total rows from {len(frames)} CSVs")
            return combined

        # --- Secondary path: API oculta ---
        self.logger.warning("Primary path failed. Trying hidden API...")
        try:
            return self._try_hidden_api()
        except Exception as e:
            self.logger.error(f"Secondary path also failed: {e}")
            self.logger.info("Returning empty DataFrame — Use literature constants for SIR.")
            return pd.DataFrame()

    def _try_csv_download(self, url: str) -> pd.DataFrame:
        """Attempt to download and parse a CSV with multiple encodings."""
        response = self.session.get(url, timeout=HTTP_TIMEOUT)
        response.raise_for_status()

        from io import BytesIO

        # Try multiple encodings (government CSVs are unreliable)
        for encoding in ["utf-8", "latin1", "iso-8859-1", "cp1252"]:
            try:
                df = pd.read_csv(BytesIO(response.content), encoding=encoding)
                if len(df) > 0:
                    return df
            except (UnicodeDecodeError, pd.errors.ParserError):
                continue

        return None

    def _try_hidden_api(self) -> pd.DataFrame:
        """
        Attempt to call the hidden SENASICA REST API.
        Endpoint: /api/Statistics/SaludAnimal/TuberculosisBovina/ObtenerDatos
        """
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Referer": "https://dj.senasica.gob.mx/sias/",
        }

        try:
            # Try GET first
            response = self.session.get(
                SENASICA_API_OCULTA,
                headers=headers,
                timeout=HTTP_TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()

            if isinstance(data, list):
                return pd.DataFrame(data)
            elif isinstance(data, dict) and "data" in data:
                return pd.DataFrame(data["data"])
            else:
                self.logger.warning(f"Unexpected API response structure: {type(data)}")
                return pd.DataFrame()

        except Exception as e:
            self.logger.warning(f"GET failed, trying POST: {e}")

            # Try POST with empty body
            try:
                response = self.session.post(
                    SENASICA_API_OCULTA,
                    json={},
                    headers=headers,
                    timeout=HTTP_TIMEOUT,
                )
                response.raise_for_status()
                data = response.json()
                return pd.DataFrame(data if isinstance(data, list) else data.get("data", []))
            except Exception as e2:
                self.logger.error(f"POST also failed: {e2}")
                raise

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and normalize SENASICA data.

        Steps:
        1. Normalize column names (lowercase, underscores)
        2. Normalize state names
        3. Convert numeric columns
        4. Remove duplicates
        """
        if df.empty:
            return df

        clean = df.copy()

        # Normalize column names
        clean.columns = (
            clean.columns.str.strip()
            .str.lower()
            .str.replace(r"\s+", "_", regex=True)
            .str.replace(r"[áàä]", "a", regex=True)
            .str.replace(r"[éèë]", "e", regex=True)
            .str.replace(r"[íìï]", "i", regex=True)
            .str.replace(r"[óòö]", "o", regex=True)
            .str.replace(r"[úùü]", "u", regex=True)
        )

        # Log what we got
        self.logger.info(f"Columns found: {list(clean.columns)}")
        self.logger.info(f"Shape: {clean.shape}")

        # Try to identify state column
        state_col = None
        for candidate in ["estado", "entidad", "entidad_federativa", "state", "nom_ent"]:
            if candidate in clean.columns:
                state_col = candidate
                break

        if state_col:
            clean[state_col] = clean[state_col].str.strip().str.title()
            self.logger.info(f"States found: {clean[state_col].nunique()} unique")

        # Convert potential numeric columns
        for col in clean.columns:
            if "num" in col or "hato" in col or "libres" in col or "total" in col:
                clean[col] = pd.to_numeric(clean[col], errors="coerce")

        # Drop full duplicates
        before = len(clean)
        clean = clean.drop_duplicates()
        if len(clean) < before:
            self.logger.info(f"  Removed {before - len(clean)} duplicates")

        return clean


# ═══════════════════════════════════════════════════
# CLI entry point
# ═══════════════════════════════════════════════════

if __name__ == "__main__":
    extractor = SenasicaTBExtractor()
    result = extractor.run()

    if not result.empty:
        print(f"\n{'='*60}")
        print(f"SENASICA TB — Extraction Complete")
        print(f"{'='*60}")
        print(f"Rows: {len(result)}")
        print(f"Columns: {list(result.columns)}")
        print(f"\nFirst 5 rows:")
        print(result.head())
        print(f"\nData saved to: data/raw/ and data/processed/")
    else:
        print("\n⚠ No data extracted. SIR model will use literature constants (R0=1.8).")
        print("This is fine for MVP — the SIR doesn't depend on raw SENASICA data.")
