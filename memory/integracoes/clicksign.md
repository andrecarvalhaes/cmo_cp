# Clicksign — Integração Assinatura Eletrônica

## Conexão
- **Credenciais**: `vm_app_keys` (Supabase) — `CLICKSIGN_API_KEY` + `CLICKSIGN_ENVIRONMENT`
- **Ambiente**: production
- **API base**: `https://app.clicksign.com/api/v1` (production) / `https://sandbox.clicksign.com/api/v1` (sandbox)
- **Autenticação**: query param `?access_token=API_KEY`

## Status no Vendemais
- **ConfiguracaoAPIKeys.tsx**: Card de configuração + teste de conexão (GET /documents?limit=1) ✅
- **clicksign-proxy** (Edge Function): proxy server-side para Clicksign API, evita CORS ✅
- **clicksignService.ts**: `dispatchContract()` via fetch direto à edge function ✅
- **contractGenerator.ts**: loadTemplate + fillTemplate (docxtemplater `{{}}`) + buildVariables (45 vars) ✅
- **ContractDataScreen.tsx**: Checkboxes reuso telefone/email, Kommo read-only, dias fixos 30 ✅
- **Fluxo de disparo**: Upload doc → criar signatários → add ao doc (3 grupos) → notificação grupo 1 ✅
- **Validação final**: Pendente — testar pela interface (botão GERAR CONTRATO) e confirmar email ao Moisés

### Bugs resolvidos
1. Template `Duplicate open tag` → delimiters `{{ }}` no docxtemplater
2. CORS → Edge Function `clicksign-proxy` como proxy server-side
3. `supabase.functions.invoke()` → fetch direto (compatibilidade headers)
4. Notificação 404 → usar `request_signature_key` (não `list.key`)
5. Empty body 202 → handler `if (!text) return { success: true }`

## Fluxo de Assinatura do Contrato ClubPetro
Grupos sequenciais:
1. **Grupo 1 — Testemunha**: Moisés Soares (moises.soares@clubpetro.com.br, CPF 116.872.696-45, nasc 27/01/1991)
2. **Grupo 2 — Cliente + Testemunha**: Representante Legal (dados do fluxo) + André Carvalhaes (andre.carvalhaes@familiapires.com.br, CPF 130.753.826-63, nasc 18/07/1997)
3. **Grupo 3 — Contratada**: Ricardo Pires (ricardo@clubpetro.com.br, CPF 047.768.946-96, nasc 17/09/1980)

## Variáveis do Contrato (45 total)
### Já coletadas no fluxo Vendemais (~16):
- Razão Social, CNPJ, endereço completo (via BrasilAPI)
- Nome/CPF/Email Representante Legal (signerInfo)
- Módulos selecionados, MRR calculado

### Faltam (~15) — precisam de nova tela:
- Nome Fantasia, Complemento endereço
- Telefone Representante Legal, Telefone Empresa
- E-mail faturamento, WhatsApp faturamento
- Tempo de Permanência Mínima
- Parcelas implantação (NPS1, VPS1, D1), App personalizado (NPS2, VPS2, D2)
- Valores individuais por módulo (VPS3-5), VED, VSMS
- Data 1º vencimento (D3)
- Testemunha 2: Moisés Soares / 116.872.696-45 (fixo)

## Tarefa ClickUp
- ID: 86agzzr3y
- Link: https://app.clickup.com/t/86agzzr3y
