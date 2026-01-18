import requests
from fastapi import HTTPException
from core import config
from core.logging import logger

def extract_output_text(resp_json: dict) -> str:
    try:
        return resp_json["output"][0]["content"][0]["text"].strip()
    except Exception:
        return ""

def classify_text_with_openai(processed_text: str) -> dict:
    if not config.OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY não configurada.")

    url = "https://api.openai.com/v1/responses"
    headers = {
        "Authorization": f"Bearer {config.OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    allowed = ["Produtivo", "Improdutivo", "Irrelevante"]

    body = {
        "model": config.OPENAI_MODEL,
        "input": [
            {"role": "system", "content": "Classifique o texto em Produtivo, Improdutivo ou Irrelevante."},
            {"role": "user", "content": processed_text}
        ],
        "temperature": 0,
        "max_output_tokens": 32
    }

    resp = requests.post(url, headers=headers, json=body, timeout=30)
    if not resp.ok:
        logger.error("OpenAI error %s: %s", resp.status_code, resp.text)
        raise HTTPException(status_code=502, detail="Erro ao consultar API externa de IA.")

    result = resp.json()
    category = extract_output_text(result)

    if category not in allowed:
        logger.warning("Categoria inesperada: '%s'", category)
        raise HTTPException(status_code=500, detail=f"Categoria inesperada retornada: {category!r}")

    return {"category": category}

def generate_reply_with_openai(category: str, user_text: str) -> str:
    if not config.OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY não configurada.")

    url = "https://api.openai.com/v1/responses"
    headers = {
        "Authorization": f"Bearer {config.OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    prompt = (
        f"O texto foi classificado como {category}.\n"
        "Gere uma resposta curta e humana.\n"
        "Produtivo → mostrar que estamos cuidando.\n"
        "Improdutivo → agradecer cordialmente.\n"
        "Irrelevante → refutar educadamente.\n"
        f"Texto original: {user_text}"
    )

    body = {
        "model": config.OPENAI_MODEL,
        "input": [
            {"role": "system", "content": "Você é um assistente de emails de uma empresa de finanças."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_output_tokens": 128
    }

    resp = requests.post(url, headers=headers, json=body, timeout=30)
    if not resp.ok:
        raise HTTPException(status_code=502, detail="Erro ao gerar resposta personalizada.")

    result = resp.json()
    return extract_output_text(result)
