import fitz  # PyMuPDF

def extract_text_from_pdf(file_path: str) -> str:
    """
    Opens a PDF file and extracts all text content.
    Args:
        file_path (str): The absolute path to the PDF file.
    Returns:
        str: The extracted text content.
    """
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""