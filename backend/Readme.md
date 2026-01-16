# Backend – Email Classifier AI

## Visão Geral
Backend desenvolvido em **Python** com **FastAPI** para classificar textos de emails em intenções operacionais, extrair entidades e gerar respostas automáticas com base em regras e probabilidades.

---

## Estrutura do Projeto

```
backend/
│
├── logs/
│   └── classify.log           # Logs de classificação
├── nlp/
│   ├── __init__.py
│   ├── classifier.py          # Orquestra a classificação e extração de entidades
│   ├── ml_classifier.py       # Classificador ML (probabilidades, modelo/regra)
│   └── training_data.py       # Dados e expressões para treino/heurísticas
├── utils/
│   ├── __init__.py
│   ├── replies.py             # Frases base e templates de resposta
│   └── response_builder.py    # Montagem da resposta final (contexto + entidades)
├── app.py                     # Aplicação FastAPI (endpoints /health e /classify)
├── requirements.txt           # Dependências do backend
└── README.md                  # Este documento
```

### Descrição dos Módulos
- **app.py**: inicializa FastAPI, configura CORS, define modelos de entrada, expõe `/health` e `/classify`, registra logs e retorna JSON.  
- **nlp/classifier.py**: função `classify_text(text)` que normaliza entrada, chama `ml_classifier`, extrai entidades, define categoria/subcategoria e retorna o resultado.  
- **nlp/ml_classifier.py**: lógica de classificação (modelo simples/heurístico), retorna `intent`, `proba` e `confidence`.  
- **nlp/training_data.py**: vocabulários, padrões e listas de apoio para intenções e entidades.  
- **utils/replies.py**: textos base e variações de resposta por intenção.  
- **utils/response_builder.py**: compõe a resposta final usando intenção, entidades e contexto.  
- **logs/classify.log**: arquivo de log com entradas de classificação.  

---

## Dependências

Instale via `requirements.txt`:

```bash
pip install -r requirements.txt
```

Após instalar, baixe o modelo de linguagem portuguesa para spaCy:

```bash
python -m spacy download pt_core_news_sm
```

Principais pacotes:
- fastapi  
- uvicorn  
- pydantic  
- scikit-learn  
- spacy>=3.0  

---

## Execução

**Opção 1: Executar da raiz do projeto**
```bash
uvicorn backend.app:app --reload
```

**Opção 2: Executar de dentro da pasta backend**
```bash
cd backend
uvicorn app:app --reload
```

Aplicação disponível em:
```
http://127.0.0.1:8000
```

---

## Endpoints da API

| Endpoint    | Método | Descrição                                   | Request Body (JSON)                         | Response Body (JSON)                       | Status Codes     |
|-------------|--------|---------------------------------------------|---------------------------------------------|--------------------------------------------|------------------|
| `/health`   | GET    | Verifica se o serviço está ativo            | —                                           | `{ "status": "ok" }`                       | 200              |
| `/classify` | POST   | Classifica o texto e retorna dados completos| `{ "text": "Quero cancelar meu contrato" }` | Campos: `category`, `subcategory`, `intent`, `reply`, `tokens`, `entities`, `confidence`, `proba` | 200, 400, 500    |

### Exemplo de Requisição
```json
{
  "text": "Quero cancelar meu contrato"
}
```

### Exemplo de Resposta
```json
{
  "category": "Operacional",
  "subcategory": "cancelamento",
  "intent": "cancelamento",
  "reply": "Certo, você deseja cancelar. Vou encaminhar para realizar o cancelamento com segurança. Contexto identificado: contrato.",
  "tokens": ["Quero", "cancelar", "meu", "contrato"],
  "entities": [
    { "text": "contrato", "label": "CONTRACT" }
  ],
  "confidence": 0.5021,
  "proba": {
    "cancelamento": 0.5021,
    "erro": 0.1124,
    "humano": 0.1118,
    "prazo": 0.1214,
    "status": 0.1521
  }
}
```

---

## Status Codes

- **200 OK**: requisição bem-sucedida; resposta contém dados de classificação.  
- **400 Bad Request**: texto inválido ou muito curto.  
  ```json
  { "detail": "Texto muito curto para classificação." }
  ```
- **500 Internal Server Error**: erro inesperado na lógica de classificação ou falha não tratada.  

---

## Modelo de Dados

### Request
- **text**: string obrigatória com o conteúdo a classificar.  

### Response
- **category**: string (ex.: "Operacional").  
- **subcategory**: string (ex.: "cancelamento").  
- **intent**: string (ex.: "cancelamento", "prazo", "status", "erro", "humano").  
- **reply**: string com resposta sugerida.  
- **tokens**: array de strings com tokens do texto.  
- **entities**: array de objetos `{ "text": string, "label": string }`.  
- **confidence**: número (float) entre 0 e 1.  
- **proba**: objeto com probabilidades por intenção.  

---

## Logs

Arquivo: `backend/logs/classify.log`  

Formato de linha:
```
YYYY-MM-DD HH:MM:SS | LEVEL | input=<texto> | intent=<intent> | confidence=<float> | entities=<lista>
```

Exemplo:
```
2026-01-16 16:45:12 | INFO | input=Quero cancelar meu contrato | intent=cancelamento | confidence=0.5021 | entities=[{'text': 'contrato', 'label': 'CONTRACT'}]
```

---

## Integração com Frontend

- CORS habilitado para chamadas a partir de `http://localhost:3000`.  
- Exemplo de consumo:
```javascript
const res = await fetch("http://localhost:8000/classify", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ text: "Quero cancelar meu contrato" })
});
const data = await res.json();
console.log(data.reply);
```

---

## Testes Manuais

Frases para validação de intenções:
- **cancelamento**: "Quero cancelar meu contrato"  
- **prazo**: "Preciso saber o prazo do projeto 123"  
- **status**: "Quero acompanhar o status do pedido 789"  
- **erro**: "Recebi uma mensagem de erro durante o processo"  
- **humano**: "Quero falar com um atendente humano"  

Verificar:
- `intent`, `reply`, `entities`, `confidence` e `proba` coerentes.  
- Registro em `classify.log`.  

---

## Limitações Conhecidas
- Extração de texto de PDF não implementada.  
- Classificador baseado em regras e heurísticas simples; pode ser expandido para maior precisão.  

---

## Melhorias Futuras
- Implementar parsing real de PDF.  
- Adicionar testes automatizados (unitários e integração).  
- Evoluir modelo de NLP para maior robustez.  
- Adicionar observabilidade (rotação de logs, métricas e tracing).  

---

## Notas de Manutenção
- **Imports internos**: utilizar caminhos absolutos do pacote (ex.: `from nlp.classifier import classify_text`).  
- **Encoding**: respostas JSON devem usar `charset=utf-8`.  
- **CORS**: manter domínios do frontend na lista `allow_origins` conforme ambiente.  
