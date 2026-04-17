"""
Registro central de ferramentas.
Adicione novas tools aqui para que o agente possa usa-las.
"""
from src.core.tools.example_tools import get_current_date, search_web

# Mapa nome -> funcao
TOOL_REGISTRY = {
    "get_current_date": get_current_date,
    "search_web": search_web,
}

# Definicoes no formato Anthropic tool_use
TOOL_DEFINITIONS = [
    {
        "name": "get_current_date",
        "description": "Retorna a data atual.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "search_web",
        "description": "Busca informacoes na web sobre um topico.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Termo de busca"}
            },
            "required": ["query"],
        },
    },
]
