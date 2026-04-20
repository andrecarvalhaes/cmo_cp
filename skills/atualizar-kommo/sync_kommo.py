#!/usr/bin/env python3
"""
sync_kommo.py — Exporta leads do Kommo e atualiza aux_kommo no Supabase.
Dois comandos:
  extract  — busca todos os leads + contatos do Kommo, salva JSON
  load     — lê JSON e insere no Supabase via PostgREST
"""

import json, sys, time, argparse
import urllib.request, urllib.error, urllib.parse
from datetime import datetime

KOMMO_BASE = "https://clubpetro.kommo.com/api/v4"
RATE_DELAY = 0.34          # ~3 req/s
PAGE_SIZE = 250
DATA_FILE = "kommo_export.json"

# ── Mapeamento telefone (enum_code Kommo → coluna aux_kommo) ──
PHONE_COL = {
    "WORK":   "Telefone comercial",
    "WORKDD": "Tel. direto com.",
    "MOB":    "Celular",
    "FAX":    "Faz",
    "HOME":   "Telefone residencial",
    "OTHER":  "Outro telefone",
}

# ── Mapeamento email ──
EMAIL_COL = {
    "WORK":  "Email comercial",
    "PRIV":  "Email pessoal",
    "OTHER": "Outro email",
}


# ═══════════════════════════════════════════════════════════════
#  Helpers HTTP
# ═══════════════════════════════════════════════════════════════

def api_get(url, token, retries=3):
    """GET com retry para 429."""
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                if resp.status == 204:
                    return None
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 204:
                return None
            if e.code == 429 and attempt < retries - 1:
                wait = 3 * (attempt + 1)
                print(f"\n  429 Rate limited — aguardando {wait}s...")
                time.sleep(wait)
                continue
            body = e.read().decode("utf-8", errors="replace")[:300]
            print(f"\n  HTTP {e.code}: {body}")
            raise
        except Exception as e:
            if attempt < retries - 1:
                print(f"\n  Erro de rede ({e}), retry em 3s...")
                time.sleep(3)
                continue
            raise
    return None


def fetch_pages(path, token, params=None, embed_key="leads"):
    """Pagina um endpoint Kommo retornando todos os itens."""
    items = []
    page = 1
    while True:
        parts = [f"limit={PAGE_SIZE}", f"page={page}"]
        for k, v in (params or {}).items():
            parts.append(f"{k}={urllib.parse.quote(str(v))}")
        url = f"{KOMMO_BASE}/{path}?{'&'.join(parts)}"

        data = api_get(url, token)
        if not data or "_embedded" not in data:
            break

        batch = data["_embedded"].get(embed_key, [])
        if not batch:
            break

        items.extend(batch)
        sys.stdout.write(f"\r  p.{page} — {len(items)} registros")
        sys.stdout.flush()

        if "next" not in data.get("_links", {}):
            break

        page += 1
        time.sleep(RATE_DELAY)

    print()
    return items


# ═══════════════════════════════════════════════════════════════
#  Transformacao
# ═══════════════════════════════════════════════════════════════

def ts_fmt(ts):
    """Unix timestamp → DD.MM.YYYY HH:MM:SS."""
    if not ts:
        return None
    try:
        return datetime.fromtimestamp(int(ts)).strftime("%d.%m.%Y %H:%M:%S")
    except (ValueError, OSError):
        return str(ts)


def flatten_lead(lead, users, pipes, statuses, contacts_db, valid_cols):
    """Achata um lead do Kommo em dict {coluna: valor} conforme aux_kommo."""
    r = {}

    # ── Core fields (nomes com acento conforme BD) ──
    r["ID"] = str(lead["id"])
    r["Lead título"] = lead.get("name") or ""
    r["Lead venda R$"] = str(lead.get("price", 0))
    r["Usuário responsável"] = users.get(lead.get("responsible_user_id"), "")
    r["Criado em"] = ts_fmt(lead.get("created_at"))
    r["Criado por"] = users.get(lead.get("created_by"), "")
    r["modificada em"] = ts_fmt(lead.get("updated_at"))
    r["Modificado por"] = users.get(lead.get("updated_by"), "")
    closed = lead.get("closed_at")
    r["Fechado às"] = ts_fmt(closed) if closed else "nao fechado"
    r["Etapa do lead"] = statuses.get(lead.get("status_id"), "")
    r["Funil de vendas"] = pipes.get(lead.get("pipeline_id"), "")

    # ── Tags ──
    tags = lead.get("_embedded", {}).get("tags", [])
    if tags:
        r["Tags"] = ", ".join(t.get("name", "") for t in tags)

    # ── Loss reason (nativo do Kommo) ──
    lr = lead.get("_embedded", {}).get("loss_reason", [])
    if lr and "Motivo de perda" in valid_cols:
        r["Motivo de perda"] = lr[0].get("name", "")

    # ── Custom fields do lead ──
    for cf in lead.get("custom_fields_values") or []:
        fn = cf.get("field_name", "")
        if not fn or fn not in valid_cols:
            continue
        vals = cf.get("values", [])
        if not vals:
            continue
        ft = cf.get("field_type", "")

        if ft == "checkbox":
            v = "Sim" if vals[0].get("value") else "Nao"
        elif ft in ("multiselect", "multitext"):
            v = ", ".join(str(x.get("value", "")) for x in vals)
        elif ft in ("date", "date_time"):
            raw = vals[0].get("value")
            v = ts_fmt(raw) if isinstance(raw, (int, float)) else str(raw or "")
        else:
            v = str(vals[0].get("value", ""))

        if v:
            r[fn] = v

    # ── Company ──
    comps = lead.get("_embedded", {}).get("companies", [])
    if comps:
        cn = comps[0].get("name", "")
        for col in ("Contato da empresa", "Empresa lead 's"):
            if col in valid_cols:
                r[col] = cn

    # ── Contato principal ──
    lc = lead.get("_embedded", {}).get("contacts", [])
    if lc:
        cid = lc[0].get("id")
        contact = contacts_db.get(cid)
        if contact:
            if "Nome completo" in valid_cols:
                r["Nome completo"] = contact.get("name", "")
            if "Pessoa de contato" in valid_cols:
                r["Pessoa de contato"] = contact.get("name", "")

            for ccf in contact.get("custom_fields_values") or []:
                fc = ccf.get("field_code", "")
                cfn = ccf.get("field_name", "")
                vs = ccf.get("values", [])

                if fc == "PHONE":
                    for v in vs:
                        ec = v.get("enum_code", "OTHER")
                        col = PHONE_COL.get(ec)
                        if col and col in valid_cols and col not in r:
                            r[col] = str(v.get("value", ""))
                elif fc == "EMAIL":
                    for v in vs:
                        ec = v.get("enum_code", "OTHER")
                        col = EMAIL_COL.get(ec)
                        if col and col in valid_cols and col not in r:
                            r[col] = str(v.get("value", ""))
                elif fc == "POSITION":
                    if vs and "Cargo" in valid_cols:
                        r["Cargo"] = str(vs[0].get("value", ""))
                else:
                    # Outros custom fields do contato
                    if cfn and cfn in valid_cols and cfn not in r and vs:
                        r[cfn] = str(vs[0].get("value", ""))

    # Filtra apenas colunas validas
    return {k: v for k, v in r.items() if k in valid_cols and v is not None}


# ═══════════════════════════════════════════════════════════════
#  Comando: extract
# ═══════════════════════════════════════════════════════════════

def cmd_extract(args):
    valid_cols = set(json.load(open(args.columns, encoding="utf-8")))
    token = args.token
    t0 = time.time()

    # 1. Referencia
    print("1/4  Dados de referencia...")
    ud = api_get(f"{KOMMO_BASE}/users?limit=250", token)
    users = {}
    if ud and "_embedded" in ud:
        for u in ud["_embedded"].get("users", []):
            users[u["id"]] = u.get("name", "")
    print(f"     {len(users)} usuarios")

    pd = api_get(f"{KOMMO_BASE}/leads/pipelines", token)
    pipes, statuses = {}, {}
    if pd and "_embedded" in pd:
        for p in pd["_embedded"].get("pipelines", []):
            pipes[p["id"]] = p.get("name", "")
            for s in p.get("_embedded", {}).get("statuses", []):
                statuses[s["id"]] = s.get("name", "")
    print(f"     {len(pipes)} pipelines, {len(statuses)} estagios")
    time.sleep(RATE_DELAY)

    # 2. Leads (pipeline Fidelidade = 8166623)
    print("2/4  Leads (Pipe | Fidelidade)...")
    leads = fetch_pages("leads", token,
                        {"with": "contacts,loss_reason,companies",
                         "filter[pipeline_id][]": "8166623"},
                        "leads")
    print(f"     Total: {len(leads)}")

    # 3. Contatos
    print("3/4  Contatos...")
    contacts_list = fetch_pages("contacts", token, {}, "contacts")
    contacts_db = {c["id"]: c for c in contacts_list}
    print(f"     Total: {len(contacts_db)}")

    # 4. Flatten
    print("4/4  Processando...")
    rows = []
    for i, lead in enumerate(leads):
        rows.append(flatten_lead(lead, users, pipes, statuses, contacts_db, valid_cols))
        if (i + 1) % 2000 == 0:
            print(f"     {i+1}/{len(leads)}")

    output = args.output
    with open(output, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False)

    elapsed = time.time() - t0
    print(f"\nExtract concluido em {elapsed:.0f}s")
    print(f"  {len(rows)} leads salvos em {output}")
    print(f"  Colunas preenchidas (amostra lead 1): {len(rows[0]) if rows else 0}")


# ═══════════════════════════════════════════════════════════════
#  Comando: load
# ═══════════════════════════════════════════════════════════════

def cmd_load(args):
    rows = json.load(open(args.input, encoding="utf-8"))
    print(f"Lendo {len(rows)} leads de {args.input}")

    base_url = args.supabase_url.rstrip("/")
    key = args.supabase_key
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    }

    batch_size = 200
    total_batches = (len(rows) - 1) // batch_size + 1
    errors = 0
    t0 = time.time()

    for i in range(0, len(rows), batch_size):
        batch = rows[i : i + batch_size]
        # Normalizar: todas as linhas do batch devem ter as mesmas chaves
        all_keys = set()
        for row in batch:
            all_keys.update(row.keys())
        batch = [{k: row.get(k) for k in all_keys} for row in batch]
        body = json.dumps(batch, ensure_ascii=False).encode("utf-8")
        url = f"{base_url}/rest/v1/aux_kommo"
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                pass
        except urllib.error.HTTPError as e:
            errors += 1
            msg = e.read().decode("utf-8", errors="replace")[:300]
            print(f"\n  ERRO batch {i//batch_size+1}: HTTP {e.code} — {msg}")

        bn = i // batch_size + 1
        sys.stdout.write(f"\r  Batch {bn}/{total_batches}")
        sys.stdout.flush()
        time.sleep(0.3)

    elapsed = time.time() - t0
    print(f"\n\nLoad concluido em {elapsed:.0f}s")
    print(f"  {len(rows)} leads inseridos, {errors} erros")


# ═══════════════════════════════════════════════════════════════
#  Main
# ═══════════════════════════════════════════════════════════════

def main():
    p = argparse.ArgumentParser(description="Sync Kommo → aux_kommo (Supabase)")
    sub = p.add_subparsers(dest="cmd")

    ex = sub.add_parser("extract", help="Exporta leads do Kommo para JSON")
    ex.add_argument("--token", required=True, help="Kommo access token")
    ex.add_argument("--columns", required=True, help="JSON com lista de colunas validas")
    ex.add_argument("--output", default=DATA_FILE, help="Arquivo de saida")

    lo = sub.add_parser("load", help="Carrega JSON no Supabase")
    lo.add_argument("--input", default=DATA_FILE, help="Arquivo de entrada")
    lo.add_argument("--supabase-url", required=True, help="URL do projeto Supabase")
    lo.add_argument("--supabase-key", required=True, help="Service role key")

    args = p.parse_args()
    if args.cmd == "extract":
        cmd_extract(args)
    elif args.cmd == "load":
        cmd_load(args)
    else:
        p.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
