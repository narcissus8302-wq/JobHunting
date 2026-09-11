from ..llm import LLMInterface

class ResumeCurator:
    def __init__(self, llm: LLMInterface = None):
        self.llm = llm or LLMInterface()

    def generate_resume(self, master_latex: str, match_data: dict) -> str:
        """
        Adjusts emphasis and selects relevant projects without inventing data (Phase 18).
        Outputs tailored LaTeX.
        """
        prompt = f"""
        You are an expert resume curator.
        You have been provided with a Master LaTeX resume and a match profile for a specific opportunity.

        HARD RULES:
        1. Never invent skills.
        2. Never invent employment.
        3. Never invent achievements or metrics.
        4. Do not fabricate experience.

        Your task is to reorder skills, select relevant projects, and adjust wording emphasis in the LaTeX source
        to perfectly align with this opportunity while strictly adhering to the Master LaTeX facts.

        Match Data: {match_data}

        Master LaTeX:
        ```latex
        {master_latex}
        ```

        Return ONLY the raw modified LaTeX text, without markdown wrappers or explanation.
        """

        try:
            curated_latex = self.llm.generate_text(prompt)
            # Basic cleanup if the LLM wrapped it in markdown code blocks
            curated_latex = curated_latex.replace('```latex', '').replace('```', '').strip()
            return curated_latex
        except Exception as e:
            print(f"Resume generation failed: {e}")
            return master_latex
