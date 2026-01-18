// Constantes
const API_BASE = "https://email-ai-js-py.onrender.com";
const MAX_CHARS = 2000;

// Elementos da interface
const form = document.getElementById("email-form");
const textArea = document.getElementById("email-text");
const fileInput = document.getElementById("email-file");
const results = document.getElementById("results");
const categoryEl = document.getElementById("category");
const replyEl = document.getElementById("suggested-reply");
const errorRow = document.getElementById("error-row");
const errorText = document.getElementById("error-text");
const loadingEl = document.getElementById("loading");
const submitBtn = document.getElementById("submit-btn");

// -------------------- Funções auxiliares --------------------

function setLoading(isLoading) {
  submitBtn.disabled = isLoading;
  loadingEl.classList.toggle("hidden", !isLoading);
}

function showError(message) {
  errorText.textContent = message;
  errorRow.classList.remove("hidden");
  results.classList.remove("hidden");
}

function clearResults() {
  errorRow.classList.add("hidden");
  errorText.textContent = "—";
  results.classList.add("hidden");
  categoryEl.textContent = "—";
  categoryEl.classList.remove("category-productive", "category-unproductive");
  replyEl.textContent = "—";
}

function applyCategoryStyle(category) {
  categoryEl.classList.remove("category-productive", "category-unproductive");
  if (category === "Produtivo") {
    categoryEl.classList.add("category-productive");
  } else {
    categoryEl.classList.add("category-unproductive");
  }
}

// -------------------- Evento principal --------------------

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const file = fileInput.files[0];
  let emailText = textArea.value.trim();

  clearResults();

  if (!emailText && !file) {
    showError("Nenhum texto ou arquivo válido foi fornecido.");
    return;
  }

  setLoading(true);

  try {
    let res;

    if (file) {
      const ext = file.name.toLowerCase().split(".").pop();

      if (ext === "txt") {
        emailText = await file.text();

        if (emailText.length > MAX_CHARS) {
          showError(`O texto excede o limite de ${MAX_CHARS} caracteres.`);
          return;
        }

        res = await fetch(`${API_BASE}/classify`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: emailText }),
        });
      } else if (ext === "pdf") {
        const formData = new FormData();
        formData.append("file", file);

        res = await fetch(`${API_BASE}/classify-pdf`, {
          method: "POST",
          body: formData,
        });
      } else {
        showError("Formato de arquivo não suportado. Use apenas .txt ou .pdf.");
        return;
      }
    } else {
      if (emailText.length > MAX_CHARS) {
        showError(`O texto excede o limite de ${MAX_CHARS} caracteres.`);
        return;
      }

      res = await fetch(`${API_BASE}/classify`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: emailText }),
      });
    }

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      const msg = err?.detail || "Erro interno ao processar sua solicitação.";
      showError(msg);
      return;
    }

    const data = await res.json();

    categoryEl.textContent = data.category;
    applyCategoryStyle(data.category);

    replyEl.textContent = data.reply;
    results.classList.remove("hidden");

    // Correção: limpar campos após envio
    textArea.value = "";
    fileInput.value = "";
  } catch (error) {
    showError("Não foi possível conectar ao servidor. Verifique sua conexão.");
  } finally {
    setLoading(false);
  }
});
