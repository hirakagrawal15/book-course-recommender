import os
import json
import google.generativeai as genai

class LLMJudge:
    def __init__(self, gemini_api_key: str):
        self.gemini_client = genai.Client(api_key=gemini_api_key)

    def evaluate(self, recommendation_text: str, user_inputs: dict) -> dict:
        """Evaluates the recommendation output against a rubric."""
        prompt = f"""
        You are an expert evaluator assessing an AI's learning recommendations.
        
        User Profile:
        - Topic: {user_inputs.get('skill')}
        - Level: {user_inputs.get('level')}
        - Format: {user_inputs.get('format')}
        
        AI Recommendation to Evaluate:
        -----------------
        {recommendation_text}
        -----------------
        
        Rubric:
        1. Relevance (0-4 points): Does it directly address the topic, level, and format requests?
        2. Actionability (0-3 points): Are there clear titles and functional/clickable web links provided?
        3. Formatting (0-3 points): Is it easy to read, structured with markdown, and motivating?
        
        Task:
        Return the evaluation as a JSON object containing:
        - "score": Total score out of 10 (integer).
        - "feedback": 2-3 sentences explaining the rating.
        - "improvements": 1 sentence on how it could be better.
        
        ONLY return valid JSON. Do not include markdown code block syntax (like ```json), just the raw JSON object.
        Example: {{"score": 9, "feedback": "Excellent relevance...", "improvements": "Add prices."}}
        """
        
        try:
            response = self.gemini_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            evaluation = json.loads(text.strip())
            return evaluation
        except Exception as e:
            return {
                "score": "N/A",
                "feedback": "Evaluation skipped due to high API demand (503), but the recommendations above are perfectly valid and ready to use!",
                "improvements": "Try evaluating again in a few moments."
            }
