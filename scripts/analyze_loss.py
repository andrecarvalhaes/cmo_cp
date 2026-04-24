import json
import sys
from collections import Counter

with open('/tmp/kommo_lost_2026_p1.json') as f:
    data = json.load(f)

leads = data.get('_embedded', {}).get('leads', [])
print(f'Total leads na pagina: {len(leads)}')

has_next = '_links' in data and 'next' in data.get('_links', {})
print(f'Tem mais paginas: {has_next}')

hunter_reasons = Counter()
closer_reasons = Counter()
dept_counts = Counter()
origin_counts = Counter()
monthly = Counter()

for lead in leads:
    dept = None
    hunter_reason = None
    closer_reason = None
    origin = None

    # Get closed month
    closed_at = lead.get('closed_at')
    if closed_at:
        import datetime
        dt = datetime.datetime.fromtimestamp(closed_at)
        monthly[dt.strftime('%Y-%m')] += 1

    for cf in (lead.get('custom_fields_values') or []):
        fid = cf.get('field_id')
        vals = cf.get('values', [])
        if fid == 1275339:
            dept = vals[0].get('value') if vals else None
        elif fid == 1288043:
            hunter_reason = vals[0].get('value') if vals else None
        elif fid == 1277082:
            closer_reason = vals[0].get('value') if vals else None
        elif fid == 1266644:
            origin = vals[0].get('value') if vals else None

    dept_counts[dept] += 1
    if origin:
        origin_counts[origin] += 1
    if hunter_reason and hunter_reason not in ('Sou Closer',):
        hunter_reasons[hunter_reason] += 1
    if closer_reason and closer_reason not in ('Sou Hunter',):
        closer_reasons[closer_reason] += 1

print(f'\n--- Departamento ---')
for d, c in dept_counts.most_common():
    print(f'  {d}: {c}')

print(f'\n--- Perdas por Mes ---')
for m, c in sorted(monthly.items()):
    print(f'  {m}: {c}')

print(f'\n--- Origem dos Leads Perdidos ---')
for o, c in origin_counts.most_common():
    print(f'  {c:3d} | {o}')

print(f'\n--- Motivos de Perda HUNTER (top 15) ---')
for r, c in hunter_reasons.most_common(15):
    print(f'  {c:3d} | {r}')

print(f'\n--- Motivos de Perda CLOSER (top 15) ---')
for r, c in closer_reasons.most_common(15):
    print(f'  {c:3d} | {r}')

print(f'\nTotal Hunter reasons (excl Sou Closer): {sum(hunter_reasons.values())}')
print(f'Total Closer reasons (excl Sou Hunter): {sum(closer_reasons.values())}')
print(f'Total leads perdidos: {len(leads)}')
