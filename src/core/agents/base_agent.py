"""Agente base que pode usar tools e chains como nós."""

import os
from typing import Dict, List, Any, Callable
from dotenv import load_dotenv
from openai import OpenAI

from src.core.chains.base_chain import SimpleChain
from src.core.memory.short_term import ConversationMemory

load_dotenv()


class Agent:
    """
    Agente que decide qual ferramenta ou chain usar.
    Cada decisão é um nó no grafo de execução.
    """
    
    def __init__(self, name: str = "Agent", model: str = "gpt-4o-mini"):
        self.name = name
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.tools: Dict[str, Callable] = {}
        self.chains: Dict[str, Any] = {}
        self.memory = ConversationMemory()
        self.system_prompt = self._default_system_prompt()
    
    def register_tool(self, name: str, func: Callable, description: str):
        """Registra uma ferramenta que o agente pode usar."""
        self.tools[name] = {"func": func, "description": description}
    
    def register_chain(self, name: str, chain: Any, description: str):
        """Registra uma chain que o agente pode executar."""
        self.chains[name] = {"chain": chain, "description": description}
    
    def run(self, user_input: str) -> str:
        """Executa o agente: decide e executa o próximo nó."""
        self.memory.add_user_message(user_input)
        
        # Decide qual ação tomar
        action = self._decide_action(user_input)
        
        # Executa o nó escolhido
        if action["type"] == "tool":
            result = self._execute_tool(action["name"], action["input"])
        elif action["type"] == "chain":
            result = self._execute_chain(action["name"], action["input"])
        else:
            result = self._chat_response(user_input)
        
        self.memory.add_assistant_message(result)
        return result
    
    def _decide_action(self, input: str) -> Dict:
        """Nó de decisão: LLM escolhe o próximo passo."""
        tools_desc = "\n".join([
            f"- {name}: {info['description']}" 
            for name, info in self.tools.items()
        ])
        chains_desc = "\n".join([
            f"- {name}: {info['description']}" 
            for name, info in self.chains.items()
        ])
        
        decision_prompt = f"""
        Você é um agente que decide qual ação tomar.
        
        FERRAMENTAS DISPONÍVEIS:
        {tools_desc if tools_desc else "Nenhuma"}
        
        CHAINS DISPONÍVEIS:
        {chains_desc if chains_desc else "Nenhuma"}
        
        HISTÓRICO RECENTE:
        {self.memory.get_last_n(4)}
        
        ENTRADA DO USUÁRIO: {input}
        
        Responda APENAS com JSON no formato:
        {{"type": "tool" ou "chain" ou "chat", "name": "nome", "input": "parametro"}}
        
        Se for chat simples, use type "chat" com name vazio.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.2,
            messages=[{"role": "user", "content": decision_prompt}]
        )
        
        import json
        content = response.choices[0].message.content
        content = content.replace("```json", "").replace("```", "").strip()
        
        try:
            return json.loads(content)
        except:
            return {"type": "chat", "name": "", "input": input}
    
    def _execute_tool(self, name: str, input: str) -> str:
        """Executa um nó de ferramenta."""
        if name not in self.tools:
            return f"Erro: Ferramenta '{name}' não encontrada"
        try:
            result = self.tools[name]["func"](input)
            return str(result)
        except Exception as e:
            return f"Erro ao executar ferramenta: {e}"
    
    def _execute_chain(self, name: str, input: str) -> str:
        """Executa um nó de chain."""
        if name not in self.chains:
            return f"Erro: Chain '{name}' não encontrada"
        try:
            return self.chains[name]["chain"].run(input)
        except Exception as e:
            return f"Erro ao executar chain: {e}"
    
    def _chat_response(self, input: str) -> str:
        """Nó de fallback: resposta direta do LLM."""
        chain = SimpleChain()
        chain.system_prompt = self.system_prompt
        return chain.run(input)
    
    def _default_system_prompt(self) -> str:
        return f"Você é {self.name}, um assistente útil e objetivo."