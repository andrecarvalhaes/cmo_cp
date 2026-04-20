---
name: finalizar-task
description: "Finaliza uma pendência/tarefa do ClickUp: adiciona comentário 'IA:' com o que foi feito e move para 'checando resultados'. Use quando o usuário invocar /finalizar-task ou quando terminar de trabalhar em uma tarefa."
---

# Finalizar Task — Report e Transição de Status

Skill de finalização de tarefas. Após concluir o trabalho em uma pendência do ClickUp, reporta o que foi feito via comentário e move a tarefa para "checando resultados".

---

## Passo 1 — Identificar a Tarefa

Identificar qual tarefa do ClickUp foi trabalhada. Fontes (em ordem de prioridade):

1. **Argumento direto**: se o usuário passou URL ou ID (ex: `/finalizar-task 86agz3jp7`)
2. **Contexto da conversa**: se já estava trabalhando em uma tarefa nesta sessão
3. **Perguntar**: se não encontrar, usar `AskUserQuestion`:

```
questions: [
  {
    "question": "Qual tarefa você quer finalizar? Cole a URL ou ID do ClickUp.",
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

## Passo 2 — Buscar Detalhes da Tarefa

Buscar a tarefa via API para confirmar:

```
GET https://api.clickup.com/api/v2/task/{task_id}
Header: Authorization: {CLICKUP_API_KEY}
```

Verificar:
- Nome da tarefa
- Status atual
- Se já está em "checando resultados" ou "concluído" (neste caso, avisar e perguntar se quer prosseguir mesmo assim)

---

## Passo 3 — Montar o Resumo

Construir um resumo do que foi feito baseado no contexto da conversa. O resumo deve:

- Ser escrito em **tom humano**, como um colega reportando
- Começar com **"IA:"** para diferenciar de comentários humanos
- Incluir:
  - O que foi investigado/analisado/implementado
  - Resultados concretos (dados, métricas, testes que passaram)
  - Se houve mudanças em sistemas (N8N, Supabase, ClickUp, código), listar quais
  - Se ficou alguma pendência ou ponto de atenção
- Ser conciso mas completo (máx 10-15 linhas)
- **NÃO usar linguagem técnica/dev** na descrição

**Formato:**
```
IA: [Resumo do que foi feito]

O que foi feito:
- [item 1]
- [item 2]

Resultado: [resultado principal]

[Se houver] Pontos de atenção:
- [ponto 1]
```

---

## Passo 4 — Postar Comentário no ClickUp

```
POST https://api.clickup.com/api/v2/task/{task_id}/comment
Header: Authorization: {CLICKUP_API_KEY}
Content-Type: application/json

{
  "comment_text": "{resumo_montado_no_passo_3}"
}
```

---

## Passo 5 — Mover para "checando resultados"

```
PUT https://api.clickup.com/api/v2/task/{task_id}
Header: Authorization: {CLICKUP_API_KEY}
Content-Type: application/json

{
  "status": "checando resultados"
}
```

---

## Passo 6 — Confirmar ao Usuário

Exibir confirmação curta:

```
Tarefa finalizada:
- Comentário adicionado com resumo do trabalho
- Status: checando resultados
- Link: {url_da_tarefa}
```

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
- Comentários sempre começam com **"IA:"**
- Tom humano, sem linguagem técnica
- Se a tarefa já estiver em "checando resultados" ou "concluído", avisar antes de sobrescrever
- Se não houve trabalho real na sessão (conversa vazia ou só perguntas), **não finalizar** — avisar o usuário
- Credenciais: `.env` do projeto (`CLICKUP_API_KEY`)
