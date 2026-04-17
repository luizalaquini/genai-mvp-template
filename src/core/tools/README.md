# Tools - Ferramentas para Agentes

Registro central de ferramentas que agentes podem chamar para executar ações.

## Arquitetura

```
Agent precisa de uma ação
    ↓
Consulta TOOL_REGISTRY
    ↓
Executa ferramenta com parâmetros
    ↓
Retorna resultado para Agent
    ↓
Agent observa e continua
```

## Estrutura de Pastas

```
src/core/tools/
├── example_tools.py      # Implementação de ferramentas
├── registry.py           # Registro central (TOOL_REGISTRY, TOOL_DEFINITIONS)
└── README.md
```

## Como Funciona

### 1. registry.py - Registro Central

Define as ferramentas disponíveis em **dois formatos:**

**a) TOOL_REGISTRY** (Python)
```python
TOOL_REGISTRY = {
    "get_current_date": get_current_date,
    "search_web": search_web,
}
```

**b) TOOL_DEFINITIONS** (API Anthropic)
```python
TOOL_DEFINITIONS = [
    {
        "name": "get_current_date",
        "description": "Retorna a data atual",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    # ...
]
```

### 2. example_tools.py - Implementação

```python
def get_current_date() -> dict:
    """Retorna a data atual."""
    return {"date": date.today().isoformat()}

def search_web(query: str) -> dict:
    """Busca informações na web."""
    # Implementar com API real
    return {"results": [...]}
```

## Adicionando uma Ferramenta

### Passo 1: Implementar a Função

```python
# src/core/tools/example_tools.py

def calculate_discount(price: float, discount_percent: float) -> dict:
    """Calcula o preço com desconto aplicado."""
    final_price = price * (1 - discount_percent / 100)
    return {
        "original_price": price,
        "discount_percent": discount_percent,
        "final_price": round(final_price, 2),
        "savings": round(price - final_price, 2)
    }
```

### Passo 2: Importar e Registrar em registry.py

```python
# src/core/tools/registry.py

from src.core.tools.example_tools import (
    get_current_date,
    search_web,
    calculate_discount  # Nova ferramenta
)

# Mapa Python
TOOL_REGISTRY = {
    "get_current_date": get_current_date,
    "search_web": search_web,
    "calculate_discount": calculate_discount,  # Adicionar aqui
}

# Definições para API
TOOL_DEFINITIONS = [
    # ... existing tools ...
    {
        "name": "calculate_discount",
        "description": "Calcula o preço final com desconto aplicado",
        "input_schema": {
            "type": "object",
            "properties": {
                "price": {
                    "type": "number",
                    "description": "Preço original"
                },
                "discount_percent": {
                    "type": "number",
                    "description": "Percentual de desconto (0-100)"
                }
            },
            "required": ["price", "discount_percent"]
        }
    }
]
```

### Passo 3: Usar com Agent

```python
from src.core.agents.base_agent import BaseAgent
from anthropic import Anthropic

client = Anthropic()
agent = BaseAgent(client)

# Agent usa a ferramenta automaticamente
response = agent.run("Qual é o preço final se um produto custa R$100 com 20% de desconto?")
print(response)
# Saída: Agent vai chamar calculate_discount(100, 20) e obter R$80
```

## Exemplos de Ferramentas

### 1. Ferramenta Simples (sem parâmetros)

```python
def get_current_date() -> dict:
    """Retorna a data atual."""
    from datetime import date
    return {"date": date.today().isoformat()}
```

### 2. Ferramenta com Parâmetros

```python
def search_web(query: str, max_results: int = 5) -> dict:
    """Busca na web usando API externa."""
    # Integrar com Tavily, SerpAPI, Brave Search...
    return {
        "query": query,
        "results": [...],
        "count": len(results)
    }
```

### 3. Ferramenta com Lógica Complexa

```python
def analyze_sentiment(text: str) -> dict:
    """Analisa sentimento usando modelo de IA."""
    from transformers import pipeline
    
    classifier = pipeline("sentiment-analysis")
    result = classifier(text)[0]
    
    return {
        "text": text,
        "label": result["label"],
        "score": round(result["score"], 3)
    }
```

### 4. Ferramenta com API Externa

```python
def fetch_weather(city: str) -> dict:
    """Busca previsão do tempo."""
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

### 5. Ferramenta com Banco de Dados

```python
def get_user_preferences(user_id: int) -> dict:
    """Recupera preferências do usuário do banco de dados."""
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

## Boas Práticas

### ✅ Faça:

1. **Retorne sempre um dict/JSON**
   ```python
   # ✅ Bom
   return {"success": True, "value": 42}
   
   # ❌ Ruim
   return "O resultado é 42"
   ```

2. **Use nomes descritivos**
   ```python
   # ✅ Bom
   def calculate_monthly_revenue(company_id: int) -> dict:
   
   # ❌ Ruim
   def calc(id):
   ```

3. **Documente com docstrings**
   ```python
   def get_weather(city: str) -> dict:
       """
       Retorna condições atuais do tempo para uma cidade.
       
       Args:
           city: Nome da cidade (ex: "São Paulo")
       
       Returns:
           Dict com temperatura, umidade, etc
       """
   ```

4. **Trate erros adequadamente**
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

### ❌ Evite:

1. **Não use print() - retorne dados**
   ```python
   # ❌ Ruim
   def tool():
       print("Resultado")
   
   # ✅ Bom
   def tool():
       return {"result": "Resultado"}
   ```

2. **Não deixe sem tratamento de erro**
   ```python
   # ❌ Ruim
   def fetch_api(url):
       return requests.get(url).json()
   
   # ✅ Bom
   def fetch_api(url):
       try:
           return requests.get(url).json()
       except Exception as e:
           return {"error": str(e)}
   ```

3. **Não modifique estado global**
   ```python
   # ❌ Ruim
   global_cache = {}
   
   def tool():
       global_cache["key"] = "value"
   
   # ✅ Bom
   def tool():
       return {"key": "value"}
   ```

## Padrões Avançados

### Pattern 1: Tool com Fallback

```python
def search_information(query: str) -> dict:
    """Busca info com fallback."""
    try:
        # Tenta API primária
        return search_api_primary(query)
    except:
        try:
            # Fallback para API secundária
            return search_api_secondary(query)
        except:
            # Último recurso - busca local
            return search_local_cache(query)
```

### Pattern 2: Tool com Cache

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_calculation(x: int) -> dict:
    """Cálculo custoso com cache."""
    result = sum(i**2 for i in range(x))
    return {"input": x, "result": result}
```

### Pattern 3: Tool Assíncrona

```python
import asyncio

async def fetch_multiple_sources(query: str) -> dict:
    """Busca de múltiplas fontes em paralelo."""
    tasks = [
        search_source_a(query),
        search_source_b(query),
        search_source_c(query)
    ]
    results = await asyncio.gather(*tasks)
    return {"query": query, "sources": results}
```

### Pattern 4: Tool com Rate Limiting

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

## Testando Ferramentas

```python
# test_tools.py
from src.core.tools.example_tools import calculate_discount

def test_calculate_discount():
    result = calculate_discount(100, 20)
    assert result["final_price"] == 80
    assert result["savings"] == 20
```

## Integração com Verificação de Segurança

Se quiser validar que ferramentas não fazem nada suspeito:

```python
# src/core/guardrails/tool_guard.py
def validate_tool_call(tool_name: str, inputs: dict) -> bool:
    """Valida se a chamada de ferramenta é permitida."""
    # Previne tools perigosas
    blocked_tools = ["delete_database", "execute_shell"]
    if tool_name in blocked_tools:
        return False
    
    # Valida parâmetros
    if tool_name == "search_web" and len(inputs.get("query", "")) > 500:
        return False
    
    return True
```

## Troubleshooting

| Problema | Causa | Solução |
|----------|-------|---------|
| Tool não encontrada | Não registrada em registry | Adicionar a TOOL_REGISTRY |
| Erro ao executar | Parâmetros incorretos | Verificar input_schema |
| Timeout | Tool muito lenta | Adicionar cache ou async |
| Agent não usa tool | Output não é dict | Retornar sempre dict |

## Próximos Passos

- [ ] Implementar ferramentas específicas do seu caso de uso
- [ ] Adicionar busca web com API real (Tavily, SerpAPI)
- [ ] Integrar com banco de dados
- [ ] Implementar rate limiting
- [ ] Adicionar caching
- [ ] Criar testes para ferramentas
