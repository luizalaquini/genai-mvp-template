"""
Guardrails de saida — valida a resposta do agente antes de retornar ao usuario.
"""


def validate_output(text: str) -> str:
    if not text or not text.strip():
        return "O agente nao produziu uma resposta. Tente reformular a tarefa."
    return text.strip()
