# CMO ClubPetro - Visão Estratégica

## Propósito
Hub estratégico do CMO do ClubPetro para debater estratégia, construir visão de liderança de marketing e integrar ferramentas de trabalho. O foco é onboardar as métricas-chave (DRE, pipeline, churn, CAC, LTV etc.) para ter uma base de dados sólida que sustente decisões estratégicas.

## Stack de Integrações
- **Supabase**: banco de dados e backend (MCP configurado)
- **ClickUp**: gestão de tarefas e projetos (via API REST, key no `.env`)
- **Gmail**: comunicação (via MCP)
- **Google Calendar**: agenda (via MCP)
- **Canva**: design e criação (via MCP)
- **Indeed**: recrutamento (via MCP)
- **Vendemais**: sistema integrador interno para Marketing e Comercial (repo em `C:\Users\ClubPetro-123\Documents\vendemais`)

## Workflow Vendemais (OBRIGATÓRIO)
Ao fazer qualquer alteração no Vendemais:
1. Criar branch a partir de `main`
2. Implementar as alterações e commitar
3. Abrir PR no GitHub com descrição em **português** explicando o que foi feito
4. Retornar o link da PR para André testar e validar
5. Só fazer merge após aprovação explícita

## Pipeline de Pendências (ClickUp)
Sempre que identificar uma investigação, pendência, ideia, dúvida ou problema durante qualquer análise ou conversa, criar automaticamente uma tarefa na lista **"ClubPetro"** (ID: `901326908797`) no ClickUp.

**Regras:**
- **Descrição**: texto explicativo e corrido, sem linguagem técnica/dev. Explicar o problema, por que importa e o que precisa ser feito
- **Subtasks**: criar quando a tarefa tiver etapas distintas
- **Comentários "IA:"**: adicionar como comentário (nunca na descrição) minhas hipóteses, opiniões, sugestões de como resolver e referências. Sempre começar com "IA:" para diferenciar de comentários humanos
- **Prioridade**: usar criteriosamente (urgent/high/normal/low)
- **Tom**: comportamento o mais humano possível, como um colega escrevendo

## ClickUp API — Encoding UTF-8 (OBRIGATÓRIO)
**NUNCA usar `curl` para chamadas ao ClickUp que contenham texto com caracteres especiais** (acentos, cedilha, etc.). O curl no Git Bash/Windows corrompe a codificação.

**Sempre usar Python `urllib.request`:**
```python
import json, urllib.request

data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, method='POST')  # ou PUT, etc.
req.add_header('Authorization', api_key)
req.add_header('Content-Type', 'application/json; charset=utf-8')
resp = urllib.request.urlopen(req)
```

Isso se aplica a **todas** as operações com texto: criar tarefas, atualizar tarefas, postar comentários, criar subtasks, etc.

## Workflow de Tarefas
- Ao finalizar uma pendência: usar `/finalizar-task` para reportar o que foi feito (comentário "IA:") e mover para "checando resultados"
- Para validar se algo funciona: usar `/testar-task` para desenhar e executar testes automatizados

## Idioma
- Comunicação em português brasileiro
- Código e configs em inglês
