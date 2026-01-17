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

const MAX_CHARS = 2000;

function setLoading(isLoading) {
  if (isLoading) {
    submitBtn.disabled = true;
    loadingEl.classList.remove("hidden");
  } else {
    submitBtn.disabled = false;
    loadingEl.classList.add("hidden");
  }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  let emailText = textArea.value.trim();

  if (!emailText && fileInput.files.length > 0) {
    const file = fileInput.files[0];
    const ext = file.name.toLowerCase().split(".").pop();
    if (ext === "txt") {
      emailText = await file.text();
    } else if (ext === "pdf") {
      emailText = "[PDF enviado — o texto será extraído no backend]";
    } else {
      showError("Formato de arquivo não suportado. Use apenas .txt ou .pdf.");
      return;
    }
  }

  if (!emailText) {
    showError("Nenhum texto ou arquivo válido foi fornecido.");
    return;
  }

  if (emailText.length > MAX_CHARS) {
    showError(`O texto excede o limite de ${MAX_CHARS} caracteres. Reduza o conteúdo e tente novamente.`);
    return;
  }

  clearResults();
  setLoading(true);

  try {
    const res = await fetch("https://email-ai-js-py.onrender.com/classify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: emailText }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      const msg = err?.detail || "Erro interno ao processar sua solicitação. Tente novamente mais tarde.";
      showError(msg);
      return;
    }

    const data = await res.json();
    categoryEl.textContent = data.category;
    categoryEl.classList.remove("category-productive", "category-unproductive");

    if (data.category === "Produtivo") {
      categoryEl.classList.add("category-productive");
    } else {
      categoryEl.classList.add("category-unproductive");
    }

    replyEl.textContent = data.reply;
    results.classList.remove("hidden");
  } catch (error) {
    showError("Não foi possível conectar ao servidor. Verifique sua conexão e tente novamente.");
  } finally {
    setLoading(false);
  }
});

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
