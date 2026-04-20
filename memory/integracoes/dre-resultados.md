# DRE / Resultados — Guia de Interpretação para CMO Advisor

## Fonte
- Arquivo: `resultados.xlsx` (arquivo local, vem do Google Sheets privado)
- Google Sheets ID: `1qAQ6Jlw3675ewWls8NBjgUYFTKOoZ8J6j0UIdbMOsjI` (privado, sem MCP — precisa exportar xlsx)
- Aba principal: `RESULTADOS POR TIME - em elaboração` (681 linhas x 139 colunas)
- **IMPORTANTE: Dados são lançados pela contabilidade. Meses sem lançamento aparecem zerados.**

## Como os dados são gerados
- Os valores vêm da aba `04 WEBPOSTO - Razão` (livro razão contábil, ~19.500 lançamentos)
- Fórmulas SUMIFS cruzam: Conta Reduzida CP (col X) × Centro de Custo CP (col W) × Mês (col O)
- Ajustes manuais vêm da aba `02 Ajustes`
- Receita detalhada por serviço na aba `FAT POR SERVIÇO`
- **Churn e New MRR (R20-R21) são valores manuais** — não vêm de fórmula, são inputados diretamente
- Quant CNPJ (R22) também é input manual

## Estrutura da DRE

### Layout
- **Coluna A (C1)**: Centro de custo / Departamento
- **Coluna B (C2)**: Descrição da conta
- **Colunas D-O (C4-C15)**: Realizado mensal Jan-Dez 2026
- **Coluna P (C16)**: Total acumulado
- **Colunas S+ (C19+)**: Acumulado de períodos anteriores (2024+)

### Estrutura Hierárquica

```
RECEITA BRUTA (R7)
├── Receita de Prestação de Serviços (R8)
│   ├── On-Demand (R9): envio de campanhas, cadastro fácil
│   ├── Add-On (R13): taxa implantação APP + taxa implantação
│   └── MRR (R17): Licença de Uso Mensal (receita recorrente)
│       ├── Churn (R20)
│       └── New MRR (R21)
├── Outras Receitas Operacionais (R25): Precin, ClubVarejo, PistaPró, Design
└── DEDUÇÕES (R35): COFINS, PIS, ISS
= RECEITA LÍQUIDA (R6)

DESPESAS OPERACIONAIS (R49)
├── COGS (R51)
│   ├── Customer Success (R53)
│   ├── Onboarding (R82)
│   ├── Suporte (R110)
│   └── Loja (R138)
├── P&D (R167)
│   ├── Servidores + Ferramentas (R170)
│   ├── B2C Novos (R198)
│   ├── B2B Fidelização (R226*)
│   ├── B2B Setup (R254*)
│   ├── Camera (R282*)
│   ├── B2B Novos (R310*)
│   ├── Precin (R338*)
│   └── ClubVarejo (R366*)
├── S&M (R394) ← DESPESAS DIRETAS DO CMO
│   ├── COMERCIAL (R396)
│   ├── MARKETING (R425)
│   └── FEIRAS E EVENTOS (R453)
└── G&A (R482)
    ├── Diretoria, Agilidade, Financeiro, Gente e Cultura, Infra, Jurídico

= RESULTADO OPERACIONAL (R655)
- Despesas Não Operacionais (R658)
```

---

## S&M — Despesas Diretas do CMO (Linha 394)

### Total S&M
| Mês | Valor |
|-----|-------|
| Jan/26 | R$ 159.470 |
| Fev/26 | R$ 132.508 |
| Total Q1 (parcial) | R$ 291.978 |

### COMERCIAL (R396) — Despesa total: R$ 135.532
| Subcategoria | Jan | Fev | Total |
|-------------|-----|-----|-------|
| Pessoal (CLT + PJ) | 61.112 | 58.858 | 119.971 |
| - Remuneração CLT | 5.808 | 8.430 | 14.238 |
| - PJ (Serviços) | 48.153 | 43.087 | 91.240 |
| - Benefícios | 2.627 | 3.294 | 5.922 |
| - Encargos | 4.472 | 3.987 | 8.459 |
| Informática/Sistemas | 2.937 | 2.954 | 5.891 |
| Comissionamentos/Brindes | 176 | 1.589 | 1.765 |
| Marketing (dentro de comercial) | 4.642 | 0 | 4.642 |
| Administrativas | 330 | 2.166 | 2.496 |
| Viagens | 0 | 1.698 | 1.698 |

### MARKETING (R425) — Despesa total: R$ 138.687
| Subcategoria | Jan | Fev | Total |
|-------------|-----|-----|-------|
| Pessoal (CLT + PJ) | 41.690 | 42.482 | 84.172 |
| - Remuneração CLT | 12.123 | 13.845 | 25.968 |
| - PJ (Serviços) | 18.750 | 18.750 | 37.500 |
| - Benefícios | 1.622 | 2.372 | 3.994 |
| - Encargos | 9.113 | 7.395 | 16.508 |
| Informática/Sistemas | 32.675 | 638 | 33.313 |
| Marketing (mídia/ads/produção) | 13.524 | 7.679 | 21.203 |

### FEIRAS E EVENTOS (R453) — Despesa total: R$ 17.758
| Subcategoria | Jan | Fev | Total |
|-------------|-----|-----|-------|
| Pessoal | 0 | 590 | 590 |
| Informática/Sistemas | 0 | 3.353 | 3.353 |
| Feiras e Eventos (direto) | 2.368 | 10.011 | 12.379 |
| Administrativas | 0 | 1.437 | 1.437 |

---

## Receita — Visão para o CMO

### MRR (Receita Recorrente)
| Indicador | Jan/26 | Fev/26 | Mar/26 |
|-----------|--------|--------|--------|
| MRR Total | R$ 1.065.756 | R$ 1.046.120 | R$ 1.073.473 |
| Licença Mensal | R$ 1.029.398 | R$ 1.022.260 | R$ 1.035.597 |
| New MRR | R$ 30.754 | R$ 10.650 | R$ 27.231 |
| Churn | R$ 5.604 | R$ 13.210 | R$ 10.645 |
| Net New MRR | R$ 25.150 | R$ -2.560 | R$ 16.586 |
| CNPJs ativos | 1.105 | 1.086 | 1.125 |
| Ticket Médio (MRR/CNPJ) | R$ 964 | R$ 963 | R$ 954 |

### Receita Bruta
| Jan/26 | Fev/26 | Mar/26 | Total |
|--------|--------|--------|-------|
| R$ 1.251.728 | R$ 1.211.725 | R$ 1.345.307 | R$ 3.808.759 |

### Margem / Resultado
| Indicador | Jan/26 | Fev/26 |
|-----------|--------|--------|
| Receita Líquida | R$ 1.168.226 | R$ 1.131.147 |
| COGS | R$ -227.030 | R$ -260.067 |
| **Gross Profit** | **R$ 941.196** | **R$ 871.080** |
| **Gross Margin** | **80,6%** | **77,0%** |
| Despesas Operacionais | R$ -989.465 | R$ -906.014 |
| Resultado Operacional | R$ 178.761 | R$ 225.133 |
| Margem Operacional | ~15,3% | ~19,9% |

### COGS Detalhado
| Centro de Custo | Jan/26 | Fev/26 |
|----------------|--------|--------|
| Customer Success | R$ -124.882 | R$ -159.914 |
| Onboarding | R$ -41.592 | R$ -41.560 |
| Suporte | R$ -55.818 | R$ -58.236 |
| Loja | R$ -4.737 | R$ -357 |
| **COGS Total** | **R$ -227.030** | **R$ -260.067** |

**Gross Margin média Jan-Fev: 78,8%** — usado no cálculo de LTV (ver contratos-faturamento.md)

---

## Métricas CMO Deriváveis

### S&M como % da Receita Líquida
- Jan: 159.470 / 1.168.226 = **13,6%**
- Fev: 132.508 / 1.131.147 = **11,7%**

### Custo de Aquisição (aproximado)
- S&M mensal médio (Jan-Fev): ~R$ 146.000
- New MRR médio (Jan-Fev): ~R$ 20.700
- Para calcular CAC real: precisa cruzar com nº de novos clientes do Kommo no período

### Marketing como % de S&M
- Jan: 87.889 / 159.470 = **55,1%**
- Fev: 50.799 / 132.508 = **38,3%**

### Composição do gasto de marketing
- **Pessoal**: ~60% (time fixo)
- **Mídia/Ads/Produção**: ~15% (campo MARKETING dentro da seção)
- **Ferramentas**: ~24% (Informática/Sistemas — inclui CRM, automação, etc.)

---

## Abas da Planilha

| Aba | Conteúdo | Uso para CMO |
|-----|----------|--------------|
| RESULTADOS POR TIME - em elabor | DRE segmentada por centro de custo | **Principal** — S&M, margens, resultado |
| 01 RESULTADOS | DRE consolidada (sem segmentação por time) | Visão geral |
| FAT POR SERVIÇO | Receita detalhada por produto/serviço | Mix de receita, ticket por produto |
| 04 WEBPOSTO - Razão | Livro razão contábil (lançamentos) | Fonte dos dados — não consultar direto |
| 02 Ajustes | Reclassificações contábeis manuais | Fonte de ajustes |
| 09 WEBPOSTO - Balancete | Balancete contábil | Referência contábil |

## Produtos de Receita (via FAT POR SERVIÇO)
- Licença de Uso Mensal - Posto (maior receita: ~R$ 848K/mês)
- Licença de Uso Mensal - Plano Campeão (~R$ 60K/mês)
- Gestão de Metas (~R$ 42K/mês)
- Envio de Campanhas (~R$ 65K/mês)
- Cadastro Fácil (~R$ 44K/mês)
- White Label / App Personalizado
- Precin, ClubVarejo, PistaPró Comunidade
- Taxa de Implantação, Taxa App Personalizado

## Foco CMO
- **Produto principal: Licença de Uso Mensal - Posto** (~80% da receita, ~R$ 848K/mês)
- Este é o produto que gera a mensalidade registrada no Kommo (campo 1262668)
- Outros produtos (Precin, ClubVarejo, PistaPró) estão em ramp-up — não monitorar por enquanto
- **Meta comercial: R$ 20K de New MRR/mês**
- Pipeline coverage = MRR em pipeline ativo / R$ 20K (alvo: 3-4x = R$ 60-80K em pipe)

## Ferramentas de Marketing (Informática/Sistemas)
Lançamentos identificados no razão contábil:
| Ferramenta | Valor mensal | Obs |
|-----------|-------------|-----|
| RD Station | ~R$ 31K (Jan) | **Pagamento anual** — normalizado = ~R$ 2.570/mês |
| RD Station | R$ 1.082 (Jan) | Segundo lançamento menor |
| Canva | R$ 58/mês | Mensal recorrente |
| ClickSign | R$ 427/mês | Assinatura de documentos |
| StreamYard | R$ 199 (Jan) | Streaming |
| Webflow | R$ 153 (Fev) | Site |
| Tally BV | R$ 81 (Jan) | Formulários |

## Observações
- Dados são contábeis (regime de competência) — vêm do sistema WebPosto (ERP)
- **Churn e New MRR (R20-R21) são inputs manuais** — calculados por alguém e digitados
- A sublinha "MARKETING" (R442) = gasto direto com mídia/ads/produção (categoria contábil no razão)
- Pico de Informática/Sistemas em Jan = RD Station (R$ 30.828) — pagamento não recorrente mensal
- Para cálculo de custo mensal normalizado de ferramentas, diluir RD Station pelo período coberto
