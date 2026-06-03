/**
 * Laura IA - Pipeline Cadencia Dashboard
 * Connected to Supabase (laura_leads_cadencia)
 */

// ============================
// SUPABASE CONFIG
// ============================
const SUPABASE_URL = 'https://azmtxhjtqodtaeoshrye.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF6bXR4aGp0cW9kdGFlb3NocnllIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTI4NTM1ODUsImV4cCI6MjAyODQyOTU4NX0.KvQovDvmATwBPc50oqnY_yJqjqoywZdSXm_bz5qn4V0';

async function sbFetch(path, options = {}) {
  const { method = 'GET', body = null, headers: extra = {} } = options;
  const url = `${SUPABASE_URL}/rest/v1/${path}`;
  const headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': `Bearer ${SUPABASE_KEY}`,
    'Content-Type': 'application/json',
    'Prefer': 'return=representation',
    ...extra,
  };
  const resp = await fetch(url, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  });
  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`Supabase ${resp.status}: ${text}`);
  }
  const text = await resp.text();
  return text ? JSON.parse(text) : null;
}

// ============================
// CADENCIA STAGES
// ============================
const STAGES = [
  { id: 'dia1', name: 'Dia 1', subtitle: 'Ligacao + WhatsApp', color: '#99ccff' },
  { id: 'dia2', name: 'Dia 2', subtitle: 'Ligacao + WhatsApp', color: '#c1e0ff' },
  { id: 'dia3', name: 'Dia 3', subtitle: 'Ligacao',            color: '#fffd7f' },
  { id: 'dia4', name: 'Dia 4', subtitle: 'Email',              color: '#ffcc66' },
  { id: 'dia5', name: 'Dia 5', subtitle: 'Ultima tentativa',   color: '#ff8f92' },
  { id: 'convertido', name: 'Convertido', color: '#CCFF66', type: 'won' },
  { id: 'perdido',    name: 'Perdido',    color: '#D5D8DB', type: 'lost' },
];

// ============================
// STATE
// ============================
let leads = [];
let currentLeadId = null;

// ============================
// DOM REFERENCES
// ============================
const boardEl = document.getElementById('board');
const modalOverlay = document.getElementById('modalOverlay');
const modalTitle = document.getElementById('modalTitle');
const modalStage = document.getElementById('modalStage');
const modalTabs = document.getElementById('modalTabs');
const modalBody = document.getElementById('modalBody');
const btnRefresh = document.getElementById('btnRefresh');
const btnSave = document.getElementById('btnSaveModal');
const btnCancel = document.getElementById('btnCancelModal');
const btnClose = document.getElementById('btnCloseModal');
const btnDelete = document.getElementById('btnDeleteLead');
const navbarStats = document.getElementById('navbarStats');

// ============================
// DATA LOADING
// ============================
async function fetchLeads() {
  boardEl.innerHTML = '<div class="board-loading">Carregando leads...</div>';
  try {
    leads = await sbFetch('laura_leads_cadencia?select=*&order=criado_em.asc');
    renderBoard();
  } catch (err) {
    console.error('Erro ao carregar leads:', err);
    boardEl.innerHTML = '<div class="board-loading board-error">Erro ao carregar leads. Verifique console.</div>';
    showToast('Erro ao conectar no Supabase');
  }
}

async function updateLead(id, data) {
  try {
    const result = await sbFetch(`laura_leads_cadencia?id=eq.${id}`, {
      method: 'PATCH',
      body: data,
    });
    if (result && result[0]) {
      const idx = leads.findIndex(l => l.id === id);
      if (idx >= 0) leads[idx] = { ...leads[idx], ...result[0] };
    }
    return true;
  } catch (err) {
    console.error('Erro ao atualizar lead:', err);
    showToast('Erro ao salvar no Supabase');
    return false;
  }
}

async function loadInteracoes(leadId) {
  try {
    return await sbFetch(`laura_interacoes?lead_cadencia_id=eq.${leadId}&order=criado_em.desc`);
  } catch { return []; }
}

async function loadComentarios(leadId) {
  try {
    return await sbFetch(`laura_comentarios?lead_cadencia_id=eq.${leadId}&order=criado_em.desc`);
  } catch { return []; }
}

async function addComentario(leadId, texto, autor = 'Dashboard') {
  try {
    return await sbFetch('laura_comentarios', {
      method: 'POST',
      body: { lead_cadencia_id: leadId, autor, texto },
    });
  } catch (err) {
    console.error('Erro ao salvar comentario:', err);
    showToast('Erro ao salvar comentario');
    return null;
  }
}

// ============================
// BOARD RENDERING
// ============================
function renderBoard() {
  boardEl.innerHTML = '';

  STAGES.forEach(stage => {
    const stageLeads = leads.filter(l => {
      if (stage.id === 'convertido') return l.status === 'convertido';
      if (stage.id === 'perdido') return l.status === 'perdido';
      return l.coluna_atual === stage.id && l.status === 'ativo';
    });

    const col = document.createElement('div');
    col.className = 'column' + (stage.type === 'won' ? ' column-won' : '') + (stage.type === 'lost' ? ' column-lost' : '');
    col.dataset.stage = stage.id;

    col.innerHTML = `
      <div class="column-header">
        <div class="column-header-left">
          <span class="column-dot" style="background:${stage.color}"></span>
          <div class="column-label">
            <span class="column-name">${stage.name}</span>
            ${stage.subtitle ? `<span class="column-subtitle">${stage.subtitle}</span>` : ''}
          </div>
        </div>
        <span class="column-count">${stageLeads.length}</span>
      </div>
      <div class="column-body" data-stage="${stage.id}"></div>
    `;

    const body = col.querySelector('.column-body');
    stageLeads.forEach(lead => body.appendChild(createCard(lead)));

    body.addEventListener('dragover', handleDragOver);
    body.addEventListener('dragleave', handleDragLeave);
    body.addEventListener('drop', handleDrop);

    boardEl.appendChild(col);
  });

  updateStats();
}

function createCard(lead) {
  const card = document.createElement('div');
  card.className = 'card';
  card.dataset.id = lead.id;
  card.draggable = true;

  const stage = STAGES.find(s => {
    if (lead.status === 'convertido') return s.id === 'convertido';
    if (lead.status === 'perdido') return s.id === 'perdido';
    return s.id === lead.coluna_atual;
  }) || STAGES[0];
  card.style.borderLeftColor = stage.color;

  const tentativas = lead.tentativas_dia_atual || 0;
  const resultado = lead.ultimo_resultado_ligacao;

  card.innerHTML = `
    <div class="card-name">${esc(lead.nome || 'Sem nome')}</div>
    <div class="card-company">${esc(lead.posto || '')}</div>
    <div class="card-footer">
      <span class="card-phone">${esc(fmtPhone(lead.telefone))}</span>
      <div class="card-meta">
        ${tentativas > 0 ? `<span class="card-tag tag-tentativas">${tentativas}x</span>` : ''}
        ${resultado ? `<span class="card-tag tag-resultado">${esc(resultado)}</span>` : ''}
      </div>
    </div>
  `;

  card.addEventListener('click', () => openModal(lead.id));
  card.addEventListener('dragstart', handleDragStart);
  card.addEventListener('dragend', handleDragEnd);

  return card;
}

function updateStats() {
  const total = leads.length;
  const ativos = leads.filter(l => l.status === 'ativo').length;
  const convertidos = leads.filter(l => l.status === 'convertido').length;
  const perdidos = leads.filter(l => l.status === 'perdido').length;

  navbarStats.innerHTML = `
    <div class="stat"><span>Total:</span> <span class="stat-value">${total}</span></div>
    <div class="stat"><span>Ativos:</span> <span class="stat-value">${ativos}</span></div>
    <div class="stat"><span>Convertidos:</span> <span class="stat-value stat-won">${convertidos}</span></div>
    <div class="stat"><span>Perdidos:</span> <span class="stat-value stat-lost">${perdidos}</span></div>
  `;
}

// ============================
// DRAG & DROP
// ============================
let draggedCardId = null;

function handleDragStart(e) {
  draggedCardId = e.target.dataset.id;
  e.target.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
}

function handleDragEnd(e) {
  e.target.classList.remove('dragging');
  draggedCardId = null;
  document.querySelectorAll('.column-body.drag-over').forEach(el => el.classList.remove('drag-over'));
}

function handleDragOver(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
  e.currentTarget.classList.add('drag-over');
}

function handleDragLeave(e) {
  e.currentTarget.classList.remove('drag-over');
}

async function handleDrop(e) {
  e.preventDefault();
  e.currentTarget.classList.remove('drag-over');

  const newStage = e.currentTarget.dataset.stage;
  if (!draggedCardId || !newStage) return;

  const lead = leads.find(l => l.id === draggedCardId);
  if (!lead) return;

  const oldColuna = lead.coluna_atual;
  const oldStatus = lead.status;

  let newColuna, newStatus;
  if (newStage === 'convertido') {
    newColuna = lead.coluna_atual;
    newStatus = 'convertido';
  } else if (newStage === 'perdido') {
    newColuna = lead.coluna_atual;
    newStatus = 'perdido';
  } else {
    newColuna = newStage;
    newStatus = 'ativo';
  }

  if (newColuna === oldColuna && newStatus === oldStatus) return;

  // Optimistic update
  lead.coluna_atual = newColuna;
  lead.status = newStatus;
  if (newColuna !== oldColuna) lead.tentativas_dia_atual = 0;
  renderBoard();

  const patch = {
    coluna_atual: newColuna,
    status: newStatus,
    atualizado_em: new Date().toISOString(),
  };
  if (newColuna !== oldColuna) {
    patch.tentativas_dia_atual = 0;
    patch.entrou_coluna_em = new Date().toISOString();
  }

  const ok = await updateLead(lead.id, patch);
  if (!ok) {
    lead.coluna_atual = oldColuna;
    lead.status = oldStatus;
    renderBoard();
  } else {
    showToast(`Lead movido para ${STAGES.find(s => s.id === newStage)?.name || newStage}`);
  }
}

// ============================
// MODAL
// ============================
async function openModal(leadId) {
  currentLeadId = leadId;
  const lead = leads.find(l => l.id === leadId);
  if (!lead) return;

  modalTitle.textContent = lead.nome || 'Lead';

  const stage = STAGES.find(s => {
    if (lead.status === 'convertido') return s.id === 'convertido';
    if (lead.status === 'perdido') return s.id === 'perdido';
    return s.id === lead.coluna_atual;
  });
  modalStage.textContent = stage?.name || lead.coluna_atual;
  modalStage.className = 'modal-badge' + (lead.status === 'convertido' ? ' badge-won' : lead.status === 'perdido' ? ' badge-lost' : '');
  modalStage.style.display = 'inline-block';
  btnDelete.style.display = 'inline-flex';

  // Fill form fields
  modalBody.querySelectorAll('[data-field]').forEach(el => {
    const value = lead[el.dataset.field] || '';
    if (el.type === 'checkbox') el.checked = !!value;
    else if (el.tagName === 'SELECT') el.value = value;
    else el.value = value;
  });

  // Load async data
  renderInteracoes(leadId);
  renderComentarios(leadId);

  setActiveTab('principal');
  modalOverlay.classList.add('open');
}

async function renderInteracoes(leadId) {
  const el = document.getElementById('interacoesTimeline');
  if (!el) return;
  el.innerHTML = '<div class="loading-text">Carregando interacoes...</div>';

  const list = await loadInteracoes(leadId);
  if (!list.length) {
    el.innerHTML = '<div class="empty-text">Nenhuma interacao registrada ainda.</div>';
    return;
  }

  el.innerHTML = list.map(i => {
    const icon = i.tipo_acao === 'ligacao' ? 'tl-call' : i.tipo_acao === 'whatsapp' ? 'tl-wpp' : i.tipo_acao === 'email' ? 'tl-email' : 'tl-default';
    return `
    <div class="tl-item">
      <div class="tl-dot ${icon}"></div>
      <div class="tl-body">
        <div class="tl-head">
          <span class="tl-type">${esc(i.tipo_acao || '?')}</span>
          <span class="tl-date">${fmtDate(i.criado_em)}</span>
        </div>
        <div class="tl-detail">Dia ${i.dia_cadencia} &middot; ${esc(i.resultado_ligacao || 'sem resultado')}${i.duracao_segundos ? ` &middot; ${Math.floor(i.duracao_segundos/60)}m${String(i.duracao_segundos%60).padStart(2,'0')}s` : ''}</div>
        ${i.notas ? `<div class="tl-notes">${esc(i.notas)}</div>` : ''}
      </div>
    </div>`;
  }).join('');
}

async function renderComentarios(leadId) {
  const el = document.getElementById('comentariosList');
  if (!el) return;
  el.innerHTML = '<div class="loading-text">Carregando...</div>';

  const list = await loadComentarios(leadId);
  if (!list.length) {
    el.innerHTML = '<div class="empty-text">Nenhum comentario.</div>';
    return;
  }

  el.innerHTML = list.map(c => `
    <div class="cmt-item">
      <div class="cmt-head">
        <span class="cmt-author">${esc(c.autor)}</span>
        <span class="cmt-date">${fmtDate(c.criado_em)}</span>
      </div>
      <div class="cmt-text">${esc(c.texto)}</div>
    </div>
  `).join('');
}

function closeModal() {
  modalOverlay.classList.remove('open');
  currentLeadId = null;
}

async function saveModal() {
  if (!currentLeadId) return;

  const data = {};
  modalBody.querySelectorAll('[data-field]').forEach(el => {
    const field = el.dataset.field;
    if (el.type === 'checkbox') data[field] = el.checked;
    else data[field] = el.value || null;
  });
  data.atualizado_em = new Date().toISOString();

  const ok = await updateLead(currentLeadId, data);
  if (ok) {
    renderBoard();
    closeModal();
    showToast('Lead atualizado');
  }
}

async function handleAddComment() {
  if (!currentLeadId) return;
  const input = document.getElementById('comentarioInput');
  if (!input) return;
  const texto = input.value.trim();
  if (!texto) return;

  input.value = '';
  input.disabled = true;
  const result = await addComentario(currentLeadId, texto);
  input.disabled = false;
  if (result) {
    renderComentarios(currentLeadId);
    showToast('Comentario adicionado');
  }
}

function markLost() {
  if (!currentLeadId) return;
  if (!confirm('Marcar este lead como perdido?')) return;

  const lead = leads.find(l => l.id === currentLeadId);
  if (!lead) return;

  updateLead(currentLeadId, { status: 'perdido', atualizado_em: new Date().toISOString() }).then(ok => {
    if (ok) {
      lead.status = 'perdido';
      renderBoard();
      closeModal();
      showToast('Lead marcado como perdido');
    }
  });
}

// ============================
// TABS
// ============================
function setActiveTab(tabId) {
  modalTabs.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tabId));
  modalBody.querySelectorAll('.tab-content').forEach(tc => tc.classList.toggle('active', tc.dataset.tab === tabId));
}

modalTabs.addEventListener('click', e => {
  const tab = e.target.closest('.tab');
  if (tab) setActiveTab(tab.dataset.tab);
});

// ============================
// EVENT LISTENERS
// ============================
btnRefresh.addEventListener('click', () => { fetchLeads(); showToast('Atualizando...'); });
btnSave.addEventListener('click', saveModal);
btnCancel.addEventListener('click', closeModal);
btnClose.addEventListener('click', closeModal);
btnDelete.addEventListener('click', markLost);
modalOverlay.addEventListener('click', e => { if (e.target === modalOverlay) closeModal(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape' && modalOverlay.classList.contains('open')) closeModal(); });

document.addEventListener('click', e => {
  if (e.target.id === 'btnAddComment' || e.target.closest('#btnAddComment')) handleAddComment();
});

document.addEventListener('keydown', e => {
  if (e.target.id === 'comentarioInput' && e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    handleAddComment();
  }
});

// ============================
// UTILS
// ============================
function esc(str) {
  if (!str) return '';
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}

function fmtPhone(phone) {
  if (!phone) return '';
  const d = phone.replace(/\D/g, '');
  if (d.length === 13 && d.startsWith('55')) {
    return `(${d.slice(2,4)}) ${d.slice(4,9)}-${d.slice(9)}`;
  }
  if (d.length === 12 && d.startsWith('55')) {
    return `(${d.slice(2,4)}) ${d.slice(4,8)}-${d.slice(8)}`;
  }
  return phone;
}

function fmtDate(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  return d.toLocaleDateString('pt-BR') + ' ' + d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
}

function showToast(msg) {
  let t = document.querySelector('.toast');
  if (!t) { t = document.createElement('div'); t.className = 'toast'; document.body.appendChild(t); }
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(t._timer);
  t._timer = setTimeout(() => t.classList.remove('show'), 2500);
}

// ============================
// INIT
// ============================
fetchLeads();
