// NK Facts – main.js

// ── THEME TOGGLE ──────────────────────────────────────────────────
// Theme is saved in localStorage so it persists across pages/sessions
// The <script> in <head> applies it instantly before page renders (no flash)
const themeToggle = document.getElementById('themeToggle');
const html        = document.documentElement;

function setTheme(theme) {
  html.setAttribute('data-theme', theme);
  localStorage.setItem('nkfacts-theme', theme);
}

if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    const current = html.getAttribute('data-theme') || 'light';
    setTheme(current === 'light' ? 'dark' : 'light');
  });
}

// ── HAMBURGER MENU ────────────────────────────────────────────────
const ham      = document.getElementById('hamburger');
const navLinks = document.getElementById('navLinks');
if (ham && navLinks) {
  ham.addEventListener('click', () => navLinks.classList.toggle('open'));
}

// ── ACTIVE NAV LINK ───────────────────────────────────────────────
document.querySelectorAll('.nav-links a').forEach(l => {
  if (l.href === location.href) l.classList.add('active');
});

// ── AUTO-DISMISS ALERTS ───────────────────────────────────────────
setTimeout(() => {
  document.querySelectorAll('.alert').forEach(a => {
    a.style.transition = 'opacity .5s';
    a.style.opacity    = '0';
    setTimeout(() => a.remove(), 500);
  });
}, 4000);
