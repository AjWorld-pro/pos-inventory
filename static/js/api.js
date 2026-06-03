/* api.js — Centralized API client for all backend calls */

const API_BASE = window.location.origin + '/api';

const Api = {
  getToken() {
    return localStorage.getItem('pos_token');
  },

  getUser() {
    try {
      return JSON.parse(localStorage.getItem('pos_user'));
    } catch { return null; }
  },

  setSession(token, user) {
    localStorage.setItem('pos_token', token);
    localStorage.setItem('pos_user', JSON.stringify(user));
  },

  clearSession() {
    localStorage.removeItem('pos_token');
    localStorage.removeItem('pos_user');
  },

  async request(method, path, body = null) {
    const token = this.getToken();
    const opts = {
      method,
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': 'Bearer ' + token } : {})
      }
    };
    if (body) opts.body = JSON.stringify(body);
    const res = await fetch(API_BASE + path, opts);
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.error || 'Request failed');
    return data;
  },

  get(path) { return this.request('GET', path); },
  post(path, body) { return this.request('POST', path, body); },
  put(path, body) { return this.request('PUT', path, body); },
  delete(path) { return this.request('DELETE', path); },

  // Auth
  login: (username, password) => Api.post('/auth/login', { username, password }),
  register: (name, username, email, password, role) => Api.post('/auth/register', { name, username, email, password, role }),
  logout: () => Api.post('/auth/logout'),
  getMe: () => Api.get('/auth/me'),
  updatePreferences: (preferences) => Api.put('/auth/preferences', { preferences }),
  updateProfile: (data) => Api.put('/auth/profile', data),

  // Products
  getProducts: (params = {}) => {
    const qs = new URLSearchParams();
    if (params.q) qs.set('q', params.q);
    if (params.category) qs.set('category', params.category);
    if (params.low_stock) qs.set('low_stock', 'true');
    if (params.preferences?.length) params.preferences.forEach(p => qs.append('preferences', p));
    return Api.get('/products/?' + qs.toString());
  },
  getProduct: (id) => Api.get('/products/' + id),
  createProduct: (data) => Api.post('/products/', data),
  updateProduct: (id, data) => Api.put('/products/' + id, data),
  deleteProduct: (id) => Api.delete('/products/' + id),
  getCategories: () => Api.get('/products/categories/list'),
  getProductStats: () => Api.get('/products/stats/overview'),

  // Transactions
  getTransactions: (params = {}) => {
    const qs = new URLSearchParams(params);
    return Api.get('/transactions/?' + qs.toString());
  },
  createTransaction: (data) => Api.post('/transactions/', data),
  getTransaction: (id) => Api.get('/transactions/' + id),
  getDailyReport: (date) => Api.get('/transactions/reports/daily' + (date ? '?date=' + date : '')),
  getWeeklyReport: () => Api.get('/transactions/reports/weekly'),
  getMonthlyReport: () => Api.get('/transactions/reports/monthly'),
  getOverview: () => Api.get('/transactions/reports/overview'),
};

// Toast notifications
function showToast(message, type = 'success', duration = 3500) {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }
  const icons = { success: '✓', error: '✕', warning: '⚠' };
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span style="font-size:16px">${icons[type] || '●'}</span> ${message}`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.animation = 'slideInToast 0.3s ease reverse';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// Auth guard — redirect to login if not authenticated
function requireAuth() {
  const token = Api.getToken();
  const user = Api.getUser();
  if (!token || !user) {
    window.location.href = '/index.html';
    return null;
  }
  return user;
}

// Format currency
function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount || 0);
}

// Format date
function formatDate(isoStr) {
  if (!isoStr) return '';
  return new Date(isoStr).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}

function formatDateTime(isoStr) {
  if (!isoStr) return '';
  return new Date(isoStr).toLocaleString('en-US', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
}

// Category emoji map
const CATEGORY_ICONS = {
  'Electronics': '💻',
  'Clothing & Apparel': '👗',
  'Food & Beverages': '🥤',
  'Health & Beauty': '💊',
  'Home & Garden': '🏡',
  'Sports & Outdoors': '⚽',
  'Toys & Games': '🎮',
  'Office Supplies': '📎',
  'Automotive': '🚗',
  'Books & Media': '📚',
};

// Populate user info in sidebar
function populateSidebarUser() {
  const user = Api.getUser();
  if (!user) return;
  const nameEl = document.getElementById('sidebar-user-name');
  const roleEl = document.getElementById('sidebar-user-role');
  const avatarEl = document.getElementById('sidebar-user-avatar');
  if (nameEl) nameEl.textContent = user.name;
  if (roleEl) roleEl.textContent = user.role;
  if (avatarEl) avatarEl.textContent = user.name ? user.name[0].toUpperCase() : 'U';
}

// Logout handler
function handleLogout() {
  Api.logout().catch(() => {});
  Api.clearSession();
  window.location.href = '/index.html';
}

// Debounce
function debounce(fn, ms = 300) {
  let t;
  return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
}
