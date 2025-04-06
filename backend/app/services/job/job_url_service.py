from services.tools.web_scraper_tool import WebScrapperTool

def get_job_link_info(
    url: str,
) -> str:
    scraper = WebScrapperTool()
    
    # Get job posting content
    scraped_response = scraper._run([url])

    return scraped_response