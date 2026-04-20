---
name: testar-task
description: "Testa e valida o trabalho feito em uma tarefa do ClickUp. Identifica o que foi implementado, desenha e executa testes apropriados, e reporta os resultados. Use quando o usuário invocar /testar-task."
---

# Testar Task — Validação do Trabalho Realizado

Skill de teste e validação. Quando o usuário quer checar se algo que foi implementado está funcionando corretamente, esta skill identifica o que precisa ser testado, executa os testes e reporta os resultados.

---

## Passo 1 — Identificar a Tarefa

Identificar qual tarefa do ClickUp precisa ser testada. Fontes (em ordem de prioridade):

1. **Argumento direto**: se o usuário passou URL ou ID (ex: `/testar-task 86agz3jp7`)
2. **Contexto da conversa**: se já estava trabalhando em uma tarefa nesta sessão
3. **Perguntar**: se não encontrar, usar `AskUserQuestion`:

```
questions: [
  {
    "question": "Qual tarefa você quer testar? Cole a URL ou ID do ClickUp.",
    "header": "Tarefa",
    "multiSelect": false,
    "options": [
      {"label": "Da conversa", "description": "A tarefa que acabamos de trabalhar nesta sessão"},
      {"label": "Outra", "description": "Vou informar a URL ou ID"}
    ]
  }
]
```

---

## Passo 2 — Buscar Contexto da Tarefa

Buscar a tarefa e seus comentários via API para entender o que foi feito:

```
GET https://api.clickup.com/api/v2/task/{task_id}
GET https://api.clickup.com/api/v2/task/{task_id}/comment
Header: Authorization: {CLICKUP_API_KEY}
```

Analisar:
- Descrição da tarefa (o que era o problema/pedido)
- Comentários "IA:" (o que foi implementado/resolvido)
- Status atual

---

## Passo 3 — Desenhar os Testes

Com base no que foi feito, definir os testes necessários. Categorias comuns:

### 3.1 Automações N8N
- Disparar webhook de teste com payloads controlados
- Verificar se os dados chegaram onde deveriam (ClickUp, Supabase, Google Sheets)
- Testar edge cases (campos vazios, valores extremos)
- Nomear testes com prefixo **"TESTE -"** para fácil identificação e limpeza

### 3.2 Dados / Queries
- Executar queries e validar resultados esperados
- Verificar consistência entre fontes (Kommo vs Supabase, DRE vs Kommo)
- Checar se filtros estão funcionando

### 3.3 Integrações API
- Testar endpoints com requests controlados
- Validar formato de resposta
- Testar autenticação

### 3.4 Processos ClickUp
- Verificar se campos custom estão sendo preenchidos
- Checar se statuses estão transitando corretamente
- Validar assignees e subtasks

---

## Passo 4 — Apresentar Plano de Teste

Antes de executar, apresentar o plano ao usuário:

```markdown
## Plano de Teste — [Nome da Tarefa]

Vou executar os seguintes testes:

| # | Teste | O que valida | Impacto |
|---|-------|-------------|---------|
| 1 | [desc] | [o que valida] | [baixo/médio/alto] |
| 2 | [desc] | [o que valida] | [baixo/médio/alto] |

**Dados de teste serão criados com prefixo "TESTE -" e deletados ao final.**

Posso executar?
```

Aguardar confirmação do usuário antes de prosseguir.

---

## Passo 5 — Executar os Testes

Executar cada teste sequencialmente:

1. **Preparar** — criar dados/payloads de teste
2. **Executar** — disparar a ação (webhook, query, API call)
3. **Aguardar** — dar tempo para processamento async (sleep 5-15s para webhooks N8N)
4. **Validar** — verificar se o resultado bate com o esperado
5. **Registrar** — anotar resultado (PASSOU / FALHOU + detalhe)

---

## Passo 6 — Limpar Dados de Teste

Após todos os testes, **SEMPRE** limpar os dados criados:
- Deletar tarefas ClickUp com prefixo "TESTE -"
- Deletar rows de teste no Supabase
- Qualquer outro dado temporário

---

## Passo 7 — Reportar Resultados

### 7.1 Resultado Geral

```markdown
## Resultado dos Testes — [Nome da Tarefa]

**Status: X/Y testes passaram** [APROVADO / REPROVADO]

| # | Teste | Resultado | Detalhe |
|---|-------|-----------|---------|
| 1 | [desc] | PASSOU | [detalhe] |
| 2 | [desc] | FALHOU | [o que deu errado] |

[Se REPROVADO]
### Problemas Encontrados
- [Problema 1]: [descrição + sugestão de fix]
- [Problema 2]: [descrição + sugestão de fix]

### Dados de teste
- Todos os dados de teste foram limpos
```

### 7.2 Se Todos Passaram

Perguntar ao usuário:

```
questions: [
  {
    "question": "Todos os testes passaram. O que quer fazer com a tarefa?",
    "header": "Ação",
    "multiSelect": false,
    "options": [
      {"label": "Concluir", "description": "Mover para 'concluído' e adicionar comentário de aprovação"},
      {"label": "Manter", "description": "Deixar em 'checando resultados' por enquanto"},
      {"label": "Mais testes", "description": "Quero testar mais alguma coisa"}
    ]
  }
]
```

Se "Concluir":
- Adicionar comentário "IA:" com resultado dos testes
- Mover status para "concluído"

### 7.3 Se Algum Falhou

- Adicionar comentário "IA:" na tarefa com os problemas encontrados
- Mover status de volta para "fazendo"
- Sugerir próximos passos para correção

---

## Referência — Statuses da Lista ClubPetro (901326908797)

| Status | Tipo |
|--------|------|
| a planejar | open |
| a priorizar | unstarted |
| a fazer | unstarted |
| fazendo | custom |
| checar | custom |
| impedimento | custom |
| documentando | custom |
| checando resultados | done |
| concluído | closed |

---

## Regras

- Toda comunicação em **português brasileiro**
- Comentários no ClickUp sempre começam com **"IA:"**
- Tom humano nos comentários
- **SEMPRE limpar dados de teste** ao final (deletar tarefas TESTE, rows temporários etc.)
- Nomear dados de teste com prefixo "TESTE -" para fácil identificação
- Se os testes envolvem sistemas de produção (N8N webhooks que criam tarefas reais), avisar o usuário antes
- Se não souber o que testar (tarefa sem contexto de implementação), perguntar ao usuário o que quer validar
- Credenciais: `.env` do projeto (`CLICKUP_API_KEY`, `N8N_API_KEY`, etc.)
