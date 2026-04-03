import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.extractors.cofepris_clausuras import CofeprisClausurasExtractor
from src.extractors.dge_2018_2024 import (
    DGEMorbilidad20182024Extractor,
    DGENationalSeriesConsolidator,
)
from src.extractors import openfmd as openfmd_module
from src.extractors import pucra_ram as pucra_module
from src.extractors.openfmd import OpenFMDExtractor
from src.extractors.pucra_ram import PucraRAMExtractor


class DGERecoveryTests(unittest.TestCase):
    def test_parse_target_line_a05(self):
        line = "Intoxicación alimentaria bacteriana A05 25 259 5 832 4 272 2 157"
        parsed = DGEMorbilidad20182024Extractor._parse_target_line(line)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["cve_cie10"], "A05")
        self.assertEqual(parsed["des_diagno"], "Intoxicación alimentaria bacteriana")
        self.assertEqual(parsed["acumulado_nacional"], 25259)

    def test_parse_target_line_tb_group(self):
        line = "Tuberculosis respiratoria A15-A16 20 968 12 885 5 965 686 735"
        parsed = DGEMorbilidad20182024Extractor._parse_target_line(line)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["cve_cie10"], "A15-A16")
        self.assertEqual(parsed["acumulado_nacional"], 20968)

    def test_build_national_series_aggregates_pre2018(self):
        pre = pd.DataFrame(
            [
                {"year_anuario": 2015, "cve_cie10": "A05", "des_diagno": "Intoxicación", "acumulado": 10},
                {"year_anuario": 2015, "cve_cie10": "A05", "des_diagno": "Intoxicación", "acumulado": 5},
            ]
        )
        post = pd.DataFrame(
            [
                {
                    "year_anuario": 2018,
                    "report_name": "distribucion_casos_nuevos_enfermedad_fuente_notificacion",
                    "cve_cie10": "A05",
                    "des_diagno": "Intoxicación",
                    "acumulado_nacional": 20,
                    "source_pdf": "dge_2018.pdf",
                    "source_page": 2,
                    "extraction_method": "pdfplumber_text",
                }
            ]
        )

        combined = DGENationalSeriesConsolidator.build_national_from_frames(pre, post)
        pre_row = combined[combined["year_anuario"] == 2015].iloc[0]
        self.assertEqual(pre_row["acumulado_nacional"], 15)
        self.assertEqual(pre_row["report_name"], "state_aggregate_from_csv")


class OpenFMDTests(unittest.TestCase):
    def test_load_local_browser_export(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "openfmd_fmdwatch_export.csv"
            csv_path.write_text("country,year,cases\nMexico,2025,3\n", encoding="utf-8")

            original_raw_dir = openfmd_module.RAW_DIR
            try:
                openfmd_module.RAW_DIR = Path(tmpdir)
                extractor = OpenFMDExtractor()
                df = extractor._load_local_browser_export()
            finally:
                openfmd_module.RAW_DIR = original_raw_dir

        self.assertIsNotNone(df)
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["source_file"], "openfmd_fmdwatch_export.csv")

    def test_skip_html_masquerading_as_csv(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bad_path = Path(tmpdir) / "openfmd_bad_export.csv"
            bad_path.write_text("<!DOCTYPE html><html><body>not csv</body></html>", encoding="utf-8")

            original_raw_dir = openfmd_module.RAW_DIR
            try:
                openfmd_module.RAW_DIR = Path(tmpdir)
                extractor = OpenFMDExtractor()
                df = extractor._load_local_browser_export()
            finally:
                openfmd_module.RAW_DIR = original_raw_dir

        self.assertIsNone(df)


class CofeprisTests(unittest.TestCase):
    def test_extract_table_rows_keeps_tidy_schema(self):
        extractor = CofeprisClausurasExtractor()
        table = [
            ["LICENCIA SANITARIA", None, None, None, None, None, None, None],
            ["NO.", "ESTABLECIMIENTO", "DOMICILIO", "ORDEN DE VERIFICACIÓN", "FECHA INICIO", "FECHA FIN", "GIRO", "MOTIVO"],
            ["1", "CARNES FINAS SA", "GUADALAJARA JALISCO", "24-MF-3314-01178-ML", "04/03/2024", "04/03/2024", "ALIMENTOS", "SALMONELLA"],
        ]
        rows = extractor._extract_table_rows(table, "Listado_2024.pdf", 1)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["establecimiento"], "CARNES FINAS SA")
        self.assertEqual(rows[0]["motivo_visita"], "SALMONELLA")


class PucraTests(unittest.TestCase):
    def test_find_local_pdf_candidates_prefers_exact_filename(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            exact = Path(tmpdir) / "pucra2024.pdf"
            backup = Path(tmpdir) / "PUCRA_reporte_resistencia.pdf"
            exact.write_bytes(b"%PDF exact")
            backup.write_bytes(b"%PDF backup")

            original_raw_dir = pucra_module.RAW_DIR
            try:
                pucra_module.RAW_DIR = Path(tmpdir)
                extractor = PucraRAMExtractor()
                candidates = extractor._find_local_pdf_candidates("pucra2024.pdf")
            finally:
                pucra_module.RAW_DIR = original_raw_dir

        self.assertEqual([path.name for path in candidates], ["pucra2024.pdf", "PUCRA_reporte_resistencia.pdf"])

    def test_parse_antibiotic_row_uses_real_pucra_periods(self):
        periods = ["2017", "2018", "2019", "2020", "2021", "2022", "2023", "Promedio"]
        parsed = PucraRAMExtractor()._parse_antibiotic_row("Ampicilina 88 86 84 88 83 88 90 87", periods)

        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["antibiotico"], "Ampicilina")
        self.assertEqual(parsed["periodos"], periods)
        self.assertEqual(parsed["values"], ["88", "86", "84", "88", "83", "88", "90", "87"])


if __name__ == "__main__":
    unittest.main()
