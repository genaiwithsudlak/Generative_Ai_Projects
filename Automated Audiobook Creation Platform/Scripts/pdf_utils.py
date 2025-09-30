import fitz  # PyMuPDF

def extract_text_from_pdf_bytes(pdf_bytes):
    """Extract plain text from PDF bytes using PyMuPDF."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages_text = []
    for page in doc:
        pages_text.append(page.get_text("text"))
    full_text = "\n\n".join(pages_text)
    return full_text, len(pages_text)
