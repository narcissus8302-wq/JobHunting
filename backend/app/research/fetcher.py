import asyncio
import httpx
from playwright.async_api import async_playwright

class WebFetcher:
    def __init__(self):
        self.cache = {} # Basic in-memory cache for Phase 5 compliance

    async def fetch_html(self, url: str, render_js: bool = False) -> str:
        """
        Retrieves HTML from a URL.
        If render_js is True, uses a headless Playwright browser.
        Otherwise uses standard HTTP. Handles basic caching.
        """
        if url in self.cache:
            return self.cache[url]

        try:
            if render_js:
                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=True)
                    page = await browser.new_page()
                    # Stealth settings to avoid bot detection
                    await page.set_extra_http_headers({
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
                    })
                    await page.goto(url, wait_until="domcontentloaded", timeout=15000)
                    html = await page.content()
                    await browser.close()
            else:
                async with httpx.AsyncClient(timeout=15.0) as client:
                    response = await client.get(
                        url,
                        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                    )
                    response.raise_for_status()
                    html = response.text

            self.cache[url] = html
            return html
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return ""
