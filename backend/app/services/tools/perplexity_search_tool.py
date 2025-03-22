from crewai.tools.base_tool import BaseTool
from services.clients.perplexity_client import PerplexityClient
from config.keys import PERPLEXITY_API_KEY
from services.memory import vector_db


class PerplexitySearchTool(BaseTool):
    name: str = "Perplexity Search Tool"
    description: str = "A tool to perform conversational search queries using Perplexity-like behavior. The goal of this tool is to search the web"

    def _run(self, query: str) -> str:
        vector_db.create_vector_db()
        result = vector_db.similarity_search(query)
        if result is None:
            # Example endpoint; replace with the actual Perplexity API endpoint if available.
            headers = {
                "Authorization": "Bearer YOUR_PERPLEXITY_API_KEY",
                "Content-Type": "application/json"
            }
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
            prelixty_client = PerplexityClient(api_key=PERPLEXITY_API_KEY, 
                                        api_url="https://api.perplexity.ai/chat/completions", 
                                        model="sonar")
            result = prelixty_client.get_response_sync(messages=messages)
            vector_db.add_message(query, result)
        return result