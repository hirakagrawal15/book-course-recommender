import json
from tavily import TavilyClient
import google.generativeai as genai


class RecommendationAgent:
    def __init__(self, gemini_api_key: str, tavily_api_key: str):
        genai.configure(api_key=gemini_api_key)

        # FINAL FIX (important)
        self.model = genai.GenerativeModel("models/gemini-pro")

        self.tavily_client = TavilyClient(api_key=tavily_api_key)

    def generate_search_queries(self, user_inputs: dict) -> list[str]:
        prompt = f"""
        User wants to learn:
        Topic: {user_inputs.get('skill')}
        Level: {user_inputs.get('level')}
        Format: {user_inputs.get('format')}
        Duration: {user_inputs.get('duration')}

        Generate 2 search queries in JSON list.
        """

        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()

            if text.startswith("```"):
                text = text.replace("```json", "").replace("```", "").strip()

            queries = json.loads(text)
            return queries if isinstance(queries, list) else [str(queries)]

        except:
            return [f"{user_inputs.get('skill')} {user_inputs.get('level')} {user_inputs.get('format')}"]

    def perform_search(self, queries: list[str]) -> str:
        results = []

        for q in queries:
            try:
                res = self.tavily_client.search(query=q, max_results=3)
                results.append(f"{q}:\n{json.dumps(res.get('results', []), indent=2)}")
            except Exception as e:
                results.append(f"Error: {str(e)}")

        return "\n\n".join(results)

    def synthesize_recommendations(self, user_inputs: dict, search_context: str) -> str:
        prompt = f"""
        User Profile:
        {user_inputs}

        Search Data:
        {search_context}

        Recommend top 3 books/courses with:
        - Title
        - Platform
        - Reason
        - Link

        Format nicely.
        """

        response = self.model.generate_content(prompt)
        return response.text

    def run(self, user_inputs: dict) -> dict:
        queries = self.generate_search_queries(user_inputs)
        search_data = self.perform_search(queries)
        final_output = self.synthesize_recommendations(user_inputs, search_data)

        return {
            "queries": queries,
            "recommendation": final_output
        }
