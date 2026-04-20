# N8N — Integração API

## Conexão
- **URL**: https://n8n.data.clubpetro.com/
- **Auth**: Header `X-N8N-API-KEY` (JWT)
- **Status**: ✅ Conectado e validado

## Escopo
- Instância compartilhada por **todos os times** (não apenas marketing)
- Acesso para: **consultar, revisar e construir automações** sob demanda do CMO
- NÃO mapear todos os flows preventivamente — consultar quando necessário

## Endpoints Disponíveis

### Workflows
- `GET /api/v1/workflows` — listar workflows (paginado, `?limit=N&cursor=X`)
- `GET /api/v1/workflows/{id}` — detalhes de um workflow específico
- `POST /api/v1/workflows` — criar workflow
- `PUT /api/v1/workflows/{id}` — atualizar workflow
- `DELETE /api/v1/workflows/{id}` — deletar workflow
- `POST /api/v1/workflows/{id}/activate` — ativar
- `POST /api/v1/workflows/{id}/deactivate` — desativar

### Executions
- `GET /api/v1/executions` — listar execuções
- `GET /api/v1/executions/{id}` — detalhes de uma execução

### Credentials
- `GET /api/v1/credentials` — listar credenciais configuradas

## Dados por Workflow
Cada workflow retorna: id, name, active, tags, nodes (completo), connections, createdAt, updatedAt

## Ferramentas Conectadas (observado nos primeiros workflows)
- Supabase
- Google Sheets
- Discord (webhooks)
- Evolution API (WhatsApp)
- Person Check API (CPF)
- Core ClubPetro API (cadastro clientes)

## Credenciais (IDs para usar em workflows)
- **Supabase (Com&Mkt)**: `{"supabaseApi": {"id": "E124roxIkDjglv24", "name": "Supabase - [Com&Mkt]"}}` — USAR ESTA para nós Supabase do marketing
- **Supabase RPC Service Role**: `{"httpHeaderAuth": {"id": "2KgWpUCUPtxUS89C", "name": "Supabase RPC - Service Role"}}` — para chamadas RPC via HTTP Request
- **Google Sheets**: `{"googleSheetsOAuth2Api": {"id": "OL50dab7dT1eN5gq", "name": "sheets_andre"}}`
- **Evolution API (WhatsApp)**: `{"httpHeaderAuth": {"id": "4nttNefSqX8Fk0qT", "name": "Evolution API - WhatsApp"}}`

## Como Usar
- Para ver workflows de marketing: buscar por nome/tag contendo "marketing", "inbound", "comercial"
- Para criar automação: usar `POST /api/v1/workflows` com JSON do workflow
- Para debugar: consultar execuções via `/api/v1/executions?workflowId={id}`
- **IMPORTANTE**: Sempre recriar workflow (DELETE + POST) em vez de múltiplos PUTs — updates repetidos podem corromper o estado interno
- **IMPORTANTE**: NÃO usar `responseMode: "responseNode"` no webhook a menos que exista um nó "Respond to Webhook" no fluxo
