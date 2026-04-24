import json
import google.generativeai as genai


class LLMJudge:
    def __init__(self, gemini_api_key: str):
        # Correct setup
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel("gemini-pro")

    def evaluate(self, recommendation_text: str, user_inputs: dict) -> dict:
        prompt = f"""
        You are an expert evaluator assessing AI recommendations.

        User Profile:
        - Topic: {user_inputs.get('skill')}
        - Level: {user_inputs.get('level')}
        - Format: {user_inputs.get('format')}

        Recommendation:
        {recommendation_text}

        Evaluate on:
        - Relevance (0-4)
        - Actionability (0-3)
        - Formatting (0-3)

        Return JSON:
        {{
            "score": number,
            "feedback": "short explanation",
            "improvements": "suggestion"
        }}
        """

        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()

            # Clean markdown if exists
            if text.startswith("```"):
                text = text.replace("```json", "").replace("```", "").strip()

            return json.loads(text)

        except Exception as e:
            return {
                "score": "N/A",
                "feedback": "Evaluation skipped due to API issue",
                "improvements": "Try again later"
            }
