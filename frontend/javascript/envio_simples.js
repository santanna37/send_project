/**
 * =====================================================
 * SISTEMA CONTÁBIL - PROCESSAMENTO EM LOTE DE PDFs
 * VERSÃO INTEGRADA COM O BACKEND
 * =====================================================
 */

const API_BASE_URL =
window.location.hostname === "localhost" ||
window.location.hostname === "127.0.0.1"
? "http://localhost:8000"
: "https://send-project-xxv7.onrender.com";

const state = {
files: [],
processing: false,
completed: [],
failed: [],
startTime: null,
finalReport: {}
};

const elements = {
uploadZone: document.getElementById("upload-zone"),
fileInput: document.getElementById("batch-upload"),
queueList: document.getElementById("queue-list"),
fileQueue: document.getElementById("file-queue"),
queueCount: document.getElementById("queue-count"),
btnProcess: document.getElementById("btn-process"),
btnClear: document.getElementById("btn-clear"),
processingList: document.getElementById("processing-list"),
overallBar: document.getElementById("overall-bar"),
overallPercent: document.getElementById("overall-percent"),
statPending: document.getElementById("stat-pending"),
statProcessing: document.getElementById("stat-processing"), // ✅ CORREÇÃO: faltava
statCompleted: document.getElementById("stat-completed"),
statFailed: document.getElementById("stat-failed"),
batchStatus: document.getElementById("batch-status"),
activityLog: document.getElementById("activity-log"),
batchSummary: document.getElementById("batch-summary"),
targetClient: document.getElementById("target-client")
};

document.addEventListener("DOMContentLoaded", () => {
checkAuth();
setupEventListeners();
loadClients();
logActivity("Sistema inicializado. Pronto para receber arquivos.");
updateUI();
updateOverallProgress();
});

function checkAuth() {
const token = localStorage.getItem("token") || sessionStorage.getItem("token");
if (!token) {
window.location.href = "/index.html";
return;
}

const user = JSON.parse(
localStorage.getItem("user") ||
sessionStorage.getItem("user") ||
"{}"
);

if (user.name) {
const nameEl = document.getElementById("user-name");
const avatarEl = document.querySelector(".avatar");
if (nameEl) nameEl.textContent = user.name;
if (avatarEl) avatarEl.textContent = user.name.charAt(0).toUpperCase();
}
}

function setupEventListeners() {
if (!elements.uploadZone || !elements.fileInput) {
console.error("Elementos de upload não encontrados no DOM.");
return;
}

elements.uploadZone.addEventListener("click", () => elements.fileInput.click());
elements.uploadZone.addEventListener("dragover", handleDragOver);
elements.uploadZone.addEventListener("dragleave", handleDragLeave);
elements.uploadZone.addEventListener("drop", handleDrop);
elements.fileInput.addEventListener("change", handleFileSelect);

elements.btnProcess?.addEventListener("click", startBatchProcessing);
elements.btnClear?.addEventListener("click", clearQueue);
}

function handleDragOver(e) {
e.preventDefault();
elements.uploadZone.classList.add("dragover");
}

function handleDragLeave(e) {
e.preventDefault();
elements.uploadZone.classList.remove("dragover");
}

function handleDrop(e) {
e.preventDefault();
elements.uploadZone.classList.remove("dragover");
const files = Array.from(e.dataTransfer.files).filter((f) => f.type === "application/pdf");
addFiles(files);
}

function handleFileSelect(e) {
const files = Array.from(e.target.files);
addFiles(files);
e.target.value = ""; // permite selecionar o mesmo arquivo novamente
}

function addFiles(newFiles) {
const validFiles = newFiles.filter((file) => {
if (file.type !== "application/pdf") {
    showMessage(`${file.name} não é um PDF válido`, "error");
    return false;
}
if (file.size > 50 * 1024 * 1024) {
    showMessage(`${file.name} excede o limite de 50MB`, "error");
    return false;
}
if (state.files.some((f) => f.name === file.name && f.size === file.size)) {
    return false;
}
return true;
});

if (validFiles.length === 0) return;

state.files.push(...validFiles);
updateQueue();
updateUI();
updateOverallProgress();
logActivity(`${validFiles.length} arquivo(s) adicionado(s) à fila`, "success");
}

function removeFile(index) {
if (state.processing) return;
const removed = state.files.splice(index, 1);
updateQueue();
updateUI();
updateOverallProgress();
if (removed[0]) logActivity(`Arquivo removido: ${removed[0].name}`);
}

function clearQueue() {
if (state.processing) return;

state.files = [];
state.completed = [];
state.failed = [];
state.finalReport = {};
state.startTime = null;

updateQueue();
updateUI();
updateOverallProgress();

if (elements.fileQueue) elements.fileQueue.style.display = "none";
if (elements.batchSummary) elements.batchSummary.style.display = "none";
if (elements.processingList) {
elements.processingList.innerHTML =
    '<div class="empty-state-proc"><p>Nenhum processamento iniciado</p></div>';
}

updateStatus("waiting");
logActivity("Fila e resultados limpos.");
}

function updateQueue() {
if (!elements.fileQueue || !elements.queueCount || !elements.queueList) return;

if (state.files.length === 0) {
elements.fileQueue.style.display = "none";
elements.queueList.innerHTML = "";
elements.queueCount.textContent = "0 arquivos";
return;
}

elements.fileQueue.style.display = "block";
elements.queueCount.textContent = `${state.files.length} arquivo${state.files.length !== 1 ? "s" : ""}`;

elements.queueList.innerHTML = state.files
.map(
    (file, index) => `
    <div class="queue-item-proc">
    <div class="queue-icon">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path d="M4 4a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" stroke="currentColor" stroke-width="1.5"/>
        </svg>
    </div>
    <div class="queue-info">
        <div class="queue-name">${file.name}</div>
        <div class="queue-meta">${formatFileSize(file.size)}</div>
    </div>
    <button class="queue-remove" onclick="removeFile(${index})" ${state.processing ? "disabled" : ""}>&times;</button>
    </div>
`
)
.join("");
}

function updateUI() {
const hasFiles = state.files.length > 0;

if (elements.btnProcess) elements.btnProcess.disabled = !hasFiles || state.processing;
if (elements.btnClear) elements.btnClear.disabled = !hasFiles || state.processing;
}

async function startBatchProcessing() {
if (state.files.length === 0 || state.processing) return;

state.processing = true;
state.startTime = Date.now();
state.completed = [];
state.failed = [];
state.finalReport = {};

updateUI();
updateStatus("processing");
updateOverallProgress();
logActivity(`Iniciando processamento de ${state.files.length} arquivo(s)...`);
renderProcessingList();

const formData = new FormData();
state.files.forEach((file) => formData.append("files", file)); // ✅ backend espera "files"

try {
const token = localStorage.getItem("token") || sessionStorage.getItem("token");

const response = await fetch(`${API_BASE_URL}/email/multi_send`, {
    method: "POST",
    headers: {
    Authorization: `Bearer ${token}`
    },
    body: formData
});

const raw = await response.text();
let payload = {};
try {
    payload = raw ? JSON.parse(raw) : {};
} catch {
    payload = { raw };
}

if (!response.ok) {
    const msg =
    payload?.response_error ||
    payload?.detail ||
    payload?.raw ||
    `Erro ${response.status}`;
    throw new Error(msg);
}

// esperado: { response: { "arquivo.pdf": {...}, ... } }
state.finalReport = payload.response || {};
processApiResponse(state.finalReport);
} catch (error) {
console.error("Falha geral no envio do lote:", error);
logActivity(`ERRO GERAL: ${error.message}`, "error");

state.files.forEach((file, index) => {
    state.failed.push({ file, error: error.message });
    updateFileStatus(index, "error", `Erro de conexão: ${error.message}`);
});
} finally {
finishProcessing();
}
}

function processApiResponse(report) {
logActivity("API respondeu. Processando relatório...");

state.files.forEach((file, index) => {
const fileResult = report[file.name];

if (!fileResult) {
    const errorMessage = "Arquivo não processado pelo servidor.";
    state.failed.push({ file, error: errorMessage });
    updateFileStatus(index, "error", errorMessage);
    logActivity(`? ${file.name}: ${errorMessage}`, "warning");
    return;
}

if (fileResult.status === "sucesso") {
    state.completed.push({ file, result: fileResult });
    updateFileStatus(index, "completed", fileResult);
    logActivity(`✓ ${file.name} → ${fileResult.email || fileResult.name || "OK"}`, "success");
} else {
    const reason = fileResult.motivo || fileResult.detalhe || "Falha no envio";
    state.failed.push({ file, error: reason });
    updateFileStatus(index, "error", reason);
    logActivity(`✗ Falha em ${file.name}: ${reason}`, "error");
}
});
}

function renderProcessingList() {
if (!elements.processingList) return;

elements.processingList.innerHTML = state.files
.map(
    (file, index) => `
    <div class="proc-item pending" id="proc-item-${index}">
    <div class="proc-icon">
        <div class="proc-spinner"></div>
    </div>
    <div class="proc-info">
        <div class="proc-name">${file.name}</div>
        <div class="proc-status"><span>Processando...</span></div>
    </div>
    </div>
`
)
.join("");
}

function updateFileStatus(index, status, data) {
const item = document.getElementById(`proc-item-${index}`);
if (!item) return;

item.className = `proc-item ${status}`;

const icon = item.querySelector(".proc-icon");
const statusText = item.querySelector(".proc-status span");

const icons = {
processing: '<div class="proc-spinner"></div>',
completed:
    '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M16.667 5L7.5 14.167 3.333 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
error:
    '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M6 6l8 8m0-8l-8 8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
};

if (icon) icon.innerHTML = icons[status] || icons.processing;

const messages = {
processing: "Processando...",
completed: `✓ Enviado para ${data?.name || data?.email || "cliente"}`,
error: `✗ ${typeof data === "string" ? data : "Erro desconhecido"}`
};

if (statusText) statusText.textContent = messages[status] || "Atualizando...";
}

function updateOverallProgress() {
// ✅ se algum elemento estiver null, evita crash
if (
!elements.overallBar ||
!elements.overallPercent ||
!elements.statPending ||
!elements.statProcessing ||
!elements.statCompleted ||
!elements.statFailed
) {
console.error("Elementos de progresso não encontrados.", elements);
return;
}

const total = state.files.length;
const processed = state.completed.length + state.failed.length;
const percent = total > 0 ? (processed / total) * 100 : 0;

elements.overallBar.style.width = `${percent}%`;
elements.overallPercent.textContent = `${Math.round(percent)}%`;

elements.statPending.textContent = String(Math.max(0, total - processed));
elements.statProcessing.textContent = String(state.processing && processed < total ? 1 : 0);
elements.statCompleted.textContent = String(state.completed.length);
elements.statFailed.textContent = String(state.failed.length);
}

function updateStatus(status) {
if (!elements.batchStatus) return;

const dot = elements.batchStatus.querySelector(".status-dot-proc");
const text = elements.batchStatus.querySelector("span:last-child");

if (!dot || !text) return;

dot.className = `status-dot-proc ${status}`;

const labels = {
waiting: "Aguardando arquivos",
processing: "Processando lote...",
completed: "Concluído",
error: "Concluído com falhas"
};

text.textContent = labels[status] || "Status";
}

function finishProcessing() {
state.processing = false;
updateUI();
updateOverallProgress();

const hasErrors = state.failed.length > 0;
updateStatus(hasErrors ? "error" : "completed");

const duration = state.startTime ? Math.round((Date.now() - state.startTime) / 1000) : 0;
const mins = Math.floor(duration / 60).toString().padStart(2, "0");
const secs = (duration % 60).toString().padStart(2, "0");

if (elements.batchSummary) elements.batchSummary.style.display = "block";

const totalEl = document.getElementById("summary-total");
const successEl = document.getElementById("summary-success");
const failedEl = document.getElementById("summary-failed");
const timeEl = document.getElementById("summary-time");

if (totalEl) totalEl.textContent = String(state.files.length);
if (successEl) successEl.textContent = String(state.completed.length);
if (failedEl) failedEl.textContent = String(state.failed.length);
if (timeEl) timeEl.textContent = `${mins}:${secs}`;

logActivity(
`Lote finalizado: ${state.completed.length} sucesso(s), ${state.failed.length} falha(s).`,
hasErrors ? "warning" : "success"
);

showMessage("Processamento concluído!", "success");

elements.batchSummary?.scrollIntoView({ behavior: "smooth" });
}

async function loadClients() {
try {
const token = localStorage.getItem("token") || sessionStorage.getItem("token");
const response = await fetch(`${API_BASE_URL}/customer/`, {
    headers: { Authorization: `Bearer ${token}` }
});

if (!response.ok) return;

const data = await response.json();
const clients = data.list_customer;

if (clients && Array.isArray(clients) && elements.targetClient) {
    clients.forEach((client) => {
    const option = document.createElement("option");
    option.value = client.id;
    option.textContent = `${client.name} (${formatCNPJ(client.cnpj)})`;
    elements.targetClient.appendChild(option);
    });
}
} catch (error) {
console.error("Erro ao carregar clientes:", error);
logActivity("Não foi possível carregar a lista de clientes.", "error");
}
}

function downloadReport() {
const blob = new Blob([JSON.stringify(state.finalReport, null, 2)], { type: "application/json" });
const url = URL.createObjectURL(blob);
const a = document.createElement("a");
a.href = url;
a.download = `relatorio_envio_${new Date().toISOString().split("T")[0]}.json`;
document.body.appendChild(a);
a.click();
document.body.removeChild(a);
URL.revokeObjectURL(url);

logActivity("Relatório detalhado baixado.");
}

function formatFileSize(bytes) {
if (bytes === 0) return "0 Bytes";
const k = 1024;
const sizes = ["Bytes", "KB", "MB", "GB"];
const i = Math.floor(Math.log(bytes) / Math.log(k));
return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}

function formatCNPJ(cnpj) {
if (!cnpj) return "";
const cleaned = String(cnpj).replace(/\D/g, "");
if (cleaned.length !== 14) return String(cnpj);
return cleaned.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, "$1.$2.$3/$4-$5");
}

function logActivity(message, type = "info") {
if (!elements.activityLog) return;

const time = new Date().toLocaleTimeString("pt-BR");
const entry = document.createElement("div");
entry.className = `log-entry-proc ${type}`;
entry.innerHTML = `<span class="log-time">${time}</span><span class="log-msg">${message}</span>`;
elements.activityLog.insertBefore(entry, elements.activityLog.firstChild);
}

function showMessage(message, type = "success") {
const container = document.getElementById("message-container");
if (!container) {
alert(message);
return;
}

const msgDiv = document.createElement("div");
msgDiv.className = `message ${type}`;
msgDiv.textContent = message;
container.appendChild(msgDiv);

setTimeout(() => msgDiv.remove(), 5000);
}

function logout() {
localStorage.clear();
sessionStorage.clear();
window.location.href = "/index.html";
}

// ===================================================
// Exporta funções que são chamadas via onclick inline
// ===================================================
window.removeFile = removeFile;
window.downloadReport = downloadReport;
window.logout = logout;