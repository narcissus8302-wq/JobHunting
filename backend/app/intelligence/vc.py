class VCDiscoveryService:
    def discover_portfolio(self, vc_name: str) -> list[str]:
        """
        Discovers startups backed by a specific VC (Phase 12).
        """
        # Mock portfolio
        portfolios = {
            "Accel": ["XYZ AI", "Acme Corp"],
            "YC": ["Stripe", "Airbnb"]
        }
        return portfolios.get(vc_name, [])
