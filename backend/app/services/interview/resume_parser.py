import io
from PyPDF2 import PdfReader

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract text from a PDF file.
    """
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text


def extract_resume_text(file_bytes: bytes, extension: str) -> str:
    """
    Extract resume text based on the file extension.
    """
    extension = extension.lower()
    if extension == "pdf":
        return extract_text_from_pdf(file_bytes)
    else:
        # For other file types, attempt to decode as plain text.
        return file_bytes.decode("utf-8", errors="ignore")