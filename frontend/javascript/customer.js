/**
 * SISTEMA CONTÁBIL - MÓDULO DE CADASTRO DE CLIENTES
 * Gerencia cadastro de empresas com upload de documentos
 */

const API_BASE_URL = 'https://send-project-xxv7.onrender.com';


// Elementos do DOM
const customerForm = document.getElementById('customer-form');
const uploadArea = document.getElementById('upload-area');
const fileUpload = document.getElementById('file-upload');
const fileList = document.getElementById('file-list');
const messageContainer = document.getElementById('message-container');

// Estado
let uploadedFiles = [];

// ==========================================
// VERIFICAÇÃO DE AUTENTICAÇÃO
// ==========================================

function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'index.html';
        return;
    }
    
    // Atualizar nome do usuário
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    if (user.name) {
        document.getElementById('user-name').textContent = user.name;
        document.querySelector('.avatar').textContent = user.name.charAt(0).toUpperCase();
    }
}

checkAuth();

// ==========================================
// MÁSCARAS DE INPUT
// ==========================================

function applyMasks() {
    // CNPJ da empresa
    const cnpjInput = document.getElementById('company-cnpj');
    cnpjInput.addEventListener('input', (e) => {
        let value = e.target.value.replace(/\D/g, '');
        value = value.replace(/(\d{2})(\d)/, '$1.$2');
        value = value.replace(/(\d{3})(\d)/, '$1.$2');
        value = value.replace(/(\d{3})(\d)/, '$1/$2');
        value = value.replace(/(\d{4})(\d{1,2})$/, '$1-$2');
        e.target.value = value;
    });

    // Telefone
    const phoneInput = document.getElementById('company-phone');
    phoneInput.addEventListener('input', (e) => {
        let value = e.target.value.replace(/\D/g, '');
        value = value.replace(/(\d{2})(\d)/, '($1) $2');
        value = value.replace(/(\d{5})(\d{4})$/, '$1-$2');
        e.target.value = value;
    });
}

applyMasks();

// ==========================================
// UPLOAD DE ARQUIVOS
// ==========================================

uploadArea.addEventListener('click', () => fileUpload.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    handleFiles(e.dataTransfer.files);
});

fileUpload.addEventListener('change', (e) => {
    handleFiles(e.target.files);
});

function handleFiles(files) {
    Array.from(files).forEach(file => {
        if (file.type !== 'application/pdf') {
            showMessage(`${file.name} não é um PDF válido`, 'error');
            return;
        }
        
        if (file.size > 10 * 1024 * 1024) {
            showMessage(`${file.name} excede 10MB`, 'error');
            return;
        }
        
        uploadedFiles.push(file);
        renderFileList();
    });
}

function renderFileList() {
    fileList.innerHTML = uploadedFiles.map((file, index) => `
        <div class="file-item">
            <div class="file-info">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M4 4a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" stroke="#059669" stroke-width="1.5"/>
                    <path d="M12 2v4a1 1 0 001 1h4" stroke="#059669" stroke-width="1.5"/>
                </svg>
                <div>
                    <div class="file-name">${file.name}</div>
                    <div class="file-size">${formatFileSize(file.size)}</div>
                </div>
            </div>
            <button type="button" class="file-remove" onclick="removeFile(${index})">
                <svg width="16" height="16" viewBox="0 0 20 20" fill="none">
                    <path d="M6 6l8 8m0-8l-8 8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
            </button>
        </div>
    `).join('');
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function removeFile(index) {
    uploadedFiles.splice(index, 1);
    renderFileList();
}

// ==========================================
// SUBMISSÃO DO FORMULÁRIO
// ==========================================

customerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const submitBtn = customerForm.querySelector('button[type="submit"]');
    const originalContent = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = `<div class="spinner"></div> Salvando...`;
    
    // Criar FormData para envio multipart (arquivos + dados)
    const formData = new FormData();
    formData.append('name', document.getElementById('company-name').value);
    formData.append('cnpj', document.getElementById('company-cnpj').value.replace(/\D/g, ''));
    formData.append('phone', document.getElementById('company-phone').value.replace(/\D/g, ''));
    formData.append('email', document.getElementById('company-email').value);
    
    // Adicionar arquivos
    uploadedFiles.forEach(file => {
        formData.append('documents', file);
    });
    
    try {
        const token = localStorage.getItem('token');
        
        const response = await fetch(`${API_BASE_URL}/customers`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage('Empresa cadastrada com sucesso!', 'success');
            resetForm();
            
            // Opcional: redirecionar para listagem
            setTimeout(() => {
                window.location.href = '/frontend/html/lista_customer.html';
            }, 1500);
        } else {
            showMessage(data.detail || 'Erro ao cadastrar empresa', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showMessage('Erro de conexão. Simulação ativada.', 'warning');
        
        // Simulação para desenvolvimento
        console.log('Dados enviados:', Object.fromEntries(formData));
        setTimeout(() => {
            showMessage('Empresa cadastrada (simulação)!', 'success');
            resetForm();
        }, 1000);
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalContent;
    }
});

function resetForm() {
    customerForm.reset();
    uploadedFiles = [];
    renderFileList();
}

// ==========================================
// UTILITÁRIOS
// ==========================================

function showMessage(message, type = 'success') {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${type}`;
    msgDiv.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            ${type === 'success' 
                ? '<path d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" fill="currentColor"/>'
                : type === 'error'
                ? '<path d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" fill="currentColor"/>'
                : '<path d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" fill="currentColor"/>'
            }
        </svg>
        <span>${message}</span>
    `;
    
    messageContainer.appendChild(msgDiv);
    
    setTimeout(() => {
        msgDiv.style.opacity = '0';
        msgDiv.style.transform = 'translateX(100%)';
        setTimeout(() => msgDiv.remove(), 300);
    }, 5000);
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'index.html';
}