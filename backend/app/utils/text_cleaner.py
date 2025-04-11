import re
from config.logger import logger

def clean_resume_text(text: str) -> str:
    """
    Clean resume text by removing problematic characters and normalizing whitespace.
    """
    if not text:
        return ""
    
    # First, replace any problematic characters with a safe placeholder
    text = re.sub(r'[^\x20-\x7E]', ' ', text)
    
    # Then, replace any curly braces with their escaped versions
    text = text.replace('{', '{{').replace('}', '}}')
    
    # Replace any format string special characters with their escaped versions
    text = text.replace('%', '%%')
    
    # Normalize whitespace but preserve paragraph breaks
    text = re.sub(r'[ \t]+', ' ', text)  # Replace multiple spaces/tabs with single space
    text = re.sub(r'\n\s*\n', '\n\n', text)  # Preserve paragraph breaks
    
    # Log the cleaned text for debugging
    logger.info(f"Cleaned resume text length: {len(text)}")
    if len(text) > 1000:
        logger.info(f"First 1000 chars of cleaned resume: {text[:1000]}")
    else:
        logger.info(f"Cleaned resume text: {text}")
    
    return text.strip() 