"""
YAML manager for reading and writing test data.
Handles all YAML operations with validation and error handling.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from src.utilities.config_manager import get_config
from src.utilities.logger import get_logger


class YAMLManager:
    """
    Manages YAML-based test data files.
    Supports reading, writing, and validation of environment-specific YAML sheets.
    """

    def __init__(self) -> None:
        """Initialize the YAML manager."""
        self.logger = get_logger()
        self.config = get_config()
        self.encoding = self.config.get_yaml_encoding()
        self.current_yaml_file: Optional[Path] = None
        self._validate_test_data_folder()

    def _validate_test_data_folder(self) -> None:
        """Validate that the Test_Data folder exists."""
        test_data_path = Path("Test_Data")
        if not test_data_path.exists():
            raise FileNotFoundError(
                f"Test_Data folder not found at {test_data_path.absolute()}"
            )
        self.logger.info(f"Test_Data folder validated at {test_data_path.absolute()}")

    def get_environment_yaml_path(self, yaml_path: Optional[Path] = None) -> Path:
        """Get the YAML file path for the current environment."""
        if yaml_path is not None:
            target_path = Path(yaml_path)
        else:
            environment = self.config.get_environment()
            for suffix in (".yaml", ".yml"):
                candidate = Path("Test_Data") / f"{environment}{suffix}"
                if candidate.exists():
                    target_path = candidate
                    break
            else:
                target_path = Path("Test_Data") / f"{environment}.yaml"

        if not target_path.exists():
            raise FileNotFoundError(
                f"YAML file not found: {target_path.absolute()}"
            )

        self.logger.info(f"Using YAML file: {target_path.absolute()}")
        return target_path

    def _normalize_rows(self, data: Any) -> List[Dict[str, Any]]:
        """Normalize YAML content into a list of row dictionaries."""
        if isinstance(data, list):
            rows = data
        elif isinstance(data, dict):
            if "test_cases" in data and isinstance(data["test_cases"], list):
                rows = data["test_cases"]
            elif "rows" in data and isinstance(data["rows"], list):
                rows = data["rows"]
            else:
                rows = [data]
        else:
            raise ValueError("YAML data must be a list or mapping of test cases")

        normalized_rows: List[Dict[str, Any]] = []
        for row in rows:
            if not isinstance(row, dict):
                raise ValueError("Each YAML row must be a dictionary")
            normalized_rows.append({str(key): value for key, value in row.items()})
        return normalized_rows

    def read_all_rows(self, yaml_path: Optional[Path] = None) -> List[Dict[str, Any]]:
        """Read all rows from an environment-specific YAML file."""
        target_path = self.get_environment_yaml_path(yaml_path)
        self.current_yaml_file = target_path

        try:
            with open(target_path, "r", encoding=self.encoding) as file:
                payload = yaml.safe_load(file) or []

            rows = self._normalize_rows(payload)
            self._validate_yaml_structure(rows[0].keys() if rows else [])

            self.logger.info(f"Read {len(rows)} rows from {target_path.name}")
            return rows
        except yaml.YAMLError as exc:
            self.logger.error(f"YAML read error in {target_path}: {exc}")
            raise ValueError(f"Invalid YAML format: {exc}") from exc
        except Exception as exc:
            self.logger.error(f"Error reading YAML file {target_path}: {exc}")
            raise

    def _validate_yaml_structure(self, fieldnames: List[str]) -> None:
        """Validate that YAML has required columns."""
        required_columns = {"Test_Case_Name", "Execute"}
        missing_columns = required_columns - set(fieldnames)

        if missing_columns:
            raise ValueError(
                f"YAML is missing required columns: {', '.join(missing_columns)}"
            )

        self.logger.debug(f"YAML structure validated. Columns: {', '.join(fieldnames)}")

    def read_executable_rows(self, yaml_path: Optional[Path] = None) -> List[Dict[str, Any]]:
        """Read only rows marked with Execute='Yes'."""
        all_rows = self.read_all_rows(yaml_path)
        executable_rows = [
            row for row in all_rows if str(row.get("Execute", "")).strip().upper() == "YES"
        ]

        self.logger.info(
            f"Found {len(executable_rows)} executable rows out of {len(all_rows)} total"
        )
        return executable_rows

    def get_rows_by_test_name(
        self, test_name: str, yaml_path: Optional[Path] = None
    ) -> List[Dict[str, Any]]:
        """Get all executable rows for a specific test name."""
        executable_rows = self.read_executable_rows(yaml_path)
        matching_rows = [
            row for row in executable_rows if str(row.get("Test_Case_Name", "")).strip() == test_name
        ]

        self.logger.debug(
            f"Found {len(matching_rows)} executable row(s) for test: {test_name}"
        )
        return matching_rows

    def update_cell(
        self,
        test_name: str,
        column_name: str,
        value: Any,
        row_index: int = 0,
        yaml_path: Optional[Path] = None,
    ) -> None:
        """Update a specific cell in the YAML test data file."""
        target_path = self.get_environment_yaml_path(yaml_path)
        rows = self.read_all_rows(target_path)

        fieldnames = list(rows[0].keys()) if rows else []
        if not fieldnames:
            raise ValueError(f"YAML file {target_path} is empty")

        if column_name not in fieldnames:
            raise ValueError(
                f"Column '{column_name}' not found in YAML. "
                f"Available columns: {', '.join(fieldnames)}"
            )

        matching_indices = [
            i
            for i, row in enumerate(rows)
            if str(row.get("Test_Case_Name", "")).strip() == test_name
            and str(row.get("Execute", "")).strip().upper() == "YES"
        ]

        if not matching_indices:
            raise ValueError(f"No executable rows found for test: {test_name}")

        if row_index >= len(matching_indices):
            raise ValueError(
                f"Row index {row_index} out of range. "
                f"Only {len(matching_indices)} row(s) found for test: {test_name}"
            )

        target_index = matching_indices[row_index]
        rows[target_index][column_name] = value
        payload = {"test_cases": rows}

        with open(target_path, "w", encoding=self.encoding) as file:
            yaml.safe_dump(payload, file, sort_keys=False, default_flow_style=False)

        if self.config.get_log_csv_operations():
            self.logger.info(
                f"Updated YAML: {test_name}[{row_index}].{column_name} = {value}"
            )

    def validate_yaml_file(self, yaml_path: Path) -> bool:
        """Validate a YAML file structure without reading all data."""
        if not yaml_path.exists():
            raise FileNotFoundError(f"YAML file not found: {yaml_path}")

        try:
            with open(yaml_path, "r", encoding=self.encoding) as file:
                data = yaml.safe_load(file) or []
            rows = self._normalize_rows(data)
            if not rows:
                raise ValueError("YAML file is empty")
            self._validate_yaml_structure(list(rows[0].keys()))
            self.logger.info(f"YAML file validated: {yaml_path.name}")
            return True
        except Exception as exc:
            self.logger.error(f"YAML validation failed for {yaml_path}: {exc}")
            raise


def get_yaml_manager() -> YAMLManager:
    """Get a new instance of the YAML manager."""
    return YAMLManager()
