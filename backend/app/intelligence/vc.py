from ..research.fetcher import WebFetcher
from ..research.extractor import HTMLExtractor
from ..llm import LLMInterface

class VCDiscoveryService:
    def __init__(self, fetcher: WebFetcher = None, extractor: HTMLExtractor = None, llm: LLMInterface = None):
        self.fetcher = fetcher or WebFetcher()
        self.extractor = extractor or HTMLExtractor()
        self.llm = llm or LLMInterface()

    async def discover_portfolio(self, vc_name: str, portfolio_url: str = None) -> list[str]:
        """
        Discovers startups backed by a specific VC (Phase 12).
        If portfolio_url is provided, it scrapes the page to find companies.
        """
        if not portfolio_url:
            # Fallback mock for testing
            portfolios = {
                "Accel": ["XYZ AI", "Acme Corp"],
                "YC": ["Stripe", "Airbnb"]
            }
            return portfolios.get(vc_name, [])

        html = await self.fetcher.fetch_html(portfolio_url, render_js=True)
        text = self.extractor.extract_text(html)

        prompt = f"""
        Extract the names of all portfolio companies listed in this text for the VC '{vc_name}'.
        Text: {text[:8000]}

        Return a JSON with:
        - companies: list of strings (e.g. ["Stripe", "Airbnb"])
        """
        try:
            result = self.llm.generate_json(prompt)
            return result.get('companies', [])
        except Exception as e:
            print(f"Failed to extract portfolio for {vc_name}: {e}")
            return []
