import json, urllib.request, os, sys
sys.stdout.reconfigure(encoding='utf-8')

api_key = os.environ['CLICKUP_API_KEY']

content = """# Disparos de WhatsApp Oficial (Vendemais)

## O que é?

O módulo de WhatsApp do Vendemais permite **criar e gerenciar campanhas de disparo em massa** usando a API oficial da Meta. É a forma organizada de enviar mensagens para listas de contatos, com rastreamento de entrega, leitura e respostas.

Acesso: [vendemais.clubpetro.com/whatsapp](https://vendemais.clubpetro.com/whatsapp/)
* * *

## Como funciona?

A tela tem **3 abas** principais:

| Aba | O que faz |
| --- | --- |
| **Campanhas** | Criar campanhas, montar listas de contatos, acompanhar disparos |
| **Templates** | Criar e gerenciar modelos de mensagem aprovados pela Meta |
| **Números** | Gerenciar os números de WhatsApp usados para envio |

* * *

## Campanhas — Passo a passo

### 1. Criar campanha

Clique em "+ Nova Campanha" e preencha:
- **Nome** — identifique a campanha (ex: "Reativação Abril")
- **Número de disparo** — de qual número a mensagem vai sair
- **Template** — qual modelo de mensagem usar (só aparecem os aprovados pela Meta)

A campanha é criada em **rascunho**.

### 2. Montar a lista de contatos

Selecione a campanha e clique em "Adicionar Destinatários". Existem **3 formas** de montar a lista:

#### Colar texto
Cole os telefones um por linha. Aceita dois formatos:
- Só o número: `5511999998888`
- Número e nome: `5511999998888;João Silva`

#### Importar CSV
Faça upload de um arquivo `.csv` com as colunas `telefone` e `nome`, separadas por `;` ou `,`. Tem um modelo para baixar direto no modal.

#### Segmentação RD Station
Puxa contatos **direto de uma segmentação do RD Station**:
1. Clique na aba "Segmentação RD"
2. Comece a digitar o nome da segmentação para buscar
3. Selecione a segmentação desejada
4. O sistema busca o celular de cada contato automaticamente (com barra de progresso)
5. Contatos sem celular ou com número incompleto aparecem como inválidos

Nos 3 métodos, um **preview** mostra quantos contatos são válidos e quantos são inválidos antes de confirmar.

### 3. Disparar

Depois de montar a lista, clique em "Marcar como Pronta". O backend pega a campanha e inicia o envio automaticamente.

### 4. Acompanhar resultados

Com a campanha selecionada, você vê em tempo real:
- **Enviados** — mensagens que saíram do servidor
- **Entregues** — mensagens que chegaram no celular do destinatário
- **Lidos** — mensagens que o destinatário abriu
- **Respostas** — mensagens que o destinatário respondeu
- **Falhas** — envios que deram erro (com o motivo do erro)

Cada destinatário mostra seu status individual na tabela abaixo.

* * *

## Templates — Modelos de mensagem

### O que são?

A Meta **exige** que toda mensagem enviada em massa use um template pré-aprovado. Não é possível enviar texto livre em campanhas.

### Como criar um template

Clique em "+ Criar Template" e preencha:
- **Nome** — em letras minúsculas com underline (ex: `reativacao_abril`)
- **Categoria** — MARKETING (promoções, novidades) ou UTILITY (avisos, confirmações)
- **Idioma** — Português Brasil, Inglês ou Espanhol
- **Componentes**:
  - **Cabeçalho** (opcional) — título curto
  - **Corpo** (obrigatório) — texto principal. Use `{{1}}`, `{{2}}` para variáveis personalizáveis
  - **Rodapé** (opcional) — texto pequeno (ex: "ClubPetro")
  - **Botões** (opcional, máx 3) — resposta rápida ou link

Um preview em tempo real mostra como a mensagem vai ficar no WhatsApp.

### Aprovação da Meta

Após criar, o template fica em **Pendente** (amarelo). A Meta revisa e pode:
- **Aprovar** (verde) — pronto para usar em campanhas
- **Rejeitar** (vermelho) — precisa ajustar e reenviar

Só templates aprovados aparecem na criação de campanhas.

* * *

## Números — Gestão de linhas WhatsApp

### O que são?

São os números de telefone cadastrados na conta WhatsApp Business da Meta. Cada campanha envia de um número específico.

### Como adicionar um número

Clique em "+ Adicionar Número" e siga os 3 passos:
1. **Dados** — selecione a conta WABA, preencha o nome verificado e o número com DDI
2. **Verificação** — escolha receber código por SMS ou ligação, depois insira o código
3. **Confirmação** — número ativo e pronto para uso

### Qualidade do número

A Meta monitora a qualidade de cada número:
- **Verde** — tudo certo, boa taxa de entrega
- **Amarelo** — atenção, monitorar performance
- **Vermelho** — problemas de entrega, pode haver restrições

* * *

## Ciclo de vida de uma campanha

| Status | O que significa |
| --- | --- |
| **Rascunho** | Campanha criada, ainda montando lista ou ajustando |
| **Pronta** | Lista finalizada, aguardando início do disparo |
| **Disparando** | Envio em andamento |
| **Concluída** | Todos os envios finalizados |
| **Pausada** | Disparo interrompido |

* * *

## Ciclo de vida de cada destinatário

| Status | O que significa |
| --- | --- |
| **Pendente** | Na fila, ainda não enviado |
| **Enviado** | Mensagem saiu do servidor |
| **Entregue** | Chegou no celular do destinatário |
| **Lido** | Destinatário abriu a mensagem |
| **Falha** | Não foi possível enviar (número inválido, WhatsApp desativado, etc) |

**Importante:** se você adiciona uma nova lista depois de um disparo, somente os novos contatos (com status "Pendente") serão enviados no próximo disparo. Os que já foram enviados não são re-enviados.

* * *

## Validação de telefone

Para um número ser considerado **válido**, precisa ter entre **10 e 15 dígitos** (após remover parênteses, traços e espaços).

Exemplos:
- `5511999998888` (13 dígitos, com DDI) — válido
- `11999998888` (11 dígitos, sem DDI) — válido
- `999998888` (9 dígitos, falta DDD) — inválido
- `91485407` (8 dígitos) — inválido

Números incompletos geralmente são cadastros mal feitos na origem (RD Station ou lista manual).

* * *

## Perguntas frequentes

**Posso usar texto livre sem template?**
Não. A Meta exige templates aprovados para mensagens em massa. Isso garante que as mensagens sigam as políticas do WhatsApp.

**O que acontece se eu subir duas listas na mesma campanha?**
Os contatos são somados. Se a primeira lista já foi disparada, os contatos dela ficam com status "Enviado" e não são re-enviados. Só os novos (status "Pendente") serão disparados.

**Contatos sem celular no RD Station aparecem?**
Sim, mas como inválidos. O sistema busca primeiro o campo "celular" e depois "telefone pessoal" do RD. Se nenhum estiver preenchido ou o número estiver incompleto, aparece como inválido no preview.

**Qual a diferença entre Entregue e Lido?**
Entregue = chegou no celular. Lido = a pessoa abriu a conversa e viu a mensagem. Se o destinatário desativou a confirmação de leitura, pode ficar em "Entregue" para sempre.

**O número pode ser bloqueado pela Meta?**
Sim, se a qualidade cair muito (muitas denúncias ou bloqueios pelos destinatários). Monitore o indicador de qualidade na aba "Números".

* * *

## Infraestrutura (para referência)

| Componente | O que é |
| --- | --- |
| **Vendemais** | Interface de gestão (frontend) |
| **Supabase** | Banco de dados: tabelas `wpp_campanhas`, `wpp_destinatarios`, `wpp_respostas` |
| **wpp-templates-proxy** | Serviço que conecta com a API da Meta (templates, números) |
| **rd-station-proxy** | Serviço que conecta com o RD Station (segmentações, contatos) |
| **Meta WhatsApp API** | API oficial da Meta para envio de mensagens |

O token do RD Station é renovado automaticamente quando expira (a cada 24h). Não precisa de ação manual.
"""

payload = json.dumps({
    'name': 'Disparos de WhatsApp Oficial (Vendemais)',
    'parent_page_id': '8cdvx3h-460473',
    'content': content,
    'content_format': 'text/md'
}).encode('utf-8')

req = urllib.request.Request(
    'https://api.clickup.com/api/v3/workspaces/9007133809/docs/8cdvx3h-133393/pages',
    data=payload,
    method='POST'
)
req.add_header('Authorization', api_key)
req.add_header('Content-Type', 'application/json; charset=utf-8')

try:
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read().decode('utf-8'))
    print(f"Pagina criada: {result.get('id', '?')}")
    print(f"Nome: {result.get('name', '?')}")
except urllib.error.HTTPError as e:
    body = e.read().decode('utf-8')
    print(f"Erro {e.code}: {body}")
