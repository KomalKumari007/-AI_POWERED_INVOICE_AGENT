import os
from pypdf import PdfReader

def extract_text_from_pdf(file_path: str) -> str:
    """
    Reads an uploaded PDF invoice file path and extracts its raw text contents.
    """
    # Defensive check: ensure file path exists on disk before reading
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Invoice file not found at local path: {file_path}")
    
    raw_text = ""
    
    # Initialize the PyPDF Reader object
    reader = PdfReader(file_path)
    
    # Loop through each page sequence and append text characters safely
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            raw_text += page_text + "\n"
            
    # Return trimmed, clean text content string
    return raw_text.strip()