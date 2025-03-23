# upload_router.py
import base64
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.interview.resume_parser import extract_resume_text
from services.interview.summarize import summarize_resume, summarize_job_details  # Your summarization service
from services.interview.extract_job import extract_job_description_trafilatura
from services.interview.generate_question import generate_interview_question
from services.interview.text_to_speech import text_to_speech

router = APIRouter()

@router.post("/upload")
async def upload_resume(
    resume: UploadFile = File(...),
    job_link: str = Form(...)
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
    resume_summary = summarize_resume(resume_text)

    job_details = extract_job_description_trafilatura(job_link)
    job_summary = summarize_job_details(job_details)

    interview_question = generate_interview_question(resume_summary, job_summary)
    print(interview_question)

    audio_content = text_to_speech(interview_question)
    audio_base64 = base64.b64encode(audio_content).decode("utf-8")

    return {
        "filename": filename,
        "file_size": len(content),
        "job_link": job_link,
        "parsed_info": {
            "resume_extracted_excerpt": resume_text[:200],
            "resume_summary": resume_summary,
            "job_description_excerpt": job_details[:200],
            "job_summary": job_summary,
            "interview_question": interview_question,
            "interview_question_audio_base64": audio_base64
        }
    }
