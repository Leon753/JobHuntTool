# services/text_to_speech.py
from dotenv import load_dotenv
import os
from google.cloud import texttospeech

# Load environment variables from .env file
load_dotenv()

def text_to_speech(text: str) -> bytes:
    """
    Converts the provided text to speech using Google Cloud Text-to-Speech API.
    
    Args:
        text (str): The text to be converted into speech.
        
    Returns:
        bytes: The audio content in MP3 format.
    """
    # Initialize the client (the client will automatically pick up the GOOGLE_APPLICATION_CREDENTIALS variable)
    client = texttospeech.TextToSpeechClient()
    
    # Set the text input to be synthesized.
    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    # Build the voice request, select the language code ("en-US") and the SSML voice gender
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-F",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    
    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    
    return response.audio_content
