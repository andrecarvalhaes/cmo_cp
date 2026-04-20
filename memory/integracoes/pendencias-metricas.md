# Pendências de Métricas — CMO Advisor ClubPetro

## Status das Integrações

### Pipeline & Demanda ✅ COMPLETO + CALCULADO
- Fonte: Kommo CRM (API direta)
- Métricas calculadas: win rate por origem, pipeline coverage (1,7x), marketing-sourced (37% Won / 55% MRR), ciclo de venda (mediana 27d), motivos de perda
- Docs: `integracoes/kommo.md`
- **Flag:** campo Departamento 98% vazio em perdas/pipeline

### Eficiência & Custo ✅ COMPLETO (v3)
- Fonte: DRE (resultados.xlsx) + Kommo + Meta Ads + store_contracts/financial_records CSVs
- CAC blended: R$ 5.725 (Jan+Fev) / R$ 7.180 (est. Q1). Deal = loja. S&M total / Won Comercial por Data de Assinatura
- LTV: R$ 51.268 (sobre Gross Margin 78,8%). LT = 1/churn = 61 meses (projeção)
- LTV:CAC: 9,0:1. Payback: 5,4 meses (sem onboarding) / 9,7 meses (com onboarding 128d)
- Churn rate: 1,64%/mês (19,7%/ano), trend de alta (0,7%→2,9%)
- Ticket em queda: Q1/24 R$ 986 → Q1/26 R$ 671 (-32%)
- Gross Margin: 78,8% (COGS = CS + Onboarding + Suporte + Loja)
- **Meta comercial: R$ 20K New MRR/mês** (apenas Fev/26 bateu: R$ 20.159)
- **Pendência:** validar churn real — base de faturas incompleta (Jan/25+), LT 61m é projeção
- Docs: `integracoes/dre-resultados.md`, `integracoes/contratos-faturamento.md`

### Crescimento & Marca ✅ COMPLETO
- Fonte: GA4 + Search Console + Meta Ads API
- Métricas: sessions, brand search +130%, Meta Ads spend/CPL
- Concorrentes mapeados: Pontuax, PostoAki, Promoflex, Cibus, Meu Posto
- **Google Ads**: investiram 1 mês, pararam por falta de resultado. 164 leads "adwords" em 2026 são resquício do período
- Docs: `integracoes/ga4-search-console.md`, `integracoes/meta-ads.md`

### Nurturing & Email ✅ COMPLETO (novo)
- Fonte: RD Station Marketing API (OAuth2)
- Métricas: open rate, CTR, bounce por campanha, conversões por LP/form, workflows ativos
- 25 segmentos, 704 emails, 25 workflows de nurturing, 60 campos de contato
- **Limite**: analytics só últimos 45 dias, funnel analytics bloqueado pelo plano
- Docs: `integracoes/rd-station.md`

### Outbound & Discadora ✅ COMPLETO (novo)
- Fonte: Pluri API (2 endpoints)
- `getRetCampanha`: ligações automáticas do discador (lista fria → outbound)
- `getRetLigSainte`: ligações manuais dos hunters (touchpoints na pipeline)
- Métricas: contact rate, tabulações, volume por campanha, performance por hunter
- Contact rate campanha ~1,4%, manuais ~66%
- Gravações de chamadas disponíveis (url_gravacao)
- Docs: `integracoes/pluri.md`

### Automações ✅ COMPLETO (novo)
- Fonte: N8N API (JWT)
- Instância compartilhada por todos os times
- Acesso para consultar, revisar e criar workflows sob demanda
- Ferramentas conectadas: Supabase, Google Sheets, Discord, Evolution API (WhatsApp), Kommo, Pluri
- Docs: `integracoes/n8n.md`

### Retenção & Produto ⚠️ PARCIAL
- Churn rate calculado: 1,64%/mês, trend de alta (0,7% → 2,9%)
- Tenure calculado: mediana 20 meses (ativas), 13 meses (churned)
- Logo churn acumulado: 354/1.450 = 24,4%
- **Faltam:** NPS, activation rate, expansion revenue, motivos de churn
- Docs: `integracoes/contratos-faturamento.md`

### Execução & Time ⚠️ PARCIAL
- ClickUp MCP ativo — Space "Marketing & Comercial" (90070422586)
- Listas mapeadas: Backlog Melhorias, Backlog Rotina, Sprints (folder Receitas|2026), Kanban Design
- 9 membros do time identificados
- **Velocity calculado**: média 48,4 tarefas/sprint (Sprints 3-7), Sprint 8 em 80+ (em andamento)
- **Faltam:** OKRs, capacity planning, velocity por pessoa
- Docs: `integracoes/clickup.md`

---

## O que ainda preciso do usuário

### 🟡 Retenção & Produto (3 itens pendentes)
| Métrica | Pergunta para o CMO | Status |
|---------|--------------------|--------|
| NPS | ❌ Não existe pesquisa de satisfação | Ponto cego assumido |
| Activation rate | ✅ Definido: sistema instalado + time pista treinado | Gap mediana 128 dias |
| Expansion revenue | Existe upsell/cross-sell? Como é registrado? | Pendente |

### 🟡 Dados Comerciais (2 itens)
| Métrica | Pergunta para o CMO | Status |
|---------|--------------------|--------|
| Motivos de churn | ❌ Não existe registro estruturado | Ponto cego assumido |
| Win rate vs concorrente | Kommo tem "Concorrência" como motivo, mas sem detalhe de qual | Pendente |

### 🟡 Execução & Time (2 itens)
| Métrica | Pergunta para o CMO | Status |
|---------|--------------------|--------|
| Sprint velocity | ✅ Calculado: média 48,4 tasks/sprint (S3-S7). Próximo: detalhar por pessoa | Feito |
| OKRs | Existem OKRs definidos para o time de marketing? | Pendente — próximo passo após diagnóstico |

### 🔴 Pendências Novas (deste chat — Abr/26)
| # | Pendência | Detalhe |
|---|-----------|---------|
| N1 | **Validar churn real** | Base de faturas incompleta (Jan/25+). LT de 61 meses é projeção pelo churn 1,64%. Precisa base completa ou acompanhamento mensal real |
| N2 | **Investigar queda de ticket** | Ticket médio caiu 32% em 2 anos (Q1/24 R$ 986 → Q1/26 R$ 671). Causa? Desconto? Mix de produto? Segmento menor? |
| N3 | **7 leads qualificados perdidos** | Dono/Gerente na BD_RDOportunidades sem id_kommo — nunca entraram no pipeline Kommo. Investigar por que e recuperar |
| N4 | **Fluxo CS para clientes existentes** | 16 registros com cliente_cp="Sim" entrando como MQL. Criar routing automático para CS (não poluir pipeline comercial) |
| N5 | **WhatsApp = mecanismo, não canal** | ~45% dos leads WhatsApp vêm de tráfego pago (UTM). Não classificar como "orgânico" — é mecanismo de conversão |
| N6 | **New MRR por Data de Assinatura** | Jan R$ 14.866 (22 lojas), Fev R$ 20.159 (29 lojas), Mar R$ 7.750 (10 lojas). Só Fev bateu R$ 20K |
| N7 | **MQLs corrigidos** | Jan 42, Fev 71, Mar 88, Abr 57. Método: emails únicos, id_kommo NOT NULL, relacao_posto filtrado, excluindo clientes |
| N8 | **Spike Fev leads** | 432 leads outbound adicionados manualmente em Fev causaram spike de 1.324 leads. Não é orgânico |
| N9 | **Gross Margin** | 78,8% (Jan-Fev/26). COGS = CS + Onboarding + Suporte + Loja. Usado no LTV |
| N10 | **Credencial Webflow** | André precisa passar acesso ao Webflow (site clubpetro.com). Gustavo Zirpoli é o webdesigner |
| N11 | **ClubPosto + Pista Digital** | Heitor de Paula Rosa toca essas 2 iniciativas. Conversar em outro momento para entender escopo |

---

## Informações já coletadas
- [x] Pipeline Kommo: estágios, campos, origens, motivos de perda
- [x] Win rate por origem: Indicação 31,8%, Inbound 8,5%, Outbound 1,7%
- [x] Pipeline coverage: 1,7x (abaixo do 3-4x alvo)
- [x] Marketing-sourced: 37,2% Won deals / 55% MRR pipeline
- [x] Ciclo de venda: mediana 27 dias, média 127 dias
- [x] Won deals Q1 (Dept Comercial, por Data de Assinatura): Jan 22, Fev 29, Mar 10 (61 total)
- [x] CAC blended: R$ 5.725 (Jan+Fev) / R$ 7.180 (est. Q1) — Deal = loja, S&M/Won por Data Assinatura
- [x] LTV: R$ 51.268 (sobre GM 78,8%) | LTV:CAC: 9,0:1 | LT: 61m (projeção, pendente validação)
- [x] Churn rate: 1,64%/mês (19,7%/ano), trend de alta
- [x] Tenure: mediana 20 meses (ativas), 13 meses (churned)
- [x] Onboarding gap: mediana 128 dias (64% >60 dias)
- [x] Logo churn acumulado: 354/1.450 = 24,4%
- [x] DRE: receita, MRR, despesas S&M por área, ferramentas
- [x] Meta comercial: R$ 20K New MRR/mês
- [x] Foco: Licença de Uso Mensal - Posto (69% MRR)
- [x] GA4 + Search Console integrados
- [x] Meta Ads: API integrada, divergência topo/fundo mapeada
- [x] Concorrentes: Pontuax, PostoAki, Promoflex, Cibus, Meu Posto
- [x] Google Ads: investiram 1 mês, pararam (sem resultado). 164 leads "adwords" em 2026 = resquício
- [x] Campo Departamento Kommo: 98% vazio em perdas
- [x] New MRR: Kommo = fonte de verdade (data assinatura). DRE = recebido. Gap 128 dias mediana
- [x] Churn de onboarding medido: 64% das lojas demoram >60 dias para primeiro faturamento
- [x] Base ativa: 1.096 lojas, MRR contratos R$ 1.169.289
- [x] Faturamento mensal ~R$ 1,13M (97% RECEBIDO)
- [x] RD Station: email analytics (open/CTR/bounce), conversões por LP, 25 workflows nurturing, segmentações, campos custom
- [x] N8N: API conectada, workflows consultáveis sob demanda, fluxo Pluri→Kommo mapeado
- [x] Pluri campanha: 887 calls/dia, contact rate 1,4%, 5 campanhas ativas, tabulações mapeadas
- [x] Pluri manual: 168 calls/dia, contact rate 66%, gravações disponíveis
- [x] Fluxo outbound completo: Pluri → N8N (split+filter+switch) → Kommo (pipeline 8166623)
- [x] ClickUp: Space Marketing & Comercial, backlogs + sprints + kanban mapeados
- [x] Time mapeado: 3 líderes (André/Bianca/Galo) + 4 sprint (Lucas/Bernardo/Gustavo/Heitor) + 2 kanban (Ederson/Henrique) + 2 iniciativas (Heitor/Alice)
- [x] Velocity: média 48,4 tasks/sprint (S3-S7). Tarefas são multi-lista (backlog→sprint), consultar via search não filter
- [x] Pipe: Sprint (social media, conteúdo, revisor, copy) + Kanban (design, videomaker)
- [x] Gross Margin: 78,8% (Jan-Fev/26). COGS = CS + Onboarding + Suporte + Loja
- [x] MQLs corrigidos: Jan 42, Fev 71, Mar 88, Abr 57 (emails únicos, id_kommo NOT NULL, relacao_posto filtrado, excl. clientes)
- [x] New MRR por Data Assinatura (Dept Comercial): Jan R$ 14.866, Fev R$ 20.159, Mar R$ 7.750
- [x] Ticket em queda: Q1/24 R$ 986 → Q1/26 R$ 671 (-32%)
- [x] WhatsApp = mecanismo de conversão (~45% vem de tráfego pago), não canal orgânico
- [x] NPS: não existe pesquisa
- [x] Motivos de churn: não existe registro estruturado
- [x] Ativação definida: sistema instalado + time de pista treinado
- [x] Base de faturas incompleta: dados reais Jan/25+ (Ago-Dez/24 = outliers)
