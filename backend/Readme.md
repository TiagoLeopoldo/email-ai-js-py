# Backend – Email Classifier AI

## Índice
- [Visão Geral](#visão-geral)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Dependências](#dependências)
- [Configuração da API Externa](#configuração-da-api-externa)
- [Execução](#execução)
- [Endpoints da API](#endpoints-da-api)
- [Exemplo de Uso](#exemplo-de-uso)
- [Logs](#logs)
- [Testes Manuais](#testes-manuais)
- [Limitações Conhecidas](#limitações-conhecidas)
- [Melhorias Futuras](#melhorias-futuras)

---

## Visão Geral
O backend foi desenvolvido em **Python/FastAPI** para classificar emails em três categorias: **Produtivo**, **Improdutivo** e **Irrelevante**.  
Ele aplica **pré-processamento NLP com NLTK** (remoção de stopwords, normalização e lematização) e consome a **OpenAI API** para análise de texto.  
Também suporta **upload de arquivos PDF**, realizando parsing automático do conteúdo.  
O sistema não depende de frases fixas: qualquer mensagem enviada é analisada pela IA, que interpreta o conteúdo e gera uma resposta natural e contextualizada.

---

## Estrutura do Projeto

```
backend/
├── app.py                     # Inicialização da aplicação FastAPI
├── core/                      # Configurações centrais
│   ├── config.py              # Variáveis de ambiente
│   ├── logging.py             # Configuração de logs
│   └── nlp.py                 # Funções de NLP
├── services/                  # Serviços auxiliares
│   ├── openai_service.py      # Integração com OpenAI
│   ├── pdf_service.py         # Extração de texto de PDFs
│   └── rules.py               # Regras fixas de classificação
├── routes/                    # Endpoints da API
│   ├── health.py              # /health
│   └── classify.py            # /classify e /classify-pdf
├── models/                    # Modelos Pydantic
│   └── schemas.py             # Schemas de entrada/saída
├── logs/
│   └── classify.log           # Logs de classificação
├── requirements.txt           # Dependências
└── README.md                  # Este documento
```

---

## Dependências

Instale via `requirements.txt`:

```bash
pip install -r requirements.txt
```

Principais pacotes:
- `fastapi`, `uvicorn` → API web
- `pydantic` → validação de dados
- `requests` → integração com OpenAI
- `nltk` → NLP (stopwords, lematização)
- `python-dotenv` → variáveis de ambiente
- `PyPDF2` → leitura de PDFs
- `python-multipart` → upload de arquivos

---

## Configuração da API Externa

Crie `.env` na pasta `backend`:

```
OPENAI_API_KEY=sua_chave_openai_aqui
OPENAI_MODEL=gpt-4.1-mini
```

---

## Execução

**Opção 1: raiz do projeto**
```bash
uvicorn backend.app:app --reload
```

**Opção 2: dentro da pasta backend**
```bash
cd backend
python -m uvicorn app:app --reload
```

Servidor disponível em:
```
http://127.0.0.1:8000
```

---

## Endpoints da API

| Endpoint        | Método | Descrição                                   | Request Body                         | Response Body (JSON)                       | Status Codes     |
|-----------------|--------|---------------------------------------------|--------------------------------------|--------------------------------------------|------------------|
| `/health`       | GET    | Verifica se o serviço está ativo            | —                                    | `{ "status": "ok" }`                       | 200              |
| `/classify`     | POST   | Classifica texto enviado em JSON            | `{ "text": "Preciso saber o status" }` | `{ "category": "...", "reply": "..." }`   | 200, 400, 500    |
| `/classify-pdf` | POST   | Classifica texto extraído de arquivo PDF    | `multipart/form-data` com campo `file` | `{ "category": "...", "reply": "..." }`   | 200, 400, 500    |

---

## Exemplo de Uso

### `/classify`
```json
{
  "text": "Preciso saber o status do pedido"
}
```

Resposta:
```json
{
  "category": "Produtivo",
  "reply": "Recebemos sua mensagem e já estamos cuidando dela para garantir uma solução rápida."
}
```

### `/classify-pdf` (curl)
```bash
curl -X POST "http://127.0.0.1:8000/classify-pdf" \
  -F "file=@exemplo.pdf"
```

---

## Logs

Arquivo: `backend/logs/classify.log`  

Formato:
```
YYYY-MM-DD HH:MM:SS | LEVEL | input=<texto> | PREPROCESSED=<texto após NLP> | output=<categoria e resposta>
```

---

## Testes Manuais

O sistema não depende de frases pré-definidas.  
O usuário pode enviar **qualquer mensagem de email** e o backend, integrado à **OpenAI API**, irá analisar o conteúdo e decidir a categoria mais adequada:

- **Produtivo:** mensagens que exigem ação ou resposta (ex.: solicitações de status, dúvidas sobre contratos, pedidos de suporte).  
- **Improdutivo:** mensagens que não exigem ação imediata (ex.: felicitações, agradecimentos).  
- **Irrelevante:** mensagens fora do escopo da empresa (ex.: brincadeiras, assuntos não relacionados).  

A IA gera também uma **resposta automática personalizada**, adaptada ao contexto da mensagem.  
Isso significa que não é um simples sistema de regras booleanas: mesmo que o usuário escreva frases diferentes ou complexas, o modelo de IA consegue interpretar e responder de forma natural.

#### Exemplos ilustrativos
- "Preciso saber o status do pedido" → Categoria: Produtivo → Resposta: confirma que a solicitação está sendo cuidada.  
- "Quero cancelar meu contrato" → Categoria: Produtivo → Resposta: informa que o cancelamento será tratado.  
- "Feliz Natal para toda a equipe" → Categoria: Improdutivo → Resposta: agradece cordialmente.  
- "Mensagem de agradecimento sem solicitação" → Categoria: Improdutivo → Resposta: agradece de forma simpática.  

---
