#!/usr/bin/env python3
"""
🚀 QUICK START - MVP GenAI em 5 minutos

Este arquivo demonstra como usar o template com um exemplo funcional.
Ele inclui tanto chains (simples) quanto agents (com ferramentas).

Para rodar:
  1. Copiar .env.example para .env
  2. Adicionar sua ANTHROPIC_API_KEY em .env
  3. Instalar: pip install -r requirements.txt
  4. Rodar: python QUICK_START.py
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar cliente
client = Anthropic()


# ============================================================================
# EXEMPLO 1: CHAIN SIMPLES (recomendado para MVP inicial)
# ============================================================================
def example_1_simple_chain():
    """
    Chain = Uma chamada ao LLM com prompt estruturado.
    ✅ Rápido
    ✅ Barato
    ✅ Previsível
    """
    print("\n" + "=" * 70)
    print("📝 EXEMPLO 1: CHAIN SIMPLES")
    print("=" * 70)

    from src.core.chains.base_chain import run_chain

    # Prompt simples
    questions = [
        "Qual é a capital do Brasil?",
        "Quanto é 10 + 5?",
        "Me diga um fato interessante sobre Python",
    ]

    for question in questions:
        print(f"\n❓ Pergunta: {question}")
        response = run_chain(
            user_input=question,
            model_client=client,
            variables={
                "domain": "assistência geral",
                "instruction_1": "Seja breve e direto",
                "instruction_2": "Use linguagem clara",
                "output_format": "Texto simples",
            },
        )
        print(f"✅ Resposta: {response[:200]}...")


# ============================================================================
# EXEMPLO 2: AGENT COM FERRAMENTAS (para lógica mais complexa)
# ============================================================================
def example_2_agent_with_tools():
    """
    Agent = ReAct loop que raciocina e executa ferramentas.
    ✅ Pode usar tools
    ✅ Raciocina complexo
    ❌ Mais caro
    ❌ Mais lento
    """
    print("\n" + "=" * 70)
    print("🤖 EXEMPLO 2: AGENT COM FERRAMENTAS")
    print("=" * 70)

    from src.core.agents.base_agent import BaseAgent

    agent = BaseAgent(model_client=client, max_iterations=5)

    tasks = [
        "Qual é a data de hoje?",
        "Busque informações sobre inteligência artificial",
    ]

    for task in tasks:
        print(f"\n🎯 Tarefa: {task}")
        try:
            response = agent.run(task)
            print(f"✅ Resultado: {response[:200]}...")
        except Exception as e:
            print(f"⚠️ Erro: {e}")


# ============================================================================
# EXEMPLO 3: USANDO MEMORY (contexto da conversa)
# ============================================================================
def example_3_with_memory():
    """
    Memory = Manter contexto entre múltiplas chamadas.
    Útil para conversas onde o contexto importa.
    """
    print("\n" + "=" * 70)
    print("💾 EXEMPLO 3: COM MEMÓRIA (Conversas)")
    print("=" * 70)

    from src.core.memory.short_term import ConversationMemory
    from src.core.chains.base_chain import run_chain

    memory = ConversationMemory(max_messages=20)

    # Simular conversa
    exchanges = [
        ("Qual é a melhor linguagem de programação?", "Programação"),
        ("E qual é a mais rápida?", "Programação"),
        ("Me recomende algo para aprender agora", "Aprendizado"),
    ]

    for user_msg, domain in exchanges:
        print(f"\n👤 Usuário: {user_msg}")

        # Adicionar à memória
        memory.add_user_message(user_msg)

        # Gerar resposta (em um sistema real, passaria memory para o LLM)
        response = run_chain(
            user_input=user_msg,
            model_client=client,
            variables={"domain": domain},
        )

        # Adicionar resposta à memória
        memory.add_assistant_message(response[:100])

        print(f"🤖 Assistant: {response[:150]}...")

    # Mostrar histórico
    print(f"\n📋 Histórico ({len(memory.get_all())} mensagens):")
    for msg in memory.get_all():
        print(f"  - {msg['role']}: {msg['content'][:50]}...")


# ============================================================================
# EXEMPLO 4: GUARDRAILS (Segurança)
# ============================================================================
def example_4_with_guardrails():
    """
    Guardrails = Validações de entrada e saída.
    Protege contra inputs inválidos e outputs ruins.
    """
    print("\n" + "=" * 70)
    print("🛡️  EXEMPLO 4: COM GUARDRAILS (Segurança)")
    print("=" * 70)

    from src.core.guardrails.input_guard import validate_input, InputValidationError

    test_inputs = [
        ("Qual é a capital do Brasil?", True),
        ("", False),  # Input vazio
        ("x" * 5000, False),  # Muito longo
    ]

    for input_text, should_pass in test_inputs:
        display_text = input_text[:50] + "..." if len(input_text) > 50 else input_text
        print(f"\n🔍 Validando: '{display_text}'")

        try:
            clean = validate_input(input_text)
            if should_pass:
                print(f"✅ PASSOU: Input válido")
            else:
                print(f"❌ ERRO: Deveria ter falhado!")
        except InputValidationError as e:
            if not should_pass:
                print(f"✅ BLOQUEADO (correto): {e}")
            else:
                print(f"❌ ERRO: Deveria ter passado! {e}")


# ============================================================================
# EXEMPLO 5: PIPELINE COMPLETO (Recomendado para produção)
# ============================================================================
def example_5_complete_pipeline():
    """
    Pipeline = Chain + Memory + Guardrails
    Assim você constrói um MVP robusto.
    """
    print("\n" + "=" * 70)
    print("🏗️  EXEMPLO 5: PIPELINE COMPLETO")
    print("=" * 70)

    from src.core.chains.base_chain import run_chain
    from src.core.memory.short_term import ConversationMemory
    from src.core.guardrails.input_guard import validate_input, InputValidationError
    from src.core.guardrails.output_guard import validate_output

    class SimpleAssistant:
        """Assistente simples com todas as camadas."""

        def __init__(self):
            self.memory = ConversationMemory(max_messages=20)

        def chat(self, user_input: str) -> str:
            # 1. Validar entrada
            try:
                user_input = validate_input(user_input)
            except InputValidationError as e:
                return f"❌ Entrada inválida: {e}"

            # 2. Adicionar à memória
            self.memory.add_user_message(user_input)

            # 3. Processar (chain)
            try:
                response = run_chain(
                    user_input=user_input,
                    model_client=client,
                    variables={"domain": "assistência geral"},
                )
            except Exception as e:
                return f"❌ Erro ao processar: {e}"

            # 4. Validar saída
            response = validate_output(response)

            # 5. Adicionar à memória
            self.memory.add_assistant_message(response)

            return response

    # Usar o assistente
    assistant = SimpleAssistant()

    messages = [
        "Olá! Como você está?",
        "Me diga algo interessante",
        "Obrigado!",
    ]

    for msg in messages:
        print(f"\n👤 Usuário: {msg}")
        response = assistant.chat(msg)
        print(f"🤖 Assistant: {response[:150]}...")


# ============================================================================
# MAIN
# ============================================================================
if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════════╗
║                   🚀 GenAI MVP Template - Quick Start                  ║
║                                                                        ║
║  Este script demonstra 5 padrões de uso do template:                  ║
║  1. Chain Simples (⭐ comece aqui)                                     ║
║  2. Agent com Ferramentas                                              ║
║  3. Com Memória (conversas)                                            ║
║  4. Com Guardrails (segurança)                                         ║
║  5. Pipeline Completo (produção)                                       ║
║                                                                        ║
║  Para rodar: python QUICK_START.py                                    ║
╚════════════════════════════════════════════════════════════════════════╝
    """)

    # Selecionar qual exemplo rodar
    print("\nQual exemplo deseja rodar?")
    print("  1 - Chain Simples (recomendado)")
    print("  2 - Agent com Ferramentas")
    print("  3 - Com Memória")
    print("  4 - Com Guardrails")
    print("  5 - Pipeline Completo")
    print("  a - Todos")

    choice = input("\nEscolha (1-5 ou 'a'): ").strip().lower()

    examples = {
        "1": example_1_simple_chain,
        "2": example_2_agent_with_tools,
        "3": example_3_with_memory,
        "4": example_4_with_guardrails,
        "5": example_5_complete_pipeline,
    }

    if choice == "a":
        for example_fn in examples.values():
            example_fn()
    elif choice in examples:
        examples[choice]()
    else:
        print("❌ Opção inválida!")

    print("\n" + "=" * 70)
    print("✅ Exemplos finalizados!")
    print("=" * 70)
    print("\n📚 Próximos passos:")
    print("  1. Leia QUICK_START_GUIDE.md")
    print("  2. Explore docs/ para documentação completa")
    print("  3. Customize para seu caso de uso")
    print("  4. Adicione suas próprias ferramentas em src/core/tools/")
