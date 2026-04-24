import json
class LLMJudge:
    def __init__(self, gemini_api_key: str):
        # Gemini not used in this safe version
        pass

    def evaluate(self, recommendation_text: str, user_inputs: dict):
        """
        Simple evaluation logic (no API dependency)
        """

        score = 0
        feedback = []
        
        # Basic checks
        if user_inputs.get("skill") and user_inputs["skill"].lower() in recommendation_text.lower():
            score += 3
            feedback.append("Relevant to the user's topic.")
        
        if "http" in recommendation_text:
            score += 3
            feedback.append("Contains useful links/resources.")
        
        if len(recommendation_text) > 100:
            score += 2
            feedback.append("Detailed explanation provided.")
        
        # Formatting check
        if "\n" in recommendation_text:
            score += 2
            feedback.append("Well formatted output.")

        return {
            "score": score,
            "feedback": " ".join(feedback) if feedback else "Basic recommendations provided.",
            "improvement": "Add more personalization and structured formatting."
        }
