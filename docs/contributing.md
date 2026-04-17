# Contribuindo

## Adicionar uma nova tool

1. Implemente a funcao em `src/core/tools/`
2. Registre em `src/core/tools/registry.py` (TOOL_REGISTRY + TOOL_DEFINITIONS)
3. Adicione testes em `tests/` cobrindo seu caso de uso

## Criar um novo agente

1. Crie `src/core/agents/meu_agente.py` herdando ou adaptando `BaseAgent`
2. Adicione endpoint correspondente em `src/main.py`

## Fluxo de PR

1. `git checkout -b feat/minha-feature`
2. `pytest tests/`
3. Abra o PR com descricao do comportamento esperado
