"""Memória de longo prazo para agentes com busca semântica."""

from typing import List, Dict, Optional
from datetime import datetime


class LongTermMemory:
    """
    Armazenamento persistente de memórias com busca semântica.
    
    Uso recomendado:
    - Resumos de conversas antigas
    - Contexto importante para futuras interações
    - Aprendizados do agente
    
    Nota: Esta é uma implementação de base. Para usar em produção,
    integre com ChromaDB, Pinecone ou similar.
    """
    
    def __init__(self, collection_name: str = "memories"):
        """
        Inicializa a memória de longo prazo.
        
        Args:
            collection_name: Nome da coleção (para organização)
        """
        self.collection_name = collection_name
        self._memories: List[Dict] = []
    
    def store(self, content: str, metadata: Optional[Dict] = None) -> str:
        """
        Armazena uma memória com metadados.
        
        Args:
            content: Conteúdo a ser armazenado (idealmente um resumo)
            metadata: Informações adicionais (usuário, tópico, importância, etc)
        
        Returns:
            ID da memória armazenada
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
        Recupera memórias por tópico (busca simples em metadata).
        
        Args:
            topic: Tópico para filtrar
        
        Returns:
            Lista de memórias relacionadas ao tópico
        """
        results = [
            mem for mem in self._memories 
            if mem.get("metadata", {}).get("topic") == topic
        ]
        # Incrementa contador de acesso
        for mem in results:
            mem["accessed_count"] += 1
        return results
    
    def retrieve_all(self) -> List[Dict]:
        """Recupera todas as memórias armazenadas."""
        return self._memories.copy()
    
    def retrieve_recent(self, n: int = 10) -> List[Dict]:
        """
        Recupera as N memórias mais recentes.
        
        Args:
            n: Número de memórias a recuperar
        
        Returns:
            Últimas N memórias (mais recentes primeiro)
        """
        return sorted(
            self._memories, 
            key=lambda x: x["timestamp"], 
            reverse=True
        )[:n]
    
    def retrieve_most_accessed(self, n: int = 10) -> List[Dict]:
        """
        Recupera as memórias mais acessadas.
        
        Args:
            n: Número de memórias a recuperar
        
        Returns:
            Memórias mais acessadas (mais relevantes)
        """
        return sorted(
            self._memories,
            key=lambda x: x["accessed_count"],
            reverse=True
        )[:n]
    
    def update_memory(self, memory_id: str, new_content: str, 
                     new_metadata: Optional[Dict] = None) -> bool:
        """
        Atualiza uma memória existente.
        
        Args:
            memory_id: ID da memória a atualizar
            new_content: Novo conteúdo
            new_metadata: Novos metadados (merge com existentes)
        
        Returns:
            True se atualizado com sucesso, False caso contrário
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
        Deleta uma memória.
        
        Args:
            memory_id: ID da memória a deletar
        
        Returns:
            True se deletado com sucesso, False caso contrário
        """
        initial_len = len(self._memories)
        self._memories = [mem for mem in self._memories if mem["id"] != memory_id]
        return len(self._memories) < initial_len
    
    def clear(self):
        """Limpa todas as memórias armazenadas."""
        self._memories = []
    
    def get_stats(self) -> Dict:
        """
        Retorna estatísticas da memória.
        
        Returns:
            Dicionário com informações sobre o armazenamento
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
