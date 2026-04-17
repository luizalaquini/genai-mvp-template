"""
Agente base com loop ReAct (Reason + Act).

Fluxo:
  1. Recebe task
  2. Raciocina qual tool usar (ou se ja tem a resposta)
  3. Executa a tool
  4. Observa o resultado
  5. Repete ate concluir ou atingir max_iterations
"""
import json
from src.core.memory.buffer_memory import BufferMemory
from src.core.tools.registry import TOOL_REGISTRY, TOOL_DEFINITIONS
from src.core.guardrails.input_guard import validate_input


class BaseAgent:
    def __init__(self, model_client, max_iterations: int = 10):
        self.client = model_client
        self.max_iterations = max_iterations
        self.memory = BufferMemory()

    def run(self, task: str) -> str:
        task = validate_input(task)
        self.memory.add("user", task)

        for i in range(self.max_iterations):
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                system=self._system_prompt(),
                tools=TOOL_DEFINITIONS,
                messages=self.memory.get_messages(),
            )

            # Agente concluiu sem chamar tool
            if response.stop_reason == "end_turn":
                answer = response.content[0].text
                self.memory.add("assistant", answer)
                return answer

            # Processa tool calls
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = self._execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(result),
                    })

            self.memory.add("assistant", response.content)
            self.memory.add("user", tool_results)

        return "Limite de iteracoes atingido sem conclusao."

    def _execute_tool(self, name: str, inputs: dict):
        fn = TOOL_REGISTRY.get(name)
        if not fn:
            return f"Tool '{name}' nao encontrada."
        try:
            return fn(**inputs)
        except Exception as e:
            return f"Erro ao executar '{name}': {e}"

    def _system_prompt(self) -> str:
        return (
            "Voce e um agente que resolve tarefas passo a passo. "
            "Use as ferramentas disponiveis quando necessario. "
            "Quando tiver a resposta final, responda diretamente sem chamar ferramentas."
        )


if __name__ == "__main__":
    import argparse, anthropic
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True)
    args = parser.parse_args()

    client = anthropic.Anthropic()
    agent = BaseAgent(model_client=client)
    print(agent.run(args.task))
