"""
Guardrails de entrada — valida e sanitiza o input antes de enviar ao agente.
"""
MAX_INPUT_LENGTH = 4000


class InputValidationError(ValueError):
    pass


def validate_input(text: str) -> str:
    if not text or not text.strip():
        raise InputValidationError("Input nao pode ser vazio.")
    if len(text) > MAX_INPUT_LENGTH:
        raise InputValidationError(
            f"Input muito longo ({len(text)} chars). Limite: {MAX_INPUT_LENGTH}."
        )
    return text.strip()
