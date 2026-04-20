---
name: atualizar-kommo
description: "Exporta todos os leads do Kommo, limpa e recarrega a tabela aux_kommo no Supabase. Use quando o usuário invocar /atualizar-kommo."
---

# Atualizar Kommo — Sync Completo da Base aux_kommo

Exporta TODOS os leads do Kommo (todas as pipelines), apaga a base `aux_kommo` no Supabase e sobe ela atualizada. Inclui contatos (telefones, emails) e todos os custom fields.

**Script:** `skills/atualizar-kommo/sync_kommo.py`

---

## Passo 1 — Credenciais

### 1.1 Token Kommo

Buscar no Supabase via MCP:
```sql
SELECT value FROM vm_app_keys WHERE category = 'crm' AND key = 'KOMMO_ACCESS_TOKEN';
```
Guardar como `KOMMO_TOKEN`.

### 1.2 Supabase URL e Key

Usar as ferramentas MCP do Supabase:
1. `get_project_url` → guardar como `SUPABASE_URL`
2. Buscar service role key:
```sql
SELECT value FROM vm_app_keys WHERE category = 'supabase' AND key = 'SERVICE_ROLE_KEY';
```
Se não existir, usar `get_publishable_keys` (anon key) — funciona se aux_kommo não tem RLS.

---

## Passo 2 — Preparar Colunas Válidas

### 2.1 Dropar colunas quebradas (primeira execução)

Verificar se as colunas quebradas ainda existem:
```sql
SELECT column_name FROM information_schema.columns
WHERE table_name = 'aux_kommo'
AND (column_name LIKE '%"_%' OR column_name LIKE '▼%' OR column_name LIKE '⬇%')
ORDER BY ordinal_position;
```

Se existirem, dropar cada uma via `execute_sql`:
```sql
ALTER TABLE aux_kommo
  DROP COLUMN IF EXISTS "Quais outros participantes?""_1,""Data da apresentacao",
  DROP COLUMN IF EXISTS "Interesse em outro produto?""_1,""Valor Mensalidade",
  DROP COLUMN IF EXISTS "Data de validade da proposta""_1,""Custo do cadastro",
  DROP COLUMN IF EXISTS "Produto Vendido""_1,""Temperatura (Hunter)""_1,""Tempeatura (Closer",
  DROP COLUMN IF EXISTS "Data de inicio do projeto""_1,""Data de inicio do pagamento",
  DROP COLUMN IF EXISTS "Procuracao assinada""_1,""Link aditivo",
  DROP COLUMN IF EXISTS "Qual ERP?""_1,""Data da retomada",
  DROP COLUMN IF EXISTS "▼ PROPOSTA▼",
  DROP COLUMN IF EXISTS "▼ SUBIR CONTRATO ▼",
  DROP COLUMN IF EXISTS "▼ POS ASSINATURA ▼",
  DROP COLUMN IF EXISTS "▼ Manual ou pelo CNPJ ▼",
  DROP COLUMN IF EXISTS "⬇️ Manual ou pelo CNPJ";
```

**Nota:** Os nomes podem ter aspas internas que dificultam o SQL. Se o ALTER falhar, dropar uma coluna por vez usando o `ordinal_position` ou testar com `SELECT` antes. Alternativa: recriar a tabela sem essas colunas.

### 2.2 Exportar lista de colunas válidas

Após o cleanup, buscar as colunas restantes:
```sql
SELECT json_agg(column_name ORDER BY ordinal_position)
FROM information_schema.columns
WHERE table_name = 'aux_kommo';
```

Salvar o resultado como `valid_columns.json` no diretório do projeto.

---

## Passo 3 — Extrair do Kommo

Rodar o script de extração:

```bash
python skills/atualizar-kommo/sync_kommo.py extract \
  --token="$KOMMO_TOKEN" \
  --columns="valid_columns.json" \
  --output="kommo_export.json"
```

**O que o script faz:**
1. Busca dados de referência (usuários, pipelines, estágios)
2. Pagina TODOS os leads (250/página, 3 req/s) com contacts + loss_reason + companies
3. Pagina TODOS os contatos (para telefones, emails, custom fields)
4. Achata cada lead em um dict com colunas da aux_kommo
5. Salva em `kommo_export.json`

**Tempo estimado:** ~2-3 min para 13.5K leads + contatos.

**Verificação:** Checar que o JSON foi gerado e tem um número razoável de leads (≥ 10.000):
```bash
python -c "import json; d=json.load(open('kommo_export.json')); print(f'{len(d)} leads')"
```

Se o número de leads for muito menor que o esperado, investigar antes de continuar.

---

## Passo 4 — Limpar e Recarregar

### 4.1 TRUNCATE (via MCP)

**SOMENTE após confirmar que a extração foi bem-sucedida:**

```sql
TRUNCATE TABLE aux_kommo;
```

### 4.2 Inserir via PostgREST

```bash
python skills/atualizar-kommo/sync_kommo.py load \
  --input="kommo_export.json" \
  --supabase-url="$SUPABASE_URL" \
  --supabase-key="$SUPABASE_KEY"
```

**O que o script faz:**
1. Lê o JSON exportado
2. Insere em batches de 200 linhas via PostgREST API
3. Reporta progresso e erros

**Se o load via PostgREST falhar** (ex: RLS bloqueando), alternativa via MCP:
- Ler o JSON com Python, gerar INSERT SQL em batches de 50 linhas
- Executar cada batch via `execute_sql`

---

## Passo 5 — Recriar Indexes

Após o load, recriar os indexes parciais via MCP `execute_sql`:

```sql
-- Indexes parciais (performance de queries)
CREATE INDEX IF NOT EXISTS idx_kommo_criado_em
  ON aux_kommo ("Criado em")
  WHERE "Criado em" IS NOT NULL AND "Criado em" <> '';

CREATE INDEX IF NOT EXISTS idx_kommo_data_assinatura
  ON aux_kommo ("Data de Assinatura")
  WHERE "Data de Assinatura" IS NOT NULL AND "Data de Assinatura" <> '';

CREATE INDEX IF NOT EXISTS idx_kommo_data_apresentacao
  ON aux_kommo ("Data da Apresentacao:")
  WHERE "Data da Apresentacao:" IS NOT NULL AND "Data da Apresentacao:" <> '';

CREATE INDEX IF NOT EXISTS idx_kommo_email_comercial
  ON aux_kommo ("Email comercial")
  WHERE "Email comercial" IS NOT NULL AND "Email comercial" <> '';

CREATE INDEX IF NOT EXISTS idx_kommo_email_pessoal
  ON aux_kommo ("Email pessoal")
  WHERE "Email pessoal" IS NOT NULL AND "Email pessoal" <> '';

CREATE INDEX IF NOT EXISTS idx_kommo_outro_email
  ON aux_kommo ("Outro email")
  WHERE "Outro email" IS NOT NULL AND "Outro email" <> '';

CREATE INDEX IF NOT EXISTS idx_kommo_etapa_do_lead
  ON aux_kommo ("Etapa do lead")
  WHERE "Etapa do lead" = 'Venda ganha';

CREATE INDEX IF NOT EXISTS idx_kommo_email_comercial_etapa
  ON aux_kommo ("Email comercial", "Etapa do lead")
  WHERE "Email comercial" IS NOT NULL AND "Email comercial" <> ''
    AND "Etapa do lead" = 'Venda ganha';

CREATE INDEX IF NOT EXISTS idx_kommo_rd_station_id
  ON aux_kommo ("RD Station_ID")
  WHERE "RD Station_ID" IS NOT NULL AND "RD Station_ID" <> '';

CREATE INDEX IF NOT EXISTS idx_kommo_valor_mensalidade
  ON aux_kommo ("Valor da Mensalidade")
  WHERE "Valor da Mensalidade" IS NOT NULL AND "Valor da Mensalidade" <> '';
```

---

## Passo 6 — Validar

### 6.1 Contagem

```sql
SELECT count(*) AS total FROM aux_kommo;
```

Comparar com o total do JSON exportado. Devem ser iguais.

### 6.2 Amostra

```sql
SELECT "ID", "Lead titulo", "Etapa do lead", "Funil de vendas",
       "Email comercial", "Origem", "Criado em"
FROM aux_kommo
ORDER BY "ID"::int DESC
LIMIT 5;
```

Verificar se os dados fazem sentido (nomes, datas, emails preenchidos).

### 6.3 Distribuição por funil

```sql
SELECT "Funil de vendas", count(*) AS total
FROM aux_kommo
GROUP BY "Funil de vendas"
ORDER BY total DESC;
```

### 6.4 Reportar ao usuário

Apresentar:
- Total de leads exportados
- Total de leads inseridos
- Distribuição por funil/pipeline
- Tempo total da operação
- Qualquer erro encontrado

---

## Passo 7 — Limpeza

Remover arquivos temporários:
```bash
rm -f valid_columns.json kommo_export.json
```

---

## Mapeamento de Campos — Referência

### Core (lead → coluna)

| Campo API | Coluna aux_kommo |
|-----------|-----------------|
| `id` | `ID` |
| `name` | `Lead titulo` |
| `price` | `Lead venda R$` |
| `responsible_user_id` → nome | `Usuario responsavel` |
| `created_at` → DD.MM.YYYY | `Criado em` |
| `created_by` → nome | `Criado por` |
| `updated_at` → DD.MM.YYYY | `modificada em` |
| `updated_by` → nome | `Modificado por` |
| `closed_at` → DD.MM.YYYY ou "nao fechado" | `Fechado as` |
| `status_id` → nome | `Etapa do lead` |
| `pipeline_id` → nome | `Funil de vendas` |
| `_embedded.tags` → join nomes | `Tags` |
| `_embedded.loss_reason` → nome | `Motivo de perda` |
| `_embedded.companies` → nome | `Contato da empresa` / `Empresa lead 's` |

### Custom Fields (lead)

Mapeados automaticamente por `field_name` → coluna de mesmo nome.

### Contato (primeiro contato do lead)

| Dado | Coluna |
|------|--------|
| `contact.name` | `Nome completo` / `Pessoa de contato` |
| Phone WORK | `Telefone comercial` |
| Phone WORKDD | `Tel. direto com.` |
| Phone MOB | `Celular` |
| Phone FAX | `Faz` |
| Phone HOME | `Telefone residencial` |
| Phone OTHER | `Outro telefone` |
| Email WORK | `Email comercial` |
| Email PRIV | `Email pessoal` |
| Email OTHER | `Outro email` |
| POSITION | `Cargo` |
| Demais custom fields | Por `field_name` |

---

## Regras

- Rate limit: **3 req/s** (margem de segurança, API permite 7)
- Toda comunicação em **português brasileiro**
- NUNCA truncar antes de confirmar que a extração foi bem-sucedida
- Se o PostgREST falhar, usar SQL direto via MCP como fallback
- Notas do lead (Nota, Nota 2, etc.) ficam NULL — são entidades separadas na API
- Colunas duplicadas do funil Varejo (sufixo `_1`) são preenchidas pelo field_name do Kommo
- Arquivos temporários devem ser limpos ao final
