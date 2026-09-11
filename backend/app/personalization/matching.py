from ..llm import LLMInterface
from ..models import Opportunity, Person, Company

class CandidateMatcher:
    def __init__(self, llm: LLMInterface = None):
        self.llm = llm or LLMInterface()

    def match_opportunity(self, company: Company, role: dict, candidate_profile: dict) -> dict:
        """
        Uses LLM to determine fit and identify matching skills (Phase 16).
        """
        prompt = f"""
        Analyze the fit between this candidate and the open role at the company.

        Company: {company.name} ({company.industry or 'Unknown industry'})
        Role Details: {role}

        Candidate Profile:
        {candidate_profile}

        Return a structured JSON evaluation matching the candidate to the opportunity.
        Output JSON format:
        {{
            "fit_score": integer (0 to 100),
            "matching_skills": ["list of strings"],
            "relevant_projects": ["list of strings"],
            "gaps": ["list of strings missing from candidate profile"],
            "why_candidate_fits": "brief string explanation"
        }}
        """
        try:
            return self.llm.generate_json(prompt)
        except Exception as e:
            print(f"Candidate matching failed: {e}")
            return {
                "fit_score": 0,
                "matching_skills": [],
                "relevant_projects": [],
                "gaps": [],
                "why_candidate_fits": "Error occurred during matching."
            }
