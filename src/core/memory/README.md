# Memory

## Available Types

### Memory Architecture (Recommended)

```
User Message
     ↓
ConversationMemory (short-term - last 20 messages)
     ↓ (when limit is reached)
Summarize with LLM
     ↓
LongTermMemory (long-term - persistent)
     ↓ (semantic search)
Next Conversation (enriched context)
```

**Three memory layers:**
1. **BufferMemory**: Simple sliding window (deprecated in favor of ConversationMemory)
2. **ConversationMemory**: Immediate recent context
3. **LongTermMemory**: History, learnings, and enriched context

---

### BufferMemory (`buffer_memory.py`)
Sliding window of messages with a generic API. Simple and suitable for most MVPs.

**Features:**
- Data structure: Python list
- Limit: last N messages (default: 20)
- Single `add()` method for all message types
- Manual limit management using slicing

**When to use:** Simple cases where you add messages homogeneously

---

### ConversationMemory (`short_term.py`)
Circular buffer with a message-type-specific API. Provides better control and clearer role handling.

**Features:**
- Data structure: `deque` (circular queue)
- Limit: last N messages (default: 20) - **automatic**
- Specific methods: `add_user_message()`, `add_assistant_message()`, `add_system_message()`
- Extra convenience: `get_last_n(n)` to retrieve the last N messages only
- Automatic limit management via `deque(maxlen)`

**When to use:** When you want clear message role differentiation and optimized performance

---

### LongTermMemory (`long_term.py`)
Persistent memory storage with metadata management and semantic-style retrieval.

**Features:**
- Persistent storage with timestamps
- Associated metadata (topic, importance, etc.)
- Multiple retrieval strategies
- Access tracking for relevance
- Supports integration with vector databases (ChromaDB, Pinecone)

**Main methods:**
- `store(content, metadata)` - Store a memory entry
- `retrieve_by_topic(topic)` - Retrieve memories by topic
- `retrieve_recent(n)` - Get the most recent N memories
- `retrieve_most_accessed(n)` - Get the most accessed memories
- `update_memory(id, content)` - Update a memory entry
- `delete_memory(id)` - Delete a memory entry
- `get_stats()` - Return usage statistics

**When to use:** Store conversation summaries, important context, and agent learnings

---

## Detailed Comparison

| Aspect | BufferMemory | ConversationMemory | LongTermMemory |
|---------|--------------|-------------------|----------------|
| **Structure** | `list` | `deque(maxlen=N)` | `list` (with timestamps) |
| **Scope** | Current session | Current session | Persistent |
| **Capacity** | ~20-50 msgs | ~20-100 msgs | Unlimited |
| **API** | Generic (`add()`) | Role-specific | Storage-specific |
| **Metadata** | No | No | Yes (rich metadata) |
| **Access** | FIFO | FIFO | By-topic, recency, access |
| **Search** | No | No | Yes (simple + semantic) |
| **Best for** | Simple cases | Recent conversations | History and context |

---

## Usage Guide

### BufferMemory - Basic Example

```python
from src.core.memory.buffer_memory import BufferMemory

# Initialize with the default limit (20 messages)
memory = BufferMemory()

# Or with a custom limit
memory = BufferMemory(max_messages=50)

# Add messages (generic)
memory.add("user", "Hello, how are you?")
memory.add("assistant", "I'm good, thank you!")
memory.add("system", "System context")

# Retrieve all messages
messages = memory.get_messages()
# Result: [
#     {"role": "user", "content": "Hello, how are you?"},
#     {"role": "assistant", "content": "I'm good, thank you!"},
#     {"role": "system", "content": "System context"}
# ]

# Check message count
print(len(memory))  # 3

# Clear history
memory.clear()
```

---

### ConversationMemory - Detailed Example

```python
from src.core.memory.short_term import ConversationMemory

# Initialize with the default limit (20 messages)
memory = ConversationMemory()

# Or with a custom limit
memory = ConversationMemory(max_messages=100)

# Add messages with specific methods
memory.add_system_message("You are a helpful assistant")
memory.add_user_message("What is the capital of Brazil?")
memory.add_assistant_message("The capital of Brazil is Brasília")

# Retrieve all messages
all_messages = memory.get_all()
# Result: [
#     {"role": "system", "content": "You are a helpful assistant"},
#     {"role": "user", "content": "What is the capital of Brazil?"},
#     {"role": "assistant", "content": "The capital of Brazil is Brasília"}
# ]

# Retrieve only the last N messages
last_2 = memory.get_last_n(2)
# Result: [
#     {"role": "user", "content": "What is the capital of Brazil?"},
#     {"role": "assistant", "content": "The capital of Brazil is Brasília"}
# ]

# Clear history
memory.clear()
```

---

## Usage Example: Integrating with an Agent

```python
from src.core.agents.base_agent import BaseAgent
from src.core.memory.short_term import ConversationMemory

class MyAgent(BaseAgent):
    def __init__(self):
        self.memory = ConversationMemory(max_messages=50)
    
    def process(self, user_input: str) -> str:
        # Add user message
        self.memory.add_user_message(user_input)
        
        # Process using the last messages as context
        context = self.memory.get_all()
        # ... use context in the LLM
        
        response = "Agent response"
        
        # Add response to history
        self.memory.add_assistant_message(response)
        
        return response
```

---

### LongTermMemory - Usage Example

```python
from src.core.memory.long_term import LongTermMemory

# Initialize
long_memory = LongTermMemory(collection_name="conversation_history")

# Store a summary of an older conversation
long_memory.store(
    content="User asked about CSV data import. Solution: use pandas.read_csv()",
    metadata={
        "topic": "data_import",
        "importance": "high",
        "user_id": "user_123"
    }
)

# Store another learning
long_memory.store(
    content="User preference: always display charts with matplotlib",
    metadata={
        "topic": "visualization",
        "importance": "medium",
        "user_id": "user_123"
    }
)

# Retrieve memories by topic
data_memories = long_memory.retrieve_by_topic("data_import")

# Retrieve the most recent memories
recent = long_memory.retrieve_recent(5)

# Retrieve the most accessed memories (most relevant)
important = long_memory.retrieve_most_accessed(3)

# Get stats
stats = long_memory.get_stats()
# Result: {
#     "total_memories": 2,
#     "total_accesses": 5,
#     "avg_accesses_per_memory": 2.5,
#     ...
# }

# Update a memory
long_memory.update_memory(
    memory_id="mem_0_1713262800",
    new_content="New information about data import...",
    new_metadata={"importance": "critical"}
)
```

---

### Full Pipeline: Short + Long Term

```python
from src.core.memory.short_term import ConversationMemory
from src.core.memory.long_term import LongTermMemory

class SmartAgent:
    def __init__(self):
        self.short_term = ConversationMemory(max_messages=20)
        self.long_term = LongTermMemory()
    
    def process(self, user_input: str) -> str:
        # 1. Add to recent context
        self.short_term.add_user_message(user_input)
        
        # 2. Retrieve relevant long-term context
        relevant_memories = self.long_term.retrieve_by_topic("general")
        
        # 3. Combine contexts
        context = {
            "recent": self.short_term.get_all(),
            "background": relevant_memories
        }
        
        # 4. Process with an LLM using the combined context
        response = "Agent response"
        
        # 5. Add the response to recent context
        self.short_term.add_assistant_message(response)
        
        # 6. If the conversation reaches the limit, summarize and store
        if len(self.short_term.get_all()) >= 20:
            summary = self._summarize_conversation()  # Use an LLM
            self.long_term.store(
                content=summary,
                metadata={"topic": "general", "importance": "medium"}
            )
            self.short_term.clear()
        
        return response
    
    def _summarize_conversation(self) -> str:
        # Use an LLM to summarize the recent messages
        messages = self.short_term.get_all()
        # ... LLM call ...
        return "Conversation summary"
```

---

## Next Steps (Production Evolution)

`LongTermMemory` provides a solid foundation. To scale in production, integrate with:

- **ChromaDB** (local, zero config) - ideal for getting started
- **Pinecone** (cloud, managed) - better performance
- **Weaviate** (open source, hybrid) - flexibility
- **Qdrant** (high performance) - for scale

### Evolution Example: ChromaDB Integration

```python
import chromadb
from typing import List, Dict

class LongTermMemoryWithChroma(LongTermMemory):
    """Extends LongTermMemory with ChromaDB for semantic search."""
    
    def __init__(self, collection_name: str = "memories"):
        super().__init__(collection_name)
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def store(self, content: str, metadata: Optional[Dict] = None) -> str:
        """Stores data locally and in ChromaDB."""
        memory_id = super().store(content, metadata)
        
        # Add to ChromaDB for semantic search
        self.collection.add(
            ids=[memory_id],
            documents=[content],
            metadatas=[metadata or {}]
        )
        
        return memory_id
    
    def retrieve_semantic(self, query: str, n: int = 5) -> List[Dict]:
        """Performs semantic search using embeddings."""
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

## Recommendations by Use Case

| Scenario | Short-term | Long-term | Notes |
|---------|-----------|----------|-------|
| **Chatbot MVP** | ConversationMemory (20 msgs) | LongTermMemory (local) | Simple and sufficient |
| **Production Chatbot** | ConversationMemory (50 msgs) | LongTermMemory + ChromaDB | Add semantic search |
| **Multi-Task Agent** | ConversationMemory (100 msgs) | LongTermMemory + Pinecone | Performance and scale |
| **Personal Assistant** | ConversationMemory (200 msgs) | LongTermMemory + Weaviate | Full user history |

---

## Suggested Pattern: Summarize and Store

1. Use `ConversationMemory` for recent context (last 20 messages)
2. When the limit is reached, **summarize the conversation with an LLM** before storing
3. Store the summary in `LongTermMemory` with metadata (topic, date, importance)
4. In new conversations, retrieve relevant summaries using semantic search
5. Use summaries as a preamble together with recent ConversationMemory

