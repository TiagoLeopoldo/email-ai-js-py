# Frontend – Email Classifier AI

## Visão Geral
Este frontend foi desenvolvido utilizando **HTML**, **CSS** e **JavaScript puro**, sem frameworks ou bibliotecas externas.  
O objetivo é permitir que o usuário insira ou envie o conteúdo de um email, envie esse conteúdo ao backend via requisição HTTP e visualize a classificação e resposta sugerida.  

Atualmente o frontend possui:
- **Estado de carregamento** (botão desabilitado + mensagem “Processando…”).  
- **Tratamento de erros padronizado**, exibindo mensagens diretamente na interface.  
- **Validação de limite de texto** (máximo de 2000 caracteres).  
- **Feedback visual aprimorado**: cores diferenciadas para categorias (verde para produtivo, vermelho para improdutivo), contraste melhorado e responsividade básica.  

---

## Estrutura do Projeto

```
frontend/
│
├── index.html           # Página principal da aplicação
├── styles.css           # Estilos visuais da interface
└── script.js            # Lógica de interação e comunicação com o backend
```

### Descrição dos Arquivos

- **index.html**  
  Estrutura da interface: cabeçalho, formulário com campo de texto e upload de arquivo, botão de envio e área de exibição de resultados.  
  Inclui elementos para exibir **estado de carregamento**, **mensagens de erro**, validação de limite de texto e feedback visual.

- **styles.css**  
  Estilização básica: layout centralizado, botões, campos de entrada e área de resultados.  
  Inclui estilos para o botão desabilitado, para a mensagem de carregamento, para mensagens de erro em destaque vermelho e para categorias com cores diferenciadas (verde/vermelho).  
  Responsividade básica para telas menores.

- **script.js**  
  Captura o envio do formulário, trata entrada de texto ou arquivo `.txt`/`.pdf`, envia requisição `POST` para o backend (`/classify`) e exibe os dados retornados (`category`, `reply`).  
  Controla o estado de carregamento, exibe erros diretamente no card de resultados, valida o limite máximo de caracteres e aplica classes visuais para diferenciar categorias.

---

## Requisitos e Execução

### Pré-requisitos
- Backend deve estar rodando em `http://localhost:8000` com CORS habilitado.  
- Navegador moderno com suporte a `fetch` e `FileReader`.

### Como Executar
1. Inicie o backend com:
   ```bash
   python -m uvicorn app:app --reload
   ```
2. Sirva o frontend via servidor local para evitar problemas de CORS:
   ```bash
   cd frontend
   python -m http.server 3000
   ```
3. Acesse no navegador:
   ```
   http://localhost:3000
   ```
4. Digite um texto ou envie um arquivo `.txt` ou `.pdf`.  
5. Clique em “Classificar e sugerir resposta”.  
6. O resultado será exibido na seção “Resultado”.  
7. Durante o processamento, o botão ficará desabilitado e aparecerá a mensagem **“Processando…”**.  
8. Se ocorrer erro, a mensagem será exibida no card de resultados.  
9. Se o texto ultrapassar **2000 caracteres**, o envio será bloqueado e aparecerá a mensagem:  
   **“O texto excede o limite de 2000 caracteres. Reduza o conteúdo e tente novamente.”**  
10. A categoria será exibida com cores diferenciadas:  
    - Verde para **Produtivo**.  
    - Vermelho para **Improdutivo**.  

---

## Fluxo de Uso

1. **Entrada de texto**  
   - Usuário digita diretamente no campo `textarea`.  
   - O texto é enviado ao backend via `fetch`.  
   - Se ultrapassar 2000 caracteres, o envio é bloqueado.

2. **Upload de arquivo**  
   - `.txt`: conteúdo lido no frontend e enviado como texto.  
   - `.pdf`: texto não é extraído no frontend; uma mensagem placeholder é enviada ao backend.  
   - Se o conteúdo do `.txt` ultrapassar 2000 caracteres, o envio é bloqueado.

3. **Resposta exibida**  
   - Categoria (badge colorida: verde ou vermelho).  
   - Resposta sugerida (texto formatado).  
   - Em caso de erro, mensagem exibida no card de resultados em vermelho.

4. **Estado de carregamento**  
   - Botão desabilitado durante requisição.  
   - Mensagem “Processando…” exibida abaixo do botão.

---

## Validações e Tratamento de Erros

- Nenhum texto ou arquivo → **“Nenhum texto ou arquivo válido foi fornecido.”**  
- Formato inválido → **“Formato de arquivo não suportado. Use apenas .txt ou .pdf.”**  
- Texto acima de 2000 caracteres → **“O texto excede o limite de 2000 caracteres. Reduza o conteúdo e tente novamente.”**  
- Erro interno → **“Erro interno ao processar sua solicitação. Tente novamente mais tarde.”**  
- Falha de conexão → **“Não foi possível conectar ao servidor. Verifique sua conexão e tente novamente.”**  
- Todas as mensagens de erro são exibidas diretamente no card de resultados, em vermelho.  
- Estado de carregamento garante que o usuário saiba que a requisição está em andamento.  
- Feedback visual reforça a categoria com cores diferenciadas.  

---

## Testes Manuais

### Casos de Entrada
- Texto direto: “Preciso saber o status da minha solicitação de suporte.”  
- Upload `.txt`: arquivo com conteúdo “Quero cancelar meu contrato.”  
- Upload `.pdf`: qualquer arquivo PDF (envia placeholder).  
- Texto longo (>2000 caracteres): string repetida para simular excesso.  

### Resultado Esperado
- Categoria exibida corretamente (**Produtivo** ou **Improdutivo**) com cores diferenciadas.  
- Resposta sugerida coerente com a intenção.  
- Layout funcional e responsivo.  
- Botão desabilitado e mensagem “Processando…” durante requisição.  
- Mensagens de erro exibidas no card em caso de falha.  
- Texto acima de 2000 caracteres bloqueado com mensagem clara.  

---

## Limitações Conhecidas
- Extração de texto de arquivos `.pdf` não é realizada no frontend.  
- Interface simples, sem responsividade avançada ou acessibilidade estendida.  
- Não há testes automatizados ou cobertura de casos extremos.  

---

## Melhorias Futuras
- Implementar leitura de `.pdf` via biblioteca JS (ex.: PDF.js).  
- Adicionar validações de conteúdo e feedback visual mais detalhado.  
- Melhorar responsividade e acessibilidade.  
- Implementar testes automatizados (unitários e integração).  
```
