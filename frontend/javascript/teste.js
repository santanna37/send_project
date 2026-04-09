/**
 * SISTEMA CONTÁBIL - MÓDULO DE AUTENTICAÇÃO
 * Gerencia Login e Registro com integração FastAPI
 */

// Configuração da API
const API_BASE_URL = 'http://localhost:8000'; // Ajuste conforme seu FastAPI

// Elementos do DOM
const tabBtns = document.querySelectorAll('.tab-btn');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const messageContainer = document.getElementById('message-container');

// ==========================================
// NAVEGAÇÃO ENTRE ABAS
// ==========================================

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const tab = btn.dataset.tab;
        
        // Atualizar botões
        tabBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        // Alternar formulários
        if (tab === 'login') {
            loginForm.classList.add('active');
            registerForm.classList.remove('active');
        } else {
            loginForm.classList.remove('active');
            registerForm.classList.add('active');
        }
    });
});

// ==========================================
// MÁSCARAS DE INPUT
// ==========================================

function applyMasks() {
    // CPF: 000.000.000-00
    const cpfInput = document.getElementById('reg-cpf');
    if (cpfInput) {
        cpfInput.addEventListener('input', (e) => {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
            e.target.value = value;
        });
    }

    // CNPJ: 00.000.000/0000-00
    const cnpjInput = document.getElementById('reg-cnpj');
    if (cnpjInput) {
        cnpjInput.addEventListener('input', (e) => {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{2})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d)/, '$1/$2');
            value = value.replace(/(\d{4})(\d{1,2})$/, '$1-$2');
            e.target.value = value;
        });
    }

    // Telefone: (00) 00000-0000
    const phoneInput = document.getElementById('reg-phone');
    if (phoneInput) {
        phoneInput.addEventListener('input', (e) => {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{2})(\d)/, '($1) $2');
            value = value.replace(/(\d{5})(\d{4})$/, '$1-$2');
            e.target.value = value;
        });
    }
}

applyMasks();

// ==========================================
// FUNÇÕES DE UTILIDADE
// ==========================================

function showMessage(message, type = 'success') {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${type}`;
    msgDiv.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            ${type === 'success' 
                ? '<path d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" fill="currentColor"/>'
                : '<path d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" fill="currentColor"/>'
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

function setLoading(button, loading = true) {
    const originalContent = button.innerHTML;
    if (loading) {
        button.disabled = true;
        button.innerHTML = `<div class="spinner"></div>`;
    } else {
        button.disabled = false;
        button.innerHTML = originalContent;
    }
    return originalContent;
}

// ==========================================
// LOGIN
// ==========================================

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const submitBtn = loginForm.querySelector('button[type="submit"]');
    const originalContent = setLoading(submitBtn, true);
    
    const formData = {
        email: document.getElementById('login-email').value,
        password: document.getElementById('login-password').value
    };
    
    try {
        // Exemplo de integração com FastAPI
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Salvar token
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));
            
            showMessage('Login realizado com sucesso!', 'success');
            
            // Redirecionar após 1 segundo
            setTimeout(() => {
                window.location.href = 'frontend/html/lista_customer.html';
            }, 1000);
        } else {
            showMessage(data.detail || 'Erro ao fazer login', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showMessage('Erro de conexão com o servidor', 'error');
        
        // Simulação para desenvolvimento (remover em produção)
        console.log('Dados de login:', formData);
        setTimeout(() => {
            localStorage.setItem('token', 'fake-token');
            window.location.href = 'frontend/html/lista_customer.html';
        }, 1000);
    } finally {
        setTimeout(() => setLoading(submitBtn, false), 1000);
    }
});

// ==========================================
// REGISTRO
// ==========================================

registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const submitBtn = registerForm.querySelector('button[type="submit"]');
    setLoading(submitBtn, true);
    
    const formData = {
        name: document.getElementById('reg-name').value,
        cpf: document.getElementById('reg-cpf').value.replace(/\D/g, ''),
        cnpj: document.getElementById('reg-cnpj').value.replace(/\D/g, '') || null,
        phone: document.getElementById('reg-phone').value.replace(/\D/g, ''),
        email: document.getElementById('reg-email').value,
        password: document.getElementById('reg-password').value
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage('Conta criada com sucesso! Faça login.', 'success');
            
            // Limpar formulário e mudar para login
            registerForm.reset();
            setTimeout(() => {
                document.querySelector('[data-tab="login"]').click();
            }, 1500);
        } else {
            showMessage(data.detail || 'Erro ao criar conta', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showMessage('Erro de conexão com o servidor', 'error');
        
        // Simulação para desenvolvimento
        console.log('Dados de registro:', formData);
        showMessage('Conta criada (simulação)!', 'success');
        registerForm.reset();
    } finally {
        setLoading(submitBtn, false);
    }
});

// Verificar se já está logado
if (localStorage.getItem('token') && window.location.pathname.includes('index')) {
    window.location.href = 'frontend/html/lista_customer.html';
}