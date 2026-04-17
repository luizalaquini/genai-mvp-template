# Arquitetura

## Visao geral

```
User
 |
 v
API (FastAPI)
 |
 v
InputGuard  <-- valida e sanitiza
 |
 v
BaseAgent (loop ReAct)
 |-- Memory (contexto da conversa)
 |-- Tools (acoes no mundo externo)
 |-- LLM (raciocinio)
 |
 v
OutputGuard <-- valida resposta
 |
 v
User
```

## Loop do agente (ReAct)

1. **Reason** — LLM raciocina sobre a tarefa e decide qual tool usar
2. **Act** — Executa a tool
3. **Observe** — Recebe o resultado e adiciona na memoria
4. Repete ate `stop_reason == end_turn` ou `max_iterations`

## Decisoes tecnicas

| Decisao | Escolha | Motivo |
|---------|---------|--------|
| Padrao de agente | ReAct | Simples, auditavel, funciona bem com Claude |
| Memoria | Buffer (sliding window) | Zero dependencias no MVP |
| Registro de tools | Dict central | Facil adicionar/remover tools |
| Guardrails | Funcoes puras | Testavel e sem overhead |

## ADRs

Adicione decisoes relevantes: `docs/adr-001-escolha-memoria.md`
