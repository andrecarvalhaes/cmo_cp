# CMO ClubPetro - Memória do Projeto

## Contexto
- Usuário é **André Carvalhaes**, CMO/Diretor de Marketing do ClubPetro
- É hands-on: ajuda na mão de obra quando time está lento
- Projeto (`cmo_cp`) = hub estratégico para debater estratégia, visão de CMO e onboardar métricas-chave
- Foco: integrar ferramentas e construir base de dados para decisões estratégicas (DRE, pipeline, churn, CAC, LTV etc.)
- Comunicação sempre em português brasileiro
- Site construído no **Webflow** (credencial pendente)

## Integrações Disponíveis
- Supabase (MCP ativo)
- ClickUp (API REST, key no `.env`) — Space "Marketing & Comercial", 4 listas/folders mapeados
- Gmail (MCP ativo)
- Google Calendar (MCP ativo)
- Canva (MCP ativo)
- **Vendemais** — sistema integrador interno (React+TS+Vite, repo em `C:\Users\ClubPetro-123\Documents\vendemais`). Workflow: branch → commit → PR (desc PT-BR) → link de teste → aprovação → merge

## Integrações Detalhadas
Guias completos em `memory/integracoes/`:
- `kommo.md` — Kommo CRM: pipeline, campos, estágios, motivos de perda
- `dre-resultados.md` — DRE: receita, MRR, churn, despesas S&M, margens
- `contratos-faturamento.md` — store_contracts + store_financial_records (churn, tenure, onboarding)
- `ga4-search-console.md` — GA4 + Search Console + Meta Ads
- `instagram.md` — Instagram Graph API: @clubpetro (22K seg.), reach, engagement, posts
- `meta-ads.md` — Meta Ads API (spend, CPL, campanhas)
- `conversoes-supabase.md` — BD_Conversoes_RD (leads) + BD_RDOportunidades (MQLs)
- `rd-station.md` — RD Station Marketing API: emails, conversões, workflows, segmentações, campos custom
- `n8n.md` — N8N: consultar/criar automações sob demanda (instância compartilhada todos os times)
- `pluri.md` — Pluri discadora: campanhas (getRetCampanha) + manuais (getRetLigSainte)
- `vendemais.md` — Vendemais: sistema integrador interno, stack, estrutura, workflow de PRs
- `clickup.md` — ClickUp: space Marketing & Comercial, backlogs, sprints, kanban design, time
- `pendencias-metricas.md` — Métricas pendentes e status geral

## Regras Importantes
- GA4 = apenas tráfego (sessions). Domínios: `clubpetro.com` + `blog.clubpetro.com` apenas
- Conversões/Leads = `BD_Conversoes_RD` (Supabase)
- MQLs/Oportunidades = `BD_RDOportunidades` campos `ld_ko_*` (Supabase)
- Kommo = API direta, NUNCA tabelas Supabase (BD_Leads_Kommo etc.)
- RD Station = API OAuth2 (token 24h, refresh necessário). Email metrics + conversões limitados a 45 dias. Funnel analytics bloqueado (plano). cf_id_kommo liga RD↔Kommo
- N8N = API REST (JWT). Instância compartilhada todos os times. Apenas consultar/criar workflows sob demanda
- Pluri = POST form-urlencoded (vToken+vApp+vMetodo+vAct+datas). Credenciais no `.env` (`PLURI_TOKEN`, `PLURI_URL`). Contact rate ~1,4%. Tabulação positiva cria lead Outbound no Kommo via N8N
- **Outbound Kommo**: filtrar Origem = Outbound (enum 914570), excluindo Departamento = "Expansão". Incluir "Comercial" e sem departamento (99% dos outbound não tem dept preenchido)
- **LTV**: Calcular sobre Margem Bruta (GM 78,8%), NÃO receita pura. Fórmula: LTV = (ARPU × GM%) / churn. ARPU R$ 1.067, GM 78,8%, churn 1,64% → LTV = R$ 51.268. LT = 1/churn = 61 meses (projeção — base de faturas incompleta, pendente validação do churn real).
- **CAC**: S&M total (Comercial+Marketing+Feiras da DRE) / Won Comercial por Data de Assinatura. Deal = loja. Jan+Fev: R$ 5.725. Est. Q1: R$ 7.180. LTV:CAC = 9,0:1.
- **Ticket em queda**: Média Q1/24 R$ 986 → Q1/26 R$ 671 (-32%). Monitorar.
- **Ativação** = loja sai do onboarding (sistema instalado + time de pista treinado). Gap mediana: 128 dias.
- **Motivos de churn**: NÃO existe registro estruturado. Ponto cego assumido.
- **NPS**: NÃO existe pesquisa de satisfação. Ponto cego assumido.
- **New MRR Comercial**: Fonte = Kommo Won, Dept=Comercial, data = campo 1262596 (Data de Assinatura, NÃO closed_at), MRR = campo 1262668. Meta: R$ 20K/mês.
- **MQLs**: Contar emails únicos em BD_RDOportunidades com id_kommo IS NOT NULL, relacao_posto = Dono/Gerente/Não se aplica, cliente_cp != Sim. Usar conversion_date.
- **DRE New MRR ≠ Kommo New MRR**: DRE mede faturamento (regime competência), Kommo mede venda (data assinatura). Usar Kommo como fonte de verdade para meta comercial.
- **WhatsApp** = mecanismo de conversão, NÃO canal orgânico. ~45% dos leads WhatsApp vêm de tráfego pago (UTM).
- **Google Ads**: investiram 1 mês, pararam por falta de resultado. 164 leads "adwords" em 2026 são resquício.
- **Gross Margin**: 78,8% (Jan-Fev/26). COGS = CS + Onboarding + Suporte + Loja. Usado no LTV.
- **Base de faturas** (store_financial_records): dados reais só Jan/25+. Ago-Dez/24 são outliers (1-16 NFs). Não serve para calcular LT observado.
- **New MRR realizado (Kommo)**: Jan R$ 14.866 (22), Fev R$ 20.159 (29), Mar R$ 7.750 (10). Só Fev bateu R$ 20K.
- **Instagram**: @clubpetro, IG Business ID `17841407201741175`, FB Page ID `139899636387139`. 22K seguidores, ~15-18K reach/dia. Token = META_ACCESS_TOKEN (vm_app_keys, analytics). API v21.0.

## Skills Configuradas
- `/trabalhar` - busca tarefas do ClickUp para trabalhar
- `/cmo-advisor` - consultoria de marketing/liderança
- `/auditoria-seo` - auditoria SEO de documentação
- `/ui-ux-pro-max` - design UI/UX
- `/Claudio` - gerenciamento de componentes Claude Code
- `/new-skill` - fábrica de skills personalizadas (pesquisa repos de referência + personaliza pro ClubPetro)
- `/funil-outbound` - report do funil outbound: Pluri (ligações) + Kommo (cards→vendas), scorecard vs metas, pontos de atenção ranqueados. Pergunta operador, período e nível de detalhe
- `/review-organico` - review periódico de alcance orgânico (Blog/SEO + Instagram + Email). Compara 12 períodos (semanal/quinzenal/mensal). GA4 + SC + IG Graph API + RD Station + Supabase
- `/review-cro` - análise CRO periódica: tráfego (GA4) × conversões (Supabase). Separa BoFu (18 páginas produto) vs ToFu. Análise individual por página BoFu. Scorecard 6 dimensões. Ações ICE. Deep: Lead→MQL, benchmarks B2B, A/B tests
- `/finalizar-task` - finaliza pendência: posta comentário "IA:" com resumo do trabalho + move para "checando resultados"
- `/testar-task` - valida trabalho feito: desenha testes, executa, reporta resultados, limpa dados de teste
- `/pendencia` - intake inteligente: entende demanda, faz análise SCQA, cria tarefa no ClickUp, mapeia soluções ranqueadas por ICE como comentários "IA:"
- `/atualizar-kommo` - sync completo aux_kommo: exporta TODOS os leads do Kommo (API 3 req/s) + contatos, TRUNCATE + INSERT no Supabase via PostgREST, recria indexes
