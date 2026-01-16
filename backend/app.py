# backend/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from nlp.classifier import classify_text
import logging
import os

app = FastAPI()

# Habilita CORS para permitir chamadas do front-end
# Em produção, ajuste o domínio do frontend hospedado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://email-ai-js-mtdyncoqd-tiagos-projects-6ffe6e70.vercel.app"],     # domínio do frontend em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Garante a pasta de logs
os.makedirs("backend/logs", exist_ok=True)

# Configuração básica de logging
logging.basicConfig(
    filename="backend/logs/classify.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

class TextIn(BaseModel):
    text: str

@app.get("/health")
def healthcheck():
    return {"status": "ok"}

@app.post("/classify")
def classify(payload: TextIn):
    text = payload.text.strip()
    if len(text) < 3:
        raise HTTPException(status_code=400, detail="Texto muito curto para classificação.")
    result = classify_text(text)
    logging.info(
        f"input={text} | intent={result['intent']} | confidence={result['confidence']:.4f} | entities={result['entities']}"
    )
    return JSONResponse(content=result, media_type="application/json; charset=utf-8")
