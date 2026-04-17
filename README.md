# GenAI Agent Template

Template para MVPs com agentes de IA Generativa — suporta agentes com loop autônomo (ReAct, plan-and-execute) e pipelines lineares.

## Estrutura

```
genai-mvp-template/
├── src/
│   ├── core/                 # Motor principal do sistema
│   │   ├── agents/           # Agentes autônomos (ReAct loop)
│   │   ├── chains/           # Fluxos lineares (sem loop)
│   │   ├── memory/           # Memória curto/longo prazo
│   │   │   ├── buffer_memory.py       # Janela deslizante simples
│   │   │   ├── short_term.py          # ConversationMemory com API rica
│   │   │   ├── long_term.py           # Armazenamento persistente
│   │   │   └── README.md
│   │   ├── tools/            # Ferramentas para o agente
│   │   │   ├── example_tools.py
│   │   │   ├── registry.py            # Registro central de tools
│   │   │   └── README.md
│   │   ├── prompts/          # Templates de prompts versionados
│   │   │   ├── base_prompt.txt
│   │   │   └── README.md
│   │   └── guardrails/       # Validações e segurança
│   │       ├── input_guard.py         # Validação de entrada
│   │       ├── output_guard.py        # Validação de saída
│   │       └── README.md
│   ├── utils/                # Utilitários compartilhados
│   │   └── logger.py
│   ├── assets/               # Recursos estáticos
│   ├── app.py               # Aplicação principal
│   ├── config.py            # Configurações globais
│   └── main.py
├── tests/
│   └── test_agent.py
├── data/
│   ├── raw/                 # Dados brutos
│   └── processed/           # Dados processados
├── docs/
│   ├── architecture.md      # Decisões arquiteturais
│   ├── contributing.md      # Guia de contribuição
│   ├── decisions.md         # ADRs (Architecture Decision Records)
│   ├── technical-documentation.md
│   ├── prompts_strategy.md
│   ├── scope.md
│   └── README.md
├── logs/                    # Logs de execução
├── playground/              # Prototipagem e testes
│   └── test_chain.py
├── .env.example             # Template de variáveis de ambiente
├── requirements.txt         # Dependências Python
└── README.md
```

## ⚡ Quick Start (5 Minutos)

### Pré-requisitos

- Python 3.10+
- Conta no [Anthropic Claude](https://console.anthropic.com)
- Sua API Key do Claude

### 1. Setup do Ambiente

```bash
# Clonar repositório
git clone <repo>
cd genai-mvp-template

# Criar ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente

```bash
# Copiar template
cp .env.example .env

# Editar .env e adicionar sua chave
ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Seu Primeiro MVP (Escolha uma opção)

#### Opção A: Chain Simples ⭐ (Recomendado)

```python
from anthropic import Anthropic
from src.core.chains.base_chain import run_chain

client = Anthropic()
response = run_chain(
    user_input="Qual é a capital do Brasil?",
    model_client=client,
    variables={"domain": "geografia"}
)
print(response)
```

**Salve como `meu_mvp.py` e rode:**
```bash
python meu_mvp.py
```

#### Opção B: Agent com Ferramentas

```python
from anthropic import Anthropic
from src.core.agents.base_agent import BaseAgent

client = Anthropic()
agent = BaseAgent(client, max_iterations=10)
response = agent.run("Qual é a data de hoje? Busque informações sobre IA")
print(response)
```

#### Opção C: Exemplos Interativos

```bash
python QUICK_START.py
```

Escolha a opção (1-5) para ver 5 padrões de uso funcionando!

---

## 📚 Entender o Template

### Componentes Principais

| Componente | Uso | Complexidade |
|-----------|-----|-------------|
| **Chain** | Call único ao LLM + prompt estruturado | ⭐ Simples |
| **Agent** | Loop ReAct (raciocina, executa tools, repete) | ⭐⭐⭐ Complexo |
| **Memory** | Manter contexto entre chamadas | ⭐ Simples |
| **Tools** | Funções que o agent pode chamar | ⭐⭐ Médio |
| **Prompts** | Templates de instrução | ⭐ Simples |
| **Guardrails** | Validar entrada e saída | ⭐ Simples |

### Estrutura de Pastas

```
src/core/
├── chains/         ← Use para MVPs simples (recomendado)
├── agents/         ← Use se precisar de raciocínio complexo
├── tools/          ← Adicione suas ferramentas aqui
├── memory/         ← Contexto das conversas
├── prompts/        ← Templates de prompts
└── guardrails/     ← Segurança (validação)
```

---

## 🔨 Customizar para Seu Caso de Uso

### Adicionar uma Ferramenta Nova

```python
# 1. Implementar em src/core/tools/example_tools.py
def buscar_preco_produto(produto_nome: str) -> dict:
    """Busca o preço de um produto."""
    return {"produto": produto_nome, "preco": 99.90}

# 2. Registrar em src/core/tools/registry.py
TOOL_REGISTRY = {
    "buscar_preco_produto": buscar_preco_produto,
}

TOOL_DEFINITIONS = [
    {
        "name": "buscar_preco_produto",
        "description": "Busca o preço de um produto",
        "input_schema": {
            "type": "object",
            "properties": {
                "produto_nome": {"type": "string"}
            },
            "required": ["produto_nome"]
        }
    },
]

# 3. Usar com agent
agent = BaseAgent(client)
response = agent.run("Qual é o preço do notebook XYZ?")
```

### Customizar Prompt

```python
# Editar src/core/prompts/base_prompt.txt
response = run_chain(
    user_input="sua pergunta",
    model_client=client,
    variables={
        "domain": "seu domínio",
        "instruction_1": "sua instrução 1",
        "instruction_2": "sua instrução 2",
    }
)
```

### Adicionar Validações Customizadas

```python
# src/core/guardrails/input_guard.py
def validate_input(text: str) -> str:
    if not text or len(text) > 4000:
        raise InputValidationError("Input inválido")
    
    # ADICIONE SUAS VALIDAÇÕES:
    if "palavra-proibida" in text.lower():
        raise InputValidationError("Conteúdo não permitido")
    
    return text.strip()
```

---

## 💡 Chain vs Agent?

### Use **Chain** se:
- ✅ A tarefa é bem definida
- ✅ Quer resposta rápida
- ✅ Não precisa raciocinar/iterar
- ✅ Quer custo baixo

**Exemplos:** Classificação, Tradução, Resumo

### Use **Agent** se:
- ✅ A tarefa é complexa
- ✅ Precisa usar múltiplas ferramentas
- ✅ Precisa "pensar" sobre a melhor ação
- ✅ A resposta depende de múltiplas etapas

**Exemplos:** Busca de informações, Análise, Resolução de problemas

---

## 🧪 Testar Seu MVP

### Teste Local

```bash
# Rodar exemplos interativos
python QUICK_START.py

# Ou rodar seu próprio script
python meu_mvp.py
```

### Com Streamlit (Interface Web)

```bash
# Instalar streamlit
pip install streamlit

# Rodar UI
streamlit run src/app.py
```

### Testes Automatizados

```bash
# Rodar todos os testes
pytest tests/

# Rodar teste específico
pytest tests/test_agent.py -v
```

---

## 🚨 Troubleshooting

### Problema: "Module not found"
```
ModuleNotFoundError: No module named 'src'
```

**Solução:**
```bash
# Certificar que está na raiz do projeto
pwd  # ou cd para genai-mvp-template

# Certificar que venv está ativado
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Problema: "API Key inválida"
```
AuthenticationError: Invalid API key
```

**Solução:**
1. Verificar que `.env` existe e tem a chave
2. Verificar que a chave começa com `sk-ant-`
3. Testar em https://console.anthropic.com

### Problema: "Rate limit exceeded"
```
RateLimitError: 429
```

**Solução:**
- Muitas requisições rápido
- Adicione delays entre chamadas
- Considere usar cache

---

## 🎓 Próximos Passos (Recomendados)

### Dia 1: MVP Funcional
- [ ] Rodar `QUICK_START.py`
- [ ] Entender Chain vs Agent
- [ ] Criar seu primeiro script com chain

### Dia 2: MVP Customizado
- [ ] Adicionar sua primeira tool
- [ ] Customizar prompt
- [ ] Adicionar validações

### Dia 3: MVP em Produção
- [ ] Adicionar logging
- [ ] Implementar testes
- [ ] Deploy (Vercel, Railway, AWS)

---

## ✨ TL;DR (Muito Longo, Não Leu)

```bash
# 1. Setup (2 min)
git clone <repo>
cd genai-mvp-template
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Editar .env com sua API key

# 2. Rodar exemplo (30 seg)
python QUICK_START.py

# 3. Criar seu MVP (2 min)
cat > meu_mvp.py << 'EOF'
from anthropic import Anthropic
from src.core.chains.base_chain import run_chain

client = Anthropic()
response = run_chain(
    user_input="Sua pergunta aqui",
    model_client=client,
    variables={"domain": "seu domínio"}
)
print(response)
EOF

python meu_mvp.py
```

**Pronto! Seu MVP está rodando.** 🎉

## Estrutura de Pastas - Guia Detalhado

### `src/core/agents/` - Agentes Autônomos
- **Loop ReAct**: Raciocina → Escolhe Tool → Executa → Observa → Repete
- Base class com suporte a múltiplas estratégias de agente
- [Documentação completa →](src/core/agents/README.md)

### `src/core/chains/` - Fluxos Lineares
- Pipelines determinísticos (sem loop autônomo)
- Ideal para workflows bem definidos
- [Documentação completa →](src/core/chains/README.md)

### `src/core/memory/` - Sistema de Memória
- **ConversationMemory**: Contexto recente (últimas 20 msgs)
- **LongTermMemory**: Histórico persistente e aprendizados
- [Documentação completa →](src/core/memory/README.md)

### `src/core/tools/` - Ferramentas
- Registro central de ferramentas disponíveis
- Integração automática com agentes
- [Documentação completa →](src/core/tools/README.md)

### `src/core/prompts/` - Templates de Prompts
- Versionamento manual de prompts
- Convenção: `{nome}_v{major}.{minor}.txt`
- [Documentação completa →](src/core/prompts/README.md)

### `src/core/guardrails/` - Segurança
- Validação de entrada do usuário
- Validação de saída do agente
- Prevenção de prompt injection
- [Documentação completa →](src/core/guardrails/README.md)

## Fluxo de Desenvolvimento

```
USER INPUT
    ↓
INPUT_GUARD (validação de entrada)
    ↓
AGENT/CHAIN (processamento)
    ├── Acessa MEMORY (contexto)
    ├── Usa TOOLS (ações)
    └── Consulta PROMPTS (instruções)
    ↓
OUTPUT_GUARD (validação de saída)
    ↓
RESPONSE PARA USUÁRIO
```

## Testes

```bash
# Rodar todos os testes
pytest tests/

# Rodar teste específico
pytest tests/test_agent.py -v
```

## 📖 Documentação Detalhada

Para aprofundar em cada componente, consulte:

- **[src/core/chains/README.md](src/core/chains/README.md)** - Chains (pipelines lineares)
- **[src/core/agents/README.md](src/core/agents/README.md)** - Agents (ReAct loop)
- **[src/core/tools/README.md](src/core/tools/README.md)** - Tools (ferramentas)
- **[src/core/memory/README.md](src/core/memory/README.md)** - Memory (contexto)
- **[src/core/guardrails/README.md](src/core/guardrails/README.md)** - Guardrails (segurança)
- **[src/core/prompts/README.md](src/core/prompts/README.md)** - Prompts (templates)

### Arquitetura e Decisões

- **[docs/architecture.md](docs/architecture.md)** - Decisões e padrões
- **[docs/contributing.md](docs/contributing.md)** - Guia de contribuição
- **[docs/decisions.md](docs/decisions.md)** - ADRs (Architecture Decision Records)
- **[docs/scope.md](docs/scope.md)** - Escopo do projeto
- **[docs/technical-documentation.md](docs/technical-documentation.md)** - Referência técnica
- **[docs/prompts_strategy.md](docs/prompts_strategy.md)** - Estratégia de prompts

## Próximos Passos

1. ✅ Configurar ambiente e instalar dependências
2. ✅ Explorar exemplos em `playground/`
3. ✅ Ler [architecture.md](docs/architecture.md)
4. ✅ Criar seu primeiro agent ou chain
5. ✅ Implementar guardrails específicos do seu caso de uso
6. ✅ Armazenar e recuperar conhecimento com LongTermMemory
