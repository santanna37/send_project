/**
 * =====================================================
 * SISTEMA CONTÁBIL - PROCESSAMENTO EM LOTE DE PDFs
 * VERSÃO INTEGRADA COM O BACKEND
 * =====================================================
 */

// ALTERADO: URL base agora aponta para o seu servidor local ou produção
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
    // NOVO: Armazena o relatório final da API
    finalReport: {} 
};

const elements = {
    uploadZone: document.getElementById('upload-zone'),
    fileInput: document.getElementById('batch-upload'),
    queueList: document.getElementById('queue-list'),
    fileQueue: document.getElementById('file-queue'),
    queueCount: document.getElementById('queue-count'),
    btnProcess: document.getElementById('btn-process'),
    btnClear: document.getElementById('btn-clear'),
    processingList: document.getElementById('processing-list'),
    overallBar: document.getElementById('overall-bar'),
    overallPercent: document.getElementById('overall-percent'),
    statPending: document.getElementById('stat-pending'),
    statCompleted: document.getElementById('stat-completed'),
    statFailed: document.getElementById('stat-failed'),
    batchStatus: document.getElementById('batch-status'),
    activityLog: document.getElementById('activity-log'),
    batchSummary: document.getElementById('batch-summary'),
    targetClient: document.getElementById('target-client')
};

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    setupEventListeners();
    loadClients();
    logActivity('Sistema inicializado. Pronto para receber arquivos.');
});

function checkAuth() {
    const token = localStorage.getItem('token') || sessionStorage.getItem('token');
    if (!token) {
        window.location.href = '/index.html';
        return;
    }
    const user = JSON.parse(localStorage.getItem('user') || sessionStorage.getItem('user') || '{}');
    if (user.name) {
        document.getElementById('user-name').textContent = user.name;
        document.querySelector('.avatar').textContent = user.name.charAt(0).toUpperCase();
    }
}

function setupEventListeners() {
    elements.uploadZone.addEventListener('click', () => elements.fileInput.click());
    elements.uploadZone.addEventListener('dragover', handleDragOver);
    elements.uploadZone.addEventListener('dragleave', handleDragLeave);
    elements.uploadZone.addEventListener('drop', handleDrop);
    elements.fileInput.addEventListener('change', handleFileSelect);
    
    // ALTERADO: O botão de processar agora chama a nova função de lote
    elements.btnProcess.addEventListener('click', startBatchProcessing);
    elements.btnClear.addEventListener('click', clearQueue);
}

function handleDragOver(e) {
    e.preventDefault();
    elements.uploadZone.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    elements.uploadZone.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    elements.uploadZone.classList.remove('dragover');
    const files = Array.from(e.dataTransfer.files).filter(f => f.type === 'application/pdf');
    addFiles(files);
}

function handleFileSelect(e) {
    const files = Array.from(e.target.files);
    addFiles(files);
    e.target.value = ''; // Limpa o input para permitir selecionar o mesmo arquivo novamente
}

function addFiles(newFiles) {
    const validFiles = newFiles.filter(file => {
        if (file.type !== 'application/pdf') {
            showMessage(`${file.name} não é um PDF válido`, 'error');
            return false;
        }
        if (file.size > 50 * 1024 * 1024) {
            showMessage(`${file.name} excede o limite de 50MB`, 'error');
            return false;
        }
        if (state.files.some(f => f.name === file.name && f.size === file.size)) {
            return false; // Evita duplicados
        }
        return true;
    });

    state.files.push(...validFiles);
    updateQueue();
    updateUI();
    
    if (validFiles.length > 0) {
        logActivity(`${validFiles.length} arquivo(s) adicionado(s) à fila`, 'success');
    }
}

function removeFile(index) {
    if (state.processing) return;
    const removedFile = state.files.splice(index, 1);
    updateQueue();
    updateUI();
    logActivity(`Arquivo removido: ${removedFile[0].name}`);
}

function clearQueue() {
    if (state.processing) return;
    state.files = [];
    state.completed = [];
    state.failed = [];
    state.finalReport = {};
    updateQueue();
    updateUI();
    elements.fileQueue.style.display = 'none';
    elements.batchSummary.style.display = 'none';
    elements.processingList.innerHTML = '<div class="empty-state-proc"><p>Nenhum processamento iniciado</p></div>';
    updateStatus('waiting');
    logActivity('Fila e resultados limpos.');
}

function updateQueue() {
    if (state.files.length === 0) {
        elements.fileQueue.style.display = 'none';
        return;
    }
    
    elements.fileQueue.style.display = 'block';
    elements.queueCount.textContent = `${state.files.length} arquivo${state.files.length !== 1 ? 's' : ''}`;
    
    elements.queueList.innerHTML = state.files.map((file, index) => `
        <div class="queue-item-proc">
            <div class="queue-icon">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M4 4a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" stroke="currentColor" stroke-width="1.5"/></svg>
            </div>
            <div class="queue-info">
                <div class="queue-name">${file.name}</div>
                <div class="queue-meta">${formatFileSize(file.size)}</div>
            </div>
            <button class="queue-remove" onclick="removeFile(${index})" ${state.processing ? 'disabled' : ''}>&times;</button>
        </div>
    `).join('');
}

function updateUI() {
    const hasFiles = state.files.length > 0;
    // A seleção de cliente não é mais um bloqueio, pois o padrão é "auto"
    elements.btnProcess.disabled = !hasFiles || state.processing;
    elements.btnClear.disabled = !hasFiles || state.processing;
}

// ==================================================================
// NOVO: Função principal que envia TODOS os arquivos de uma vez
// ==================================================================
async function startBatchProcessing() {
    if (state.files.length === 0 || state.processing) return;

    state.processing = true;
    state.startTime = Date.now();
    state.completed = [];
    state.failed = [];
    state.finalReport = {};

    updateUI();
    updateStatus('processing');
    logActivity(`Iniciando processamento de ${state.files.length} arquivo(s)...`);
    renderProcessingList(); // Prepara a UI para mostrar o progresso

    const formData = new FormData();
    state.files.forEach(file => {
        // A chave 'files' (plural) deve corresponder ao nome do parâmetro no backend
        formData.append('files', file);
    });

    try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/email/multi_send`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
                // NÃO defina 'Content-Type', o browser faz isso automaticamente com o boundary correto para FormData
            },
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Erro da API (${response.status}): ${errorData.detail || response.statusText}`);
        }

        const result = await response.json();
        state.finalReport = result.response; // O objeto com o resultado de cada arquivo
        
        // Processa o relatório recebido da API
        processApiResponse(state.finalReport);

    } catch (error) {
        console.error("Falha catastrófica no envio do lote:", error);
        logActivity(`ERRO GERAL: ${error.message}`, 'error');
        // Marca todos os arquivos como falha em caso de erro de rede/API
        state.files.forEach((file, index) => {
            state.failed.push({ file, error: error.message });
            updateFileStatus(index, 'error', `Erro de conexão: ${error.message}`);
        });
    } finally {
        finishProcessing();
    }
}

// NOVO: Função para processar a resposta da API
function processApiResponse(report) {
    logActivity('API respondeu. Processando relatório...');
    state.files.forEach((file, index) => {
        const fileResult = report[file.name];

        if (fileResult) {
            if (fileResult.status === 'sucesso') {
                state.completed.push({ file, result: fileResult });
                updateFileStatus(index, 'completed', fileResult);
                logActivity(`✓ ${file.name} → ${fileResult.name}`, 'success');
            } else {
                state.failed.push({ file, error: fileResult.motivo });
                updateFileStatus(index, 'error', fileResult.motivo);
                logActivity(`✗ Falha em ${file.name}: ${fileResult.motivo}`, 'error');
            }
        } else {
            // Caso um arquivo enviado não retorne no relatório
            const errorMessage = 'Arquivo não processado pelo servidor.';
            state.failed.push({ file, error: errorMessage });
            updateFileStatus(index, 'error', errorMessage);
            logActivity(`? ${file.name}: ${errorMessage}`, 'warning');
        }
    });
}

function renderProcessingList() {
    elements.processingList.innerHTML = state.files.map((file, index) => `
        <div class="proc-item pending" id="proc-item-${index}">
            <div class="proc-icon">
                <div class="proc-spinner"></div>
            </div>
            <div class="proc-info">
                <div class="proc-name">${file.name}</div>
                <div class="proc-status"><span>Processando...</span></div>
            </div>
        </div>
    `).join('');
}

function updateFileStatus(index, status, data) {
    const item = document.getElementById(`proc-item-${index}`);
    if (!item) return;
    
    item.className = `proc-item ${status}`;
    const icon = item.querySelector('.proc-icon');
    const statusText = item.querySelector('.proc-status span');
    
    const icons = {
        processing: '<div class="proc-spinner"></div>',
        completed: '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M16.667 5L7.5 14.167 3.333 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
        error: '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M6 6l8 8m0-8l-8 8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
    };
    icon.innerHTML = icons[status];
    
    const messages = {
        processing: 'Processando...',
        completed: `✓ Enviado para ${data?.name || 'cliente'}`,
        error: `✗ ${data || 'Erro desconhecido'}`
    };
    statusText.textContent = messages[status];
}

function updateOverallProgress() {
    const total = state.files.length;
    const processed = state.completed.length + state.failed.length;
    const percent = total > 0 ? (processed / total) * 100 : 0;
    
    elements.overallBar.style.width = `${percent}%`;
    elements.overallPercent.textContent = `${Math.round(percent)}%`;
    
    elements.statPending.textContent = total - processed;
    elements.statProcessing.textContent = state.processing && processed < total ? 1 : 0;
    elements.statCompleted.textContent = state.completed.length;
    elements.statFailed.textContent = state.failed.length;
}

function updateStatus(status) {
    const dot = elements.batchStatus.querySelector('.status-dot-proc');
    const text = elements.batchStatus.querySelector('span:last-child');
    
    dot.className = `status-dot-proc ${status}`;
    const labels = {
        waiting: 'Aguardando arquivos',
        processing: 'Processando lote...',
        completed: 'Concluído',
        error: 'Concluído com falhas'
    };
    text.textContent = labels[status];
}

function finishProcessing() {
    state.processing = false;
    updateUI();
    updateOverallProgress();
    
    const hasErrors = state.failed.length > 0;
    updateStatus(hasErrors ? 'error' : 'completed');
    
    const duration = Math.round((Date.now() - state.startTime) / 1000);
    const mins = Math.floor(duration / 60).toString().padStart(2, '0');
    const secs = (duration % 60).toString().padStart(2, '0');
    
    elements.batchSummary.style.display = 'block';
    document.getElementById('summary-total').textContent = state.files.length;
    document.getElementById('summary-success').textContent = state.completed.length;
    document.getElementById('summary-failed').textContent = state.failed.length;
    document.getElementById('summary-time').textContent = `${mins}:${secs}`;
    
    logActivity(`Lote finalizado: ${state.completed.length} sucesso(s), ${state.failed.length} falha(s).`, hasErrors ? 'warning' : 'success');
    showMessage(`Processamento concluído!`, 'success');
    
    elements.batchSummary.scrollIntoView({ behavior: 'smooth' });
}

// ALTERADO: Corrigido para buscar na rota correta e tratar a resposta aninhada
async function loadClients() {
    try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/customer/`, { // Rota corrigida
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            const data = await response.json();
            const clients = data.list_customer; // Acessa a lista dentro do objeto
            if (clients && Array.isArray(clients)) {
                clients.forEach(client => {
                    const option = document.createElement('option');
                    option.value = client.id;
                    option.textContent = `${client.name} (${formatCNPJ(client.cnpj)})`;
                    elements.targetClient.appendChild(option);
                });
            }
        }
    } catch (error) {
        console.error('Erro ao carregar clientes:', error);
        logActivity('Não foi possível carregar a lista de clientes.', 'error');
    }
}

function downloadReport() {
    const blob = new Blob([JSON.stringify(state.finalReport, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `relatorio_envio_${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    logActivity('Relatório detalhado baixado.');
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatCNPJ(cnpj) {
    if (!cnpj) return '';
    const cleaned = String(cnpj).replace(/\D/g, '');
    if (cleaned.length !== 14) return cnpj;
    return cleaned.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
}

function logActivity(message, type = 'info') {
    const time = new Date().toLocaleTimeString('pt-BR');
    const entry = document.createElement('div');
    entry.className = `log-entry-proc ${type}`;
    entry.innerHTML = `<span class="log-time">${time}</span><span class="log-msg">${message}</span>`;
    elements.activityLog.insertBefore(entry, elements.activityLog.firstChild);
}

function showMessage(message, type = 'success') {
    const container = document.getElementById('message-container');
    if (!container) { alert(message); return; }
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${type}`;
    msgDiv.textContent = message;
    container.appendChild(msgDiv);
    setTimeout(() => msgDiv.remove(), 5000);
}

function logout() {
    localStorage.clear();
    sessionStorage.clear();
    window.location.href = '/index.html';
}