"""
Central tool registry.
Add new tools here so the agent can use them.
"""
from src.core.tools.example_tools import get_current_date, search_web

# Map name -> function
TOOL_REGISTRY = {
    "get_current_date": get_current_date,
    "search_web": search_web,
}

# Anthropic tool_use definitions
TOOL_DEFINITIONS = [
    {
        "name": "get_current_date",
        "description": "Returns the current date.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "search_web",
        "description": "Searches the web for information on a topic.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"],
        },
    },
]
