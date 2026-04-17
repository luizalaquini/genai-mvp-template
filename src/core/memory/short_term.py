"""Short-term memory for agents."""

from typing import List, Dict
from collections import deque


class ConversationMemory:
    """Circular message buffer for agent context."""
    
    def __init__(self, max_messages: int = 20):
        self.messages: deque = deque(maxlen=max_messages)
    
    def add_user_message(self, content: str):
        self.messages.append({"role": "user", "content": content})
    
    def add_assistant_message(self, content: str):
        self.messages.append({"role": "assistant", "content": content})
    
    def add_system_message(self, content: str):
        self.messages.append({"role": "system", "content": content})
    
    def get_all(self) -> List[Dict]:
        return list(self.messages)
    
    def get_last_n(self, n: int) -> List[Dict]:
        return list(self.messages)[-n:]
    
    def clear(self):
        self.messages.clear()