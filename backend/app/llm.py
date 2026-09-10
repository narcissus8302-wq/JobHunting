import json
import os
import httpx
from typing import Dict, Any

class LLMInterface:
    def __init__(self, api_key: str = None, provider: str = "gemini"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.provider = provider
        self.client = httpx.Client(timeout=30.0)

    def generate_json(self, prompt: str) -> dict:
        """
        Calls a free-tier API (Gemini) and returns structured JSON.
        If the API key is missing, falls back to a mock for local zero-cost testing.
        """
        if not self.api_key:
            return {
                "fit_score": 91,
                "matching_skills": ["Python", "FastAPI"],
                "gaps": ["Kubernetes"],
                "mocked": True
            }

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt + "\n\nReturn strictly valid JSON without Markdown blocks or other formatting."}]}],
            "generationConfig": {
                "responseMimeType": "application/json"
            }
        }

        try:
            response = self.client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            text_response = data['candidates'][0]['content']['parts'][0]['text']
            return json.loads(text_response)
        except Exception as e:
            # Fallback on failure
            return {"error": str(e), "failed": True}

    def generate_text(self, prompt: str) -> str:
        """Generates unstructured text."""
        if not self.api_key:
            return "Mock generated text from LLM (No API Key found)."

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        try:
            response = self.client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            return f"Error communicating with LLM: {str(e)}"
