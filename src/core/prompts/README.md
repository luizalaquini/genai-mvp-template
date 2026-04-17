# Prompts - Versioned Templates

Centralized library of prompts for agents and chains, with manual versioning and quality control.

## Philosophy

- ✅ Prompts in **files** (not hardcoded)
- ✅ Manual versioning for traceability
- ✅ Templates with placeholders for reuse
- ✅ Different versions for A/B testing
- ✅ Documentation for each version

## Naming Convention

```
{descriptive_name}_v{major}.{minor}.txt
```

**Examples:**
- `base_prompt_v1.0.txt` - Initial version
- `base_prompt_v1.1.txt` - Minor adjustment
- `base_prompt_v2.0.txt` - Significant change
- `summarize_v1.0.txt` - New prompt
- `classify_sentiment_v1.0.txt` - Another prompt

**When to bump versions:**
- `major++`: Change in approach / core instructions
- `minor++`: Wording or clarity improvement

## Prompt Structure

```
# Prompt: {name}
# Version: {major}.{minor}
# Description: What this prompt does

## System
[Instructions for model behavior]

## Instructions
[Specific steps]

## Response Format
[How to format the output]

## Examples (optional)
[Input/output examples]

## Variables
- {variable_1}: Description
- {variable_2}: Description
```

## Full Example

```txt
# Prompt: summarize
# Version: 1.0
# Description: Summarizes long texts while keeping the main points

## System
You are an expert in synthesis and summarization.
Your goal is to extract the most important information concisely.
Always respond in {language}.

## Instructions
1. Identify the 3-5 main points of the text
2. Remove redundancies and secondary details
3. Keep the output clear and cohesive
4. Use direct, professional language

## Response Format
Use bullet points, maximum {max_words} words.

## Examples
INPUT: "Artificial intelligence is a field of computer science that aims..."
OUTPUT:
• AI is a field of computer science
• It aims to simulate human intelligence
• Practical applications across multiple sectors

## Variables
- {language}: Response language (default: English)
- {max_words}: Word limit (default: 150)
- {tone}: Tone (formal, casual, technical)
```

## Using Prompts

### With Chains

```python
from src.core.chains.base_chain import run_chain
from anthropic import Anthropic

client = Anthropic()

# Loads base_prompt_v1.0.txt automatically
response = run_chain(
    user_input="Your text here",
    model_client=client,
    variables={
        "domain": "data science",
        "instruction_1": "Be concise",
        "instruction_2": "Use examples",
        "output_format": "JSON"
    }
)
```

### With Agents

```python
from src.core.agents.base_agent import BaseAgent

class CustomAgent(BaseAgent):
    def _system_prompt(self) -> str:
        from pathlib import Path
        prompt_path = Path(__file__).parent / "prompts" / "base_prompt_v1.0.txt"
        template = prompt_path.read_text()
        
        return template.format(
            domain="technical support",
            instruction_1="Use clear language",
            instruction_2="Provide practical solutions"
        )
```

## Prompt Management

### Creating a New Prompt

1. Pick a descriptive name: `analyze_sentiment_v1.0.txt`
2. Structure it with the standard sections
3. Document the variables used
4. Test with varied cases
5. Commit it to version control

```bash
# Structure
src/core/prompts/
├── base_prompt_v1.0.txt
├── base_prompt_v1.1.txt
├── base_prompt_v2.0.txt
├── summarize_v1.0.txt
├── classify_sentiment_v1.0.txt
└── README.md
```

### Prompt A/B Testing

```python
# Test different versions
def test_prompt_versions():
    from pathlib import Path
    
    versions = [
        ("base_prompt_v1.0.txt", "Original version"),
        ("base_prompt_v1.1.txt", "With examples"),
        ("base_prompt_v2.0.txt", "New template"),
    ]
    
    for version, desc in versions:
        prompt_path = Path(__file__).parent / "prompts" / version
        template = prompt_path.read_text()
        
        result = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=template.format(**test_vars),
            messages=[{"role": "user", "content": test_input}]
        )
        
        print(f"{desc}: {result.content[0].text[:100]}...")
```

## Prompt Patterns

### Pattern 1: Role-Playing

```txt
# Prompt: expert_analyst
# Version: 1.0

## System
You are a specialist analyst in {domain}.
With {years_of_experience} years of experience in the field.
You are known for clear explanations and deep insights.

## Instructions
1. Analyze the following text/data
2. Identify main patterns
3. Suggest recommended actions

## Format
Structure the answer as: Analysis | Patterns | Recommendations
```

### Pattern 2: Chain-of-Thought

```txt
# Prompt: reasoning
# Version: 1.0

## System
You are a logical, structured thinker.
Always show your reasoning step by step.

## Instructions
1. Present the problem
2. Break it into sub-problems
3. Solve each one
4. Combine them into a final solution

## Format
Use this template:
PROBLEM: [...]
SUB-PROBLEMS: [...]
SOLUTIONS: [...]
FINAL ANSWER: [...]
```

### Pattern 3: Few-Shot Learning

```txt
# Prompt: classify_entities
# Version: 1.0

## System
You classify entities into categories.

## Examples
INPUT: "João lives in São Paulo"
CLASSIFY: João (Person), São Paulo (Location)

INPUT: "Apple launched a new iPhone"
CLASSIFY: Apple (Company), iPhone (Product)

## Task
Classify the entities in the following text:
{user_text}

## Format
ENTITY: [entity] | CATEGORY: [category]
```

### Pattern 4: Temperature Variants

```txt
# Prompt: creative_writing
# Version: 1.0
# NOTE: Use temperature=0.8+ for better results

## System
You are a creative and imaginative writer.
Write in an engaging, original style.

[remaining prompt]
```

## Best Practices

✅ **Do:**
- Use clear versioning (semver)
- Document changes between versions
- Test with multiple inputs
- Use well-named variables `{var_name}`
- Include examples in prompts
- Add explanatory comments
- Keep history in Git

❌ **Avoid:**
- Prompts that are too long (>2000 chars)
- Hardcoding values
- No versioning
- Changes without documentation
- Confusing variable names
- No usage examples

## Prompt Optimization

### 1. Test Variations

```python
def benchmark_prompt(template, test_cases):
    results = []
    for input_text in test_cases:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=512,
            system=template,
            messages=[{"role": "user", "content": input_text}]
        )
        results.append({
            "input": input_text,
            "output": response.content[0].text
        })
    return results
```

### 2. Quality Metrics

```python
def evaluate_output(output, criteria):
    """Evaluate output quality"""
    score = 0
    
    # Completeness
    if len(output) > 50:
        score += 1
    
    # Relevance
    if any(word in output for word in ["important", "significant"]):
        score += 1
    
    # Clarity
    if output.count("?") < output.count("."):
        score += 1
    
    return score / 3  # 0-1
```

### 3. Data-Driven Iteration

```python
# Improvement history
PROMPT_VERSIONS = {
    "1.0": "Baseline",
    "1.1": "Added examples (+10% quality)",
    "1.2": "Improved output instruction (+5% quality)",
    "2.0": "New role-playing template (+20% quality)"
}
```

## CI/CD Integration

```yaml
# .github/workflows/test-prompts.yml
name: Test Prompts
on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Test Prompt Quality
        run: python tests/test_prompts.py
```

## Version Migration

When you want to change the default version:

```python
# Old version
from src.core.chains.base_chain import load_prompt
template = load_prompt("base_prompt")  # Loads v1.0 automatically

# New version
template_v2 = load_prompt("base_prompt_v2")  # Loads v2.0 explicitly
```

## Change Documentation

Keep a CHANGELOG:

```markdown
# Changelog - Prompts

## [2.0.0] - 2024-04-16
### Changed
- New prompt template with stronger role-playing
- Improved output instruction
- Added edge case examples

### Performance
- +20% quality in internal tests
- -5% latency (more concise prompt)

## [1.1.0] - 2024-04-10
### Added
- Expected output examples
- Customizable `tone` variable

### Fixed
- Fixed JSON formatting instruction
```

## Troubleshooting

| Problem | Cause | Fix |
|----------|-------|---------|
| Inconsistent output | Vague prompt | Add examples |
| Model ignores instructions | Prompt too long | Simplify or prioritize |
| Wrong output format | Unclear instructions | Add explicit format |
| Poor performance | Generic prompt | Add context/role |

## Next Steps

- [ ] Build a library of tested prompts
- [ ] Implement prompt versioning in the database
- [ ] Set up automatic A/B testing
- [ ] Build a prompt quality dashboard
- [ ] Document best practices by domain
- [ ] Integrate with observability/monitoring
