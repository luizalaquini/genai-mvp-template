#!/usr/bin/env python3
"""
🚀 QUICK START - GenAI MVP in 5 minutes

This file demonstrates how to use the template with working examples.
It includes both chains (simple) and agents (with tools).

To run:
  1. Copy .env.example to .env
  2. Add your ANTHROPIC_API_KEY in .env
  3. Install: pip install -r requirements.txt
  4. Run: python QUICK_START.py
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv()

# Initialize client
client = Anthropic()


# ============================================================================
# EXAMPLE 1: SIMPLE CHAIN (recommended for initial MVP)
# ============================================================================
def example_1_simple_chain():
    """
    Chain = one LLM call with a structured prompt.
    ✅ Fast
    ✅ Cheap
    ✅ Predictable
    """
    print("\n" + "=" * 70)
    print("📝 EXAMPLE 1: SIMPLE CHAIN")
    print("=" * 70)

    from src.core.chains.base_chain import run_chain

    questions = [
        "What is the capital of Brazil?",
        "What is 10 + 5?",
        "Tell me an interesting fact about Python",
    ]

    for question in questions:
        print(f"\n❓ Question: {question}")
        response = run_chain(
            user_input=question,
            model_client=client,
            variables={
                "domain": "general assistance",
                "instruction_1": "Be brief and direct",
                "instruction_2": "Use clear language",
                "output_format": "Plain text",
            },
        )
        print(f"✅ Answer: {response[:200]}...")


# ============================================================================
# EXAMPLE 2: AGENT WITH TOOLS (for more complex reasoning)
# ============================================================================
def example_2_agent_with_tools():
    """
    Agent = ReAct loop that reasons and executes tools.
    ✅ Can use tools
    ✅ Handles complex reasoning
    ❌ More expensive
    ❌ Slower
    """
    print("\n" + "=" * 70)
    print("🤖 EXAMPLE 2: AGENT WITH TOOLS")
    print("=" * 70)

    from src.core.agents.base_agent import BaseAgent

    agent = BaseAgent(model_client=client, max_iterations=5)

    tasks = [
        "What is today's date?",
        "Search for information about artificial intelligence",
    ]

    for task in tasks:
        print(f"\n🎯 Task: {task}")
        try:
            response = agent.run(task)
            print(f"✅ Result: {response[:200]}...")
        except Exception as e:
            print(f"⚠️ Error: {e}")


# ============================================================================
# EXAMPLE 3: USING MEMORY (conversation context)
# ============================================================================
def example_3_with_memory():
    """
    Memory = keep context across multiple calls.
    Useful for conversations where context matters.
    """
    print("\n" + "=" * 70)
    print("💾 EXAMPLE 3: WITH MEMORY (Conversations)")
    print("=" * 70)

    from src.core.memory.short_term import ConversationMemory
    from src.core.chains.base_chain import run_chain

    memory = ConversationMemory(max_messages=20)

    exchanges = [
        ("What is the best programming language?", "programming"),
        ("Which language is the fastest?", "programming"),
        ("Recommend something to learn now", "learning"),
    ]

    for user_msg, domain in exchanges:
        print(f"\n👤 User: {user_msg}")

        memory.add_user_message(user_msg)

        response = run_chain(
            user_input=user_msg,
            model_client=client,
            variables={"domain": domain},
        )

        memory.add_assistant_message(response[:100])
        print(f"🤖 Assistant: {response[:150]}...")

    print(f"\n📋 History ({len(memory.get_all())} messages):")
    for msg in memory.get_all():
        print(f"  - {msg['role']}: {msg['content'][:50]}...")


# ============================================================================
# EXAMPLE 4: GUARDRAILS (Safety)
# ============================================================================
def example_4_with_guardrails():
    """
    Guardrails = input and output validation.
    Protects against invalid inputs and bad outputs.
    """
    print("\n" + "=" * 70)
    print("🛡️  EXAMPLE 4: WITH GUARDRAILS (Safety)")
    print("=" * 70)

    from src.core.guardrails.input_guard import validate_input, InputValidationError

    test_inputs = [
        ("What is the capital of Brazil?", True),
        ("", False),
        ("x" * 5000, False),
    ]

    for input_text, should_pass in test_inputs:
        display_text = input_text[:50] + "..." if len(input_text) > 50 else input_text
        print(f"\n🔍 Validating: '{display_text}'")

        try:
            clean = validate_input(input_text)
            if should_pass:
                print("✅ PASSED: Valid input")
            else:
                print("❌ ERROR: This should have failed!")
        except InputValidationError as e:
            if not should_pass:
                print(f"✅ BLOCKED (expected): {e}")
            else:
                print(f"❌ ERROR: This should have passed! {e}")


# ============================================================================
# EXAMPLE 5: COMPLETE PIPELINE (Recommended for production)
# ============================================================================
def example_5_complete_pipeline():
    """
    Pipeline = Chain + Memory + Guardrails
    This builds a more robust MVP.
    """
    print("\n" + "=" * 70)
    print("🏗️  EXAMPLE 5: COMPLETE PIPELINE")
    print("=" * 70)

    from src.core.chains.base_chain import run_chain
    from src.core.memory.short_term import ConversationMemory
    from src.core.guardrails.input_guard import validate_input, InputValidationError
    from src.core.guardrails.output_guard import validate_output

    class SimpleAssistant:
        """Simple assistant with all layers."""

        def __init__(self):
            self.memory = ConversationMemory(max_messages=20)

        def chat(self, user_input: str) -> str:
            try:
                user_input = validate_input(user_input)
            except InputValidationError as e:
                return f"❌ Invalid input: {e}"

            self.memory.add_user_message(user_input)

            try:
                response = run_chain(
                    user_input=user_input,
                    model_client=client,
                    variables={"domain": "general assistance"},
                )
            except Exception as e:
                return f"❌ Processing error: {e}"

            response = validate_output(response)
            self.memory.add_assistant_message(response)
            return response

    assistant = SimpleAssistant()

    messages = [
        "Hello! How are you?",
        "Tell me something interesting",
        "Thank you!",
    ]

    for msg in messages:
        print(f"\n👤 User: {msg}")
        response = assistant.chat(msg)
        print(f"🤖 Assistant: {response[:150]}...")


# ============================================================================
# MAIN
# ============================================================================
if __name__ == "__main__":
    print('''
╔════════════════════════════════════════════════════════════════════════╗
║                   🚀 GenAI MVP Template - Quick Start                  ║
║                                                                        ║
║  This script demonstrates 5 usage patterns for the template:           ║
║  1. Simple Chain (⭐ start here)                                       ║
║  2. Agent with Tools                                                  ║
║  3. With Memory (conversations)                                       ║
║  4. With Guardrails (safety)                                          ║
║  5. Complete Pipeline (production)                                    ║
║                                                                        ║
║  Run with: python QUICK_START.py                                      ║
╚════════════════════════════════════════════════════════════════════════╝
    ''')

    print("\nWhich example would you like to run?")
    print("  1 - Simple Chain (recommended)")
    print("  2 - Agent with Tools")
    print("  3 - With Memory")
    print("  4 - With Guardrails")
    print("  5 - Complete Pipeline")
    print("  a - All")

    choice = input("\nChoose (1-5 or 'a'): ").strip().lower()

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
        print("❌ Invalid option!")

    print("\n" + "=" * 70)
    print("✅ Examples completed!")
    print("=" * 70)
    print("\n📚 Next steps:")
    print("  1. Read the main README")
    print("  2. Explore docs/ for complete documentation")
    print("  3. Customize for your use case")
    print("  4. Add your own tools in src/core/tools/")
