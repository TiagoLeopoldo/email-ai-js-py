# Backend – Email Classifier AI

## Visão Geral
Backend desenvolvido em **Python** com **FastAPI** para classificar textos de emails em duas categorias principais: **Produtivo** e **Improdutivo**.  
O sistema consome a **OpenAI API** para análise de texto e retorna a categoria e uma resposta sugerida para o frontend.  
Agora também suporta **upload de arquivos PDF**, realizando parsing automático do conteúdo.  
Além disso, o backend realiza **pré-processamento NLP com NLTK** (remoção de stopwords, normalização e lematização) antes de enviar o texto para a API externa.

---

## Estrutura do Projeto

```
backend/
│
├── logs/
│   └── classify.log           # Logs de classificação
├── app.py                     # Aplicação FastAPI (endpoints /health, /classify e /classify-pdf)
├── requirements.txt           # Dependências do backend
└── README.md                  # Este documento
```

### Descrição dos Módulos
- **app.py**: inicializa FastAPI, configura CORS, define modelos de entrada, aplica pipeline NLP (stopwords + lematização), consome a OpenAI API, registra logs e retorna JSON.  
- **logs/classify.log**: arquivo de log com entradas de classificação.  

---

## Dependências

Instale via `requirements.txt`:

```bash
pip install -r requirements.txt
```

Conteúdo atualizado do `requirements.txt`:

```txt
fastapi
uvicorn[standard]
pydantic
requests
nltk
python-dotenv
PyPDF2
python-multipart
```

> **Nota:** Na primeira execução, o backend baixa automaticamente os recursos necessários do NLTK (stopwords, wordnet, punkt).

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

Durante a primeira execução, o backend pode baixar corpora do NLTK (stopwords, wordnet, punkt). Isso é feito automaticamente.

---

## Endpoints da API

| Endpoint        | Método | Descrição                                   | Request Body                         | Response Body (JSON)                       | Status Codes     |
|-----------------|--------|---------------------------------------------|--------------------------------------|--------------------------------------------|------------------|
| `/health`       | GET    | Verifica se o serviço está ativo            | —                                    | `{ "status": "ok" }`                       | 200              |
| `/classify`     | POST   | Classifica texto enviado em JSON            | `{ "text": "Preciso saber o status" }` | Campos: `category`, `reply`                | 200, 400, 500    |
| `/classify-pdf` | POST   | Classifica texto extraído de arquivo PDF    | `multipart/form-data` com campo `file` | Campos: `category`, `reply`                | 200, 400, 500    |

> **Nota:** O texto enviado é normalizado, tokenizado, tem stopwords removidas e passa por lematização antes de ser classificado.

### Exemplo de Requisição `/classify`
```json
{
  "text": "Preciso saber o status do pedido"
}
```

### Exemplo de Resposta `/classify`
```json
{
  "category": "Produtivo",
  "reply": "Recebemos sua mensagem e já estamos cuidando dela para garantir uma solução rápida."
}
```

### Exemplo de Requisição `/classify-pdf` (curl)
```bash
curl -X POST "http://127.0.0.1:8000/classify-pdf" \
  -F "file=@exemplo.pdf"
```

### Exemplo de Resposta `/classify-pdf`
```json
{
  "category": "Improdutivo",
  "reply": "Agradecemos sua mensagem! Não é necessário nenhuma ação neste momento."
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
YYYY-MM-DD HH:MM:SS | LEVEL | input=<texto> | PREPROCESSED=<texto após NLP> | output=<categoria e resposta>
```

Exemplo:
```
2026-01-16 16:45:12 | INFO | input=Preciso saber o status do pedido | PREPROCESSED=preciso saber status pedido | output={'category': 'Produtivo', 'reply': 'Recebemos sua mensagem e já estamos cuidando dela para garantir uma solução rápida.'}
```

---

## Integração com Frontend

- CORS habilitado para chamadas a partir dos domínios do Vercel.  
- Exemplo de consumo `/classify`:
```javascript
const res = await fetch("https://email-ai-js-py.onrender.com/classify", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ text: "Preciso saber o status do pedido" })
});
const data = await res.json();
console.log(data.reply);
```

- Exemplo de consumo `/classify-pdf`:
```javascript
const formData = new FormData();
formData.append("file", file);

const res = await fetch("https://email-ai-js-py.onrender.com/classify-pdf", {
  method: "POST",
  body: formData
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
- Registro em `classify.log` com campo `PREPROCESSED` mostrando texto após NLP  
- Resposta vinda da OpenAI API  
- Upload de PDF funcionando corretamente  

---

## Limitações Conhecidas
- Dependência da resposta da OpenAI API; pode variar conforme modelo usado.  
- Parsing de PDF depende da qualidade do arquivo (PDFs escaneados como imagem não são suportados).  
- A lematização do NLTK é baseada em inglês; para português pode não ser perfeita, mas ajuda a reduzir variações.  

---

## Melhorias Futuras
- Suporte a OCR para PDFs escaneados.  
- Adicionar testes automatizados.  
- Evoluir integração com modelos mais robustos.  
- Adicionar observabilidade (rotação de logs, métricas e tracing).  

---

## Notas de Manutenção
- **CORS**: manter domínios do frontend na lista `allow_origins` conforme ambiente.  
- **API externa**: definir chave de acesso como variável de ambiente (`OPENAI_API_KEY`).  
- **Encoding**: respostas JSON devem usar `charset=utf-8`.  
- **NLP**: pipeline atual remove stopwords e aplica lematização; revisar periodicamente para melhorar suporte ao português.  
