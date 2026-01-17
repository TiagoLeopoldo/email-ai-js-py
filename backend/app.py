from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import requests
import re
from dotenv import load_dotenv

# PDF parsing
from PyPDF2 import PdfReader
import io

# NLP (NLTK)
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# -----------------------------------------------------------------------------
# Boot de ambiente
# -----------------------------------------------------------------------------
load_dotenv()

app = FastAPI()

# CORS (mantém produção e previews do Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://email-ai-js-py.vercel.app",
        "https://*.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logs
os.makedirs("backend/logs", exist_ok=True)
logging.basicConfig(
    filename="backend/logs/classify.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# -----------------------------------------------------------------------------
# NLTK bootstrap (seguro para produção: tenta baixar se não existir)
# -----------------------------------------------------------------------------
def _ensure_nltk_resources():
    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords")
    try:
        nltk.data.find("corpora/wordnet")
    except LookupError:
        nltk.download("wordnet")
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")

_ensure_nltk_resources()

# Instâncias NLP
lemmatizer = WordNetLemmatizer()
# Stopwords em português; se não houver, usa um fallback mínimo
try:
    STOP_PT = set(stopwords.words("portuguese"))
except Exception:
    STOP_PT = {
        "a","o","os","as","de","da","do","das","dos","e","é","em","um","uma",
        "para","por","com","sem","no","na","nos","nas","que","se","sua","seu"
    }

# -----------------------------------------------------------------------------
# Modelos
# -----------------------------------------------------------------------------
class TextIn(BaseModel):
    text: str

# -----------------------------------------------------------------------------
# NLP helpers
# -----------------------------------------------------------------------------
def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-ZÀ-ÿ\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize(text: str) -> list:
    return text.split()

def remove_stopwords(tokens: list) -> list:
    return [t for t in tokens if t not in STOP_PT and len(t) > 1]

def lemmatize_tokens(tokens: list) -> list:
    return [lemmatizer.lemmatize(t) for t in tokens]

def preprocess_text(text: str) -> str:
    norm = normalize_text(text)
    toks = tokenize(norm)
    toks = remove_stopwords(toks)
    toks = lemmatize_tokens(toks)
    processed = " ".join(toks).strip()
    return processed if processed else norm

# -----------------------------------------------------------------------------
# OpenAI Responses API
# -----------------------------------------------------------------------------
def extract_output_text(resp_json: dict) -> str:
    try:
        return resp_json["output"][0]["content"][0]["text"].strip()
    except Exception:
        return ""

def classify_text_with_openai(processed_text: str) -> dict:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY não configurada no processo.")

    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    url = "https://api.openai.com/v1/responses"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    allowed = ["Produtivo", "Improdutivo"]

    body = {
        "model": model,
        "input": [
            {
                "role": "system",
                "content": (
                    "Classifique o texto do usuário em exatamente UMA das categorias: "
                    "Produtivo ou Improdutivo. "
                    "Responda apenas com a palavra da categoria."
                )
            },
            {"role": "user", "content": processed_text}
        ],
        "temperature": 0,
        "max_output_tokens": 32
    }

    try:
        resp = requests.post(url, headers=headers, json=body, timeout=30)
    except requests.RequestException as e:
        logging.exception("Erro de rede ao consultar OpenAI: %s", str(e))
        raise HTTPException(status_code=502, detail="Erro de rede ao consultar API externa de IA.")

    if resp.status_code < 200 or resp.status_code >= 300:
        logging.error("OpenAI error %s: %s", resp.status_code, resp.text)
        raise HTTPException(
            status_code=502,
            detail=f"Erro ao consultar API externa de IA. Status={resp.status_code}"
        )

    result = resp.json()
    category = extract_output_text(result)

    if category not in allowed:
        logging.warning("Categoria inesperada: '%s' | full=%s", category, result)
        raise HTTPException(status_code=500, detail=f"Categoria inesperada retornada pela IA: {category!r}")

    respostas = {
        "Produtivo": "Recebemos sua mensagem e já estamos cuidando dela para garantir uma solução rápida.",
        "Improdutivo": "Agradecemos sua mensagem! Não é necessário nenhuma ação neste momento."
    }

    output = {
        "category": category,
        "reply": respostas.get(category, f"Sugestão de resposta para categoria {category}")
    }
    return output

# -----------------------------------------------------------------------------
# PDF
# -----------------------------------------------------------------------------
def extract_text_from_pdf(file: UploadFile) -> str:
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Arquivo inválido: é esperado um PDF.")

    try:
        content = file.file.read()
        if not content or len(content) == 0:
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
    except HTTPException:
        raise
    except Exception as e:
        logging.exception("Falha ao extrair texto do PDF: %s", str(e))
        raise HTTPException(status_code=500, detail="Falha ao processar o PDF.")

# -----------------------------------------------------------------------------
# Endpoints
# -----------------------------------------------------------------------------
@app.get("/health")
def healthcheck():
    return {"status": "ok"}

@app.post("/classify")
def classify(payload: TextIn):
    text = payload.text.strip()
    if len(text) < 3:
        raise HTTPException(status_code=400, detail="Texto muito curto para classificação.")

    processed_text = preprocess_text(text)
    logging.info("INPUT: %s | PREPROCESSED: %s", text, processed_text)

    output = classify_text_with_openai(processed_text)
    logging.info("OUTPUT: %s", output)
    return JSONResponse(content=output, media_type="application/json; charset=utf-8")

@app.post("/classify-pdf")
async def classify_pdf(file: UploadFile = File(...)):
    pdf_text = extract_text_from_pdf(file)
    processed_text = preprocess_text(pdf_text)
    logging.info("INPUT_PDF: %s chars | PREPROCESSED: %s", len(pdf_text), processed_text[:120])

    output = classify_text_with_openai(processed_text)
    logging.info("OUTPUT_PDF: %s", output)
    return JSONResponse(content=output, media_type="application/json; charset=utf-8")
