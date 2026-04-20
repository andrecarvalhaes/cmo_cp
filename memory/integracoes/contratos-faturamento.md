# Contratos e Faturamento — store_contracts + store_financial_records

## Fonte
- Arquivos CSV exportados do Supabase projeto `ycvspvdzumfpzvruziku` (não acessível via MCP atual)
- `store_contracts_rows.csv` — 6.739 contratos (1.476 lojas, 676 redes)
- `store_financial_records_rows.csv` — 19.831 notas fiscais. **ATENÇÃO:** dados reais só a partir de Jan/25 (Ago/24=1 NF, Set/24=1, Dez/24=16 — outliers). Janela útil: Jan/25 a Mar/26 = 15 meses.

## store_contracts — Campos Importantes
| Campo | Tipo | Uso |
|-------|------|-----|
| store_id | UUID | Identificador da loja |
| network_id | UUID | Rede/grupo |
| name | text | Produto (Licença, Cadastro Fácil, etc.) |
| status | text | active / canceled / suspended |
| value | numeric | Valor mensal do contrato |
| start_date | timestamp | Início do contrato |
| end_date | timestamp | Fim do contrato |
| signed_at | timestamp | Data de assinatura |
| cod_contrato | text | Código Omie |

## store_financial_records — Campos Importantes
| Campo | Tipo | Uso |
|-------|------|-----|
| store_id | UUID | Identificador da loja |
| description | text | Produtos faturados |
| amount | numeric | Valor da nota |
| status | text | RECEBIDO / ATRASADO / CANCELADO / A VENCER |
| due_date | date | Vencimento |
| paid_at | date | Data do pagamento efetivo |
| issue_date | date | Data de emissão (data_emissao na URL) |
| invoice_number | text | Número da NF |
| cod_nota_fiscal | text | Código Omie |

## Métricas Calculadas

### Churn
- Churn rate médio 12m: **1,64%/mês = 19,7%/ano**
- Tendência: subindo de 0,7% (Abr/25) para 1,8-2,9% (Q4/25-Q1/26)
- Logo churn acumulado: 354 lojas / 1.450 total = 24,4%
- Pico: Dez/25 = 2,9% (31 lojas)

### Tenure
- Ativas: mediana 20 meses (593 dias)
- Churned: mediana 13 meses (395 dias)

### LTV e CAC (CORRIGIDO v3 — Abril 2026)

**Metodologia LTV (padrão SaaS):**
- LTV = (ARPU × Gross Margin%) / Churn Rate Mensal
- LTV se calcula sobre **Margem Bruta**, não receita pura nem EBITDA
- Receita superestima (ignora COGS). EBITDA subestima (inclui despesas que não variam por cliente)
- LT (Lifetime) = 1 / Churn Rate Mensal

**Gross Margin:**
- Jan/26: RL R$ 1.168K - COGS R$ 227K = GM 80,6%
- Fev/26: RL R$ 1.131K - COGS R$ 260K = GM 77,0%
- **Média Jan-Fev: 78,8%**
- COGS = Customer Success + Onboarding + Suporte + Loja

**CAC:**
- S&M DRE disponível: Jan + Fev = R$ 291.978 (Mar ainda não lançado)
- Método: S&M total (Comercial+Marketing+Feiras) / Won Comercial (por Data de Assinatura, campo 1262596)
- 2 meses (Jan+Fev): R$ 291.978 / 51 lojas = **R$ 5.725**
- Est. Q1 (~R$ 438K): R$ 438K / 61 lojas = **R$ 7.180**
- Deal = loja (confirmado)

**LTV:**
- ARPU (ticket médio/loja): R$ 1.067/mês
- ARPU ajustado (× GM 78,8%): R$ 841/mês
- Churn rate mensal: 1,64%
- LT = 1 / 0,0164 = **61 meses**
- **LTV = R$ 841 / 0,0164 = R$ 51.268**

**LTV:CAC:**
- R$ 51.268 / R$ 5.725 = **9,0:1** 🟢
- Mesmo com churn a 3%: R$ 27.753 / R$ 5.725 = 4,8:1 🟢

**Payback:**
- Sem onboarding: R$ 5.725 / R$ 1.067 = **5,4 meses**
- Com onboarding (mediana 128 dias): 5,4 + 4,3 = **9,7 meses**

**Ticket em queda (contratos ativos por trimestre de início):**
- Q1/24: R$ 986 média | Q1/25: R$ 763 | Q1/26: R$ 671
- Queda de ~32% em 2 anos

**PENDÊNCIA: validar churn real** — base de faturas incompleta (dados reais só a partir de Jan/25, máx 15 meses). LT de 61 meses é projeção teórica pelo churn médio de 1,64%. Churn subindo (0,7%→2,9%) pode reduzir LT significativamente. Precisa acompanhar churn real para validar.

### Onboarding Gap
- Mediana: **128 dias** entre assinatura e primeiro faturamento
- 64% das lojas demoram >60 dias
- Payback real: 5,2 meses (CAC) + 4,3 meses (onboarding) = **9,5 meses**

### Base de Clientes
- 1.096 lojas com contrato ativo
- MRR total contratos: R$ 1.169.289
- Produto principal: Licença de Uso Mensal - Posto (R$ 801K, 69%)

### Faturamento
- ~R$ 1.13M/mês faturado (Jan-Mar/26)
- 97% status RECEBIDO
- 2% ATRASADO
