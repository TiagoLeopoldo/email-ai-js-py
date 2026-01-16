# backend/nlp/classifier.py
import spacy
import re
from utils.response_builder import build_response
from nlp.ml_classifier import predict_intent, predict_proba


nlp = spacy.load("pt_core_news_sm")

# Palavras-chave ampliadas para fallback por regras
KEYWORDS = {
    "status": ["status", "andamento", "progresso", "acompanhar", "situação", "situacao"],
    "prazo": ["prazo", "deadline", "quando", "data", "previsão", "previsao", "conclusao", "entrega"],
    "cancelamento": ["cancelar", "encerrar", "desistir", "cancelamento", "anular", "remover"],
    "erro": ["erro", "falha", "bug", "problema", "inconsistência", "inconsistencia", "travou"],
    "humano": ["atendente", "suporte humano", "telefone", "falar com atendente", "pessoa", "humano"]
}

CATEGORY_MAP = {
    "status": ("Produtivo", "status"),
    "prazo": ("Produtivo", "prazo"),
    "cancelamento": ("Operacional", "cancelamento"),
    "erro": ("Suporte", "erro"),
    "humano": ("Atendimento", "humano"),
    "default": ("Geral", "outros")
}

# Termos de domínio adicionais
DOMAIN_TERMS = {
    "pedido": "ORDER",
    "contrato": "CONTRACT",
    "assinatura": "SUBSCRIPTION",
    "projeto": "PROJECT",
    "requisição": "REQUEST",
    "solicitação": "REQUEST"
}

def match_intent_rules(text: str) -> str:
    """Fallback por regras simples"""
    t = text.lower()
    for intent, words in KEYWORDS.items():
        if any(w in t for w in words):
            return intent
    return "default"

def extract_entities(doc, text: str):
    """Extrai entidades via spaCy + regex + termos de domínio"""
    entities = []
    for ent in doc.ents:
        entities.append({"text": ent.text, "label": ent.label_})

    # Captura números isolados que não fazem parte de datas
    for match in re.findall(r"\b\d+\b", text):
        if not re.search(rf"{match}\s+de\s+\w+", text.lower()):
            entities.append({"text": match, "label": "NUMBER"})

    # Captura datas no formato "15 de fevereiro"
    for match in re.findall(r"\d{1,2}\s+de\s+\w+", text.lower()):
        entities.append({"text": match, "label": "DATE"})

    # Captura termos de domínio
    t_lower = text.lower()
    for term, label in DOMAIN_TERMS.items():
        if term in t_lower:
            entities.append({"text": term, "label": label})

    return entities

def classify_text(text: str) -> dict:
    """Classifica usando ML + fallback por regras e gera resposta personalizada"""
    doc = nlp(text)

    # Primeiro tenta ML
    ml_intent = predict_intent(text)
    proba = predict_proba(text)
    confidence = max(proba.values())

    # Threshold ajustado para 0.3
    if confidence < 0.3:
        intent = match_intent_rules(text)
    else:
        intent = ml_intent

    category, subcategory = CATEGORY_MAP.get(intent, CATEGORY_MAP["default"])
    entities = extract_entities(doc, text)

    # Usa o response_builder para montar resposta dinâmica
    reply = build_response(intent, entities)

    return {
        "category": category,
        "subcategory": subcategory,
        "intent": intent,
        "reply": reply,
        "tokens": [token.text for token in doc],
        "entities": entities,
        "confidence": confidence,
        "proba": proba
    }
