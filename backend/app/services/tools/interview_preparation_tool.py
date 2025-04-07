from crewai.tools.base_tool import BaseTool
from services.clients.perplexity_client import PerplexityClient
from config.keys import PERPLEXITY_API_KEY
from services.memory import vector_db


class InterviewPreparationTool(BaseTool):

    def _run(self, query: str) -> str:
        pass