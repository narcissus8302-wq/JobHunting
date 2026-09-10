import json

class LLMInterface:
    def __init__(self, api_key: str = None, provider: str = "gemini"):
        self.api_key = api_key
        self.provider = provider

    def generate_json(self, prompt: str) -> dict:
        """
        Calls a free-tier API (Gemini or OpenRouter) and returns structured JSON.
        """
        # Mock LLM response
        return {
            "fit_score": 91,
            "matching_skills": ["Python", "FastAPI"],
            "gaps": ["Kubernetes"]
        }

    def generate_text(self, prompt: str) -> str:
        return "Mock generated text from LLM."
