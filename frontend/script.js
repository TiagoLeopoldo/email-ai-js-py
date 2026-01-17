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
      // Mantém comportamento atual (placeholder) até implementarmos parsing no backend
      emailText = "[PDF enviado — o texto será extraído no backend]";
    } else {
      alert("Formato não suportado. Use .txt ou .pdf");
      return;
    }
  }

  if (!emailText) {
    alert("Insira texto ou faça upload de um arquivo.");
    return;
  }

  // Limpa estado anterior
  errorRow.classList.add("hidden");
  errorText.textContent = "—";
  results.classList.add("hidden");
  categoryEl.textContent = "—";
  replyEl.textContent = "—";

  setLoading(true);

  try {
    const res = await fetch("https://email-ai-js-py.onrender.com/classify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: emailText }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      const msg = err?.detail || `Erro ${res.status}`;
      errorText.textContent = msg;
      errorRow.classList.remove("hidden");
      results.classList.remove("hidden");
      return;
    }

    const data = await res.json();

    categoryEl.textContent = data.category;
    categoryEl.style.borderColor =
      data.category === "Produtivo" ? "#22c55e" : "#ef4444";
    replyEl.textContent = data.reply;
    results.classList.remove("hidden");
  } catch (error) {
    errorText.textContent = "Erro ao conectar com o backend: " + error;
    errorRow.classList.remove("hidden");
    results.classList.remove("hidden");
  } finally {
    setLoading(false);
  }
});
