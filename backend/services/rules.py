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
