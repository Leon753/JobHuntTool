from crewai.tools.base_tool import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun
search = DuckDuckGoSearchRun()


class DuckDuckGoSearchTool(BaseTool):
    name: str = "DuckDuckGo Search Tool"
    description: str = "A tool to perform conversational search queries using DuckDuckGo Search Tool. The goal of this tool is to search the web. Ensure to store the URLS from the search results for further processing."

    def _run(self, query: str) -> dict:
        return search.invoke(query)