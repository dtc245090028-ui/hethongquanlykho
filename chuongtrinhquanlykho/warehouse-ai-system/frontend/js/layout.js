/* =====================================================
   layout.js — Render sidebar navigation và top navbar
   Inject HTML vào #sidebar-container và #topbar-container
   ===================================================== */

/* Danh sách menu item — icon Bootstrap Icons, label, href, roles được phép */
const MENU_ITEMS = [
  { icon: 'bi-speedometer2', label: 'Dashboard',         href: '/dashboard.html',             roles: ['admin','warehouse_manager','warehouse_keeper'] },
  { icon: 'bi-truck',        label: 'Nhà cung cấp',      href: '/pages/suppliers.html',        roles: ['admin','warehouse_manager'] },
  { icon: 'bi-box-seam',     label: 'Hàng hóa',          href: '/pages/goods.html',            roles: ['admin','warehouse_manager','warehouse_keeper'] },
  { icon: 'bi-cart-plus',    label: 'Đơn đặt hàng',      href: '/pages/purchase-orders.html',  roles: ['admin','warehouse_manager','warehouse_keeper'] },
  { icon: 'bi-arrow-down-circle', label: 'Phiếu nhập kho', href: '/pages/goods-receipts.html', roles: ['admin','warehouse_manager','warehouse_keeper'] },
  { icon: 'bi-arrow-up-circle',   label: 'Phiếu xuất kho', href: '/pages/goods-issues.html',   roles: ['admin','warehouse_manager','warehouse_keeper'] },
  { icon: 'bi-clipboard-check',   label: 'Kiểm kê kho',    href: '/pages/stocktakes.html',     roles: ['admin','warehouse_manager','warehouse_keeper'] },
  { icon: 'bi-receipt',      label: 'Hóa đơn & Công nợ', href: '/pages/invoices.html',         roles: ['admin','warehouse_manager'] },
  { icon: 'bi-bar-chart-line', label: 'Báo cáo thống kê', href: '/pages/reports.html',         roles: ['admin','warehouse_manager'] },
  { icon: 'bi-robot',        label: 'AI Trợ lý',          href: '/pages/ai-features.html',     roles: ['admin','warehouse_manager','warehouse_keeper'] },
];

/* Đường dẫn prefix để xác định item active */
function isActiveLink(href) {
  const current = window.location.pathname;
  return current === href || current.endsWith(href);
}

function prepareLazyContent(root) {
  if (!root) return;

  root.querySelectorAll('img:not([loading]), iframe:not([loading])').forEach(media => {
    media.loading = 'lazy';
  });

  Array.from(root.children).slice(1).forEach(section => {
    section.classList.add('lazy-content');
  });
}

/* =====================================================
   SPA Shell State Management & Helpers
   ===================================================== */
let isShellLoading = false;
let isNavigationBound = false;
let currentAbortController = null;
let pendingPageInits = [];

/* Đăng ký callback khởi tạo cho trang con được nạp qua shell */
window.__registerPageInit = function (callback) {
  if (typeof callback === 'function') {
    pendingPageInits.push(callback);
  }
};

/* Cập nhật active link trên sidebar menu */
function updateActiveSidebarLink(urlPath) {
  const currentPath = (urlPath || window.location.pathname).split('?')[0];
  document.querySelectorAll('#sidebar nav a').forEach(item => {
    const href = item.getAttribute('href');
    if (!href) return;
    const itemPath = href.split('?')[0];
    if (
      currentPath === itemPath ||
      currentPath.endsWith(itemPath) ||
      ((itemPath === '/dashboard.html' || itemPath === 'dashboard.html') &&
        (currentPath === '/' || currentPath.endsWith('index.html') || currentPath.endsWith('dashboard.html')))
    ) {
      item.classList.add('active');
    } else {
      item.classList.remove('active');
    }
  });
}

/* Đóng tất cả modal Bootstrap và xóa backdrop cũ */
function cleanupModalsAndBackdrops() {
  try {
    document.querySelectorAll('.modal.show').forEach(modalEl => {
      const modalInstance = bootstrap.Modal.getInstance(modalEl);
      if (modalInstance) {
        modalInstance.hide();
      }
    });
  } catch (_) {}
  document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
  document.body.classList.remove('modal-open');
  document.body.style.removeProperty('padding-right');
  document.body.style.removeProperty('overflow');
}

/* Nạp nội dung trang con vào Shell an toàn, không kích hoạt lại DOMContentLoaded toàn cục */
async function loadContentIntoShell(url, pushState = true) {
  const pageContent = document.getElementById('page-content');
  if (!pageContent) return;

  // Chốt chặn chống spam request / double-fetch
  if (isShellLoading) return;
  isShellLoading = true;

  // Hủy tác vụ fetch cũ nếu đang chạy
  if (currentAbortController) {
    currentAbortController.abort();
  }
  currentAbortController = new AbortController();

  cleanupModalsAndBackdrops();

  // Dọn dẹp DOM cũ được inject từ lần trước
  document.querySelectorAll('[data-shell-injected="true"]').forEach(node => node.remove());
  document.querySelectorAll('script[data-shell-script="true"]').forEach(node => node.remove());

  // Reset hàm khởi tạo trang con
  window.initPage = null;
  pendingPageInits = [];

  const markInjectedNode = (node) => {
    node.setAttribute('data-shell-injected', 'true');
    return node;
  };

  const targetBaseUrl = new URL(url, window.location.origin);
  const CORE_SCRIPTS = ['bootstrap', 'api.js', 'auth.js', 'utils.js', 'layout.js'];
  const isCoreScript = (src) => {
    if (!src) return false;
    return CORE_SCRIPTS.some(core => src.toLowerCase().includes(core.toLowerCase()));
  };

  const executeFetchedScripts = async (scripts) => {
    for (const script of scripts) {
      const rawSrc = script.getAttribute('src');
      if (rawSrc) {
        // Bỏ qua các script cốt lõi đã nạp sẵn trong shell
        if (isCoreScript(rawSrc)) {
          continue;
        }

        // Tính URL tuyệt đối dựa trên URL của trang nguồn được nạp
        const scriptUrl = new URL(rawSrc, targetBaseUrl).href;
        const alreadyLoaded = Array.from(document.scripts).some(existing => {
          return existing.src && new URL(existing.src, window.location.href).href === scriptUrl;
        });

        if (alreadyLoaded) continue;

        await new Promise((resolve, reject) => {
          const newScript = document.createElement('script');
          newScript.setAttribute('data-shell-script', 'true');
          newScript.src = scriptUrl;
          newScript.async = false;
          newScript.onload = () => resolve();
          newScript.onerror = () => reject(new Error(`Không tải được script: ${scriptUrl}`));
          document.body.appendChild(newScript);
        });
      } else {
        const newScript = document.createElement('script');
        newScript.setAttribute('data-shell-script', 'true');
        // Tương thích an toàn: Thay thế addEventListener('DOMContentLoaded'...) bằng window.__registerPageInit
        // để không phụ thuộc và không kích hoạt lại DOMContentLoaded toàn cục
        const transformedCode = script.textContent.replace(
          /document\.addEventListener\(\s*['"]DOMContentLoaded['"]\s*,/g,
          'window.__registerPageInit('
        );
        newScript.textContent = `(function() {\n${transformedCode}\n})();`;
        document.body.appendChild(newScript);
      }
    }
  };

  try {
    const response = await fetch(url, {
      headers: { 'X-Requested-With': 'fetch' },
      signal: currentAbortController.signal,
    });

    if (!response.ok) {
      throw new Error(`Không tải được trang: ${response.status}`);
    }

    const html = await response.text();
    const fetchedDocument = new DOMParser().parseFromString(html, 'text/html');
    const fetchedBody = fetchedDocument.body;

    const fetchedMain = fetchedDocument.querySelector('main#page-content') || fetchedDocument.querySelector('main');
    const extraNodes = Array.from(fetchedBody?.children || []).filter(node =>
      node !== fetchedMain &&
      !node.contains(fetchedMain) &&
      !node.matches('script') &&
      node.id !== 'sidebar-container' &&
      node.id !== 'topbar-container' &&
      node.id !== 'main-wrapper'
    );

    const contentHtml = fetchedMain ? fetchedMain.innerHTML : (fetchedBody?.innerHTML || '');
    pageContent.innerHTML = contentHtml;
    prepareLazyContent(pageContent);

    // Chèn modals và các phần tử con phụ thuộc vào body
    extraNodes.forEach(node => {
      document.body.appendChild(markInjectedNode(node.cloneNode(true)));
    });

    // Đồng bộ URL và trạng thái sidebar
    if (pushState) {
      window.history.pushState({ url }, '', url);
    }
    updateActiveSidebarLink(url);

    // Nạp và thực thi script của trang con (bỏ qua các core scripts đã có sẵn)
    const fetchedScripts = Array.from(fetchedDocument.querySelectorAll('script')).filter(script => {
      const rawSrc = script.getAttribute('src');
      if (!rawSrc) return true;
      if (isCoreScript(rawSrc)) return false;
      const scriptUrl = new URL(rawSrc, targetBaseUrl).href;
      return !Array.from(document.scripts).some(existing => existing.src && new URL(existing.src, window.location.href).href === scriptUrl);
    });
    await executeFetchedScripts(fetchedScripts);

    // Khởi tạo trang con: Ưu tiên window.initPage, sau đó chạy các callback đã đăng ký
    if (typeof window.initPage === 'function') {
      try {
        await window.initPage();
      } catch (initErr) {
        console.error('Lỗi khi chạy window.initPage:', initErr);
      }
    }
    for (const initFn of pendingPageInits) {
      try {
        await initFn();
      } catch (err) {
        console.error('Lỗi khi chạy callback khởi tạo trang:', err);
      }
    }
    pendingPageInits = [];

    // Bắn sự kiện riêng cho trang con nếu cần lắng nghe
    document.dispatchEvent(new CustomEvent('shell:content-loaded', { detail: { url } }));
  } catch (error) {
    if (error.name === 'AbortError') return;
    pageContent.innerHTML = `
      <div class="alert alert-danger m-3">
        <i class="bi bi-exclamation-triangle-fill me-2"></i>
        ${utils.escapeHtml(error.message || 'Không thể tải nội dung trang.')}
      </div>
    `;
    console.error('loadContentIntoShell error:', error);
  } finally {
    isShellLoading = false;
  }
}

/* Đăng ký sự kiện điều hướng Shell — Chỉ chạy DUY NHẤT 1 LẦN */
function bindShellNavigation() {
  if (isNavigationBound) return;
  isNavigationBound = true;

  document.addEventListener('click', function (event) {
    const link = event.target.closest('a[href]');
    if (!link) return;

    if (link.id === 'btn-logout' || link.hasAttribute('data-bs-toggle') || link.hasAttribute('data-bs-dismiss')) {
      return;
    }

    const href = link.getAttribute('href');
    if (!href || href.startsWith('#') || href.startsWith('javascript:') || href.startsWith('mailto:')) {
      return;
    }

    let targetUrl;
    try {
      targetUrl = new URL(href, window.location.origin);
      if (targetUrl.origin !== window.location.origin) return;
    } catch {
      return;
    }

    const isPageNavigation = href.endsWith('.html') || href.startsWith('/');
    if (!isPageNavigation) return;

    const currentPath = window.location.pathname;
    const targetPath = targetUrl.pathname;
    if (targetPath === currentPath && targetUrl.search === window.location.search) {
      event.preventDefault();
      return;
    }

    // Các trang cổng riêng biệt chạy độc lập ngoài shell
    if (
      targetPath.endsWith('index.html') ||
      targetPath.endsWith('vendor-login.html') ||
      targetPath.endsWith('buyer-portal.html') ||
      targetPath.endsWith('supplier-portal.html')
    ) {
      return;
    }

    event.preventDefault();
    loadContentIntoShell(href, true);
  });

  // Hỗ trợ nút Back / Forward trên trình duyệt
  window.addEventListener('popstate', () => {
    loadContentIntoShell(window.location.pathname + window.location.search, false);
  });
}

/* Render toàn bộ layout (sidebar + topbar) */
function renderLayout() {
  const role = auth.getRole();
  const user = auth.getUser();
  const currentPath = window.location.pathname;

  /* ----- Render SIDEBAR ----- */
  const sidebarContainer = document.getElementById('sidebar-container');
  if (sidebarContainer) {
    // Lọc menu theo role
    const visibleItems = MENU_ITEMS.filter(item => item.roles.includes(role));

    const navLinks = visibleItems.map(item => {
      const active = isActiveLink(item.href) ? 'active' : '';
      return `
        <a href="${item.href}" class="${active}" title="${item.label}">
          <i class="bi ${item.icon}"></i>
          <span class="nav-label ms-2">${item.label}</span>
        </a>`;
    }).join('');

    sidebarContainer.innerHTML = `
      <div id="sidebar">
        <!-- Brand logo -->
        <div class="sidebar-brand">
          <span class="brand-icon"><i class="bi bi-boxes"></i></span>
          <div class="ms-2">
            <span class="brand-text d-block">Warehouse AI</span>
            <span class="brand-sub">// Quản lý kho</span>
          </div>
        </div>

        <!-- Navigation links -->
        <nav class="sidebar-nav">
          ${navLinks}
        </nav>

        <!-- Footer sidebar: version -->
        <div class="sidebar-footer d-flex align-items-center" style="white-space:nowrap;overflow:hidden;">
          <i class="bi bi-circle-fill" style="min-width:38px;text-align:center;font-size:0.4rem;color:var(--accent-green);filter:drop-shadow(0 0 4px var(--accent-green));"></i>
          <small class="nav-label" style="font-family:'Space Mono',monospace;font-size:0.65rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em;">v1.0 // SYS_STABLE</small>
        </div>
      </div>
      <!-- Overlay mobile -->
      <div class="sidebar-overlay" id="sidebar-overlay"></div>
    `;
  }

  /* ----- Render TOPBAR ----- */
  const topbarContainer = document.getElementById('topbar-container');
  if (topbarContainer) {
    const roleLabel = auth.getRoleLabel();
    const roleBadgeClass = {
      admin: 'bg-danger',
      warehouse_manager: 'bg-warning',
      warehouse_keeper: 'bg-success',
    }[role] || 'bg-secondary';

    topbarContainer.innerHTML = `
      <div id="topbar">
        <!-- Nút toggle sidebar -->
        <button id="sidebar-toggle" class="btn btn-sm btn-outline-secondary" title="Thu/mở menu">
          <i class="bi bi-list fs-5"></i>
        </button>

        <!-- Tiêu đề trang (được set bởi mỗi trang) -->
        <span class="page-title" id="page-title-text">Hệ thống Quản lý Kho</span>

        <div class="ms-auto d-flex align-items-center gap-2">
          <!-- Badge role -->
          <span class="badge ${roleBadgeClass} d-none d-md-inline">${roleLabel}</span>

          <!-- Dropdown user -->
          <div class="dropdown">
            <button class="btn btn-sm btn-outline-secondary dropdown-toggle" data-bs-toggle="dropdown">
              <i class="bi bi-person-circle me-1"></i>
              <span class="d-none d-sm-inline">${utils.escapeHtml(user.full_name || user.username || 'User')}</span>
            </button>
            <ul class="dropdown-menu dropdown-menu-end">
              <li><span class="dropdown-item-text text-muted small">${utils.escapeHtml(user.username || '')}</span></li>
              <li><hr class="dropdown-divider"></li>
              <li>
                <a class="dropdown-item text-danger" href="#" id="btn-logout">
                  <i class="bi bi-box-arrow-right me-2"></i>Đăng xuất
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    `;

    /* Gắn sự kiện logout */
    document.getElementById('btn-logout')?.addEventListener('click', async (e) => {
      e.preventDefault();
      const ok = await utils.confirmDialog('Đăng xuất', 'Bạn có muốn đăng xuất khỏi hệ thống?');
      if (ok) auth.logout();
    });

    /* Toggle sidebar */
    document.getElementById('sidebar-toggle')?.addEventListener('click', () => {
      const sidebar = document.getElementById('sidebar');
      const mainWrapper = document.getElementById('main-wrapper');
      const overlay = document.getElementById('sidebar-overlay');

      if (window.innerWidth <= 768) {
        // Mobile: overlay mode
        sidebar?.classList.toggle('mobile-open');
        overlay?.classList.toggle('visible');
      } else {
        // Desktop: collapse mode
        sidebar?.classList.toggle('collapsed');
        mainWrapper?.classList.toggle('expanded');
      }
    });

    /* Click overlay để đóng sidebar trên mobile */
    document.getElementById('sidebar-overlay')?.addEventListener('click', () => {
      document.getElementById('sidebar')?.classList.remove('mobile-open');
      document.getElementById('sidebar-overlay')?.classList.remove('visible');
    });
  }

  /* Áp dụng ẩn/hiện theo role */
  auth.applyRoleVisibility();
}

/* Hàm tiện ích: set tiêu đề trang trên topbar */
function setPageTitle(title) {
  const el = document.getElementById('page-title-text');
  if (el) el.textContent = title;
  document.title = title + ' — Quản lý Kho';
}

/* Tự động gọi khi DOM ready */
document.addEventListener('DOMContentLoaded', () => {
  // Kiểm tra đăng nhập trước khi render layout
  if (!auth.requireLogin()) return;
  renderLayout();
  prepareLazyContent(document.getElementById('page-content'));
  bindShellNavigation();
  updateActiveSidebarLink();
});

