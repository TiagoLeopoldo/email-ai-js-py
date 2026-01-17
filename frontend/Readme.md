# Frontend – Email Classifier AI

## Visão Geral
Este frontend foi desenvolvido utilizando **HTML**, **CSS** e **JavaScript puro**, sem frameworks ou bibliotecas externas.  
O objetivo é permitir que o usuário insira ou envie o conteúdo de um email, envie esse conteúdo ao backend via requisição HTTP e visualize a classificação e resposta sugerida.  
Agora o frontend também possui **estado de carregamento** e **tratamento de erros mais amigável**, exibindo mensagens diretamente na interface.

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
  Inclui elementos para exibir **estado de carregamento** (“Processando…”) e **mensagens de erro**.

- **styles.css**  
  Estilização básica: layout centralizado, botões, campos de entrada e área de resultados.  
  Inclui estilos para o botão desabilitado e para a mensagem de carregamento.

- **script.js**  
  Captura o envio do formulário, trata entrada de texto ou arquivo `.txt`/`.pdf`, envia requisição `POST` para o backend (`/classify`) e exibe os dados retornados (`category`, `reply`).  
  Agora também controla o estado de carregamento e exibe erros diretamente no card de resultados.

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

---

## Fluxo de Uso

1. **Entrada de texto**  
   - Usuário digita diretamente no campo `textarea`.  
   - O texto é enviado ao backend via `fetch`.

2. **Upload de arquivo**  
   - `.txt`: conteúdo lido no frontend e enviado como texto.  
   - `.pdf`: texto não é extraído no frontend; uma mensagem placeholder é enviada ao backend.

3. **Resposta exibida**  
   - Categoria (badge colorida).  
   - Resposta sugerida (texto formatado).  
   - Em caso de erro, mensagem exibida no card de resultados.

4. **Estado de carregamento**  
   - Botão desabilitado durante requisição.  
   - Mensagem “Processando…” exibida abaixo do botão.

---

## Integração com Backend

- Requisição `POST` para:
  ```
  http://localhost:8000/classify
  ```

- Corpo da requisição:
  ```json
  {
    "text": "<conteúdo do email>"
  }
  ```

- Exemplo de chamada no `script.js`:
  ```javascript
  const res = await fetch("http://localhost:8000/classify", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: emailText })
  });
  const data = await res.json();
  ```

- Campos utilizados da resposta:
  - `data.category` (Produtivo ou Improdutivo)  
  - `data.reply` (resposta humanizada sugerida)

---

## Validações e Tratamento de Erros

- Se nenhum texto for inserido e nenhum arquivo for enviado, exibe alerta.  
- Se o arquivo não for `.txt` ou `.pdf`, exibe alerta de formato não suportado.  
- Se houver erro de conexão ou resposta inválida, a mensagem é exibida diretamente no card de resultados.  
- Estado de carregamento garante que o usuário saiba que a requisição está em andamento.

---

## Testes Manuais

### Casos de Entrada
- Texto direto: “Preciso saber o status da minha solicitação de suporte.”  
- Upload `.txt`: arquivo com conteúdo “Quero cancelar meu contrato.”  
- Upload `.pdf`: qualquer arquivo PDF (envia placeholder).  

### Resultado Esperado
- Categoria exibida corretamente (**Produtivo** ou **Improdutivo**).  
- Resposta sugerida coerente com a intenção.  
- Layout funcional e responsivo.  
- Botão desabilitado e mensagem “Processando…” durante requisição.  
- Mensagem de erro exibida no card em caso de falha.

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

---

## Notas de Manutenção
- O script depende da estrutura de resposta do backend (`category`, `reply`).  
- O campo `category` é utilizado para definir cor da borda (verde para **Produtivo**, vermelho para **Improdutivo**).  
- O botão de envio está vinculado ao evento `submit` do formulário `#email-form`.  
- O estado de carregamento é controlado via função `setLoading` no `script.js`.  

