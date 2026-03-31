"""
DGE Morbilidad 2018-2024 Extractor Placeholder
==============================================
This script documents the attempt to find CSV data for 2018-2024.
Full investigation details are in docs/DGE_DATA_SEARCH.md.
"""

import logging
import pandas as pd
from src.base_extractor import BaseExtractor

class DGEMorbilidad20182024Extractor(BaseExtractor):
    def __init__(self):
        super().__init__(name="dge_morbilidad_2018_2024")
        self.logger = logging.getLogger(__name__)

    def extract(self) -> pd.DataFrame:
        self.logger.error("Could not find CSV data URLs for 2018-2024.")
        self.logger.info("PDFs are available at: https://epidemiologia.salud.gob.mx/anuario/{year}/morbilidad/nacional/distribucion_casos_nuevos_enfermedad_fuente_notificacion.pdf")
        return pd.DataFrame()

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return df

if __name__ == "__main__":
    print("DGE Morbilidad 2018-2024: Data Not Found in CSV format.")
    print("Refer to docs/DGE_DATA_SEARCH.md for details on attempted URLs.")
