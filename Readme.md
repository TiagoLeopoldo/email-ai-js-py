# Email Classifier AI

## Índice
- [Visão Geral](#visão-geral)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Frontend](#frontend)
  - [Dependências](#dependências)
  - [Execução](#execução)
  - [Fluxo de Uso](#fluxo-de-uso)
- [Backend](#backend)
  - [Dependências](#dependências-1)
  - [Configuração da API Externa](#configuração-da-api-externa)
  - [Execução](#execução-1)
  - [Endpoints](#endpoints)
- [Integração Frontend ↔ Backend](#integração-frontend--backend)
- [Testes Manuais](#testes-manuais)
- [Deploy Online](#deploy-online)
- [Limitações Conhecidas](#limitações-conhecidas)
- [Melhorias Futuras](#melhorias-futuras)

---

## Visão Geral
O projeto **Email Classifier AI** foi desenvolvido como solução para uma empresa do setor financeiro que lida com alto volume de emails diariamente.  
Objetivo: **automatizar a leitura e classificação de emails** em categorias predefinidas e sugerir respostas automáticas, liberando tempo da equipe.

**Categorias de Classificação:**
- **Produtivo:** requer ação ou resposta específica.  
- **Improdutivo:** não requer ação imediata.  
- **Irrelevante:** não relacionado ao escopo da empresa.  

---

## Estrutura do Projeto

```
email-ai/
│
├── backend/                  # API em Python/FastAPI
│   ├── app.py
│   ├── core/                 # Configuração, logging, NLP
│   ├── services/             # Regras, OpenAI, PDF
│   ├── routes/               # Endpoints
│   ├── models/               # Schemas Pydantic
│   ├── logs/                 # classify.log
│   ├── requirements.txt
│   └── README.md             # Documentação backend
│
├── frontend/                 # Interface web
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   └── README.md             # Documentação frontend
│
├── .gitignore
└── README.md                 # Este documento
```

---

## Frontend

### Dependências
Não há dependências externas.  
Para servir localmente:
```bash
cd frontend
python -m http.server 3000
```

### Execução
1. Inicie o backend em `http://localhost:8000`.  
2. Sirva o frontend em `http://localhost:3000`.  
3. Abra no navegador: `http://localhost:3000`.

### Fluxo de Uso
1. Usuário digita texto ou faz upload de `.txt` ou `.pdf`.  
2. Clica em **Classificar e sugerir resposta**.  
3. Frontend envia requisição ao backend.  
4. Backend retorna categoria e resposta.  
5. Resultado exibido na tela.  
6. Campos de entrada são limpos após envio.

---

## Backend

### Dependências
Instale via `requirements.txt`:
```bash
pip install -r backend/requirements.txt
```

### Configuração da API Externa
Crie `.env` em `backend`:
```
OPENAI_API_KEY=sua_chave_openai_aqui
OPENAI_MODEL=gpt-4.1-mini
```

### Execução
```bash
uvicorn backend.app:app --reload
```

Servidor disponível em:
```
http://127.0.0.1:8000
```

### Endpoints
- **GET /health** → Verifica se o serviço está ativo.  
- **POST /classify** → Classifica texto enviado em JSON.  
- **POST /classify-pdf** → Classifica texto extraído de arquivo PDF.  

---

## Integração Frontend ↔ Backend
- Frontend consome endpoints do backend via `fetch`.  
- Em produção:  
  - **Frontend (Vercel):** `https://email-ai-js-py.vercel.app`  
  - **Backend (Render):** `https://email-ai-js-py.onrender.com`

---

Perfeito, Tiago 👌. Esse trecho do README realmente ficou parecendo que o sistema só reconhece frases fixas, quando na verdade ele está **integrado a uma IA (OpenAI)** e pode lidar com qualquer texto enviado pelo usuário. Vou reformular a seção **Testes Manuais** do README geral (e isso vale também para o backend/frontend) para deixar claro que não é um sistema de regras fixas, mas sim um classificador inteligente com IA.

---

### Testes Manuais

O sistema não depende de frases pré-definidas.  
O usuário pode enviar **qualquer mensagem de email** e o backend, integrado à **OpenAI API**, irá analisar o conteúdo e decidir a categoria mais adequada:

- **Produtivo:** mensagens que exigem ação ou resposta (ex.: solicitações de status, dúvidas sobre contratos, pedidos de suporte).  
- **Improdutivo:** mensagens que não exigem ação imediata (ex.: felicitações, agradecimentos).  
- **Irrelevante:** mensagens fora do escopo da empresa (ex.: brincadeiras, assuntos não relacionados).  

A IA gera também uma **resposta automática personalizada**, adaptada ao contexto da mensagem.  
Isso significa que não é um simples sistema de regras booleanas:  
mesmo que o usuário escreva frases diferentes ou complexas, o modelo de IA consegue interpretar e responder de forma natural.

#### Exemplos de teste
- "Preciso saber o status do pedido" → Categoria: Produtivo → Resposta: confirma que a solicitação está sendo cuidada.  
- "Quero cancelar meu contrato" → Categoria: Produtivo → Resposta: informa que o cancelamento será tratado.  
- "Feliz Natal para toda a equipe" → Categoria: Improdutivo → Resposta: agradece cordialmente.  
- "Mensagem de agradecimento sem solicitação" → Categoria: Improdutivo → Resposta: agradece de forma simpática.  

Esses exemplos são apenas ilustrativos.  
Na prática, o sistema aceita **qualquer frase** e a IA decide a categoria e resposta de acordo com o conteúdo.

Verificar:
- Categoria correta.  
- Resposta coerente.  
- Campos limpos após envio.  
- Logs registrados em `classify.log`.  

---

## Deploy Online
- **Frontend (Vercel):**  
  `https://email-ai-js-py.vercel.app`  
- **Backend (Render):**  
  `https://email-ai-js-py.onrender.com`

---

