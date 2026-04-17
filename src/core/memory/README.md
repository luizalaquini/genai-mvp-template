# Memory

## Tipos disponíveis

### Arquitetura de Memória (Recomendado)

```
User Message
     ↓
ConversationMemory (curto prazo - últimas 20 msgs)
     ↓ (quando atinge limite)
Resumir com LLM
     ↓
LongTermMemory (longo prazo - persistente)
     ↓ (busca semântica)
Próxima Conversa (contexto enriquecido)
```

**Três camadas de memória:**
1. **BufferMemory**: Janela simples (deprecated em favor de ConversationMemory)
2. **ConversationMemory**: Contexto recente e imediato
3. **LongTermMemory**: Histórico, aprendizados e contexto enriquecido

---

### BufferMemory (`buffer_memory.py`)
Janela deslizante de mensagens com API genérica. Simples e suficiente para a maioria dos MVPs.

**Características:**
- Estrutura de dados: lista Python
- Limite: últimas N mensagens (padrão: 20)
- Método único `add()` para todos os tipos de mensagem
- Gerenciamento manual de limite com slicing

**Quando usar:** Casos simples onde você adiciona mensagens de forma homogênea

---

### ConversationMemory (`short_term.py`)
Buffer circular com API específica por tipo de mensagem. Oferece mais controle e clareza nos tipos de role.

**Características:**
- Estrutura de dados: `deque` (fila circular)
- Limite: últimas N mensagens (padrão: 20) - **automático**
- Métodos específicos: `add_user_message()`, `add_assistant_message()`, `add_system_message()`
- Funcionalidades extras: `get_last_n(n)` para recuperar apenas as últimas N mensagens
- Gerenciamento automático de limite via `maxlen` do deque

**Quando usar:** Quando você quer diferenciação clara de tipos de mensagem e performance otimizada

---

### LongTermMemory (`long_term.py`)
Armazenamento persistente de memórias com busca e gerenciamento de metadados.

**Características:**
- Armazenamento persistente com timestamps
- Metadados associados (tópico, importância, etc)
- Múltiplas estratégias de recuperação
- Rastreamento de acessos (relevância)
- Suporta integração com vector databases (ChromaDB, Pinecone)

**Métodos principais:**
- `store(content, metadata)` - Armazena uma memória
- `retrieve_by_topic(topic)` - Busca por tópico
- `retrieve_recent(n)` - Últimas N memórias
- `retrieve_most_accessed(n)` - Memórias mais relevantes
- `update_memory(id, content)` - Atualiza uma memória
- `delete_memory(id)` - Deleta uma memória
- `get_stats()` - Estatísticas de uso

**Quando usar:** Para armazenar resumos de conversas, contexto importante e aprendizados do agente

---

## Comparativo Detalhado

| Aspecto | BufferMemory | ConversationMemory | LongTermMemory |
|---------|--------------|-------------------|----------------|
| **Estrutura** | `list` | `deque(maxlen=N)` | `list` (com timestamps) |
| **Scope** | Sessão atual | Sessão atual | Persistente |
| **Capacidade** | ~20-50 msgs | ~20-100 msgs | Ilimitada |
| **API** | Genérica (`add()`) | Específica por role | Por tipo de armazenamento |
| **Metadados** | Não | Não | Sim (rich metadata) |
| **Acesso** | FIFO | FIFO | By-topic, by-recency, by-access |
| **Busca** | Não | Não | Sim (simples + semântica) |
| **Melhor para** | Casos simples | Conversas recentes | Histórico e contexto |

---

## Guia de Utilização

### BufferMemory - Exemplo Básico

```python
from src.core.memory.buffer_memory import BufferMemory

# Inicializar com limite padrão (20 mensagens)
memory = BufferMemory()

# Ou com limite customizado
memory = BufferMemory(max_messages=50)

# Adicionar mensagens (genérico)
memory.add("user", "Olá, como você está?")
memory.add("assistant", "Estou bem, obrigado!")
memory.add("system", "Contexto do sistema")

# Recuperar todas as mensagens
messages = memory.get_messages()
# Resultado: [
#     {"role": "user", "content": "Olá, como você está?"},
#     {"role": "assistant", "content": "Estou bem, obrigado!"},
#     {"role": "system", "content": "Contexto do sistema"}
# ]

# Verificar quantidade de mensagens
print(len(memory))  # 3

# Limpar histórico
memory.clear()
```

---

### ConversationMemory - Exemplo Detalhado

```python
from src.core.memory.short_term import ConversationMemory

# Inicializar com limite padrão (20 mensagens)
memory = ConversationMemory()

# Ou com limite customizado
memory = ConversationMemory(max_messages=100)

# Adicionar mensagens com métodos específicos
memory.add_system_message("Você é um assistente helpful")
memory.add_user_message("Qual é a capital do Brasil?")
memory.add_assistant_message("A capital do Brasil é Brasília")

# Recuperar todas as mensagens
all_messages = memory.get_all()
# Resultado: [
#     {"role": "system", "content": "Você é um assistente helpful"},
#     {"role": "user", "content": "Qual é a capital do Brasil?"},
#     {"role": "assistant", "content": "A capital do Brasil é Brasília"}
# ]

# Recuperar apenas as últimas N mensagens
last_2 = memory.get_last_n(2)
# Resultado: [
#     {"role": "user", "content": "Qual é a capital do Brasil?"},
#     {"role": "assistant", "content": "A capital do Brasil é Brasília"}
# ]

# Limpar histórico
memory.clear()
```

---

## Caso de Uso: Integração com Agent

```python
from src.core.agents.base_agent import BaseAgent
from src.core.memory.short_term import ConversationMemory

class MyAgent(BaseAgent):
    def __init__(self):
        self.memory = ConversationMemory(max_messages=50)
    
    def process(self, user_input: str) -> str:
        # Adicionar mensagem do usuário
        self.memory.add_user_message(user_input)
        
        # Processar com contexto das últimas mensagens
        context = self.memory.get_all()
        # ... usar context no LLM
        
        response = "Resposta do agente"
        
        # Adicionar resposta ao histórico
        self.memory.add_assistant_message(response)
        
        return response
```

---

### LongTermMemory - Exemplo de Uso

```python
from src.core.memory.long_term import LongTermMemory

# Inicializar
long_memory = LongTermMemory(collection_name="conversation_history")

# Armazenar um resumo de conversa antiga
long_memory.store(
    content="Usuário perguntou sobre importação de dados CSV. Solução: usar pandas.read_csv()",
    metadata={
        "topic": "data_import",
        "importance": "high",
        "user_id": "user_123"
    }
)

# Armazenar outro aprendizado
long_memory.store(
    content="Preferência do usuário: quer sempre gráficos em matplotlib",
    metadata={
        "topic": "visualization",
        "importance": "medium",
        "user_id": "user_123"
    }
)

# Recuperar memórias por tópico
data_memories = long_memory.retrieve_by_topic("data_import")

# Recuperar memórias mais recentes
recent = long_memory.get_last_n(5)

# Recuperar memórias mais acessadas (mais relevantes)
important = long_memory.retrieve_most_accessed(3)

# Ver estatísticas
stats = long_memory.get_stats()
# Resultado: {
#     "total_memories": 2,
#     "total_accesses": 5,
#     "avg_accesses_per_memory": 2.5,
#     ...
# }

# Atualizar uma memória
long_memory.update_memory(
    memory_id="mem_0_1713262800",
    new_content="Nova informação sobre importação...",
    new_metadata={"importance": "critical"}
)
```

---

### Pipeline Completo: Curto + Longo Prazo

```python
from src.core.memory.short_term import ConversationMemory
from src.core.memory.long_term import LongTermMemory

class SmartAgent:
    def __init__(self):
        self.short_term = ConversationMemory(max_messages=20)
        self.long_term = LongTermMemory()
    
    def process(self, user_input: str) -> str:
        # 1. Adicionar ao contexto recente
        self.short_term.add_user_message(user_input)
        
        # 2. Recuperar contexto relevante do longo prazo
        relevant_memories = self.long_term.retrieve_by_topic("general")
        
        # 3. Combinar contextos
        context = {
            "recent": self.short_term.get_all(),
            "background": relevant_memories
        }
        
        # 4. Processar com LLM usando contexto combinado
        response = "Resposta do agente"
        
        # 5. Adicionar resposta ao contexto recente
        self.short_term.add_assistant_message(response)
        
        # 6. Se conversa atingir limite, resumir e armazenar
        if len(self.short_term) >= 20:
            summary = self._summarize_conversation()  # Usar LLM
            self.long_term.store(
                content=summary,
                metadata={"topic": "general", "importance": "medium"}
            )
            self.short_term.clear()
        
        return response
    
    def _summarize_conversation(self) -> str:
        # Usar LLM para resumir as mensagens recentes
        messages = self.short_term.get_all()
        # ... chamada ao LLM ...
        return "Resumo da conversa"
```

---

## Próximos Passos (Evolução em Produção)

O `LongTermMemory` oferece uma base sólida. Para escalar em produção, integre com:

- **ChromaDB** (local, zero config) - ideal para começar
- **Pinecone** (cloud, gerenciado) - melhor performance
- **Weaviate** (open source, híbrido) - flexibilidade
- **Qdrant** (alta performance) - para escala

### Exemplo de Evolução: ChromaDB Integration

```python
import chromadb
from typing import List, Dict

class LongTermMemoryWithChroma(LongTermMemory):
    """Estende LongTermMemory com ChromaDB para busca semântica."""
    
    def __init__(self, collection_name: str = "memories"):
        super().__init__(collection_name)
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def store(self, content: str, metadata: Optional[Dict] = None) -> str:
        """Armazena em memória local + ChromaDB."""
        memory_id = super().store(content, metadata)
        
        # Adicionar ao ChromaDB para busca semântica
        self.collection.add(
            ids=[memory_id],
            documents=[content],
            metadatas=[metadata or {}]
        )
        
        return memory_id
    
    def retrieve_semantic(self, query: str, n: int = 5) -> List[Dict]:
        """Busca semântica usando embeddings."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n
        )
        
        return [
            {
                "id": id,
                "content": doc,
                "metadata": metadata,
                "distance": distance
            }
            for id, doc, metadata, distance in zip(
                results["ids"][0],
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            )
        ]
```

---

## Recomendações por Caso de Uso

| Cenário | Short-term | Long-term | Observação |
|---------|-----------|----------|-----------|
| **Chatbot MVP** | ConversationMemory (20 msgs) | LongTermMemory (local) | Simples e suficiente |
| **Chatbot em Produção** | ConversationMemory (50 msgs) | LongTermMemory + ChromaDB | Adicione busca semântica |
| **Agente Multi-Task** | ConversationMemory (100 msgs) | LongTermMemory + Pinecone | Performance e escala |
| **Assistente Pessoal** | ConversationMemory (200 msgs) | LongTermMemory + Weaviate | Histórico completo do usuário |

---

## Padrão Sugerido: Resumo e Armazenamento

1. Use `ConversationMemory` para contexto recente (últimas 20 mensagens)
2. Quando atinge limite, **resuma a conversa com LLM** antes de armazenar
3. Armazene resumo em `LongTermMemory` com metadados (tópico, data, importância)
4. Em novas conversas, recupere resumos relevantes via busca semântica
5. Use resumos como "preâmbulo" junto com ConversationMemory recente

