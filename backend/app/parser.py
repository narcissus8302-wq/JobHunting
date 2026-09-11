from .llm import LLMInterface

class RequestParser:
    def __init__(self, llm: LLMInterface = None):
        self.llm = llm or LLMInterface()

    def parse_natural_language(self, query: str) -> dict:
        """
        Converts natural language commands into structured parameters (Phase 28).
        """
        prompt = f"""
        Convert this user request into a structured JSON research query object.
        Request: "{query}"

        Output JSON format:
        {{
            "intent": string (e.g. "DISCOVER_FUNDING", "DISCOVER_VC", "PROCESS_LIST"),
            "target_url": string or null (if they provided a sheet or list url),
            "industries": [list of strings],
            "locations": [list of strings],
            "vc_names": [list of strings]
        }}
        """
        try:
            return self.llm.generate_json(prompt)
        except Exception as e:
            print(f"Failed to parse request: {e}")
            return {"intent": "UNKNOWN"}
