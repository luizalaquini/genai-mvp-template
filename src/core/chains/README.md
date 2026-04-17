# Chains - Fluxos Lineares

Pipelines determinísticos sem loop autônomo. Use para workflows bem definidos onde o fluxo é previsível.

## Quando Usar Chains vs Agents

| Aspecto | Chains | Agents |
|--------|--------|--------|
| **Fluxo** | Linear e previsível | Autônomo e iterativo |
| **Complexidade** | Simples | Complexa |
| **Ferramentas** | Não suportadas | Suportadas |
| **Latência** | Baixa (1 request) | Alta (múltiplos requests) |
| **Custo** | Baixo | Alto |
| **Caso de Uso** | Tarefas simples | Tarefas que precisam raciocinar |

## Arquitetura de uma Chain

```
Input
  ↓
Load Prompt Template
  ↓
Format com Variáveis
  ↓
Call LLM (uma única vez)
  ↓
Output
```

## BaseChain - Exemplo de Uso

```python
from anthropic import Anthropic
from src.core.chains.base_chain import run_chain

client = Anthropic()

# Chain simples
response = run_chain(
    user_input="Qual é a capital do Brasil?",
    model_client=client,
    variables={"tone": "formal"}
)
print(response)
```

## Componentes Principais

### run_chain()

**Parâmetros:**
- `user_input`: Mensagem do usuário
- `model_client`: Cliente de IA (ex: Anthropic)
- `variables`: Dicionário para substituir placeholders no prompt

**Retorno:**
- String com resposta do LLM

**Exemplo:**

```python
response = run_chain(
    user_input="Resuma este texto em 3 pontos",
    model_client=client,
    variables={
        "tone": "técnico",
        "max_words": 100,
        "language": "português"
    }
)
```

### load_prompt()

Carrega template de prompt de `src/core/prompts/`

**Convenção:**
- Nome do arquivo: `{nome_descritivo}_v{major}.{minor}.txt`
- Exemplo: `summarize_v1.0.txt`, `translate_v2.1.txt`

## Criando Suas Próprias Chains

### Opção 1: Usar run_chain() Diretamente

```python
from anthropic import Anthropic
from src.core.chains.base_chain import run_chain

client = Anthropic()

# Simples e direto
result = run_chain(
    user_input="Traduza para espanhol: Olá mundo",
    model_client=client,
    variables={"target_language": "espanhol"}
)
```

### Opção 2: Criar Chain Customizada

```python
from src.core.chains.base_chain import load_prompt
from src.core.guardrails.input_guard import validate_input
from src.core.guardrails.output_guard import validate_output

class SummarizationChain:
    """Chain para sumarizar textos."""
    
    def __init__(self, model_client):
        self.client = model_client
        self.prompt = load_prompt("summarize")
    
    def run(self, text: str, max_words: int = 100) -> str:
        # 1. Validar entrada
        text = validate_input(text)
        
        # 2. Preparar prompt
        prompt = self.prompt.format(max_words=max_words)
        
        # 3. Chamar LLM (uma única vez)
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=512,
            system=prompt,
            messages=[{"role": "user", "content": text}]
        )
        
        # 4. Validar e retornar saída
        result = response.content[0].text
        validate_output(result)
        return result

# Usar
from anthropic import Anthropic
client = Anthropic()
chain = SummarizationChain(client)
summary = chain.run("Seu texto longo aqui...", max_words=50)
```

## Padrões Comuns

### Pattern 1: Classificação

```python
def classify_sentiment(text: str, model_client) -> str:
    return run_chain(
        user_input=text,
        model_client=model_client,
        variables={"task": "Classificar sentimento"}
    )
```

### Pattern 2: Tradução

```python
def translate(text: str, target_lang: str, model_client) -> str:
    return run_chain(
        user_input=text,
        model_client=model_client,
        variables={"target_language": target_lang}
    )
```

### Pattern 3: Extração de Dados

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

### Pattern 4: Composição de Chains

```python
def complex_workflow(text: str, model_client):
    # Chain 1: Sumarizar
    summary = run_chain(
        user_input=text,
        model_client=model_client,
        variables={"task": "summarize"}
    )
    
    # Chain 2: Classificar
    classification = run_chain(
        user_input=summary,
        model_client=model_client,
        variables={"task": "classify"}
    )
    
    # Chain 3: Traduzir
    translation = run_chain(
        user_input=classification,
        model_client=model_client,
        variables={"target_language": "espanhol"}
    )
    
    return {
        "summary": summary,
        "classification": classification,
        "translation": translation
    }
```

## Gerenciamento de Prompts

### Estrutura de Prompts para Chains

```
src/core/prompts/
├── summarize_v1.0.txt
├── classify_v1.0.txt
├── translate_v1.0.txt
└── extract_v2.1.txt
```

### Exemplo de Prompt com Placeholders

```txt
# summarize_v1.0.txt

Você é um especialista em resumos. Seu trabalho é criar resumos concisos e informativos.

Tome o seguinte texto e crie um resumo em português com no máximo {max_words} palavras.
Mantenha os pontos principais e ignore detalhes secundários.

Formato de saída: {output_format}
Público alvo: {audience}

Texto a resumir:
{text}
```

**Uso:**

```python
run_chain(
    user_input="Seu texto aqui...",
    model_client=client,
    variables={
        "max_words": 150,
        "output_format": "bullet points",
        "audience": "executivos"
    }
)
```

## Boas Práticas

✅ **Faça:**
- Use chains para tarefas bem definidas
- Mantenha prompts em arquivos versionados
- Valide entrada e saída com guardrails
- Use variáveis para customizar comportamento
- Teste diferentes prompt versions (v1.0, v1.1, v2.0)

❌ **Evite:**
- Chains com lógica muito complexa (use agents)
- Hardcoding de prompts no código
- Sem validação de entrada/saída
- Prompts muito longos (use summarization)
- Modificar prompts em runtime sem versionar

## Performance

### Comparação com Agents

**Chain:**
- 1 request ao LLM
- Latência: ~500ms
- Custo: Baixo

**Agent (com 3 iterações):**
- 3+ requests ao LLM
- Latência: ~2000ms
- Custo: 3x maior

**Recomendação:** Use chains quando possível, agents quando necessário raciocinar.

## Integração com Outros Componentes

```
Chain Input
    ↓
Input Guard (validar)
    ↓
Load Prompt (templates)
    ↓
Format Variáveis
    ↓
Call LLM
    ↓
Output Guard (validar)
    ↓
Chain Output
```

## Troubleshooting

| Problema | Causa | Solução |
|----------|-------|---------|
| Variável não substituída | Placeholder incorreto | Usar `{nome}` no prompt |
| Prompt não encontrado | Arquivo não existe | Verificar nome em `src/core/prompts/` |
| Saída inválida | Formato inesperado | Adicionar instrução de formato no prompt |
| Latência alta | LLM lento | Usar modelo mais rápido ou cache |

## Próximos Passos

- [ ] Criar prompts para casos de uso específicos
- [ ] Versionar prompts existentes
- [ ] Implementar cache de prompts
- [ ] Adicionar logging detalhado
- [ ] Otimizar custo via prompt engineering
