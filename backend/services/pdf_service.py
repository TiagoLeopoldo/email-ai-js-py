from fastapi import UploadFile, HTTPException
from PyPDF2 import PdfReader
import io

def extract_text_from_pdf(file: UploadFile) -> str:
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Arquivo inválido: é esperado um PDF.")

    content = file.file.read()
    if not content:
        raise HTTPException(status_code=400, detail="PDF vazio ou não lido corretamente.")

    pdf_stream = io.BytesIO(content)
    reader = PdfReader(pdf_stream)

    pages_text = []
    for page in reader.pages:
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        pages_text.append(text)

    full_text = "\n".join(pages_text).strip()
    if len(full_text) < 3:
        raise HTTPException(status_code=400, detail="Não foi possível extrair texto útil do PDF.")

    return full_text
