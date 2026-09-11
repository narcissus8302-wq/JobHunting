from ..models import Company
from ..llm import LLMInterface
from ..research.fetcher import WebFetcher
from ..research.extractor import HTMLExtractor

class HiringResearchService:
    def __init__(self, llm: LLMInterface = None, fetcher: WebFetcher = None, extractor: HTMLExtractor = None):
        self.llm = llm or LLMInterface()
        self.fetcher = fetcher or WebFetcher()
        self.extractor = extractor or HTMLExtractor()

    async def discover_opportunities(self, company: Company, careers_url: str = None) -> list[dict]:
        """
        Searches for current opportunities on a company's career page (Phase 13).
        """
        if not careers_url and company.website:
            # Guess standard career page paths
            base = company.website.rstrip('/')
            careers_url = f"{base}/careers"

        if not careers_url:
            return []

        html = await self.fetcher.fetch_html(careers_url, render_js=True)
        text = self.extractor.extract_text(html)

        prompt = f"""
        Extract a list of current job opportunities for {company.name} from this careers page text.
        Text: {text[:8000]}

        Return a JSON with:
        - roles: list of objects, each containing:
            - title: string
            - location: string
            - employment_type: string (e.g. Full-time, Internship)
            - category: string (AI, Backend, ML, Data, etc)
        """
        try:
            result = self.llm.generate_json(prompt)
            return result.get('roles', [])
        except Exception as e:
            print(f"Failed to discover opportunities for {company.name}: {e}")
            return []
