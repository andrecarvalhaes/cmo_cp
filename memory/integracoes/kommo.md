# Kommo CRM — Guia de Interpretação para CMO Advisor

## Acesso
- API: `https://clubpetro.kommo.com/api/v4/`
- Account ID: 31982463
- Credenciais: tabela `vm_app_keys` (category: 'crm') no Supabase
- **IMPORTANTE: Sempre consultar dados via API do Kommo diretamente, NUNCA pelas tabelas Supabase (BD_Leads_Kommo etc.) — essas tabelas não são mais atualizadas.**

---

## Pipeline: Pipe | Fidelidade (ID: 8166623)

Única pipeline a monitorar. Filtrar sempre por **Departamento = Comercial** (campo 1275339).

### Estágios

| Ordem | Status ID | Etapa | Fase CMO |
|-------|-----------|-------|----------|
| 1 | 65190267 | Etapa de leads de entrada | Lead (unsorted) |
| 2 | 65190271 | ASAP | Lead |
| 3 | 78990456 | TRATATIVA | Lead |
| 4 | 65403031 | Qualificação | MQL |
| 5 | 65190619 | Reunião Agendada | SAL |
| 6 | 65190627 | Reunião Realizada | SAL |
| 7 | 69600491 | Proposta Enviada | SQL / Opportunity |
| 8 | 103148407 | FUP (Follow-up) | SQL / Opportunity |
| 9 | 65190631 | Forecast | Opportunity |
| 10 | 80996616 | STANDBY | Pausa (não contar em velocidade) |
| 11 | 65190647 | Contrato na Rua | Opportunity (fundo) |
| 12 | 68940727 | Criar Loja Core | Pós-venda / Onboarding |
| 13 | 68940731 | Corrigir SLA | Pós-venda / Onboarding |
| — | 142 | Venda Ganha | Closed Won |
| — | 143 | Venda Perdida | Closed Lost |

---

## Campos Importantes

### Classificação e Origem

| Campo ID | Nome | Tipo | Descrição |
|----------|------|------|-----------|
| 1275339 | Departamento | select | "Comercial" ou "Expansão" — **foco apenas em Comercial** |
| 1266644 | Origem | select | Canal de aquisição do lead |
| 1266176 | Sub Origem | text | Detalhamento livre da origem |

#### Valores de Origem (campo 1266644)
| Enum ID | Valor | Tipo de canal |
|---------|-------|---------------|
| 914568 | Inbound | Marketing inbound |
| 914570 | Outbound | Prospecção ativa (SDR) |
| 914572 | Feiras e Eventos | Field marketing |
| 914574 | Retomada | Re-engajamento de leads antigos |
| 914576 | Indicação | Referral / boca a boca |
| 914578 | Expansão | Cross-sell de rede existente |
| 917834 | Parcerias | Channel partners |
| 931377 | Geolocalizada | Prospecção por região |

### Time Comercial

| Campo ID | Nome | Descrição |
|----------|------|-----------|
| 1265304 | Hunter | SDR/prospector responsável |
| 1265318 | Closer | Vendedor que fecha o negócio |

### Datas-Chave

| Campo ID | Nome | Uso para métricas |
|----------|------|-------------------|
| created_at | Data de criação | Início do ciclo de venda |
| 1281649 | Data de apresentação | Marco: lead recebeu demo |
| 1262596 | Data de assinatura | Marco: venda fechada (se preenchido = Closed Won) |

### Valores Financeiros

| Campo ID | Nome | Descrição |
|----------|------|-----------|
| 1262668 | MRR | Receita recorrente mensal do negócio |
| 1268928 | Implantação | Valor único de implantação |
| 1262660 | Aplicativo | Valor de setup do aplicativo |

### Onboarding / Sistema

| Campo ID | Nome | Descrição |
|----------|------|-----------|
| 1268100 | ID da Loja | Se preenchido = criado no sistema, onboarding iniciado |
| 1268102 | ID da Rede | Rede à qual a loja pertence |

### Motivos de Perda

#### Hunter (campo 1288043)
| Enum ID | Motivo |
|---------|--------|
| 936451 | Alta Taxa de No-Show |
| 936473 | Tentativas esgotadas e sem sucesso (Nunca interagiu) |
| 937137 | Tentativas esgotadas e sem sucesso (Teve uma interação) |
| 936485 | Nunca me respondeu, ligo e desliga (sem contato) |
| 937191 | Não é mais o proprietário |
| 936453 | Pouco Engajamento |
| 936455 | Falta de abertura (Rejeição direta) |
| 936457 | Já usa concorrente |
| 936459 | Incompatibilidade técnica (sem placa de automação / incompatível) |
| 936461 | Outras prioridades |
| 936463 | Timing inadequado (não é o momento) |
| 936465 | Dados de contato ruins/faltando |
| 936467 | Falta de autoridade, não é o decisor |
| 936469 | Não é posto |
| 936471 | Já é cliente |
| 936475 | Telefone inválido |
| 936477 | Negócio duplicado |
| 936479 | Já tem programa de bandeira e não quer outro |
| 936481 | Já tem programa de fidelidade e não é de bandeira |
| 936483 | Raio de exclusividade |
| 936487 | Sou Closer (marcado quando hunter não é responsável pela perda) |

#### Closer (campo 1277082)
| Enum ID | Motivo |
|---------|--------|
| 925872 | Concorrência (Preencher o campo embaixo) |
| 926026 | Mensalidade |
| 934677 | App |
| 926030 | Implantação |
| 933235 | Falta de funcionalidades esperadas |
| 926028 | Integração com ERP |
| 926032 | Integração com Smart POS |
| 926034 | Timing inadequado (não é o momento) |
| 926040 | Resistência à tecnologia (lead não qualificado) |
| 926042 | Processo decisório complexo (não é o decisor) |
| 926044 | Falta de estrutura (lead não qualificado) |
| 926046 | "Medo" da dificuldade de implementação |
| 926048 | Dependência dos apps dos distribuidores |
| 926050 | Contrato extenso |
| 932703 | Falta de Budget |
| 936489 | Sou Hunter (marcado quando closer não é responsável pela perda) |

---

## Regras de Negócio

- Cada **loja** é a unidade de venda (deal = 1 loja)
- Lojas podem pertencer à mesma **rede** (grupo/franquia)
- Lead com ID da Loja (1268100) + ID da Rede (1268102) preenchidos = entrou no sistema para onboarding
- Negócio com Data de Assinatura (1262596) preenchida = **venda confirmada**
- Motivo de perda é separado: hunter perde na prospecção, closer perde na negociação
- Quando o campo de motivo marca "Sou Closer" ou "Sou Hunter" = a perda foi responsabilidade do outro papel

---

## Como Calcular Métricas CMO a partir do Kommo

### Funil de Conversão
- **Lead → MQL**: Leads que saem de (Entrada/ASAP/TRATATIVA) e chegam em Qualificação
- **MQL → SAL**: Qualificação → Reunião Agendada/Realizada
- **SAL → SQL**: Reunião Realizada → Proposta Enviada
- **SQL → Opportunity**: Proposta → Forecast/Contrato na Rua
- **Opportunity → Closed Won**: → Venda Ganha (142)

### MRR Novo por Período
- Filtrar: status_id = 142, Departamento = Comercial
- Somar campo MRR (1262668) dos negócios com data de assinatura no período

### Ciclo de Venda
- `Data de assinatura (1262596) - created_at` = ciclo total
- `Data de apresentação (1281649) - created_at` = tempo até demo
- `Data de assinatura - Data de apresentação` = tempo de negociação

### Win Rate
- Negócios com status 142 / (142 + 143) no período = win rate
- Segmentar por origem para win rate por canal

### Pipeline Coverage
- Soma de MRR dos negócios em estágios ativos (Qualificação até Contrato na Rua) vs meta

### CAC por Origem
- Cruzar custo do canal (externo) com quantidade de Closed Won por Origem (1266644)

### Win/Loss Analysis
- Agrupar motivos de perda do Hunter e Closer por frequência
- Identificar padrões: "Concorrência" + "Mensalidade" = problema de pricing/posicionamento
- "Timing inadequado" + "Outras prioridades" = problema de qualificação
- "Incompatibilidade técnica" = filtro de ICP no topo do funil

---

## Como Consultar via API

### Autenticação
- Token: buscar na tabela `vm_app_keys` (category: 'crm', key: 'KOMMO_ACCESS_TOKEN') no Supabase
- Header: `Authorization: Bearer {token}`

### Endpoints Principais

**Leads por status (ex: Venda Ganha):**
```
GET /api/v4/leads?filter[pipe][]=8166623&filter[statuses][0][pipeline_id]=8166623&filter[statuses][0][status_id]=142&with=custom_fields_values&limit=250
```

**Leads por período (created_at em unix timestamp):**
```
GET /api/v4/leads?filter[pipe][]=8166623&filter[created_at][from]={timestamp}&filter[created_at][to]={timestamp}&with=custom_fields_values&limit=250
```

**Paginação:** usar `&page=N` (máx 250 por página). Campo `_links.next` indica se há mais páginas.

### Campos Retornados na API
- `id`, `name`, `price` (valor do deal no Kommo)
- `status_id` → estágio atual
- `pipeline_id` → deve ser 8166623
- `created_at`, `updated_at`, `closed_at` → timestamps unix
- `custom_fields_values[]` → array com field_id, field_name, values
- `responsible_user_id` → responsável pelo lead
- `loss_reason_id` → motivo de perda (campo nativo do Kommo, diferente dos custom fields)

### Nomes reais dos campos (confirmados via API)
| Campo ID | field_name na API |
|----------|-------------------|
| 1262660 | Valor Aplicativo White Label |
| 1262668 | Valor da Mensalidade |
| 1268928 | Valor da Implantação |
| 1268610 | Permanência Mínima |
| 1268100 | Store_ID |
| 1266176 | Sub Origem |
| 1265318 | Closer |
| 1266566 | Produto Vendido (multiselect) |

### Observações Importantes
- O campo `price` do lead NÃO é o MRR — usar custom field 1262668 (Valor da Mensalidade)
- Datas em custom fields vêm como unix timestamp
- Produto Vendido (1266566) é multiselect — um lead pode ter vários produtos
- Permanência Mínima (1268610) indica meses de contrato
