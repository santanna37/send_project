/**
 * SISTEMA CONTÁBIL - PROCESSAMENTO EM LOTE DE PDFs
 */

const API_BASE_URL = 'http://localhost:8000';

const state = {
    files: [],
    processing: false,
    completed: [],
    failed: [],
    startTime: null
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
    statProcessing: document.getElementById('stat-processing'),
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
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'index.html';
        return;
    }
    const user = JSON.parse(localStorage.getItem('user') || '{}');
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
    
    elements.targetClient.addEventListener('change', updateUI);
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
            return false;
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
    state.files.splice(index, 1);
    updateQueue();
    updateUI();
    logActivity('Arquivo removido da fila');
}

function clearQueue() {
    if (state.processing) return;
    state.files = [];
    updateQueue();
    updateUI();
    elements.fileQueue.style.display = 'none';
    logActivity('Fila limpa');
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
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M4 4a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" stroke="currentColor" stroke-width="1.5"/>
                    <path d="M12 2v4a1 1 0 001 1h4" stroke="currentColor" stroke-width="1.5"/>
                </svg>
            </div>
            <div class="queue-info">
                <div class="queue-name">${file.name}</div>
                <div class="queue-meta">${formatFileSize(file.size)}</div>
            </div>
            <button class="queue-remove" onclick="removeFile(${index})" ${state.processing ? 'disabled' : ''}>
                <svg width="16" height="16" viewBox="0 0 20 20" fill="none">
                    <path d="M6 6l8 8m0-8l-8 8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
            </button>
        </div>
    `).join('');
}

function updateUI() {
    const hasFiles = state.files.length > 0;
    const clientSelected = elements.targetClient.value !== '';
    
    elements.btnProcess.disabled = !hasFiles || !clientSelected || state.processing;
    elements.btnClear.disabled = !hasFiles || state.processing;
}

async function startProcessing() {
    if (state.files.length === 0) return;
    
    state.processing = true;
    state.startTime = Date.now();
    state.completed = [];
    state.failed = [];
    
    updateUI();
    updateStatus('processing');
    logActivity('Iniciando processamento do lote...');
    
    renderProcessingList();
    
    for (let i = 0; i < state.files.length; i++) {
        await processFile(i);
    }
    
    finishProcessing();
}

async function processFile(index) {
    const file = state.files[index];
    updateFileStatus(index, 'processing');
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('client_id', elements.targetClient.value);
        formData.append('doc_type', document.getElementById('doc-type').value);
        formData.append('notify', document.getElementById('notify-client').checked);
        
        await simulateProgress(index);
        
        // Simulação de resposta bem-sucedida
        const result = {
            success: true,
            extracted_data: { cnpj: '12.345.678/0001-90', valor: 'R$ 1.234,56' },
            client_matched: 'Tech Solutions Ltda'
        };
        
        state.completed.push({ file, result });
        updateFileStatus(index, 'completed', result);
        logActivity(`✓ ${file.name} → ${result.client_matched}`, 'success');
        
    } catch (error) {
        state.failed.push({ file, error: error.message });
        updateFileStatus(index, 'error', error.message);
        logActivity(`✗ Falha em ${file.name}: ${error.message}`, 'error');
    }
    
    updateOverallProgress();
}

function simulateProgress(index) {
    return new Promise((resolve) => {
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress >= 100) {
                progress = 100;
                clearInterval(interval);
                updateFileProgress(index, 100);
                setTimeout(resolve, 300);
            } else {
                updateFileProgress(index, progress);
            }
        }, 300);
    });
}

function renderProcessingList() {
    elements.processingList.innerHTML = state.files.map((file, index) => `
        <div class="proc-item pending" id="proc-item-${index}">
            <div class="proc-icon">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="2"/>
                </svg>
            </div>
            <div class="proc-info">
                <div class="proc-name">${file.name}</div>
                <div class="proc-status">
                    <span>Aguardando...</span>
                </div>
            </div>
            <div class="proc-progress">
                <div class="mini-progress-bg">
                    <div class="mini-progress-fill" id="prog-bar-${index}" style="width: 0%"></div>
                </div>
                <span class="mini-progress-text" id="prog-text-${index}">0%</span>
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
    
    icon.innerHTML = icons[status] || icons.processing;
    
    const messages = {
        processing: 'Processando...',
        completed: `✓ Enviado para ${data?.client_matched || 'cliente'}`,
        error: `✗ ${data || 'Erro no processamento'}`
    };
    
    statusText.textContent = messages[status];
}

function updateFileProgress(index, percent) {
    const bar = document.getElementById(`prog-bar-${index}`);
    const text = document.getElementById(`prog-text-${index}`);
    if (bar && text) {
        bar.style.width = `${Math.min(percent, 100)}%`;
        text.textContent = `${Math.round(Math.min(percent, 100))}%`;
    }
}

function updateOverallProgress() {
    const total = state.files.length;
    const completed = state.completed.length;
    const failed = state.failed.length;
    const processing = state.processing && completed + failed < total ? 1 : 0;
    const pending = total - completed - failed - processing;
    
    const percent = total > 0 ? ((completed + failed) / total) * 100 : 0;
    
    elements.overallBar.style.width = `${percent}%`;
    elements.overallPercent.textContent = `${Math.round(percent)}%`;
    
    elements.statPending.textContent = pending;
    elements.statProcessing.textContent = processing;
    elements.statCompleted.textContent = completed;
    elements.statFailed.textContent = failed;
}

function updateStatus(status) {
    const dot = elements.batchStatus.querySelector('.status-dot-proc');
    const text = elements.batchStatus.querySelector('span:last-child');
    
    dot.className = `status-dot-proc ${status}`;
    const labels = {
        waiting: 'Aguardando arquivos',
        processing: 'Processando lote...',
        completed: 'Concluído',
        error: 'Erro no processamento'
    };
    text.textContent = labels[status];
}

function finishProcessing() {
    state.processing = false;
    updateUI();
    
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
    
    logActivity(`Lote finalizado: ${state.completed.length} sucesso(s), ${state.failed.length} falha(s)`, hasErrors ? 'warning' : 'success');
    showMessage(`Processamento concluído! ${state.completed.length} arquivo(s) enviado(s).`, 'success');
    
    // Rolar para o resumo
    elements.batchSummary.scrollIntoView({ behavior: 'smooth' });
}

async function loadClients() {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/customers`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            const clients = await response.json();
            clients.forEach(client => {
                const option = document.createElement('option');
                option.value = client.id;
                option.textContent = `${client.name} (${formatCNPJ(client.cnpj)})`;
                elements.targetClient.appendChild(option);
            });
        }
    } catch (error) {
        console.log('Modo de demonstração - clientes não carregados');
    }
}

function downloadReport() {
    const report = {
        data: new Date().toISOString(),
        total: state.files.length,
        sucessos: state.completed,
        falhas: state.failed,
        tempo: document.getElementById('summary-time').textContent
    };
    
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `relatorio-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
    
    logActivity('Relatório baixado');
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
    const cleaned = cnpj.replace(/\D/g, '');
    return cleaned.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
}

function logActivity(message, type = 'info') {
    const time = new Date().toLocaleTimeString('pt-BR');
    const entry = document.createElement('div');
    entry.className = `log-entry-proc ${type}`;
    entry.innerHTML = `
        <span class="log-time">${time}</span>
        <span class="log-msg">${message}</span>
    `;
    
    elements.activityLog.insertBefore(entry, elements.activityLog.firstChild);
    
    while (elements.activityLog.children.length > 50) {
        elements.activityLog.removeChild(elements.activityLog.lastChild);
    }
}

function showMessage(message, type = 'success') {
    const container = document.getElementById('message-container');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${type}`;
    msgDiv.style.cssText = 'padding: 1rem 1.25rem; border-radius: 8px; margin-bottom: 0.5rem; animation: slideInRight 0.3s ease;';
    msgDiv.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none" style="margin-right: 0.5rem;">
            ${type === 'success' 
                ? '<path d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" fill="currentColor"/>'
                : '<path d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" fill="currentColor"/>'
            }
        </svg>
        <span>${message}</span>
    `;
    
    container.appendChild(msgDiv);
    
    setTimeout(() => {
        msgDiv.style.opacity = '0';
        setTimeout(() => msgDiv.remove(), 300);
    }, 5000);
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'index.html';
}