# Instagram Graph API — Integração ClubPetro

## Credenciais
- **Instagram Business Account ID**: `17841407201741175`
- **Facebook Page ID (ClubPetro)**: `139899636387139`
- **Username**: `@clubpetro`
- **META_ACCESS_TOKEN**: tabela `vm_app_keys` (category: 'analytics')
- **API Version**: v21.0
- **Base URL**: `https://graph.facebook.com/v21.0/`

Também disponível: Precin.ai (Page `292093883997306`, IG `17841466408527293`)

## Dados da Conta (ref. Abr/2026)
| Dado | Valor |
|------|-------|
| Seguidores | 22.044 |
| Posts publicados | 1.495 |
| Reach diário | ~15-18K |
| Novos seguidores/dia | ~14-21 |

## Endpoints Disponíveis

### 1. Account Info
```bash
GET /17841407201741175?fields=id,username,name,followers_count,media_count,profile_picture_url
```

### 2. Account Insights (diário)
```bash
GET /17841407201741175/insights?metric=reach,follower_count&period=day&since={timestamp}&until={timestamp}
```

**Métricas disponíveis (period=day):**
- `reach` — alcance diário (contas únicas)
- `follower_count` — novos seguidores net (ganhos - perdidos)

**Métricas disponíveis (metric_type=total_value + period=day):**
- `accounts_engaged` — contas que engajaram
- `total_interactions` — total de interações
- `website_clicks` — cliques no link do perfil
- `profile_views` — visitas ao perfil
- `follows_and_unfollows` — follows e unfollows

### 3. Media List (posts)
```bash
GET /17841407201741175/media?fields=id,caption,timestamp,like_count,comments_count,media_type,permalink&limit=100
```

**media_type**: `IMAGE`, `VIDEO` (Reels), `CAROUSEL_ALBUM`

Paginar com `after` cursor se necessário.

### 4. Media Insights (por post)
```bash
GET /{media_id}/insights?metric=reach,likes,comments,shares,saved,total_interactions
```

**Métricas por post:**
| Métrica | Descrição |
|---------|-----------|
| reach | Contas únicas alcançadas |
| likes | Curtidas |
| comments | Comentários |
| shares | Compartilhamentos |
| saved | Salvamentos |
| total_interactions | Total de engajamento (likes + comments + shares + saves - removes) |

### 5. Account Insights (total_value para período)
```bash
GET /17841407201741175/insights?metric=accounts_engaged,reach,total_interactions,website_clicks,profile_views&metric_type=total_value&period=day&since={timestamp}&until={timestamp}
```

## Cálculos

### Engagement Rate
```
ER = (Total Interactions do período) / (Reach do período) × 100
```
Ou por post:
```
ER por post = (likes + comments + shares + saves) / reach × 100
```

### Benchmarks B2B Instagram (referência)
| Métrica | Bom | Excelente |
|---------|-----|-----------|
| ER por post | > 1,5% | > 3% |
| ER geral conta | > 1% | > 2% |
| Reach/Followers | > 30% | > 50% |

## Limitações
- **Rate limit**: 200 calls/user/hour (geralmente suficiente)
- **Insights históricos**: account insights disponíveis até 30 dias atrás (para `period=day`)
- **Token expiration**: META_ACCESS_TOKEN pode expirar. Se retornar erro 190, renovar no Meta Business Suite e atualizar `vm_app_keys`
- **Sem dados de Stories**: API não retorna insights de Stories expirados

## Notas de Ambiente
- Usar `curl` (melhor que urllib neste ambiente Windows)
- Timestamps em Unix epoch para `since`/`until`
- Datas retornadas em UTC (end_time com offset +0000)
