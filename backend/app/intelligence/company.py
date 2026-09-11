from sqlalchemy.orm import Session
import asyncio
from ..models import Company
from ..llm import LLMInterface
from ..research.fetcher import WebFetcher
from ..research.extractor import HTMLExtractor

class CompanyIntelligenceService:
    def __init__(self, db: Session, llm: LLMInterface = None, fetcher: WebFetcher = None, extractor: HTMLExtractor = None):
        self.db = db
        self.llm = llm or LLMInterface()
        self.fetcher = fetcher or WebFetcher()
        self.extractor = extractor or HTMLExtractor()

    async def extract_company_profile(self, company: Company) -> dict:
        """
        Extracts deep profile information using the research engine and LLM (Phase 10).
        """
        if not company.website:
            return {}

        html = await self.fetcher.fetch_html(company.website, render_js=True)
        text = self.extractor.extract_text(html)
        meta = self.extractor.extract_metadata(html)

        prompt = f"""
        Extract a structured company profile based on this website text and metadata.
        Company Name: {company.name}
        Metadata: {meta}
        Website Text: {text[:4000]}

        Return a JSON with:
        - industry: string
        - product: string (What do they make/do?)
        - business_model: string (e.g. B2B SaaS, B2C Marketplace)
        - founders: list of strings
        - employees_estimate: string (e.g. 10-50)
        - technology: list of strings (e.g. Python, React)
        """

        try:
            profile = self.llm.generate_json(prompt)
            # Update database record if new info is found
            if profile.get('industry') and not company.industry:
                company.industry = profile['industry']
            if profile.get('product'):
                company.description = profile['product']

            self.db.commit()
            return profile
        except Exception as e:
            print(f"Failed to extract profile for {company.name}: {e}")
            return {}
