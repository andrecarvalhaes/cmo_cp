# Conversões e MQLs — Supabase (BD_Conversoes_RD + BD_RDOportunidades)

## Regra Fundamental
- **GA4** = apenas tráfego/acessos (sessions, pageviews, canais). Filtrar por: `clubpetro.com` e `blog.clubpetro.com` — ignorar demais domínios.
- **Conversões (leads)** = tabela `BD_Conversoes_RD` no Supabase
- **MQLs (oportunidades)** = tabela `BD_RDOportunidades` no Supabase, campos `ld_ko_*` (dados tratados)
- **NUNCA usar conversões do GA4** — não são confiáveis

---

## BD_Conversoes_RD — Leads/Conversões

### Campos Principais
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | bigint | PK |
| created_at | date | Data da conversão |
| name | text | Nome do lead |
| email | text | Email |
| telefone | text | Telefone |
| uuid_conversion | text | UUID único da conversão |
| url_conversion | text | URL onde converteu |
| sub_origem | text | Identificador detalhado da origem (padrão: tipo-categoria-nome) |
| Tag | text | Tag do produto/interesse |
| utm_source | text | UTM source |
| utm_campaign | text | UTM campaign |
| utm_medium | text | UTM medium |
| utm_content | text | UTM content |
| utm_value | text | UTM value |
| leadscore_points | numeric | Pontuação de lead scoring |
| relacao_posto | text | Relação do lead com posto |

### Volume Mensal (2026)
| Mês | Conversões |
|-----|-----------|
| Jan/26 | 647 |
| Fev/26 | 1.324 |
| Mar/26 | 814 |
| Abr/26* | 439 |

*Abril parcial (17 dias)

### Top Fontes (utm_source, 2026)
| Fonte | Total | Tipo |
|-------|-------|------|
| meta | 920 | Paid Social (Meta Ads) |
| unknown | 690 | Sem rastreamento |
| (direct) | 359 | Tráfego direto |
| Google | 288 | Orgânico Google |
| RD Station | 220 | Email marketing |
| whatsapp | 205 | WhatsApp |
| adwords | 164 | Google Ads |
| ig | 86 | Instagram orgânico |

### Padrão da sub_origem
Formato: `{tipo}-{categoria}-{nome-do-conteudo}`
- `inbound-materiais-*` = materiais ricos (e-books, checklists)
- `marketing-webinar-*` = webinars/aulões
- `marketing-site-lp-*` = landing pages
- `marketing-pop-up-*` = pop-ups do site (ex: WhatsApp)
- `marketing-blog-*` = blog
- `marketing-site-formulario-*` = formulários do site
- `lista_outbound` = lista de prospecção ativa

### Top Sub-origens (2026)
| Sub-origem | Total | Tipo |
|-----------|-------|------|
| inbound-materiais-escala-de-frentistas | 772 | E-book |
| lista_outbound | 432 | Outbound |
| marketing-pop-up-botao-de-whatsapp-site-clubpetro | 218 | WhatsApp site |
| inbound-materiais-deveres-dos-frentistas | 200 | E-book |
| marketing-webinar-aulao-clubpetro (vários) | ~760 | Webinars |
| marketing-site-lp-newsletter | 136 | Newsletter |

### Tags (2026)
| Tag | Total |
|-----|-------|
| Gestão de Metas | 833 |
| Aumentar as vendas | 45 |
| Fidelidade | 11 |

---

## BD_RDOportunidades — MQLs/Oportunidades

### O que é esta tabela
- Leads que foram qualificados como oportunidades (MQL) no RD Station
- Contém dados brutos do RD + dados tratados com prefixo `ld_ko_*` (já preparados para Kommo)
- **USAR SEMPRE os campos `ld_ko_*`** para análises — são os dados limpos

### Campos Importantes (ld_ko_*)
| Campo | Tipo | Descrição |
|-------|------|-----------|
| ld_ko_id | bigint | ID do lead (RD Station) |
| ld_ko_nome | text | Nome tratado |
| ld_ko_sub_origem | text | Sub-origem tratada |
| ld_ko_channel | text | Canal de aquisição (agrupado) |
| ld_ko_source | text | Fonte (utm_source tratado) |
| ld_ko_medium | text | Medium tratado |
| ld_ko_campaign | text | Campanha |
| ld_ko_tag | text | Tag tratada (tipo de conversão) |
| ld_ko_valor | text | Valor (geralmente "0") |
| ld_ko_cnpj | text | CNPJ do lead |
| ld_ko_link_rd | text | Link para o lead no RD Station |
| conversion_date | date | Data da conversão em oportunidade |
| id_kommo | bigint | ID do lead no Kommo (se já enviado) |

### Outros campos úteis
| Campo | Descrição |
|-------|-----------|
| fc_* | First conversion (primeira conversão) — source, medium, campaign, channel |
| lc_* | Last conversion (última conversão antes de virar MQL) |
| co_ko_* | Dados do contato tratados para Kommo |
| uuid_oportunidade | UUID único da oportunidade |

### Volume Mensal de MQLs (2026)
| Mês | MQLs |
|-----|------|
| Jan/26 | 62 |
| Fev/26 | 104 |
| Mar/26 | 122 |
| Abr/26* | 74 |

*Abril parcial

### MQLs por Canal (ld_ko_channel, 2026)
| Canal | Jan | Fev | Mar | Abr* | Total |
|-------|-----|-----|-----|------|-------|
| Paid Search (meta + adwords) | 14 | 30 | 38 | 33 | 115 |
| Organic Search | 18 | 23 | 19 | 11 | 71 |
| (Other) | 8 | 16 | 43 | 1 | 68 |
| Direct | 9 | 8 | 7 | 8 | 32 |
| Unknown | 2 | 9 | 9 | 8 | 28 |
| Social | 5 | 8 | 1 | 5 | 19 |
| Email | 3 | 4 | 2 | 8 | 17 |
| Referral | 3 | 6 | 3 | 0 | 12 |

### Tags de MQL (ld_ko_tag, 2026)
| Tag | Total | Significado |
|-----|-------|-------------|
| WhatsApp Site | 148 | Converteu pelo botão WhatsApp |
| Formulário Fundo | 62 | Formulário de fundo de funil |
| Lead Score | 21 | Atingiu lead score mínimo |
| Forms Planos | 10 | Formulário de planos/preços |

### Top Sub-origens de MQL (2026)
| Sub-origem | Total |
|-----------|-------|
| marketing-pop-up-botao-de-whatsapp-site-clubpetro | 148 |
| marketing-site-lp-solucao-definitiva | 53 |
| marketing-site-formulario-de-fale-com-um-especialista | 28 |
| marketing-site-lp-fundo-de-funil-aumente-seu-ticket-medio | 26 |

---

## Métricas CMO Deriváveis

### Taxa de Conversão (Lead → MQL)
- Jan: 62 MQLs / 647 leads = **9,6%**
- Fev: 104 / 1.324 = **7,9%**
- Mar: 122 / 814 = **15,0%**

### Funil Completo (cruzando com Kommo)
```
BD_Conversoes_RD (leads) → BD_RDOportunidades (MQLs) → Kommo pipeline (SAL → SQL → Won)
```
- Lead: conversão no site/material (BD_Conversoes_RD)
- MQL: qualificado como oportunidade (BD_RDOportunidades)
- SAL/SQL/Won: pipeline comercial (Kommo API, pipeline 8166623)

### CAC por Canal
- Cruzar: custo do canal (Meta Ads API / DRE) ÷ MQLs por ld_ko_channel
- Paid Search domina MQLs (~32%), Organic Search em 2º (~20%)

---

## Observações
- `ld_ko_channel = "Paid Search"` com `ld_ko_source = "meta"` é na verdade **Paid Social** (classificação errada do GA4/RD) — o Meta Ads é social, não search
- `(Other)` geralmente = tráfego de `ig` (Instagram) com paid_social como medium — também é Meta Ads
- Somando meta + ig + fb no paid = **a maior fonte de MQLs é Meta Ads**
- `ld_ko_valor` está sempre "0" — campo não utilizado atualmente
- Nem todo MQL tem `id_kommo` — alguns ainda não foram enviados para o Kommo
