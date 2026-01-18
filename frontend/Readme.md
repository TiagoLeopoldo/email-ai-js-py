# Frontend – Email Classifier AI

## Índice
- [Visão Geral](#visão-geral)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Dependências](#dependências)
- [Execução](#execução)
- [Fluxo de Uso](#fluxo-de-uso)
- [Integração com Backend](#integração-com-backend)
- [Estados de Carregamento e Erros](#estados-de-carregamento-e-erros)
- [Testes Manuais](#testes-manuais)
- [Limitações Conhecidas](#limitações-conhecidas)
- [Melhorias Futuras](#melhorias-futuras)

---

## Visão Geral
O frontend é uma **interface web simples e intuitiva** desenvolvida em **HTML, CSS e JavaScript**.  
Ele permite que o usuário insira texto de emails ou faça upload de arquivos `.txt` ou `.pdf`, envia os dados para o backend e exibe:

- A **categoria** atribuída ao email (**Produtivo**, **Improdutivo** ou **Irrelevante**).  
- A **resposta automática sugerida** pelo sistema.  

O sistema está integrado à **OpenAI API**, o que significa que não depende de frases fixas: qualquer mensagem enviada é analisada pela IA, que interpreta o conteúdo e gera uma resposta natural e contextualizada.

---

## Estrutura do Projeto

```
frontend/
├── index.html      # Página principal
├── styles.css      # Estilos da interface
├── script.js       # Lógica de interação e integração com backend
└── README.md       # Este documento
```

---

## Dependências
O frontend não depende de frameworks externos.  
Para servir localmente, pode-se usar o servidor embutido do Python:

```bash
cd frontend
python -m http.server 3000
```

---

## Execução
1. Certifique-se de que o **backend** está rodando em `http://localhost:8000`.  
2. Sirva o frontend em `http://localhost:3000`.  
3. Abra o navegador e acesse `http://localhost:3000`.  

---

## Fluxo de Uso
1. Digite o texto do email no campo de texto ou faça upload de um arquivo `.txt` ou `.pdf`.  
2. Clique em **Classificar e sugerir resposta**.  
3. O frontend envia requisição `POST` para o backend:  
   - Texto ou `.txt` → `/classify`  
   - `.pdf` → `/classify-pdf`  
4. O backend retorna a classificação e resposta sugerida.  
5. O resultado é exibido na seção **Resultado**.  
6. Após envio, os campos de texto e upload são **limpos automaticamente**.  

---

## Integração com Backend
- O frontend consome os endpoints do backend hospedado em Render:  
  - `https://email-ai-js-py.onrender.com/classify`  
  - `https://email-ai-js-py.onrender.com/classify-pdf`  
- Em ambiente local, basta alterar a constante `API_BASE` no `script.js` para `http://localhost:8000`.

---

## Estados de Carregamento e Erros
- Durante o processamento, o botão é desabilitado e aparece a mensagem **“Processando…”**.  
- Em caso de erro (texto inválido, arquivo não suportado, falha de conexão), o frontend exibe mensagem clara na seção de resultados.  
- Campos são limpos após envio bem-sucedido.  

---

## Testes Manuais
O sistema não depende de frases pré-definidas.  
O usuário pode enviar **qualquer mensagem de email** e o backend, integrado à **OpenAI API**, irá analisar o conteúdo e decidir a categoria mais adequada:

- **Produtivo:** mensagens que exigem ação ou resposta (ex.: solicitações de status, dúvidas sobre contratos, pedidos de suporte).  
- **Improdutivo:** mensagens que não exigem ação imediata (ex.: felicitações, agradecimentos).  
- **Irrelevante:** mensagens fora do escopo da empresa (ex.: brincadeiras, assuntos não relacionados).  

A IA gera também uma **resposta automática personalizada**, adaptada ao contexto da mensagem.  
Isso significa que não é um simples sistema de regras booleanas: mesmo que o usuário escreva frases diferentes ou complexas, o modelo de IA consegue interpretar e responder de forma natural.

#### Exemplos de teste
- "Preciso saber o status do pedido" → Categoria: Produtivo → Resposta: confirma que a solicitação está sendo cuidada.  
- "Quero cancelar meu contrato" → Categoria: Produtivo → Resposta: informa que o cancelamento será tratado.  
- "Feliz Natal para toda a equipe" → Categoria: Improdutivo → Resposta: agradece cordialmente.  
- "Mensagem de agradecimento sem solicitação" → Categoria: Improdutivo → Resposta: agradece de forma simpática.  

Esses exemplos são apenas ilustrativos.  
Na prática, o sistema aceita **qualquer frase** e a IA decide a categoria e resposta de acordo com o conteúdo.

---
