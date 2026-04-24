import json
import uuid

def uid():
    return str(uuid.uuid4())

# Credentials
SUPA_CRED = {"supabaseApi": {"id": "E124roxIkDjglv24", "name": "Supabase - [Com&Mkt]"}}
SUPA_RPC_CRED = {"httpHeaderAuth": {"id": "2KgWpUCUPtxUS89C", "name": "Supabase RPC - Service Role"}}
SHEETS_CRED = {"googleSheetsOAuth2Api": {"id": "OL50dab7dT1eN5gq", "name": "sheets_andre"}}
EVOLUTION_CRED = {"httpHeaderAuth": {"id": "4nttNefSqX8Fk0qT", "name": "Evolution API - WhatsApp"}}

SUPABASE_URL = "https://azmtxhjtqodtaeoshrye.supabase.co"
WEBHOOK_PATH = "anp-mapeamento"
ANP_CSV_URL = "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/arquivos-dados-cadastrais-dos-revendedores-varejistas-de-combustiveis-automotivos/dados-cadastrais-revendedores-varejistas-combustiveis-automoveis.csv"
SHEETS_ID = "1RfYvcQ_dF6n6jPnizharA6L1yzeLCy3J_iH8XcIo5RQ"
EVOLUTION_URL = "https://evolution-evolution.mzpvnn.easypanel.host/message/sendText/andre_grupos"
WPP_GROUP = "120363406760037910@g.us"

nodes = []

# ============================================================
# 1. Schedule Trigger - 9h-12h, 30min, seg-sex
# ============================================================
nodes.append({
    "parameters": {
        "rule": {
            "interval": [
                {
                    "field": "cronExpression",
                    "expression": "0,30 9-11 * * 1-5"
                }
            ]
        }
    },
    "type": "n8n-nodes-base.scheduleTrigger",
    "typeVersion": 1.2,
    "position": [0, 0],
    "id": uid(),
    "name": "Schedule 9h-12h"
})

# ============================================================
# 2. Webhook Trigger - manual do Vendemais
# ============================================================
webhook_id = uid()
nodes.append({
    "parameters": {
        "httpMethod": "POST",
        "path": WEBHOOK_PATH,
        "options": {}
    },
    "type": "n8n-nodes-base.webhook",
    "typeVersion": 2,
    "position": [0, 300],
    "id": uid(),
    "name": "Webhook Manual",
    "webhookId": webhook_id
})

# ============================================================
# 3. Is Updated Today? - IF (checked after Parse CSV)
# ============================================================
nodes.append({
    "parameters": {
        "conditions": {
            "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "loose", "version": 2},
            "conditions": [{
                "id": uid(),
                "leftValue": "={{ $json.shouldProcess }}",
                "rightValue": True,
                "operator": {"type": "boolean", "operation": "true", "singleValue": True}
            }],
            "combinator": "and"
        },
        "options": {}
    },
    "type": "n8n-nodes-base.if",
    "typeVersion": 2.2,
    "position": [820, 150],
    "id": uid(),
    "name": "Atualizado Hoje?"
})

# ============================================================
# 6. Log No Update (false branch, if hour >= 12)
# ============================================================
log_skip_code = r"""
const data = $('Parse & Classify CSV').first().json;
const hour = new Date().getHours() - 3; // BRT = UTC-3

if (hour < 12) {
    // Before noon - stop silently, will retry at next schedule
    return [{ json: { action: 'retry_later', hour, shouldLog: false } }];
}

// After noon - log sem_atualizacao
return [{ json: {
    data_execucao: new Date().toISOString().split('T')[0],
    hora_execucao: new Date().toTimeString().split(' ')[0],
    status: 'sem_atualizacao',
    anp_atualizado_em: data.maxDate || 'nao_encontrado',
    novos_postos: 0,
    trocas_bandeira: 0,
    postos_retirados: 0,
    notificacao_enviada: false,
    duracao_segundos: 0,
    shouldLog: true
}}];
"""

nodes.append({
    "parameters": {"jsCode": log_skip_code},
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [1080, 400],
    "id": uid(),
    "name": "Check If Should Log"
})

# 6b. Filter only logs that should be saved
nodes.append({
    "parameters": {
        "conditions": {
            "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "loose", "version": 2},
            "conditions": [{
                "id": uid(),
                "leftValue": "={{ $json.shouldLog }}",
                "rightValue": True,
                "operator": {"type": "boolean", "operation": "true", "singleValue": True}
            }],
            "combinator": "and"
        },
        "options": {}
    },
    "type": "n8n-nodes-base.if",
    "typeVersion": 2.2,
    "position": [1340, 400],
    "id": uid(),
    "name": "Should Log?"
})

# 6c. Insert log sem_atualizacao
nodes.append({
    "parameters": {
        "tableId": "vm_anp_execucoes",
        "fieldsUi": {
            "fieldValues": [
                {"fieldId": "status", "fieldValue": "={{ $json.status }}"},
                {"fieldId": "anp_atualizado_em", "fieldValue": "={{ $json.anp_atualizado_em }}"},
                {"fieldId": "novos_postos", "fieldValue": "=0"},
                {"fieldId": "trocas_bandeira", "fieldValue": "=0"},
                {"fieldId": "postos_retirados", "fieldValue": "=0"}
            ]
        }
    },
    "type": "n8n-nodes-base.supabase",
    "typeVersion": 1,
    "position": [1600, 340],
    "id": uid(),
    "name": "Log Sem Atualização",
    "credentials": SUPA_CRED
})

# ============================================================
# 7. Check Idempotency - query vm_anp_execucoes
# ============================================================
nodes.append({
    "parameters": {
        "operation": "getAll",
        "tableId": "vm_anp_execucoes",
        "returnAll": False,
        "limit": 1,
        "matchType": "allFilters",
        "filters": {
            "conditions": [
                {"keyName": "data_execucao", "condition": "eq", "keyValue": "={{ new Date().toISOString().split('T')[0] }}"},
                {"keyName": "status", "condition": "eq", "keyValue": "concluido"}
            ]
        }
    },
    "type": "n8n-nodes-base.supabase",
    "typeVersion": 1,
    "position": [1080, 0],
    "id": uid(),
    "name": "Check Idempotency",
    "credentials": SUPA_CRED,
    "alwaysOutputData": True
})

# ============================================================
# 8. Already Done? - IF
# ============================================================
nodes.append({
    "parameters": {
        "conditions": {
            "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "loose", "version": 2},
            "conditions": [{
                "id": uid(),
                "leftValue": "={{ $json.id }}",
                "rightValue": "",
                "operator": {"type": "string", "operation": "notExists"}
            }],
            "combinator": "and"
        },
        "options": {}
    },
    "type": "n8n-nodes-base.if",
    "typeVersion": 2.2,
    "position": [1340, 0],
    "id": uid(),
    "name": "Já Processou?"
})

# ============================================================
# 9. Download CSV
# ============================================================
nodes.append({
    "parameters": {
        "url": ANP_CSV_URL,
        "options": {
            "timeout": 120000
        }
    },
    "type": "n8n-nodes-base.httpRequest",
    "typeVersion": 4.2,
    "position": [1600, -60],
    "id": uid(),
    "name": "Download CSV",
    "retryOnFail": True,
    "maxTries": 3,
    "waitBetweenTries": 10000
})

# ============================================================
# 10. Parse & Classify CSV - Code
# ============================================================
parse_csv_code = r"""
const startTime = Date.now();
const raw = $input.first().json.data || $input.first().json.body || '';

// Parse CSV (separator ;)
const lines = raw.split('\n');
if (lines.length < 2) {
    throw new Error('CSV vazio ou inválido: ' + lines.length + ' linhas');
}

// Parse headers - handle BOM and quotes
let headerLine = lines[0].replace(/^\uFEFF/, '');
const headers = headerLine.split(';').map(h => h.trim().replace(/^"|"$/g, '').toUpperCase());

// Find column indices
const colMap = {};
const colNames = {
    'CNPJ': ['CNPJ DO REVENDA', 'CNPJ', 'CNPJ_REVENDA'],
    'RAZAO': ['RAZÃO SOCIAL', 'RAZAO SOCIAL', 'RAZAO_SOCIAL'],
    'FANTASIA': ['NOME FANTASIA', 'NOME_FANTASIA'],
    'BANDEIRA': ['BANDEIRA'],
    'ENDERECO': ['ENDEREÇO', 'ENDERECO'],
    'BAIRRO': ['BAIRRO'],
    'CEP': ['CEP'],
    'MUNICIPIO': ['MUNICÍPIO', 'MUNICIPIO'],
    'UF': ['ESTADO', 'UF'],
    'DATA_PUB': ['DATA DE PUBLICAÇÃO DPA', 'DATAPUBLICACAO', 'DATA PUBLICAÇÃO', 'DATA_PUBLICACAO'],
    'DATA_VINC': ['DATA DA VINCULAÇÃO BANDEIRA', 'DATAVINCULACAO', 'DATA VINCULAÇÃO', 'DATA_VINCULACAO']
};

for (const [key, variants] of Object.entries(colNames)) {
    for (const variant of variants) {
        const idx = headers.indexOf(variant);
        if (idx !== -1) {
            colMap[key] = idx;
            break;
        }
    }
}

// Helper: parse DD/MM/YYYY to Date object
function parseDate(str) {
    if (!str || !str.trim()) return null;
    const parts = str.trim().split('/');
    if (parts.length !== 3) return null;
    const d = parseInt(parts[0]), m = parseInt(parts[1]), y = parseInt(parts[2]);
    if (isNaN(d) || isNaN(m) || isNaN(y)) return null;
    return new Date(y, m - 1, d);
}

// Today in DD/MM/YYYY format
const now = new Date();
const today = `${String(now.getDate()).padStart(2, '0')}/${String(now.getMonth() + 1).padStart(2, '0')}/${now.getFullYear()}`;
const todayDate = new Date(now.getFullYear(), now.getMonth(), now.getDate());

const novos = [];
const trocas = [];
const allCnpjs = [];
let totalRows = 0;
let maxDateObj = null;
let maxDateStr = '';

for (let i = 1; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) continue;
    totalRows++;

    const values = line.split(';').map(v => v.trim().replace(/^"|"$/g, ''));

    const cnpjRaw = colMap.CNPJ !== undefined ? values[colMap.CNPJ] : '';
    const cnpjDigits = cnpjRaw.replace(/\D/g, '');
    if (!cnpjDigits || cnpjDigits.length !== 14) continue;

    allCnpjs.push(cnpjDigits);

    const dataPub = colMap.DATA_PUB !== undefined ? values[colMap.DATA_PUB] : '';
    const dataVinc = colMap.DATA_VINC !== undefined ? values[colMap.DATA_VINC] : '';

    // Track max date across both date columns
    for (const ds of [dataPub, dataVinc]) {
        const dt = parseDate(ds);
        if (dt && (!maxDateObj || dt > maxDateObj)) {
            maxDateObj = dt;
            maxDateStr = ds.trim();
        }
    }

    // Normalize dates for comparison (pad to DD/MM/YYYY)
    const normPub = dataPub ? dataPub.trim().split('/').map((p,i) => i < 2 ? p.padStart(2,'0') : p).join('/') : '';
    const normVinc = dataVinc ? dataVinc.trim().split('/').map((p,i) => i < 2 ? p.padStart(2,'0') : p).join('/') : '';

    // vm_anp convention: cnpj = formatted, cnpj2 = plain digits
    const cnpjFormatted = cnpjDigits.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/, '$1.$2.$3/$4-$5');

    const posto = {
        cnpj: cnpjFormatted,
        cnpj2: cnpjDigits,
        razao_social: colMap.RAZAO !== undefined ? values[colMap.RAZAO] : '',
        bandeira: colMap.BANDEIRA !== undefined ? values[colMap.BANDEIRA] : '',
        uf: colMap.UF !== undefined ? values[colMap.UF] : '',
        cidade: colMap.MUNICIPIO !== undefined ? values[colMap.MUNICIPIO] : '',
        endereco: colMap.ENDERECO !== undefined ? values[colMap.ENDERECO] : '',
        bairro: colMap.BAIRRO !== undefined ? values[colMap.BAIRRO] : '',
        cep: colMap.CEP !== undefined ? values[colMap.CEP].replace(/\D/g, '') : '',
    };

    if (normPub === today) {
        novos.push(posto);
    } else if (normVinc === today) {
        trocas.push({ ...posto, bandeira_nova: posto.bandeira });
    }
}

// Check if max date in CSV = today
const maxDateNorm = maxDateObj
    ? `${String(maxDateObj.getDate()).padStart(2,'0')}/${String(maxDateObj.getMonth()+1).padStart(2,'0')}/${maxDateObj.getFullYear()}`
    : 'nenhuma';
const isUpdatedToday = maxDateObj && maxDateObj.getTime() === todayDate.getTime();

const elapsed = Math.round((Date.now() - startTime) / 1000);

return [{
    json: {
        novos,
        trocas,
        allCnpjs,
        totalRows,
        totalCnpjs: allCnpjs.length,
        novosCount: novos.length,
        trocasCount: trocas.length,
        today,
        maxDate: maxDateNorm,
        maxDateRaw: maxDateStr,
        shouldProcess: isUpdatedToday,
        colMap,
        parseTime: elapsed
    }
}];
"""

nodes.append({
    "parameters": {"jsCode": parse_csv_code},
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [1900, -60],
    "id": uid(),
    "name": "Parse & Classify CSV"
})

# ============================================================
# 11. Get current ANP records (cnpj + bandeira)
# ============================================================
nodes.append({
    "parameters": {
        "operation": "getAll",
        "tableId": "vm_anp",
        "returnAll": True
    },
    "type": "n8n-nodes-base.supabase",
    "typeVersion": 1,
    "position": [2200, -60],
    "id": uid(),
    "name": "Get ANP Records",
    "credentials": SUPA_CRED
})

# ============================================================
# 12. Detect Removals & Prepare Changes - Code
# ============================================================
detect_code = r"""
const startTime = Date.now();
const anpRecords = $input.all().map(item => item.json);
const parsed = $('Parse & Classify CSV').first().json;

const csvCnpjSet = new Set(parsed.allCnpjs);

// vm_anp uses: cnpj = formatted (XX.XXX.XXX/XXXX-XX), cnpj2 = plain digits
// CSV uses plain digits. Compare via cnpj2.
const retirados = anpRecords
    .filter(r => r.cnpj2 && !csvCnpjSet.has(r.cnpj2))
    .map(r => ({
        cnpj: r.cnpj || '',
        cnpj2: r.cnpj2 || '',
        razao_social: r.razao_social || '',
        bandeira: r.bandeira || '',
        uf: r.uf || '',
        cidade: r.cidade || ''
    }));

// Add old bandeira to trocas (keyed by plain digits = cnpj2)
const anpMap = new Map(anpRecords.map(r => [r.cnpj2, r]));
const trocas = parsed.trocas.map(t => {
    const current = anpMap.get(t.cnpj2);  // t.cnpj2 = plain digits = vm_anp.cnpj2
    return {
        ...t,
        bandeira_antiga: current ? current.bandeira : 'DESCONHECIDA',
        bandeira_nova: t.bandeira_nova || t.bandeira
    };
}).filter(t => t.bandeira_antiga !== t.bandeira_nova);

const elapsed = Math.round((Date.now() - startTime) / 1000);

return [{
    json: {
        p_trocas: JSON.stringify(trocas),
        p_novos: JSON.stringify(parsed.novos),
        p_retirados: JSON.stringify(retirados),
        summary: {
            trocas: trocas.length,
            novos: parsed.novos.length,
            retirados: retirados.length,
            total_csv: parsed.totalCnpjs,
            total_anp: anpRecords.length
        },
        detectTime: elapsed
    }
}];
"""

nodes.append({
    "parameters": {"jsCode": detect_code},
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [2500, -60],
    "id": uid(),
    "name": "Detect & Prepare"
})

# ============================================================
# 13. Execute Changes via RPC (fn_process_anp_changes)
# ============================================================
nodes.append({
    "parameters": {
        "method": "POST",
        "url": f"{SUPABASE_URL}/rest/v1/rpc/fn_process_anp_changes",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "supabaseApi",
        "sendHeaders": True,
        "headerParameters": {
            "parameters": [
                {"name": "Content-Type", "value": "application/json"}
            ]
        },
        "sendBody": True,
        "specifyBody": "json",
        "jsonBody": '={\n  "p_trocas": {{ $json.p_trocas }},\n  "p_novos": {{ $json.p_novos }},\n  "p_retirados": {{ $json.p_retirados }}\n}',
        "options": {"timeout": 300000}
    },
    "type": "n8n-nodes-base.httpRequest",
    "typeVersion": 4.2,
    "position": [2800, -60],
    "id": uid(),
    "name": "Execute Changes (RPC)",
    "credentials": SUPA_CRED,
    "retryOnFail": True,
    "maxTries": 2,
    "waitBetweenTries": 5000
})

# ============================================================
# 14. Refresh Materialized View (RPC)
# ============================================================
nodes.append({
    "parameters": {
        "method": "POST",
        "url": f"{SUPABASE_URL}/rest/v1/rpc/fn_refresh_mv_postos_socios",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "supabaseApi",
        "sendHeaders": True,
        "headerParameters": {
            "parameters": [
                {"name": "Content-Type", "value": "application/json"}
            ]
        },
        "sendBody": True,
        "specifyBody": "json",
        "jsonBody": "={}",
        "options": {"timeout": 120000}
    },
    "type": "n8n-nodes-base.httpRequest",
    "typeVersion": 4.2,
    "position": [3100, -60],
    "id": uid(),
    "name": "Refresh MV Postos Socios",
    "credentials": SUPA_CRED
})

# ============================================================
# 15. Query Prospects - Get from mv_postos_socios for changed CNPJs
# ============================================================
query_prospects_code = r"""
const summary = $('Detect & Prepare').first().json.summary;
const trocas = JSON.parse($('Detect & Prepare').first().json.p_trocas);
const novos = JSON.parse($('Detect & Prepare').first().json.p_novos);

const today = new Date().toISOString().split('T')[0];
const hasChanges = summary.novos > 0 || summary.trocas > 0 || summary.retirados > 0;

// Build RPC calls to get prospects (socios) from mv_postos_socios, filtered by vm_telefones
const rpcCalls = [];
const listsToCreate = [];

if (trocas.length > 0) {
    rpcCalls.push({
        p_cnpjs: trocas.map(t => t.cnpj2),
        p_nome_lista: `alteracao-anp-${today}`,
        tipo: 'troca_bandeira',
        qtd_cnpjs: trocas.length
    });
}

if (novos.length > 0) {
    rpcCalls.push({
        p_cnpjs: novos.map(n => n.cnpj2),
        p_nome_lista: `novo-posto-${today}`,
        tipo: 'novo_posto',
        qtd_cnpjs: novos.length
    });
}

// Build WhatsApp notification message
const wppMessage = hasChanges
    ? `🏪 *Mapeamento ANP - ${today}*\n\n` +
      `📊 Resumo:\n` +
      `• ${summary.novos} novo(s) posto(s)\n` +
      `• ${summary.trocas} troca(s) de bandeira\n` +
      `• ${summary.retirados} posto(s) retirado(s)\n\n` +
      `📋 Total base: ${summary.total_csv} postos`
    : `🏪 *Mapeamento ANP - ${today}*\n\n✅ Sem alterações detectadas hoje.`;

return [{
    json: {
        rpcCalls,
        summary,
        wppMessage,
        hasChanges,
        today
    }
}];
"""

nodes.append({
    "parameters": {"jsCode": query_prospects_code},
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [3400, -60],
    "id": uid(),
    "name": "Prepare Prospects & Lists"
})

# ============================================================
# 16. Has Sheets Rows? - IF
# ============================================================
nodes.append({
    "parameters": {
        "conditions": {
            "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "loose", "version": 2},
            "conditions": [{
                "id": uid(),
                "leftValue": "={{ $json.rpcCalls.length }}",
                "rightValue": "0",
                "operator": {"type": "number", "operation": "gt"}
            }],
            "combinator": "and"
        },
        "options": {}
    },
    "type": "n8n-nodes-base.if",
    "typeVersion": 2.2,
    "position": [3700, -60],
    "id": uid(),
    "name": "Has Sheets Data?"
})

# ============================================================
# 17. Prepare Sheets Items - Code (split array to individual items)
# ============================================================
# 17. Fetch Prospects via RPC (socios from mv_postos_socios, filtered by vm_telefones)
# ============================================================
fetch_prospects_code = r"""
const data = $('Prepare Prospects & Lists').first().json;
const results = [];

for (const call of data.rpcCalls) {
    // Call fn_get_prospects_for_cnpjs via Supabase REST
    const resp = await this.helpers.httpRequest({
        method: 'POST',
        url: '""" + SUPABASE_URL + r"""/rest/v1/rpc/fn_get_prospects_for_cnpjs',
        headers: {
            'Content-Type': 'application/json',
            'apikey': '""" + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF6bXR4aGp0cW9kdGFlb3NocnllIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTI4NTM1ODUsImV4cCI6MjAyODQyOTU4NX0.KvQovDvmATwBPc50oqnY_yJqjqoywZdSXm_bz5qn4V0" + r"""',
            'Authorization': 'Bearer """ + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF6bXR4aGp0cW9kdGFlb3NocnllIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTI4NTM1ODUsImV4cCI6MjAyODQyOTU4NX0.KvQovDvmATwBPc50oqnY_yJqjqoywZdSXm_bz5qn4V0" + r"""'
        },
        body: {
            p_cnpjs: call.p_cnpjs,
            p_nome_lista: call.p_nome_lista
        },
        json: true
    });

    const prospects = Array.isArray(resp) ? resp : [];
    results.push(...prospects);

    // Also push list metadata
    data.rpcCalls.find(c => c.p_nome_lista === call.p_nome_lista)._qtd_cpfs = prospects.length;
}

return [{ json: { prospects: results, rpcCalls: data.rpcCalls, summary: data.summary } }];
"""

nodes.append({
    "parameters": {"jsCode": fetch_prospects_code},
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [3960, -120],
    "id": uid(),
    "name": "Fetch Prospects (RPC)"
})

# ============================================================
# 17b. Prepare Sheets Items - split prospects into individual items
# ============================================================
prepare_sheets_code = r"""
const data = $input.first().json;
if (!data.prospects || data.prospects.length === 0) return [];
return data.prospects.map(p => ({ json: { nome: p.nome, cpf: p.cpf, nome_lista: p.nome_lista } }));
"""

nodes.append({
    "parameters": {"jsCode": prepare_sheets_code},
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [4240, -180],
    "id": uid(),
    "name": "Prepare Sheets Items"
})

# ============================================================
# 18. Write to Google Sheets
# ============================================================
nodes.append({
    "parameters": {
        "operation": "append",
        "documentId": {
            "__rl": True,
            "value": f"https://docs.google.com/spreadsheets/d/{SHEETS_ID}/edit",
            "mode": "url"
        },
        "sheetName": {
            "__rl": True,
            "value": 0,
            "mode": "list",
            "cachedResultName": "Sheet1",
            "cachedResultUrl": f"https://docs.google.com/spreadsheets/d/{SHEETS_ID}/edit#gid=0"
        },
        "columns": {
            "mappingMode": "autoMapInputData",
            "value": {}
        },
        "options": {}
    },
    "type": "n8n-nodes-base.googleSheets",
    "typeVersion": 4.5,
    "position": [4520, -180],
    "id": uid(),
    "name": "Write Sheets",
    "credentials": SHEETS_CRED
})

# ============================================================
# 19. Register Lists in Supabase
# ============================================================
register_lists_code = r"""
const data = $('Fetch Prospects (RPC)').first().json;
return data.rpcCalls.map(call => ({
    json: {
        nome_lista: call.p_nome_lista,
        tipo: call.tipo,
        qtd_cnpjs: call.qtd_cnpjs,
        qtd_cpfs: call._qtd_cpfs || 0,
        status: 'pendente',
        sheets_url: 'https://docs.google.com/spreadsheets/d/1RfYvcQ_dF6n6jPnizharA6L1yzeLCy3J_iH8XcIo5RQ',
        resumo: JSON.stringify(data.summary)
    }
}));
"""

nodes.append({
    "parameters": {"jsCode": register_lists_code},
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [4240, 200],
    "id": uid(),
    "name": "Prepare List Records"
})

# ============================================================
# 20. Insert vm_listas_anp
# ============================================================
nodes.append({
    "parameters": {
        "tableId": "vm_listas_anp",
        "dataToSend": "autoMapInputData"
    },
    "type": "n8n-nodes-base.supabase",
    "typeVersion": 1,
    "position": [4300, 200],
    "id": uid(),
    "name": "Insert Listas ANP",
    "credentials": SUPA_CRED
})

# ============================================================
# 21. Merge paths - NoOp to converge Sheets and No-Sheets paths
# ============================================================
nodes.append({
    "parameters": {},
    "type": "n8n-nodes-base.noOp",
    "typeVersion": 1,
    "position": [4560, -60],
    "id": uid(),
    "name": "Converge"
})

# ============================================================
# 22. Log Execution in vm_anp_execucoes
# ============================================================
log_exec_code = r"""
const data = $('Prepare Prospects & Lists').first().json;
const startStr = $('Parse & Classify CSV').first().json.parseTime || 0;
const detectStr = $('Detect & Prepare').first().json.detectTime || 0;

return [{
    json: {
        status: 'concluido',
        anp_atualizado_em: data.today,
        novos_postos: data.summary.novos,
        trocas_bandeira: data.summary.trocas,
        postos_retirados: data.summary.retirados,
        notificacao_enviada: false,
        duracao_segundos: startStr + detectStr + 10
    }
}];
"""

nodes.append({
    "parameters": {"jsCode": log_exec_code},
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [4800, -60],
    "id": uid(),
    "name": "Prepare Exec Log"
})

# ============================================================
# 23. Insert vm_anp_execucoes
# ============================================================
nodes.append({
    "parameters": {
        "tableId": "vm_anp_execucoes",
        "dataToSend": "autoMapInputData"
    },
    "type": "n8n-nodes-base.supabase",
    "typeVersion": 1,
    "position": [5080, -60],
    "id": uid(),
    "name": "Insert Exec Log",
    "credentials": SUPA_CRED
})

# ============================================================
# 24a. Prepare WhatsApp Payload
# ============================================================
wpp_payload_code = r"""
const msg = $('Prepare Prospects & Lists').first().json.wppMessage;
return [{ json: { number: '""" + WPP_GROUP + r"""', text: msg } }];
"""

nodes.append({
    "parameters": {"jsCode": wpp_payload_code},
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [5300, -60],
    "id": uid(),
    "name": "Prepare WPP Payload"
})

# ============================================================
# 24b. Send WhatsApp Notification
# ============================================================
nodes.append({
    "parameters": {
        "method": "POST",
        "url": EVOLUTION_URL,
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "sendBody": True,
        "specifyBody": "json",
        "jsonBody": '={"number": "{{ $json.number }}", "text": "{{ $json.text }}"}',
        "options": {"timeout": 30000}
    },
    "type": "n8n-nodes-base.httpRequest",
    "typeVersion": 4.2,
    "position": [5560, -60],
    "id": uid(),
    "name": "Send WhatsApp",
    "credentials": EVOLUTION_CRED,
    "onError": "continueRegularOutput"
})

# ============================================================
# 25. Mark Notified
# ============================================================
nodes.append({
    "parameters": {
        "operation": "update",
        "tableId": "vm_anp_execucoes",
        "filters": {
            "conditions": [
                {"keyName": "id", "condition": "eq", "keyValue": "={{ $('Insert Exec Log').first().json.id }}"}
            ]
        },
        "fieldsUi": {
            "fieldValues": [
                {"fieldId": "notificacao_enviada", "fieldValue": "=true"}
            ]
        }
    },
    "type": "n8n-nodes-base.supabase",
    "typeVersion": 1,
    "position": [5640, -60],
    "id": uid(),
    "name": "Mark Notified",
    "credentials": SUPA_CRED
})

# ============================================================
# CONNECTIONS
# ============================================================
connections = {
    # Both triggers → Idempotency check first
    "Schedule 9h-12h": {
        "main": [[{"node": "Check Idempotency", "type": "main", "index": 0}]]
    },
    "Webhook Manual": {
        "main": [[{"node": "Check Idempotency", "type": "main", "index": 0}]]
    },
    "Check Idempotency": {
        "main": [[{"node": "Já Processou?", "type": "main", "index": 0}]]
    },
    "Já Processou?": {
        "main": [
            # TRUE (count == 0, NOT yet processed) → Download CSV
            [{"node": "Download CSV", "type": "main", "index": 0}],
            # FALSE (already processed) → stop
            []
        ]
    },
    "Download CSV": {
        "main": [[{"node": "Parse & Classify CSV", "type": "main", "index": 0}]]
    },
    "Parse & Classify CSV": {
        "main": [[{"node": "Atualizado Hoje?", "type": "main", "index": 0}]]
    },
    "Atualizado Hoje?": {
        "main": [
            # TRUE → continue processing
            [{"node": "Get ANP Records", "type": "main", "index": 0}],
            # FALSE → check if should log or retry
            [{"node": "Check If Should Log", "type": "main", "index": 0}]
        ]
    },
    "Check If Should Log": {
        "main": [[{"node": "Should Log?", "type": "main", "index": 0}]]
    },
    "Should Log?": {
        "main": [
            # TRUE → Log
            [{"node": "Log Sem Atualização", "type": "main", "index": 0}],
            # FALSE → stop (retry later)
            []
        ]
    },
    "Get ANP Records": {
        "main": [[{"node": "Detect & Prepare", "type": "main", "index": 0}]]
    },
    "Detect & Prepare": {
        "main": [[{"node": "Execute Changes (RPC)", "type": "main", "index": 0}]]
    },
    "Execute Changes (RPC)": {
        "main": [[{"node": "Refresh MV Postos Socios", "type": "main", "index": 0}]]
    },
    "Refresh MV Postos Socios": {
        "main": [[{"node": "Prepare Prospects & Lists", "type": "main", "index": 0}]]
    },
    "Prepare Prospects & Lists": {
        "main": [[{"node": "Has Sheets Data?", "type": "main", "index": 0}]]
    },
    "Has Sheets Data?": {
        "main": [
            # TRUE → Fetch prospects then write
            [{"node": "Fetch Prospects (RPC)", "type": "main", "index": 0}],
            # FALSE → Skip to Converge
            [{"node": "Converge", "type": "main", "index": 0}]
        ]
    },
    "Fetch Prospects (RPC)": {
        "main": [[
            {"node": "Prepare Sheets Items", "type": "main", "index": 0},
            {"node": "Prepare List Records", "type": "main", "index": 0}
        ]]
    },
    "Prepare Sheets Items": {
        "main": [[{"node": "Write Sheets", "type": "main", "index": 0}]]
    },
    "Write Sheets": {
        "main": [[{"node": "Converge", "type": "main", "index": 0}]]
    },
    "Prepare List Records": {
        "main": [[{"node": "Insert Listas ANP", "type": "main", "index": 0}]]
    },
    "Insert Listas ANP": {
        "main": [[{"node": "Converge", "type": "main", "index": 0}]]
    },
    "Converge": {
        "main": [[{"node": "Prepare Exec Log", "type": "main", "index": 0}]]
    },
    "Prepare Exec Log": {
        "main": [[{"node": "Insert Exec Log", "type": "main", "index": 0}]]
    },
    "Insert Exec Log": {
        "main": [[{"node": "Prepare WPP Payload", "type": "main", "index": 0}]]
    },
    "Prepare WPP Payload": {
        "main": [[{"node": "Send WhatsApp", "type": "main", "index": 0}]]
    },
    "Send WhatsApp": {
        "main": [[{"node": "Mark Notified", "type": "main", "index": 0}]]
    }
}

# ============================================================
# WORKFLOW
# ============================================================
workflow = {
    "name": "[MKTCOM] mapeamento-anp",
    "nodes": nodes,
    "connections": connections,
    "settings": {
        "executionOrder": "v1"
    }
}

output_path = r"C:\Users\ClubPetro-123\Documents\cmo_cp\workflow_anp.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(workflow, f, indent=2, ensure_ascii=False)

print(f"Workflow JSON salvo em {output_path}")
print(f"Total de nodes: {len(nodes)}")
print(f"Connections: {len(connections)} sources")
