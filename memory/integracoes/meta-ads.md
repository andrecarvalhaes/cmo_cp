# Meta Ads — Integração e Diagnóstico CMO

## Acesso
- API: Graph API v21.0
- Account: `act_121742801507768` (CA - ClubPetro)
- Currency: BRL | Timezone: America/Sao_Paulo
- Credenciais: tabela `vm_app_keys` (category: 'analytics')
  - `META_ACCESS_TOKEN`, `META_AD_ACCOUNT_ID`, `META_APP_ID`, `META_APP_SECRET`

## Convenção de Nomes das Campanhas
Padrão: `[DATA] [J] [OBJETIVO] [ESTÁGIO] [CONTEÚDO/LP]`
- `[CADASTRO]` = geração de leads (OUTCOME_LEADS)
- `[ENGAJAMENTO]` = awareness (OUTCOME_ENGAGEMENT)
- `[TRÁFEGO]` = visitas ao site (OUTCOME_TRAFFIC)
- `[TOPO]` / `[F]` / `[Q]` / `[MEIO]` = indicadores de estágio de funil (nem sempre presentes)

## Spend Mensal 2026
| Mês | Spend | Leads (Meta) | CPL (Meta) |
|-----|-------|-------------|------------|
| Jan/26 | R$ 4.989 | 680 | R$ 7,34 |
| Fev/26 | R$ 7.036 | 690 | R$ 10,20 |
| Mar/26 | R$ 9.371 | 518 | R$ 18,09 |
| Abr/26* | R$ 5.597 | 270 | R$ 20,73 |
| **Total** | **R$ 26.993** | **2.158** | **R$ 12,51** |

## DIVERGÊNCIA CRÍTICA: 3 camadas de "lead"

### Camada 1 — Meta Ads reporta: 2.158 leads
Contagem da plataforma. Inclui qualquer evento de conversão (pixel fire, lead form, etc.)

### Camada 2 — Supabase (BD_Conversoes_RD, source=meta): ~1.015 leads
Leads que efetivamente entraram no RD Station. Diferença de ~1.143 (provavelmente: eventos duplicados no pixel, formulários incompletos, ou definição diferente de "conversão")

### Camada 3 — MQLs (BD_RDOportunidades, source=meta): 142 MQLs
Leads qualificados como oportunidade. **Este é o número real para o CMO.**

| Mês | Leads Meta | Leads RD (real) | MQLs | Taxa Lead→MQL |
|-----|-----------|----------------|------|---------------|
| Jan | 680 | 261 | 22 | 8,4% |
| Fev | 690 | 303 | 33 | 10,9% |
| Mar | 518 | 205 | 61 | 29,8% |
| Abr* | 270 | 151 | 26 | 17,2% |

## PROBLEMA: Topo e Fundo misturados

### TOPO DE FUNIL (~85% dos leads, ~18% dos MQLs)
| Sub-origem | Leads | MQLs | Conv% | Tipo |
|-----------|-------|------|-------|------|
| escala-de-frentistas | 579 | 10 | 1,7% | E-book |
| deveres-dos-frentistas | 147 | 8 | 5,4% | E-book |
| Aulões (vários) | ~113 | 3 | 2,7% | Webinar |
| Outros e-books | ~20 | 5 | ~25% | E-book |
| **Total TOPO** | **~860** | **~26** | **~3%** | |

### FUNDO DE FUNIL (~15% dos leads, ~82% dos MQLs)
| Sub-origem | Leads | MQLs | Conv% | Tipo |
|-----------|-------|------|-------|------|
| lp-solucao-definitiva | 56 | 46 | 82% | LP fundo |
| pop-up-whatsapp-site | 60 | 38 | 63% | WhatsApp |
| lp-aumente-ticket-medio | 23 | 20 | 87% | LP fundo |
| lp-fidelize-com-beneficios | 12 | 8 | 67% | LP fundo |
| lp-conheca-seu-cliente | 3 | 4 | 133%* | LP fundo |
| **Total FUNDO** | **~154** | **~116** | **~75%** | |

*MQLs > leads = conversões de meses anteriores entrando no período

## Campanhas Ativas por Tipo (Jan-Abr 2026)

### TOPO (e-books + aulões + engajamento)
| Campanha | Spend | Leads Meta | CPL |
|----------|-------|-----------|-----|
| [Q] TESTE DE E-BOOK | R$ 4.793 | 1.426 | R$ 3,36 |
| ENGAJAMENTO TOPO | R$ 3.688 | 0 | — |
| E-BOOKS TESTE DE PÚBLICO | R$ 587 | 150 | R$ 3,92 |
| Aulões (vários) | ~R$ 1.400 | ~350 | ~R$ 4,00 |
| **Total TOPO** | **~R$ 10.470** | **~1.926** | **~R$ 5,44** |

### FUNDO (LPs de solução)
| Campanha | Spend | Leads Meta | CPL |
|----------|-------|-----------|-----|
| LP AUMENTE TICKET MÉDIO | R$ 3.235 | 34 | R$ 95,15 |
| SOLUÇÕES WPP (legado) | R$ 2.841 | 112 | R$ 25,37 |
| LP SOLUÇÕES | R$ 2.172 | 18 | R$ 120,68 |
| LISTA FRIA ANP LP SOLUÇÕES | R$ 1.567 | 2 | R$ 783,45 |
| NOVA LP FIDELIZE | R$ 1.509 | 22 | R$ 68,60 |
| LP CONHEÇA SEU CLIENTE | R$ 846 | 12 | R$ 70,53 |
| **Total FUNDO** | **~R$ 12.170** | **~200** | **~R$ 60,85** |

## CPL Real por Estágio (cruzando Meta spend com Supabase MQLs)

| Estágio | Spend | MQLs gerados | CPL por MQL |
|---------|-------|-------------|-------------|
| TOPO | ~R$ 10.470 | ~26 | **~R$ 403** |
| FUNDO | ~R$ 12.170 | ~116 | **~R$ 105** |
| Blended | R$ 26.993 | 142 | **~R$ 190** |

## Observações
- Fonte de verdade para leads = `BD_Conversoes_RD` (Supabase)
- Fonte de verdade para MQLs = `BD_RDOportunidades` campos `ld_ko_*` (Supabase)
- Meta Ads = APENAS para custo/spend, impressões, cliques
- O e-book "Escala de Frentistas" sozinho = 57% de TODOS os leads Meta, mas gera apenas 1,7% de conversão em MQL
- Engajamento (R$ 3.688) + Tráfego legado (R$ 1.367) = R$ 5.055 sem leads diretos
