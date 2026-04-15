"""Base chains para orquestração de LLM no MVP."""

import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class SimpleChain:
    """Chain mais simples possível: prompt -> LLM -> resposta."""
    
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.7):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.temperature = temperature
        self.system_prompt = "Você é um assistente útil e objetivo."
    
    def run(self, user_input: str) -> str:
        """Executa o chain com uma entrada do usuário."""
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content


class StructuredChain:
    """Chain que retorna JSON estruturado (bom para extração de dados)."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
    
    def run(self, user_input: str, output_schema: Dict[str, str]) -> Dict[str, Any]:
        """
        Executa chain com saída estruturada.
        
        Args:
            user_input: Texto do usuário
            output_schema: Ex: {"nome": "string", "idade": "int"}
        """
        schema_desc = "\n".join([f"- {k}: {v}" for k, v in output_schema.items()])
        
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.1,  # Baixo para consistência
            messages=[
                {"role": "system", "content": f"""
                Extraia as informações solicitadas do texto do usuário.
                Responda APENAS com JSON válido, sem explicações.
                
                Schema esperado:
                {schema_desc}
                """},
                {"role": "user", "content": user_input}
            ]
        )
        
        import json
        content = response.choices[0].message.content
        # Limpa possíveis marcações de código
        content = content.replace("```json", "").replace("```", "").strip()
        return json.loads(content)


class RAGChain:
    """Chain com contexto (RAG simples). Para usar com ingest.py."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.context_docs: List[str] = []  # Será populada pelo ingest.py
    
    def add_context(self, documents: List[str]):
        """Adiciona documentos ao contexto do chain."""
        self.context_docs.extend(documents)
    
    def run(self, user_query: str) -> str:
        """Executa chain com contexto aumentado."""
        if not self.context_docs:
            return self._fallback_response(user_query)
        
        # Pega documentos mais relevantes (simples: últimos adicionados)
        # TODO: Substituir por busca por similaridade quando tiver embeddings
        context = "\n\n---\n\n".join(self.context_docs[-3:])
        
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.3,
            messages=[
                {"role": "system", "content": f"""
                Você é um assistente que responde baseado APENAS no contexto fornecido.
                Se a resposta não estiver no contexto, diga "Não encontrei essa informação nos documentos disponíveis."
                
                CONTEXTO:
                {context}
                """},
                {"role": "user", "content": user_query}
            ]
        )
        return response.choices[0].message.content
    
    def _fallback_response(self, query: str) -> str:
        """Resposta quando não há contexto carregado."""
        return "⚠️ Nenhum documento foi carregado. Execute o script ingest.py primeiro."


class ChainBuilder:
    """Factory para criar chains com configurações pré-definidas."""
    
    @staticmethod
    def chatbot() -> SimpleChain:
        """Chain para chat geral."""
        chain = SimpleChain(temperature=0.7)
        chain.system_prompt = "Você é um assistente amigável e conversacional."
        return chain
    
    @staticmethod
    def extrator() -> StructuredChain:
        """Chain para extração de dados."""
        return StructuredChain()
    
    @staticmethod
    def suporte(documentos: List[str]) -> RAGChain:
        """Chain para suporte ao cliente com base em documentos."""
        chain = RAGChain()
        chain.add_context(documentos)
        return chain


# Exemplo de uso direto (para testes rápidos no playground/)
if __name__ == "__main__":
    print("=== Testando SimpleChain ===")
    chat = SimpleChain()
    resposta = chat.run("Explique o que é um MVP em uma frase.")
    print(f"Resposta: {resposta}\n")
    
    print("=== Testando StructuredChain ===")
    extrator = StructuredChain()
    dados = extrator.run(
        "Meu nome é João, tenho 32 anos e sou desenvolvedor.",
        {"nome": "string", "idade": "int", "profissao": "string"}
    )
    print(f"Dados extraídos: {dados}")