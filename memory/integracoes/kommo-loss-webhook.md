# Webhook Kommo → RD Station: Sincronizar Perdidos

## Resumo
Edge Function `kommo-loss-webhook` (v5) no Supabase recebe webhook do Kommo quando um lead é movido para "Venda Perdida" (status 143) e sincroniza com o RD Station.

## URL
`https://azmtxhjtqodtaeoshrye.supabase.co/functions/v1/kommo-loss-webhook`

## Fluxo
1. Kommo envia webhook (form-urlencoded) ao mudar status do lead
2. Function filtra: só processa status_id === 143
3. Checa idempotência (5 min window na tabela de log)
4. GET Kommo /leads/{id}?with=contacts,custom_fields_values
5. Determina motivo de perda real (lógica Hunter/Closer)
6. Extrai email do contato vinculado
7. RD Station:
   - GET contato por email → obtém UUID
   - PUT /funnels/default → desmarca oportunidade
   - POST /events → OPPORTUNITY_LOST
   - PATCH /contacts/uuid:{uuid} → atualiza cf_motivo_de_perda_hunter ou _closer

## Lógica de Motivo de Perda
- Campo Hunter: 1288043, Campo Closer: 1277082
- Se Hunter = "Sou Closer" (enum 936487) → usar motivo do Closer → cf_motivo_de_perda_closer
- Se Closer = "Sou Hunter" (enum 936489) → usar motivo do Hunter → cf_motivo_de_perda_hunter
- Senão: usar o campo preenchido

## Mapeamento Kommo → RD Station
Os campos cf_motivo_de_perda_hunter e cf_motivo_de_perda_closer no RD são select lists com opções fixas diferentes dos nomes no Kommo. A function mapeia 20 motivos Hunter e 15 motivos Closer do Kommo para as opções válidas do RD.

### Hunter (20 motivos → 24 opções RD)
Principais mapeamentos:
- No-Show → "No-show"
- Tentativas esgotadas → "Tentativas de contato esgotadas"
- Timing/Outras prioridades → "Tempo - Não é a hora para falar"
- Concorrente/Fidelidade → "Concorrência - Já possui programa de fidelidade"
- Incompatibilidade técnica → "Placa de automação incompatível"
- Não é posto → "Não é posto de combustíveis"
- Já é cliente → "Negócio duplicado - Já é cliente"

### Closer (15 motivos → 11 opções RD)
Principais mapeamentos:
- Concorrência → "Concorrência - Está negociando com outra empresa"
- Mensalidade/Budget → "Orçamento - Falta de Budget"
- App/Funcionalidades/Medo → "Lead alegou que não viu valor"
- ERP/Smart POS/Timing → "Tempo - Troca do sistema de gestão"
- Resistência/Estrutura → "Perfil inadequado"

## Tabela de Log
`webhook_kommo_loss_log`:
- id, created_at, kommo_lead_id, contact_email
- loss_role (hunter/closer), loss_reason
- rd_contact_found, rd_opp_unmarked, rd_event_posted, rd_field_updated
- status (processing/success/error), error_message, duration_ms
- rd_debug (JSONB com detalhes das respostas RD)

## Credenciais (vm_app_keys)
- KOMMO_ACCESS_TOKEN
- RD_ACCESS_TOKEN (refresh automático em 401)
- RD_REFRESH_TOKEN
- RD_CLIENT_SECRET
- RD_CLIENT_ID hardcoded: c66161a0-febd-4db7-ba94-40d0fcf110f5

## Observações
- Sempre retorna 200 para o Kommo (evita retries infinitos)
- verify_jwt = false (webhook público, sem auth header do Kommo)
- Leads sem email no contato Kommo = registrados como erro no log
- Token RD refresh automático: tenta chamada, se 401 faz refresh, salva no vm_app_keys, retry
- ClickUp task: https://app.clickup.com/t/86ah1y8dt
