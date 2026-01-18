from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from core.nlp import preprocess_text
from core.logging import logger
from models.schemas import TextIn, CategoryResponse
from services.rules import apply_rules
from services.openai_service import classify_text_with_openai, generate_reply_with_openai
from services.pdf_service import extract_text_from_pdf

router = APIRouter()

@router.post("/classify", response_model=CategoryResponse)
def classify(payload: TextIn):
    text = payload.text.strip()
    if len(text) < 3:
        raise HTTPException(status_code=400, detail="Texto muito curto para classificação.")

    processed_text = preprocess_text(text)
    logger.info("INPUT: %s | PREPROCESSED: %s", text, processed_text)

    # Primeiro tenta aplicar regras fixas
    category = apply_rules(processed_text)
    if not category:
        category = classify_text_with_openai(processed_text)["category"]

    reply = generate_reply_with_openai(category, text)
    output = {"category": category, "reply": reply}

    logger.info("OUTPUT: %s", output)
    return JSONResponse(content=output, media_type="application/json; charset=utf-8")


@router.post("/classify-pdf", response_model=CategoryResponse)
async def classify_pdf(file: UploadFile = File(...)):
    pdf_text = extract_text_from_pdf(file)
    processed_text = preprocess_text(pdf_text)
    logger.info("INPUT_PDF: %s chars | PREPROCESSED: %s", len(pdf_text), processed_text[:120])

    category = apply_rules(processed_text)
    if not category:
        category = classify_text_with_openai(processed_text)["category"]

    reply = generate_reply_with_openai(category, pdf_text)
    output = {"category": category, "reply": reply}

    logger.info("OUTPUT_PDF: %s", output)
    return JSONResponse(content=output, media_type="application/json; charset=utf-8")
