/**
 * js/api.js  –  Shared API client, Auth, and utilities
 */

const API_BASE = "http://127.0.0.1:5000";

// ── Auth ─────────────────────────────────────────────────────────────────
const Auth = {
  getToken:   ()            => localStorage.getItem("blog_token"),
  getUser:    ()            => JSON.parse(localStorage.getItem("blog_user") || "null"),
  save:       (token, user) => { localStorage.setItem("blog_token", token); localStorage.setItem("blog_user", JSON.stringify(user)); },
  clear:      ()            => { localStorage.removeItem("blog_token"); localStorage.removeItem("blog_user"); },
  isLoggedIn: ()            => !!localStorage.getItem("blog_token"),
};

// ── Core fetch wrapper ────────────────────────────────────────────────────
async function apiRequest(path, method = "GET", body = null) {
  const headers = { "Content-Type": "application/json" };
  const token = Auth.getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const opts = { method, headers };
  if (body) opts.body = JSON.stringify(body);

  try {
    const res  = await fetch(`${API_BASE}${path}`, opts);
    const data = await res.json();
    return { ok: res.ok, status: res.status, data };
  } catch (err) {
    return { ok: false, status: 0, data: { error: "Network error – is the server running?" } };
  }
}

// ── Toast ─────────────────────────────────────────────────────────────────
function showToast(message, type = "info") {
  let toast = document.getElementById("toast");
  if (!toast) { toast = document.createElement("div"); toast.id = "toast"; document.body.appendChild(toast); }
  toast.textContent = message;
  toast.className   = `${type} show`;
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => toast.classList.remove("show"), 3200);
}

// ── Navbar ────────────────────────────────────────────────────────────────
function renderNavbar() {
  const nav = document.getElementById("navbar");
  if (!nav) return;
  const user = Auth.getUser();
  nav.innerHTML = `
    <nav class="navbar">
      <div class="container">
        <a href="index.html" class="navbar-brand">✍️ Blog<span>BOO</span>Hub</a>
        <div class="navbar-links">
          <a href="index.html" class="nav-link">Home</a>
          ${user ? `
            <a href="create-post.html" class="nav-link">+ Write</a>
            <div class="nav-user">Hi, <strong>${escapeHtml(user.username)}</strong></div>
            <button class="btn btn-ghost btn-sm" onclick="logout()">Logout</button>
          ` : `
            <a href="login.html"    class="nav-link">Login</a>
            <a href="register.html" class="btn btn-primary btn-sm">Sign Up</a>
          `}
        </div>
      </div>
    </nav>`;
}

// ── Logout ────────────────────────────────────────────────────────────────
function logout() {
  Auth.clear();
  showToast("Logged out successfully", "info");
  setTimeout(() => { window.location.href = "index.html"; }, 800);
}

// ── Helpers ───────────────────────────────────────────────────────────────
function escapeHtml(str = "") {
  const d = document.createElement("div");
  d.textContent = str;
  return d.innerHTML;
}

function formatDate(iso) {
  return new Date(iso).toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" });
}

function formatRelative(iso) {
  const diff = Date.now() - new Date(iso).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1)  return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24)  return `${hrs}h ago`;
  const days = Math.floor(hrs / 24);
  if (days < 30) return `${days}d ago`;
  return formatDate(iso);
}

function requireAuth(redirectTo = "login.html") {
  if (!Auth.isLoggedIn()) {
    showToast("Please log in to continue", "error");
    window.location.href = redirectTo;
    return false;
  }
  return true;
}
