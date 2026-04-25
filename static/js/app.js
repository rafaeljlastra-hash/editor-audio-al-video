const videoForm = document.querySelector("#video-form");
const audioForm = document.querySelector("#audio-form");
const videoStatus = document.querySelector("#video-status");
const audioStatus = document.querySelector("#audio-status");
const processStatus = document.querySelector("#process-status");
const processButton = document.querySelector("#process-button");
const downloadLink = document.querySelector("#download-link");
const generatedFile = document.querySelector("#generated-file");

function setStatus(element, message, type = "") {
  element.textContent = message;
  element.className = type ? `hint ${type}` : "hint";
}

function setProcessStatus(message, type = "") {
  processStatus.textContent = message;
  processStatus.className = type ? `status-box ${type}` : "status-box";
}

async function uploadFile(form, url, fieldName, statusElement) {
  const input = form.querySelector(`input[name="${fieldName}"]`);

  if (!input.files.length) {
    setStatus(statusElement, "Selecciona un archivo antes de subirlo.", "error");
    return;
  }

  const body = new FormData();
  body.append(fieldName, input.files[0]);

  setStatus(statusElement, "Subiendo...");
  downloadLink.classList.add("hidden");
  generatedFile.classList.add("hidden");
  generatedFile.textContent = "";

  try {
    const response = await fetch(url, {
      method: "POST",
      body,
    });
    const data = await response.json();

    if (!response.ok || !data.ok) {
      throw new Error(data.error || "No se pudo subir el archivo.");
    }

    setStatus(statusElement, `${data.message} (${data.filename})`, "success");
    setProcessStatus("Archivo recibido. Continua con el siguiente paso.");
  } catch (error) {
    setStatus(statusElement, error.message, "error");
    setProcessStatus(error.message, "error");
  }
}

videoForm.addEventListener("submit", (event) => {
  event.preventDefault();
  uploadFile(videoForm, "/api/upload/video", "video", videoStatus);
});

audioForm.addEventListener("submit", (event) => {
  event.preventDefault();
  uploadFile(audioForm, "/api/upload/audio", "audio", audioStatus);
});

processButton.addEventListener("click", async () => {
  processButton.disabled = true;
  downloadLink.classList.add("hidden");
  generatedFile.classList.add("hidden");
  generatedFile.textContent = "";
  setProcessStatus("Procesando video...");

  try {
    const response = await fetch("/api/process", {
      method: "POST",
    });
    const data = await response.json();

    if (!response.ok || !data.ok) {
      throw new Error(data.error || "No se pudo procesar el video.");
    }

    downloadLink.href = data.download_url;
    downloadLink.textContent = "Descargar video final";
    downloadLink.classList.remove("hidden");
    generatedFile.textContent = `Archivo generado: ${data.filename}`;
    generatedFile.classList.remove("hidden");
    setProcessStatus(data.message, "success");
  } catch (error) {
    setProcessStatus(error.message, "error");
  } finally {
    processButton.disabled = false;
  }
});
