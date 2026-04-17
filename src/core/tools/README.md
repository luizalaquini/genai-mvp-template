# Tools - Agent Tools

Central tool registry that agents can call to execute actions.

## Architecture

```
Agent needs an action
    ↓
Lookup TOOL_REGISTRY
    ↓
Execute tool with parameters
    ↓
Return result to Agent
    ↓
Agent observes and continues
```

## Folder Structure

```
src/core/tools/
├── example_tools.py      # Tool implementations
├── registry.py           # Central registry (TOOL_REGISTRY, TOOL_DEFINITIONS)
└── README.md
```

## How It Works

### 1. registry.py - Central Registry

Defines available tools in **two formats:**

**a) TOOL_REGISTRY** (Python)
```python
TOOL_REGISTRY = {
    "get_current_date": get_current_date,
    "search_web": search_web,
}
```

**b) TOOL_DEFINITIONS** (Anthropic API)
```python
TOOL_DEFINITIONS = [
    {
        "name": "get_current_date",
        "description": "Returns the current date",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    # ...
]
```

### 2. example_tools.py - Implementation

```python
def get_current_date() -> dict:
    """Returns the current date."""
    return {"date": date.today().isoformat()}

def search_web(query: str) -> dict:
    """Searches the web for information."""
    # Implement with a real API
    return {"results": [...]}
```

## Adding a New Tool

### Step 1: Implement the Function

```python
# src/core/tools/example_tools.py

def calculate_discount(price: float, discount_percent: float) -> dict:
    """Calculates the final price after a discount."""
    final_price = price * (1 - discount_percent / 100)
    return {
        "original_price": price,
        "discount_percent": discount_percent,
        "final_price": round(final_price, 2),
        "savings": round(price - final_price, 2)
    }
```

### Step 2: Import and Register in registry.py

```python
# src/core/tools/registry.py

from src.core.tools.example_tools import (
    get_current_date,
    search_web,
    calculate_discount  # New tool
)

# Python map
TOOL_REGISTRY = {
    "get_current_date": get_current_date,
    "search_web": search_web,
    "calculate_discount": calculate_discount,
}

# API definitions
TOOL_DEFINITIONS = [
    # ... existing tools ...
    {
        "name": "calculate_discount",
        "description": "Calculates the final price with discount applied",
        "input_schema": {
            "type": "object",
            "properties": {
                "price": {
                    "type": "number",
                    "description": "Original price"
                },
                "discount_percent": {
                    "type": "number",
                    "description": "Discount percentage (0-100)"
                }
            },
            "required": ["price", "discount_percent"]
        }
    }
]
```

### Step 3: Use with the Agent

```python
from src.core.agents.base_agent import BaseAgent
from anthropic import Anthropic

client = Anthropic()
agent = BaseAgent(client)

# The agent will use the tool automatically
response = agent.run("What is the final price if a product costs $100 with a 20% discount?")
print(response)
# Output: Agent will call calculate_discount(100, 20) and return $80
```

## Tool Examples

### 1. Simple Tool (no parameters)

```python
def get_current_date() -> dict:
    """Returns the current date."""
    from datetime import date
    return {"date": date.today().isoformat()}
```

### 2. Tool with Parameters

```python
def search_web(query: str, max_results: int = 5) -> dict:
    """Searches the web using an external API."""
    # Integrate with Tavily, SerpAPI, Brave Search...
    return {
        "query": query,
        "results": [...],
        "count": len(results)
    }
```

### 3. Tool with Complex Logic

```python
def analyze_sentiment(text: str) -> dict:
    """Analyzes sentiment using an AI model."""
    from transformers import pipeline
    
    classifier = pipeline("sentiment-analysis")
    result = classifier(text)[0]
    
    return {
        "text": text,
        "label": result["label"],
        "score": round(result["score"], 3)
    }
```

### 4. Tool with External API

```python
def fetch_weather(city: str) -> dict:
    """Fetches weather forecast."""
    import requests
    
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"https://api.weatherapi.com/v1/current.json"
    
    response = requests.get(url, params={
        "key": api_key,
        "q": city,
        "aqi": "yes"
    })
    
    return response.json()
```

### 5. Tool with Database Access

```python
def get_user_preferences(user_id: int) -> dict:
    """Retrieves user preferences from the database."""
    import sqlite3
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT preferences FROM users WHERE id = ?", (user_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    return {
        "user_id": user_id,
        "preferences": result[0] if result else None
    }
```

## Best Practices

### ✅ Do:

1. **Always return a dict/JSON**
   ```python
   # ✅ Good
   return {"success": True, "value": 42}
   
   # ❌ Bad
   return "The result is 42"
   ```

2. **Use descriptive names**
   ```python
   # ✅ Good
def calculate_monthly_revenue(company_id: int) -> dict:
   
   # ❌ Bad
def calc(id):
   ```

3. **Document with docstrings**
   ```python
def get_weather(city: str) -> dict:
    """
    Returns current weather conditions for a city.
    
    Args:
        city: City name (e.g. "São Paulo")
    
    Returns:
        Dict with temperature, humidity, etc.
    """
```

4. **Handle errors properly**
   ```python
def fetch_api(url: str) -> dict:
    try:
        response = requests.get(url, timeout=5)
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e), "url": url}
```

5. **Use type hints**
   ```python
def process(data: list[str], threshold: float = 0.5) -> dict:
    pass
```

### ❌ Avoid:

1. **Using print() instead of returning data**
   ```python
   # ❌ Bad
def tool():
       print("Result")
   
   # ✅ Good
def tool():
       return {"result": "Result"}
   ```

2. **Leaving errors unhandled**
   ```python
   # ❌ Bad
def fetch_api(url):
       return requests.get(url).json()
   
   # ✅ Good
def fetch_api(url):
       try:
           return requests.get(url).json()
       except Exception as e:
           return {"error": str(e)}
```

3. **Modifying global state**
   ```python
   # ❌ Bad
global_cache = {}
   
   def tool():
       global_cache["key"] = "value"
   
   # ✅ Good
def tool():
       return {"key": "value"}
```

## Advanced Patterns

### Pattern 1: Tool with Fallback

```python
def search_information(query: str) -> dict:
    """Searches with fallback."""
    try:
        return search_api_primary(query)
    except:
        try:
            return search_api_secondary(query)
        except:
            return search_local_cache(query)
```

### Pattern 2: Tool with Cache

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_calculation(x: int) -> dict:
    """Expensive calculation with caching."""
    result = sum(i**2 for i in range(x))
    return {"input": x, "result": result}
```

### Pattern 3: Async Tool

```python
import asyncio

async def fetch_multiple_sources(query: str) -> dict:
    """Fetches multiple sources in parallel."""
    tasks = [
        search_source_a(query),
        search_source_b(query),
        search_source_c(query)
    ]
    results = await asyncio.gather(*tasks)
    return {"query": query, "sources": results}
```

### Pattern 4: Rate-limited Tool

```python
import time
from functools import wraps

def rate_limit(calls_per_minute):
    def decorator(func):
        last_called = [0.0]
        min_interval = 60.0 / calls_per_minute
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

@rate_limit(calls_per_minute=10)
def api_call(endpoint: str) -> dict:
    pass
```

## Testing Tools

```python
# test_tools.py
from src.core.tools.example_tools import calculate_discount

def test_calculate_discount():
    result = calculate_discount(100, 20)
    assert result["final_price"] == 80
    assert result["savings"] == 20
```

## Integration with Security Checks

If you want to validate that tools do not perform suspicious actions:

```python
# src/core/guardrails/tool_guard.py
def validate_tool_call(tool_name: str, inputs: dict) -> bool:
    """Validates whether the tool call is allowed."""
    blocked_tools = ["delete_database", "execute_shell"]
    if tool_name in blocked_tools:
        return False
    
    if tool_name == "search_web" and len(inputs.get("query", "")) > 500:
        return False
    
    return True
```

## Troubleshooting

| Problem | Cause | Fix |
|----------|-------|---------|
| Tool not found | Not registered in registry | Add it to TOOL_REGISTRY |
| Execution error | Incorrect parameters | Check input_schema |
| Timeout | Tool too slow | Add caching or async behavior |
| Agent does not use tool | Output is not a dict | Always return a dict |

## Next Steps

- [ ] Implement tools for your use case
- [ ] Add real web search with API integration (Tavily, SerpAPI)
- [ ] Integrate with a database
- [ ] Implement rate limiting
- [ ] Add caching
- [ ] Create tests for tools
