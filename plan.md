# Plano: Import CSV no DestinatariosModal

## Objetivo
Adicionar opção de upload CSV no modal de destinatários existente, com download de modelo CSV.

## Alterações

### 1. `DestinatariosModal.tsx` — Lógica e UI
- Adicionar toggle entre 2 modos: **Colar texto** (atual) e **Importar CSV**
- Usar `tab-menu` / `tab-item` do design system existente
- **Modo CSV:**
  - Botão "Baixar modelo CSV" que gera e faz download de um arquivo `modelo_destinatarios.csv` com header `telefone;nome` e 2 linhas de exemplo
  - Área de upload (input file accept=".csv") com drag-and-drop visual
  - Parser CSV: lê o arquivo com FileReader, detecta separador (`;` ou `,`), mapeia colunas `telefone` e `nome`
  - Reutiliza o mesmo `parseContacts` já existente após ler o CSV
  - Preview e validação idênticos ao modo texto (mesma tabela)
- **Modo texto:** permanece exatamente como está hoje
- `parsed` e `inserts` são compartilhados — independente do modo de entrada, o resultado vai pro mesmo estado e o botão "Adicionar" funciona igual

### 2. `index.css` — Estilos
- Adicionar estilos para a área de upload/drop zone (`.csv-upload-area`)
- Botão de download do modelo (`.csv-download-link`)
- Reutilizar classes existentes (`tab-menu`, `tab-item`, `button-secondary`)

### Não será alterado
- `types.ts` — WppDestinatarioInsert já atende
- `DashboardDisparos.tsx` — não precisa mexer
- Edge functions — não precisa mexer
- Nenhuma dependência externa (sem lib de CSV parser — o formato é simples o suficiente para parse nativo)

## Fluxo do usuário
1. Abre modal "Adicionar Destinatários"
2. Vê 2 abas: "Colar texto" | "Importar CSV"
3. Na aba CSV: clica "Baixar modelo" → recebe arquivo .csv de exemplo
4. Preenche o CSV, volta e faz upload
5. Preview mostra contatos válidos/inválidos (mesma tabela de hoje)
6. Clica "Adicionar X Contatos"
