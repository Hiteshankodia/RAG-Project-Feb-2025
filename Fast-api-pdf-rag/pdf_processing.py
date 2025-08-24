import fitz  # PyMuPDF

# Extract text from a PDF file
def extract_text_from_pdf(pdf_path: str):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text
