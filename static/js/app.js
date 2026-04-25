const videoForm = document.querySelector("#video-form");
const audioForm = document.querySelector("#audio-form");
const videoStatus = document.querySelector("#video-status");
const audioStatus = document.querySelector("#audio-status");
const videoInput = document.querySelector("#video-input");
const audioInput = document.querySelector("#audio-input");
const processStatus = document.querySelector("#process-status");
const processButton = document.querySelector("#process-button");
const downloadLink = document.querySelector("#download-link");
const generatedFile = document.querySelector("#generated-file");
const delayInput = document.querySelector("#delay-input");

function setStatus(element, message, type = "") {
  element.textContent = message;
  element.className = type ? `hint ${type}` : "hint";
}

function setProcessStatus(message, type = "") {
  processStatus.textContent = message;
  processStatus.className = type ? `status-box ${type}` : "status-box";
}

async function uploadFile(input, url, fieldName, statusElement) {
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

videoInput.addEventListener("change", () => {
  uploadFile(videoInput, "/api/upload/video", "video", videoStatus);
});

audioInput.addEventListener("change", () => {
  uploadFile(audioInput, "/api/upload/audio", "audio", audioStatus);
});

processButton.addEventListener("click", async () => {
  const delay = Number(delayInput.value || 0);

  if (!Number.isFinite(delay) || delay < 0) {
    setProcessStatus("El retraso del audio debe ser un numero mayor o igual a 0.", "error");
    return;
  }

  processButton.disabled = true;
  downloadLink.classList.add("hidden");
  generatedFile.classList.add("hidden");
  generatedFile.textContent = "";
  setProcessStatus("Procesando video...");

  try {
    const response = await fetch("/api/process", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ delay }),
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
