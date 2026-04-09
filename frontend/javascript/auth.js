/**
 * SISTEMA CONTÁBIL - MÓDULO DE CLIENTES (CUSTOMERS)
 * Gerencia a listagem e o cadastro de empresas vinculadas ao contador
 */

const API_BASE_URL = 'http://localhost:8000';

// ==========================================
// PROTEÇÃO DE ROTA E LOGOUT
// ==========================================
const token = localStorage.getItem('token');
if (!token) {
    window.location.href = '../index.html';
}

function logout() {
    localStorage.clear();
    window.location.href = '../index.html';
}

// ==========================================
// INICIALIZAÇÃO
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    // Aplicar máscaras se os campos existirem na página
    applyCustomerMasks();

    if (document.getElementById('customer-list-container')) {
        loadCustomers();
    }

    if (document.getElementById('customer-registration-form')) {
        initRegistrationForm();
    }
});

// ==========================================
// MÁSCARAS DE INPUT (Padrão Santanna)
// ==========================================
function applyCustomerMasks() {
    const cnpjInput = document.getElementById('cust-cnpj');
    if (cnpjInput) {
        cnpjInput.addEventListener('input', (e) => {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/^(\d{2})(\d)/, '$1.$2');
            value = value.replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3');
            value = value.replace(/\.(\d{3})(\d)/, '.$1/$2');
            value = value.replace(/(\d{4})(\d)/, '$1-$2');
            e.target.value = value.substring(0, 18);
        });
    }

    const phoneInput = document.getElementById('cust-phone');
    if (phoneInput) {
        phoneInput.addEventListener('input', (e) => {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/^(\d{2})(\d)/, '($1) $2');
            value = value.replace(/(\d{5})(\d)/, '$1-$2');
            e.target.value = value.substring(0, 15);
        });
    }
}

// ==========================================
// LISTAGEM DE EMPRESAS
// ==========================================
async function loadCustomers() {
    const tbody = document.querySelector('#customer-table tbody');
    
    try {
        const response = await fetch(`${API_BASE_URL}/customers`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const customers = await response.json();
            renderCustomerTable(customers);
        } else if (response.status === 401) {
            logout();
        }
    } catch (error) {
        console.error('Erro de conexão:', error);
        // Mock para teste de interface
        renderCustomerTable([
            { id: 1, name: "Empresa Teste", cnpj: "00.000.000/0001-00", phone: "(11) 99999-9999", email: "teste@empresa.com" }
        ]);
    }
}

function renderCustomerTable(customers) {
    const tbody = document.querySelector('#customer-table tbody');
    if (!tbody) return;

    if (customers.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">Nenhuma empresa encontrada.</td></tr>';
        return;
    }

    tbody.innerHTML = customers.map(c => `
        <tr>
            <td>${c.name}</td>
            <td>${c.cnpj}</td>
            <td>${c.phone}</td>
            <td>${c.email}</td>
            <td>
                <button class="btn-action" onclick="alert('Visualizando PDF ID: ${c.id}')">Ver PDF</button>
            </td>
        </tr>
    `).join('');
}

// ==========================================
// CADASTRO DE EMPRESA (UPLOAD DE ARQUIVO)
// ==========================================
function initRegistrationForm() {
    const form = document.getElementById('customer-registration-form');
    const messageContainer = document.getElementById('message-container');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = "Enviando...";

        const formData = new FormData();
        formData.append('name', document.getElementById('cust-name').value);
        formData.append('cnpj', document.getElementById('cust-cnpj').value.replace(/\D/g, ''));
        formData.append('phone', document.getElementById('cust-phone').value.replace(/\D/g, ''));
        formData.append('email', document.getElementById('cust-email').value);
        
        const pdfFile = document.getElementById('cust-pdf').files[0];
        if (pdfFile) {
            formData.append('file', pdfFile);
        }

        try {
            const response = await fetch(`${API_BASE_URL}/customers`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` },
                body: formData
            });

            if (response.ok) {
                alert('Empresa cadastrada com sucesso!');
                window.location.href = 'lista_customer.html';
            } else {
                const err = await response.json();
                alert(err.detail || 'Erro ao cadastrar');
            }
        } catch (error) {
            alert('Erro de conexão com o servidor');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    });
}