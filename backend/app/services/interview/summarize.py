from openai import OpenAI
import os
from dotenv import load_dotenv
from config.logger import logger

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# Ensure your OpenAI API key is set (or set it directly here)

def summarize_resume(resume_text: str) -> str:
    """
    Uses ChatGPT to summarize a resume.
    """
    prompt = (
        "Summarize the following resume. Extract and list the candidate's name, "
        "professional summary, key work experiences (job title, company, and duration), "
        "education, projects, awards/certificates, and skills. Keep the summary concise and well-structured.\n\n"
        f"Resume:\n{resume_text}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or use "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are an expert resume analyzer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Lower temperature for more focused output
            max_tokens=250
        )
        # Use attribute access instead of dict-style indexing
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        print("Error summarizing resume:", e)
        return "Error generating summary."

def summarize_job_details(job_details: str) -> str:
    """
    Uses ChatGPT to summarize a job description, focusing on key details relevant for generating behavioral interview questions.
    """
    prompt = (
        "Summarize the following job description by extracting the key details relevant for "
        "generating behavioral interview questions. Focus on the core responsibilities, company culture, "
        "required skills, and aspects related to teamwork or leadership. Keep the summary concise and informative.\n\n"
        f"Job Description:\n{job_details}"
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are an HR expert specialized in behavioral interviewing."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,  # moderate creativity for a focused summary
            max_tokens=300,   # adjust as needed based on job description length
        )
        # Use attribute access instead of dictionary indexing
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        logger.error("Error summarizing job details:", e)
        return "Error generating job description summary."
