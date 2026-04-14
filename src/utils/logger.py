"""
Centralized logging configuration.

Uses Loguru for structured and easy-to-use logging across the project.
"""

import sys
from loguru import logger
from src.config import config


def setup_logger():
    """
    Configure global logger.
    """

    # Remove default logger
    logger.remove()

    log_level = "DEBUG" if config.app.debug else "INFO"

    # Console logger
    logger.add(
        sys.stdout,
        level=log_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
    )

    # File logger (optional but recommended)
    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="7 days",
        level=log_level,
        format="{time} | {level} | {message}",
    )


# Initialize logger on import (simple approach for MVPs)
setup_logger()