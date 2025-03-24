from PyPDF2 import PdfReader

from .gen import DocumentProcessor


def is_valid_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            return len(reader.pages) > 0
    except Exception as e:
        return False


def extract_text_from_pdf(file_path):
    doc = DocumentProcessor('gemini-2.0-flash', file_path)
    return doc.process_pdf()