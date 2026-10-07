import allure
import pytest
import requests
from typing import Any, Dict, List, Optional
from _pytest.fixtures import FixtureRequest, SubRequest
from _pytest.nodes import Item
from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import Page, Playwright

from src.utilities.axe_helper import AxeHelper
from src.utilities.constants import Constants
from src.utilities.config import get_base_url
from src.utilities.logger import get_logger
from src.utilities.config_manager import get_config
from src.utilities.csv_manager import get_data_manager
from src.utilities.execution_context import get_execution_context


# ============================================================================
# CSV-DRIVEN TEST EXECUTION FRAMEWORK
# ============================================================================


class ExecutionTracker:
    """Tracks test execution statistics for CSV-driven tests."""

    def __init__(self) -> None:
        """Initialize execution tracker."""
        self.total_tests = 0
        self.executed_tests = 0
        self.skipped_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.test_results: List[Dict[str, Any]] = []

    def record_test_result(
        self, test_name: str, status: str, error: Optional[str] = None
    ) -> None:
        """Record test result."""
        self.test_results.append(
            {"test_name": test_name, "status": status, "error": error}
        )

    def print_summary(self, logger: Any) -> None:
        """Print execution summary."""
        summary_msg = (
            f"\n{'=' * 80}\n"
            f"CSV-DRIVEN TEST EXECUTION SUMMARY\n"
            f"{'=' * 80}\n"
            f"Total Tests Collected: {self.total_tests}\n"
            f"Executed: {self.executed_tests}\n"
            f"Skipped: {self.skipped_tests}\n"
            f"Passed: {self.passed_tests}\n"
            f"Failed: {self.failed_tests}\n"
            f"{'=' * 80}"
        )
        
        try:
            # Try to log to the logger
            for line in summary_msg.split('\n'):
                if line.strip():
                    logger.info(line)
        except Exception:
            # If logging fails, silently print to stdout instead
            import sys
            print(summary_msg, file=sys.stdout)


# Global execution tracker
execution_tracker = ExecutionTracker()


def pytest_configure(config):
    """Override base_url based on TEST_ENV environment variable.
    
    This hook runs before any tests are collected, allowing us to set
    the base_url from the environment configuration.
    
    Also initializes the CSV-driven test execution framework.
    """
    logger = get_logger()
    
    try:
        # Load config for CSV framework
        config_manager = get_config()
        environment = config_manager.get_environment()
        logger.info(f"Pytest configured for environment: {environment}")
        logger.info("CSV-driven test execution framework initialized")
        
        # Get base URL
        base_url = get_base_url()
        config.option.base_url = base_url
        logger.info(f"Base URL set to: {base_url}")
        
    except Exception as e:
        logger.error(f"Configuration error: {e}")
        raise


def pytest_collection_modifyitems(config: Any, items: List[Any]) -> None:
    """
    Pytest hook: Called after test collection.
    Filters tests based on CSV data and marks skipped tests.

    Args:
        config: Pytest config object.
        items: List of collected test items.
    """
    logger = get_logger()

    try:
        config_manager = get_config()
        data_manager = get_data_manager()
        executable_rows = data_manager.read_executable_rows()

        # Create a set of executable test names
        executable_test_map: Dict[str, List[Dict[str, str]]] = {}
        for row in executable_rows:
            test_name = row.get("Test_Case_Name", "").strip()
            if test_name:
                if test_name not in executable_test_map:
                    executable_test_map[test_name] = []
                executable_test_map[test_name].append(row)

        logger.info(
            f"Loaded {len(executable_test_map)} executable test(s) from CSV"
        )

        # Mark tests as skip or keep them
        for item in items:
            test_name = item.name
            
            # Strip browser parameter (e.g., [chromium], [firefox], [webkit])
            # to match against CSV test names
            base_test_name = test_name.split("[")[0] if "[" in test_name else test_name

            # Check if test is in executable list
            if base_test_name not in executable_test_map:
                if config_manager.get_auto_skip_disabled():
                    item.add_marker(
                        pytest.mark.skip(
                            reason=f"Test '{base_test_name}' not marked for execution in CSV"
                        )
                    )
                    logger.debug(f"Marked test for skip: {base_test_name}")
                    execution_tracker.skipped_tests += 1
            else:
                execution_tracker.executed_tests += 1
                logger.debug(f"Test marked for execution: {base_test_name}")

        execution_tracker.total_tests = len(items)

    except Exception as e:
        logger.error(f"Error modifying collection: {e}")
        raise


@pytest.fixture(autouse=True)
def navigate_to_base_url(page: Page) -> Any:
    """
    Pytest fixture: Auto-used for every test.
    Navigates to the base URL based on the configured environment before test runs.
    
    The environment (SIT, UAT, PROD) is determined by config/config.yaml.
    Each environment has its own base URL that is launched automatically.

    Args:
        page: Playwright page object.

    Yields:
        None
    """
    logger = get_logger()
    
    try:
        config_manager = get_config()
        from src.utilities.config import get_base_url
        
        base_url = get_base_url()
        environment = config_manager.get_environment()
        
        logger.info(f"Navigating to {environment} environment: {base_url}")
        page.goto(base_url)
        logger.info(f"Successfully navigated to {environment} environment")
        
        yield
        
    except Exception as e:
        logger.error(f"Error navigating to base URL: {e}")
        raise


@pytest.fixture(autouse=True)
def csv_test_data_fixture(request: Any) -> Any:
    """
    Pytest fixture: Auto-used for every test.
    Sets up execution context with CSV data before test runs.
    Cleans up context after test completes.

    Args:
        request: Pytest request object.

    Yields:
        None
    """
    logger = get_logger()
    test_name = request.node.name
    # Strip browser parameter to match against CSV test names
    base_test_name = test_name.split("[")[0] if "[" in test_name else test_name
    context = get_execution_context()

    try:
        data_manager = get_data_manager()

        # Get matching rows from the configured data source using base test name
        matching_rows = data_manager.get_rows_by_test_name(base_test_name)

        if matching_rows:
            # Use the first matching row (for parameterized tests, handle multiple rows)
            row_data = matching_rows[0]

            # Set execution context
            context.set_current_row(row_data)
            logger.info(f"Test '{test_name}' context set with CSV data")

        yield

    except Exception as e:
        logger.error(f"Error in CSV test data fixture for {test_name}: {e}")
        raise
    finally:
        # Cleanup
        context.clear_context()


# ============================================================================
# ORIGINAL FIXTURES AND HOOKS
# ============================================================================



def goto(page: Page, request: SubRequest):
    """Fixture to navigate to the base URL based on the user.

    If the 'storage_state' is set in 'browser_context_args', it navigates to the inventory page,
    otherwise, it navigates to the login page.

    Args:
        page (Page): Playwright page object.
        request (SubRequest): Pytest request object to get the 'browser_context_args' fixture value.
            If 'browser_context_args' is set to a user parameter (e.g., 'standard_user'),
            the navigation is determined based on the user.

    Example:
        @pytest.mark.parametrize('browser_context_args', ["standard_user"], indirect=True)

    """
    if request.getfixturevalue("browser_context_args").get("storage_state"):
        page.goto("/inventory.html")
    else:
        page.goto("")


@pytest.fixture(scope="session")
def axe_playwright():
    """Fixture to provide an instance of AxeHelper with Axe initialized.

    This fixture has a session scope, meaning it will be created once per test session
    and shared across all tests.

    Returns:
        AxeHelper: An instance of AxeHelper with Axe initialized.

    """
    return AxeHelper(Axe())


@pytest.fixture(scope="function")
def browser_context_args(browser_context_args: dict, base_url: str, request: SubRequest) -> dict:
    """This fixture allows setting browser context arguments for Playwright.

    Args:
        browser_context_args (dict): Base browser context arguments.
        request (SubRequest): Pytest request object to get the 'browser_context_args' fixture value.
        base_url (str): The base URL for the application under test.

    Returns:
        dict: Updated browser context arguments.

    See Also:
        https://playwright.dev/python/docs/api/class-browser#browser-new-contex

    Returns:
        dict: Updated browser context arguments.

    """
    context_args = {
        **browser_context_args,
        "no_viewport": True,
        "user_agent": Constants.AUTOMATION_USER_AGENT,
        "permissions": ["geolocation", "microphone", "camera", "clipboard-read", "clipboard-write"],
    }

    if hasattr(request, "param"):
        context_args["storage_state"] = {
            "cookies": [
                {
                    "name": "session-username",
                    "value": request.param,
                    "url": base_url,
                }
            ]
        }
    return context_args


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict, playwright: Playwright) -> dict:
    """Fixture to set browser launch arguments.

    This fixture updates the browser launch arguments to start the browser maximized
    and sets the test ID attribute for selectors.

    Args:
        browser_type_launch_args (Dict): Original browser type launch arguments.
        playwright (Playwright): The Playwright instance.

    Returns:
        Dict: Updated browser type launch arguments with maximized window setting.

    Note:
        This fixture has a session scope, meaning it will be executed once per test session.

    See Also:
        https://playwright.dev/python/docs/api/class-browsertype#browser-type-launch

    """
    playwright.selectors.set_test_id_attribute("data-test")
    return {
        **browser_type_launch_args,
        "headless": False,
        "args": [
            "--start-maximized",
            "--allow-file-access-from-files",
            "--use-fake-device-for-media-stream",
            "--use-fake-ui-for-media-stream",
            "--hide-scrollbars",
            "--disable-features=IsolateOrigins,site-per-process,VizDisplayCompositor,SidePanelPinning,OptimizationGuideModelDownloading,OptimizationHintsFetching,OptimizationTargetPrediction,OptimizationHints",
            "--disable-popup-blocking",
            "--disable-search-engine-choice-screen",
            "--disable-infobars",
            "--disable-dev-shm-usage",
            "--disable-notifications",
            "--disable-blink-features=AutomationControlled",
        ],
    }


def get_public_ip() -> str:
    """Function to retrieve public IP address.

    Returns:
        str: Public IP address.

    """
    return requests.get(
        "http://checkip.amazonaws.com",
        timeout=40,
        headers={"User-Agent": Constants.AUTOMATION_USER_AGENT},
    ).text.rstrip()


@pytest.fixture(autouse=True)
def attach_playwright_results(page: Page, request: FixtureRequest):
    """Fixture to perform teardown actions and attach results to Allure report
    on failure.

    Args:
        page (Page): Playwright page object.
        request: Pytest request object.

    """
    yield
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        allure.attach(
            body=page.url,
            name="URL",
            attachment_type=allure.attachment_type.URI_LIST,
        )
        allure.attach(
            page.screenshot(full_page=True),
            name="Screen shot on failure",
            attachment_type=allure.attachment_type.PNG,
        )
        allure.attach(
            body=get_public_ip(),
            name="public ip address",
            attachment_type=allure.attachment_type.TEXT,
        )


def pytest_runtest_logreport(report: Any) -> None:
    """
    Pytest hook: Called when a test report is created.
    Tracks test results for CSV execution tracking and updates CSV with results.

    Args:
        report: Pytest report object.
    """
    logger = get_logger()

    # Only process the final report (not setup/teardown)
    if report.when == "call":
        test_name = report.nodeid.split("::")[-1]

        try:
            if report.passed:
                logger.info(f"Test PASSED: {test_name}")
                execution_tracker.passed_tests += 1
                execution_tracker.record_test_result(test_name, "PASSED")
            elif report.failed:
                logger.error(f"Test FAILED: {test_name}")
                execution_tracker.failed_tests += 1
                error_message = (
                    report.longrepr if report.longrepr else "Unknown error"
                )
                execution_tracker.record_test_result(
                    test_name, "FAILED", str(error_message)
                )
            elif report.skipped:
                logger.warning(f"Test SKIPPED: {test_name}")
                execution_tracker.record_test_result(test_name, "SKIPPED")

        except Exception as e:
            logger.error(f"Error recording test result: {e}")


def pytest_sessionfinish(session: Any, exitstatus: Any) -> None:
    """
    Pytest hook: Called after all tests have been run.
    Can be used for final cleanup or reporting.

    Args:
        session: Pytest session object.
        exitstatus: Exit status code.
    """
    # Skip the custom summary logging as pytest provides its own summary
    # and our logger handlers may be closed at this point
    pass

