import os
from google import genai

class Evaluator:
    def __init__(self):
        key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=key)

    def evaluate(self, topic, recommendations):
        try:
            prompt = f"""
            Evaluate these recommendations for {topic}

            {recommendations}

            Give:
            - Feedback
            - Improvements
            """

            res = self.client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )

            return res.text

        except Exception as e:
            return f"Error: {e}"
