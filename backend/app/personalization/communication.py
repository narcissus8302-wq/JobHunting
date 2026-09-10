from ..llm import LLMInterface
from ..models import Opportunity

class CommunicationGenerator:
    def __init__(self, llm: LLMInterface):
        self.llm = llm

    def generate_short_description(self, opportunity: Opportunity) -> str:
        """Brief summary of fit (Phase 20)."""
        return f"Brief description of {opportunity.id}"

    def generate_cold_email(self, template: str, context: dict) -> str:
        """Fills template with personalized context (Phase 21)."""
        return template.format(**context)

    def generate_cover_letter(self, template: str, context: dict) -> str:
        """Conditionally generates a cover letter (Phase 22)."""
        return template.format(**context)
