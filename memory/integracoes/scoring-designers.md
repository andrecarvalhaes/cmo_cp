# Scoring de Designers — vm_interno_mkt

## Visão Geral
Tabela `vm_interno_mkt` (Supabase) registra pontuação dos designers (Felipe Galo, Ederson Carlos, Henrique Felix) com base em tarefas concluídas no ClickUp.

## Arquitetura
- **Fonte**: Lista "Marketing 2.0" (ClickUp, ID: `901300892447`)
- **Automação**: N8N workflow `V5X0rAPeYUzsYcbw` ("[MKTCOM] solicitacao_marketing")
- **Tipo**: Event-driven via ClickUp Trigger (dispara quando tarefa muda de status)
- **Destino**: Supabase `vm_interno_mkt`
- **Leitura**: Vendemais → DashboardDesign.tsx (hooks: useDesignMetrics, useDesignMetricsDetailed, useDesignOperadores)

## Colunas da Tabela
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | bigint | PK auto |
| created_at | timestamptz | Quando o registro foi inserido |
| nome | text | Nome da tarefa |
| user | text | Nome do designer |
| score | numeric | Pontuação do entregável |
| due_date | date | Prazo da tarefa |
| id_task | text | ID da tarefa no ClickUp (nem sempre preenchido) |
| data_entrega_designer | timestamptz | Data real de entrega (raramente preenchido) |

## Tabela de Scoring por Tipo de Entregável
| Tipo | Score | Exemplos |
|------|-------|----------|
| TIER 3 (solicitação simples) | 1 | "TIER 3: Atualização no CRM" |
| banner-site | 2 | alteração simples de banner |
| banner-email, EMAIL, Thumb, banner-blog | 3 | "banner-email (1)", "EMAIL 02: Educação", "Thumb com data" |
| feed-1-tela, stories-1-tela, feed estático, stories estático, Whatsapp, feed-stories-organico, feed-stories-ads, pop-up, impresso simples, [CAMPANHA] criativos | 4 | "feed-1-tela (2)", "stories-3 desconto preço", "Whatsapp (Grupo de Inscritos): 01" |
| reels-shorts-edicao | 5 | edição de vídeo para reels/shorts |
| reels-shorts-motion, stories com (motion) | 6 | motion design para reels/shorts |
| carrossel-feed, carrossel-stories, stand/feira impresso, apresentação, ebook-cartilha (simples) | 10 | "carrossel-feed (3)", "arte para stand Feira" |
| ebook-cartilha (completo), id-visual, reels-shorts-motion (complexo), apresentação institucional | 20 | "ebook aulão Pista Digital", "id-visual (1)" |

## Statuses ClickUp (lista Marketing 2.0)
- `a fazer` (open) → `impedimento` (unstarted) → `fazendo` (custom) → `checar` (done) → `concluído` (closed)

## Vulnerabilidade: Gap por Desconexão do ClickUp Trigger
**Problema**: O ClickUp Trigger do N8N pode desconectar silenciosamente. Quando isso acontece, tarefas concluídas no período NÃO são registradas no Supabase. O trigger não reprocessa eventos perdidos.

**Como detectar**: Comparar contagem diária de registros em `vm_interno_mkt` — se houver dias sem nenhum registro durante dias úteis, há gap.

**Como reprocessar manualmente**:
1. Puxar tarefas concluídas via API ClickUp:
   ```
   GET /api/v2/list/901300892447/task?statuses[]=checar&statuses[]=concluído&date_done_gt={ts_ms}&date_done_lt={ts_ms}&include_closed=true&subtasks=true
   ```
2. Filtrar por designers (Felipe Galo, Ederson Carlos, Henrique Felix)
3. Aplicar tabela de scoring acima com base no nome da tarefa
4. Verificar duplicatas contra registros existentes no Supabase
5. INSERT no `vm_interno_mkt` (nome, user, score, due_date, id_task)

**Incidente abr/2026**: Trigger desconectou ~10/abr, reconectou ~18/abr. 56 tarefas reprocessadas manualmente em 20/abr.
