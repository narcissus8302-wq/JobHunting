from ..llm import LLMInterface
from ..models import Opportunity, Person, Company

class CandidateMatcher:
    def __init__(self, llm: LLMInterface):
        self.llm = llm

    def match_opportunity(self, company: Company, role: dict, candidate_profile: dict) -> dict:
        """
        Uses LLM to determine fit and identify matching skills (Phase 16).
        """
        prompt = f"Match candidate {candidate_profile} to role {role} at {company.name}"
        return self.llm.generate_json(prompt)
