import os
import google.generativeai as genai


class Evaluator:
    def __init__(self):
        self.gemini_key = os.getenv("GEMINI_API_KEY")

        if not self.gemini_key:
            raise ValueError("Missing GEMINI_API_KEY")

        genai.configure(api_key=self.gemini_key)
        self.model = genai.GenerativeModel("models/gemini-1.5-flash")

    def evaluate(self, topic, recommendations):
        try:
            prompt = f"""
            Evaluate the following recommendations for the topic: {topic}

            Recommendations:
            {recommendations}

            Give:
            1. Feedback
            2. Improvement Areas
            """

            response = self.model.generate_content(prompt)

            return response.text

        except Exception as e:
            return f"Evaluation Error: {str(e)}"
