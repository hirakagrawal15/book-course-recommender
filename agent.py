import os
import json
from tavily import TavilyClient
from google import genai
from google.genai import types

class RecommendationAgent:
    def __init__(self, gemini_api_key: str, tavily_api_key: str):
        self.gemini_client = genai.Client(api_key=gemini_api_key)
        self.tavily_client = TavilyClient(api_key=tavily_api_key)
        
    def generate_search_queries(self, user_inputs: dict) -> list[str]:
        """Use Gemini to generate targeted search queries based on user inputs."""
        prompt = f"""
        You are an expert learning consultant. The user wants to learn a new skill.
        User Profile:
        - Topic: {user_inputs.get('skill')}
        - Current Level: {user_inputs.get('level')}
        - Preferred Format: {user_inputs.get('format')}
        - Time Commitment: {user_inputs.get('duration')}
        
        Generate exactly 2 optimized search queries to find the most relevant, up-to-date {user_inputs.get('format')}s for this user.
        Return the queries as a JSON list of strings. Do not include markdown formatting.
        Example: ["Best advanced python books 2024", "Top asynchronous python programming books"]
        """
        
        response = self.gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        try:
            # Clean up the response if it contains markdown formatting
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            queries = json.loads(text.strip())
            return queries if isinstance(queries, list) else [str(queries)]
        except Exception as e:
            # Fallback query
            return [f"Best {user_inputs.get('level')} {user_inputs.get('skill')} {user_inputs.get('format')}"]

    def perform_search(self, queries: list[str]) -> str:
        """Use Tavily to search the internet based on the generated queries."""
        search_results = []
        for query in queries:
            try:
                response = self.tavily_client.search(
                    query=query,
                    search_depth="advanced",
                    max_results=3
                )
                search_results.append(f"Results for query '{query}':\n{json.dumps(response.get('results', []), indent=2)}")
            except Exception as e:
                search_results.append(f"Error searching for '{query}': {str(e)}")
                
        return "\n\n".join(search_results)

    def synthesize_recommendations(self, user_inputs: dict, search_context: str) -> str:
        """Use Gemini to synthesize the final recommendations."""
        prompt = f"""
        You are an AI learning consultant.
        
        User Profile:
        - Topic: {user_inputs.get('skill')}
        - Current Level: {user_inputs.get('level')}
        - Preferred Format: {user_inputs.get('format')}
        - Time Commitment: {user_inputs.get('duration')}
        
        Here is the latest data gathered from the web:
        {search_context}
        
        Task:
        Based on the User Profile and the web search data, provide the top 3 recommendations. 
        Format your response beautifully in Markdown.
        For each recommendation, include:
        1. Title
        2. Format (Book/Course)
        3. Why it fits the user
        4. A link (URL) from the search context
        
        Be highly encouraging, structured, and clear.
        """
        
        response = self.gemini_client.models.generate_content(
            model='gemini-2.5-flash', # Changed to flash to avoid rate limits
            contents=prompt,
        )
        return response.text

    def run(self, user_inputs: dict) -> dict:
        """Orchestrate the entire flow."""
        # 1. Generate Queries
        queries = self.generate_search_queries(user_inputs)
        
        # 2. Search
        search_context = self.perform_search(queries)
        
        # 3. Synthesize
        final_recommendation = self.synthesize_recommendations(user_inputs, search_context)
        
        return {
            "queries": queries,
            "search_context": search_context,
            "recommendation": final_recommendation
        }
