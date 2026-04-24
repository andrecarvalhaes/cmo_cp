# Padrões Operacionais — Erros & Lições Aprendidas

> Arquivo auto-atualizado. Sempre que um erro for resolvido após tentativas, registrar aqui o padrão correto.

---

## Encoding & Caracteres Especiais

### ClickUp / qualquer API com texto PT-BR no Windows
- **SEMPRE** usar Python `urllib.request` com `.encode('utf-8')`
- **NUNCA** usar `curl` no Git Bash — corrompe acentos e cedilha
- Header obrigatório: `Content-Type: application/json; charset=utf-8`

### Pluri API
- Formato: POST **form-urlencoded** (não JSON)
- Token base64 DEVE manter padding `=` no final
- Usar `quote_via=urllib.parse.quote` no urlencode (preserva `+` e `=`)

---

## Kommo CRM

- **NUNCA** usar tabelas Supabase (BD_Leads_Kommo etc.) — são desatualizadas. Sempre API direta
- MRR = campo `1262668` (Valor da Mensalidade), NÃO o `price` do lead
- Data de receita = campo `1262596` (Data de Assinatura), NÃO `closed_at`
- Departamento: filtrar `Comercial` apenas, excluir `Expansão`
- Custom fields retornam timestamps Unix para datas
- Hunter vs Closer: checar campo `1288043` (Hunter) e `1277082` (Closer). Se valor = "Sou Closer"/"Sou Hunter", inverter responsável

---

## RD Station

- Token expira em **24h** — sempre buscar fresh de `vm_app_keys` no início
- Se 401: refresh imediato + salvar novo token de volta no Supabase
- Limite de **45 dias** para email analytics e conversões
- Endpoint `/platform/contacts` é instável (502). Usar `/platform/segmentations/{id}/contacts` em vez
- Link RD ↔ Kommo: campo `cf_id_kommo`

---

## Supabase / Postgres

- Conversões = `BD_Conversoes_RD` (fonte de verdade, NÃO GA4)
- MQLs = `BD_RDOportunidades` com filtros: `id_kommo IS NOT NULL`, `relacao_posto IN (Dono, Gerente, Não se aplica)`, `cliente_cp != 'Sim'`
- Faturas (`store_financial_records`): dados confiáveis só a partir de **Jan/25**. Ago-Dez/24 = outliers
- LTV: calcular sobre Gross Margin (78,8%), NUNCA receita pura

---

## GA4 + Search Console

- GA4 = **APENAS tráfego/sessions**. Nunca usar pra conversões
- Domínios: filtrar `clubpetro.com` + `blog.clubpetro.com` apenas
- Search Console: usar `sc-domain:clubpetro.com` no siteUrl
- Service account key: escapar `\n` no private_key ao montar JSON

---

## Meta Ads

- Leads do Meta ≠ MQLs. Divergência em 3 camadas: Meta (1.092) → RD (1.045) → MQLs (96)
- "Paid Search" no RD = Meta Ads (na verdade é Paid Social, classificação errada)
- UTM padrão (pós 15/Abr/2026): `utm_source=meta`, `utm_medium=cpc`, `utm_campaign=[product-objective]`

---

## N8N Automação

- Webhooks event-driven **desconectam silenciosamente** — monitorar gaps diários
- Para reprocessar scoring designers: buscar tasks no ClickUp com `statuses[]=checar&statuses[]=concluído` no período
- Credenciais Supabase no N8N: `E124roxIkDjglv24` (Com&Mkt), `2KgWpUCUPtxUS89C` (RPC Service Role)
- Não usar múltiplos PUTs consecutivos em workflows — deletar e recriar (DELETE + POST)

---

## Instagram Graph API

- Reach = contas únicas/dia. Não confundir com impressions (total views)
- Rate limit: 200 calls/user/hora
- Token = `META_ACCESS_TOKEN` (vm_app_keys, category: 'analytics')
- Stories expiradas não retornam insights via API

---

## ClickUp API — Peculiaridades

- Tasks em sprints: usar `clickup_search` com filtro `subcategories` (list_id). O `filter_tasks` NÃO retorna assignments secundários
- Comentários IA: sempre prefixar com "IA:" para diferenciar de humanos

---

## Vendemais (Sistema Interno)

- **NUNCA** commitar direto na main — sempre branch → PR → aprovação
- PR descriptions em **português**
- `.env.local` requer `GEMINI_API_KEY`
- Main faz auto-deploy — merge só com aprovação explícita do André

---

## Webhooks & Idempotência

- Kommo loss webhook: janela de idempotência = 5 minutos
- Sempre retornar 200 pro sender (evita retries infinitos)
- Logar tudo em tabela dedicada com status (processing/success/error)
- Refresh de token dentro do handler se receber 401
