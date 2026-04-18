/**
 * =====================================================
 * SISTEMA CONTÁBIL - LISTAGEM DE EMPRESAS
 * Versão Production Ready - HOTFIX CIRÚRGICO
 * =====================================================
 * OBJETIVO:
 * ✅ Corrigir renderização dos dados vindos da API
 * ✅ Manter tudo que já funcionava
 * ✅ Não alterar fluxo existente
 * ✅ Apenas adicionar compatibilidade de campos
 * =====================================================
 */

/* =====================================================
   CONFIGURAÇÃO DE AMBIENTE
===================================================== */

const API_BASE_URL =
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1"
        ? "http://localhost:8000"
        : "https://send-project-xxv7.onrender.com";

/* =====================================================
   ESTADO GLOBAL
===================================================== */

let companies = [];
let filteredCompanies = [];
let currentPage = 1;
let itemsPerPage = 10;
let isLoading = false;

/* =====================================================
   ELEMENTOS DOM
===================================================== */

const tableBody = document.getElementById("table-body");
const emptyState = document.getElementById("empty-state");
const searchInput = document.getElementById("search-input");
const filterStatus = document.getElementById("filter-status");
const prevPageBtn = document.getElementById("prev-page");
const nextPageBtn = document.getElementById("next-page");

/* =====================================================
   INIT
===================================================== */

document.addEventListener("DOMContentLoaded", () => {
    if (!checkAuth()) return;

    loadUserData();
    setupEventListeners();
    loadCompanies();
});

/* =====================================================
   AUTH
===================================================== */

function checkAuth() {
    const token =
        localStorage.getItem("token") ||
        sessionStorage.getItem("token");

    if (!token) {
        window.location.href = "/index.html";
        return false;
    }

    const expiry =
        localStorage.getItem("tokenExpiry") ||
        sessionStorage.getItem("tokenExpiry");

    if (expiry && Date.now() > Number(expiry)) {
        logout();
        return false;
    }

    return true;
}

function logout() {
    localStorage.clear();
    sessionStorage.clear();
    window.location.href = "../index.html";
}

/* =====================================================
   USER INFO
===================================================== */

function loadUserData() {
    try {
        const user = JSON.parse(
            localStorage.getItem("user") ||
            sessionStorage.getItem("user") ||
            "{}"
        );

        const nameEl = document.getElementById("user-name");
        const avatarEl = document.querySelector(".avatar");

        if (user?.name) {
            if (nameEl) nameEl.textContent = user.name;

            if (avatarEl) {
                avatarEl.textContent =
                    user.name.charAt(0).toUpperCase();
            }
        }
    } catch (error) {
        console.error("Erro ao carregar usuário:", error);
    }
}

/* =====================================================
   EVENTOS
===================================================== */

function setupEventListeners() {
    let debounce;

    searchInput?.addEventListener("input", (e) => {
        clearTimeout(debounce);

        debounce = setTimeout(() => {
            currentPage = 1;

            filterCompanies(
                e.target.value.toLowerCase(),
                filterStatus?.value || ""
            );
        }, 300);
    });

    filterStatus?.addEventListener("change", (e) => {
        currentPage = 1;

        filterCompanies(
            searchInput?.value.toLowerCase() || "",
            e.target.value
        );
    });

    prevPageBtn?.addEventListener("click", () => {
        if (currentPage > 1) {
            currentPage--;
            renderTable();
        }
    });

    nextPageBtn?.addEventListener("click", () => {
        const totalPages = Math.ceil(
            filteredCompanies.length / itemsPerPage
        );

        if (currentPage < totalPages) {
            currentPage++;
            renderTable();
        }
    });
}

/* =====================================================
   API LOAD
===================================================== */

async function loadCompanies() {
    if (isLoading) return;

    isLoading = true;
    showLoading(true);

    try {
        const token =
            localStorage.getItem("token") ||
            sessionStorage.getItem("token");

        const response = await fetch(`${API_BASE_URL}/customer/`, {
            method: "GET",
            headers: {
                Authorization: `Bearer ${token}`,
                Accept: "application/json",
                "Content-Type": "application/json",
            },
        });

        if (response.status === 401) {
            logout();
            return;
        }

        if (!response.ok) {
            throw new Error(
                `Erro ${response.status}: ${response.statusText}`
            );
        }

        const data = await response.json();

        console.log("Payload API:", data);

        if (Array.isArray(data)) {
            companies = data;
        } else if (Array.isArray(data.list_customer)) {
            companies = data.list_customer;
        } else if (Array.isArray(data.data)) {
            companies = data.data;
        } else if (Array.isArray(data.items)) {
            companies = data.items;
        } else {
            companies = [];
        }

        console.log("Empresas carregadas:", companies);
    } catch (error) {
        console.error("Erro ao carregar empresas:", error);

        showMessage(
            "API indisponível. Exibindo dados de exemplo.",
            "warning"
        );

        companies = getMockData();
    } finally {
        filteredCompanies = [...companies];

        renderTable();
        showLoading(false);
        isLoading = false;
    }
}

/* =====================================================
   MOCK DATA
===================================================== */

function getMockData() {
    return [
        {
            id: 1,
            name: "Empresa Alpha",
            cnpj: "12345678000199",
            phone: "11999999999",
            email: "alpha@email.com",
            status: "active",
        },
        {
            id: 2,
            name: "Beta Comércio",
            cnpj: "98765432000188",
            phone: "11988888888",
            email: "beta@email.com",
            status: "inactive",
        },
    ];
}

/* =====================================================
   REFRESH
===================================================== */

function refreshData() {
    currentPage = 1;
    loadCompanies();
}

/* =====================================================
   FILTRO
===================================================== */

function filterCompanies(searchTerm, status) {
    filteredCompanies = companies.filter((company) => {
        const companyName =
            company.name ||
            company.corporate_name ||
            company.fantasy_name ||
            "";

        const companyEmail =
            company.email || "";

        const companyStatus =
            company.status ||
            (company.active === true
                ? "active"
                : "inactive");

        const matchSearch =
            !searchTerm ||
            companyName
                .toLowerCase()
                .includes(searchTerm) ||
            companyEmail
                .toLowerCase()
                .includes(searchTerm) ||
            String(company.cnpj || "").includes(searchTerm);

        const matchStatus =
            !status || companyStatus === status;

        return matchSearch && matchStatus;
    });

    renderTable();
}

/* =====================================================
   RENDER TABLE
===================================================== */

function renderTable() {
    if (!tableBody) return;

    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;

    const pageItems = filteredCompanies.slice(start, end);

    const totalPages =
        Math.ceil(filteredCompanies.length / itemsPerPage) || 1;

    updatePagination(totalPages);

    if (filteredCompanies.length === 0) {
        tableBody.innerHTML = "";
        emptyState?.classList.remove("hidden");
        return;
    }

    emptyState?.classList.add("hidden");

    tableBody.innerHTML = pageItems
        .map((company) => {
            /* ==========================================
               HOTFIX:
               Compatibilidade sem quebrar legado
            ========================================== */

            const id =
                company.id ||
                company.id_customer ||
                0;

            const name =
                company.name ||
                company.corporate_name ||
                company.fantasy_name ||
                "-";

            const cnpj =
                company.cnpj || "-";

            const phone =
                company.phone ||
                company.cellphone ||
                company.telephone ||
                "-";

            const email =
                company.email || "-";

            const status =
                company.status ||
                (company.active === true
                    ? "active"
                    : "inactive");

            return `
        <tr>
            <td>${escapeHtml(name)}</td>
            <td>${formatCNPJ(cnpj)}</td>
            <td>${formatPhone(phone)}</td>
            <td>${escapeHtml(email)}</td>
            <td>
                <span class="status-badge ${
                    status === "active"
                        ? "status-active"
                        : "status-inactive"
                }">
                    ${
                        status === "active"
                            ? "Ativo"
                            : "Inativo"
                    }
                </span>
            </td>
            <td>
                <button onclick="editCompany(${id})">
                    Editar
                </button>

                <button onclick="confirmDelete(${id})">
                    Excluir
                </button>
            </td>
        </tr>
        `;
        })
        .join("");
}

function updatePagination(totalPages) {
    const currentEl =
        document.getElementById("current-page");

    const totalEl =
        document.getElementById("total-pages");

    if (currentEl) currentEl.textContent = currentPage;
    if (totalEl) totalEl.textContent = totalPages;

    if (prevPageBtn)
        prevPageBtn.disabled = currentPage === 1;

    if (nextPageBtn)
        nextPageBtn.disabled =
            currentPage >= totalPages;
}

/* =====================================================
   AÇÕES
===================================================== */

function editCompany(id) {
    const company = companies.find(
        (c) =>
            c.id === id ||
            c.id_customer === id
    );

    if (!company) return;

    sessionStorage.setItem(
        "editingCompany",
        JSON.stringify(company)
    );

    window.location.href =
        `/html/cadastro_customer.html?edit=${id}`;
}

function confirmDelete(id) {
    const company = companies.find(
        (c) =>
            c.id === id ||
            c.id_customer === id
    );

    if (!company) return;

    const companyName =
        company.name ||
        company.corporate_name ||
        company.fantasy_name ||
        "empresa";

    const ok = confirm(
        `Deseja excluir ${companyName}?`
    );

    if (ok) deleteCompany(id);
}

async function deleteCompany(id) {
    try {
        const token =
            localStorage.getItem("token") ||
            sessionStorage.getItem("token");

        const response = await fetch(
            `${API_BASE_URL}/customer/${id}`,
            {
                method: "DELETE",
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        );

        if (!response.ok) {
            throw new Error("Erro ao excluir");
        }

        companies = companies.filter(
            (c) =>
                c.id !== id &&
                c.id_customer !== id
        );

        filteredCompanies =
            filteredCompanies.filter(
                (c) =>
                    c.id !== id &&
                    c.id_customer !== id
            );

        renderTable();

        showMessage(
            "Empresa removida com sucesso.",
            "success"
        );
    } catch (error) {
        console.error(error);

        showMessage(
            "Erro ao excluir empresa",
            "error"
        );
    }
}

/* =====================================================
   HELPERS
===================================================== */

function formatCNPJ(cnpj) {
    if (!cnpj) return "-";

    const v = String(cnpj).replace(/\D/g, "");

    if (v.length !== 14) return cnpj;

    return v.replace(
        /(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/,
        "$1.$2.$3/$4-$5"
    );
}

function formatPhone(phone) {
    if (!phone) return "-";

    const v = String(phone).replace(/\D/g, "");

    if (v.length === 11) {
        return v.replace(
            /(\d{2})(\d{5})(\d{4})/,
            "($1) $2-$3"
        );
    }

    if (v.length === 10) {
        return v.replace(
            /(\d{2})(\d{4})(\d{4})/,
            "($1) $2-$3"
        );
    }

    return phone;
}

function escapeHtml(text) {
    if (!text) return "-";

    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

/* =====================================================
   UI
===================================================== */

function showLoading(show) {
    const btn = document.querySelector(
        'button[onclick="refreshData()"]'
    );

    if (!btn) return;

    btn.disabled = show;

    btn.innerHTML = show
        ? "Carregando..."
        : "Atualizar";
}

function showMessage(
    message,
    type = "success"
) {
    console.log(
        `[${type.toUpperCase()}] ${message}`
    );

    const container =
        document.getElementById(
            "message-container"
        );

    if (!container) {
        alert(message);
        return;
    }

    const div =
        document.createElement("div");

    div.className = `message ${type}`;
    div.textContent = message;

    container.appendChild(div);

    setTimeout(() => div.remove(), 4000);
}

/* =====================================================
   EXPORT GLOBAL
===================================================== */

window.refreshData = refreshData;
window.editCompany = editCompany;
window.confirmDelete = confirmDelete;
window.logout = logout;