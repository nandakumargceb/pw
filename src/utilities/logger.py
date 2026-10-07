"""
Logger utility for the CSV-driven test execution framework.
Provides centralized logging configuration and management.
"""

import logging
import os
from pathlib import Path
from typing import Optional


class FrameworkLogger:
    """
    Centralized logger for the entire framework.
    Handles both file and console logging with configurable levels.
    """

    _instance: Optional["FrameworkLogger"] = None
    _logger: Optional[logging.Logger] = None

    def __new__(cls) -> "FrameworkLogger":
        """Singleton pattern to ensure only one logger instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize the logger if not already initialized."""
        if self._logger is None:
            self._setup_logger()

    @staticmethod
    def _setup_logger() -> None:
        """
        Setup logger with both console and file handlers.
        Creates logs directory if it doesn't exist.
        """
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)

        logger = logging.getLogger("CSV_Framework")
        logger.setLevel(logging.DEBUG)

        # Create formatters
        detailed_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
        )
        console_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        # File handler
        file_handler = logging.FileHandler(logs_dir / "execution.log")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)

        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        FrameworkLogger._logger = logger

    def get_logger(self) -> logging.Logger:
        """
        Get the configured logger instance.

        Returns:
            logging.Logger: The framework logger instance.
        """
        if self._logger is None:
            self._setup_logger()
        return self._logger


def get_logger() -> logging.Logger:
    """
    Get or create the framework logger instance.

    Returns:
        logging.Logger: The framework logger.
    """
    return FrameworkLogger().get_logger()


# Create a module-level logger for convenience
logger = get_logger()
