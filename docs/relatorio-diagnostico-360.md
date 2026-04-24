# Relatório Diagnóstico 360° — CMO ClubPetro

**Data:** 17 de abril de 2026
**Versão:** 3.0 (LTV sobre Gross Margin + LT por churn)
**Período de referência:** Jan-Abr 2026
**Autor:** CMO Advisor (Claude Code)

> **Changelog v3.0:** LTV recalculado sobre Margem Bruta (padrão SaaS), não receita. Gross Margin = 78,8%. LT projetado por churn (1/0,0164 = 61 meses) — base de faturas incompleta (Jan/25+), não serve para LT observado. LTV = R$ 51.268 (GM). LTV:CAC = 9,0:1. Score Eficiência ajustado para 7/10. Ticket em queda (-32% em 2 anos) registrado. Pendência: validar churn real.
>
> **Changelog v2.0:** Corrigidos cálculos de LTV e CAC. CAC antigo (R$ 3.696) usava 2 meses de custo / 3 meses de deals. LTV antigo (R$ 65K) usava fórmula teórica ARPU/churn que superestimava 3-5x vs tenure real observado.

---

## 1. Scorecard de Maturidade

Pontuação de 0 a 10 por pilar. Critério: 0-3 = dados ausentes ou inutilizáveis; 4-6 = dados parciais, decisões limitadas; 7-8 = dados sólidos, gaps pontuais; 9-10 = visão completa e acionável.

| # | Pilar | Score | Status | Justificativa |
|---|-------|:-----:|--------|---------------|
| 1 | Pipeline & Demanda | **8/10** | 🟢 | Kommo mapeado e CALCULADO: win rate por origem, pipeline coverage (1,7x), marketing-sourced (37% Won / 55% MRR pipe), ciclo de venda, motivos de perda. Flags: pipeline coverage baixo, campo Departamento 98% vazio |
| 2 | Eficiência & Custo | **7/10** | 🟢 | CAC R$ 5.725 (blended), LTV R$ 51.268 (sobre GM 78,8%), LTV:CAC 9,0:1. Payback 5,4 meses (+4,3 onboarding = 9,7 total). Ticket em queda (-32% em 2 anos). Churn rate 1,64%/mês trend de alta. Pendência: validar churn real (base faturas incompleta). Falta: CAC por canal |
| 3 | Crescimento & Marca | **8/10** | 🟢 | GA4 + Search Console + Meta Ads integrados. Brand search +130%. Concorrentes mapeados: Pontuax, PostoAki, Promoflex, Cibus, Meu Posto. Falta: win rate específico por concorrente |
| 4 | Retenção & Produto | **6/10** | 🟡 | Churn rate calculado (1,64%/mês, trend de alta). Tenure medido (13 meses churned). Onboarding gap 128 dias. Falta: motivos de churn, NPS, activation rate, expansion revenue |
| 5 | Execução & Time | **3/10** | 🔴 | ClickUp e Indeed integrados mas sem métricas configuradas. Sem sprint velocity, sem hiring pipeline mapeado, sem OKRs visíveis |

**Score Geral: 6,4/10** — Pipeline e crescimento sólidos. Eficiência saudável (LTV:CAC 9,0:1) mas com dois alertas: ticket em queda (-32%) e churn em alta (0,7%→2,9%). LT de 61 meses é projeção — precisa validar com dados de churn reais. Gaps restantes: motivos de churn, NPS, ativação, CAC por canal, execução do time.

---

## 2. Status das Integrações

| Fonte | Tipo | Status | O que fornece | Docs |
|-------|------|--------|---------------|------|
| **Kommo CRM** | API direta | ✅ Completo | Pipeline, funil, win/loss, MRR por deal, ciclo de venda, origens | `memory/integracoes/kommo.md` |
| **DRE (resultados.xlsx)** | Arquivo local | ✅ Completo | Receita, MRR, S&M por área, margens, ferramentas | `memory/integracoes/dre-resultados.md` |
| **GA4** | Service Account | ✅ Completo | Sessions por canal, tráfego, engajamento | `memory/integracoes/ga4-search-console.md` |
| **Search Console** | Service Account | ✅ Completo | Brand search, non-brand queries, CTR, posições | `memory/integracoes/ga4-search-console.md` |
| **Meta Ads** | Graph API | ✅ Completo | Spend, campanhas, CPL, impressões, cliques | `memory/integracoes/meta-ads.md` |
| **BD_Conversoes_RD** | Supabase | ✅ Completo | Leads reais, UTMs, sub_origem, volume mensal | `memory/integracoes/conversoes-supabase.md` |
| **BD_RDOportunidades** | Supabase | ✅ Completo | MQLs, canal, tag, conversão para Kommo | `memory/integracoes/conversoes-supabase.md` |
| **Google Ads** | — | ⬜ Não utilizado | ClubPetro não investe em Google Ads | — |
| **Sistema Core (WebPosto)** | — | ❌ Não integrado | Churn detalhado, cancelamentos, tenure | — |
| **NPS** | — | ❌ Desconhecido | Satisfação do cliente | — |
| **ClickUp** | MCP | ⚠️ Conectado, não configurado | Tarefas, sprints, produtividade | — |
| **Indeed** | MCP | ⚠️ Conectado, não configurado | Vagas, candidatos, hiring pipeline | — |

---

## 3. Números-Base (Jan-Mar 2026)

### 3.1 Receita e MRR
| Indicador | Jan/26 | Fev/26 | Mar/26 | Fonte |
|-----------|--------|--------|--------|-------|
| Receita Bruta | R$ 1.251.728 | R$ 1.211.725 | R$ 1.345.307 | DRE |
| MRR Total | R$ 1.065.756 | R$ 1.046.120 | R$ 1.073.473 | DRE |
| New MRR | R$ 30.754 | R$ 10.650 | R$ 27.231 | DRE (manual) |
| Churn MRR | R$ 5.604 | R$ 13.210 | R$ 10.645 | DRE (manual) |
| Net New MRR | R$ 25.150 | -R$ 2.560 | R$ 16.586 | DRE |
| CNPJs ativos | 1.105 | 1.086 | 1.125 | DRE (manual) |
| Ticket Médio | R$ 964 | R$ 963 | R$ 954 | Calculado |

### 3.2 Funil de Marketing (CORRIGIDO v2)

**Nota metodológica v2:** MQLs = emails únicos em BD_RDOportunidades com id_kommo preenchido, relacao_posto = Dono/Gerente/Não se aplica, cliente_cp != Sim. Usar conversion_date.

| Indicador | Jan/26 | Fev/26 | Mar/26 | Abr/26* | Fonte |
|-----------|--------|--------|--------|---------|-------|
| Leads (total) | 647 | 1.324 | 814 | 439 | BD_Conversoes_RD |
| ~~MQLs (antigo, rows brutas)~~ | ~~62~~ | ~~104~~ | ~~122~~ | ~~76~~ | ~~inflado ~29%~~ |
| **MQLs (corrigido, únicos+filtros)** | **42** | **71** | **88** | **57** | BD_RDOportunidades |
| **Taxa Lead→MQL (corrigida)** | **6,5%** | **5,4%** | **10,8%** | **13,0%** | Calculado |

*Abril parcial (18 dias). Nota: pico de Fev em leads (1.324) inclui 432 leads outbound cadastrados manualmente.

### 3.3 S&M (Despesas Diretas do CMO)
| Área | Jan/26 | Fev/26 | Total | Fonte |
|------|--------|--------|-------|-------|
| Comercial | R$ 74.230 | R$ 61.302 | R$ 135.532 | DRE |
| Marketing | R$ 82.872 | R$ 55.815 | R$ 138.687 | DRE |
| Feiras e Eventos | R$ 2.368 | R$ 15.391 | R$ 17.758 | DRE |
| **Total S&M** | **R$ 159.470** | **R$ 132.508** | **R$ 291.978** | DRE |
| S&M % Receita Líq. | 13,6% | 11,7% | — | Calculado |

### 3.4 Tráfego
| Canal | Sessions/mês | % | Fonte |
|-------|-------------|---|-------|
| Organic Search | 6.873 | 45% | GA4 |
| Direct | 2.571 | 17% | GA4 |
| Paid Social | 2.509 | 16% | GA4 |
| Display | 1.418 | 9% | GA4 |
| Organic Social | 1.379 | 9% | GA4 |
| Email | 329 | 2% | GA4 |
| Referral | 272 | 2% | GA4 |

### 3.5 Brand Search
| Indicador | Valor | Fonte |
|-----------|-------|-------|
| Brand clicks (28d) | ~2.100 | Search Console |
| Crescimento Out/25→Mar/26 | +130% clicks | Search Console |
| CTR brand | >60% | Search Console |

### 3.6 Pipeline Comercial (Kommo — dados reais, abril/2026)

#### Vendas Ganhas 2026 (86 deals)
| Origem | Deals | MRR | % Deals | Win Rate |
|--------|:-----:|----:|:-------:|:--------:|
| **Inbound** | 30 | R$ 21.829 | 34,9% | 8,5% |
| Outbound | 19 | R$ 12.489 | 22,1% | 1,7% |
| Expansão | 19 | R$ 10.781 | 22,1% | 100% |
| Indicação | 7 | R$ 5.400 | 8,1% | 31,8% |
| Parcerias | 5 | R$ 1.894 | 5,8% | 29,4% |
| Retomada | 3 | R$ 2.100 | 3,5% | 60,0% |
| Feiras e Eventos | 2 | R$ 1.600 | 2,3% | 6,9% |
| **Total** | **86** | **R$ 56.093** | | **5,3%** |

**Marketing-sourced Won (Inbound + Feiras): 32/86 = 37,2%**

#### Won por mês (por Data de Assinatura, campo 1262596 — Comercial only)
| Mês | Deals | MRR Comercial | % Meta R$ 20K | Status |
|-----|:-----:|:------------:|:-------------:|:------:|
| Jan/26 | 22 | R$ 14.866 | 74% | Abaixo |
| Fev/26 | 29 | R$ 20.159 | 101% | Bateu |
| Mar/26 | 10 | R$ 7.750 | 39% | Longe |
| Abr/26* | 6 | R$ 3.337 | 17%* | Parcial |
| **Média Q1** | | **R$ 14.258** | **71%** | **-29%** |

**Nota metodológica v2:** Mês do deal = Data de Assinatura (1262596), não closed_at. Filtro: Departamento = Comercial. DRE New MRR ≠ Kommo (DRE mede faturamento, Kommo mede venda).

#### Pipeline Ativo (Qualificação em diante — 108 deals)
| Estágio | Deals | MRR |
|---------|:-----:|----:|
| Qualificação | 73 | R$ 10.914 |
| Reunião Agendada | 7 | R$ 715 |
| Proposta Enviada | 23 | R$ 17.148 |
| FUP | 4 | R$ 3.700 |
| Forecast | 1 | R$ 1.200 |
| **Total** | **108** | **R$ 33.677** |

**Pipeline Coverage: 1,7x** (alvo: 3-4x) — 🔴 ABAIXO DO SAUDÁVEL

**Marketing-sourced pipeline: 38/108 deals (35,2%) | MRR R$ 18.510/R$ 33.677 (55,0%)**

#### Ciclo de Venda
| Indicador | Valor |
|-----------|-------|
| Ciclo médio | 127 dias |
| Ciclo mediana | 27 dias |
| Observação | Spread enorme — negócios simples fecham rápido, complexos demoram meses |

#### Win Rate por Origem (2026)
| Origem | Won | Lost | Win Rate | Qualidade |
|--------|:---:|:----:|:--------:|-----------|
| Expansão | 19 | 0 | 100% | Cross-sell — sempre converte |
| Retomada | 3 | 2 | 60,0% | Re-engajamento eficiente |
| Indicação | 7 | 15 | 31,8% | Melhor canal novo |
| Parcerias | 5 | 12 | 29,4% | Canal de alta qualidade |
| **Inbound** | **30** | **325** | **8,5%** | Volume + qualidade razoável |
| Feiras | 2 | 27 | 6,9% | Baixo retorno |
| Outbound | 19 | 1.128 | 1,7% | Volume altíssimo, conversão mínima |

#### Concorrentes (informados pelo CMO)
- Pontuax, PostoAki, Promoflex, Cibus, Meu Posto

### 3.7 Churn, LTV e Faturamento (store_contracts + store_financial_records)

#### Base de Clientes
| Indicador | Valor | Fonte |
|-----------|-------|-------|
| Lojas com contrato ativo | 1.096 | store_contracts |
| Lojas churned (todos contratos cancelados) | 354 | store_contracts |
| Logo churn acumulado | 24,4% (354/1.450) | store_contracts |
| Redes únicas | 676 | store_contracts |
| Contratos ativos | 4.801 | store_contracts |
| MRR total (contratos ativos) | **R$ 1.169.289** | store_contracts |

#### Churn Mensal (últimos 12 meses)
| Mês | Lojas faturando | Churns | Churn Rate |
|-----|:--------------:|:------:|:----------:|
| Abr/25 | 1.073 | 7 | 0,7% |
| Mai/25 | 1.095 | 10 | 0,9% |
| Jun/25 | 1.099 | 8 | 0,7% |
| Jul/25 | 1.089 | 11 | 1,0% |
| Ago/25 | 1.084 | 17 | 1,6% |
| Set/25 | 1.083 | 21 | 1,9% |
| Out/25 | 1.080 | 27 | **2,5%** |
| Nov/25 | 1.067 | 17 | 1,6% |
| Dez/25 | 1.086 | 31 | **2,9%** |
| Jan/26 | 1.101 | 26 | 2,4% |
| Fev/26 | 1.080 | 19 | 1,8% |
| Mar/26 | 1.118 | 20 | 1,8% |

**Churn rate médio (12m): 1,64%/mês = 19,7%/ano**
**Tendência: subindo de 0,7% (Abr/25) para 1,8-2,9% (Q4/25-Q1/26)**

#### Tenure (tempo de vida)
| Grupo | Lojas | Tenure médio | Tenure mediana |
|-------|:-----:|:------------:|:--------------:|
| Ativas | 1.096 | 546 dias (18 meses) | 593 dias (20 meses) |
| Churned | 354 | 519 dias (17 meses) | 395 dias (13 meses) |

#### LTV e Eficiência (CORRIGIDO — v3)

**Nota metodológica v3:** LTV calculado sobre Margem Bruta (padrão SaaS). LT projetado por churn rate (base de faturas incompleta — dados só a partir de Jan/25). Deal = loja.

| Métrica | Valor | Método | Status |
|---------|:-----:|--------|:------:|
| ARPU (ticket médio/loja) | **R$ 1.067/mês** | MRR contratos / lojas ativas | 🟢 |
| Gross Margin | **78,8%** | DRE Jan-Fev (RL - COGS) | 🟢 |
| ARPU ajustado (× GM) | **R$ 841/mês** | 1.067 × 78,8% | 🟢 |
| Churn rate mensal | **1,64%** (média 12m) | store_contracts | 🟡 tendência de alta |
| **LT (Lifetime)** | **61 meses** | 1 / churn (1/0,0164) | 🟡 projeção — pendente validação |
| **LTV** | **R$ 51.268** | ARPU×GM / churn = 841 / 0,0164 | 🟢 |
| CAC blended | **R$ 5.725** | S&M Jan+Fev / 51 lojas Won | 🟢 |
| CAC est. Q1 | **R$ 7.180** | S&M est. Q1 / 61 lojas Won | 🟡 |
| **LTV:CAC** | **9,0:1** | R$ 51.268 / R$ 5.725 | 🟢 saudável |
| Payback (sem onboarding) | **5,4 meses** | R$ 5.725 / R$ 1.067 | 🟡 |
| **Payback real (com onboarding)** | **9,7 meses** | 5,4 + 4,3 meses | 🟡 |

**Cenários de sensibilidade ao churn:**

| Churn | LT | LTV (GM) | LTV:CAC |
|-------|-----|----------|---------|
| 1,64% (média) | 61m | R$ 51.268 | 9,0:1 🟢 |
| 2,0% | 50m | R$ 42.050 | 7,3:1 🟢 |
| 2,5% | 40m | R$ 33.640 | 5,9:1 🟢 |
| 3,0% (pico Dez/25) | 33m | R$ 27.753 | 4,8:1 🟢 |

**Alertas:**
- **Ticket em queda:** média Q1/24 R$ 986 → Q1/26 R$ 671 (-32% em 2 anos). Novos clientes pagam menos.
- **Churn em alta:** 0,7% (Abr/25) → 2,9% (Dez/25). Se estabilizar acima de 2,5%, LTV cai ~35%.
- **Pendência:** LT de 61 meses é projeção teórica. Base de faturas incompleta (só Jan/25+). Validar com dados de churn reais.

#### Gap Assinatura → Primeiro Faturamento
| Indicador | Valor |
|-----------|:-----:|
| Gap mediana | **128 dias (4,3 meses)** |
| Gap médio | 140 dias |
| Até 30 dias | 20% das lojas |
| 31-60 dias | 15% |
| >60 dias | **64% das lojas** |

#### Faturamento Mensal (store_financial_records)
| Mês | Receita Faturada | Notas |
|-----|:----------------:|:-----:|
| Jan/26 | R$ 1.127.398 | 1.338 |
| Fev/26 | R$ 1.112.952 | 1.282 |
| Mar/26 | R$ 1.132.397 | 1.339 |

**Status das notas:** 97% RECEBIDO | 2% ATRASADO | 0,9% CANCELADO | 0,1% A VENCER

---

## 4. Diagnósticos — Problemas Identificados

### D1. Meta Ads: Plataforma infla 2x os leads reais
**Severidade: 🔴 Alta**

| O que o Meta diz | O que o Supabase mostra | Diferença |
|-----------------|------------------------|-----------|
| 2.158 leads | ~1.015 leads (RD) | -53% |
| CPL R$ 12,51 | CPL real R$ 26,60 | 2,1x maior |

**Causa provável:** Eventos duplicados no pixel, formulários incompletos, definição diferente de "conversão" entre Meta e RD Station.

**Impacto:** Qualquer decisão baseada no dashboard do Meta Ads está distorcida. O gestor de tráfego pode acreditar que está performando bem quando na verdade o custo real é o dobro.

**Ação:** Auditar configuração do pixel e eventos de conversão. Usar BD_Conversoes_RD como fonte de verdade.

---

### D2. Meta Ads: Topo e fundo de funil embolados
**Severidade: 🔴 Alta**

Todas as campanhas de geração de leads (e-books, aulões, LPs de solução) usam o mesmo objetivo `OUTCOME_LEADS` e são reportadas juntas. Isso esconde uma diferença brutal de qualidade:

| Estágio | % dos Leads | Conversão→MQL | CPL por MQL | Spend |
|---------|:-----------:|:-------------:|:-----------:|-------|
| **TOPO** (e-books + aulões) | 85% | **3%** | **R$ 403** | ~R$ 10.470 |
| **FUNDO** (LPs de solução) | 15% | **75%** | **R$ 105** | ~R$ 12.170 |

O e-book **"Escala de Frentistas"** sozinho gera 579 leads (57% do total via Meta) mas apenas 10 MQLs (1,7% de conversão).

**Impacto:** O CPL blended de R$ 12,51 é um número enganoso que mistura R$ 3,36 (e-book inútil para pipeline) com R$ 95-120 (LP qualificada). Impossível otimizar budget sem separar.

**Ação:** Separar reporting por estágio de funil. Avaliar se o investimento em topo (R$ 10K/mês) se justifica dado o retorno de 3% em MQLs.

---

### D3. E-book "Escala de Frentistas" — Principal armadilha de volume
**Severidade: 🟡 Média**

| Indicador | Valor |
|-----------|-------|
| Leads gerados (2026) | 579 (57% de todos os leads Meta) |
| MQLs gerados | 10 |
| Conversão Lead→MQL | 1,7% |
| Spend estimado (campanha TESTE DE E-BOOK) | ~R$ 4.793 |
| CPL por MQL | ~R$ 479 |

**Diagnóstico:** Este e-book atrai frentistas e gerentes de pista buscando informação operacional — não decisores de postos. O público-alvo não é o ICP (dono/gestor de posto). É a campanha com maior volume e menor qualidade.

**Ação:** Reduzir ou pausar investimento nesta campanha. Redirecionar budget para LPs de fundo que convertem 75%.

---

### D4. Churn: agora mensurável, mas sem motivos ✅ PARCIALMENTE RESOLVIDO
**Severidade: 🟡 Média (era 🔴 Alta)**

**O que temos agora** (via store_contracts + store_financial_records CSVs):

| Métrica | Valor | Status |
|---------|:-----:|:------:|
| Churn rate (12m) | 1,64%/mês = 19,7%/ano | 🟢 calculado |
| Logo churn acumulado | 354/1.450 = 24,4% | 🟢 calculado |
| Tenure (churned) | mediana 13 meses | 🟢 calculado |
| Tenure (ativas) | mediana 20 meses | 🟢 calculado |
| LTV (conservador, tenure 13m) | R$ 13.871 | 🟡 corrigido v2 |
| LTV (moderado, tenure 20m) | R$ 21.340 | 🟡 corrigido v2 |
| CAC blended | R$ 5.500 | 🟡 corrigido v2 |
| LTV:CAC | 9,0:1 | 🟢 corrigido v3 (sobre GM) |
| Motivos de cancelamento | ❌ Desconhecidos | 🔴 pendente |
| Cohort de churn por origem | ❌ Não cruzado | 🟡 possível (Kommo × contracts) |

**O que ainda falta:**
- **Motivos de churn**: Por que as lojas cancelam? Existe registro no WebPosto ou planilha do CS?
- **Cohort analysis**: Cruzar origem do deal (Kommo) com churn para saber se Inbound/Outbound tem retenção diferente
- **Revenue churn vs logo churn**: Lojas grandes ou pequenas que saem?

**Ação:** Buscar fonte de motivos de cancelamento. Cruzar store_contracts com Kommo para cohort por origem.

---

### D5. CAC e LTV — Metodologia corrigida (v3)
**Severidade: 🟡 Média — eficiência saudável, mas ticket caindo e churn subindo**

#### Metodologia (padrão SaaS)
- **LTV** = (ARPU × Gross Margin%) / Churn Rate Mensal
- LTV se calcula sobre **Margem Bruta**, não receita pura nem EBITDA
- **LT** = 1 / Churn Rate = 1 / 0,0164 = 61 meses (projeção)
- **CAC** = S&M total (Comercial+Marketing+Feiras) / Won Comercial por Data de Assinatura
- Deal = loja

#### CAC

| Período | S&M | Lojas Won | CAC |
|---------|-----|-----------|-----|
| Jan/26 | R$ 159.470 | 22 | R$ 7.249 |
| Fev/26 | R$ 132.508 | 29 | R$ 4.569 |
| **Jan+Fev** | **R$ 291.978** | **51** | **R$ 5.725** |
| Est. Q1 | ~R$ 438K | 61 | R$ 7.180 |

#### LTV

| Componente | Valor |
|-----------|-------|
| ARPU | R$ 1.067/mês |
| Gross Margin | 78,8% (COGS = CS + Onboarding + Suporte + Loja) |
| ARPU × GM | R$ 841/mês |
| Churn rate | 1,64%/mês |
| **LTV** | **R$ 51.268** |

#### LTV:CAC e Payback

| Métrica | Valor | Status |
|---------|-------|--------|
| **LTV:CAC** | **9,0:1** | 🟢 saudável |
| Payback (sem onboarding) | 5,4 meses | 🟡 |
| Payback real (+128d onboarding) | 9,7 meses | 🟡 |

#### Alertas

1. **Ticket em queda:** Q1/24 R$ 986 → Q1/26 R$ 671 (-32%). Se o ARPU cair para R$ 800, LTV cai para R$ 38.400.
2. **Churn em alta:** Se estabilizar em 2,5%, LTV cai para R$ 33.640 (LTV:CAC 5,9:1 — ainda ok). Se chegar a 3%, LTV = R$ 27.753 (4,8:1).
3. **Base de faturas incompleta:** Dados só a partir de Jan/25 (15 meses). LT de 61 meses é projeção — não foi possível validar com dados reais. **Pendência: obter base completa ou acompanhar churn real.**

**Impacto:** Eficiência saudável no cenário atual, mas em deterioração. Ticket caindo + churn subindo = LTV comprimindo dos dois lados.

**Ação:** Monitorar churn mensal de perto. Investigar causa da queda de ticket. Obter base de faturas completa para validar LT real.

---

### D6. S&M como % da receita: dentro do benchmark, mas...
**Severidade: 🟢 Informativo**

| Indicador | ClubPetro | Benchmark SaaS B2B |
|-----------|-----------|-------------------|
| S&M % Receita Líq. | 11,7-13,6% | 30-50% (growth) / 15-25% (mature) |
| Marketing % de S&M | 38-55% | 30-50% |

**Análise:** O S&M está abaixo do benchmark para SaaS em crescimento. Com LTV:CAC de 9,0:1 (sobre GM), há espaço para escalar — mas o ticket em queda (-32%) e churn em alta (0,7%→2,9%) sugerem cautela.

Cenários:
- (a) Se churn estabilizar em 1,5%/mês e ticket se manter → há espaço para aumentar S&M
- (b) Se churn continuar acima de 2,5% → LTV cai ~35% → escalar com cuidado
- (c) Reduzir onboarding gap (128 dias) melhora payback e reduz churn precoce

**Ação:** Não aumentar S&M até estabilizar churn. Focar em eficiência dos canais existentes (realocar de Outbound/Feiras para Inbound/Indicação). Reduzir onboarding gap para acelerar payback.

---

### D7. Classificação de canais inconsistente entre ferramentas
**Severidade: 🟡 Média**

Observado na tabela `BD_RDOportunidades`:
- `ld_ko_channel = "Paid Search"` com `ld_ko_source = "meta"` — Meta Ads é **Paid Social**, não Paid Search
- `ld_ko_channel = "(Other)"` com source `ig` — Instagram é Paid Social ou Organic Social
- `utm_source = "unknown"` em 690 leads (21% do total) — sem rastreamento

**Impacto:** Reports de canal ficam distorcidos. Meta Ads aparece como "Paid Search" em vez de "Paid Social". Análises de mix de canais ficam imprecisas.

**Ação:** Corrigir mapeamento de canais no RD Station ou criar regra de normalização no Supabase.

---

### D8. Pipeline coverage em 1,7x — abaixo do saudável
**Severidade: 🔴 Alta**

| Indicador | ClubPetro | Alvo saudável |
|-----------|:---------:|:-------------:|
| Pipeline Coverage | **1,7x** | 3-4x |
| MRR em pipeline ativo | R$ 33.677 | R$ 60-80K |
| Deals de Qualificação+ | 108 | — |

**Diagnóstico:** Com R$ 33,7K em pipeline vs meta de R$ 20K New MRR, a cobertura de 1,7x é insuficiente. Considerando win rate de 5,3%, o pipeline precisaria de **R$ 377K para garantir R$ 20K** (R$ 20K / 5,3%). Porém, se contarmos apenas da Qualificação em diante (win rate mais alta), a cobertura melhora mas ainda é apertada.

**Impacto:** Risco alto de não bater a meta mensal de New MRR. Pipeline fraco = receita futura comprometida.

**Ação:** Investigar se há gargalo no topo (poucos leads entrando) ou no meio (leads empacando). Verificar se deals estão sendo movidos corretamente nos estágios.

---

### D9. Campo "Departamento" no Kommo: 98% em branco
**Severidade: 🟡 Média**

| Situação | Deals |
|----------|:-----:|
| Perdas 2026 sem Departamento | 1.513 / 1.532 (98,8%) |
| Pipeline ativo sem Departamento | 106 / 108 (98,1%) |
| Won 2026 sem Departamento | 19 / 86 (22,1%) |

**Diagnóstico:** O campo Departamento (1275339) só é preenchido de forma consistente nos deals ganhos (78%). Nos perdidos e pipeline ativo, quase ninguém preenche. Isso impede segmentar corretamente Comercial vs Expansão.

**Impacto:** Análises filtradas por Departamento=Comercial perdem 98% dos dados. Motivos de perda ficam subreportados.

**Ação:** Tornar o campo obrigatório no Kommo. Retroativamente, como a pipeline é única (Pipe Fidelidade), a maioria dos deals é Comercial.

---

### D10. Outbound: volume extremo, conversão mínima
**Severidade: 🟡 Média**

| Indicador | Valor |
|-----------|-------|
| Leads Outbound perdidos (2026) | 1.128 |
| Leads Outbound ganhos (2026) | 19 |
| Win rate Outbound | **1,7%** |
| Win rate Inbound | **8,5%** (5x maior) |

**Diagnóstico:** Outbound gera 70% de todas as perdas do pipeline. A operação de SDR está com volume alto mas qualificação muito baixa. Maioria das perdas são provavelmente rejeições no topo (prospecção fria).

**Impacto:** O time comercial gasta energia desproporcional em leads que não convertem. Custo oculto de oportunidade.

**Ação:** Revisar ICP e critérios de qualificação do SDR. Avaliar se os motivos de perda do Hunter (Pouco Engajamento, Timing inadequado) indicam problema de targeting.

---

### D11. Gap entre MRR assinado (Kommo) e MRR recebido (DRE)
**Severidade: 🔴 Alta**

| Fonte | Momento | New MRR Q1 2026 |
|-------|---------|:--------------:|
| **Kommo** (data de assinatura) | Contrato fechado | R$ 56.093 |
| **DRE** (contabilidade) | Receita efetivamente recebida | R$ 68.635 |
| **Diferença** | | **R$ 12.542 (18%)** |

**Explicação do CMO:**
- **Kommo = fonte de verdade** para "venda fechada" (data de assinatura)
- **DRE = receita recebida** (regime de competência/caixa)
- A DRE inclui pagamentos de deals assinados em meses anteriores que começaram a pagar agora
- O Kommo inclui deals assinados que AINDA NÃO PAGARAM (estão em onboarding)
- **Existe churn pré-receita**: clientes que assinam mas desistem antes de pagar por problemas no onboarding
- O acompanhamento de "emitido vs faturado" é fraco — não há tracking claro entre assinatura e primeiro pagamento

**Diagnóstico — AGORA COM DADOS REAIS (store_contracts + store_financial_records):**

O gap entre assinatura e primeiro faturamento foi medido:
```
Kommo: Venda Ganha (assinatura)
   → Onboarding: MEDIANA DE 128 DIAS (4,3 meses!)
   → 64% das lojas demoram mais de 60 dias
   → Apenas 20% começam a pagar em até 30 dias
   → DRE: Primeiro faturamento
```

**Impacto:** Um deal fechado hoje só gera receita daqui a ~4 meses. Isso significa:
- O payback real é 5,2 meses (CAC corrigido) + 4,3 meses (onboarding) = **~9,5 meses até ROI**
- Qualquer meta de New MRR faturado precisa considerar o pipeline de 4 meses atrás
- Deals que churnam no onboarding são custo puro (S&M gasto, sem receita)

**Ação:**
1. Reduzir tempo de onboarding (meta: <60 dias para 50%+ das lojas)
2. Monitorar taxa de churn no onboarding cruzando Kommo Won com store_financial_records
3. Alinhar expectativa do board: New MRR assinado ≠ New MRR faturado (lag de 4 meses)

---

### D8. WhatsApp Site: canal de MQL forte, mas não otimizado
**Severidade: 🟢 Oportunidade**

| Indicador | Valor |
|-----------|-------|
| Leads via pop-up WhatsApp | 218 (total 2026) |
| MQLs via WhatsApp Site | 148 |
| Conversão Lead→MQL | **68%** |
| Tag no RDOportunidades | "WhatsApp Site" = maior tag de MQL |

**Análise:** O botão de WhatsApp do site é o 2º maior gerador de MQLs (depois de LP Solução Definitiva). Alta intenção — pessoa quer falar com alguém. Custo = zero de mídia (tráfego orgânico/direto).

**Ação:** Otimizar posicionamento do botão, testar CTAs diferentes, medir tempo de resposta.

---

### D12. Churn em tendência de alta
**Severidade: 🔴 Alta**

| Período | Churn Rate Mensal | Trend |
|---------|:-----------------:|:-----:|
| Abr-Jun/25 | 0,7-0,9% | Saudável |
| Jul-Set/25 | 1,0-1,9% | Subindo |
| Out-Dez/25 | 1,6-2,9% | **Pico em Dez (2,9%)** |
| Jan-Mar/26 | 1,8-2,4% | Estabilizando, mas acima do ideal |

**Churn rate médio 12 meses: 1,64%/mês (19,7%/ano)**

Para contexto SaaS B2B:
- <1%/mês = excelente
- 1-2%/mês = aceitável
- \>2%/mês = preocupante

O ClubPetro estava excelente (0,7%) há 12 meses e agora está no limite (1,8%). Dez/25 foi alarmante (2,9% = 31 lojas).

**Impacto:** Se o churn continuar em 1,8%, a empresa precisa adicionar ~20 lojas/mês só para manter o MRR estável. Isso consome toda a meta de R$ 20K New MRR.

**Ação:** Investigar motivos de churn. Cruzar lojas churned com dados de healthScore, produtos, tenure para identificar padrões.

---

### D13. Onboarding de 128 dias é excessivo
**Severidade: 🔴 Alta**

| Indicador | Valor |
|-----------|:-----:|
| Gap mediana assinatura→faturamento | **128 dias** |
| Lojas que levam >60 dias | **64%** |
| Lojas que pagam em até 30 dias | Apenas 20% |

**Benchmark:** SaaS B2B com onboarding complexo tipicamente leva 30-60 dias. O ClubPetro está 2-4x acima.

**Impacto direto no CMO:**
- Payback real: 5,2 meses (CAC corrigido) + 4,3 meses (onboarding) = **9,5 meses total**
- Projeções de receita precisam de lag de 4 meses
- Qualquer aceleração de vendas hoje só impacta receita em agosto

**Ação:** Não é responsabilidade direta do marketing, mas impacta diretamente o ROI de aquisição. Levar dados para CS/Produto e propor meta de redução.

---

## 5. Pendências Prioritárias

### 🔴 Críticas — Bloqueiam decisões estratégicas

| # | Pendência | Métrica desbloqueada | Status |
|---|-----------|---------------------|--------|
| ~~P1~~ | ~~Dados de churn detalhado~~ | ~~LTV, LTV:CAC, churn rate~~ | **✅ RESOLVIDO** via store_contracts CSV. Churn 1,64%/mês. **LTV v3:** R$ 51.268 (sobre GM 78,8%). LTV:CAC 9,0:1. **Pendência:** validar churn real (base faturas incompleta, LT 61m é projeção). Ticket em queda -32%. |
| P2 | **CAC por canal** | Alocação de budget, decisão de escalar/cortar | ⚠️ Estimativa feita, falta refinar alocação de custos |
| ~~P3~~ | ~~Marketing-sourced pipeline %~~ | ~~Contribuição real do marketing~~ | **✅ RESOLVIDO** via Kommo: 37,2% Won deals / 55% MRR pipeline |
| ~~P4~~ | ~~Nº clientes novos/mês por canal~~ | ~~CAC unitário por canal~~ | **✅ RESOLVIDO** via Kommo: Won por origem por mês |
| P1b | **Motivos de churn** | Ação preventiva, cohort de risco | 🔴 Não existe registro. Onde vivem os motivos de cancelamento? |

### 🟡 Importantes — Limitam profundidade

| # | Pendência | Métrica desbloqueada | Depende de |
|---|-----------|---------------------|------------|
| ~~P5~~ | ~~Google Ads: custo separado~~ | ~~N/A~~ | **RESOLVIDO: ClubPetro não investe em Google Ads** |
| ~~P6~~ | ~~Concorrentes principais~~ | ~~Win rate vs. concorrente~~ | **RESOLVIDO: Pontuax, PostoAki, Promoflex, Cibus, Meu Posto** |
| P7 | **NPS** | Satisfação por cohort, detratores | Saber se existe pesquisa de NPS e qual ferramenta |
| P8 | **Activation rate** | Qualidade dos clientes que marketing traz | Definir critério de ativação (primeiro login? 1ª campanha? X dias?) |
| P9 | **Expansion revenue** | LTV completo com upsell/cross-sell | Saber se existe upsell formalizado |
| P10 | **Pipeline coverage automatizado** | Saúde do pipeline em tempo real | Script que cruza MRR em estágios ativos vs meta R$ 20K |

### 🟢 Desejáveis — Completam a visão

| # | Pendência | Métrica desbloqueada | Depende de |
|---|-----------|---------------------|------------|
| P11 | **Sprint velocity (ClickUp)** | Produtividade do time de marketing | Configurar Space/Lista no ClickUp |
| P12 | **Hiring pipeline (Indeed)** | Planejamento de headcount | Mapear vagas abertas de marketing |
| P13 | **Normalização de canais** | Reports precisos por canal | Corrigir mapeamento no RD Station |
| P14 | **Funil completo end-to-end automatizado** | Dashboard Lead→MQL→SAL→SQL→Won | Script que cruza Supabase + Kommo API |
| P15 | **DRE atualizada automaticamente** | Dados financeiros em tempo real | Integrar Google Sheets API ou manter xlsx atualizado |

---

## 6. Melhorias Propostas

### M1. Realocar budget Meta Ads de topo para fundo
**Impacto estimado: 🔴 Alto**

**Situação atual:**
- TOPO: ~R$ 10.470/mês → 26 MQLs → CPL/MQL R$ 403
- FUNDO: ~R$ 12.170/mês → 116 MQLs → CPL/MQL R$ 105

**Proposta:** Redirecionar R$ 5K do topo para fundo.
- Cenário: TOPO cai de R$ 10,5K para R$ 5,5K (~13 MQLs) / FUNDO sobe para R$ 17K (~163 MQLs)
- **Resultado projetado: +34 MQLs/mês com o mesmo budget total**
- Risco: Reduz volume de leads no topo do funil (nutrição a longo prazo diminui)

---

### M2. Separar reporting Meta Ads por estágio
**Impacto estimado: 🟡 Médio**

Criar convenção obrigatória de naming nas campanhas:
- `[TOPO]` = e-books, materiais educativos
- `[MEIO]` = webinars, aulões
- `[FUNDO]` = LPs de solução, fale com especialista

Medir separadamente: CPL, volume, e taxa de conversão para MQL de cada estágio. Hoje está tudo junto e é impossível otimizar.

---

### M3. Construir funil Lead→Won automatizado
**Impacto estimado: 🔴 Alto**

Cruzar 3 fontes em um script/dashboard:
1. `BD_Conversoes_RD` (leads por canal/mês)
2. `BD_RDOportunidades` (MQLs por canal/mês)
3. Kommo API (SAL→SQL→Won por origem/mês)

Métricas geradas:
- Taxas de conversão por estágio por canal
- Win rate por origem
- Ciclo de venda médio por canal
- Marketing-sourced pipeline %

---

### M4. Criar CAC por canal
**Impacto estimado: 🔴 Alto**

Cruzar:
- **Inbound**: spend de marketing (mídia Meta + Google + ferramentas) ÷ Won de origem Inbound
- **Outbound**: custo do time comercial (SDR/Hunter) ÷ Won de origem Outbound
- **Feiras**: despesa Feiras e Eventos ÷ Won de origem Feiras
- **Indicação**: custo alocado ÷ Won de origem Indicação

Precisa: vendas ganhas por origem no Kommo (campo 1266644) por período.

---

### M5. Automatizar pipeline coverage
**Impacto estimado: 🟡 Médio**

Script que consulta Kommo API:
- Soma MRR (campo 1262668) de deals nos estágios Qualificação até Contrato na Rua
- Divide pela meta mensal (R$ 20K)
- Alvo saudável: 3-4x = R$ 60-80K em pipeline ativo

Pode rodar semanalmente e salvar histórico no Supabase.

---

### M6. Auditar pixel do Meta e eventos de conversão
**Impacto estimado: 🟡 Médio**

A plataforma reporta 2.158 leads, mas só 1.015 existem no RD Station. Diferença de 1.143 leads fantasma. Possíveis causas:
- Pixel disparando em pageview de thank-you page (conta visit como conversão)
- Formulário sem redirecionamento correto
- Eventos duplicados
- Leads que desistem antes de completar o form

**Ação:** Auditar eventos de conversão configurados no Meta Business Manager.

---

### M7. Otimizar WhatsApp Site
**Impacto estimado: 🟢 Baixo custo, bom retorno**

WhatsApp Site é o 2º maior gerador de MQLs com 68% de conversão e custo de mídia zero (vem de tráfego orgânico/direto).

Ações:
- Testar posicionamento do botão (flutuante? por página?)
- Medir tempo de resposta do time (SLA)
- A/B test de CTA ("Fale com especialista" vs "Tire suas dúvidas")

---

## 7. CMO Dashboard — Métricas Calculadas

### Métricas do Framework CMO — Status Atual

| Categoria | Métrica | Valor ClubPetro | Alvo Saudável | Status |
|-----------|---------|:--------------:|:-------------:|:------:|
| **Pipeline** | Marketing-sourced pipeline (deals) | 35,2% | 50-70% | 🟡 abaixo |
| **Pipeline** | Marketing-sourced pipeline (MRR) | **55,0%** | 50-70% | 🟢 saudável |
| **Pipeline** | Pipeline coverage | **1,7x** | 3-4x | 🔴 crítico |
| **Pipeline** | MQL→Opp rate | *pendente cruzamento* | >15% | ⬜ |
| **Eficiência** | CAC blended (Jan+Fev) | **R$ 5.725** | — | 🟢 corrigido v3 |
| **Eficiência** | CAC est. Q1 | **R$ 7.180** | — | 🟡 estimado |
| **Eficiência** | Payback (sem onboarding) | **5,4 meses** | <18 meses | 🟡 ok |
| **Eficiência** | Payback real (com onboarding) | **9,7 meses** | <18 meses | 🟡 |
| **Eficiência** | LTV (sobre GM 78,8%) | **R$ 51.268** | — | 🟢 (LT pendente validação) |
| **Eficiência** | LTV:CAC | **9,0:1** | >3:1 | 🟢 saudável |
| **Eficiência** | Ticket trend | **-32% (2 anos)** | estável | 🔴 queda |
| **Eficiência** | Marketing % de S&M | 38-55% | 30-50% | 🟢 saudável |
| **Crescimento** | Brand search trend | **+130% QoQ** | ↑ QoQ | 🟢 forte |
| **Crescimento** | Win rate geral | **5,3%** | — | 🟡 ref. contextual |
| **Crescimento** | Win rate Inbound | **8,5%** | — | 🟢 melhor canal novo |
| **Crescimento** | Win rate vs concorrente | *pendente* | >50% | 🔴 falta dados |
| **Retenção** | NPS | **desconhecido** | >40 | 🔴 falta dados |
| **Retenção** | Churn rate | **1,64%/mês** (19,7%/ano) | <2%/mês | 🟡 no limite, trend de alta |

### Métricas recém-calculadas (Kommo, abril/2026)

| Métrica | Valor | Confiança |
|---------|-------|:---------:|
| Won deals Q1 2026 | 79 (Jan-Mar) + 7 (Abr parcial) = 86 | 🟢 verificado |
| Won MRR total 2026 | R$ 56.093 | 🟢 verificado |
| Marketing-sourced Won | 37,2% (deals) | 🟢 verificado |
| Inbound = #1 canal de receita | R$ 21.829 MRR (30 deals) | 🟢 verificado |
| Pipeline ativo | 108 deals, R$ 33.677 MRR | 🟢 verificado |
| Ciclo de venda mediana | 27 dias | 🟢 verificado |
| Win rate Indicação | 31,8% (melhor canal novo) | 🟢 verificado |
| Win rate Outbound | 1,7% (pior canal) | 🟢 verificado |
| Top motivo perda Hunter | Pouco Engajamento (6) | 🟡 amostra pequena (dept vazio) |
| Top motivo perda Closer | Processo decisório complexo (3) | 🟡 amostra pequena |

---

## 8. Próximos Passos — Roadmap de Resolução

### Fase 1: Quick Wins ✅ FEITO
1. ~~Gerar funil completo Lead→MQL por canal e mês (Supabase)~~ ✅
2. ~~Puxar win rate e ciclo de venda do Kommo por origem~~ ✅
3. ~~Calcular pipeline coverage atual (Kommo)~~ ✅ 1,7x
4. ~~Calcular marketing-sourced pipeline % (Kommo)~~ ✅ 55% MRR
5. ~~Gerar análise de motivos de perda (Kommo)~~ ✅ parcial (dept vazio)
6. ~~Google Ads~~ ✅ Não investem
7. ~~Concorrentes~~ ✅ Pontuax, PostoAki, Promoflex, Cibus, Meu Posto

### Fase 2: Precisa de input do CMO (PENDENTE — 8 perguntas)

**Retenção & Produto:**
8. ~~**P1 — Churn rate:**~~ ✅ Calculado: 1,64%/mês via store_contracts
9. **P1b — Motivos de churn:** ❌ Não existe registro estruturado. Ponto cego assumido — ações de retenção serão baseadas em padrões indiretos (tenure, origem, produto).
10. **P7 — NPS:** ❌ Não existe pesquisa de satisfação. Ponto cego assumido — criar NPS entra como ação recomendada.
11. **P8 — Ativação:** ✅ RESOLVIDO. Loja ativada = sistema instalado + time de pista treinado (saída do onboarding). Gap mediana: 128 dias.
12. **P9 — Expansion:** Existe upsell formal? Como é registrado?

**Execução & Time:**
13. **P11 — ClickUp:** Qual Space/Lista usar para medir produtividade?
14. **P12 — Hiring:** Há vagas abertas de marketing?
15. **P13 — Sprints:** Usam sprints no ClickUp?

### Fase 3: Integrações técnicas
16. **M6 — Auditar pixel Meta** (divergência 2x entre Meta e RD Station)
17. **D9 — Campo Departamento no Kommo** (tornar obrigatório, corrigir histórico)
18. **M3 — Construir funil automatizado** (script Supabase + Kommo)
19. **M5 — Automatizar pipeline coverage** (script recorrente)

### Fase 4: Decisões estratégicas (após dados completos)
20. **D12 — Churn em tendência de alta** — investigar padrões e motivos
21. **D8 — Pipeline coverage 1,7x** — investigar gargalo e aumentar cobertura
22. **M1 — Realocação de budget Meta Ads** (topo → fundo)
23. **D10 — Revisão da operação Outbound** (win rate 1,7%)
24. **M4 — Modelo de CAC por canal** definitivo
25. **D6 — Avaliar nível de S&M** vs meta de crescimento
26. **M2 — Nova convenção de naming** nas campanhas Meta
27. **D13 — Redução do onboarding gap** (128 dias → meta <60 dias)

---

## Anexo: Referência Rápida de Fontes

| Dado | Fonte de verdade | NUNCA usar |
|------|-------------------|-----------|
| Leads/Conversões | `BD_Conversoes_RD` (Supabase) | GA4 conversions, Meta Ads lead count |
| MQLs/Oportunidades | `BD_RDOportunidades` campos `ld_ko_*` (Supabase) | — |
| Pipeline comercial | Kommo API (pipeline 8166623, Dept=Comercial) | Tabelas Supabase BD_Leads_Kommo |
| Tráfego | GA4 property 316433329 | — |
| Brand search | Search Console sc-domain:clubpetro.com | — |
| Custo Meta Ads | Meta Ads Graph API (act_121742801507768) | — |
| Receita/Despesas | DRE resultados.xlsx | — |
| Domínios GA4 | Apenas `clubpetro.com` + `blog.clubpetro.com` | Demais domínios |
