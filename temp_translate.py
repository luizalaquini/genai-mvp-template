# coding: utf-8
from pathlib import Path

files = {
    "README.md": """# GenAI Agent Template

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
│   │   │   ├── base_prompt.txt
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
├── tests/
│   └── test_agent.py
├── data/
│   ├── raw/                 # Raw data
│   └── processed/           # Processed data
├── docs/
│   ├── architecture.md      # Architecture decisions
│   ├── contributing.md      # Contribution guide
│   ├── decisions.md         # ADRs (Architecture Decision Records)
│   ├── technical-documentation.md
│   ├── prompts_strategy.md
│   ├── scope.md
│   └── README.md
├── logs/                    # Execution logs
├── playground/              # Prototyping and tests
│   └── test_chain.py
├── .env.example             # Environment variable template
├── requirements.txt         # Python dependencies
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.10+
- Anthropic Claude account
- Your Claude API key

### Install

```bash
python -m venv venv
venv\\Scripts\\activate  # Windows
pip install -r requirements.txt
```

### Run example

```bash
python QUICK_START.py
```

### Run Streamlit UI

```bash
streamlit run src/app.py
```

## Files

- `src/app.py` - Streamlit UI
- `src/core/agents/` - Agent implementations
- `src/core/chains/` - Chain implementations
- `src/core/tools/` - Tools for agents
- `src/core/memory/` - Memory storage
- `src/core/guardrails/` - Input/output validation
""",
    "src/app.py": """\"\"\"Streamlit UI for the MVP.\"\"\"
import streamlit as st
from anthropic import Anthropic
from src.core.chains.base_chain import run_chain

st.set_page_config(page_title=\"GenAI MVP\", page_icon=\"🤖\")
st.title(\"GenAI MVP Template\")

client = Anthropic()
user_input = st.text_input(\"Enter your message:\")

if user_input:
    with st.spinner(\"Processing...\"):
        response = run_chain(
            user_input=user_input,
            model_client=client,
            variables={\"domain\": \"general assistance\"}
        )
    st.write(response)
""",
    "tests/test_agent.py": """\"\"\"Base agent tests.\"\"\"
from unittest.mock import MagicMock
from src.core.agents.base_agent import BaseAgent
from src.core.guardrails.input_guard import validate_input, InputValidationError
import pytest


def test_validate_input_ok():
    assert validate_input(\"Hello, how are you?\") == \"Hello, how are you?\"


def test_validate_input_empty():
    with pytest.raises(InputValidationError):
        validate_input(\"\")


def test_validate_input_too_long():
    with pytest.raises(InputValidationError):
        validate_input(\"x\" * 5000)


def test_agent_uses_memory():
    mock_client = MagicMock()
    agent = BaseAgent(model_client=mock_client, max_iterations=1)
    assert len(agent.memory) == 0
""",
    "docs/contributing.md": """# Contributing

## Add a new tool

1. Implement the function in `src/core/tools/`
2. Register it in `src/core/tools/registry.py`
3. Add tests in `tests/` covering your feature

## Create a new agent

1. Create `src/core/agents/my_agent.py` and adapt BaseAgent
2. Add the endpoint or integration in `src/main.py`

## PR Workflow

1. git checkout -b feat/my-feature
2. pytest tests/
3. Open a PR with your change description
"""
}

for path, content in files.items():
    Path(path).write_text(content, encoding='utf-8')
    print(f'Wrote {path}')
# coding: utf-8
from pathlib import Path

files = {
    "README.md": '''# GenAI Agent Template

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
│   │   │   ├── base_prompt.txt
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
├── tests/
│   └── test_agent.py
├── data/
│   ├── raw/                 # Raw data
│   └── processed/           # Processed data
├── docs/
│   ├── architecture.md      # Architecture decisions
│   ├── contributing.md      # Contribution guide
│   ├── decisions.md         # ADRs (Architecture Decision Records)
│   ├── technical-documentation.md
│   ├── prompts_strategy.md
│   ├── scope.md
│   └── README.md
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
- Anthropic Claude account
- Your Claude API key

### 1. Environment Setup

```bash
# Clone the repository
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
# Edit src/core/prompts/base_prompt.txt
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
OUTPUT_GUARD (validate output)
    ↓
USER RESPONSE
```

## Tests

```bash
pytest tests/
pytest tests/test_agent.py -v
```

## Detailed Documentation

- **[src/core/chains/README.md](src/core/chains/README.md)** - Chains (linear pipelines)
- **[src/core/agents/README.md](src/core/agents/README.md)** - Agents (ReAct loop)
- **[src/core/tools/README.md](src/core/tools/README.md)** - Tools
- **[src/core/memory/README.md](src/core/memory/README.md)** - Memory
- **[src/core/guardrails/README.md](src/core/guardrails/README.md)** - Guardrails
- **[src/core/prompts/README.md](src/core/prompts/README.md)** - Prompts

### Architecture and Decisions

- **[docs/architecture.md](docs/architecture.md)** - Architecture overview
- **[docs/contributing.md](docs/contributing.md)** - Contribution guide
- **[docs/decisions.md](docs/decisions.md)** - Architecture decision records
- **[docs/scope.md](docs/scope.md)** - Project scope
- **[docs/technical-documentation.md](docs/technical-documentation.md)** - Technical reference
- **[docs/prompts_strategy.md](docs/prompts_strategy.md)** - Prompt strategy

## Next Steps

1. ✅ Set up your environment and install dependencies
2. ✅ Explore `playground/` examples
3. ✅ Read `docs/architecture.md`
4. ✅ Build your first agent or chain
5. ✅ Add your own tools in `src/core/tools/`
6. ✅ Add guardrails and tests
'''
}

for path, content in files.items():
    Path(path).write_text(content, encoding='utf-8')
    print(f'Wrote {path}')
from pathlib import Path

files = {
    "README.md": '''# GenAI Agent Template

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
│   │   │   ├── base_prompt.txt
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
├── tests/
│   └── test_agent.py
├── data/
│   ├── raw/                 # Raw data
│   └── processed/           # Processed data
├── docs/
│   ├── architecture.md      # Architecture decisions
│   ├── contributing.md      # Contribution guide
│   ├── decisions.md         # ADRs (Architecture Decision Records)
│   ├── technical-documentation.md
│   ├── prompts_strategy.md
│   ├── scope.md
│   └── README.md
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
- Anthropic Claude account
- Your Claude API key

### 1. Environment Setup

```bash
# Clone the repository
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
# Edit src/core/prompts/base_prompt.txt
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
OUTPUT_GUARD (validate output)
    ↓
USER RESPONSE
```

## Tests

```bash
pytest tests/
pytest tests/test_agent.py -v
```

## Detailed Documentation

- **[src/core/chains/README.md](src/core/chains/README.md)** - Chains (linear pipelines)
- **[src/core/agents/README.md](src/core/agents/README.md)** - Agents (ReAct loop)
- **[src/core/tools/README.md](src/core/tools/README.md)** - Tools
- **[src/core/memory/README.md](src/core/memory/README.md)** - Memory
- **[src/core/guardrails/README.md](src/core/guardrails/README.md)** - Guardrails
- **[src/core/prompts/README.md](src/core/prompts/README.md)** - Prompts

### Architecture and Decisions

- **[docs/architecture.md](docs/architecture.md)** - Architecture overview
- **[docs/contributing.md](docs/contributing.md)** - Contribution guide
- **[docs/decisions.md](docs/decisions.md)** - Architecture decision records
- **[docs/scope.md](docs/scope.md)** - Project scope
- **[docs/technical-documentation.md](docs/technical-documentation.md)** - Technical reference
- **[docs/prompts_strategy.md](docs/prompts_strategy.md)** - Prompt strategy

## Next Steps

1. ✅ Set up your environment and install dependencies
2. ✅ Explore `playground/` examples
3. ✅ Read `docs/architecture.md`
4. ✅ Build your first agent or chain
5. ✅ Add your own tools in `src/core/tools/`
6. ✅ Add guardrails and tests
''',
    "QUICK_START.py": '''#!/usr/bin/env python3
"""
🚀 QUICK START - GenAI MVP in 5 minutes

This file demonstrates how to use the template with working examples.
It includes both chains (simple) and agents (with tools).

To run:
  1. Copy .env.example to .env
  2. Add your ANTHROPIC_API_KEY in .env
  3. Install: pip install -r requirements.txt
  4. Run: python QUICK_START.py
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv()

# Initialize client
client = Anthropic()


# ============================================================================
# EXAMPLE 1: SIMPLE CHAIN (recommended for initial MVP)
# ============================================================================
def example_1_simple_chain():
    """
    Chain = one LLM call with a structured prompt.
    ✅ Fast
    ✅ Cheap
    ✅ Predictable
    """
    print("\n" + "=" * 70)
    print("📝 EXAMPLE 1: SIMPLE CHAIN")
    print("=" * 70)

    from src.core.chains.base_chain import run_chain

    questions = [
        "What is the capital of Brazil?",
        "What is 10 + 5?",
        "Tell me an interesting fact about Python",
    ]

    for question in questions:
        print(f"\n❓ Question: {question}")
        response = run_chain(
            user_input=question,
            model_client=client,
            variables={
                "domain": "general assistance",
                "instruction_1": "Be brief and direct",
                "instruction_2": "Use clear language",
                "output_format": "Plain text",
            },
        )
        print(f"✅ Answer: {response[:200]}...")


# ============================================================================
# EXAMPLE 2: AGENT WITH TOOLS (for more complex reasoning)
# ============================================================================def example_2_agent_with_tools():
    """
    Agent = ReAct loop that reasons and executes tools.
    ✅ Can use tools
    ✅ Handles complex reasoning
    ❌ More expensive
    ❌ Slower
    """
    print("\n" + "=" * 70)
    print("🤖 EXAMPLE 2: AGENT WITH TOOLS")
    print("=" * 70)

    from src.core.agents.base_agent import BaseAgent

    agent = BaseAgent(model_client=client, max_iterations=5)

    tasks = [
        "What is today's date?",
        "Search for information about artificial intelligence",
    ]

    for task in tasks:
        print(f"\n🎯 Task: {task}")
        try:
            response = agent.run(task)
            print(f"✅ Result: {response[:200]}...")
        except Exception as e:
            print(f"⚠️ Error: {e}")


# ============================================================================
# EXAMPLE 3: USING MEMORY (conversation context)
# ============================================================================
def example_3_with_memory():
    """
    Memory = keep context across multiple calls.
    Useful for conversations where context matters.
    """
    print("\n" + "=" * 70)
    print("💾 EXAMPLE 3: WITH MEMORY (Conversations)")
    print("=" * 70)

    from src.core.memory.short_term import ConversationMemory
    from src.core.chains.base_chain import run_chain

    memory = ConversationMemory(max_messages=20)

    exchanges = [
        ("What is the best programming language?", "programming"),
        ("Which language is the fastest?", "programming"),
        ("Recommend something to learn now", "learning"),
    ]

    for user_msg, domain in exchanges:
        print(f"\n👤 User: {user_msg}")

        memory.add_user_message(user_msg)

        response = run_chain(
            user_input=user_msg,
            model_client=client,
            variables={"domain": domain},
        )

        memory.add_assistant_message(response[:100])
        print(f"🤖 Assistant: {response[:150]}...")

    print(f"\n📋 History ({len(memory.get_all())} messages):")
    for msg in memory.get_all():
        print(f"  - {msg['role']}: {msg['content'][:50]}...")


# ============================================================================
# EXAMPLE 4: GUARDRAILS (Safety)
# ============================================================================
def example_4_with_guardrails():
    """
    Guardrails = input and output validation.
    Protects against invalid inputs and bad outputs.
    """
    print("\n" + "=" * 70)
    print("🛡️  EXAMPLE 4: WITH GUARDRAILS (Safety)")
    print("=" * 70)

    from src.core.guardrails.input_guard import validate_input, InputValidationError

    test_inputs = [
        ("What is the capital of Brazil?", True),
        ("", False),
        ("x" * 5000, False),
    ]

    for input_text, should_pass in test_inputs:
        display_text = input_text[:50] + "..." if len(input_text) > 50 else input_text
        print(f"\n🔍 Validating: '{display_text}'")

        try:
            clean = validate_input(input_text)
            if should_pass:
                print("✅ PASSED: Valid input")
            else:
                print("❌ ERROR: This should have failed!")
        except InputValidationError as e:
            if not should_pass:
                print(f"✅ BLOCKED (expected): {e}")
            else:
                print(f"❌ ERROR: This should have passed! {e}")


# ============================================================================
# EXAMPLE 5: COMPLETE PIPELINE (Recommended for production)
# ============================================================================
def example_5_complete_pipeline():
    """
    Pipeline = Chain + Memory + Guardrails
    This builds a more robust MVP.
    """
    print("\n" + "=" * 70)
    print("🏗️  EXAMPLE 5: COMPLETE PIPELINE")
    print("=" * 70)

    from src.core.chains.base_chain import run_chain
    from src.core.memory.short_term import ConversationMemory
    from src.core.guardrails.input_guard import validate_input, InputValidationError
    from src.core.guardrails.output_guard import validate_output

    class SimpleAssistant:
        """Simple assistant with all layers."""

        def __init__(self):
            self.memory = ConversationMemory(max_messages=20)

        def chat(self, user_input: str) -> str:
            try:
                user_input = validate_input(user_input)
            except InputValidationError as e:
                return f"❌ Invalid input: {e}"

            self.memory.add_user_message(user_input)

            try:
                response = run_chain(
                    user_input=user_input,
                    model_client=client,
                    variables={"domain": "general assistance"},
                )
            except Exception as e:
                return f"❌ Processing error: {e}"

            response = validate_output(response)
            self.memory.add_assistant_message(response)
            return response

    assistant = SimpleAssistant()

    messages = [
        "Hello! How are you?",
        "Tell me something interesting",
        "Thank you!",
    ]

    for msg in messages:
        print(f"\n👤 User: {msg}")
        response = assistant.chat(msg)
        print(f"🤖 Assistant: {response[:150]}...")


# ============================================================================
# MAIN
# ============================================================================
if __name__ == "__main__":
    print('''
╔════════════════════════════════════════════════════════════════════════╗
║                   🚀 GenAI MVP Template - Quick Start                  ║
║                                                                        ║
║  This script demonstrates 5 usage patterns for the template:           ║
║  1. Simple Chain (⭐ start here)                                       ║
║  2. Agent with Tools                                                  ║
║  3. With Memory (conversations)                                       ║
║  4. With Guardrails (safety)                                          ║
║  5. Complete Pipeline (production)                                    ║
║                                                                        ║
║  Run with: python QUICK_START.py                                      ║
╚════════════════════════════════════════════════════════════════════════╝
    ''')

    print("\nWhich example would you like to run?")
    print("  1 - Simple Chain (recommended)")
    print("  2 - Agent with Tools")
    print("  3 - With Memory")
    print("  4 - With Guardrails")
    print("  5 - Complete Pipeline")
    print("  a - All")

    choice = input("\nChoose (1-5 or 'a'): ").strip().lower()

    examples = {
        "1": example_1_simple_chain,
        "2": example_2_agent_with_tools,
        "3": example_3_with_memory,
        "4": example_4_with_guardrails,
        "5": example_5_complete_pipeline,
    }

    if choice == "a":
        for example_fn in examples.values():
            example_fn()
    elif choice in examples:
        examples[choice]()
    else:
        print("❌ Invalid option!")

    print("\n" + "=" * 70)
    print("✅ Examples completed!")
    print("=" * 70)
    print("\n📚 Next steps:")
    print("  1. Read the main README")
    print("  2. Explore docs/ for complete documentation")
    print("  3. Customize for your use case")
    print("  4. Add your own tools in src/core/tools/")
''',
    "src/app.py": '''"""Streamlit UI for the MVP."""
import streamlit as st
from anthropic import Anthropic
from src.core.chains.base_chain import run_chain

st.set_page_config(page_title="GenAI MVP", page_icon="🤖")
st.title("🤖 GenAI MVP Template")

client = Anthropic()
user_input = st.text_input("Enter your message:")

if user_input:
    with st.spinner("Processing..."):
        response = run_chain(
            user_input=user_input,
            model_client=client,
            variables={"domain": "general assistance"}
        )
    st.write(response)
''',
    "tests/test_agent.py": '''"""Base agent tests."""
from unittest.mock import MagicMock
from src.core.agents.base_agent import BaseAgent
from src.core.guardrails.input_guard import validate_input, InputValidationError
import pytest


def test_validate_input_ok():
    assert validate_input("Hello, how are you?") == "Hello, how are you?"


def test_validate_input_empty():
    with pytest.raises(InputValidationError):
        validate_input("")


def test_validate_input_too_long():
    with pytest.raises(InputValidationError):
        validate_input("x" * 5000)


def test_agent_uses_memory():
    mock_client = MagicMock()
    agent = BaseAgent(model_client=mock_client, max_iterations=1)
    assert len(agent.memory) == 0
''',
    "docs/contributing.md": '''# Contributing

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
''',
}

for path, content in files.items():
    Path(path).write_text(content, encoding="utf-8")
    print(f"Wrote {path}")
