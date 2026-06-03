/* sidebar.js — Injects the shared sidebar navigation */

const ROLE_NAV = {
  user:     { inventory: false, reports: false },
  cashier:  { inventory: true,  reports: false },
  manager:  { inventory: true,  reports: true  },
  admin:    { inventory: true,  reports: true  },
};

const SIDEBAR_HTML = (activePage, role) => {
  const nav = ROLE_NAV[role] || ROLE_NAV.user;
  return `
<div class="sidebar-logo">
  <a href="/dashboard.html" class="logo-mark">
    <div class="logo-icon">🏪</div>
    <div>
      <div class="logo-text">POSIFY</div>
      <div class="logo-sub">POS & Inventory</div>
    </div>
  </a>
</div>
<nav class="sidebar-nav">
  <span class="nav-section-label">Main Menu</span>
  <a href="/dashboard.html" class="nav-link ${activePage === 'dashboard' ? 'active' : ''}">
    <svg class="nav-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
    Dashboard
  </a>
  ${nav.inventory ? `<a href="/inventory.html" class="nav-link ${activePage === 'inventory' ? 'active' : ''}">
    <svg class="nav-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M20 7H4a2 2 0 00-2 2v10a2 2 0 002 2h16a2 2 0 002-2V9a2 2 0 00-2-2z"/><path d="M16 7V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v2"/></svg>
    Inventory
    <span class="nav-badge" id="low-stock-badge" style="display:none">!</span>
  </a>` : ''}
  <a href="/pos.html" class="nav-link ${activePage === 'pos' ? 'active' : ''}">
    <svg class="nav-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 002 1.61h9.72a2 2 0 001.95-1.57L23 6H6"/></svg>
    Point of Sale
  </a>
  ${nav.reports ? `<a href="/reports.html" class="nav-link ${activePage === 'reports' ? 'active' : ''}">
    <svg class="nav-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
    Reports
  </a>` : ''}
  <span class="nav-section-label">Account</span>
  <a href="/settings.html" class="nav-link ${activePage === 'settings' ? 'active' : ''}">
    <svg class="nav-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"/></svg>
    Settings
  </a>
</nav>
<div class="sidebar-user">
  <div class="user-avatar" id="sidebar-user-avatar">A</div>
  <div class="user-info">
    <div class="user-name" id="sidebar-user-name">Loading…</div>
    <div class="user-role" id="sidebar-user-role">—</div>
  </div>
  <button class="btn-logout" onclick="handleLogout()" title="Sign out">
    <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
      <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
    </svg>
  </button>
</div>
`;};

function initSidebar(activePage) {
  const user = Api.getUser();
  const role = user ? user.role : 'user';
  const sidebar = document.getElementById('app-sidebar');
  if (sidebar) {
    sidebar.innerHTML = SIDEBAR_HTML(activePage, role);
    populateSidebarUser();
  }
  // Mobile overlay
  const mobileBtn = document.getElementById('mobile-menu-btn');
  if (mobileBtn) {
    mobileBtn.addEventListener('click', () => sidebar.classList.toggle('open'));
  }
  // Load low stock count for badge
  Api.getProducts({ low_stock: true }).then(({ products }) => {
    const badge = document.getElementById('low-stock-badge');
    if (badge && products.length > 0) {
      badge.textContent = products.length;
      badge.style.display = 'inline-flex';
    }
  }).catch(() => {});
}
