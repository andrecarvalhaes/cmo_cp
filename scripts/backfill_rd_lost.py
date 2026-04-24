"""Backfill: desmarcar oportunidade no RD Station para todos os leads perdidos no Kommo desde Jul/2025"""
import json, urllib.request, urllib.parse, sys, time

sys.stdout.reconfigure(encoding='utf-8')

KOMMO_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjA5MzIyM2VmODJjZjIzYWE4MWQ5MmI3YmU0M2FkMDlkOWYwMjI1YmM4NGU5N2JlMWEyMjgxZTRmNzNlYmNmYjE4MTQ4YTM2ZmZmYmY5OTRlIn0.eyJhdWQiOiIxZjczY2E0NS05MmI5LTQ1MGQtOWY0ZS0xYjdlNzdmMjBlZjgiLCJqdGkiOiIwOTMyMjNlZjgyY2YyM2FhODFkOTJiN2JlNDNhZDA5ZDlmMDIyNWJjODRlOTdiZTFhMjI4MWU0ZjczZWJjZmIxODE0OGEzNmZmZmJmOTk0ZSIsImlhdCI6MTc3NDU0ODg5OCwibmJmIjoxNzc0NTQ4ODk4LCJleHAiOjE4NjE4MzM2MDAsInN1YiI6IjEwNjU1NzUxIiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMxOTgyNDYzLCJiYXNlX2RvbWFpbiI6ImtvbW1vLmNvbSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJwdXNoX25vdGlmaWNhdGlvbnMiLCJmaWxlcyIsImNybSIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiZGYxZWM3ZTEtYTU4My00NjJlLWE5NzktMzM5M2FiMmMyNTA4IiwiYXBpX2RvbWFpbiI6ImFwaS1jLmtvbW1vLmNvbSJ9.k_5DU6Of3PLfSqFG8zxIbGKfwd9ubpM0G5V9BALICK79laSKDHc7f_VVlacf-h6M2xrAu80f0ZGZA2xvMrByaaCa1VC5v5uRkdd5oTLOmxxHOygxmD_BuRX-UGVYuoCw6zet4qyw2p8YZeFMEF4URpyUHFvklz7pS3GmMAOREQnNn-LF0Q9-xHDCrlIelnYarGqCbeU5PWFCMDFfH_ITxLGf89il3I7IR0MIFkBn4-rx5ekQjxEbPgxVBI9e_wtZjTXAfG_vJGAqvZYCAtTsBB5TLsLB68EAIqAveA27q1Zrne6S2J1Rs1NJ14CMsGhxI2a-4sfDdmp1D5NENza16w'
KOMMO_BASE = 'https://clubpetro.kommo.com/api/v4'
RD_BASE = 'https://api.rd.services'
RD_CLIENT_ID = 'c66161a0-febd-4db7-ba94-40d0fcf110f5'
FROM_TS = 1751328000  # Jul 1, 2025

rd_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FwaS5yZC5zZXJ2aWNlcyIsInN1YiI6IlVBODEwTU1tcUNjeGQwVGpMX2hiellZbklWNTBoclQtTlFqM3cxWXpqTjRAY2xpZW50cyIsImF1ZCI6Imh0dHBzOi8vYXBwLnJkc3RhdGlvbi5jb20uYnIvYXBpL3YyLyIsImFwcF9uYW1lIjoibjhuXzIiLCJleHAiOjE3NzcwMzQ2NTgsImlhdCI6MTc3Njk0ODI1OCwic2NvcGUiOiIifQ.G_KmQjpZDoliPIbIG3n6mOOZCPC3sOb8Os9_N-KQZ0plUH5PO4m6serOZAT93stXy4cYb4QTExSOtBPO1mJYX2A_3i5JoHe7AwZcCpRAEbBm3BTmTDJ1jvzhrPBgAb1hReFvbIS28v2rAZOUSDWlKyPW6k5fXG36S7y9PXnaTRkFqZs9i3qvcOaFjeaP8IbAR5CQ1_0x3_gRkktYvN5TGRCgi4RderfGOSNnn6Zdq1hCSh-ULiO9p7ddjz_ovtiwV5-ts-SzGM7hvDMZLFFmvHTMHxea6-e5HAKDwUhs_UYg2SJaWKO0KutfcbT1euQJLhpiR4spVus1frTSXNDLSQ'
rd_refresh = 'Sj5qQJhp7W0xZcj9noJrD5OE1h1NmALuETP5S1Ot2tk'
rd_secret = 'eea29560955b44a7bca9d4997a1bfba7'


def refresh_rd():
    global rd_token, rd_refresh
    body = json.dumps({
        'client_id': RD_CLIENT_ID,
        'client_secret': rd_secret,
        'refresh_token': rd_refresh,
    }).encode()
    req = urllib.request.Request(f'{RD_BASE}/auth/token', data=body, method='POST')
    req.add_header('Content-Type', 'application/json')
    resp = urllib.request.urlopen(req, timeout=30)
    data = json.loads(resp.read().decode())
    rd_token = data['access_token']
    if 'refresh_token' in data:
        rd_refresh = data['refresh_token']
    print('  [RD token refreshed]', flush=True)


def rd_call(path, method, body=None, retry=True):
    global rd_token
    req = urllib.request.Request(f'{RD_BASE}{path}', method=method)
    req.add_header('Authorization', f'Bearer {rd_token}')
    req.add_header('Content-Type', 'application/json')
    if body and method != 'GET':
        req.data = json.dumps(body).encode()
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return {'ok': True, 'status': resp.status, 'data': json.loads(resp.read().decode())}
    except urllib.error.HTTPError as e:
        if e.code == 401 and retry:
            refresh_rd()
            return rd_call(path, method, body, retry=False)
        try:
            e.read()
        except:
            pass
        return {'ok': False, 'status': e.code, 'data': None}


# Mappings Kommo enum -> RD valid option
HUNTER_TO_RD = {
    936451: 'No-show',
    936473: 'Tentativas de contato esgotadas',
    937137: 'Tentativas de contato esgotadas',
    936485: 'Tentativas de contato esgotadas',
    937191: 'Autoridade - n\u00e3o tem poder de decis\u00e3o',
    936453: 'Tentativas de contato esgotadas',
    936455: 'Tempo - N\u00e3o \u00e9 a hora para falar',
    936457: 'Concorr\u00eancia - J\u00e1 possui programa de fidelidade',
    936459: 'Placa de automa\u00e7\u00e3o incompat\u00edvel',
    936461: 'Tempo - N\u00e3o \u00e9 a hora para falar',
    936463: 'Tempo - N\u00e3o \u00e9 a hora para falar',
    936465: 'Dados insuficientes',
    936467: 'Autoridade - n\u00e3o tem poder de decis\u00e3o',
    936469: 'N\u00e3o \u00e9 posto de combust\u00edveis',
    936471: 'Neg\u00f3cio duplicado - J\u00e1 \u00e9 cliente',
    936475: 'Dados insuficientes',
    936477: 'Neg\u00f3cio duplicado - J\u00e1 est\u00e1 em negocia\u00e7\u00e3o',
    936479: 'J\u00e1 possui compromisso financeiro com o programa da bandeira',
    936481: 'Concorr\u00eancia - J\u00e1 possui programa de fidelidade',
    936483: 'Contrato de exclusividade na regi\u00e3o',
    936487: 'N\u00e3o se Aplica',
}

CLOSER_TO_RD = {
    925872: 'Concorr\u00eancia - Est\u00e1 negociando com outra empresa',
    926026: 'Or\u00e7amento - Falta de Budget',
    934677: 'Lead alegou que n\u00e3o viu valor',
    926030: 'Churn - Dificuldade na implanta\u00e7\u00e3o',
    933235: 'Lead alegou que n\u00e3o viu valor',
    926028: 'Tempo - Troca do sistema de gest\u00e3o',
    926032: 'Tempo - Troca do sistema de gest\u00e3o',
    926034: 'Tempo - Troca do sistema de gest\u00e3o',
    926040: 'Perfil inadequado',
    926042: 'N\u00e3o tem autoridade',
    926044: 'Perfil inadequado',
    926046: 'Lead alegou que n\u00e3o viu valor',
    926048: 'Tempo - Troca do sistema de gest\u00e3o',
    926050: 'Lead alegou que n\u00e3o viu valor',
    932703: 'Or\u00e7amento - Falta de Budget',
    936489: 'N\u00e3o se Aplica',
}


def get_field(lead, fid):
    for f in (lead.get('custom_fields_values') or []):
        if f['field_id'] == fid and f.get('values'):
            return f['values'][0].get('enum_id', 0), f['values'][0].get('value', '')
    return None, None


def get_loss_info(lead):
    h_enum, _ = get_field(lead, 1288043)
    c_enum, _ = get_field(lead, 1277082)
    if h_enum == 936487:  # Sou Closer
        return 'cf_motivo_de_perda_closer', CLOSER_TO_RD.get(c_enum, 'N\u00e3o se Aplica')
    if c_enum == 936489:  # Sou Hunter
        return 'cf_motivo_de_perda_hunter', HUNTER_TO_RD.get(h_enum, 'N\u00e3o se Aplica')
    if h_enum:
        return 'cf_motivo_de_perda_hunter', HUNTER_TO_RD.get(h_enum, 'N\u00e3o se Aplica')
    if c_enum:
        return 'cf_motivo_de_perda_closer', CLOSER_TO_RD.get(c_enum, 'N\u00e3o se Aplica')
    return 'cf_motivo_de_perda_hunter', 'Sem Identifid'


# --- Main loop ---
stats = {
    'total': 0, 'with_email': 0, 'rd_found': 0,
    'opp_unmarked': 0, 'field_updated': 0, 'errors': 0,
}
page = 1

print(f'Iniciando backfill de leads perdidos desde Jul/2025...', flush=True)
print(f'Carregando pagina 1...', flush=True)

while True:
    url = (
        f'{KOMMO_BASE}/leads'
        f'?filter[statuses][0][pipeline_id]=8166623'
        f'&filter[statuses][0][status_id]=143'
        f'&filter[closed_at][from]={FROM_TS}'
        f'&with=contacts,custom_fields_values'
        f'&limit=250&page={page}'
    )
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Bearer {KOMMO_TOKEN}')
    try:
        resp = urllib.request.urlopen(req, timeout=30)
    except urllib.error.HTTPError as e:
        if e.code == 204:
            break
        print(f'Kommo error: {e.code}', flush=True)
        break

    data = json.loads(resp.read().decode())
    leads = data.get('_embedded', {}).get('leads', [])
    if not leads:
        break

    print(f'  Pagina {page}: {len(leads)} leads', flush=True)
    for lead in leads:
        stats['total'] += 1

        # Get contact
        contacts = lead.get('_embedded', {}).get('contacts', [])
        if not contacts:
            continue

        cid = contacts[0]['id']
        time.sleep(0.35)
        try:
            creq = urllib.request.Request(f'{KOMMO_BASE}/contacts/{cid}?with=custom_fields_values')
            creq.add_header('Authorization', f'Bearer {KOMMO_TOKEN}')
            cresp = urllib.request.urlopen(creq, timeout=15)
            contact = json.loads(cresp.read().decode())
        except Exception as exc:
            stats['errors'] += 1
            print(f'  #{stats["total"]} Lead {lead["id"]}: contact error {exc}', flush=True)
            continue

        email = None
        for cf in (contact.get('custom_fields_values') or []):
            if cf.get('field_code') == 'EMAIL' or cf.get('field_name') == 'Email':
                if cf.get('values'):
                    email = cf['values'][0]['value']
                break

        if not email:
            continue
        stats['with_email'] += 1

        rd_field, rd_value = get_loss_info(lead)

        # RD: find contact
        time.sleep(0.2)
        rd = rd_call(f'/platform/contacts/email:{urllib.parse.quote(email)}', 'GET')
        if not rd['ok']:
            print(f'  #{stats["total"]} {email}: nao encontrado no RD', flush=True)
            continue
        stats['rd_found'] += 1
        uuid = rd['data'].get('uuid')
        if not uuid:
            continue

        # RD: unmark opportunity
        time.sleep(0.2)
        opp = rd_call(
            f'/platform/contacts/{uuid}/funnels/default',
            'PUT',
            {'lifecycle_stage': 'Lead', 'opportunity': False},
        )
        if opp['ok']:
            stats['opp_unmarked'] += 1

        # RD: update loss reason field
        time.sleep(0.2)
        fld = rd_call(f'/platform/contacts/uuid:{uuid}', 'PATCH', {rd_field: rd_value})
        if fld['ok']:
            stats['field_updated'] += 1

        opp_s = 'OK' if opp['ok'] else f'FAIL({opp["status"]})'
        fld_s = 'OK' if fld['ok'] else f'FAIL({fld["status"]})'
        print(f'  #{stats["total"]} {email}: opp={opp_s} field={fld_s} ({rd_field}={rd_value})', flush=True)

    has_next = '_links' in data and 'next' in data['_links']
    if not has_next or len(leads) < 250:
        break
    page += 1
    print(f'Page {page}... ({stats["total"]} processados)', flush=True)
    time.sleep(0.35)

print('', flush=True)
print('=== BACKFILL CONCLUIDO ===', flush=True)
print(f"Total leads perdidos: {stats['total']}", flush=True)
print(f"Com email no contato: {stats['with_email']}", flush=True)
print(f"Encontrados no RD:    {stats['rd_found']}", flush=True)
print(f"Opp desmarcada:       {stats['opp_unmarked']}", flush=True)
print(f"Campo atualizado:     {stats['field_updated']}", flush=True)
print(f"Erros:                {stats['errors']}", flush=True)
