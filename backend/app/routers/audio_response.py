# audio_feedback_router.py
import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException
from dotenv import load_dotenv
from openai import OpenAI  # Using the new client interface
from services.interview.audio_feedback_service import process_audio_feedback

router = APIRouter()
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

@router.post("/audio-feedback")
async def audio_feedback(audio_response: UploadFile = File(...)):
    try:
        # Read the uploaded audio content
        content = await audio_response.read()

        # Process the audio using our dedicated service
        result = process_audio_feedback(content, client)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))