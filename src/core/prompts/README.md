# Prompts - Templates Versionados

Biblioteca centralizada de prompts para agentes e chains, com versionamento manual e controle de qualidade.

## Filosofia

- ✅ Prompts em **arquivos** (não hardcoded)
- ✅ Versionamento manual para rastreabilidade
- ✅ Templates com placeholders para reutilização
- ✅ Versões diferentes para A/B testing
- ✅ Documentação de cada versão

## Convenção de Nomes

```
{nome_descritivo}_v{major}.{minor}.txt
```

**Exemplos:**
- `base_prompt_v1.0.txt` - Versão inicial
- `base_prompt_v1.1.txt` - Pequeno ajuste
- `base_prompt_v2.0.txt` - Mudança significativa
- `summarize_v1.0.txt` - Novo prompt
- `classify_sentiment_v1.0.txt` - Outro prompt

**Quando incrementar versão:**
- `major++`: Mudança de abordagem/instruções principais
- `minor++`: Ajuste de phrasing/clareza

## Estrutura de um Prompt

```
# Prompt: {nome}
# Versão: {major}.{minor}
# Descrição: O que este prompt faz

## System
[Instruções para o modelo agir como]

## Instruções
[Passos específicos]

## Formato de Resposta
[Como formatar a saída]

## Exemplos (opcional)
[Exemplos de input/output]

## Variáveis
- {variavel_1}: Descrição
- {variavel_2}: Descrição
```

## Exemplo Completo

```txt
# Prompt: summarize
# Versão: 1.0
# Descrição: Sumariza textos longos mantendo pontos-chave

## System
Você é um especialista em síntese e resumo de conteúdo.
Seu objetivo é extrair as informações mais importantes de forma concisa.
Sempre responda em {language}.

## Instruções
1. Identifique os 3-5 pontos principais do texto
2. Elimine redundâncias e detalhes secundários
3. Mantenha a clareza e coesão
4. Use linguagem direta e profissional

## Formato de Resposta
Use bullet points, máximo {max_words} palavras.

## Exemplos
INPUT: "A inteligência artificial é uma área da ciência da computação que busca..."
OUTPUT:
• IA é uma área da ciência da computação
• Busca simular inteligência humana
• Aplicações práticas em diversos setores

## Variáveis
- {language}: Idioma de resposta (padrão: português)
- {max_words}: Limite de palavras (padrão: 150)
- {tone}: Tom (formal, casual, técnico)
```

## Usando Prompts

### Com Chains

```python
from src.core.chains.base_chain import run_chain
from anthropic import Anthropic

client = Anthropic()

# Carrega base_prompt_v1.0.txt automaticamente
response = run_chain(
    user_input="Seu texto aqui",
    model_client=client,
    variables={
        "domain": "data science",
        "instruction_1": "Seja objetivo",
        "instruction_2": "Use exemplos",
        "output_format": "JSON"
    }
)
```

### Com Agents

```python
from src.core.agents.base_agent import BaseAgent

class CustomAgent(BaseAgent):
    def _system_prompt(self) -> str:
        from pathlib import Path
        prompt_path = Path(__file__).parent / "prompts" / "base_prompt_v1.0.txt"
        template = prompt_path.read_text()
        
        return template.format(
            domain="assistência técnica",
            instruction_1="Use linguagem clara",
            instruction_2="Ofereça soluções práticas"
        )
```

## Gerenciamento de Prompts

### Criando um Novo Prompt

1. Defina um nome descritivo: `analyze_sentiment_v1.0.txt`
2. Estruture com as seções padrão
3. Documente variáveis usadas
4. Teste com casos variados
5. Guarde no versionamento

```bash
# Estrutura
src/core/prompts/
├── base_prompt_v1.0.txt
├── base_prompt_v1.1.txt
├── base_prompt_v2.0.txt
├── summarize_v1.0.txt
├── classify_sentiment_v1.0.txt
└── README.md
```

### A/B Testing de Prompts

```python
# Testar diferentes versões
def test_prompt_versions():
    from pathlib import Path
    
    versions = [
        ("base_prompt_v1.0.txt", "Versão original"),
        ("base_prompt_v1.1.txt", "Com exemplos"),
        ("base_prompt_v2.0.txt", "Novo template"),
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

## Padrões de Prompts

### Pattern 1: Role-Playing

```txt
# Prompt: expert_analyst
# Versão: 1.0

## System
Você é um analista especializado em {domain}.
Com {years_of_experience} anos de experiência na área.
Você é conhecido por explicações claras e insights profundos.

## Instruções
1. Analise o seguinte texto/dados
2. Identifique padrões principais
3. Sugira ações recomendadas

## Formato
Estruture a resposta em: Análise | Padrões | Recomendações
```

### Pattern 2: Chain-of-Thought

```txt
# Prompt: reasoning
# Versão: 1.0

## System
Você é um pensador lógico e estruturado.
Sempre mostra seu raciocínio passo a passo.

## Instruções
1. Apresente o problema
2. Quebre em sub-problemas
3. Resolva cada um
4. Combine para solução final

## Formato
Use este template:
PROBLEMA: [...]
SUB-PROBLEMAS: [...]
SOLUÇÕES: [...]
RESPOSTA FINAL: [...]
```

### Pattern 3: Few-Shot Learning

```txt
# Prompt: classify_entities
# Versão: 1.0

## System
Você classifica entidades em categorias.

## Exemplos
INPUT: "João mora em São Paulo"
CLASSIFY: João (Person), São Paulo (Location)

INPUT: "Apple lançou novo iPhone"
CLASSIFY: Apple (Company), iPhone (Product)

## Tarefa
Classifique as entidades no seguinte texto:
{user_text}

## Formato
ENTITY: [entity] | CATEGORY: [category]
```

### Pattern 4: Temperature Variants

```txt
# Prompt: creative_writing
# Versão: 1.0
# NOTA: Use temperature=0.8+ para melhores resultados

## System
Você é um escritor criativo e imaginativo.
Escreva de forma envolvente e original.

[resto do prompt]
```

## Boas Práticas

✅ **Faça:**
- Versionamento claro (semver)
- Documentação de mudanças entre versões
- Testes com múltiplos inputs
- Variáveis bem nomeadas `{var_name}`
- Exemplos nos prompts
- Comentários explicativos
- Manter histórico em Git

❌ **Evite:**
- Prompts muito longos (>2000 chars)
- Hardcoding de valores
- Sem versionamento
- Mudanças sem documentar
- Nomes confusos de variáveis
- Sem exemplos de uso

## Otimização de Prompts

### 1. Teste Variações

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

### 2. Métricas de Qualidade

```python
def evaluate_output(output, criteria):
    """Avaliar qualidade da saída"""
    score = 0
    
    # Completude
    if len(output) > 50:
        score += 1
    
    # Relevância
    if any(word in output for word in ["importante", "significante"]):
        score += 1
    
    # Clareza
    if output.count("?") < output.count("."):
        score += 1
    
    return score / 3  # 0-1
```

### 3. Iteração Orientada por Dados

```python
# Histórico de melhorias
PROMPT_VERSIONS = {
    "1.0": "Baseline",
    "1.1": "Adicionados exemplos (+10% qualidade)",
    "1.2": "Melhorada instrução de output (+5% qualidade)",
    "2.0": "Novo template com role-playing (+20% qualidade)"
}
```

## Integração com CI/CD

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

## Migração Entre Versões

Quando quiser mudar a versão padrão:

```python
# Versão antiga
from src.core.chains.base_chain import load_prompt
template = load_prompt("base_prompt")  # Carrega v1.0 automaticamente

# Versão nova
template_v2 = load_prompt("base_prompt_v2")  # Carrega v2.0 explicitamente
```

## Documentação de Mudanças

Mantenha um CHANGELOG:

```markdown
# Changelog - Prompts

## [2.0.0] - 2024-04-16
### Changed
- Novo template com role-playing mais forte
- Melhorada instrução de output
- Adicionados exemplos de edge cases

### Performance
- +20% qualidade em testes internos
- -5% latência (prompt mais conciso)

## [1.1.0] - 2024-04-10
### Added
- Exemplos de output esperado
- Variável `tone` customizável

### Fixed
- Corrigida instrução de formatação JSON
```

## Troubleshooting

| Problema | Causa | Solução |
|----------|-------|---------|
| Saída inconsistente | Prompt vago | Adicionar exemplos |
| Modelo ignora instruções | Prompt muito longo | Simplificar ou priorizar |
| Output em formato errado | Instruções claras | Adicionar formato explícito |
| Performance ruim | Prompt genérico | Adicionar context/role |

## Próximos Passos

- [ ] Criar banco de prompts testados
- [ ] Implementar prompt versioning em BD
- [ ] Setup de A/B testing automático
- [ ] Criar dashboard de qualidade de prompts
- [ ] Documentar melhores práticas por domínio
- [ ] Integrar com observability/monitoring
