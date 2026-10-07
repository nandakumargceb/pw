"""
Configuration manager for the CSV-driven test execution framework.
Loads and manages environment and framework configurations from YAML.
"""

import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from src.utilities.logger import get_logger


class ConfigManager:
    """
    Manages framework configuration from config.yaml.
    Supports multiple environments: SIT, UAT, PROD.
    """

    _instance: Optional["ConfigManager"] = None
    _config: Dict[str, Any] = {}

    def __new__(cls) -> "ConfigManager":
        """Singleton pattern to ensure only one config instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize the config manager and load configuration."""
        if not self._config:
            self._load_config()

    def _load_config(self) -> None:
        """
        Load configuration from config.yaml file.
        Validates that the file exists and contains required fields.

        Raises:
            FileNotFoundError: If config.yaml is not found.
            ValueError: If environment is not properly configured.
        """
        logger = get_logger()
        config_path = Path("config/config.yaml")

        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_path.absolute()}"
            )

        try:
            with open(config_path, "r", encoding="utf-8") as config_file:
                self._config = yaml.safe_load(config_file)
                logger.info(f"Configuration loaded from {config_path}")
        except yaml.YAMLError as e:
            logger.error(f"Error parsing config.yaml: {e}")
            raise

        self._validate_config()

    def _validate_config(self) -> None:
        """
        Validate that the configuration contains all required fields.

        Raises:
            ValueError: If required configuration fields are missing.
        """
        logger = get_logger()
        required_fields = ["environment"]

        for field in required_fields:
            if field not in self._config:
                raise ValueError(f"Missing required configuration field: {field}")

        environment = self._config.get("environment")
        valid_environments = ["SIT", "UAT", "PROD"]

        if environment not in valid_environments:
            raise ValueError(
                f"Invalid environment '{environment}'. "
                f"Must be one of: {', '.join(valid_environments)}"
            )

        logger.info(f"Configuration validated successfully. Environment: {environment}")

    def get_environment(self) -> str:
        """
        Get the configured environment.

        Returns:
            str: The environment name (SIT, UAT, or PROD).
        """
        return self._config.get("environment", "SIT")

    def get_logging_config(self) -> Dict[str, Any]:
        """
        Get logging configuration.

        Returns:
            Dict[str, Any]: Logging configuration parameters.
        """
        return self._config.get("logging", {})

    def get_framework_config(self) -> Dict[str, Any]:
        """
        Get framework configuration.

        Returns:
            Dict[str, Any]: Framework configuration parameters.
        """
        return self._config.get("framework", {})

    def get_data_format(self) -> str:
        """
        Get the active test-data format.

        Returns:
            str: The configured format, typically 'csv' or 'yaml'.
        """
        framework_config = self.get_framework_config()
        return str(framework_config.get("data_format", "csv")).lower()

    def get_csv_encoding(self) -> str:
        """
        Get CSV file encoding.

        Returns:
            str: The encoding to use when reading/writing CSV files.
        """
        framework_config = self.get_framework_config()
        return framework_config.get("csv_encoding", "utf-8")

    def get_yaml_encoding(self) -> str:
        """
        Get YAML file encoding.

        Returns:
            str: The encoding to use when reading/writing YAML files.
        """
        framework_config = self.get_framework_config()
        return framework_config.get("yaml_encoding", "utf-8")

    def get_auto_skip_disabled(self) -> bool:
        """
        Check if disabled tests should be auto-skipped.

        Returns:
            bool: True if disabled tests should be auto-skipped.
        """
        framework_config = self.get_framework_config()
        return framework_config.get("auto_skip_disabled", True)

    def get_log_csv_operations(self) -> bool:
        """
        Check if CSV operations should be logged.

        Returns:
            bool: True if CSV operations should be logged.
        """
        framework_config = self.get_framework_config()
        return framework_config.get("log_csv_operations", True)


def get_config() -> ConfigManager:
    """
    Get or create the config manager instance.

    Returns:
        ConfigManager: The configuration manager.
    """
    return ConfigManager()
