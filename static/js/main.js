/* ===== main.js — ATS Resume Builder ===== */

// ---- Theme ----
const html = document.documentElement;
const themeToggle = document.getElementById('themeToggle');

function getTheme() {
  return localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
}
function applyTheme(t) {
  html.setAttribute('data-theme', t);
  const moon = document.getElementById('iconMoon');
  const sun = document.getElementById('iconSun');
  if (moon) moon.style.display = t === 'dark' ? 'none' : '';
  if (sun) sun.style.display = t === 'dark' ? '' : 'none';
}
applyTheme(getTheme());
if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    localStorage.setItem('theme', next);
    applyTheme(next);
  });
}

// ---- Hamburger ----
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('navLinks');
if (hamburger && navLinks) {
  hamburger.addEventListener('click', () => navLinks.classList.toggle('open'));
}

// ---- Avatar Dropdown ----
const avatarBtn = document.getElementById('avatarBtn');
const avatarDropdown = document.getElementById('avatarDropdown');
if (avatarBtn && avatarDropdown) {
  avatarBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    avatarDropdown.classList.toggle('open');
  });
  document.addEventListener('click', () => avatarDropdown.classList.remove('open'));
}

// ---- Toast auto-dismiss ----
const isAiPage = window.location.pathname.includes('/ai/');
document.querySelectorAll('.toast').forEach(t => {
  if (isAiPage) {
    t.remove();
  } else {
    setTimeout(() => t.remove(), 5000);
  }
});

// ---- Toast helper ----
function showToast(msg, type = 'success') {
  const container = document.getElementById('toastContainer') || (() => {
    const el = document.createElement('div');
    el.className = 'toast-container';
    el.id = 'toastContainer';
    document.body.appendChild(el);
    return el;
  })();
  const toast = document.createElement('div');
  toast.className = `toast toast--${type}`;
  toast.innerHTML = `<span>${msg}</span><button class="toast-close" onclick="this.parentElement.remove()">×</button>`;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 5000);
}

// ---- CSRF helper ----
function getCsrf() {
  return document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
    document.cookie.split('; ').find(r => r.startsWith('csrftoken='))?.split('=')[1] || '';
}

async function apiFetch(url, options = {}) {
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf(), ...options.headers },
    ...options,
  });
  return res.json();
}

// ---- Utility & AI Response Markdown Formatter ----
function escapeHtml(str) {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function copyCodeBlock(btn) {
  const codeEl = btn.closest('.ai-code-card')?.querySelector('code');
  if (codeEl) {
    navigator.clipboard.writeText(codeEl.textContent);
    const orig = btn.textContent;
    btn.textContent = '✓ Copied!';
    setTimeout(() => { btn.textContent = orig; }, 2000);
  }
}

function formatAIResponse(text) {
  if (!text) return '';
  let str = String(text);

  // 1. Code blocks ```lang\ncode\n```
  str = str.replace(/```(\w*)\n([\s\S]*?)```/g, (match, lang, code) => {
    const l = lang || 'code';
    return `<div class="ai-code-card">
      <div class="ai-code-bar">
        <span class="ai-code-lang">${escapeHtml(l)}</span>
        <button class="ai-copy-btn" onclick="copyCodeBlock(this)">Copy</button>
      </div>
      <pre><code>${escapeHtml(code.trim())}</code></pre>
    </div>`;
  });

  // 2. Inline code `code`
  str = str.replace(/`([^`]+)`/g, (match, c) => `<code class="ai-inline-badge">${escapeHtml(c)}</code>`);

  // 3. Headings ###, ##, #
  str = str.replace(/^### (.*$)/gim, '<h4 class="ai-h4">$1</h4>');
  str = str.replace(/^## (.*$)/gim, '<h3 class="ai-h3">$1</h3>');
  str = str.replace(/^# (.*$)/gim, '<h2 class="ai-h2">$1</h2>');

  // 4. Bold & Italics
  str = str.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  str = str.replace(/\*(.*?)\*/g, '<em>$1</em>');

  // 5. Bullet points & lists
  str = str.replace(/^[•\-\*]\s+(.*)$/gim, '<li class="ai-li">$1</li>');
  str = str.replace(/^(\d+)\.\s+(.*)$/gim, '<li class="ai-li">$2</li>');

  // Group consecutive <li> items into <ul>
  str = str.replace(/(<li class="ai-li">[\s\S]*?<\/li>)(?!\s*<li)/g, '<ul class="ai-ul">$1</ul>');

  // 6. Paragraphs and newlines
  const blocks = str.split(/\n\n+/);
  const formattedBlocks = blocks.map(b => {
    b = b.trim();
    if (b.startsWith('<div') || b.startsWith('<h') || b.startsWith('<ul')) {
      return b;
    }
    return `<p class="ai-p">${b.replace(/\n/g, '<br>')}</p>`;
  });

  return `<div class="ai-formatted-body">${formattedBlocks.join('')}</div>`;
}

function markdownToHtml(text) {
  return formatAIResponse(text);
}

// ---- AI Chat Widget ----
const aiBubble = document.getElementById('aiBubble');
const aiWidgetPanel = document.getElementById('aiWidgetPanel');
const aiWidgetClose = document.getElementById('aiWidgetClose');
const aiWidgetMessages = document.getElementById('aiWidgetMessages');
const aiWidgetInput = document.getElementById('aiWidgetInput');
const aiWidgetSend = document.getElementById('aiWidgetSend');
let widgetSessionId = null;

if (aiBubble) {
  aiBubble.addEventListener('click', () => {
    aiWidgetPanel.classList.toggle('open');
    if (aiWidgetPanel.classList.contains('open')) {
      aiWidgetInput?.focus();
      const badge = document.getElementById('aiBubbleBadge');
      if (badge) badge.style.display = 'none';
    }
  });
}
if (aiWidgetClose) aiWidgetClose.addEventListener('click', () => aiWidgetPanel.classList.remove('open'));

function appendWidgetMsg(role, content) {
  const div = document.createElement('div');
  div.className = `ai-msg ai-msg--${role}`;
  const htmlContent = role === 'assistant' ? formatAIResponse(content) : `<div class="ai-msg-content">${escapeHtml(content)}</div>`;
  div.innerHTML = role === 'assistant' ? `<div class="ai-msg-content">${htmlContent}</div>` : htmlContent;
  aiWidgetMessages.appendChild(div);
  aiWidgetMessages.scrollTop = aiWidgetMessages.scrollHeight;
}

async function sendWidgetMessage() {
  const msg = aiWidgetInput?.value.trim();
  if (!msg) return;
  aiWidgetInput.value = '';
  appendWidgetMsg('user', msg);
  const typing = document.createElement('div');
  typing.className = 'ai-msg ai-msg--assistant';
  typing.id = 'widgetTyping';
  typing.innerHTML = '<div class="ai-msg-content"><span class="typing-indicator"><span></span><span></span><span></span></span></div>';
  aiWidgetMessages.appendChild(typing);
  aiWidgetMessages.scrollTop = aiWidgetMessages.scrollHeight;
  try {
    const data = await apiFetch('/ai/chat/', {
      method: 'POST',
      body: JSON.stringify({ message: msg, session_id: widgetSessionId }),
    });
    typing.remove();
    if (data.success) {
      widgetSessionId = data.session_id;
      appendWidgetMsg('assistant', data.response);
    } else {
      appendWidgetMsg('assistant', 'Sorry, I encountered an error: ' + (data.error || 'Unknown error'));
    }
  } catch {
    typing.remove();
    appendWidgetMsg('assistant', 'Network error. Please try again.');
  }
}

if (aiWidgetSend) aiWidgetSend.addEventListener('click', sendWidgetMessage);
if (aiWidgetInput) {
  aiWidgetInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendWidgetMessage(); }
  });
}

// Expose globally
window.showToast = showToast;
window.apiFetch = apiFetch;
window.getCsrf = getCsrf;
window.escapeHtml = escapeHtml;
window.formatAIResponse = formatAIResponse;
window.markdownToHtml = markdownToHtml;
window.copyCodeBlock = copyCodeBlock;
