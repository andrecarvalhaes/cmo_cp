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

## Spend Mensal 2026 (atualizado 21/Abr/2026 via API)
| Mês | Spend | Impressões | Cliques | CTR | Leads (Meta) | CPL (Meta) |
|-----|-------|-----------|---------|-----|-------------|------------|
| Jan/26 | R$ 4.989 | 1.122.029 | 11.938 | 1,06% | 340 | R$ 14,67 |
| Fev/26 | R$ 7.036 | 584.529 | 6.705 | 1,15% | 345 | R$ 20,39 |
| Mar/26 | R$ 9.371 | 671.722 | 6.825 | 1,02% | 259 | R$ 36,18 |
| Abr/26* | R$ 7.030 | 567.384 | 5.250 | 0,93% | 148 | R$ 47,50 |
| **Total** | **R$ 28.426** | **2.945.664** | **30.718** | **1,04%** | **1.092** | **R$ 26,03** |

> *Abr/26 = parcial até 21/Abr. Leads = action_type "lead" (pixel + lead forms). Valores anteriores (680, 690, 518, 270) provavelmente incluíam onsite_web_lead duplicado — agora usando apenas "lead" action_type.*

## DIVERGÊNCIA CRÍTICA: 3 camadas de "lead"

### Camada 1 — Meta Ads reporta: 1.092 leads (action_type=lead)
Contagem da plataforma. Pixel fire + lead forms.

### Camada 2 — Supabase (BD_Conversoes_RD, utm_source=meta/ig/facebook): 1.045 leads únicos
Leads que efetivamente entraram no RD Station. Diferença de ~47 = eventos de pixel sem form submit real.

### Camada 3 — MQLs (BD_RDOportunidades, fc/lc_source=meta/ig): 96 MQLs
Leads qualificados como oportunidade. **Este é o número real para o CMO.**

| Mês | Leads Meta | Leads RD (únicos) | MQLs | Taxa Lead→MQL |
|-----|-----------|-------------------|------|---------------|
| Jan | 340 | 237 | 14 | 5,9% |
| Fev | 345 | 267 | 23 | 8,6% |
| Mar | 259 | 258 | 35 | 13,6% |
| Abr* | 148 | 150 | 24 | 16,0% |

> *MQLs filtrados por: id_kommo IS NOT NULL, relacao_posto IN ('Dono(a) ou Diretor(a)', 'Gerente ou Supervisor(a)', 'Não se aplica'), cliente_cp != 'Sim'*

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

## Convenção de UTMs (Padrão João Augusto)

> **IMPORTANTE**: Padrão válido a partir de ~15/Abr/2026. Campanhas anteriores NÃO seguem essa convenção (source pode ser "facebook", "ads", etc.). Nas análises históricas, considerar ambos os padrões ao filtrar.

### Regras
1. **Hierarquia rígida**: source/medium SEMPRE alinhado com canal
   - Meta = `meta / cpc` (nunca "facebook" ou "ads")
   - Google = `google / cpc`
2. **Sintaxe limpa**: tudo minúsculas, sem espaços (usar hífens), sem acentos
3. **Foco no produto**: `utm_campaign` = `[produto]-[objetivo]`
   - "leads" → traduzir para `cadastro` (consistência do funil)
4. **Parâmetros dinâmicos**: em Meta/Google Ads, priorizar variáveis dinâmicas (`{{adset.name}}`, `{{ad.name}}`)
5. **Sem datas**: NUNCA usar meses/datas nas UTMs. Campanhas perpétuas ou identificadas pelo nome

### Exemplo Padrão
```
utm_source=meta&utm_medium=cpc&utm_campaign=fidelidade-cadastro&utm_content={{adset.name}}&utm_term={{ad.name}}
```

### Mapeamento Channel Grouping
| Canal | source | medium |
|-------|--------|--------|
| Meta Ads | meta | cpc |
| Google Ads | google | cpc |

### Para Análises de Cruzamento
- Ao cruzar Meta Ads × Supabase × Kommo: filtrar por `source=meta` e `medium=cpc`
- `utm_campaign` indica produto + objetivo (ex: `fidelidade-cadastro`)
- `utm_content` = nome do adset (público/segmentação)
- `utm_term` = nome do anúncio (criativo)

## Observações
- Fonte de verdade para leads = `BD_Conversoes_RD` (Supabase)
- Fonte de verdade para MQLs = `BD_RDOportunidades` campos `ld_ko_*` (Supabase)
- Meta Ads = APENAS para custo/spend, impressões, cliques
- O e-book "Escala de Frentistas" sozinho = 57% de TODOS os leads Meta, mas gera apenas 1,7% de conversão em MQL
- Engajamento (R$ 3.688) + Tráfego legado (R$ 1.367) = R$ 5.055 sem leads diretos
