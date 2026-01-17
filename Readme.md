# Email Classifier AI

## Índice
- [Visão Geral](#visão-geral)  
- [Estrutura do Projeto](#estrutura-do-projeto)  
- [Backend](#backend)  
  - [Dependências](#dependências)  
  - [Configuração da API Externa](#configuração-da-api-externa)  
  - [Execução](#execução)  
  - [Endpoints](#endpoints)  
  - [Logs](#logs)  
- [Frontend](#frontend)  
  - [Estrutura](#estrutura)  
  - [Execução](#execução-1)  
  - [Fluxo de Uso](#fluxo-de-uso)  
  - [Estados de Carregamento e Erros](#estados-de-carregamento-e-erros)  
- [Integração Frontend ↔ Backend](#integração-frontend--backend)  
- [Testes Manuais](#testes-manuais)  
- [Testar Online (Deploy)](#testar-online-deploy)  
- [Limitações Conhecidas](#limitações-conhecidas)  
- [Melhorias Futuras](#melhorias-futuras)  

---

## Visão Geral
O projeto **Email Classifier AI** tem como objetivo classificar textos de emails em duas categorias principais — **Produtivo** e **Improdutivo** — e sugerir respostas automáticas adequadas.  
A solução é composta por dois módulos:

- **Backend**: API em Python/FastAPI que consome a **OpenAI API** para classificação e geração de respostas.  
- **Frontend**: Interface em HTML/CSS/JavaScript para interação com o usuário.  

---

## Estrutura do Projeto

```
email-ai/
│
├── backend/
│   ├── logs/
│   │   └── classify.log
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   └── README.md
│
└── README.md   # Este documento
```

---

## Backend

### Dependências
Instale as dependências listadas em `backend/requirements.txt`:

```bash
pip install -r backend/requirements.txt
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

### Configuração da API Externa
Este backend consome a **OpenAI API**.  
É necessário definir a variável de ambiente `OPENAI_API_KEY` com sua chave de acesso.  

No Render ou em execução local:
1. Crie um arquivo `.env` dentro da pasta `backend`.  
2. Adicione as variáveis:  
   ```
   OPENAI_API_KEY=sua_chave_openai_aqui
   OPENAI_MODEL=gpt-4.1-mini
   ```

### Execução

**Opção 1: Executar da raiz do projeto**
```bash
uvicorn backend.app:app --reload
```

**Opção 2: Executar de dentro da pasta backend**
```bash
cd backend
python -m uvicorn app:app --reload
```

O servidor estará disponível em:
```
http://127.0.0.1:8000
```

### Endpoints

| Endpoint        | Método | Descrição                                   | Request Body                         | Response Body (JSON)                       | Status Codes     |
|-----------------|--------|---------------------------------------------|--------------------------------------|--------------------------------------------|------------------|
| `/health`       | GET    | Verifica se o serviço está ativo            | —                                    | `{ "status": "ok" }`                       | 200              |
| `/classify`     | POST   | Classifica texto enviado em JSON            | `{ "text": "Preciso saber o status" }` | Campos: `category`, `reply`                | 200, 400, 500    |
| `/classify-pdf` | POST   | Classifica texto extraído de arquivo PDF    | `multipart/form-data` com campo `file` | Campos: `category`, `reply`                | 200, 400, 500    |

---

## Frontend

### Estrutura
- **index.html**: página principal com formulário de entrada e área de resultados.  
- **styles.css**: estilos da interface.  
- **script.js**: lógica de envio de requisições ao backend e exibição dos resultados.  

### Execução
Para evitar problemas de CORS, recomenda-se servir o frontend via servidor local:

```bash
cd frontend
python -m http.server 3000
```

Acesse no navegador:
```
http://localhost:3000
```

### Fluxo de Uso
1. Digite o texto do email no campo de texto ou faça upload de um arquivo `.txt` ou `.pdf`.  
2. Clique em **Classificar e sugerir resposta**.  
3. O frontend envia requisição `POST`:  
   - Texto ou `.txt` → `/classify`  
   - `.pdf` → `/classify-pdf`  
4. O backend retorna a classificação e resposta sugerida.  
5. O resultado é exibido na seção **Resultado**.  

---

## Integração Frontend ↔ Backend

### Pré-requisitos
- Backend rodando em `http://localhost:8000`.  
- Frontend servido em `http://localhost:3000`.  
- Navegador moderno.  

### Passo a passo
1. Inicie o backend:
   ```bash
   python -m uvicorn app:app --reload
   ```
2. Sirva o frontend:
   ```bash
   cd frontend
   python -m http.server 3000
   ```
3. Acesse `http://localhost:3000`.  
4. Digite ou envie um arquivo de email.  
5. Clique em **Classificar e sugerir resposta**.  
6. Veja a categoria e resposta sugerida exibidas na tela.  

---

## Testes Manuais

### Casos de entrada
- **Produtivo:** "Preciso saber o prazo do projeto 123"  
- **Produtivo:** "Quero acompanhar o status do pedido 789"  
- **Improdutivo:** "Feliz Natal para toda a equipe"  
- **Improdutivo:** "Mensagem de agradecimento sem solicitação"  

### Resultado esperado
- Categoria exibida corretamente.  
- Resposta sugerida coerente com a intenção.  
- Registro em `classify.log`.  
- Botão desabilitado e mensagem “Processando…” durante requisição.  
- Mensagens de erro exibidas no card em caso de falha.  
- Upload de `.pdf` funcionando corretamente.  

---

## Testar Online (Deploy)

- **Frontend (Vercel):**  
  `https://email-ai-js-py.vercel.app`  
- **Backend (Render):**  
  `https://email-ai-js-py.onrender.com`

---

## Limitações Conhecidas
- PDFs escaneados como imagem não são suportados (apenas PDFs com texto).  
- Interface simples, sem design avançado.  
- Dependência da API externa (resultados podem variar conforme modelo da OpenAI).  
- Não há testes automatizados.  

---

## Melhorias Futuras
- Implementar suporte a OCR para PDFs escaneados.  
- Adicionar testes automatizados (unitários e integração).  
- Melhorar interface (responsividade, acessibilidade, design mais moderno).  
- Evoluir integração com modelos mais robustos da OpenAI ou Hugging Face.  
- Documentar e automatizar deploy em Vercel (frontend) e Render (backend).  
- Adicionar observabilidade (logs avançados, métricas e tracing).  
