"""
Output guardrails — validate the agent response before returning it to the user.
"""


def validate_output(text: str) -> str:
    if not text or not text.strip():
        return "The agent did not produce an answer. Try rephrasing the task."
    return text.strip()
