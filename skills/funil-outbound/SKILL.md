---
name: funil-outbound
description: "Reporta o status do time comercial no funil outbound com métricas vs metas, tendências e pontos de atenção ranqueados. Puxa dados da Pluri (ligações) e Kommo (cards até vendas). Use quando o usuário invocar /funil-outbound."
---

# Funil Outbound — Report do Time Comercial

Skill de monitoramento do funil outbound. Puxa dados reais da Pluri e Kommo, monta o funil completo (Ligações → Cards → Qualificados → Agendas → Shows → Vendas → MRR), compara com metas e entrega pontos de atenção ranqueados por impacto.

**Inspirações:** Revenue Operations + SaaS Metrics Coach (alirezarezvani/claude-skills), Pipeline Management Framework, SDR Benchmarks (Apollo, Crunchbase, Autobound)

---

## Passo 1 — Perguntas Iniciais

Antes de qualquer análise, fazer **3 perguntas** usando `AskUserQuestion` em uma única chamada:

```
questions: [
  {
    "question": "De qual(is) operador(es) você quer ver o funil?",
    "header": "Operador",
    "multiSelect": true,
    "options": [
      {"label": "Daniel", "description": "Daniel Oliveira"},
      {"label": "Camila", "description": "Camila Torres"},
      {"label": "Cibely", "description": "Cibely Cristina"},
      {"label": "Todos", "description": "Visão consolidada de todo o time"}
    ]
  },
  {
    "question": "Qual período de análise?",
    "header": "Período",
    "multiSelect": false,
    "options": [
      {"label": "Último mês", "description": "Mês atual ou último mês fechado"},
      {"label": "3 meses", "description": "Últimos 3 meses com visão MoM"},
      {"label": "6 meses", "description": "Últimos 6 meses com visão MoM"},
      {"label": "Período custom", "description": "Você define as datas"}
    ]
  },
  {
    "question": "Que nível de detalhe você quer?",
    "header": "Detalhe",
    "multiSelect": false,
    "options": [
      {"label": "Só scorecard", "description": "Tabela com métricas vs metas — rápido e direto"},
      {"label": "Análise completa", "description": "Scorecard + pontos de atenção ranqueados + recomendações de ação"}
    ]
  }
]
```

**Regras das perguntas:**
- Se o usuário marcar "Todos" junto com operadores individuais, tratar como "Todos"
- Se marcar operadores individuais, mostrar dados individuais + consolidado deles
- Se escolher "Período custom", perguntar datas de início e fim
- Se o usuário já tiver especificado algum parâmetro no comando (ex: `/funil-outbound camila 3 meses`), inferir as respostas e pular as perguntas já respondidas

---

## Passo 2 — Coleta de Dados

### 2.1 Autenticação Kommo

Buscar token na tabela `vm_app_keys` do Supabase:
```sql
SELECT value FROM vm_app_keys WHERE category = 'crm' AND key = 'KOMMO_ACCESS_TOKEN';
```
- Base URL: `https://clubpetro.kommo.com/api/v4/`
- Header: `Authorization: Bearer {token}`

### 2.2 Dados do Kommo — Cards Outbound

Buscar leads na pipeline 8166623 com filtros:
- `filter[pipe][]=8166623`
- `filter[created_at][from]={timestamp_inicio}` e `filter[created_at][to]={timestamp_fim}`
- `with=custom_fields_values`
- `limit=250` (paginar se necessário com `&page=N`)

Dos leads retornados, filtrar:
- **Departamento = Comercial**: campo 1275339 = "Comercial"
- **Origem = Outbound**: campo 1266644 enum 914570

Para filtrar por operador, usar o campo **Hunter** (1265304) comparando com o nome do operador selecionado.

### 2.3 Dados da Pluri — Ligações de Campanha

```
POST https://clubpetro.acessocloud.com/ws/index.php
Content-Type: application/x-www-form-urlencoded

vToken={token}&vApp=Telecom&vMetodo=Chamada&vAct=getRetCampanha&vDataInicio={DD/MM/YYYY HH:MM:SS}&vDataFim={DD/MM/YYYY HH:MM:SS}
```

Token da Pluri: buscar no `.env` ou na tabela `vm_app_keys` (category: 'pluri').

Filtrar por operador usando o campo `operador` da resposta.

---

## Passo 3 — Montagem do Funil

### Definição das Etapas

| # | Etapa | Meta/mês | Como calcular |
|---|-------|----------|---------------|
| 1 | **Ligações** | Sem meta | Contar ligações na Pluri (`getRetCampanha`) no período. Filtrar por operador se aplicável. Contar apenas `status = Atendida` como ligações efetivas, mas reportar total também |
| 2 | **Cards** | 200 | Contar leads Kommo com Origem = Outbound (campo 1266644, enum 914570) + Departamento = Comercial (campo 1275339) criados no período |
| 3 | **Qualificados** | 60 | Dos cards acima, filtrar os que têm campo **1286201 = "Sim"** |
| 4 | **Agendas** | 18 | Dos qualificados, filtrar os que têm campo **1281649** (Data de Apresentação) **preenchido** |
| 5 | **Shows** | 14 | Das agendas, filtrar os que: (a) atingiram status ≥ **Reunião Realizada** (65190627) ou posterior na pipe, OU (b) foram **perdidos pelo Closer** (campo 1277082 preenchido, o que significa que chegou até o closer) |
| 6 | **Vendas** | 4 | Dos shows, filtrar os que têm campo **1262596** (Data de Assinatura) **preenchido** |
| 7 | **MRR** | R$ 3.200 | Dos deals com venda, **somar o campo 1262668** (Valor da Mensalidade) |

### Referência de Status IDs (para lógica de Shows)

Estágios que significam "chegou no closer / seguiu na pipe":
- 65190627 — Reunião Realizada
- 69600491 — Proposta Enviada
- 103148407 — FUP (Follow-up)
- 65190631 — Forecast
- 65190647 — Contrato na Rua
- 142 — Venda Ganha

Perdido pelo Closer = status 143 (Venda Perdida) + campo 1277082 (motivo perda Closer) preenchido.

### Taxas de Conversão (calculadas automaticamente)

| Transição | Meta implícita | Benchmark SaaS SMB |
|-----------|---------------|-------------------|
| Cards → Qualificados | 30% | 25-35% |
| Qualificados → Agendas | 30% | 30-40% |
| Agendas → Shows | 78% | 65-80% |
| Shows → Vendas | 29% | 20-30% |

---

## Passo 4 — Output: Scorecard

**Sempre gerar este output, independente do nível de detalhe escolhido.**

### 4.1 Scorecard Relâmpago

Se o usuário selecionou operadores individuais, mostrar uma tabela por operador + uma consolidada. Se selecionou "Todos", mostrar apenas consolidada.

**Meta individual**: dividir a meta total pelo número de operadores ativos (3 por padrão).

```markdown
## Funil Outbound — [Período]
### [Nome do Operador | Time Completo]

| Etapa | Realizado | Meta | % Meta | Status |
|-------|-----------|------|--------|--------|
| Ligações | X | — | — | 📊 |
| Cards | X | 67 | X% | 🟢/🟡/🟠/🔴 |
| Qualificados | X | 20 | X% | 🟢/🟡/🟠/🔴 |
| Agendas | X | 6 | X% | 🟢/🟡/🟠/🔴 |
| Shows | X | 5 | X% | 🟢/🟡/🟠/🔴 |
| Vendas | X | 1-2 | X% | 🟢/🟡/🟠/🔴 |
| MRR | R$ X | R$ 1.067 | X% | 🟢/🟡/🟠/🔴 |

**Conversões:**
| Transição | Taxa | Benchmark |
|-----------|------|-----------|
| Cards → Qualificados | X% | 30% |
| Qualificados → Agendas | X% | 30% |
| Agendas → Shows | X% | 78% |
| Shows → Vendas | X% | 29% |
```

### 4.2 Semáforo de Status

| Indicador | Critério |
|-----------|----------|
| 🟢 SAUDÁVEL | ≥ 90% da meta |
| 🟡 ATENÇÃO | 75-89% da meta |
| 🟠 ALERTA | 50-74% da meta |
| 🔴 CRÍTICO | < 50% da meta |

### 4.3 Tendência MoM (se período > 1 mês)

Mostrar evolução mês a mês com seta de direção:

```markdown
### Tendência MoM

| Etapa | Mês 1 | Mês 2 | Mês 3 | Direção |
|-------|-------|-------|-------|---------|
| Cards | X | X | X | ↑/↓/→ |
| Qualificados | X | X | X | ↑/↓/→ |
| ... | | | | |
```

**Se o usuário escolheu "Só scorecard", PARAR AQUI.** Não gerar análise completa.

---

## Passo 5 — Output: Análise Completa

**Só gerar se o usuário escolheu "Análise completa".**

### 5.1 Bottom Line

2-3 frases no formato executivo:
> "O funil outbound está [saudável/em risco/crítico] no período X. [Principal destaque positivo]. [Principal ponto de atenção com dado numérico]."

### 5.2 Pontos de Atenção Ranqueados

Cada ponto de atenção recebe um **score de impacto** (0-100) baseado em 3 fatores:

| Fator | Peso | Cálculo |
|-------|------|---------|
| Gap vs meta | 40% | Quanto mais longe da meta, maior o score |
| Tendência MoM | 30% | Queda consistente pesa mais que estagnação |
| Posição no funil | 30% | Etapas mais ao fundo (Shows, Vendas, MRR) pesam mais porque afetam receita diretamente |

**Fórmula simplificada:**
- Gap score: `(1 - realizado/meta) × 40`, capped em 40
- Tendência score: queda >30% = 30, queda 15-30% = 20, queda <15% = 10, estável = 5, subindo = 0
- Posição score: Ligações=5, Cards=10, Qualificados=15, Agendas=20, Shows=25, Vendas=30, MRR=30

**Output:**

```markdown
### Pontos de Atenção (por prioridade)

#### 1. 🔴 [Nome do Problema] — Score: XX/100
**O que está acontecendo:** [dado concreto — ex: "Cards caíram de 180 para 95 nos últimos 2 meses"]
**Por que importa:** [consequência — ex: "Com 95 cards, mesmo com conversão perfeita, máximo de 2 vendas"]
**Ação sugerida:** [recomendação concreta — ex: "Revisar volume de listas na Pluri e/ou adicionar campanha de prospecção"]

#### 2. 🟠 [Nome do Problema] — Score: XX/100
...
```

### 5.3 O que Está Funcionando

1-2 destaques positivos com dados (ex: "Taxa de conversão Agendas → Shows em 85%, acima do benchmark de 78%").

### 5.4 Foco do Mês

Uma métrica prioritária + target numérico + dono:
> "**Foco:** Aumentar Cards de 95 para 150 este mês. **Dono:** Camila + Daniel. **Como:** Subir 2 novas campanhas na Pluri com lista de 500+ contatos."

### 5.5 Análise de Perdas (se houver dados)

Se houver leads perdidos no período, agrupar motivos de perda:

**Perdas pelo Hunter (campo 1288043):**
| Motivo | Qtd | % |
|--------|-----|---|
| ... | | |

**Perdas pelo Closer (campo 1277082):**
| Motivo | Qtd | % |
|--------|-----|---|
| ... | | |

Destacar os top 3 motivos e sugerir ações.

---

## Time Comercial Outbound

| Nome | Papel | Identificação Pluri | Identificação Kommo |
|------|-------|--------------------|--------------------|
| Daniel | Hunter/SDR | Daniel Oliveira (campo `operador`) | Campo Hunter (1265304) |
| Camila | Hunter/SDR | Camila Torres (campo `operador`) | Campo Hunter (1265304) |
| Cibely | Hunter/SDR | Cibely Cristina (campo `operador`) | Campo Hunter (1265304) |

**Para alterar o time:** editar esta tabela diretamente neste arquivo.

---

## Metas Mensais

| Etapa | Meta Total/mês | Meta Individual (÷3) |
|-------|---------------|---------------------|
| Ligações | Sem meta | — |
| Cards | 200 | ~67 |
| Qualificados | 60 | 20 |
| Agendas | 18 | 6 |
| Shows | 14 | ~5 |
| Vendas | 4 | ~1-2 |
| MRR | R$ 3.200 | ~R$ 1.067 |

**Para alterar as metas:** editar esta tabela diretamente neste arquivo.

---

## Campos Kommo — Referência Rápida

| Campo ID | Nome | Uso na Skill |
|----------|------|-------------|
| 1275339 | Departamento | Filtrar = "Comercial" |
| 1266644 | Origem | Filtrar = Outbound (enum 914570) |
| 1265304 | Hunter | Identificar operador |
| 1265318 | Closer | Identificar closer (para análise de perdas) |
| 1286201 | Qualificado | = "Sim" → lead qualificado |
| 1281649 | Data de Apresentação | Preenchido → agenda marcada |
| 1262596 | Data de Assinatura | Preenchido → venda fechada |
| 1262668 | Valor da Mensalidade | MRR do deal |
| 1288043 | Motivo perda Hunter | Análise de perdas |
| 1277082 | Motivo perda Closer | Análise de perdas + lógica de Shows |

---

## Regras

- Toda comunicação em **português brasileiro**
- Não inventar dados — se a API retornar erro ou dados insuficientes, avisar claramente
- Se o período solicitado incluir o mês atual (ainda não fechado), indicar que os dados são parciais e projetar o resultado pro mês completo (regra de três simples pelos dias úteis)
- Arredondar percentuais para 1 casa decimal
- Valores monetários em formato brasileiro: R$ 1.234,56
- Se identificar um ponto de atenção CRÍTICO na análise completa, sugerir criar tarefa no ClickUp (lista 901326908797) mas **não criar automaticamente** — perguntar antes
