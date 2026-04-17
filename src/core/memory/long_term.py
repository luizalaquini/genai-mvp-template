"""Long-term memory for agents with semantic search."""

from typing import List, Dict, Optional
from datetime import datetime


class LongTermMemory:
    """
    Persistent memory storage with semantic search.
    
    Recommended use:
    - Summaries of older conversations
    - Important context for future interactions
    - Agent learning and knowledge retention
    
    Note: This is a baseline implementation. For production use,
    integrate with ChromaDB, Pinecone, or similar.
    """
    
    def __init__(self, collection_name: str = "memories"):
        """
        Initialize long-term memory.
        
        Args:
            collection_name: Name of the collection for organization
        """
        self.collection_name = collection_name
        self._memories: List[Dict] = []
    
    def store(self, content: str, metadata: Optional[Dict] = None) -> str:
        """
        Store a memory entry with metadata.
        
        Args:
            content: Content to store (ideally a summary)
            metadata: Additional information (user, topic, importance, etc.)
        
        Returns:
            Stored memory ID
        """
        memory_id = f"mem_{len(self._memories)}_{int(datetime.now().timestamp())}"
        
        memory_entry = {
            "id": memory_id,
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
            "accessed_count": 0
        }
        
        self._memories.append(memory_entry)
        return memory_id
    
    def retrieve_by_topic(self, topic: str) -> List[Dict]:
        """
        Retrieve memories by topic using simple metadata filtering.
        
        Args:
            topic: Topic to filter by
        
        Returns:
            List of memory entries for the topic
        """
        results = [
            mem for mem in self._memories 
            if mem.get("metadata", {}).get("topic") == topic
        ]
        # Increment access counter
        for mem in results:
            mem["accessed_count"] += 1
        return results
    
    def retrieve_all(self) -> List[Dict]:
        """Retrieve all stored memories."""
        return self._memories.copy()
    
    def retrieve_recent(self, n: int = 10) -> List[Dict]:
        """
        Retrieve the most recent N memories.
        
        Args:
            n: Number of memories to retrieve
        
        Returns:
            Last N memories, most recent first
        """
        return sorted(
            self._memories, 
            key=lambda x: x["timestamp"], 
            reverse=True
        )[:n]
    
    def retrieve_most_accessed(self, n: int = 10) -> List[Dict]:
        """
        Retrieve the most accessed memories.
        
        Args:
            n: Number of memories to retrieve
        
        Returns:
            Most accessed memories (most relevant)
        """
        return sorted(
            self._memories,
            key=lambda x: x["accessed_count"],
            reverse=True
        )[:n]
    
    def update_memory(self, memory_id: str, new_content: str, 
                     new_metadata: Optional[Dict] = None) -> bool:
        """
        Update an existing memory.
        
        Args:
            memory_id: ID of the memory to update
            new_content: New content
            new_metadata: New metadata to merge with existing values
        
        Returns:
            True if updated successfully, False otherwise
        """
        for mem in self._memories:
            if mem["id"] == memory_id:
                mem["content"] = new_content
                if new_metadata:
                    mem["metadata"].update(new_metadata)
                mem["timestamp"] = datetime.now().isoformat()
                return True
        return False
    
    def delete_memory(self, memory_id: str) -> bool:
        """
        Delete a memory.
        
        Args:
            memory_id: ID of the memory to delete
        
        Returns:
            True if deleted successfully, False otherwise
        """
        initial_len = len(self._memories)
        self._memories = [mem for mem in self._memories if mem["id"] != memory_id]
        return len(self._memories) < initial_len
    
    def clear(self):
        """Clear all stored memories."""
        self._memories = []
    
    def get_stats(self) -> Dict:
        """
        Return memory statistics.
        
        Returns:
            Dictionary with storage information
        """
        total_memories = len(self._memories)
        if total_memories == 0:
            return {
                "total_memories": 0,
                "collection": self.collection_name
            }
        
        total_accesses = sum(m.get("accessed_count", 0) for m in self._memories)
        
        return {
            "total_memories": total_memories,
            "total_accesses": total_accesses,
            "avg_accesses_per_memory": total_accesses / total_memories,
            "collection": self.collection_name,
            "oldest_memory": min(m["timestamp"] for m in self._memories),
            "newest_memory": max(m["timestamp"] for m in self._memories)
        }
