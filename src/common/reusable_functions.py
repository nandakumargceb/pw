"""
Reusable functions for the CSV/YAML-driven test execution framework.
Provides Read_Test_Data and Write_Test_Data helpers for tests.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

from src.utilities.csv_manager import get_data_manager
from src.utilities.execution_context import get_execution_context
from src.utilities.logger import get_logger
from src.utilities.yaml_manager import get_yaml_manager


def Read_Test_Data(column_name: str) -> Optional[Any]:
    """
    Read data from the currently executing test row.

    This function retrieves data from the current test's row in the active CSV or YAML sheet.
    Must be called from within a test function that's being executed by the framework.
    """
    logger = get_logger()
    context = get_execution_context()

    try:
        value = context.get_cell_value(column_name)
        logger.debug(f"Read from current data sheet: {column_name} = {value}")
        return value
    except RuntimeError as e:
        logger.error(str(e))
        raise
    except Exception as e:
        logger.error(f"Error reading test data for column '{column_name}': {e}")
        raise


def Write_Test_Data(column_name: str, value: Any) -> None:
    """
    Update the currently executing test row with new data.

    This function writes data back to the active CSV or YAML file.
    """
    logger = get_logger()
    context = get_execution_context()
    data_manager = get_data_manager()

    try:
        context.set_cell_value(column_name, value)

        current_row = context.get_current_row()
        if current_row is None:
            raise RuntimeError("No execution context available")

        test_name = current_row.get("Test_Case_Name")
        if not test_name:
            raise ValueError("Test_Case_Name not found in execution context")

        data_manager.update_cell(test_name, column_name, value, row_index=0)
        logger.debug(f"Written to data sheet: {column_name} = {value}")

    except RuntimeError as e:
        logger.error(str(e))
        raise
    except Exception as e:
        logger.error(f"Error writing test data for column '{column_name}': {e}")
        raise


def extract_yaml_data(
    test_name: Optional[str] = None, file_path: Optional[Path] = None
) -> List[Dict[str, Any]]:
    """Extract data rows from a YAML sheet, optionally filtering by test name."""
    yaml_manager = get_yaml_manager()
    rows = yaml_manager.read_all_rows(file_path)

    if test_name is not None:
        return [
            row
            for row in rows
            if str(row.get("Test_Case_Name", "")).strip() == test_name
        ]
    return rows


def update_yaml_data(
    test_name: str,
    column_name: str,
    value: Any,
    row_index: int = 0,
    file_path: Optional[Path] = None,
) -> None:
    """Update a cell in a YAML sheet using the same semantics as CSV updates."""
    yaml_manager = get_yaml_manager()
    yaml_manager.update_cell(test_name, column_name, value, row_index=row_index, yaml_path=file_path)


def Read_YAML_Test_Data(column_name: str) -> Optional[Any]:
    """Read data from the current YAML row using the execution context."""
    return Read_Test_Data(column_name)


def Read_Yaml_Test_Data(column_name: str) -> Optional[Any]:
    """Compatibility alias for YAML reads using the common CamelCase naming style."""
    return Read_Test_Data(column_name)


def Write_YAML_Test_Data(column_name: str, value: Any) -> None:
    """Write data back to the current YAML row using the execution context."""
    Write_Test_Data(column_name, value)


def Write_Yaml_Test_Data(column_name: str, value: Any) -> None:
    """Compatibility alias for YAML writes using the common CamelCase naming style."""
    Write_Test_Data(column_name, value)


# Alias functions for convenience
def get_test_data(column_name: str) -> Optional[Any]:
    """Alias for Read_Test_Data."""
    return Read_Test_Data(column_name)


def set_test_data(column_name: str, value: Any) -> None:
    """Alias for Write_Test_Data."""
    Write_Test_Data(column_name, value)


def get_yaml_test_data(column_name: str) -> Optional[Any]:
    """Alias for Read_YAML_Test_Data."""
    return Read_YAML_Test_Data(column_name)


def set_yaml_test_data(column_name: str, value: Any) -> None:
    """Alias for Write_YAML_Test_Data."""
    Write_YAML_Test_Data(column_name, value)


def get_yaml_data(column_name: str) -> Optional[Any]:
    """Alias for Read_Yaml_Test_Data."""
    return Read_Yaml_Test_Data(column_name)


def set_yaml_data(column_name: str, value: Any) -> None:
    """Alias for Write_Yaml_Test_Data."""
    Write_Yaml_Test_Data(column_name, value)
