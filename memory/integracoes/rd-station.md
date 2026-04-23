# RD Station Marketing — Integração API

## Conexão
- **API**: OAuth2 (access_token + refresh_token)
- **Client ID**: c66161a0-febd-4db7-ba94-40d0fcf110f5
- **Client Secret**: Supabase `vm_app_keys` key=`RD_CLIENT_SECRET`
- **Refresh Token**: Supabase `vm_app_keys` key=`RD_REFRESH_TOKEN`
- **Access Token**: Supabase `vm_app_keys` key=`RD_ACCESS_TOKEN` (atualizar via refresh)
- **Base URL**: `https://api.rd.services/platform/`
- **App name**: n8n_2 (integração via N8N)
- **Account ID**: 170307789894841983 (analytics) / 741603 (emails)
- **Token expira**: 24h. Quando expirar, fazer refresh:
```python
POST https://api.rd.services/auth/token
Body: { client_id, client_secret, refresh_token }
# Salvar novo access_token no Supabase vm_app_keys
```
- **Limitação**: API não expõe body/HTML dos emails, apenas metadados (nome, tipo, destinatários, datas)
- **Total de emails**: 700+ (203 em 2025-2026)

## Endpoints Disponíveis

### 1. Segmentations ✅
- **Endpoint**: `GET /platform/segmentations`
- **Total**: 25 segmentos

**Segmentos padrão (funil):**
| ID | Nome |
|---|---|
| 11001112 | Todos os contatos da base de Leads |
| 11001113 | Leads (estágio no funil) |
| 11001114 | Leads Qualificados (estágio no funil) |
| 11001115 | Clientes (estágio no funil) |
| 11001116 | Oportunidades |
| 11001118 | Leads ativos |
| 11001119 | Leads inativos |

**Segmentos migrados HubSpot:**
- [MARKETING][BASE HUBSPOT] Leads (11240049)
- [MARKETING][BASE HUBSPOT] Leads Qualificados (11245821)
- [MARKETING][BASE HUBSPOT] Oportunidades (11246411)
- [MARKETING][BASE HUBSPOT] Clientes (11247442)
- + versões "inscritos na newsletter" de cada

**Segmentos exemplo (default RD):** 8 segmentos [EXEMPLO]

### 2. Email Analytics ✅
- **Endpoint**: `GET /platform/analytics/emails?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
- **Limite**: últimos 45 dias

**Snapshot 15/Mar - 18/Abr 2026 (15 campanhas):**

| Campanha | Enviados | Open Rate | CTR | Bounce |
|---|---|---|---|---|
| Newsletter 07/04 | 1.533 | 28,1% | 1,7% | 1,4% |
| Newsletter 14/04 | 1.547 | 25,8% | 0,7% | 1,1% |
| Newsletter 31/03 | 1.509 | 27,9% | 1,5% | 2,9% |
| Newsletter 24/03 | 1.486 | 25,9% | 1,6% | 0,7% |
| Newsletter 17/03 | 1.468 | 28,1% | 1,4% | 1,2% |
| Aulão Copa no Caixa - Email 1 | 12.802 | 12,9% | 0,1% | 0,9% |
| Aulão Copa no Caixa - Email 2 | 12.702 | 12,2% | 0,1% | 0,1% |
| Aulão Copa no Caixa - Email 3 | 11.238 | 3,4% | 0,1% | 0,3% |
| Aulão Copa no Caixa - Email 4 | 11.211 | 3,1% | 0,1% | 0,0% |
| Aulão Copa no Caixa - Email 5 | 3.318 | 9,1% | 0,1% | 0,1% |
| Aulão Copa no Caixa - Pós | 82 | 22,5% | 7,5% | 2,4% |
| Aulão Escala 6x1 - Email 2 | 4.499 | 36,2% | 0,3% | 0,4% |
| Aulão Escala 6x1 - Email 3 | 12.677 | 13,0% | 0,2% | 0,2% |
| Aulão Escala 6x1 - Email 4 | 4.326 | 37,9% | 0,5% | 0,1% |
| [Roleta] Email 3 | 1.635 | 40,1% | 0,1% | 1,0% |

**Métricas consolidadas (período):**
- Base newsletter: ~1.500 contatos
- Base aulão: ~12.000 contatos
- Open rate newsletter: 25-28% (bom)
- Open rate aulão: 3-38% (varia muito por sequência)
- CTR geral: 0,1-1,7% (baixo, típico B2B nicho)
- Spam reports: quase zero
- Unsubscribes: zero no período

### 3. Conversion Analytics ✅
- **Endpoint**: `GET /platform/analytics/conversions?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
- **Limite**: últimos 45 dias

**Snapshot 15/Mar - 18/Abr 2026:**
- **Total de assets**: 266 (167 LP Embeddable, 82 LP, 17 Popup)
- **Total conversões**: 833
- **Total visitas**: 15.474
- **Taxa geral**: 5,38%

**Top 5 por conversão:**
| Asset | Conversões | Visitas | Taxa |
|---|---|---|---|
| Escala de Frentistas (material) | 198 | 1.019 | 19,4% |
| Aulão Escala 6x1 (webinar) | 144 | 311 | 46,3% |
| Aulão Copa no Caixa (webinar) | 87 | 276 | 31,5% |
| LP Newsletter | 70 | 1.567 | 4,5% |
| Deveres dos Frentistas (material) | 66 | 225 | 29,3% |

**Insights:**
- 77% das conversões vêm dos 6 primeiros assets
- Webinars convertem muito bem (31-46%)
- Popups geraram ZERO conversões
- Form do blog (newsletter): 4.629 visitas mas só 1,2% conversão — oportunidade CRO
- Materiais de escala/frentistas = topo do funil mais forte

### 4. Automation Workflows ✅
- **Endpoint**: `GET /platform/workflows`
- **Total**: 25 workflows, **todos ativos**

**Categorias:**
- **[Inbound][Materiais]**: ~20 fluxos de nurturing pós-download de materiais
- **[Inbound][Relatórios]**: ~5 fluxos para relatórios/pesquisas

**Temas dos fluxos ativos:**
- Segurança no Posto
- Procedimentos Instalação/Manutenção
- Lealdade dos clientes
- Avaliação do consumidor
- Qualidade dos combustíveis
- Hábitos de pagamento (Pix)
- Sistema eletrônico de medição
- Hábitos de consumo motoristas
- Panorama troca de óleo
- Checklist loja de conveniência
- Checklist caminhão-tanque
- Venda de produtos na pista
- Escala de frentistas (13 dicas)
- Composição valor combustível
- Manutenção preventiva equipamentos
- Escala de Frentistas (principal)
- Kit metas para postos
- Tabela de calibragem
- Quebra de caixa na ducha
- Descrição de cargos
- Funil de vendas lubrificantes
- OKR para postos
- Documentação/sinalização obrigatórios
- POPs (procedimentos operacionais)
- Guerra de preços

### 5. Emails/Templates ✅
- **Endpoint**: `GET /platform/emails`
- **Total**: 704 emails/templates
- Tipos: email (campanhas enviadas), email_model (templates), email_ab (testes A/B)
- Naming convention: `[Inbound][Marketing]`, `[CS][Marketing]`, `[MARKETING][EVENTO]`, `[CLUBPOSTO]`

### 6. Contact Fields ✅
- **Endpoint**: `GET /platform/contacts/fields`
- **Total**: 60 campos (15 padrão + 45 custom)

**Campos custom relevantes para CMO:**
| Campo | Tipo | Uso |
|---|---|---|
| cf_cnpj / cf_cnpj02 | INT/STRING | Identificação empresa |
| cf_bandeira | STRING | Bandeira do posto |
| cf_tipo_de_posto | STRING | Classificação |
| cf_posto_rede | STRING | Se é rede |
| cf_nome_do_posto_rede | STRING | Nome da rede |
| cf_quantidade_de_postos_campo_numerico | INT | Porte |
| cf_galonagem | STRING | Volume |
| cf_quantidade_de_frentistas | INT | Porte operacional |
| cf_funcionalidades_clubpetro | STRING[] | Interesse produto |
| cf_cliente_clubpetro | STRING | Se já é cliente |
| cf_id_kommo | STRING | Link com Kommo CRM |
| cf_proprietario_do_contato | STRING | Owner |
| cf_motivo_de_perda_hunter | STRING | Perda no hunter |
| cf_motivo_de_perda_closer | STRING | Perda no closer |
| cf_dia_agendamento / cf_horario_agendamento | STRING | Agenda demo |
| cf_newsletter | STRING | Opt-in newsletter |
| cf_receita_anual | STRING | Porte financeiro |

### 7. Funnel Analytics ❌
- **Endpoint**: `GET /platform/analytics/funnel`
- **Status**: 401 Forbidden — requer plano superior

### 8. Contacts ⚠️
- **Endpoint**: `GET /platform/contacts` — retornou 502 (instável)
- **Via segmentação**: `GET /platform/segmentations/{id}/contacts` — alternativa funcional
- Contatos também estão no Supabase (BD_Conversoes_RD)

## Relação com Outras Integrações

| Dado | RD Station | Supabase | Kommo |
|---|---|---|---|
| Leads/Conversões | Origem (forms, LPs) | BD_Conversoes_RD (espelho) | Não |
| MQLs/Oportunidades | Marcação funil | BD_RDOportunidades (campos ld_ko_*) | Pipeline deals |
| Clientes | Estágio funil | Não | Won deals |
| Email metrics | Fonte primária | Não | Não |
| Automações | Fonte primária (workflows) | Não | Não |
| Campos comerciais | cf_id_kommo (link) | Não | Fonte primária |

## Como Consultar

### Email performance (últimos 45 dias)
```
GET /platform/analytics/emails?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
```

### Conversões por LP/Form (últimos 45 dias)
```
GET /platform/analytics/conversions?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
```

### Contatos de um segmento
```
GET /platform/segmentations/{segment_id}/contacts
```

### Todos os workflows
```
GET /platform/workflows
```

### Refresh token (quando expirar)
```
POST https://api.rd.services/auth/token
Body: { client_id, client_secret, refresh_token }
```
