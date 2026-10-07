"""
Execution context manager for maintaining current test row state.
Provides thread-safe access to the currently executing test data row.
"""

import threading
from typing import Any, Dict, Optional
from src.utilities.logger import get_logger


class ExecutionContext:
    """
    Thread-safe execution context manager.
    Maintains the current test row context for Read_Test_Data and Write_Test_Data functions.
    """

    _instance: Optional["ExecutionContext"] = None
    _lock = threading.Lock()
    _context: Dict[int, Dict[str, Any]] = {}  # thread_id -> context

    def __new__(cls) -> "ExecutionContext":
        """Singleton pattern with thread-safety."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def _get_thread_id() -> int:
        """Get current thread ID."""
        return threading.get_ident()

    def set_current_row(self, row_data: Dict[str, Any]) -> None:
        """
        Set the current test row data for this thread.

        Args:
            row_data (Dict[str, Any]): The current row data from CSV.

        Example:
            context.set_current_row({
                'Test_Case_Name': 'test_login',
                'Execute': 'Yes',
                'Field_1': 'user1',
                'Result': ''
            })
        """
        thread_id = self._get_thread_id()
        logger = get_logger()

        with self._lock:
            self._context[thread_id] = row_data.copy()
            logger.debug(
                f"[Thread {thread_id}] Context set for test: "
                f"{row_data.get('Test_Case_Name', 'Unknown')}"
            )

    def get_current_row(self) -> Optional[Dict[str, Any]]:
        """
        Get the current test row data for this thread.

        Returns:
            Optional[Dict[str, Any]]: Current row data or None if not set.
        """
        thread_id = self._get_thread_id()
        with self._lock:
            return self._context.get(thread_id)

    def get_cell_value(self, column_name: str) -> Optional[Any]:
        """
        Get a specific cell value from the current row.

        Args:
            column_name (str): The column name to retrieve.

        Returns:
            Optional[Any]: The cell value or None if not found.

        Raises:
            RuntimeError: If no context is set for current thread.
        """
        row = self.get_current_row()
        if row is None:
            raise RuntimeError(
                "No execution context set. Are you calling this from within a test?"
            )
        return row.get(column_name)

    def set_cell_value(self, column_name: str, value: Any) -> None:
        """
        Set a specific cell value in the current row.

        Args:
            column_name (str): The column name to update.
            value (Any): The new value for the cell.

        Raises:
            RuntimeError: If no context is set for current thread.
        """
        row = self.get_current_row()
        if row is None:
            raise RuntimeError(
                "No execution context set. Are you calling this from within a test?"
            )

        with self._lock:
            thread_id = self._get_thread_id()
            self._context[thread_id][column_name] = value

    def clear_context(self) -> None:
        """Clear the execution context for this thread."""
        thread_id = self._get_thread_id()
        logger = get_logger()

        with self._lock:
            if thread_id in self._context:
                del self._context[thread_id]
                logger.debug(f"[Thread {thread_id}] Context cleared")

    def has_context(self) -> bool:
        """
        Check if execution context is set for this thread.

        Returns:
            bool: True if context is set, False otherwise.
        """
        thread_id = self._get_thread_id()
        with self._lock:
            return thread_id in self._context


def get_execution_context() -> ExecutionContext:
    """
    Get or create the execution context instance.

    Returns:
        ExecutionContext: The execution context manager.
    """
    return ExecutionContext()
