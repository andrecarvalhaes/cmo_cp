# GA4 + Google Search Console — Guia de Integração para CMO Advisor

## Credenciais
- **Service Account**: `ga4-api-access@boot-308904.iam.gserviceaccount.com`
- **Credenciais**: tabela `vm_app_keys` (category: 'analytics') no Supabase
  - `GA_PROPERTY_ID`: 316433329
  - `GA_SA_JSON`: JSON da service account (precisa tratar `\n` na private_key)
- **Arquivo local**: salvo em `/tmp/ga4_sa.json` (temporário, recriar se necessário)

## GA4 — Google Analytics 4

### REGRA: Apenas Tráfego
- **GA4 serve APENAS para dados de tráfego/acessos** (sessions, pageviews, canais)
- **NUNCA usar GA4 para conversões** — dados não confiáveis
- **Domínios a rastrear**: apenas `clubpetro.com` e `blog.clubpetro.com` — ignorar demais
- Conversões → `BD_Conversoes_RD` (Supabase)
- MQLs → `BD_RDOportunidades` campos `ld_ko_*` (Supabase)
- Ver: `integracoes/conversoes-supabase.md`

### Acesso
- Property ID: **316433329**
- Biblioteca Python: `google-analytics-data` (`BetaAnalyticsDataClient`)
- Escopo: automático via service account

### Como consultar
```python
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric
from google.oauth2 import service_account

creds = service_account.Credentials.from_service_account_file('/tmp/ga4_sa.json')
client = BetaAnalyticsDataClient(credentials=creds)

request = RunReportRequest(
    property=f"properties/316433329",
    date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
    dimensions=[Dimension(name="sessionDefaultChannelGroup")],
    metrics=[Metric(name="sessions")]
)
response = client.run_report(request)
```

### Dados disponíveis (últimos 30 dias, ref. Abr/2026)
| Canal | Sessions |
|-------|----------|
| Organic Search | 6.873 |
| Direct | 2.571 |
| Paid Social | 2.509 |
| Display | 1.418 |
| Organic Social | 1.379 |
| Email | 329 |
| Referral | 272 |

### Métricas úteis para CMO
- `sessions`, `totalUsers`, `newUsers` — volume de tráfego
- `sessionDefaultChannelGroup` — canal de aquisição
- `sessionSource`, `sessionMedium` — fonte detalhada
- `bounceRate`, `averageSessionDuration` — engajamento
- `conversions`, `eventCount` — conversões (se eventos configurados)
- `landingPage` — páginas de entrada

---

## Google Search Console

### Acesso
- Site: **sc-domain:clubpetro.com** (domínio completo)
- Permissão: **siteFullUser**
- Biblioteca Python: `google-api-python-client` (service `searchconsole` v1)
- Escopo: `https://www.googleapis.com/auth/webmasters.readonly`

### Como consultar
```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

creds = service_account.Credentials.from_service_account_file(
    '/tmp/ga4_sa.json',
    scopes=['https://www.googleapis.com/auth/webmasters.readonly']
)
service = build('searchconsole', 'v1', credentials=creds)

response = service.searchanalytics().query(
    siteUrl='sc-domain:clubpetro.com',
    body={
        'startDate': '2026-03-20',
        'endDate': '2026-04-16',
        'dimensions': ['query'],
        'rowLimit': 25
    }
).execute()
```

### Brand Search (28 dias, ref. Abr/2026)
| Query | Clicks | Impressions | CTR | Pos |
|-------|--------|-------------|-----|-----|
| clubpetro | 715 | 1.178 | 60,7% | 1,2 |
| clubpetro login | 296 | 320 | 92,5% | 1,0 |
| clubpetro 2.0 | 71 | 82 | 86,6% | 1,0 |
| app clubpetro | 48 | 51 | 94,1% | 1,0 |
| **Total brand** | **~1.233** | **~1.796** | | |

**IMPORTANTE**: Variações com grafia errada ("clube petros", "clube petro", "club petro", "clubepetro") somam mais ~865 clicks. Brand search real = ~2.100 clicks/28 dias.

### Non-Brand Orgânico (top queries)
| Query | Clicks | Impressions |
|-------|--------|-------------|
| certificado de posto revendedor (variações) | ~80 | ~1.700 |
| franquia de posto de gasolina | ~11 | ~167 |
| arrendamento de posto de gasolina | 10 | 59 |
| combustíveis alternativos | ~13 | ~562 |

### Trend Mensal (clicks totais)
| Mês | Clicks | Impressions |
|-----|--------|-------------|
| Out/25 | 3.207 | 228.746 |
| Nov/25 | 5.838 | 539.998 |
| Dez/25 | 5.431 | 562.942 |
| Jan/26 | 5.960 | 654.684 |
| Fev/26 | 5.767 | 658.355 |
| Mar/26 | 7.385 | 824.873 |
| Abr/26* | 3.209 | 351.033 |

*Abril parcial (17 dias). Projeção: ~5.700 clicks.

**Crescimento Out→Mar: +130% em clicks, +260% em impressions.**

---

## Métricas CMO Deriváveis

### Brand Awareness
- **Brand search volume**: ~2.100 clicks/28 dias (somar branded + misspellings)
- **Trend**: crescimento consistente Out/25→Mar/26
- **CTR de marca**: >60% (saudável, posição 1)

### Organic Traffic
- **Sessions orgânicas**: ~6.873/mês (GA4)
- **Mix de canais**: Organic Search ~45% do tráfego total
- **Content SEO**: blog atrai via "certificado ANP", "franquia posto gasolina"

### Paid Media (GA4)
- **Paid Social**: 2.509 sessions (provável Meta Ads)
- **Display**: 1.418 sessions
- Cruzar com Meta Ads API para ROAS

---

## Meta Ads (credenciais encontradas, ainda não testado)
- Credenciais na `vm_app_keys` (category: 'ads')
- `META_ACCESS_TOKEN`: disponível
- `META_AD_ACCOUNT_ID`: act_121742801507768
- **Pendente**: testar acesso e documentar métricas disponíveis

---

## Observações
- Mesma service account (`ga4-api-access@boot-308904`) tem acesso a GA4 e Search Console
- GA4 property 316433329 cobre o site principal do ClubPetro
- Search Console cobre todo o domínio `clubpetro.com`
- Meta Ads API ainda não testada — próximo passo
