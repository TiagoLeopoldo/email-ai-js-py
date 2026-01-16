# Email Classifier AI

## Visão Geral
O projeto **Email Classifier AI** tem como objetivo classificar textos de emails em diferentes intenções operacionais e sugerir respostas automáticas com base em regras de negócio e entidades extraídas.  
Ele é composto por dois módulos principais:

- **Backend**: API em Python/FastAPI responsável pela classificação e geração de respostas.  
- **Frontend**: Interface em HTML/CSS/JS para interação com o usuário.  

Este documento centraliza a documentação necessária para instalação, execução, integração e testes.

---

## Estrutura do Projeto

```
email-ai/
│
├── backend/
│   ├── logs/
│   │   └── classify.log
│   ├── nlp/
│   │   ├── __init__.py
│   │   ├── classifier.py
│   │   ├── ml_classifier.py
│   │   └── training_data.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── replies.py
│   │   └── response_builder.py
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

Após instalar, baixe o modelo de linguagem portuguesa para spaCy:

```bash
python -m spacy download pt_core_news_sm
```

Este modelo é necessário para a extração de entidades e processamento de texto em português.

### Execução

**Opção 1: Executar da raiz do projeto**
```bash
uvicorn backend.app:app --reload
```

**Opção 2: Executar de dentro da pasta backend**
```bash
cd backend
uvicorn app:app --reload
```

O servidor estará disponível em:
```
http://127.0.0.1:8000
```

### Endpoints

| Endpoint    | Método | Descrição                                   | Request Body (JSON)                         | Response Body (JSON)                       | Status Codes     |
|-------------|--------|---------------------------------------------|---------------------------------------------|--------------------------------------------|------------------|
| `/health`   | GET    | Verifica se o serviço está ativo            | —                                           | `{ "status": "ok" }`                       | 200              |
| `/classify` | POST   | Classifica o texto e retorna dados completos| `{ "text": "Quero cancelar meu contrato" }` | Campos: `category`, `subcategory`, `intent`, `reply`, `tokens`, `entities`, `confidence`, `proba` | 200, 400, 500    |

### Exemplo de requisição
```json
{
  "text": "Quero cancelar meu contrato"
}
```

### Exemplo de resposta
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

### Logs
Todos os requests ao endpoint `/classify` são registrados em `backend/logs/classify.log`.

---

## Frontend

### Estrutura
- **index.html**: página principal com formulário de entrada e área de resultados.  
- **styles.css**: estilos básicos da interface.  
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

Se abrir o `index.html` diretamente (via `file://`), o navegador pode bloquear a requisição ao backend.

### Fluxo de uso
1. Digite o texto do email no campo de texto ou faça upload de um arquivo `.txt` ou `.pdf`.  
2. Clique em **Classificar e sugerir resposta**.  
3. O frontend envia requisição `POST` para `http://localhost:8000/classify`.  
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
   uvicorn backend.app:app --reload
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
- **Cancelamento:** "Quero cancelar meu contrato"  
- **Prazo:** "Preciso saber o prazo do projeto 123"  
- **Status:** "Quero acompanhar o status do pedido 789"  
- **Erro:** "Recebi uma mensagem de erro durante o processo"  
- **Humano:** "Quero falar com um atendente humano"  

### Resultado esperado
- Categoria exibida corretamente.  
- Resposta sugerida coerente com a intenção.  
- Entidades extraídas quando aplicável.  
- Registro em `classify.log`.  

---

## Limitações Conhecidas
- Extração de texto de arquivos `.pdf` não implementada.  
- Interface simples, sem design avançado.  
- Não há testes automatizados.  

---

## Melhorias Futuras
- Implementar parsing real de PDF.  
- Adicionar testes automatizados (unitários e integração).  
- Melhorar interface (responsividade, acessibilidade).  
- Expandir modelo de NLP para maior precisão.  
- Documentar deploy em Vercel (frontend) e Render/Railway (backend).  
