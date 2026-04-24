import json
from tavily import TavilyClient
from google import genai


class RecommendationAgent:
    def __init__(self, gemini_api_key: str, tavily_api_key: str):
        self.client = genai.Client(api_key=gemini_api_key)
        self.tavily_client = TavilyClient(api_key=tavily_api_key)

    def generate_search_queries(self, user_inputs: dict):
        prompt = f"""
        User wants to learn:
        Topic: {user_inputs.get('skill')}
        Level: {user_inputs.get('level')}
        Format: {user_inputs.get('format')}
        Duration: {user_inputs.get('duration')}

        Generate 2 short search queries in JSON list format.
        Example: ["best python books beginner", "top python courses online"]
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )

            text = response.text.strip()

            # Clean markdown
            if text.startswith("```"):
                text = text.replace("```json", "").replace("```", "").strip()

            queries = json.loads(text)
            return queries if isinstance(queries, list) else [str(queries)]

        except:
            return [f"{user_inputs.get('skill')} {user_inputs.get('level')} {user_inputs.get('format')}"]

    def perform_search(self, queries):
        results = []

        for q in queries:
            try:
                res = self.tavily_client.search(query=q, max_results=3)
                results.append(f"{q}:\n{json.dumps(res.get('results', []), indent=2)}")
            except Exception as e:
                results.append(f"Error: {str(e)}")

        return "\n\n".join(results)

    def synthesize_recommendations(self, user_inputs, search_context):
        prompt = f"""
        User Profile:
        {user_inputs}

        Search Data:
        {search_context}

        Recommend top 3 books or courses.
        Include:
        - Title
        - Platform
        - Reason
        - Link

        Format nicely in markdown.
        """

        response = self.client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        return response.text

    def run(self, user_inputs):
        queries = self.generate_search_queries(user_inputs)
        search_data = self.perform_search(queries)
        final_output = self.synthesize_recommendations(user_inputs, search_data)

        return {
            "queries": queries,
            "recommendation": final_output
        }
