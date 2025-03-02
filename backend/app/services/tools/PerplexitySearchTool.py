from crewai.tools.base_tool import BaseTool
from services.perplexity_client import PerplexityClient
from dotenv import load_dotenv
import os
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_API_URL = os.getenv("PERPLEXITY_API_URL")
class PerplexitySearchTool(BaseTool):
    name: str = "Perplexity Search Tool"
    description: str = "A tool to perform conversational search queries using Perplexity-like behavior."

    async def _run(self, query: str) -> str:
        # Example endpoint; replace with the actual Perplexity API endpoint if available.
        endpoint = "https://api.perplexity.ai/search"
        headers = {
            "Authorization": "Bearer YOUR_PERPLEXITY_API_KEY",
            "Content-Type": "application/json"
        }
        payload = {"query": query}
        messages = [
            {
                "role": "system",
                "content": (
                    "Give a consice but informative answer"
                ),
            },
            {   
                "role": "user",
                "content": (
                    query
                ),
            },
        ] 
        client  = PerplexityClient(api_key=PERPLEXITY_API_KEY, api_url=PERPLEXITY_API_URL, model="sonar")
        response = await client.get_response(messages=messages)
        return response