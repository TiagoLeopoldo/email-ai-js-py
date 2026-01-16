const form = document.getElementById("email-form");
const textArea = document.getElementById("email-text");
const fileInput = document.getElementById("email-file");
const results = document.getElementById("results");
const categoryEl = document.getElementById("category");
const replyEl = document.getElementById("suggested-reply");

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
      alert("Formato não suportado. Use .txt ou .pdf");
      return;
    }
  }

  if (!emailText) {
    alert("Insira texto ou faça upload de um arquivo.");
    return;
  }

  try {
    const res = await fetch("https://email-ai-js-py.onrender.com/classify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: emailText }),
    });

    const data = await res.json();

    // Exibe os resultados vindos do backend
    categoryEl.textContent = data.category;
    categoryEl.style.borderColor =
      data.category === "Operacional" ? "#22c55e" : "#ef4444";
    replyEl.textContent = data.reply;
    results.classList.remove("hidden");
  } catch (error) {
    alert("Erro ao conectar com o backend: " + error);
  }
});
