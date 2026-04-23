# ClickUp — Integração API REST

## Conexão
- **Acesso**: API REST v2 (key no `.env` do projeto)
- **Base URL**: `https://api.clickup.com/api/v2`
- **Header**: `Authorization: {CLICKUP_API_KEY}`
- **Workspace ID**: 9007133809
- **Space**: Marketing & Comercial (ID: 90070422586)
- **Status**: ✅ Conectado e validado

## Pipe de Trabalho

O time é dividido em **duas pipes**:
1. **Sprint** → Social Media, Analista de Conteúdo, Revisor, Copy
2. **Kanban** → Design e Videomaker

### Backlogs (entrada de trabalho)

#### Backlog Melhorias (list 901323662979)
- **URL**: https://app.clickup.com/9007133809/v/li/901323662979
- **Uso**: Melhorias estratégicas e projetos
- **Statuses**: a priorizar → a fazer → fazendo → checar → done, impedimento

#### Backlog Rotina (list 901326735121)
- **URL**: https://app.clickup.com/9007133809/v/li/901326735121
- **Uso**: Calendário de conteúdo e entregas recorrentes (posts, newsletters, blogs, aulões, ebooks)

### Execução

#### Sprint do Time (folder 901315877931 "Receitas | 2026")
- **URL**: https://app.clickup.com/9007133809/v/f/901315877931/90070422586
- **Quem**: Social Media, Conteúdo, Revisor, Copy
- **Cadência**: Sprints quinzenais (uma lista por sprint)
- **Sprint 8**: 4/6 - 4/20 (list 901323659581)
- **Sprint 7**: 3/16 - 4/5 (list 901323659578)

#### Kanban Design (list 901300892447)
- **URL**: https://app.clickup.com/9007133809/v/li/901300892447
- **Quem**: Designers e Videomakers
- **Uso**: Pipeline contínuo de demandas visuais (feed, carrosséis, reels, banners, criativos)

## Time de Marketing

### Liderança
| Nome | ID | Cargo | Pipe | Observação |
|---|---|---|---|---|
| **André Carvalhaes** | 55002108 | Diretor (CMO) | Sprint | Hands-on — ajuda na mão de obra quando time está lento |
| **Bianca Salim** | 44243473 | Coordenadora do time | Sprint | Puxa copy + revisões além da coordenação |
| **Felipe Galo** | 82079060 | Coordenador de Criação | Kanban | Lidera design + produz (feeds, stories, criativos, campanhas) |

### Sprint (Social Media, Conteúdo, Revisor, Copy)
| Nome | ID | Função | Observação |
|---|---|---|---|
| **Lucas Pereira Miranda** | 44243742 | Analista de Conteúdo | Copy, notícias, blog |
| **Bernardo Bueno** | 248459771 | Social Media | Posts Instagram, carrosséis, stories |
| **Gustavo Zirpoli** | 44243471 | Webdesigner | Site (Webflow) |

### Kanban (Design, Videomaker)
| Nome | ID | Função | Observação |
|---|---|---|---|
| **Ederson Carlos** | 44243475 | Designer | Feeds, carrosséis, banners email, artes |
| **Henrique Felix** | 100085870 | Videomaker/Motion | Reels, shorts, edição de vídeo |

### Outras iniciativas (ClubPosto + Pista Digital)
| Nome | ID | Cargo | Observação |
|---|---|---|---|
| **Heitor de Paula Rosa** | 88028989 | Analista de Negócio | Toca ClubPosto e Pista Digital — conversar em outro momento |
| **Alice Marques** | 284571291 | Analista de Negócio | ClubPosto (compra coletiva, novos produtos) — conversar em outro momento |

### Saiu / Mudou
| Nome | ID | Observação |
|---|---|---|
| Gabriel Premoli | 152674086 | Tarefas antigas no Backlog Melhorias, sem atividade recente |

## Velocity (tarefas concluídas por sprint)

| Sprint | Período | Concluídas |
|---|---|---|
| Sprint 2 | 1/5 - 1/18 | 5 (ramp-up) |
| Sprint 3 | 1/19 - 2/1 | 49 |
| Sprint 4 | 2/2 - 2/15 | 61 |
| Sprint 5 | 2/16 - 3/1 | 44 |
| Sprint 6 | 3/2 - 3/15 | 35 |
| Sprint 7 | 3/16 - 4/5 | 53 |
| Sprint 8 | 4/6 - 4/20 | 80 (em andamento 18/Abr) |

**Velocity médio (Sprints 3-7): 48,4 tarefas/sprint**

**IMPORTANTE**: Tarefas vivem nos backlogs e são **adicionadas** nas sprints como lista secundária.
A API `filter_tasks` NÃO retorna essas tarefas — usar `clickup_search` com filtro de `subcategories` (list_id da sprint).

## Métricas CMO Disponíveis

Com o ClickUp consigo acompanhar:
- **Velocity**: tarefas concluídas por sprint (via search)
- **WIP**: tarefas "fazendo" em qualquer momento
- **Backlog health**: tarefas "a priorizar" vs "a fazer"
- **Distribuição**: carga por membro do time
- **Impedimentos**: tarefas bloqueadas

## Fluxo de Criação de Tarefas — Kanban Design

Pipeline automatizado para criar tarefas no kanban dos designers (Marketing 2.0 / Implantação 2.0):

1. **Forms de solicitação**: `C:\Users\ClubPetro-123\Documents\forms_mkt`
   - Formulários que o time preenche para solicitar demandas de design
2. **N8N workflow**: https://n8n.data.clubpetro.com/workflow/V5X0rAPeYUzsYcbw
   - Automação que recebe o form e cria a tarefa no ClickUp
3. **Kanban Design** (destino): list 901300892447
   - URL: https://app.clickup.com/9007133809/v/li/901300892447

**Bug resolvido (Abr/2026)**: texto com caracteres especiais (acentos, cedilha) chegava corrompido no kanban. Causa: encoding — mesma regra do CLAUDE.md (usar Python urllib com UTF-8, nunca curl para texto com acentos).

## Como Consultar (API REST)

### Tarefas de uma lista
```bash
curl -s "https://api.clickup.com/api/v2/list/{list_id}/task" -H "Authorization: $CLICKUP_API_KEY"
```

### Tarefas da sprint atual
```bash
curl -s "https://api.clickup.com/api/v2/list/{sprint_list_id}/task?statuses[]=a%20fazer&statuses[]=fazendo" -H "Authorization: $CLICKUP_API_KEY"
```

### Criar tarefa
```bash
curl -s -X POST "https://api.clickup.com/api/v2/list/{list_id}/task" \
  -H "Authorization: $CLICKUP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"...", "description":"...", "priority": 3}'
```

### Adicionar comentário
```bash
curl -s -X POST "https://api.clickup.com/api/v2/task/{task_id}/comment" \
  -H "Authorization: $CLICKUP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"comment_text":"IA: ..."}'
```
