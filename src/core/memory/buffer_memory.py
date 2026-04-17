"""
Memoria de curto prazo — janela deslizante de mensagens.
"""


class BufferMemory:
    def __init__(self, max_messages: int = 20):
        self._messages: list[dict] = []
        self.max_messages = max_messages

    def add(self, role: str, content):
        self._messages.append({"role": role, "content": content})
        # Mantem apenas as ultimas N mensagens (preserva a primeira)
        if len(self._messages) > self.max_messages:
            self._messages = self._messages[-self.max_messages:]

    def get_messages(self) -> list[dict]:
        return self._messages.copy()

    def clear(self):
        self._messages = []

    def __len__(self):
        return len(self._messages)
