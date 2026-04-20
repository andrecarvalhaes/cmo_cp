# Pluri (Discadora) — Integração API

## Conexão
- **URL**: `https://clubpetro.acessocloud.com/ws/index.php`
- **Método**: POST form-urlencoded
- **Auth**: parâmetro `vToken` no body
- **Credenciais**: `.env` do projeto (`PLURI_TOKEN` e `PLURI_URL`)
- **IMPORTANTE**: token é base64 e PRECISA do `=` de padding no final. Usar `quote_via=urllib.parse.quote` no urlencode para não converter `+` e `=`
- **Status**: ✅ Conectado e validado

## Endpoints Disponíveis

### 1. Ligações de Campanha (discador automático / outbound)
```
POST /ws/index.php
vToken=...&vApp=Telecom&vMetodo=Chamada&vAct=getRetCampanha&vDataInicio=DD/MM/YYYY HH:MM:SS&vDataFim=DD/MM/YYYY HH:MM:SS
```
- Lista fria sobem, discador liga automaticamente, hunter tabula resultado
- Contact rate ~1,4% (maioria falha técnica do discador)
- Tabulação positiva → cria lead Outbound no Kommo via N8N

### 2. Ligações Manuais (touchpoints na pipeline)
```
POST /ws/index.php
vToken=...&vApp=Telecom&vMetodo=Chamada&vAct=getRetLigSainte&vDataInicio=DD/MM/YYYY HH:MM:SS&vDataFim=DD/MM/YYYY HH:MM:SS
```
- Hunters ligam manualmente para leads já na pipeline do Kommo
- Contact rate ~66% (muito superior ao discador)
- Campos: clid (nome hunter), destino, status, tabulacao, duracao, conversa, url_gravacao
- Operador = ID numérico (nome vem no campo clid)
- url_gravacao = link MP3 da gravação quando atendida

## Campos Retornados por Ligação

| Campo | Descrição | Exemplo |
|---|---|---|
| campanha_nome | Nome da campanha (com tag entre []) | [Feira_ipatinga] Campanha feira... |
| operador | Hunter que atendeu | Camila Torres |
| nome | Nome do contato | MARIA RISETE FIORIN |
| nome_empresa | Nome da empresa | (igual nome ou razão social) |
| cnpj | CNPJ do lead | 42.309.849/0001-91 |
| cidade | Cidade | RIO DE JANEIRO |
| uf | Estado | RJ |
| destino | Telefone discado | (21) 98179-6240 |
| tabulacao | Resultado da ligação | Em tratamento, Sem interesse... |
| status | Status técnico da chamada | Atendida, Falha, Abandono |
| duracao | Duração em segundos | 27 |
| conversa | Tempo de conversa | 00:02:30 |
| data | Data/hora da ligação | 2026-04-17 17:26:40 |
| obs_tabulacao | Observação do hunter | texto livre |
| integracao | Origem da lista | Qualify |
| id_campanha | ID numérico da campanha | 257 |
| url_gravacao | Link para gravação | (quando disponível) |
| bairro, endereco, cpf, data_nascimento | Dados adicionais do lead | (nem sempre preenchidos) |

## Tabulações (resultado da ligação)

### Positivas (geram lead no Kommo via N8N)
- **Em tratamento** → cria oportunidade Outbound no Kommo
- **Reunião agendada** → disparo de agendamento

### Negativas (não geram lead)
- **Não é posto** → black_list (Supabase)
- **Está com o concorrente** → lista_espera (Supabase)
- **Sem interesse** → lista_espera (Supabase)
- **Parceiro** → parceiro (Supabase)
- **Ligação falhou** → cria oportunidade para retry
- **Já é cliente** → descartado
- **Atendeu e desligou** → descartado
- **Caixa postal** → descartado

### Técnicas
- **Falha** — discador não conseguiu conectar (maioria das ligações)
- **Abandono** — conectou mas caiu antes de atender
- **Não atendida** — tocou mas ninguém atendeu

## Fluxo Atual (N8N)

```
Pluri API (getRetCampanha) → Split por ligação → Filter (status != Falha)
→ Switch por tabulação:
  - "Em tratamento" / "Ligação falhou" → Criar lead Kommo (Outbound, pipeline 8166623, status 65190271)
  - "Não é posto" → Supabase black_list
  - "Concorrente" / "Sem interesse" → Supabase lista_espera
  - "Parceiro" → Supabase parceiro
  - "Reunião agendada" → Disparo agendamento
```

**Schedule**: Roda 2x/dia (12:45 e 19:30)

## Snapshot 17/Abr/2026

### Campanha (discador automático)
| Métrica | Valor |
|---|---|
| Total ligações | 887 |
| Falha (não conectou) | 846 (95,4%) |
| Abandono | 28 (3,2%) |
| Atendida | 12 (1,4%) |
| Contact rate efetivo | **1,4%** |

**Campanhas ativas:**
- Campanha inicial de hunters 25/03 (374 calls)
- Troca de lista Paulo 04/03 (207 calls)
- Workshop São Luís 06/03 (174 calls)
- Campanha 90k+ 25 postos (67 calls)
- Feira Ipatinga (65 calls)

**Hunters (campanha):** Camila Torres (6), Cibely Cristina (4), Daniel Oliveira (2)

### Manuais (touchpoints pipeline)
| Métrica | Valor |
|---|---|
| Total ligações | 168 |
| Atendida | 111 (66,1%) |
| Não atendida | 46 (27,4%) |
| Ocupada | 10 (6,0%) |
| Contact rate efetivo | **66,1%** |

**Hunters (manual):** Operador 5 (74), Op.25 (50), Op.12 (34), Op.8 (10)
- Gravações disponíveis via url_gravacao (MP3)

## Métricas CMO Disponíveis

Com esta API consigo calcular:
- **Contact rate**: Atendidas / Total (excl. Falha técnica)
- **Conversion por tabulação**: distribuição de resultados
- **Volume por campanha**: quais campanhas geram mais contatos
- **Performance por hunter**: calls/dia, taxa de tabulação positiva
- **Eficiência do discador**: % falha técnica vs tentativas reais
- **Custo por connected call**: se cruzar com DRE (custo Pluri)

## Relação com Outras Integrações

| Dado | Pluri | N8N | Kommo |
|---|---|---|---|
| Ligação bruta | Fonte primária | Processa | Não |
| Lead outbound | Origem | Cria via API | Destino (pipeline) |
| Tabulação | Fonte primária | Roteia | Campo custom 1286197 |
| Hunter | operador | Passa | Campo 1265304 |
| Campanha | campanha_nome | Passa como suborigem | Campo 1266176 |
