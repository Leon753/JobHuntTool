import requests
import trafilatura

def extract_job_description_trafilatura(url: str) -> str:
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the URL: {url}")
    
    downloaded = trafilatura.extract(response.text)
    return downloaded or "Job description not found."