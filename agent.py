import json
from tavily import TavilyClient


class RecommendationAgent:
    def __init__(self, gemini_api_key: str, tavily_api_key: str):
        self.tavily_client = TavilyClient(api_key=tavily_api_key)

    def generate_search_queries(self, user_inputs):
        return [
            f"{user_inputs.get('skill')} beginner course",
            f"best books for {user_inputs.get('skill')}"
        ]

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
        return f"""
        📚 Recommended Resources for {user_inputs.get('skill')}:

        Based on latest search:

        {search_context}

        ✔ These are relevant books and courses.
        ✔ You can explore links above.
        """

    def run(self, user_inputs):
        queries = self.generate_search_queries(user_inputs)
        search_data = self.perform_search(queries)
        final_output = self.synthesize_recommendations(user_inputs, search_data)

        return {
            "queries": queries,
            "recommendation": final_output
        }
