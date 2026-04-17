# Contributing

## Add a new tool

1. Implement the function in `src/core/tools/`
2. Register it in `src/core/tools/registry.py` (TOOL_REGISTRY + TOOL_DEFINITIONS)
3. Add tests in `tests/` covering your use case

## Create a new agent

1. Create `src/core/agents/my_agent.py` inheriting or adapting `BaseAgent`
2. Add the corresponding endpoint in `src/main.py`

## PR Workflow

1. `git checkout -b feat/my-feature`
2. `pytest tests/`
3. Open a PR with the expected behavior described
