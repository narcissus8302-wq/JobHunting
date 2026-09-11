from ..llm import LLMInterface
from ..research.fetcher import WebFetcher

class FundingDiscoveryService:
    def __init__(self, llm: LLMInterface = None, fetcher: WebFetcher = None):
        self.llm = llm or LLMInterface()
        self.fetcher = fetcher or WebFetcher()

    def parse_funding_request(self, query: str) -> dict:
        """
        Parses natural language requests into structured queries via LLM (Phase 11).
        """
        prompt = f"""
        Convert this natural language query into structured criteria for finding startups.
        Query: "{query}"

        Return a JSON with:
        - industry: list of strings (e.g. ["AI", "SaaS"])
        - geography: list of strings (e.g. ["India", "SF"])
        - funding_recency_days: integer (default to 90 if not specified)
        - stage: list of strings (e.g. ["Seed", "Series A"])
        """
        try:
            return self.llm.generate_json(prompt)
        except Exception:
            # Safe defaults
            return {
                "industry": [],
                "geography": [],
                "funding_recency_days": 90,
                "stage": []
            }

    async def discover_recently_funded(self, criteria: dict) -> list[dict]:
        """
        Searches accessible public sources for recent funding announcements.
        In a complete implementation, this would iterate through a list of VC blogs,
        news aggregators, or open datasets.
        """
        # A real implementation requires specific target URLs.
        # This returns an empty list conceptually to fulfill the API structure.
        return []
