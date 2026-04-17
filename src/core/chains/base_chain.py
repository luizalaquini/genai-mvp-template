"""
Linear pipeline (no autonomous loop).
Use when the flow is predictable: prompt -> LLM -> response.
"""
from pathlib import Path


def load_prompt(name: str) -> str:
    path = Path(__file__).parent.parent / "prompts" / f"{name}.txt"
    return path.read_text(encoding="utf-8")


def run_chain(user_input: str, model_client, variables: dict = {}, model: str = "claude-3-5-sonnet-20241022") -> str:
    template = load_prompt("base_prompt")
    prompt = template.format(**variables)
    response = model_client.messages.create(
        model=model,
        max_tokens=2048,
        system=prompt,
        messages=[{"role": "user", "content": user_input}],
    )
    return response.content[0].text
