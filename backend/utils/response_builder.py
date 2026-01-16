# backend/utils/response_builder.py
from utils.replies import REPLIES

def build_response(intent: str, entities: list) -> str:
    base_reply = REPLIES.get(intent, REPLIES["default"])

    # Números (ex: ID de pedido, contrato, solicitação)
    numbers = [e["text"] for e in entities if e["label"] in ("NUMBER", "CARDINAL")]
    if numbers:
        base_reply = base_reply.replace(".", f" (referência: {', '.join(numbers)}).")

    # Datas
    dates = [e["text"] for e in entities if e["label"] == "DATE"]
    if dates:
        base_reply += f" Data mencionada: {', '.join(dates)}."

    # Entidades de domínio — resposta mais natural
    domain_map = {
        "ORDER": "pedido",
        "CONTRACT": "contrato",
        "SUBSCRIPTION": "assinatura",
        "PROJECT": "projeto",
        "REQUEST": "solicitação"
    }
    domain_entities = [domain_map[e["label"]] for e in entities if e["label"] in domain_map]
    if domain_entities:
        # Se houver mais de uma, junta com vírgula
        base_reply += f" Contexto identificado: {', '.join(domain_entities)}."

    return base_reply
