"""
Input guardrails — validate and sanitize text before sending it to the agent.
"""
MAX_INPUT_LENGTH = 4000


class InputValidationError(ValueError):
    pass


def validate_input(text: str) -> str:
    if not text or not text.strip():
        raise InputValidationError("Input cannot be empty.")
    if len(text) > MAX_INPUT_LENGTH:
        raise InputValidationError(
            f"Input too long ({len(text)} chars). Limit: {MAX_INPUT_LENGTH}."
        )
    return text.strip()
