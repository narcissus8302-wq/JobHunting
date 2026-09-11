from ..llm import LLMInterface

class ResumeAuditor:
    def __init__(self, llm: LLMInterface = None):
        self.llm = llm or LLMInterface()

    def audit(self, tailored_resume: str, master_profile: dict) -> bool:
        """
        Detects unsupported claims (Phase 19).
        If claims are found, the resume is rejected.
        """
        prompt = f"""
        Act as a strict Fact Checker.
        Compare the Generated Resume against the Source of Truth (Master Profile).
        Count the number of unsupported claims in the generated resume (e.g., skills, jobs, metrics, or technologies
        that do NOT exist in the Master Profile).

        Master Profile:
        {master_profile}

        Generated Resume:
        {tailored_resume}

        Return a JSON with:
        - unsupported_claims: integer (count of fabrications)
        - explanation: list of strings (detailing the fabricated claims, or empty if none)
        """

        try:
            result = self.llm.generate_json(prompt)
            unsupported_claims = int(result.get("unsupported_claims", 1)) # Default fail safe
            if unsupported_claims > 0:
                print(f"Audit failed. Fabrications found: {result.get('explanation')}")
                return False
            return True
        except Exception as e:
            print(f"Audit engine error: {e}")
            return False # Fail safe
