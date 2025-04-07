# services/generate_question.py
from openai import OpenAI
import os
from dotenv import load_dotenv

# Set your OpenAI API key (make sure the environment variable is set)
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_interview_question(resume_summary: str, job_description: str) -> str:
    """
    Uses ChatGPT to generate a behavioral interview question based on the resume summary
    and job description.
    """
    prompt = (
        "Given the following candidate resume summary and job description, "
        "generate 5 technical interview question that evaluates the candidate's fit for the job.\n\n"
        "Candidate Resume Summary:\n"
        f"{resume_summary}\n\n"
        "Job Description:\n"
        f"{job_description}\n\n"
        "Behavioral Interview Question:"
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or gpt-4 if available
            messages=[
                {"role": "system", "content": "You are an expert HR interviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150,
        )
        question = response.choices[0].message.content.strip() 
        return question
    except Exception as e:
        print("Error generating interview question:", e)
        return "Error generating interview question."
