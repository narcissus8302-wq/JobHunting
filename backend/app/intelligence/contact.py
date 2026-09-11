from ..models import Company, Person
from ..llm import LLMInterface
from ..research.fetcher import WebFetcher
from ..research.extractor import HTMLExtractor

class ContactDiscoveryService:
    def __init__(self, llm: LLMInterface = None, fetcher: WebFetcher = None, extractor: HTMLExtractor = None):
        self.llm = llm or LLMInterface()
        self.fetcher = fetcher or WebFetcher()
        self.extractor = extractor or HTMLExtractor()

    async def discover_contacts(self, company: Company, team_url: str = None) -> list[dict]:
        """
        Identifies appropriate contacts based on company stage/size (Phase 14).
        """
        if not team_url and company.website:
            base = company.website.rstrip('/')
            team_url = f"{base}/about"

        if not team_url:
            return []

        html = await self.fetcher.fetch_html(team_url, render_js=True)
        text = self.extractor.extract_text(html)

        hierarchy = "Small (<50): Founder/CTO. Mid (50-500): Recruiter/Hiring Manager. Large: Tech Recruiter."

        prompt = f"""
        Extract team members for {company.name} from the text below.
        Rules for outreach: {hierarchy}
        Current estimate size: {company.employee_count or 'Unknown'}

        Text: {text[:8000]}

        Return a JSON with:
        - contacts: list of objects, each containing:
            - name: string
            - title: string
            - relevance: string (HIGH, MEDIUM, LOW based on the outreach rules)
        """
        try:
            result = self.llm.generate_json(prompt)
            return result.get('contacts', [])
        except Exception as e:
            print(f"Failed to discover contacts for {company.name}: {e}")
            return []
