# Agents - Autonomous Agents

Agents that reason about tasks and execute actions autonomously using the **ReAct loop** (Reason + Act).

## Architecture

```
Task Input
    ↓
[REASON] - Decide which action to take
    ↓
[ACT] - Execute a tool or respond
    ↓
[OBSERVE] - Observe the result
    ↓
Repeat until completion or max_iterations
    ↓
Final Response
```

## Agent Flow

1. **Receives a task** from the user (validated via `input_guard`)
2. **Reasons** about which tool to use (or answers directly)
3. **Executes the tool** by checking `TOOL_REGISTRY`
4. **Observes the result** and adds it to memory
5. **Repeats** until finished or the iteration limit is reached
6. **Returns final response** (validated via `output_guard`)

## BaseAgent - Example Usage

```python
from anthropic import Anthropic
from src.core.agents.base_agent import BaseAgent

# Initialize AI client
client = Anthropic()

# Create an agent with up to 10 iterations
agent = BaseAgent(model_client=client, max_iterations=10)

# Execute a task
response = agent.run("What is the capital of Brazil and how many inhabitants does it have?")
print(response)
```

## Main Components

### BaseAgent

**Responsibilities:**
- Manage the ReAct loop
- Validate input and output
- Maintain conversation memory
- Execute tools dynamically

**Attributes:**
- `client`: AI client (e.g. Anthropic)
- `max_iterations`: Iteration limit (default: 10)
- `memory`: Conversation context (ConversationMemory)

**Methods:**
- `run(task: str) -> str`: Execute the task and return the response
- `_execute_tool(name, inputs)`: Execute a tool from the registry
- `_system_prompt()`: Return the system prompt for the model

### Integration with Other Components

```
Agent
├── Memory (ConversationMemory)
│   └── Keeps recent context
├── Tools (TOOL_REGISTRY)
│   └── Available tools
├── Prompts (system_prompt)
│   └── Instructions for the model
├── Input Guard
│   └── Validates user input
└── Output Guard
    └── Validates final response
```

## Creating Your Own Agent

```python
from src.core.agents.base_agent import BaseAgent
from src.core.memory.short_term import ConversationMemory
from src.core.memory.long_term import LongTermMemory

class CustomAgent(BaseAgent):
    """Custom agent with long-term memory."""
    
    def __init__(self, model_client, max_iterations=10):
        super().__init__(model_client, max_iterations)
        self.long_term_memory = LongTermMemory(collection_name="custom_agent")
    
    def run(self, task: str) -> str:
        # 1. Retrieve relevant history
        relevant_context = self.long_term_memory.retrieve_by_topic("general")
        
        # 2. Run the agent normally
        response = super().run(task)
        
        # 3. If the conversation reaches the limit, store a summary
        if len(self.memory) >= 20:
            summary = self._summarize_conversation()
            self.long_term_memory.store(
                content=summary,
                metadata={"topic": "general", "importance": "medium"}
            )
            self.memory.clear()
        
        return response
    
    def _summarize_conversation(self) -> str:
        """Summarize the conversation for LongTermMemory."""
        messages = self.memory.get_all()
        # Here you would call an LLM to generate the summary
        return "Conversation summary..."
```

## Adding New Tools

1. Implement the function in `src/core/tools/example_tools.py`
2. Register it in `src/core/tools/registry.py`
3. The agent will use it automatically

Example:

```python
# src/core/tools/example_tools.py
def calculate_sum(a: int, b: int) -> int:
    """Calculates the sum of two numbers."""
    return a + b

# src/core/tools/registry.py
from src.core.tools.example_tools import calculate_sum

TOOL_REGISTRY = {
    "calculate_sum": calculate_sum,
}

TOOL_DEFINITIONS = [
    {
        "name": "calculate_sum",
        "description": "Calculates the sum of two numbers",
        "input_schema": {
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": "integer"}
            },
            "required": ["a", "b"]
        }
    }
]
```

## Usage Patterns

### Pattern 1: Simple Agent (MVP)

```python
agent = BaseAgent(client)
response = agent.run("your task")
```

### Pattern 2: Agent with Persistent Context

```python
agent = CustomAgent(client)
# First conversation
response1 = agent.run("Learn that I like data science")
# Second conversation - access first conversation context
response2 = agent.run("Recommend a topic to study")
```

### Pattern 3: Agent with Custom Validation

```python
class SecureAgent(BaseAgent):
    def run(self, task: str) -> str:
        # Custom validation
        if len(task) > 1000:
            raise ValueError("Task is too long")
        return super().run(task)
```

## Advanced Configuration

### Adjust Model and Max Tokens

```python
# Override _system_prompt to use a different model
class AgentWithGPT(BaseAgent):
    def run(self, task: str) -> str:
        # Custom logic here
        pass
```

### Control Iterations

```python
# Less aggressive agent - fewer iterations
agent = BaseAgent(client, max_iterations=3)

# More aggressive agent - more iterations
agent = BaseAgent(client, max_iterations=20)
```

## Troubleshooting

| Problem | Cause | Fix |
|----------|-------|---------|
| Agent cannot find tool | Tool not registered | Check `TOOL_REGISTRY` |
| Incomplete response | Iteration limit too low | Increase `max_iterations` |
| Infinite loops | Tool calls itself | Review tool logic |
| Validation error | Input/output fails guard | Review guardrail rules |

## Next Steps

- [ ] Implement more tools in `src/core/tools/`
- [ ] Build custom agents for specific use cases
- [ ] Integrate with LongTermMemory for learning
- [ ] Add custom validation with guardrails
- [ ] Implement logging and monitoring
