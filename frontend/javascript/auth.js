/**
 * SISTEMA CONTÁBIL - MÓDULO DE AUTENTICAÇÃO COMPLETO
 * Localização: ./javascript/auth.js
 */

const API_BASE_URL = 'https://send-project-xxv7.onrender.com';

// Estado global para evitar cliques duplos
let isSubmitting = false;

// ==========================================
// INICIALIZAÇÃO
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    // 1. Verifica sessão antes de qualquer coisa
    checkExistingSession();
    
    // 2. Configura eventos de clique e abas
    setupEventListeners();
    
    // 3. Aplica máscaras nos campos de registro
    applyInputMasks();
});

/**
 * CORREÇÃO DO LOOP INFINITO:
 * Baseia a lógica na existência dos elementos do DOM.
 */
function checkExistingSession() {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    const isLoggedIn = (token !== null && user !== null);

    // Verifica se estamos na página de LOGIN (pela existência do form de login)
    const isLoginPage = document.getElementById('login-form') !== null;

    if (isLoggedIn && isLoginPage) {
        // Se estou logado e na página de login, vou para a lista
        window.location.href = 'lista_customer.html'; 
    } else if (!isLoggedIn && !isLoginPage) {
        // Se não estou logado e NÃO estou na página de login, volto para o início
        window.location.href = 'index.html';
    }
}

function setupEventListeners() {
    // Abas de navegação (Login / Registro)
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    });

    // Submissão do Login
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    // Submissão do Registro
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
}

// ==========================================
// NAVEGAÇÃO ENTRE ABAS
// ==========================================
function switchTab(tab) {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');

    tabBtns.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tab);
    });
    
    if (tab === 'login') {
        registerForm.classList.remove('active');
        // O erro estava aqui: faltava o .classList antes do .add
        setTimeout(() => loginForm.classList.add('active'), 50);
    } else {
        loginForm.classList.remove('active');
        // E aqui também
        setTimeout(() => registerForm.classList.add('active'), 50);
    }
    clearMessages();
}
// function switchTab(tab) {
//     const tabBtns = document.querySelectorAll('.tab-btn');
//     const loginForm = document.getElementById('login-form');
//     const registerForm = document.getElementById('register-form');

//     tabBtns.forEach(btn => {
//         btn.classList.toggle('active', btn.dataset.tab === tab);
//     });
    
//     if (tab === 'login') {
//         registerForm.classList.remove('active');
//         setTimeout(() => loginForm.add('active'), 50);
//     } else {
//         loginForm.classList.remove('active');
//         setTimeout(() => registerForm.add('active'), 50);
//     }
//     clearMessages();
// }

// ==========================================
// MÁSCARAS DE INPUT (Padrão Santanna)
// ==========================================
function applyInputMasks() {
    const cpfInput = document.getElementById('reg-cpf');
    if (cpfInput) {
        cpfInput.addEventListener('input', (e) => {
            let v = e.target.value.replace(/\D/g, '');
            v = v.replace(/(\d{3})(\d)/, '$1.$2');
            v = v.replace(/(\d{3})(\d)/, '$1.$2');
            v = v.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
            e.target.value = v.substring(0, 14);
        });
    }

    const cnpjInput = document.getElementById('reg-cnpj');
    if (cnpjInput) {
        cnpjInput.addEventListener('input', (e) => {
            let v = e.target.value.replace(/\D/g, '');
            v = v.replace(/^(\d{2})(\d)/, '$1.$2');
            v = v.replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3');
            v = v.replace(/\.(\d{3})(\d)/, '.$1/$2');
            v = v.replace(/(\d{4})(\d)/, '$1-$2');
            e.target.value = v.substring(0, 18);
        });
    }

    const phoneInput = document.getElementById('reg-phone');
    if (phoneInput) {
        phoneInput.addEventListener('input', (e) => {
            let v = e.target.value.replace(/\D/g, '');
            v = v.replace(/^(\d{2})(\d)/, '($1) $2');
            v = v.replace(/(\d{5})(\d)/, '$1-$2');
            e.target.value = v.substring(0, 15);
        });
    }
}

// ==========================================
// LÓGICA DE LOGIN
// ==========================================
async function handleLogin(e) {
    e.preventDefault();
    if (isSubmitting) return;

    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;

    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    try {
        isSubmitting = true;
        setButtonLoading(submitBtn, true);

        const response = await fetch(`${API_BASE_URL}/person/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            saveSession(data, document.getElementById('remember').checked);
            showMessage('Login realizado!', 'success');
            window.location.href = 'html/lista_customer.html';
        } else {
            throw new Error(data.detail || 'Falha no login');
        }
    } catch (error) {
        showMessage(error.message, 'error');
    } finally {
        setButtonLoading(submitBtn, false, originalText);
        isSubmitting = false;
    }
}

// ==========================================
// LÓGICA DE REGISTRO
// ==========================================
async function handleRegister(e) {
    e.preventDefault();
    if (isSubmitting) return;

    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;

    const formData = {
        name: document.getElementById('reg-name').value,
        cpf: document.getElementById('reg-cpf').value.replace(/\D/g, ''),
        cnpj: document.getElementById('reg-cnpj').value.replace(/\D/g, ''),
        phone: document.getElementById('reg-phone').value.replace(/\D/g, ''),
        email: document.getElementById('reg-email').value,
        password: document.getElementById('reg-password').value
    };

    try {
        isSubmitting = true;
        setButtonLoading(submitBtn, true);

        const response = await fetch(`${API_BASE_URL}/person/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            showMessage('Conta criada! Faça login.', 'success');
            form.reset();
            switchTab('login');
        } else {
            const data = await response.json();
            throw new Error(data.detail || 'Erro no registro');
        }
    } catch (error) {
        showMessage(error.message, 'error');
    } finally {
        setButtonLoading(submitBtn, false, originalText);
        isSubmitting = false;
    }
}

// ==========================================
// UTILITÁRIOS (MANTIDOS)
// ==========================================
function saveSession(data, remember) {
    const storage = remember ? localStorage : sessionStorage;
    storage.setItem('token', data.access_token || data.token);
    storage.setItem('user', JSON.stringify(data.user || { email: 'contato@santanna.dev' }));
}

function setButtonLoading(button, loading, originalText) {
    button.disabled = loading;
    button.innerHTML = loading ? 'Aguarde...' : originalText;
}

function showMessage(message, type) {
    const container = document.getElementById('message-container');
    container.innerHTML = `<div class="message ${type}">${message}</div>`;
    setTimeout(clearMessages, 5000);
}

function clearMessages() {
    const container = document.getElementById('message-container');
    if (container) container.innerHTML = '';
}

function logout() {
    localStorage.clear();
    sessionStorage.clear();
    window.location.href = 'index.html';
}

window.logout = logout;