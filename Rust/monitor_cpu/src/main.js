const { invoke } = window.__TAURI__.core;

let fileInputEl;
let fileMsgEl;
let stopMsgEl;

async function startMonitoring() {
  fileMsgEl.textContent = await invoke("monitor_cpu", {
    name: fileInputEl.value,
  });
}

async function stopMonitoring() {
  stopMsgEl.textContent = await invoke("stop_monitoring");
}

async function getFilePath() {
  const filePathMsg = await invoke("get_file_path", {
    name: fileInputEl.value,
  });
  fileMsgEl.textContent = `\n${filePathMsg}`;
}

window.addEventListener("DOMContentLoaded", () => {
  fileInputEl = document.querySelector("#file-input");
  fileMsgEl = document.querySelector("#file-msg");
  stopMsgEl = document.querySelector("#stop-msg");

  document.querySelector("#file-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    await startMonitoring();
  });

  document.querySelector("#stop-btn").addEventListener("click", async () => {
    await stopMonitoring();
  });
  document.querySelector("#file-btn").addEventListener("click", async () => {
    await getFilePath();
  });
});
