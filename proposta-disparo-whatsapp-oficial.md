# Proposta: Estrutura Profissional de Disparos WhatsApp via Meta API

## Diagnóstico do Fluxo Atual

**Workflow:** `[MKTCOM] disparo-oficial` (ID: `opcRr4ghzhOj7uHS`) — ATIVO

O fluxo tem duas partes: **envio** e **recebimento de feedback**.

### Envio (parte superior)
```
Manual Trigger → Google Sheets (Página3, filtra "recebeu" vazio)
  → Loop Over Items → HTTP Request (Meta API, template "clube_ale")
  → Wait 2s → volta pro Loop
```
- Existe um node Supabase (`Get many rows` de `vm_telefones`) **desconectado** — parece ter sido a intenção original, mas foi abandonado em favor do Google Sheets

### Recebimento de feedback (WhatsApp Trigger)
```
WhatsApp Trigger → resposta de texto? → salva em aux_resposta (Supabase) ✓
                 → clique em botão? → salva em aux_resposta (Supabase) ✓
                 → status update? → Switch:
                     read      → Google Sheets (leu = "Sim")
                     delivered → Google Sheets (recebeu = "Sim")
                     failed    → Google Sheets (recebeu = "Falha")
```

### Problemas identificados

| Área | Problema | Impacto |
|------|----------|---------|
| **Lista** | Google Sheets como fonte — precisa editar planilha manualmente a cada campanha | Trabalho manual, propenso a erro |
| **Lista** | Template hardcoded ("clube_ale") — não reutiliza pra outra campanha | Precisa editar o workflow toda vez |
| **Lista** | Node Supabase desconectado — a infra tá lá mas não funciona | Desperdício de estrutura pronta |
| **Feedback** | Status (delivered/read/failed) vai pra Google Sheets | Não é consultável, não escala, não tem histórico |
| **Feedback** | `aux_resposta` não tem contexto de campanha | Impossível saber qual campanha gerou a resposta |
| **Feedback** | Sem métricas agregadas | Não consegue responder "como foi a campanha X?" |
| **Erros** | Zero tratamento de erro no HTTP Request | Se a Meta retorna erro, silenciosamente ignora |
| **Erros** | Sem notificação de falha | Ninguém fica sabendo que deu problema |
| **Erros** | Sem retry | Erro temporário = mensagem perdida |

---

## Proposta: 3 Pilares

### 1. Preparar lista de disparo de forma profissional

**Princípio:** A lista vive no Supabase. O Google Sheets sai de cena como fonte de verdade.

#### Novas tabelas Supabase

**`wpp_campanhas`** — registro de cada campanha/disparo
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | serial PK | |
| nome | text | Ex: "Clube Ale - CE/PI", "Expansão MG - Abril" |
| template_name | text | Nome do template aprovado na Meta (ex: "clube_ale") |
| template_language | text | Default "pt_BR" |
| status | text | "rascunho", "pronta", "disparando", "concluida", "pausada" |
| total_contatos | integer | Preenchido automaticamente |
| enviados | integer | Contadores atualizados pelo webhook |
| entregues | integer | |
| lidos | integer | |
| falhas | integer | |
| respostas | integer | |
| created_at | timestamptz | |
| started_at | timestamptz | Quando começou o disparo |
| finished_at | timestamptz | Quando terminou |

**`wpp_destinatarios`** — cada telefone de cada campanha
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | serial PK | |
| campanha_id | integer FK | Referência à campanha |
| telefone | text | Formato: 5511999999999 |
| nome | text | Para personalização do template |
| dados_extra | jsonb | Campos variáveis do template (ex: nome_posto, regiao) |
| status | text | "pendente", "enviado", "entregue", "lido", "falha" |
| wamid | text | ID da mensagem retornado pela Meta — chave para rastrear |
| erro | text | Mensagem de erro se falhou |
| enviado_at | timestamptz | |
| entregue_at | timestamptz | |
| lido_at | timestamptz | |
| created_at | timestamptz | |

**`wpp_respostas`** — substitui `aux_resposta` com contexto
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | serial PK | |
| campanha_id | integer FK | |
| telefone | text | |
| tipo | text | "texto", "botao", "lista" |
| conteudo | text | O que respondeu |
| created_at | timestamptz | |

#### Como subir uma nova lista

**Opção A — Upload direto no Supabase (recomendado)**
1. Criar a campanha em `wpp_campanhas` (nome, template, status = "rascunho")
2. Importar contatos via CSV no Supabase Table Editor → `wpp_destinatarios` com o `campanha_id`
3. O workflow lê de `wpp_destinatarios WHERE campanha_id = X AND status = 'pendente'`

**Opção B — Via Google Sheets + workflow auxiliar**
1. Preencher uma planilha-padrão (template fixo com colunas: telefone, nome, dados_extra)
2. Um workflow auxiliar lê a planilha e insere em `wpp_destinatarios` vinculado a uma campanha
3. Isso preserva o conforto da planilha mas centraliza os dados no Supabase

Em ambos os casos, **o workflow de disparo nunca toca no Google Sheets como fonte**. Ele sempre lê do Supabase.

#### Como escolher a campanha pra disparar

O workflow principal recebe **um parâmetro**: `campanha_id`. Ao executar manualmente, o operador informa qual campanha quer disparar. O workflow:
1. Busca a campanha em `wpp_campanhas` → pega `template_name` e `template_language`
2. Busca destinatários em `wpp_destinatarios WHERE campanha_id = X AND status = 'pendente'`
3. Faz o loop de envio usando o template da campanha (não mais hardcoded)
4. Após enviar, atualiza o destinatário com `status = 'enviado'` e salva o `wamid`

---

### 2. Acompanhar feedback de forma profissional

**Princípio:** Tudo no Supabase, indexado por campanha. Status em tempo real.

#### Status de entrega (webhook da Meta)

Quando o WhatsApp Trigger recebe um status update:

1. **Identificar o destinatário** pelo `wamid` (ID da mensagem) → busca em `wpp_destinatarios WHERE wamid = X`
2. **Atualizar o status** do destinatário:
   - `delivered` → status = "entregue", entregue_at = now()
   - `read` → status = "lido", lido_at = now()
   - `failed` → status = "falha", erro = mensagem de erro
3. **Incrementar contadores** na campanha (`wpp_campanhas`):
   - UPDATE wpp_campanhas SET entregues = entregues + 1 WHERE id = campanha_id

#### Respostas

Quando recebe mensagem de texto ou clique em botão:
1. Identificar campanha pelo telefone (busca o destinatário mais recente com aquele telefone)
2. Salvar em `wpp_respostas` com campanha_id, tipo e conteúdo
3. Incrementar contador de respostas na campanha

#### Dashboard instantâneo

Com os dados no Supabase, uma query simples dá o panorama:

```sql
SELECT
  nome,
  template_name,
  total_contatos,
  enviados,
  entregues,
  lidos,
  falhas,
  respostas,
  ROUND(100.0 * entregues / NULLIF(enviados, 0), 1) AS taxa_entrega,
  ROUND(100.0 * lidos / NULLIF(entregues, 0), 1) AS taxa_leitura,
  ROUND(100.0 * respostas / NULLIF(enviados, 0), 1) AS taxa_resposta
FROM wpp_campanhas
ORDER BY created_at DESC;
```

Isso substitui completamente o Google Sheets como tracker.

---

### 3. Receber alerta de erros de forma profissional

**Princípio:** Erro tem que gritar. Três camadas de alerta.

#### Camada 1 — Erro no envio (HTTP Request falha)

No loop de disparo, após o HTTP Request:
- **If** status ≠ 200 → salvar erro no `wpp_destinatarios` (campo `erro`) + marcar status = "falha"
- Acumular contagem de falhas consecutivas
- **Se 5 falhas consecutivas** → pausar o disparo, atualizar campanha status = "pausada"

#### Camada 2 — Erro reportado pelo webhook (status = "failed")

Já tratado pelo Switch existente, mas agora ao invés de ir pro Google Sheets:
- Atualiza `wpp_destinatarios` com status "falha" e mensagem de erro
- Incrementa contador de falhas na campanha

#### Camada 3 — Notificação ativa

Criar um node de alerta que dispara quando:
- **Taxa de falha > 10%** em uma campanha → envia email/Discord
- **5 falhas consecutivas** (possível bloqueio) → envia email + pausa o disparo
- **Campanha concluída** → envia resumo com as métricas finais

**Destinos sugeridos:**
- Email (Gmail node já disponível no n8n)
- Discord webhook (já usado em outros workflows do n8n)
- Ou ambos

#### Formato da notificação de erro
```
⚠️ ALERTA DISPARO WHATSAPP

Campanha: [nome]
Template: [template_name]
Situação: 5 falhas consecutivas - DISPARO PAUSADO

Enviados: 342
Entregues: 338
Falhas: 5
Último erro: "Rate limit exceeded"

Link: https://n8n.data.clubpetro.com/workflow/opcRr4ghzhOj7uHS
```

#### Formato do resumo final
```
✅ DISPARO CONCLUÍDO

Campanha: [nome]
Template: [template_name]
Duração: 2h 15min

📊 Resultados:
- Enviados: 1.200
- Entregues: 1.156 (96,3%)
- Lidos: 847 (73,2%)
- Respostas: 89 (7,4%)
- Falhas: 44 (3,7%)
```

---

## Redesenho do Workflow

### Workflow 1: `[MKTCOM] disparo-oficial` (envio)

```
Manual Trigger (input: campanha_id)
  → Supabase: GET wpp_campanhas WHERE id = campanha_id
  → Supabase: UPDATE status = "disparando"
  → Supabase: GET wpp_destinatarios WHERE campanha_id = X AND status = "pendente"
  → Loop Over Items
    → HTTP Request (Meta API, template dinâmico da campanha)
    → IF sucesso:
        → Supabase: UPDATE wpp_destinatarios SET status="enviado", wamid=response.messages[0].id
      ELSE:
        → Supabase: UPDATE wpp_destinatarios SET status="falha", erro=response.error
        → Contagem falhas consecutivas > 5? → PAUSA + ALERTA
    → Wait 2s
    → Volta pro Loop
  → Supabase: UPDATE wpp_campanhas SET status="concluida", finished_at=now()
  → ALERTA: resumo final
```

### Workflow 2: `[MKTCOM] webhook-whatsapp` (recebimento — já existe como parte do mesmo workflow)

```
WhatsApp Trigger
  → É resposta (texto/botão)?
    → Supabase: INSERT wpp_respostas (com campanha_id identificado pelo telefone)
    → Supabase: UPDATE wpp_campanhas SET respostas = respostas + 1
  → É status update?
    → Supabase: busca wpp_destinatarios pelo wamid do status
    → Switch (delivered/read/failed):
      → UPDATE wpp_destinatarios com novo status + timestamp
      → UPDATE wpp_campanhas incrementa contador
      → Se "failed" e taxa > 10%: ALERTA
```

---

## O que muda na prática operacional

| Antes | Depois |
|-------|--------|
| Editar Google Sheets com lista de telefones | Criar campanha no Supabase + importar CSV |
| Editar workflow pra mudar template | Informar campanha_id ao executar — template vem do BD |
| Checar planilha pra ver quem recebeu/leu | Query SQL ou view no Supabase com métricas em tempo real |
| Não saber se deu erro | Alerta por email/Discord + pausa automática |
| Sem histórico de campanhas | Tabela `wpp_campanhas` com todo o histórico |
| `aux_resposta` sem contexto | `wpp_respostas` vinculada à campanha |

## Próximos passos

1. **Criar as 3 tabelas** no Supabase (`wpp_campanhas`, `wpp_destinatarios`, `wpp_respostas`)
2. **Refatorar o workflow de envio** para ler do Supabase + template dinâmico + tratamento de erro
3. **Refatorar o webhook** para gravar no Supabase (não mais Google Sheets)
4. **Adicionar alertas** (email ou Discord)
5. **Testar com campanha piloto** de ~50 contatos
6. **Migrar dados da `aux_resposta`** para `wpp_respostas` (39 registros)
