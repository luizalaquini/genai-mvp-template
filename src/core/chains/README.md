# Chains - Linear Workflows

Deterministic pipelines without an autonomous loop. Use for well-defined workflows where the flow is predictable.

## When to Use Chains vs Agents

| Aspect | Chains | Agents |
|--------|--------|--------|
| **Flow** | Linear and predictable | Autonomous and iterative |
| **Complexity** | Simple | Complex |
| **Tools** | Not supported | Supported |
| **Latency** | Low (1 request) | High (multiple requests) |
| **Cost** | Low | High |
| **Use Case** | Simple tasks | Tasks that require reasoning |

## Chain Architecture

```
Input
  ↓
Load Prompt Template
  ↓
Format with Variables
  ↓
Call LLM (one time)
  ↓
Output
```

## BaseChain - Usage Example

```python
from anthropic import Anthropic
from src.core.chains.base_chain import run_chain

client = Anthropic()

# Simple chain
response = run_chain(
    user_input="What is the capital of Brazil?",
    model_client=client,
    variables={"tone": "formal"}
)
print(response)
```

## Main Components

### run_chain()

**Parameters:**
- `user_input`: User message
- `model_client`: AI client (e.g. Anthropic)
- `variables`: Dictionary to replace placeholders in the prompt

**Returns:**
- String with the LLM response

**Example:**

```python
response = run_chain(
    user_input="Summarize this text into 3 points",
    model_client=client,
    variables={
        "tone": "technical",
        "max_words": 100,
        "language": "english"
    }
)
```

### load_prompt()

Loads a prompt template from `src/core/prompts/`

**Convention:**
- File name: `{descriptive_name}_v{major}.{minor}.txt`
- Example: `summarize_v1.0.txt`, `translate_v2.1.txt`

## Common Patterns

### Pattern 1: Classification

```python
def classify_sentiment(text: str, model_client) -> str:
    return run_chain(
        user_input=text,
        model_client=model_client,
        variables={"task": "Classify sentiment"}
    )
```

### Pattern 2: Translation

```python
def translate(text: str, target_lang: str, model_client) -> str:
    return run_chain(
        user_input=text,
        model_client=model_client,
        variables={"target_language": target_lang}
    )
```

### Pattern 3: Data Extraction

```python
def extract_entities(text: str, model_client) -> dict:
    response = run_chain(
        user_input=text,
        model_client=model_client,
        variables={"format": "JSON"}
    )
    # Parse JSON response
    import json
    return json.loads(response)
```

### Pattern 4: Chain Composition

```python
def complex_workflow(text: str, model_client):
    # Chain 1: Summarize
    summary = run_chain(
        user_input=text,
        model_client=model_client,
        variables={"task": "summarize"}
    )
    
    # Chain 2: Classify
    classification = run_chain(
        user_input=summary,
        model_client=model_client,
        variables={"task": "classify"}
    )
    
    # Chain 3: Translate
    translation = run_chain(
        user_input=classification,
        model_client=model_client,
        variables={"target_language": "spanish"}
    )
    
    return {
        "summary": summary,
        "classification": classification,
        "translation": translation
    }
```

## Prompt Management

### Prompt Structure for Chains

```
src/core/prompts/
├── summarize_v1.0.txt
├── classify_v1.0.txt
├── translate_v1.0.txt
└── extract_v2.1.txt
```

### Prompt Example with Placeholders

```txt
# summarize_v1.0.txt

You are a summary expert. Your job is to create concise, informative summaries.

Take the following text and create an English summary with a maximum of {max_words} words.
Keep the main points and ignore secondary details.

Output format: {output_format}
Target audience: {audience}

Text to summarize:
{text}
```

**Usage:**

```python
run_chain(
    user_input="Your text here...",
    model_client=client,
    variables={
        "max_words": 150,
        "output_format": "bullet points",
        "audience": "executives"
    }
)
```

## Best Practices

✅ **Do:**
- Use chains for well-defined tasks
- Keep prompts in versioned files
- Validate input and output with guardrails
- Use variables to customize behavior
- Test different prompt versions (v1.0, v1.1, v2.0)

❌ **Avoid:**
- Chains with too much logic (use agents instead)
- Hardcoding prompts in code
- No input/output validation
- Prompts that are too long (use summarization)
- Modifying prompts at runtime without versioning

## Performance

### Comparison with Agents

**Chain:**
- 1 request to the LLM
- Latency: ~500ms
- Cost: Low

**Agent (with 3 iterations):**
- 3+ requests to the LLM
- Latency: ~2000ms
- Cost: 3x higher

**Recommendation:** Use chains when possible, agents when reasoning is required.

## Integration with Other Components

```
Chain Input
    ↓
Input Guard (validate)
    ↓
Load Prompt (templates)
    ↓
Format Variables
    ↓
Call LLM
    ↓
Output Guard (validate)
    ↓
Chain Output
```

## Troubleshooting

| Problem | Cause | Fix |
|----------|-------|---------|
| Variable not substituted | Incorrect placeholder | Use `{name}` in the prompt |
| Prompt not found | File does not exist | Check name in `src/core/prompts/` |
| Invalid output | Unexpected format | Add output format instructions to the prompt |
| High latency | Slow LLM | Use a faster model or cache |

## Next Steps

- [ ] Create prompts for specific use cases
- [ ] Version existing prompts
- [ ] Implement prompt caching
- [ ] Add detailed logging
- [ ] Optimize cost via prompt engineering

## Creating Your Own Chains

### Option 1: Use run_chain() Directly

```python
from anthropic import Anthropic
from src.core.chains.base_chain import run_chain

client = Anthropic()

# Simple and direct
result = run_chain(
    user_input="Translate to Spanish: Hello world",
    model_client=client,
    variables={"target_language": "spanish"}
)
```

### Option 2: Create a Custom Chain

```python
from src.core.chains.base_chain import load_prompt
from src.core.guardrails.input_guard import validate_input
from src.core.guardrails.output_guard import validate_output

class SummarizationChain:
    """Chain to summarize texts."""
    
    def __init__(self, model_client):
        self.client = model_client
        self.prompt = load_prompt("summarize")
    
    def run(self, text: str, max_words: int = 100) -> str:
        # 1. Validate input
        text = validate_input(text)
        
        # 2. Prepare prompt
        prompt = self.prompt.format(max_words=max_words)
        
        # 3. Call LLM (one time)
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=512,
            system=prompt,
            messages=[{"role": "user", "content": text}]
        )
        
        # 4. Validate and return output
        result = response.content[0].text
        validate_output(result)
        return result

# Usage
from anthropic import Anthropic
client = Anthropic()
chain = SummarizationChain(client)
summary = chain.run("Your long text here...", max_words=50)
```

## Common Patterns

### Pattern 1: Classification

```python
def classify_sentiment(text: str, model_client) -> str:
    return run_chain(
        user_input=text,
        model_client=model_client,
        variables={"task": "Classify sentiment"}
    )
```

### Pattern 2: Translation

```python
def translate(text: str, target_lang: str, model_client) -> str:
    return run_chain(
        user_input=text,
        model_client=model_client,
        variables={"target_language": target_lang}
    )
```

### Pattern 3: Data Extraction

```python
def extract_entities(text: str, model_client) -> dict:
    response = run_chain(
        user_input=text,
        model_client=model_client,
        variables={"format": "JSON"}
    )
    # Parse JSON response
    import json
    return json.loads(response)
```

### Pattern 4: Chain Composition

```python
def complex_workflow(text: str, model_client):
    # Chain 1: Summarize
    summary = run_chain(
        user_input=text,
        model_client=model_client,
        variables={"task": "summarize"}
    )
    
    # Chain 2: Classify
    classification = run_chain(
        user_input=summary,
        model_client=model_client,
        variables={"task": "classify"}
    )
    
    # Chain 3: Translate
    translation = run_chain(
        user_input=classification,
        model_client=model_client,
        variables={"target_language": "spanish"}
    )
    
    return {
        "summary": summary,
        "classification": classification,
        "translation": translation
    }
```

## Prompt Management

### Prompt Structure for Chains

```
src/core/prompts/
├── summarize_v1.0.txt
├── classify_v1.0.txt
├── translate_v1.0.txt
└── extract_v2.1.txt
```

### Prompt Example with Placeholders

```txt
# summarize_v1.0.txt

You are a summary specialist. Your job is to create concise, informative summaries.

Take the following text and create an English summary with a maximum of {max_words} words.
Keep the main points and ignore secondary details.

Output format: {output_format}
Target audience: {audience}

Text to summarize:
{text}
```

**Usage:**

```python
run_chain(
    user_input="Your text here...",
    model_client=client,
    variables={
        "max_words": 150,
        "output_format": "bullet points",
        "audience": "executives"
    }
)
```

## Best Practices

✅ **Do:**
- Use chains for well-defined tasks
- Keep prompts in versioned files
- Validate input and output with guardrails
- Use variables to customize behavior
- Test different prompt versions (v1.0, v1.1, v2.0)

❌ **Avoid:**
- Chains with too much logic (use agents)
- Hardcoding prompts in code
- Missing input/output validation
- Prompts that are too long (use summarization)
- Modifying prompts at runtime without versioning

## Performance

### Comparison with Agents

**Chain:**
- 1 request to the LLM
- Latency: ~500ms
- Cost: Low

**Agent (with 3 iterations):**
- 3+ requests to the LLM
- Latency: ~2000ms
- Cost: 3x higher

**Recommendation:** Use chains when possible, agents when necessary for reasoning.

## Integration with Other Components

```
Chain Input
    ↓
Input Guard (validate)
    ↓
Load Prompt (templates)
    ↓
Format Variables
    ↓
Call LLM
    ↓
Output Guard (validate)
    ↓
Chain Output
```

## Troubleshooting

| Problem | Cause | Fix |
|----------|-------|---------|
| Variable not substituted | Incorrect placeholder | Use `{name}` in the prompt |
| Prompt not found | File does not exist | Check name in `src/core/prompts/` |
| Invalid output | Unexpected format | Add output format instructions to the prompt |
| High latency | Slow LLM | Use a faster model or cache |

## Next Steps

- [ ] Create prompts for specific use cases
- [ ] Version existing prompts
- [ ] Implement prompt caching
- [ ] Add detailed logging
- [ ] Optimize cost via prompt engineering
