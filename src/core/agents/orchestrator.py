"""Orquestrador de múltiplos agentes (supervisor pattern)."""

from typing import Dict, List
from src.core.agents.base_agent import Agent


class MultiAgentOrchestrator:
    """
    Gerencia múltiplos agentes especialistas.
    Cada agente é um nó no grafo maior.
    """
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.supervisor = Agent(name="Supervisor")
    
    def register_agent(self, name: str, agent: Agent, description: str):
        """Registra um agente especialista."""
        self.agents[name] = {"agent": agent, "description": description}
    
    def run(self, user_input: str) -> str:
        """Roteia a requisição para o agente mais adequado."""
        # Nó 1: Supervisor decide qual agente usar
        selected = self._select_agent(user_input)
        
        # Nó 2: Agente especialista processa
        result = self.agents[selected]["agent"].run(user_input)
        
        return result
    
    def _select_agent(self, input: str) -> str:
        """LLM decide qual agente especialista chamar."""
        agents_desc = "\n".join([
            f"- {name}: {info['description']}"
            for name, info in self.agents.items()
        ])
        
        prompt = f"""
        Escolha o melhor agente para processar: "{input}"
        
        AGENTES DISPONÍVEIS:
        {agents_desc}
        
        Responda APENAS com o nome do agente.
        """
        
        # Chamada LLM simplificada (use sua implementação real)
        # Por enquanto, fallback para primeiro agente
        return list(self.agents.keys())[0] if self.agents else "default"