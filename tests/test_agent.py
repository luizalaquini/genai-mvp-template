"""Base agent tests."""
from unittest.mock import MagicMock
from src.core.agents.base_agent import BaseAgent
from src.core.guardrails.input_guard import validate_input, InputValidationError
import pytest


def test_validate_input_ok():
    assert validate_input("Hello, how are you?") == "Hello, how are you?"


def test_validate_input_empty():
    with pytest.raises(InputValidationError):
        validate_input("")


def test_validate_input_too_long():
    with pytest.raises(InputValidationError):
        validate_input("x" * 5000)


def test_agent_uses_memory():
    mock_client = MagicMock()
    agent = BaseAgent(model_client=mock_client, max_iterations=1)
    assert len(agent.memory) == 0
