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

# CORS
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
# NLTK bootstrap
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

lemmatizer = WordNetLemmatizer()
try:
    STOP_PT = set(stopwords.words("portuguese"))
except Exception:
    STOP_PT = {"a","o","os","as","de","da","do","das","dos","e","é","em","um","uma","para","por","com","sem","no","na","nos","nas","que","se","sua","seu"}

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
# Regras fixas de categoria
# -----------------------------------------------------------------------------
def apply_rules(processed_text: str) -> str | None:
    impro_keywords = ["feliz natal", "parabéns", "obrigado", "agradecimento", "felicitações", "bom dia", "boa tarde"]
    prod_keywords = ["status", "prazo", "cancelar", "erro", "contrato", "pedido", "assinatura", "entrega", "suporte"]
    irrelevant_keywords = ["azul", "cor", "piada", "brincadeira", "besteira", "nada haver"]

    for kw in impro_keywords:
        if kw in processed_text:
            return "Improdutivo"
    for kw in prod_keywords:
        if kw in processed_text:
            return "Produtivo"
    for kw in irrelevant_keywords:
        if kw in processed_text:
            return "Irrelevante"
    return None

# -----------------------------------------------------------------------------
# OpenAI helpers
# -----------------------------------------------------------------------------
def extract_output_text(resp_json: dict) -> str:
    try:
        return resp_json["output"][0]["content"][0]["text"].strip()
    except Exception:
        return ""

def classify_text_with_openai(processed_text: str) -> dict:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY não configurada.")

    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    url = "https://api.openai.com/v1/responses"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    allowed = ["Produtivo", "Improdutivo", "Irrelevante"]

    body = {
        "model": model,
        "input": [
            {
                "role": "system",
                "content": (
                    "Classifique o texto do usuário em exatamente UMA das categorias: "
                    "Produtivo, Improdutivo ou Irrelevante. "
                    "Responda apenas com a palavra da categoria."
                )
            },
            {"role": "user", "content": processed_text}
        ],
        "temperature": 0,
        "max_output_tokens": 32
    }

    resp = requests.post(url, headers=headers, json=body, timeout=30)
    if resp.status_code < 200 or resp.status_code >= 300:
        logging.error("OpenAI error %s: %s", resp.status_code, resp.text)
        raise HTTPException(status_code=502, detail=f"Erro ao consultar API externa de IA. Status={resp.status_code}")

    result = resp.json()
    category = extract_output_text(result)

    if category not in allowed:
        logging.warning("Categoria inesperada: '%s' | full=%s", category, result)
        raise HTTPException(status_code=500, detail=f"Categoria inesperada retornada pela IA: {category!r}")

    return {"category": category}

def generate_reply_with_openai(category: str, user_text: str) -> str:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY não configurada.")

    model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    url = "https://api.openai.com/v1/responses"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    prompt = (
        "Você é um assistente que responde emails de forma educada e natural.\n"
        f"O texto do usuário foi classificado como {category}.\n"
        "Gere uma resposta curta e humana, sem soar robótica.\n"
        "Se for Produtivo, mostre que estamos cuidando da solicitação.\n"
        "Se for Improdutivo, agradeça de forma simpática e cordial.\n"
        "Se for Irrelevante, refute com educação e explique que não está relacionado aos serviços financeiros.\n"
        "Se a mensagem for uma pergunta sobre o ramo da empresa, responda de forma profissional e institucional, "
        "explicando que atuamos no setor financeiro e estamos à disposição para apoiar o cliente.\n"
        "IMPORTANTE: Não mencione nomes de bancos, fintechs ou empresas específicas. Responda sempre em nome da nossa empresa apenas.\n"
        f"Texto original: {user_text}"
    )


    body = {
        "model": model,
        "input": [
            {"role": "system", "content": "Você é um assistente de emails de uma empresa de finanças."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_output_tokens": 128
    }

    resp = requests.post(url, headers=headers, json=body, timeout=30)
    if resp.status_code < 200 or resp.status_code >= 300:
        raise HTTPException(status_code=502, detail="Erro ao gerar resposta personalizada.")

    result = resp.json()
    return extract_output_text(result)

# -----------------------------------------------------------------------------
# PDF
# -----------------------------------------------------------------------------
def extract_text_from_pdf(file: UploadFile) -> str:
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Arquivo inválido: é esperado um PDF.")

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

    category = apply_rules(processed_text)
    if not category:
        category = classify_text_with_openai(processed_text)["category"]

    reply = generate_reply_with_openai(category, text)
    output = {"category": category, "reply": reply}

    logging.info("OUTPUT: %s", output)
    return JSONResponse(content=output, media_type="application/json; charset=utf-8")

@app.post("/classify-pdf")
async def classify_pdf(file: UploadFile = File(...)):
    pdf_text = extract_text_from_pdf(file)
    processed_text = preprocess_text(pdf_text)
    logging.info("INPUT_PDF: %s chars | PREPROCESSED: %s", len(pdf_text), processed_text[:120])

    category = apply_rules(processed_text)
    if not category:
        category = classify_text_with_openai(processed_text)["category"]

    reply = generate_reply_with_openai(category, pdf_text)
    output = {"category": category, "reply": reply}

    logging.info("OUTPUT_PDF: %s", output)
    return JSONResponse(content=output, media_type="application/json; charset=utf-8")
