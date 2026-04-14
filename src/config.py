"""
Central configuration module.

Loads environment variables and exposes typed config objects
to be used across the application.
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


@dataclass
class LLMConfig:
    provider: str
    model: str
    temperature: float
    max_tokens: int


@dataclass
class AppConfig:
    environment: str
    debug: bool


@dataclass
class Config:
    app: AppConfig
    llm: LLMConfig


def get_config() -> Config:
    """
    Factory function to build the application config.
    """

    return Config(
        app=AppConfig(
            environment=os.getenv("ENVIRONMENT", "development"),
            debug=os.getenv("DEBUG", "true").lower() == "true",
        ),
        llm=LLMConfig(
            provider=os.getenv("LLM_PROVIDER", "openai"),
            model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
            temperature=float(os.getenv("LLM_TEMPERATURE", 0.7)),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", 500)),
        ),
    )


# Singleton-like access (optional but practical)
config = get_config()