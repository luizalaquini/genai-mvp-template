# GenAI Agent Template

Template for generative AI MVPs that supports autonomous agents (ReAct, plan-and-execute) and linear pipelines.

## Structure

```
genai-mvp-template/
├── src/
│   ├── core/                 # Core engine
│   │   ├── agents/           # Autonomous agents (ReAct loop)
│   │   ├── chains/           # Linear pipelines (no loop)
│   │   ├── memory/           # Short-term and long-term memory
│   │   │   ├── buffer_memory.py       # Simple sliding window
│   │   │   ├── short_term.py          # ConversationMemory with rich API
│   │   │   ├── long_term.py           # Persistent storage
│   │   │   └── README.md
│   │   ├── tools/            # Agent tools
│   │   │   ├── example_tools.py
│   │   │   ├── registry.py            # Central tool registry
│   │   │   └── README.md
│   │   ├── prompts/          # Versioned prompt templates
│   │   │   ├── base_prompt_v1.0.txt
│   │   │   └── README.md
│   │   └── guardrails/       # Validation and safety
│   │       ├── input_guard.py         # Input validation
│   │       ├── output_guard.py        # Output validation
│   │       └── README.md
│   ├── utils/                # Shared utilities
│   │   └── logger.py
│   ├── assets/               # Static assets
│   ├── app.py               # Main app
│   ├── config.py            # Global configuration
│   └── main.py
├── tests/                   # Automated tests
│   └── test_agent.py
├── data/
│   ├── raw/                 # Raw data
│   └── processed/           # Processed data
├── docs/
│   ├── architecture.md      # Architecture detailing
│   ├── contributing.md      # Contribution guide
│   ├── decisions.md         # ADRs (Architecture Decision Records) and other decisions (business, etc.)
│   └── scope.md             # What is included and what is not included
├── logs/                    # Execution logs
├── playground/              # Prototyping and tests
│   └── test_chain.py
├── .env.example             # Environment variable template
├── requirements.txt         # Python dependencies
└── README.md
```

## ⚡ Quick Start (5 Minutes)

### Prerequisites

- Python 3.10+
- Anthropic Claude account - or other provider
- Your Claude API key - or other provider

### 1. Environment Setup

```bash
# Clone repository
git clone <repo>
cd genai-mvp-template

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy the environment template
cp .env.example .env

# Edit .env and add your key
ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Your First MVP (Choose one)

#### Option A: Simple Chain ⭐ (Recommended)

```python
from anthropic import Anthropic
from src.core.chains.base_chain import run_chain

client = Anthropic()
response = run_chain(
    user_input="What is the capital of Brazil?",
    model_client=client,
    variables={"domain": "geography"}
)
print(response)
```

**Save as `my_mvp.py` and run:**
```bash
python my_mvp.py
```

#### Option B: Agent with Tools

```python
from anthropic import Anthropic
from src.core.agents.base_agent import BaseAgent

client = Anthropic()
agent = BaseAgent(model_client=client, max_iterations=10)
response = agent.run("What is today's date? Search for information about AI")
print(response)
```

#### Option C: Interactive Examples

```bash
python QUICK_START.py
```

Choose an option (1-5) to see 5 working usage patterns.

---

## 📚 Understand the Template

### Main Components

| Component | Purpose | Complexity |
|-----------|---------|------------|
| **Chain** | One LLM call with a structured prompt | ⭐ Simple |
| **Agent** | ReAct loop (reason, execute tools, repeat) | ⭐⭐⭐ Complex |
| **Memory** | Keep context between calls | ⭐ Simple |
| **Tools** | Functions the agent can call | ⭐⭐ Medium |
| **Prompts** | Instruction templates | ⭐ Simple |
| **Guardrails** | Validate input/output | ⭐ Simple |

### Folder Structure

```
src/core/
├── chains/         ← Use for simple MVPs (recommended)
├── agents/         ← Use when you need complex reasoning
├── tools/          ← Add your tools here
├── memory/         ← Conversation context
├── prompts/        ← Prompt templates
└── guardrails/     ← Validation and safety
```

---

## 🔨 Customize for Your Use Case

### Add a New Tool

```python
# 1. Implement in src/core/tools/example_tools.py
def fetch_product_price(product_name: str) -> dict:
    """Fetch the price for a product."""
    return {"product": product_name, "price": 99.90}

# 2. Register in src/core/tools/registry.py
TOOL_REGISTRY = {
    "fetch_product_price": fetch_product_price,
}

TOOL_DEFINITIONS = [
    {
        "name": "fetch_product_price",
        "description": "Fetches the price for a product",
        "input_schema": {
            "type": "object",
            "properties": {
                "product_name": {"type": "string"}
            },
            "required": ["product_name"]
        }
    },
]

# 3. Use with the agent
agent = BaseAgent(model_client=client)
response = agent.run("What is the price of the XYZ laptop?")
```

### Customize the Prompt

```python
# Edit src/core/prompts/base_prompt_v1.0.txt
response = run_chain(
    user_input="your question",
    model_client=client,
    variables={
        "domain": "your domain",
        "instruction_1": "Be concise",
        "instruction_2": "Use clear language",
        "output_format": "Plain text",
    }
)
```

### Add Custom Validation

```python
# src/core/guardrails/input_guard.py
def validate_input(text: str) -> str:
    if not text or len(text) > 4000:
        raise InputValidationError("Invalid input")

    # ADD YOUR VALIDATIONS:
    if "forbidden-word" in text.lower():
        raise InputValidationError("Content not allowed")

    return text.strip()
```

---

## 💡 Chain vs Agent?

### Use **Chain** if:
- ✅ The task is well defined
- ✅ You want a fast response
- ✅ It does not require reasoning / iteration
- ✅ You want lower cost

**Examples:** Classification, Translation, Summarization

### Use **Agent** if:
- ✅ The task is complex
- ✅ It needs multiple tools
- ✅ It needs to "think" about the next action
- ✅ The answer depends on multiple steps

**Examples:** Search, Analysis, Problem solving

---

## 🧪 Test Your MVP

### Local Test

```bash
# Run interactive examples
python QUICK_START.py

# Or run your own script
python my_mvp.py
```

### Streamlit UI

```bash
pip install streamlit
streamlit run src/app.py
```

### Automated Tests

```bash
pytest tests/
pytest tests/test_agent.py -v
```

---

## 🚨 Troubleshooting

### Problem: "Module not found"

```
ModuleNotFoundError: No module named 'src'
```

**Fix:**

```bash
# Make sure you are at the repository root
pwd  # or cd into genai-mvp-template

# Make sure the virtual environment is active
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Problem: "API Key invalid"

```
AuthenticationError: Invalid API key
```

**Fix:**
1. Confirm `.env` exists and contains the key
2. Confirm the key begins with `sk-ant-`
3. Verify it in https://console.anthropic.com

### Problem: "Rate limit exceeded"

```
RateLimitError: 429
```

**Fix:**
- Too many requests too quickly
- Add delays between calls
- Consider caching

---

## 🎓 Recommended Next Steps

### Day 1: Working MVP
- [ ] Run `QUICK_START.py`
- [ ] Understand Chain vs Agent
- [ ] Build your first chain script

### Day 2: Customized MVP
- [ ] Add your first tool
- [ ] Customize prompts
- [ ] Add validation

### Day 3: Production MVP
- [ ] Add logging
- [ ] Implement tests
- [ ] Deploy (Vercel, Railway, AWS)

---

## ✨ TL;DR

```bash
# 1. Setup (2 min)
git clone <repo>
cd genai-mvp-template
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API key

# 2. Run example (30 sec)
python QUICK_START.py

# 3. Create your MVP (2 min)
cat > my_mvp.py << 'EOF'
from anthropic import Anthropic
from src.core.chains.base_chain import run_chain

client = Anthropic()
response = run_chain(
    user_input="Your question here",
    model_client=client,
    variables={"domain": "your domain"}
)
print(response)
EOF

python my_mvp.py
```

**Ready! Your MVP is running.** 🎉

## Folder Structure - Detailed Guide

### `src/core/agents/` - Autonomous Agents
- **ReAct loop**: Reason → Choose Tool → Execute → Observe → Repeat
- Base class with multiple agent strategies
- [Full docs →](src/core/agents/README.md)

### `src/core/chains/` - Linear Pipelines
- Deterministic workflows without autonomous loops
- Ideal for well-defined tasks
- [Full docs →](src/core/chains/README.md)

### `src/core/memory/` - Memory System
- **ConversationMemory**: Recent context (last 20 messages)
- **LongTermMemory**: Persistent history and learnings
- [Full docs →](src/core/memory/README.md)

### `src/core/tools/` - Tools
- Central registry of available tools
- Automatic agent integration
- [Full docs →](src/core/tools/README.md)

### `src/core/prompts/` - Prompt Templates
- Manual prompt versioning
- Convention: `{name}_v{major}.{minor}.txt`
- [Full docs →](src/core/prompts/README.md)

### `src/core/guardrails/` - Safety Layer
- User input validation
- Agent output validation
- Prompt injection protection
- [Full docs →](src/core/guardrails/README.md)

## Development Flow

```
USER INPUT
    ↓
INPUT_GUARD (validate input)
    ↓
AGENT/CHAIN (processing)
    ├── Uses MEMORY (context)
    ├── Uses TOOLS (actions)
    └── Uses PROMPTS (instructions)
    ↓
OUTPUT_GUARD (validation)
    ↓
USER RESPONSE
```

## Tests

```bash
pytest tests/
pytest tests/test_agent.py -v
```

## Documentation

- **[src/core/chains/README.md](src/core/chains/README.md)** - Chains (linear pipelines)
- **[src/core/agents/README.md](src/core/agents/README.md)** - Agents (ReAct loop)
- **[src/core/tools/README.md](src/core/tools/README.md)** - Tools
- **[src/core/memory/README.md](src/core/memory/README.md)** - Memory
- **[src/core/guardrails/README.md](src/core/guardrails/README.md)** - Guardrails
- **[src/core/prompts/README.md](src/core/prompts/README.md)** - Prompts

### Architecture and Decisions

- **[docs/architecture.md](docs/architecture.md)** - Architecture overview
- **[docs/contributing.md](docs/contributing.md)** - Contribution guide
- **[docs/decisions.md](docs/decisions.md)** - ADRs (Architecture Decision Records) and other decisions (business, etc.)
- **[docs/scope.md](docs/scope.md)** - Project scope
- **[docs/technical-documentation.md](docs/technical-documentation.md)** - Technical reference
- **[src/core/prompts/README.md](src/core/prompts/README.md)** - Prompt strategy

## Next Steps

1. ✅ Configure the environment and install dependencies
2. ✅ Explore examples in `playground/`
3. ✅ Read `docs/architecture.md`
4. ✅ Build your first agent or chain
5. ✅ Add custom guardrails for your use case
6. ✅ Store and retrieve knowledge with LongTermMemory

```bash
# Install streamlit
pip install streamlit

# Run UI
streamlit run src/app.py
```

### Automated Tests

```bash
# Run all tests
pytest tests/

# Run a specific test
pytest tests/test_agent.py -v
```

---

## 🚨 Troubleshooting

### Problem: "Module not found"
```
ModuleNotFoundError: No module named 'src'
```

**Fix:**
```bash
# Make sure you are at the project root
pwd  # or cd into genai-mvp-template

# Make sure the virtual environment is active
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Problem: "API key invalid"
```
AuthenticationError: Invalid API key
```

**Fix:**
1. Confirm `.env` exists and contains the key
2. Confirm the key begins with `sk-ant-`
3. Verify the key in https://console.anthropic.com

### Problem: "Rate limit exceeded"
```
RateLimitError: 429
```

**Fix:**
- Too many requests too quickly
- Add delays between calls
- Consider caching

---

## 🎓 Recommended Next Steps

### Day 1: Working MVP
- [ ] Run `QUICK_START.py`
- [ ] Understand Chain vs Agent
- [ ] Build your first chain script

### Day 2: Customized MVP
- [ ] Add your first tool
- [ ] Customize prompts
- [ ] Add validation

### Day 3: Production MVP
- [ ] Add logging
- [ ] Implement tests
- [ ] Deploy (Vercel, Railway, AWS)

---

## ✨ TL;DR (Too Long; Didn’t Read)

```bash
# 1. Setup (2 min)
git clone <repo>
cd genai-mvp-template
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API key

# 2. Run example (30 sec)
python QUICK_START.py

# 3. Create your MVP (2 min)
cat > my_mvp.py << 'EOF'
from anthropic import Anthropic
from src.core.chains.base_chain import run_chain

client = Anthropic()
response = run_chain(
    user_input="Your question here",
    model_client=client,
    variables={"domain": "your domain"}
)
print(response)
EOF

python my_mvp.py
```

**Ready! Your MVP is running.** 🎉

## Folder Structure - Detailed Guide

### `src/core/agents/` - Autonomous Agents
- **ReAct loop**: Reason → Choose Tool → Execute → Observe → Repeat
- Base class with support for multiple agent strategies
- [Full docs →](src/core/agents/README.md)

### `src/core/chains/` - Linear Pipelines
- Deterministic workflows without autonomous loops
- Ideal for well-defined tasks
- [Full docs →](src/core/chains/README.md)

### `src/core/memory/` - Memory System
- **ConversationMemory**: Recent context (last 20 messages)
- **LongTermMemory**: Persistent history and learnings
- [Full docs →](src/core/memory/README.md)

### `src/core/tools/` - Tools
- Central registry of available tools
- Automatic agent integration
- [Full docs →](src/core/tools/README.md)

### `src/core/prompts/` - Prompt Templates
- Manual prompt versioning
- Convention: `{name}_v{major}.{minor}.txt`
- [Full docs →](src/core/prompts/README.md)

### `src/core/guardrails/` - Safety Layer
- User input validation
- Agent output validation
- Prompt injection protection
- [Full docs →](src/core/guardrails/README.md)

## Development Flow

```
USER INPUT
    ↓
INPUT_GUARD (input validation)
    ↓
AGENT/CHAIN (processing)
    ├── Uses MEMORY (context)
    ├── Uses TOOLS (actions)
    └── Uses PROMPTS (instructions)
    ↓
OUTPUT_GUARD (validation)
    ↓
USER RESPONSE
```

## Tests

```bash
# Run all tests
pytest tests/

# Run a specific test
pytest tests/test_agent.py -v
```

## 📖 Detailed Documentation

For more details on each component, see:

- **[src/core/chains/README.md](src/core/chains/README.md)** - Chains (linear pipelines)
- **[src/core/agents/README.md](src/core/agents/README.md)** - Agents (ReAct loop)
- **[src/core/tools/README.md](src/core/tools/README.md)** - Tools
- **[src/core/memory/README.md](src/core/memory/README.md)** - Memory
- **[src/core/guardrails/README.md](src/core/guardrails/README.md)** - Guardrails
- **[src/core/prompts/README.md](src/core/prompts/README.md)** - Prompts

### Architecture and Decisions

- **[docs/architecture.md](docs/architecture.md)** - Decisions and patterns
- **[docs/contributing.md](docs/contributing.md)** - Contribution guide
- **[docs/decisions.md](docs/decisions.md)** - ADRs (Architecture Decision Records) and other decisions (business, etc.)
- **[docs/scope.md](docs/scope.md)** - Project scope
- **[docs/technical-documentation.md](docs/technical-documentation.md)** - Technical reference
- **[src/core/prompts/README.md](src/core/prompts/README.md)** - Prompt strategy

## Next Steps

1. ✅ Configure the environment and install dependencies
2. ✅ Explore examples in `playground/`
3. ✅ Read [architecture.md](docs/architecture.md)
4. ✅ Build your first agent or chain
5. ✅ Add custom guardrails for your use case
6. ✅ Store and retrieve knowledge with LongTermMemory
