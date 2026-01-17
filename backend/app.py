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

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = FastAPI()

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://email-ai-js-py.vercel.app",   # domínio fixo de produção
        "https://*.vercel.app"                 # qualquer preview do Vercel
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pasta de logs
os.makedirs("backend/logs", exist_ok=True)

logging.basicConfig(
    filename="backend/logs/classify.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

class TextIn(BaseModel):
    text: str

def preprocess_text(text: str) -> str:
    """
    Pré-processa o texto: minúsculas e remove caracteres especiais.
    """
    text = text.lower()
    text = re.sub(r"[^a-zA-ZÀ-ÿ\s]", "", text)
    return text.strip()

def extract_output_text(resp_json: dict) -> str:
    """
    Extrai texto da resposta da Responses API.
    """
    try:
        return resp_json["output"][0]["content"][0]["text"].strip()
    except Exception:
        return ""

def classify_text_with_openai(processed_text: str) -> dict:
    """
    Consulta a OpenAI Responses API e retorna dict com category e reply.
    """
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

def extract_text_from_pdf(file: UploadFile) -> str:
    """
    Extrai texto de um arquivo PDF usando PyPDF2.
    """
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

@app.get("/health")
def healthcheck():
    return {"status": "ok"}

@app.post("/classify")
def classify(payload: TextIn):
    """
    Endpoint existente — mantém integração atual com o frontend.
    """
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
    """
    Novo endpoint para PDF — NÃO altera o contrato atual do frontend.
    """
    pdf_text = extract_text_from_pdf(file)
    processed_text = preprocess_text(pdf_text)
    logging.info("INPUT_PDF: %s chars | PREPROCESSED: %s", len(pdf_text), processed_text[:120])

    output = classify_text_with_openai(processed_text)
    logging.info("OUTPUT_PDF: %s", output)
    return JSONResponse(content=output, media_type="application/json; charset=utf-8")
