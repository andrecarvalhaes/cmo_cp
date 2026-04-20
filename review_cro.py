"""Review CRO - Coleta GA4 + Processamento de Leads - v2"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import json
import os
import re
import statistics
from datetime import datetime, timedelta
from collections import defaultdict
from urllib.parse import urlparse

# ============================================================
# 1. SERVICE ACCOUNT SETUP
# ============================================================
# Credentials loaded from external file (not committed to repo)
SA_PATH = os.environ.get("GA4_SA_PATH", "C:/tmp/ga4_sa.json")
if not os.path.exists(SA_PATH):
    raise FileNotFoundError(f"GA4 service account file not found: {SA_PATH}. Set GA4_SA_PATH env var.")

# ============================================================
# 2. PERIODS
# ============================================================
today = datetime(2026, 4, 18)
current_monday = today - timedelta(days=today.weekday())
periods = []
for i in range(12):
    mon = current_monday - timedelta(weeks=i)
    sun = mon + timedelta(days=6)
    partial = (i == 0)
    periods.append({
        "label": f"P{i+1}",
        "start": mon,
        "end": sun if not partial else today,
        "end_full": sun,
        "partial": partial,
        "days_elapsed": (today - mon).days + 1 if partial else 7
    })

date_start = periods[-1]["start"].strftime("%Y-%m-%d")
date_end = periods[0]["end"].strftime("%Y-%m-%d")

# ============================================================
# 3. BOFU PAGES
# ============================================================
BOFU_SLUGS = [
    "/aumente-seu-ticket-medio", "/solucao-definitiva",
    "/conheca-seu-cliente-de-verdade", "/fidelize-seu-cliente-com-beneficios",
    "/gestao-de-metas", "/fale-com-os-especialistas",
    "/crm-whatsapp", "/roleta-premiada",
    "/historias-de-sucesso", "/planos",
    "/metas-por-ia", "/modulo-sorteio",
    "/integracoes", "/modulo-premios",
    "/whatsapp-integrado-do-clubpetro", "/indique-e-ganhe",
    "/fidelicash", "/analise-360"
]

def classify_page(path):
    if not path:
        return "ToFu", None
    path_clean = path.split("?")[0].rstrip("/")
    if not path_clean:
        path_clean = "/"
    for slug in BOFU_SLUGS:
        slug_clean = slug.rstrip("/")
        if path_clean == slug_clean or path_clean.startswith(slug_clean + "/"):
            return "BoFu", slug_clean
        if path_clean.endswith(slug_clean):
            return "BoFu", slug_clean
    return "ToFu", None

def get_period_index(dt):
    for i, p in enumerate(periods):
        if p["start"] <= dt <= p["end_full"]:
            return i
    return None

# ============================================================
# 4. GA4 DATA - Two queries
# ============================================================
print("Coletando GA4...")
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest, DateRange, Dimension, Metric,
    FilterExpression, Filter, FilterExpressionList
)
from google.oauth2 import service_account

creds = service_account.Credentials.from_service_account_file("C:/tmp/ga4_sa.json")
client = BetaAnalyticsDataClient(credentials=creds)

host_filter = FilterExpression(
    or_group=FilterExpressionList(expressions=[
        FilterExpression(filter=Filter(
            field_name="hostName",
            string_filter=Filter.StringFilter(value="www.clubpetro.com")
        )),
        FilterExpression(filter=Filter(
            field_name="hostName",
            string_filter=Filter.StringFilter(value="clubpetro.com")
        )),
        FilterExpression(filter=Filter(
            field_name="hostName",
            string_filter=Filter.StringFilter(value="blog.clubpetro.com")
        ))
    ])
)

# Query 1: Site-level users by landingPage + date
req1 = RunReportRequest(
    property="properties/316433329",
    date_ranges=[DateRange(start_date=date_start, end_date=date_end)],
    dimensions=[Dimension(name="landingPage"), Dimension(name="date")],
    metrics=[Metric(name="totalUsers"), Metric(name="sessions")],
    dimension_filter=host_filter,
    limit=100000
)
resp1 = client.run_report(req1)
print(f"  Query 1 (landing pages): {len(resp1.rows)} rows")

# Query 2: Page views by pagePath + date (for BoFu page-level CR)
req2 = RunReportRequest(
    property="properties/316433329",
    date_ranges=[DateRange(start_date=date_start, end_date=date_end)],
    dimensions=[Dimension(name="pagePath"), Dimension(name="date")],
    metrics=[Metric(name="screenPageViews"), Metric(name="totalUsers")],
    dimension_filter=host_filter,
    limit=100000
)
resp2 = client.run_report(req2)
print(f"  Query 2 (page views): {len(resp2.rows)} rows")

# Process Query 1: Site-level traffic
site_traffic = defaultdict(lambda: {"users": 0, "sessions": 0})
for row in resp1.rows:
    date_str = row.dimension_values[1].value
    dt = datetime.strptime(date_str, "%Y%m%d")
    pi = get_period_index(dt)
    if pi is None:
        continue
    site_traffic[pi]["users"] += int(row.metric_values[0].value)
    site_traffic[pi]["sessions"] += int(row.metric_values[1].value)

# Process Query 2: BoFu page views
bofu_pageviews = defaultdict(lambda: defaultdict(lambda: {"views": 0, "users": 0}))
for row in resp2.rows:
    page_path = row.dimension_values[0].value
    date_str = row.dimension_values[1].value
    dt = datetime.strptime(date_str, "%Y%m%d")
    pi = get_period_index(dt)
    if pi is None:
        continue
    group, slug = classify_page(page_path)
    if group == "BoFu":
        bofu_pageviews[pi][slug]["views"] += int(row.metric_values[0].value)
        bofu_pageviews[pi][slug]["users"] += int(row.metric_values[1].value)

# ============================================================
# 5. LEADS DATA
# ============================================================
print("Processando leads...")
leads_file = r"C:\Users\ClubPetro-123\.claude\projects\C--Users-ClubPetro-123-Documents-cmo-cp\20e92175-3147-4769-b5d3-ba01c581e5c8\tool-results\mcp-supabase-execute_sql-1776546423357.txt"

with open(leads_file, "r", encoding="utf-8") as f:
    raw = f.read()

outer = json.loads(raw)
text_field = outer[0]["text"]
inner = json.loads(text_field)
result_str = inner["result"]
arr_start = result_str.find('[{"created_at"')
arr_end = result_str.rfind(']')
leads_json = json.loads(result_str[arr_start:arr_end+1])
print(f"  Total leads: {len(leads_json)}")

# Process leads
leads_by_period = defaultdict(lambda: {"total": 0, "bofu": 0, "tofu": 0, "emails": set()})
leads_by_page = defaultdict(lambda: defaultdict(lambda: {"count": 0, "emails": set(), "sub_origens": defaultdict(int), "utm_sources": defaultdict(int)}))

for lead in leads_json:
    created = lead.get("created_at", "")
    if not created:
        continue
    try:
        dt = datetime.strptime(created[:10], "%Y-%m-%d")
    except:
        continue
    pi = get_period_index(dt)
    if pi is None:
        continue

    url = lead.get("url_conversion", "") or ""
    email = (lead.get("email", "") or "").lower().strip()
    sub_origem = lead.get("sub_origem", "") or ""
    utm_source = lead.get("utm_source", "") or ""

    if url:
        try:
            path = urlparse(url).path.rstrip("/") or "/"
        except:
            path = "/"
    else:
        path = "/"

    group, slug = classify_page(path)

    leads_by_period[pi]["total"] += 1
    leads_by_period[pi][group.lower()] += 1
    if email:
        leads_by_period[pi]["emails"].add(email)

    if group == "BoFu" and slug:
        leads_by_page[pi][slug]["count"] += 1
        if email:
            leads_by_page[pi][slug]["emails"].add(email)
        if sub_origem:
            leads_by_page[pi][slug]["sub_origens"][sub_origem] += 1
        if utm_source:
            leads_by_page[pi][slug]["utm_sources"][utm_source] += 1

# ============================================================
# 6. CALCULATE ALL METRICS
# ============================================================
print("\nCalculando metricas...\n")

# Build results table
results = []
for i in range(12):
    p = periods[i]
    total_users = site_traffic[i]["users"]
    total_sessions = site_traffic[i]["sessions"]
    total_leads = leads_by_period[i]["total"]
    bofu_leads = leads_by_period[i]["bofu"]
    tofu_leads = leads_by_period[i]["tofu"]

    # BoFu page views (sum of all BoFu pages)
    bofu_views = sum(bofu_pageviews[i][slug]["views"] for slug in BOFU_SLUGS if slug.rstrip("/") in bofu_pageviews[i])
    bofu_users_pv = sum(bofu_pageviews[i][slug]["users"] for slug in BOFU_SLUGS if slug.rstrip("/") in bofu_pageviews[i])

    cr_site = (total_leads / total_users * 100) if total_users > 0 else 0
    cr_bofu = (bofu_leads / bofu_views * 100) if bofu_views > 0 else 0  # leads / page views
    cr_tofu = (tofu_leads / (total_users - bofu_users_pv) * 100) if (total_users - bofu_users_pv) > 0 else 0

    results.append({
        "label": p["label"],
        "start": p["start"].strftime("%d/%m"),
        "end": p["end"].strftime("%d/%m"),
        "partial": p["partial"],
        "days": p["days_elapsed"],
        "total_users": total_users,
        "total_sessions": total_sessions,
        "total_leads": total_leads,
        "cr_site": cr_site,
        "bofu_leads": bofu_leads,
        "bofu_views": bofu_views,
        "bofu_users": bofu_users_pv,
        "cr_bofu": cr_bofu,
        "tofu_leads": tofu_leads,
        "tofu_users": total_users,  # site-level
        "cr_tofu": cr_tofu,
        "bofu_pct_leads": (bofu_leads / total_leads * 100) if total_leads > 0 else 0,
        "tofu_pct_leads": (tofu_leads / total_leads * 100) if total_leads > 0 else 0,
        "unique_emails": len(leads_by_period[i]["emails"]),
    })

# ============================================================
# 7. OUTPUT
# ============================================================
print("=" * 100)
print("VISAO GERAL - SITE + BLOG (12 semanas)")
print("=" * 100)
print(f"{'Per.':<5} {'Datas':<12} {'Users':>7} {'Sess.':>7} {'Leads':>6} {'CR Site':>8} | {'BoFu Vw':>8} {'BoFu Ld':>7} {'CR BoFu':>8} | {'ToFu Ld':>7}")
print("-" * 100)
for r in results:
    tag = " *" if r["partial"] else ""
    print(f"{r['label']:<5} {r['start']}-{r['end']:<8} {r['total_users']:>7,} {r['total_sessions']:>7,} {r['total_leads']:>6,} {r['cr_site']:>7.1f}% | {r['bofu_views']:>8,} {r['bofu_leads']:>7,} {r['cr_bofu']:>7.1f}% | {r['tofu_leads']:>7,}{tag}")

# Variations
p1, p2 = results[0], results[1]
avg11 = lambda key: sum(r[key] for r in results[1:]) / 11

print(f"\n--- Variacoes P1 vs P2 ---")
for name, key, is_pct in [("Users", "total_users", False), ("Leads", "total_leads", False),
                            ("CR Site", "cr_site", True), ("CR BoFu", "cr_bofu", True),
                            ("BoFu Views", "bofu_views", False), ("BoFu Leads", "bofu_leads", False)]:
    v1, v2 = p1[key], p2[key]
    a11 = avg11(key)
    if is_pct:
        delta = v1 - v2
        vs_avg = v1 - a11
        # Adjust P1 if partial
        if p1["partial"]:
            proj = v1 / p1["days"] * 7
            print(f"  {name:<12}: P1={v1:.1f}% (proj {proj:.1f}%) | P2={v2:.1f}% | D={delta:+.1f}pp | Media 11P={a11:.1f}%")
        else:
            print(f"  {name:<12}: P1={v1:.1f}% | P2={v2:.1f}% | D={delta:+.1f}pp | Media 11P={a11:.1f}%")
    else:
        delta_pct = ((v1 - v2) / v2 * 100) if v2 > 0 else 0
        vs_avg_pct = ((v1 - a11) / a11 * 100) if a11 > 0 else 0
        if p1["partial"]:
            proj = int(v1 / p1["days"] * 7)
            print(f"  {name:<12}: P1={v1:,} (proj {proj:,}) | P2={v2:,} | D={delta_pct:+.1f}% | Media 11P={a11:,.0f}")
        else:
            print(f"  {name:<12}: P1={v1:,} | P2={v2:,} | D={delta_pct:+.1f}% | Media 11P={a11:,.0f}")

# Mix analysis
print(f"\n--- Mix BoFu / ToFu (P1) ---")
print(f"  BoFu = {p1['bofu_pct_leads']:.0f}% dos leads | ToFu = {p1['tofu_pct_leads']:.0f}% dos leads")
avg_bofu_share = sum(r["bofu_pct_leads"] for r in results) / 12
print(f"  Share BoFu medio 12P: {avg_bofu_share:.0f}%")

# Trends
print(f"\n--- Tendencias (slope linear 12 semanas) ---")
for name, key in [("CR Site", "cr_site"), ("CR BoFu", "cr_bofu"), ("Users", "total_users"), ("Leads", "total_leads")]:
    vals = [r[key] for r in results]
    n = len(vals)
    x = [n - 1 - j for j in range(n)]  # chronological
    mx = sum(x) / n
    my = sum(vals) / n
    num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, vals))
    den = sum((xi - mx)**2 for xi in x)
    slope = num / den if den > 0 else 0
    d = "subindo" if slope > 0.01 else "caindo" if slope < -0.01 else "estavel"
    print(f"  {name:<12}: {d} (slope={slope:+.3f})")

# ============================================================
# 8. BOFU PAGES DETAIL
# ============================================================
print(f"\n{'='*100}")
print("PAGINAS BOFU - RANKING")
print(f"{'='*100}")

page_summary = {}
for slug in BOFU_SLUGS:
    sc = slug.rstrip("/")
    total_views = 0
    total_leads = 0
    cr_series = []
    views_series = []
    leads_series = []
    users_series = []
    sub_origens_total = defaultdict(int)

    for i in range(12):
        v = bofu_pageviews[i].get(sc, {}).get("views", 0)
        u = bofu_pageviews[i].get(sc, {}).get("users", 0)
        l = leads_by_page[i].get(sc, {}).get("count", 0)
        cr = (l / v * 100) if v > 0 else 0
        total_views += v
        total_leads += l
        cr_series.append(cr)
        views_series.append(v)
        leads_series.append(l)
        users_series.append(u)

        for so, cnt in leads_by_page[i].get(sc, {}).get("sub_origens", {}).items():
            sub_origens_total[so] += cnt

    cr_avg = (total_leads / total_views * 100) if total_views > 0 else 0

    # Trend
    n = len(cr_series)
    x = [n - 1 - j for j in range(n)]
    mx = sum(x) / n
    my = sum(cr_series) / n
    num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, cr_series))
    den = sum((xi - mx)**2 for xi in x)
    slope = num / den if den > 0 else 0
    direction = "subindo" if slope > 0.01 else "caindo" if slope < -0.01 else "estavel"

    top_sub = sorted(sub_origens_total.items(), key=lambda x: -x[1])[:3]

    page_summary[sc] = {
        "slug": sc,
        "total_views": total_views,
        "total_leads": total_leads,
        "cr_avg": cr_avg,
        "slope": slope,
        "direction": direction,
        "cr_series": cr_series,
        "views_series": views_series,
        "leads_series": leads_series,
        "users_series": users_series,
        "top_sub_origens": top_sub
    }

sorted_pages = sorted(page_summary.values(), key=lambda x: -x["total_leads"])
total_bofu_leads_12p = sum(p["total_leads"] for p in sorted_pages)

print(f"\n{'#':<3} {'Pagina':<42} {'Views 12P':>10} {'Leads 12P':>10} {'CR Media':>8} {'Tend.':>8} {'Share':>7}")
print("-" * 95)
for idx, p in enumerate(sorted_pages, 1):
    share = (p["total_leads"] / total_bofu_leads_12p * 100) if total_bofu_leads_12p > 0 else 0
    limited = " [L]" if p["total_views"] < 360 else ""  # <30/period avg
    print(f"{idx:<3} {p['slug']:<42} {p['total_views']:>10,} {p['total_leads']:>10,} {p['cr_avg']:>7.1f}% {p['direction']:>8} {share:>6.1f}%{limited}")

# Per-page detail
print(f"\n{'='*100}")
print("FICHAS INDIVIDUAIS - PAGINAS BOFU")
print(f"{'='*100}")

for p in sorted_pages:
    print(f"\n### {p['slug']}")
    print(f"  {'Per.':<6} {'Views':>7} {'Leads':>6} {'CR':>7}")
    print(f"  {'-'*30}")
    for i in range(12):
        v = p["views_series"][i]
        l = p["leads_series"][i]
        cr = p["cr_series"][i]
        limited = " [L]" if v < 30 else ""
        print(f"  P{i+1:<5} {v:>7,} {l:>6,} {cr:>6.1f}%{limited}")

    print(f"\n  CR Media 12P: {p['cr_avg']:.1f}% | Tendencia: {p['direction']} (slope={p['slope']:+.3f})")
    print(f"  Total: {p['total_views']:,} views, {p['total_leads']:,} leads")
    share = (p["total_leads"] / total_bofu_leads_12p * 100) if total_bofu_leads_12p > 0 else 0
    print(f"  Share of BoFu leads: {share:.1f}%")
    if p["top_sub_origens"]:
        print(f"  Sub-origens: {', '.join(f'{so}({cnt})' for so, cnt in p['top_sub_origens'])}")

    # Alerts
    if p["total_views"] > 200 and p["total_leads"] == 0:
        print(f"  >> ALERTA: Trafego sem conversao ({p['total_views']} views, 0 leads)")
    if p["slope"] < -0.1 and p["total_leads"] > 5:
        print(f"  >> ALERTA: CR em queda acentuada")
    # P1 with views but 0 leads
    if p["views_series"][0] > 20 and p["leads_series"][0] == 0:
        print(f"  >> ALERTA: {p['views_series'][0]} views na semana atual, 0 leads")

# Classify pages
print(f"\n{'='*100}")
print("MATRIZ DE CLASSIFICACAO BOFU")
print(f"{'='*100}")

views_list = [p["total_views"] for p in sorted_pages]
cr_list = [p["cr_avg"] for p in sorted_pages if p["total_views"] >= 30]
median_views = sorted(views_list)[len(views_list)//2] if views_list else 0
median_cr = sorted(cr_list)[len(cr_list)//2] if cr_list else 0

print(f"Medianas: Views={median_views:,} | CR={median_cr:.1f}%")

categories = {"Star": [], "Oportunidade": [], "Nicho": [], "Inativa": []}
for p in sorted_pages:
    hv = p["total_views"] >= median_views
    hc = p["cr_avg"] >= median_cr and p["cr_avg"] > 0
    if hv and hc:
        categories["Star"].append(p["slug"])
    elif hv and not hc:
        categories["Oportunidade"].append(p["slug"])
    elif not hv and hc:
        categories["Nicho"].append(p["slug"])
    else:
        categories["Inativa"].append(p["slug"])

for cat, pages in categories.items():
    acao = {"Star": "Escalar trafego", "Oportunidade": "Otimizar conversao", "Nicho": "Mais trafego", "Inativa": "Avaliar redesign"}[cat]
    print(f"  {cat}: {', '.join(pages) if pages else '(nenhuma)'} -> {acao}")

# ============================================================
# 9. SCORECARD CRO
# ============================================================
print(f"\n{'='*100}")
print("SCORECARD CRO")
print(f"{'='*100}")

# 1. Volume (P1 vs avg)
users_vals = [r["total_users"] for r in results]
avg_u = sum(users_vals[1:]) / 11
var_u = ((users_vals[0] - avg_u) / avg_u * 100) if avg_u > 0 else 0
# Adjust for partial
if results[0]["partial"]:
    proj_u = users_vals[0] / results[0]["days"] * 7
    var_u = ((proj_u - avg_u) / avg_u * 100) if avg_u > 0 else 0

if var_u > 15: s1 = 5
elif var_u > 5: s1 = 4
elif var_u > -5: s1 = 3
elif var_u > -20: s1 = 2
else: s1 = 1

# 2. CR total
cr_vals = [r["cr_site"] for r in results]
cr_p1 = cr_vals[0]
n = len(cr_vals)
x = [n-1-j for j in range(n)]
mx, my = sum(x)/n, sum(cr_vals)/n
sl = sum((xi-mx)*(yi-my) for xi,yi in zip(x,cr_vals)) / sum((xi-mx)**2 for xi in x) if sum((xi-mx)**2 for xi in x) > 0 else 0

if cr_p1 > 2 and sl > 0: s2 = 5
elif cr_p1 > 1.5 or (cr_p1 > 1 and sl > 0): s2 = 4
elif cr_p1 > 0.5: s2 = 3
elif cr_p1 > 0.3: s2 = 2
else: s2 = 1

# 3. BoFu efficiency - ratio BoFu CR vs site CR
cr_bofu_vals = [r["cr_bofu"] for r in results]
cr_bofu_avg = sum(cr_bofu_vals) / len(cr_bofu_vals) if cr_bofu_vals else 0
cr_site_avg = sum(cr_vals) / len(cr_vals) if cr_vals else 1
ratio = cr_bofu_avg / cr_site_avg if cr_site_avg > 0 else 0

if ratio > 5: s3 = 5
elif ratio > 3: s3 = 4
elif ratio > 2: s3 = 3
elif ratio > 1: s3 = 2
else: s3 = 1

# 4. Consistency (CV of site CR)
if len(cr_vals) > 1 and my > 0:
    cv = (statistics.stdev(cr_vals) / my * 100)
else:
    cv = 100

if cv < 15: s4 = 5
elif cv < 20: s4 = 4
elif cv < 40: s4 = 3
elif cv < 50: s4 = 2
else: s4 = 1

# 5. Coverage
pages_with_leads = sum(1 for p in sorted_pages if p["total_leads"] > 0)
cov = pages_with_leads / 18 * 100

if cov > 80: s5 = 5
elif cov > 70: s5 = 4
elif cov > 50: s5 = 3
elif cov > 30: s5 = 2
else: s5 = 1

# 6. Momentum
last3 = sum(cr_vals[:3]) / 3
allcr = sum(cr_vals) / len(cr_vals)
mom = ((last3 - allcr) / allcr * 100) if allcr > 0 else 0

if mom > 10: s6 = 5
elif mom > 5: s6 = 4
elif mom > -5: s6 = 3
elif mom > -15: s6 = 2
else: s6 = 1

weights = [
    ("Volume de Trafego", s1, 0.15),
    ("Taxa de Conversao", s2, 0.30),
    ("Eficiencia BoFu", s3, 0.20),
    ("Consistencia", s4, 0.10),
    ("Cobertura de Paginas", s5, 0.10),
    ("Momentum", s6, 0.15),
]
total_score = sum(s * w for _, s, w in weights)

if total_score >= 4.0: rating = "Strong"
elif total_score >= 3.0: rating = "Moderate"
elif total_score >= 2.0: rating = "Weak"
else: rating = "Critical"

print(f"\n{'Dimensao':<25} {'Score':>5} {'Peso':>6} {'Ponderado':>10}")
print("-" * 50)
for dim, score, weight in weights:
    print(f"{dim:<25} {score:>5}/5 {weight*100:>5.0f}% {score*weight:>9.2f}")
print("-" * 50)
print(f"{'TOTAL':<25} {'':>5} {'':>6} {total_score:>9.2f}/5")
print(f"\nRating: {rating}")
print(f"CV da CR: {cv:.1f}%")
print(f"Cobertura: {pages_with_leads}/18 paginas gerando leads ({cov:.0f}%)")
print(f"Ratio BoFu/Site CR: {ratio:.1f}x")
print(f"Momentum (3P vs 12P): {mom:+.1f}%")

# ============================================================
# 10. ALERTS
# ============================================================
print(f"\n{'='*100}")
print("ALERTAS E DESTAQUES")
print(f"{'='*100}")

alerts = []
# CR drops 3 consecutive
if all(cr_vals[i] < cr_vals[i+1] for i in range(min(3, len(cr_vals)-1))):
    alerts.append(("ALTO", "Site", "CR Geral em queda por 3+ semanas consecutivas"))

# P11 anomaly (53.7% CR)
if max(cr_vals) > 3 * my:
    max_idx = cr_vals.index(max(cr_vals))
    alerts.append(("INFO", "Site", f"P{max_idx+1} = anomalia ({max(cr_vals):.1f}% CR vs media {my:.1f}%). Provavelmente campanha pontual"))

# BoFu pages with views but 0 leads in recent periods
for p in sorted_pages:
    recent_leads = sum(p["leads_series"][:3])
    recent_views = sum(p["views_series"][:3])
    if recent_views > 50 and recent_leads == 0:
        alerts.append(("MEDIO", "BoFu", f"{p['slug']}: {recent_views} views em 3 sem, 0 leads"))

# Pages with falling CR
for p in sorted_pages:
    if p["slope"] < -0.1 and p["total_leads"] > 10:
        alerts.append(("ALTO", "BoFu", f"{p['slug']}: CR em queda acentuada (slope={p['slope']:+.3f})"))

for prio, scope, detail in sorted(alerts, key=lambda x: {"CRITICO": 0, "ALTO": 1, "MEDIO": 2, "INFO": 3}[x[0]]):
    print(f"  [{prio}] {scope}: {detail}")

# Sparkline
print(f"\n--- Sparkline CR Site (P12 -> P1) ---")
blocks = " _.,:-=+*#@"
cr_rev = list(reversed(cr_vals))
mn, mx = min(cr_rev), max(cr_rev)
rng = mx - mn if mx > mn else 1
for i, v in enumerate(cr_rev):
    idx = min(int((v - mn) / rng * (len(blocks) - 1)), len(blocks) - 1)
    per = f"P{12-i}"
    print(f"  {per:<4} {'|' * max(1, int(v / mx * 30)):>30} {v:.1f}%")

print(f"\n=== SCORE CRO: {total_score:.2f}/5 -- {rating} ===")

# Save results to JSON for reference
output = {
    "score": total_score,
    "rating": rating,
    "periods": [{
        "label": r["label"],
        "dates": f"{r['start']}-{r['end']}",
        "partial": r["partial"],
        "users": r["total_users"],
        "leads": r["total_leads"],
        "cr_site": round(r["cr_site"], 2),
        "bofu_views": r["bofu_views"],
        "bofu_leads": r["bofu_leads"],
        "cr_bofu": round(r["cr_bofu"], 2),
        "tofu_leads": r["tofu_leads"],
    } for r in results],
    "bofu_pages": [{
        "slug": p["slug"],
        "views_12p": p["total_views"],
        "leads_12p": p["total_leads"],
        "cr_avg": round(p["cr_avg"], 2),
        "trend": p["direction"],
    } for p in sorted_pages],
}
with open("C:/tmp/review_cro_output.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
print("Resultados salvos em C:/tmp/review_cro_output.json")
