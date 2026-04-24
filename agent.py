import os
from tavily import TavilyClient
from google import genai

class RecommendationAgent:
    def __init__(self):
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.tavily_key = os.getenv("TAVILY_API_KEY")

        if not self.gemini_key or not self.tavily_key:
            raise ValueError("API keys missing")

        self.gemini = genai.Client(api_key=self.gemini_key)
        self.tavily = TavilyClient(api_key=self.tavily_key)

    def get_recommendations(self, topic, level, format_type, time_commitment):
        try:
            query = f"{topic} {level} best {format_type}"

            search = self.tavily.search(query=query)
            results = search.get("results", [])

            search_context = " ".join(
                [r.get("content", "") for r in results]
            )

            if not search_context:
                search_context = "Basic knowledge resources for learning."

            prompt = f"""
            Recommend best {format_type} for {topic}

            Level: {level}
            Time: {time_commitment}

            Data:
            {search_context}

            Give 5 structured recommendations.
            """

            response = self.gemini.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )

            return {
                "recommendations": response.text,
                "search_context": search_context
            }

        except Exception as e:
            return {
                "recommendations": f"Error: {e}",
                "search_context": ""
            }
