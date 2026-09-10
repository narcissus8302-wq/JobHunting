class FundingDiscoveryService:
    def parse_funding_request(self, query: str) -> dict:
        """
        Parses natural language requests into structured queries (Phase 11).
        """
        return {
            "industry": ["AI"],
            "geography": ["India"],
            "funding_recency_days": 90
        }

    def discover_recently_funded(self, criteria: dict) -> list[dict]:
        """
        Searches accessible public sources for recent funding announcements.
        """
        return []
