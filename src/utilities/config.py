"""Environment configuration for YETI Customizable HTML testing."""
import os
from enum import Enum


class Environment(Enum):
    """Available test environments."""
    YETI_CUSTOMIZER = "https://customize.dev.yeti.com/feature/artboard/configurable.html"


def get_base_url() -> str:
    """
    Get the base URL for YETI Customizer.
    
    Returns:
        str: Base URL for https://customize.dev.yeti.com/feature/artboard/configurable.html
    """
    return Environment.YETI_CUSTOMIZER.value
