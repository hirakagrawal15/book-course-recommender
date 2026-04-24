import os
from tavily import TavilyClient
import google.generativeai as genai


class RecommendationAgent:
    def __init__(self):
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.tavily_key = os.getenv("TAVILY_API_KEY")

        if not self.gemini_key or not self.tavily_key:
            raise ValueError("API keys missing. Check Streamlit Secrets.")

        genai.configure(api_key=self.gemini_key)
        self.model = genai.GenerativeModel("gemini-pro")

        self.client = TavilyClient(api_key=self.tavily_key)

    def get_recommendations(self, topic, level, format_type, time_commitment):
        try:
            query = f"{topic} {level} best {format_type} {time_commitment}"

            # 🔍 Tavily Search
            response = self.client.search(query=query)

            results = response.get("results", [])
            search_context = " ".join([r.get("content", "") for r in results])

            if not search_context:
                search_context = "No useful search data found."

            # 🤖 Gemini Prompt
            prompt = f"""
            Based on the following search data, recommend the best {format_type} for learning {topic}.

            User Level: {level}
            Time Commitment: {time_commitment}

            Search Data:
            {search_context}

            Give clear, structured recommendations with names and short descriptions.
            """

            gemini_response = self.model.generate_content(prompt)

            return {
                "recommendations": gemini_response.text,
                "search_context": search_context
            }

        except Exception as e:
            return {
                "recommendations": f"Error: {str(e)}",
                "search_context": ""
            }
