# Agents - Agentes Autônomos

Agentes que raciocinam sobre tarefas e executam ações de forma autônoma usando **loop ReAct** (Reason + Act).

## Arquitetura

```
Task Input
    ↓
[REASON] - Raciocinar qual ação tomar
    ↓
[ACT] - Executar ferramenta ou responder
    ↓
[OBSERVE] - Ver resultado
    ↓
Repete até conclusão ou max_iterations
    ↓
Final Response
```

## Fluxo de um Agent

1. **Recebe uma task** do usuário (validada via `input_guard`)
2. **Raciocina** qual ferramenta usar (ou responde direto)
3. **Executa a ferramenta** consultando o `TOOL_REGISTRY`
4. **Observa o resultado** e adiciona à memória
5. **Repete** até terminar ou atingir limite de iterações
6. **Retorna resposta final** (validada via `output_guard`)

## BaseAgent - Exemplo de Uso

```python
from anthropic import Anthropic
from src.core.agents.base_agent import BaseAgent

# Inicializar cliente de IA
client = Anthropic()

# Criar agente com até 10 iterações
agent = BaseAgent(model_client=client, max_iterations=10)

# Executar tarefa
response = agent.run("Qual é a capital do Brasil e quantos habitantes tem?")
print(response)
```

## Componentes Principais

### BaseAgent

**Responsabilidades:**
- Gerenciar o loop ReAct
- Validar entrada e saída
- Manter memória da conversa
- Executar ferramentas dinamicamente

**Atributos:**
- `client`: Cliente de IA (ex: Anthropic)
- `max_iterations`: Limite de tentativas (padrão: 10)
- `memory`: Contexto da conversa (ConversationMemory)

**Métodos:**
- `run(task: str) -> str`: Executa a tarefa e retorna resposta
- `_execute_tool(name, inputs)`: Executa ferramenta do registro
- `_system_prompt()`: Retorna prompt do sistema para o modelo

### Integração com Outros Componentes

```
Agent
├── Memory (ConversationMemory)
│   └── Mantém contexto recente
├── Tools (TOOL_REGISTRY)
│   └── Ferramentas disponíveis
├── Prompts (system_prompt)
│   └── Instruções para o modelo
├── Input Guard
│   └── Valida entrada do usuário
└── Output Guard
    └── Valida resposta final
```

## Criando Seu Próprio Agent

```python
from src.core.agents.base_agent import BaseAgent
from src.core.memory.short_term import ConversationMemory
from src.core.memory.long_term import LongTermMemory

class CustomAgent(BaseAgent):
    """Agent customizado com memória de longo prazo."""
    
    def __init__(self, model_client, max_iterations=10):
        super().__init__(model_client, max_iterations)
        self.long_term_memory = LongTermMemory(collection_name="custom_agent")
    
    def run(self, task: str) -> str:
        # 1. Recuperar contexto relevante do histórico
        relevant_context = self.long_term_memory.retrieve_by_topic("general")
        
        # 2. Executar agent normalmente
        response = super().run(task)
        
        # 3. Se conversa atingiu limite, armazenar resumo
        if len(self.memory) >= 20:
            summary = self._summarize_conversation()
            self.long_term_memory.store(
                content=summary,
                metadata={"topic": "general", "importance": "medium"}
            )
            self.memory.clear()
        
        return response
    
    def _summarize_conversation(self) -> str:
        """Resumir conversa para armazenar em LongTermMemory."""
        messages = self.memory.get_all()
        # Aqui você chamaria um LLM para gerar o resumo
        return "Resumo da conversa..."
```

## Adicionando Novas Ferramentas

1. Implementar a função em `src/core/tools/example_tools.py`
2. Registrar em `src/core/tools/registry.py`
3. Agent usa automaticamente

Exemplo:

```python
# src/core/tools/example_tools.py
def calculate_sum(a: int, b: int) -> int:
    """Calcula a soma de dois números."""
    return a + b

# src/core/tools/registry.py
from src.core.tools.example_tools import calculate_sum

TOOL_REGISTRY = {
    "calculate_sum": calculate_sum,
    # ... outros tools
}

TOOL_DEFINITIONS = [
    {
        "name": "calculate_sum",
        "description": "Calcula a soma de dois números",
        "input_schema": {
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": "integer"}
            },
            "required": ["a", "b"]
        }
    },
    # ... outros tools
]
```

## Padrões de Uso

### Pattern 1: Agent Simples (MVP)

```python
agent = BaseAgent(client)
response = agent.run("sua tarefa")
```

### Pattern 2: Agent com Contexto Persistente

```python
agent = CustomAgent(client)
# Primeira conversa
response1 = agent.run("Aprenda que gosto de data science")
# Segunda conversa - acessa contexto da primeira
response2 = agent.run("Recomende um tópico para estudar")
```

### Pattern 3: Agent com Validações Customizadas

```python
class SecureAgent(BaseAgent):
    def run(self, task: str) -> str:
        # Validações customizadas
        if len(task) > 1000:
            raise ValueError("Tarefa muito longa")
        return super().run(task)
```

## Configuração Avançada

### Ajustar Model e Max Tokens

```python
# Modificar _system_prompt para usar modelo diferente
class AgentWithGPT(BaseAgent):
    def run(self, task: str) -> str:
        # Lógica customizada aqui
        pass
```

### Controlar Iterações

```python
# Agent mais "preguiçoso" - menos iterações
agent = BaseAgent(client, max_iterations=3)

# Agent mais "agressivo" - mais iterações
agent = BaseAgent(client, max_iterations=20)
```

## Troubleshooting

| Problema | Causa | Solução |
|----------|-------|---------|
| Agent não encontra ferramenta | Tool não registrada | Verificar `TOOL_REGISTRY` |
| Resposta incompleta | Limite de iterações muito baixo | Aumentar `max_iterations` |
| Loops infinitos | Tool chama a si mesma | Revisar lógica da tool |
| Erro de validação | Input/output não passa em guard | Revisar regras de guardrails |

## Próximos Passos

- [ ] Implementar mais ferramentas em `src/core/tools/`
- [ ] Criar agents customizados para casos específicos
- [ ] Integrar com LongTermMemory para aprendizado
- [ ] Adicionar validações customizadas via guardrails
- [ ] Implementar logging e monitoramento
