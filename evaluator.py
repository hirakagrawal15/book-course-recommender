import json
from google import genai


class LLMJudge:
    def __init__(self, gemini_api_key: str):
        self.client = genai.Client(api_key=gemini_api_key)

    def evaluate(self, recommendation_text: str, user_inputs: dict):
        prompt = f"""
        Evaluate this recommendation:

        {recommendation_text}

        Based on:
        - Relevance (0-4)
        - Actionability (0-3)
        - Formatting (0-3)

        Return JSON:
        {{
            "score": number,
            "feedback": "short explanation",
            "improvement": "one suggestion"
        }}
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )

            text = response.text.strip()

            if text.startswith("```"):
                text = text.replace("```json", "").replace("```", "").strip()

            return json.loads(text)

        except:
            return {
                "score": "N/A",
                "feedback": "Evaluation failed",
                "improvement": "Try again"
            }
