"""
Browser-assisted openFMD export helper.

This helper is intentionally separate from openFMD.py so the extractor can stay
focused on normalization while Playwright handles the browser-only download
workflow exposed by the FMDwatch dashboard.
"""

from contextlib import suppress
from pathlib import Path

from src.config import OPENFMD_DASHBOARD, RAW_DIR


def export_openfmd_csv(output_path: Path | None = None, timeout_ms: int = 45_000) -> Path:
    try:
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Playwright is not installed. Run `pip install playwright`.") from exc

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    output_path = output_path or (RAW_DIR / "openfmd_fmdwatch_export.csv")
    debug_dir = RAW_DIR / "debug"
    debug_dir.mkdir(parents=True, exist_ok=True)
    debug_html_path = debug_dir / "openfmd_export_debug.html"
    debug_screenshot_path = debug_dir / "openfmd_export_debug.png"

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(
            accept_downloads=True,
            viewport={"width": 1600, "height": 1200},
        )
        page = context.new_page()

        try:
            page.goto(OPENFMD_DASHBOARD, wait_until="commit", timeout=timeout_ms)
            with suppress(PlaywrightTimeoutError):
                page.wait_for_load_state("domcontentloaded", timeout=10_000)
            with suppress(PlaywrightTimeoutError):
                # Shiny apps often keep websocket traffic open forever.
                page.wait_for_load_state("networkidle", timeout=10_000)
            page.wait_for_timeout(8_000)

            # The download control is attached to the Data table tab.
            data_table_locators = [
                page.locator("[data-value='Data table']"),
                page.get_by_role("tab", name="Data table"),
                page.get_by_text("Data table", exact=False),
                page.locator("button:has-text('Data table')"),
                page.locator("a:has-text('Data table')"),
            ]
            for locator in data_table_locators:
                try:
                    locator.first.click(timeout=5_000)
                    page.wait_for_timeout(2_000)
                    break
                except Exception:
                    continue

            csv_anchor = page.locator("#loc_data_table-download_csv").first
            with suppress(Exception):
                csv_anchor.wait_for(state="visible", timeout=10_000)
                page.wait_for_function(
                    """
                    () => {
                        const el = document.querySelector('#loc_data_table-download_csv');
                        return Boolean(el && el.getAttribute('href') && el.getAttribute('href').trim());
                    }
                    """,
                    timeout=15_000,
                )

            visible_control_labels: list[str] = []
            with suppress(Exception):
                visible_control_labels = page.locator("a, button").all_inner_texts()

            href = csv_anchor.get_attribute("href")
            if not href:
                with suppress(Exception):
                    debug_html_path.write_text(page.content(), encoding="utf-8")
                with suppress(Exception):
                    page.screenshot(path=str(debug_screenshot_path), full_page=True)
                raise RuntimeError(
                    "openFMD CSV anchor never received an href. "
                    f"Saved diagnostics to {debug_html_path} and {debug_screenshot_path}. "
                    f"Visible controls snapshot: {visible_control_labels[:20]}"
                )

            full_url = page.evaluate("href => new URL(href, window.location.href).toString()", href)
            response_payload = page.evaluate(
                """
                async (fullUrl) => {
                    const response = await fetch(fullUrl, { credentials: 'include' });
                    const text = await response.text();
                    return {
                        status: response.status,
                        content_type: response.headers.get('content-type') || '',
                        text,
                    };
                }
                """,
                full_url,
            )

            if response_payload["status"] != 200:
                raise RuntimeError(
                    f"openFMD fetch returned HTTP {response_payload['status']} for {full_url}"
                )

            output_path.write_text(response_payload["text"], encoding="utf-8")
            sample = response_payload["text"][:2048].lower()
            content_type = response_payload["content_type"].lower()
            if "text/csv" not in content_type and ("<!doctype html" in sample or "<html" in sample):
                bad_download_path = debug_dir / "openfmd_export_downloaded.html"
                output_path.replace(bad_download_path)
                raise RuntimeError(
                    "openFMD fetch completed but returned HTML instead of CSV. "
                    f"Saved the artifact to {bad_download_path}."
                )
            return output_path
        finally:
            browser.close()


if __name__ == "__main__":
    path = export_openfmd_csv()
    print(f"Saved openFMD export to: {path}")
