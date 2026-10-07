"""
CSV manager for reading and writing test data.
Handles all CSV operations with validation and error handling.
"""

import csv
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from src.utilities.logger import get_logger
from src.utilities.config_manager import get_config


class CSVManager:
    """
    Manages CSV operations for test data management.
    Supports reading, writing, and validation of test data CSV files.
    """

    def __init__(self) -> None:
        """Initialize the CSV manager."""
        self.logger = get_logger()
        self.config = get_config()
        self.encoding = self.config.get_csv_encoding()
        self.current_csv_file: Optional[Path] = None
        self._validate_test_data_folder()

    def _validate_test_data_folder(self) -> None:
        """
        Validate that the Test_Data folder exists.

        Raises:
            FileNotFoundError: If Test_Data folder doesn't exist.
        """
        test_data_path = Path("Test_Data")
        if not test_data_path.exists():
            raise FileNotFoundError(
                f"Test_Data folder not found at {test_data_path.absolute()}"
            )
        self.logger.info(f"Test_Data folder validated at {test_data_path.absolute()}")

    def get_environment_csv_path(self) -> Path:
        """
        Get the CSV file path for the current environment.

        Returns:
            Path: Path to the environment-specific CSV file.

        Raises:
            FileNotFoundError: If the environment CSV file doesn't exist.
        """
        environment = self.config.get_environment()
        csv_path = Path("Test_Data") / f"{environment}.csv"

        if not csv_path.exists():
            raise FileNotFoundError(
                f"CSV file for environment '{environment}' not found: {csv_path.absolute()}"
            )

        self.logger.info(f"Using CSV file: {csv_path.absolute()}")
        return csv_path

    def read_all_rows(self) -> List[Dict[str, str]]:
        """
        Read all rows from the environment-specific CSV file.

        Returns:
            List[Dict[str, str]]: List of dictionaries containing row data.

        Raises:
            FileNotFoundError: If CSV file doesn't exist.
            ValueError: If CSV has invalid structure.
        """
        csv_path = self.get_environment_csv_path()
        self.current_csv_file = csv_path

        rows = []
        try:
            with open(csv_path, "r", encoding=self.encoding, newline="") as file:
                csv_reader = csv.DictReader(file)

                if csv_reader.fieldnames is None:
                    raise ValueError(f"CSV file {csv_path} is empty or has no headers")

                self._validate_csv_structure(csv_reader.fieldnames)

                for row_num, row in enumerate(csv_reader, start=2):
                    rows.append(row)

            self.logger.info(f"Read {len(rows)} rows from {csv_path.name}")
            return rows

        except csv.Error as e:
            self.logger.error(f"CSV read error in {csv_path}: {e}")
            raise ValueError(f"Invalid CSV format: {e}") from e
        except Exception as e:
            self.logger.error(f"Error reading CSV file {csv_path}: {e}")
            raise

    def _validate_csv_structure(self, fieldnames: List[str]) -> None:
        """
        Validate that CSV has required columns.

        Args:
            fieldnames (List[str]): The column names from CSV header.

        Raises:
            ValueError: If required columns are missing.
        """
        required_columns = {"Test_Case_Name", "Execute"}
        missing_columns = required_columns - set(fieldnames)

        if missing_columns:
            raise ValueError(
                f"CSV is missing required columns: {', '.join(missing_columns)}"
            )

        self.logger.debug(f"CSV structure validated. Columns: {', '.join(fieldnames)}")

    def read_executable_rows(self) -> List[Dict[str, str]]:
        """
        Read only rows marked with Execute='Yes'.

        Returns:
            List[Dict[str, str]]: List of executable rows.

        Raises:
            FileNotFoundError: If CSV file doesn't exist.
            ValueError: If CSV has invalid structure.
        """
        all_rows = self.read_all_rows()
        executable_rows = [
            row for row in all_rows if row.get("Execute", "").strip().upper() == "YES"
        ]

        self.logger.info(
            f"Found {len(executable_rows)} executable rows out of {len(all_rows)} total"
        )
        return executable_rows

    def get_rows_by_test_name(self, test_name: str) -> List[Dict[str, str]]:
        """
        Get all executable rows for a specific test name.

        Args:
            test_name (str): The test case name to search for.

        Returns:
            List[Dict[str, str]]: List of matching executable rows.
        """
        executable_rows = self.read_executable_rows()
        matching_rows = [
            row
            for row in executable_rows
            if row.get("Test_Case_Name", "").strip() == test_name
        ]

        self.logger.debug(
            f"Found {len(matching_rows)} executable row(s) for test: {test_name}"
        )
        return matching_rows

    def update_cell(
        self, test_name: str, column_name: str, value: Any, row_index: int = 0
    ) -> None:
        """
        Update a specific cell in the CSV file.

        Args:
            test_name (str): The test case name to update.
            column_name (str): The column name to update.
            value (Any): The new value.
            row_index (int): If multiple rows exist for same test, which one to update (0-based).

        Raises:
            FileNotFoundError: If CSV file doesn't exist.
            ValueError: If test case not found or invalid column.
        """
        csv_path = self.get_environment_csv_path()

        # Read all rows
        rows = []
        fieldnames = []

        with open(csv_path, "r", encoding=self.encoding, newline="") as file:
            csv_reader = csv.DictReader(file)
            fieldnames = csv_reader.fieldnames or []
            rows = list(csv_reader)

        if column_name not in fieldnames:
            raise ValueError(
                f"Column '{column_name}' not found in CSV. "
                f"Available columns: {', '.join(fieldnames)}"
            )

        # Find and update the row
        updated = False
        matching_indices = [
            i
            for i, row in enumerate(rows)
            if row.get("Test_Case_Name", "").strip() == test_name
            and row.get("Execute", "").strip().upper() == "YES"
        ]

        if not matching_indices:
            raise ValueError(f"No executable rows found for test: {test_name}")

        if row_index >= len(matching_indices):
            raise ValueError(
                f"Row index {row_index} out of range. "
                f"Only {len(matching_indices)} row(s) found for test: {test_name}"
            )

        target_index = matching_indices[row_index]
        rows[target_index][column_name] = str(value)

        # Write back to CSV
        with open(csv_path, "w", encoding=self.encoding, newline="") as file:
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(rows)

        if self.config.get_log_csv_operations():
            self.logger.info(
                f"Updated CSV: {test_name}[{row_index}].{column_name} = {value}"
            )

        updated = True

        if not updated:
            raise ValueError(f"Could not update CSV for test: {test_name}")

    def validate_csv_file(self, csv_path: Path) -> bool:
        """
        Validate a CSV file structure without reading all data.

        Args:
            csv_path (Path): Path to the CSV file to validate.

        Returns:
            bool: True if CSV is valid.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If CSV structure is invalid.
        """
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        try:
            with open(csv_path, "r", encoding=self.encoding, newline="") as file:
                csv_reader = csv.DictReader(file)
                if csv_reader.fieldnames is None:
                    raise ValueError("CSV file is empty")
                self._validate_csv_structure(csv_reader.fieldnames)
            self.logger.info(f"CSV file validated: {csv_path.name}")
            return True
        except Exception as e:
            self.logger.error(f"CSV validation failed for {csv_path}: {e}")
            raise


def get_csv_manager() -> CSVManager:
    """
    Get a new instance of the CSV manager.

    Returns:
        CSVManager: A CSV manager instance.
    """
    return CSVManager()


def get_data_manager() -> Any:
    """
    Get the data manager for the configured format.

    Returns:
        CSVManager | YAMLManager: The data manager selected by config.
    """
    config = get_config()
    if config.get_data_format() == "yaml":
        from src.utilities.yaml_manager import get_yaml_manager

        return get_yaml_manager()
    return get_csv_manager()
