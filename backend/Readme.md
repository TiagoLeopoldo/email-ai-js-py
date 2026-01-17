# Backend – Email Classifier AI

## Visão Geral
Backend desenvolvido em **Python** com **FastAPI** para classificar textos de emails em duas categorias principais: **Produtivo** e **Improdutivo**.  
O sistema consome a **OpenAI API** para análise de texto e retorna a categoria e uma resposta sugerida para o frontend.

---

## Estrutura do Projeto

```
backend/
│
├── logs/
│   └── classify.log           # Logs de classificação
├── app.py                     # Aplicação FastAPI (endpoints /health e /classify)
├── requirements.txt           # Dependências do backend
└── README.md                  # Este documento
```

### Descrição dos Módulos
- **app.py**: inicializa FastAPI, configura CORS, define modelos de entrada, consome a OpenAI API, registra logs e retorna JSON.  
- **logs/classify.log**: arquivo de log com entradas de classificação.  

---

## Dependências

Instale via `requirements.txt`:

```bash
pip install -r requirements.txt
```

Conteúdo do `requirements.txt`:

```txt
fastapi
uvicorn[standard]
pydantic
requests
nltk
python-dotenv
```

---

## Configuração da API Externa

Este backend consome a **OpenAI API**.  
É necessário definir a variável de ambiente `OPENAI_API_KEY` com sua chave de acesso.  

### Configuração local
Crie um arquivo `.env` dentro da pasta `backend` com o conteúdo:

```
OPENAI_API_KEY=sua_chave_openai_aqui
OPENAI_MODEL=gpt-4.1-mini
```

### Configuração no Render
1. Vá em **Dashboard → Service → Environment**.  
2. Adicione as variáveis:  
   - **Key**: `OPENAI_API_KEY`  
   - **Value**: sua chave da OpenAI.  
   - **Key**: `OPENAI_MODEL`  
   - **Value**: `gpt-4.1-mini`  

---

## Execução

**Opção 1: Executar da raiz do projeto**
```bash
uvicorn backend.app:app --reload
```

**Opção 2: Executar de dentro da pasta backend**
```bash
cd backend
python -m uvicorn app:app --reload
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
| `/classify` | POST   | Classifica o texto via OpenAI API           | `{ "text": "Preciso saber o status do pedido" }` | Campos: `category`, `reply`                | 200, 400, 500    |

### Exemplo de Requisição
```json
{
  "text": "Preciso saber o status do pedido"
}
```

### Exemplo de Resposta
```json
{
  "category": "Produtivo",
  "reply": "Recebemos sua mensagem e já estamos cuidando dela para garantir uma solução rápida."
}
```

---

## Status Codes

- **200 OK**: requisição bem-sucedida; resposta contém dados de classificação.  
- **400 Bad Request**: texto inválido ou muito curto.  
  ```json
  { "detail": "Texto muito curto para classificação." }
  ```
- **500 Internal Server Error**: erro inesperado ou falha na comunicação com a API externa.  

---

## Logs

Arquivo: `backend/logs/classify.log`  

Formato de linha:
```
YYYY-MM-DD HH:MM:SS | LEVEL | input=<texto> | output=<categoria e resposta>
```

Exemplo:
```
2026-01-16 16:45:12 | INFO | input=Preciso saber o status do pedido | output={'category': 'Produtivo', 'reply': 'Recebemos sua mensagem e já estamos cuidando dela para garantir uma solução rápida.'}
```

---

## Integração com Frontend

- CORS habilitado para chamadas a partir dos domínios do Vercel.  
- Exemplo de consumo:
```javascript
const res = await fetch("https://email-ai-js-py.onrender.com/classify", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ text: "Preciso saber o status do pedido" })
});
const data = await res.json();
console.log(data.reply);
```

---

## Testes Manuais

Frases para validação:
- "Preciso saber o status do pedido" → Produtivo  
- "Quero cancelar meu contrato" → Produtivo  
- "Feliz Natal para toda a equipe" → Improdutivo  
- "Mensagem de agradecimento sem solicitação" → Improdutivo  

Verificar:
- `category` e `reply` coerentes  
- Registro em `classify.log`  
- Resposta vinda da OpenAI API  

---

## Limitações Conhecidas
- Extração de texto de PDF não implementada.  
- Dependência da resposta da OpenAI API; pode variar conforme modelo usado.  

---

## Melhorias Futuras
- Implementar parsing real de PDF.  
- Adicionar testes automatizados.  
- Evoluir integração com modelos mais robustos.  
- Adicionar observabilidade (rotação de logs, métricas e tracing).  

---

## Notas de Manutenção
- **CORS**: manter domínios do frontend na lista `allow_origins` conforme ambiente.  
- **API externa**: definir chave de acesso como variável de ambiente (`OPENAI_API_KEY`).  
- **Encoding**: respostas JSON devem usar `charset=utf-8`.  

