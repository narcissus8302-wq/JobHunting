from ..llm import LLMInterface
from ..models import Opportunity, Company, Person

class CommunicationGenerator:
    def __init__(self, llm: LLMInterface = None):
        self.llm = llm or LLMInterface()

    def generate_short_description(self, company: Company, person: Person, role: dict, match_data: dict) -> str:
        """Brief summary of fit (Phase 20)."""
        prompt = f"""
        Generate a concise, 4-sentence summary of this opportunity.
        Company: {company.name} (What they do: {company.description})
        Contact: {person.name}, {person.title}
        Role: {role}
        Why relevant: {match_data.get('why_candidate_fits')}

        Rules:
        - Sentence 1: Company, what they do, why interesting.
        - Sentence 2: Current hiring signal.
        - Sentence 3: Who you're contacting and why that person.
        - Sentence 4: Why the candidate is relevant.

        Return ONLY the summary paragraph.
        """
        try:
            return self.llm.generate_text(prompt)
        except Exception:
            return f"Opportunity at {company.name} contacting {person.name}."

    def generate_cold_email(self, template: str, context: dict) -> str:
        """
        Fills template with personalized context (Phase 21).
        Uses LLM to dynamically generate the email based on the YAML template structure.
        """
        prompt = f"""
        Draft a cold email based on this YAML template structure:
        {template}

        Inject this context naturally into the email:
        {context}

        Return ONLY the final email text (Subject and Body).
        """
        try:
            return self.llm.generate_text(prompt)
        except Exception:
            return "Error generating email."

    def generate_cover_letter(self, template: str, context: dict, requires_cover_letter: bool = False) -> str:
        """
        Conditionally generates a cover letter (Phase 22).
        Returns None if a cover letter is not required based on the application rules.
        """
        if not requires_cover_letter:
            return None

        prompt = f"""
        Draft a cover letter based on this YAML template structure:
        {template}

        Inject this context naturally into the letter:
        {context}

        Return ONLY the final cover letter text.
        """
        try:
            return self.llm.generate_text(prompt)
        except Exception:
            return "Error generating cover letter."
