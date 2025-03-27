# services/audio_feedback_service.py
import os
import base64
import tempfile
from fastapi import HTTPException
from openai import OpenAI  # Using the new client interface
from services.text_to_speech import text_to_speech

def process_audio_feedback(audio_content: bytes, client: OpenAI) -> dict:
    """
    Processes an audio file by transcribing it and generating feedback.

    Args:
        audio_content (bytes): The audio file content.
        client (openai.OpenAI): An initialized OpenAI client instance.

    Returns:
        dict: A dictionary containing the transcription and feedback.
    """
    try:
        # Save the audio content to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
            tmp.write(audio_content)
            tmp.flush()
            tmp_path = tmp.name

        # Transcribe the audio using Whisper via the client's audio transcription interface
        with open(tmp_path, "rb") as audio_file:
            transcription_response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        # Access the transcribed text via attribute access
        transcribed_text = transcription_response.text.strip()

        # Clean up the temporary file
        os.remove(tmp_path)

        if not transcribed_text:
            raise HTTPException(status_code=400, detail="Could not transcribe audio.")

        # Build a prompt for ChatGPT to generate feedback
        prompt = (
            "Analyze the following interview response and provide constructive feedback. "
            "Comment on what was done well and suggest improvements for clarity, delivery, and content.\n\n"
            f"Interview Response:\n{transcribed_text}\n\nFeedback:"
        )

        feedback_response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are a professional HR interviewer providing constructive feedback."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200,
        )
        feedback = feedback_response.choices[0].message.content.strip()

        # Convert the feedback text to audio using your text_to_speech service
        feedback_audio = text_to_speech(feedback)
        # Base64-encode the audio content so that it can be easily transferred via JSON
        feedback_audio_base64 = base64.b64encode(feedback_audio).decode("utf-8")

        return {
            "transcription": transcribed_text,
            "feedback_text": feedback,
            "feedback_audio_base64": feedback_audio_base64,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
