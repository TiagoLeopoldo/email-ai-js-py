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
*(sem alterações nesta parte, permanece igual ao que você enviou)*

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

Se abrir o `index.html` diretamente (via `file://`), o navegador pode bloquear a requisição ao backend.

### Fluxo de Uso
1. Digite o texto do email no campo de texto ou faça upload de um arquivo `.txt` ou `.pdf`.  
2. Clique em **Classificar e sugerir resposta**.  
3. O frontend envia requisição `POST` para `http://localhost:8000/classify`.  
4. O backend retorna a classificação e resposta sugerida.  
5. O resultado é exibido na seção **Resultado**.  

### Estados de Carregamento e Erros
- Durante o envio da requisição, o botão **Classificar e sugerir resposta** fica **desabilitado**.  
- É exibida a mensagem **“Processando…”** abaixo do botão.  
- Caso ocorra algum erro (ex.: falha de conexão ou resposta inválida), o erro é mostrado dentro do card de resultados, em vez de apenas via `alert`.  
- Isso garante uma experiência mais clara e amigável para o usuário.  

---

## Integração Frontend ↔ Backend
*(sem alterações, permanece igual)*

---

## Testes Manuais
*(sem alterações, permanece igual)*

---

## Testar Online (Deploy)
*(sem alterações, permanece igual)*

---

## Limitações Conhecidas
- Extração de texto de arquivos `.pdf` não implementada.  
- Interface simples, sem design avançado.  
- Dependência da API externa (variação de resultados).  
- Não há testes automatizados.  

---

## Melhorias Futuras
- Implementar parsing real de PDF.  
- Adicionar testes automatizados (unitários e integração).  
- Melhorar interface (responsividade, acessibilidade).  
- Evoluir integração com modelos mais robustos.  
- Documentar deploy em Vercel (frontend) e Render (backend).  
