import json
import uuid

def uid():
    return str(uuid.uuid4())

SUPA_CRED = {"supabaseApi": {"id": "E124roxIkDjglv24", "name": "Supabase - [Com&Mkt]"}}
WPP_CRED = {"whatsAppApi": {"id": "kNfW4MC2xJaFa6n0", "name": "Whatsapp Marketing"}}
WPP_TRIGGER_CRED = {"whatsAppTriggerApi": {"id": "QBy0v1GZcHbJEpLU", "name": "Trigger Whatsapp Marketing"}}

# ============================================================
# NODES
# ============================================================
nodes = []

# --- ENVIO PATH ---

# 1. Manual Trigger (preservar ID original)
nodes.append({
    "parameters": {},
    "type": "n8n-nodes-base.manualTrigger",
    "typeVersion": 1,
    "position": [-240, 200],
    "id": "4ff2049c-70e9-4ae9-9be3-7384b13ab0c2",
    "name": "Disparo Manual"
})

# 2. Buscar Campanha Pronta
nodes.append({
    "parameters": {
        "operation": "getAll",
        "tableId": "wpp_campanhas",
        "returnAll": False,
        "limit": 1,
        "matchType": "allFilters",
        "filters": {
            "conditions": [
                {"keyName": "status", "condition": "eq", "keyValue": "pronta"}
            ]
        }
    },
    "type": "n8n-nodes-base.supabase",
    "typeVersion": 1,
    "position": [40, 200],
    "id": uid(),
    "name": "Buscar Campanha Pronta",
    "credentials": SUPA_CRED
})

# 3. Iniciar Campanha (status → disparando)
nodes.append({
    "parameters": {
        "operation": "update",
        "tableId": "wpp_campanhas",
        "filters": {
            "conditions": [
                {"keyName": "id", "condition": "eq", "keyValue": "={{ $json.id }}"}
            ]
        },
        "fieldsUi": {
            "fieldValues": [
                {"fieldId": "status", "fieldValue": "disparando"},
                {"fieldId": "started_at", "fieldValue": "={{ new Date().toISOString() }}"}
            ]
        }
    },
    "type": "n8n-nodes-base.supabase",
    "typeVersion": 1,
    "position": [280, 200],
    "id": uid(),
    "name": "Iniciar Campanha",
    "credentials": SUPA_CRED
})

# 4. Buscar Destinatarios pendentes
nodes.append({
    "parameters": {
        "operation": "getAll",
        "tableId": "wpp_destinatarios",
        "returnAll": True,
        "matchType": "allFilters",
        "filters": {
            "conditions": [
                {"keyName": "campanha_id", "condition": "eq", "keyValue": "={{ $json.id }}"},
                {"keyName": "status", "condition": "eq", "keyValue": "pendente"}
            ]
        }
    },
    "type": "n8n-nodes-base.supabase",
    "typeVersion": 1,
    "position": [520, 200],
    "id": uid(),
    "name": "Buscar Destinatários",
    "credentials": SUPA_CRED
})

# 5. Loop
nodes.append({
    "parameters": {"options": {}},
    "type": "n8n-nodes-base.splitInBatches",
    "typeVersion": 3,
    "position": [760, 200],
    "id": uid(),
    "name": "Loop"
})

# 6. Enviar WhatsApp (Meta API, template dinâmico)
meta_body = (
    '={\n'
    '  "messaging_product": "whatsapp",\n'
    '  "recipient_type": "individual",\n'
    '  "to": "{{ $json.telefone }}",\n'
    '  "type": "template",\n'
    '  "template": {\n'
    '    "name": "{{ $(\'Buscar Campanha Pronta\').first().json.template_name }}",\n'
    '    "language": {\n'
    '      "code": "{{ $(\'Buscar Campanha Pronta\').first().json.template_language }}"\n'
    '    }\n'
    '  }\n'
    '}'
)
nodes.append({
    "parameters": {
        "method": "POST",
        "url": "https://graph.facebook.com/v22.0/950546414815263/messages",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "whatsAppApi",
        "sendBody": True,
        "specifyBody": "json",
        "jsonBody": meta_body,
        "options": {}
    },
    "type": "n8n-nodes-base.httpRequest",
    "typeVersion": 4.3,
    "position": [1020, 260],
    "id": uid(),
    "name": "Enviar WhatsApp",
    "credentials": WPP_CRED,
    "onError": "continueRegularOutput"
})

# 7. Envio OK?
nodes.append({
    "parameters": {
        "conditions": {
            "options": {
                "caseSensitive": True,
                "leftValue": "",
                "typeValidation": "strict",
                "version": 3
            },
            "conditions": [
                {
                    "id": uid(),
                    "leftValue": "={{ $json.messages }}",
                    "rightValue": "",
                    "operator": {
                        "type": "object",
                        "operation": "exists",
                        "singleValue": True
                    }
                }
            ],
            "combinator": "and"
        },
        "options": {}
    },
    "type": "n8n-nodes-base.if",
    "typeVersion": 2.3,
    "position": [1280, 260],
    "id": uid(),
    "name": "Envio OK?"
})

# 8. Marcar Enviado
nodes.append({
    "parameters": {
        "operation": "update",
        "tableId": "wpp_destinatarios",
        "filters": {
            "conditions": [
                {"keyName": "id", "condition": "eq", "keyValue": "={{ $('Loop').item.json.id }}"}
            ]
        },
        "fieldsUi": {
            "fieldValues": [
                {"fieldId": "status", "fieldValue": "enviado"},
                {"fieldId": "wamid", "fieldValue": "={{ $json.messages[0].id }}"},
                {"fieldId": "enviado_at", "fieldValue": "={{ new Date().toISOString() }}"}
            ]
        }
    },
    "type": "n8n-nodes-base.supabase",
    "typeVersion": 1,
    "position": [1520, 180],
    "id": uid(),
    "name": "Marcar Enviado",
    "credentials": SUPA_CRED
})

# 9. Marcar Falha
nodes.append({
    "parameters": {
        "operation": "update",
        "tableId": "wpp_destinatarios",
        "filters": {
            "conditions": [
                {"keyName": "id", "condition": "eq", "keyValue": "={{ $('Loop').item.json.id }}"}
            ]
        },
        "fieldsUi": {
            "fieldValues": [
                {"fieldId": "status", "fieldValue": "falha"},
                {"fieldId": "erro", "fieldValue": "={{ $json.message || 'Erro no envio' }}"}
            ]
        }
    },
    "type": "n8n-nodes-base.supabase",
    "typeVersion": 1,
    "position": [1520, 360],
    "id": uid(),
    "name": "Marcar Falha",
    "credentials": SUPA_CRED
})

# 10. Aguardar 2s
nodes.append({
    "parameters": {"amount": 2},
    "type": "n8n-nodes-base.wait",
    "typeVersion": 1.1,
    "position": [1760, 260],
    "id": uid(),
    "name": "Aguardar",
    "webhookId": uid()
})

# 11. Finalizar Campanha
nodes.append({
    "parameters": {
        "operation": "update",
        "tableId": "wpp_campanhas",
        "filters": {
            "conditions": [
                {"keyName": "id", "condition": "eq", "keyValue": "={{ $('Buscar Campanha Pronta').first().json.id }}"}
            ]
        },
        "fieldsUi": {
            "fieldValues": [
                {"fieldId": "status", "fieldValue": "concluida"},
                {"fieldId": "finished_at", "fieldValue": "={{ new Date().toISOString() }}"}
            ]
        }
    },
    "type": "n8n-nodes-base.supabase",
    "typeVersion": 1,
    "position": [1020, 60],
    "id": uid(),
    "name": "Finalizar Campanha",
    "credentials": SUPA_CRED
})

# --- WEBHOOK PATH ---

# 12. WhatsApp Trigger (preservar IDs originais)
nodes.append({
    "parameters": {
        "updates": ["messages"],
        "options": {}
    },
    "type": "n8n-nodes-base.whatsAppTrigger",
    "typeVersion": 1,
    "position": [-240, -200],
    "id": "3d4169f6-74f8-4664-a170-0c9be7c81319",
    "name": "WhatsApp Trigger",
    "webhookId": "d101dc03-8802-402f-8639-1771c7226e0d",
    "credentials": WPP_TRIGGER_CRED
})

# 13. Tem Texto?
nodes.append({
    "parameters": {
        "conditions": {
            "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict", "version": 3},
            "conditions": [{
                "id": uid(),
                "leftValue": "={{ $json.messages[0].text.body }}",
                "rightValue": "",
                "operator": {"type": "string", "operation": "notEmpty", "singleValue": True}
            }],
            "combinator": "and"
        },
        "options": {}
    },
    "type": "n8n-nodes-base.if",
    "typeVersion": 2.3,
    "position": [40, -200],
    "id": uid(),
    "name": "Tem Texto?"
})

# 14. Salvar Resposta Texto
nodes.append({
    "parameters": {
        "tableId": "wpp_respostas",
        "fieldsUi": {
            "fieldValues": [
                {"fieldId": "telefone", "fieldValue": "={{ $json.contacts[0].wa_id }}"},
                {"fieldId": "tipo", "fieldValue": "texto"},
                {"fieldId": "conteudo", "fieldValue": "={{ $json.messages[0].text.body }}"}
            ]
        }
    },
    "type": "n8n-nodes-base.supabase",
    "typeVersion": 1,
    "position": [320, -300],
    "id": uid(),
    "name": "Salvar Resposta Texto",
    "credentials": SUPA_CRED
})

# 15. Tem Botão?
nodes.append({
    "parameters": {
        "conditions": {
            "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict", "version": 3},
            "conditions": [{
                "id": uid(),
                "leftValue": "={{ $json.messages[0].button.payload }}",
                "rightValue": "",
                "operator": {"type": "string", "operation": "exists", "singleValue": True}
            }],
            "combinator": "and"
        },
        "options": {}
    },
    "type": "n8n-nodes-base.if",
    "typeVersion": 2.3,
    "position": [320, -100],
    "id": uid(),
    "name": "Tem Botão?"
})

# 16. Salvar Resposta Botão
nodes.append({
    "parameters": {
        "tableId": "wpp_respostas",
        "fieldsUi": {
            "fieldValues": [
                {"fieldId": "telefone", "fieldValue": "={{ $('WhatsApp Trigger').item.json.contacts[0].wa_id }}"},
                {"fieldId": "tipo", "fieldValue": "botao"},
                {"fieldId": "conteudo", "fieldValue": "={{ $('WhatsApp Trigger').item.json.messages[0].button.text }}"}
            ]
        }
    },
    "type": "n8n-nodes-base.supabase",
    "typeVersion": 1,
    "position": [600, -200],
    "id": uid(),
    "name": "Salvar Resposta Botão",
    "credentials": SUPA_CRED
})

# 17. Tipo de Status (Switch)
nodes.append({
    "parameters": {
        "rules": {
            "values": [
                {
                    "conditions": {
                        "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict", "version": 3},
                        "conditions": [{
                            "leftValue": "={{ $json.statuses[0].status }}",
                            "rightValue": "read",
                            "operator": {"type": "string", "operation": "equals"},
                            "id": uid()
                        }],
                        "combinator": "and"
                    }
                },
                {
                    "conditions": {
                        "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict", "version": 3},
                        "conditions": [{
                            "leftValue": "={{ $json.statuses[0].status }}",
                            "rightValue": "delivered",
                            "operator": {"type": "string", "operation": "equals", "name": "filter.operator.equals"},
                            "id": uid()
                        }],
                        "combinator": "and"
                    }
                },
                {
                    "conditions": {
                        "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict", "version": 3},
                        "conditions": [{
                            "leftValue": "={{ $json.statuses[0].status }}",
                            "rightValue": "failed",
                            "operator": {"type": "string", "operation": "equals", "name": "filter.operator.equals"},
                            "id": uid()
                        }],
                        "combinator": "and"
                    }
                }
            ]
        },
        "options": {}
    },
    "type": "n8n-nodes-base.switch",
    "typeVersion": 3.4,
    "position": [600, -40],
    "id": uid(),
    "name": "Tipo de Status"
})

# 18. Atualizar Lido
nodes.append({
    "parameters": {
        "operation": "update",
        "tableId": "wpp_destinatarios",
        "filters": {
            "conditions": [
                {"keyName": "wamid", "condition": "eq", "keyValue": "={{ $json.statuses[0].id }}"}
            ]
        },
        "fieldsUi": {
            "fieldValues": [
                {"fieldId": "status", "fieldValue": "lido"},
                {"fieldId": "lido_at", "fieldValue": "={{ new Date().toISOString() }}"}
            ]
        }
    },
    "type": "n8n-nodes-base.supabase",
    "typeVersion": 1,
    "position": [880, -120],
    "id": uid(),
    "name": "Atualizar Lido",
    "credentials": SUPA_CRED
})

# 19. Atualizar Entregue
nodes.append({
    "parameters": {
        "operation": "update",
        "tableId": "wpp_destinatarios",
        "filters": {
            "conditions": [
                {"keyName": "wamid", "condition": "eq", "keyValue": "={{ $json.statuses[0].id }}"}
            ]
        },
        "fieldsUi": {
            "fieldValues": [
                {"fieldId": "status", "fieldValue": "entregue"},
                {"fieldId": "entregue_at", "fieldValue": "={{ new Date().toISOString() }}"}
            ]
        }
    },
    "type": "n8n-nodes-base.supabase",
    "typeVersion": 1,
    "position": [880, -40],
    "id": uid(),
    "name": "Atualizar Entregue",
    "credentials": SUPA_CRED
})

# 20. Atualizar Falha (webhook)
nodes.append({
    "parameters": {
        "operation": "update",
        "tableId": "wpp_destinatarios",
        "filters": {
            "conditions": [
                {"keyName": "wamid", "condition": "eq", "keyValue": "={{ $json.statuses[0].id }}"}
            ]
        },
        "fieldsUi": {
            "fieldValues": [
                {"fieldId": "status", "fieldValue": "falha"},
                {"fieldId": "erro", "fieldValue": "=falha na entrega"}
            ]
        }
    },
    "type": "n8n-nodes-base.supabase",
    "typeVersion": 1,
    "position": [880, 40],
    "id": uid(),
    "name": "Atualizar Falha Entrega",
    "credentials": SUPA_CRED
})

# ============================================================
# CONNECTIONS
# ============================================================
connections = {
    # ENVIO PATH
    "Disparo Manual": {
        "main": [[{"node": "Buscar Campanha Pronta", "type": "main", "index": 0}]]
    },
    "Buscar Campanha Pronta": {
        "main": [[{"node": "Iniciar Campanha", "type": "main", "index": 0}]]
    },
    "Iniciar Campanha": {
        "main": [[{"node": "Buscar Destinatários", "type": "main", "index": 0}]]
    },
    "Buscar Destinatários": {
        "main": [[{"node": "Loop", "type": "main", "index": 0}]]
    },
    "Loop": {
        "main": [
            [{"node": "Finalizar Campanha", "type": "main", "index": 0}],  # output 0 = done
            [{"node": "Enviar WhatsApp", "type": "main", "index": 0}]      # output 1 = loop item
        ]
    },
    "Enviar WhatsApp": {
        "main": [[{"node": "Envio OK?", "type": "main", "index": 0}]]
    },
    "Envio OK?": {
        "main": [
            [{"node": "Marcar Enviado", "type": "main", "index": 0}],  # TRUE
            [{"node": "Marcar Falha", "type": "main", "index": 0}]     # FALSE
        ]
    },
    "Marcar Enviado": {
        "main": [[{"node": "Aguardar", "type": "main", "index": 0}]]
    },
    "Marcar Falha": {
        "main": [[{"node": "Aguardar", "type": "main", "index": 0}]]
    },
    "Aguardar": {
        "main": [[{"node": "Loop", "type": "main", "index": 0}]]
    },

    # WEBHOOK PATH
    "WhatsApp Trigger": {
        "main": [[{"node": "Tem Texto?", "type": "main", "index": 0}]]
    },
    "Tem Texto?": {
        "main": [
            [{"node": "Salvar Resposta Texto", "type": "main", "index": 0}],  # TRUE
            [{"node": "Tem Botão?", "type": "main", "index": 0}]               # FALSE
        ]
    },
    "Tem Botão?": {
        "main": [
            [{"node": "Salvar Resposta Botão", "type": "main", "index": 0}],   # TRUE
            [{"node": "Tipo de Status", "type": "main", "index": 0}]            # FALSE
        ]
    },
    "Tipo de Status": {
        "main": [
            [{"node": "Atualizar Lido", "type": "main", "index": 0}],          # read
            [{"node": "Atualizar Entregue", "type": "main", "index": 0}],      # delivered
            [{"node": "Atualizar Falha Entrega", "type": "main", "index": 0}]  # failed
        ]
    }
}

# ============================================================
# WORKFLOW COMPLETO
# ============================================================
workflow = {
    "name": "[MKTCOM] disparo-oficial",
    "nodes": nodes,
    "connections": connections,
    "settings": {
        "executionOrder": "v1",
        "binaryMode": "separate"
    }
}

output_path = r"C:\Users\ClubPetro-123\Documents\cmo_cp\workflow_update.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(workflow, f, indent=2, ensure_ascii=False)

print(f"Workflow JSON salvo em {output_path}")
print(f"Total de nodes: {len(nodes)}")
print(f"Connections: {len(connections)} sources")
