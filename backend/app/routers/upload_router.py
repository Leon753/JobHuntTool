# upload_router.py
import base64
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.interview.insert_resume import insert_resume
from services.interview.resume_parser import extract_resume_text
from services.interview.summarize import summarize_resume, summarize_job_details  # Your summarization service
from services.interview.extract_job import extract_job_description_trafilatura
from services.interview.generate_question import generate_interview_question
from services.interview.text_to_speech import text_to_speech

router = APIRouter()

@router.post("/upload-resume")
async def upload_resume(
    resume: UploadFile = File(...),
):

    allowed_extensions = {"pdf", "doc", "docx"}
    filename = resume.filename
    extension = filename.split('.')[-1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload a PDF, DOC, or DOCX file."
        )

    content = await resume.read()
    resume_text = extract_resume_text(content, extension)
    insert_resume(filename, resume_text)