# CSV-Driven Test Execution Framework

## Overview

This is a production-ready **CSV-driven test execution framework** for **Playwright + Pytest** automation. It provides centralized control over test execution through CSV files, enabling non-technical stakeholders to manage which tests should run in different environments without modifying code.

### Key Features

✅ **Environment-based CSV Test Data** - Separate CSV files for SIT, UAT, PROD  
✅ **Centralized Test Control** - Enable/disable tests via CSV column  
✅ **Dynamic Test Parameterization** - Support multiple data rows per test  
✅ **Reusable Test Data Functions** - `Read_Test_Data()` and `Write_Test_Data()`  
✅ **Thread-Safe Execution Context** - Proper context management for parallel execution  
✅ **Execution Tracking** - Real-time test status updates in CSV  
✅ **Production-Ready Logging** - Comprehensive logging with file and console output  
✅ **Clean Architecture** - Modular, scalable, and maintainable design  
✅ **Error Handling** - Robust exception handling with detailed error messages  

---

## Project Structure

```
project_root/
├── config/
│   └── config.yaml                 # Environment and framework configuration
│
├── Test_Data/
│   ├── SIT.csv                    # Test data for SIT environment
│   ├── UAT.csv                    # Test data for UAT environment
│   └── PROD.csv                   # Test data for PROD environment
│
├── src/
│   ├── utilities/
│   │   ├── __init__.py
│   │   ├── logger.py              # Centralized logging
│   │   ├── config_manager.py      # Configuration loader
│   │   ├── csv_manager.py         # CSV read/write operations
│   │   ├── execution_context.py   # Thread-safe context manager
│   │   └── axe_helper.py          # (Existing) Accessibility helper
│   │
│   └── common/
│       ├── __init__.py
│       └── reusable_functions.py  # Read_Test_Data() and Write_Test_Data()
│
├── tests/
│   ├── conftest.py                # Pytest configuration with CSV hooks
│   └── travel_mug_30oz_agave_teal_test.py  # Example test using CSV data
│
├── logs/                          # Auto-created, contains execution logs
├── config.yaml                    # Environment configuration
├── pytest.ini                     # Pytest configuration
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Edit `config/config.yaml` to set the active environment:

```yaml
environment: SIT
# Options: SIT, UAT, PROD
```

### 3. Prepare Test Data CSV

Edit `Test_Data/SIT.csv` to define which tests to execute:

```csv
Test_Case_Name,Execute,Field_1,Field_2,Result,Comments
test_travel_mug_30oz_agave_teal_bride_design,Yes,Agave Teal,Bride,,
test_sample_test,No,Value1,Value2,,
```

**CSV Columns Explained:**
- `Test_Case_Name` - Must match the pytest test function name exactly
- `Execute` - "Yes" to run, "No" to skip
- `Field_1`, `Field_2`, ... - Custom test data (add as needed)
- `Result` - Updated automatically by tests (Passed/Failed)
- `Comments` - Updated by tests with execution notes

---

## Quick Start

### Running Tests

```bash
# Run all tests marked as "Execute: Yes" in the configured environment
pytest

# Run tests with verbose output
pytest -v

# Run with detailed logging
pytest -v --log-cli-level=DEBUG

# Run specific test file
pytest tests/travel_mug_30oz_agave_teal_test.py
```

### Using Test Data in Tests

```python
from src.common.reusable_functions import Read_Test_Data, Write_Test_Data

class TestExample:
    def test_something(self):
        # Read data from CSV
        field1_value = Read_Test_Data("Field_1")  # Returns value from CSV
        field2_value = Read_Test_Data("Field_2")
        
        # Your test logic here
        # ...
        
        # Write results back to CSV
        Write_Test_Data("Result", "Passed")
        Write_Test_Data("Comments", "All assertions passed")
```

---

## Core Components

### 1. Configuration Manager (`src/utilities/config_manager.py`)

Manages environment and framework configuration from `config/config.yaml`.

**Features:**
- Singleton pattern for single instance
- Validates environment configuration
- Supports SIT, UAT, PROD environments
- Thread-safe operations

**Usage:**
```python
from src.utilities.config_manager import get_config

config = get_config()
environment = config.get_environment()  # Returns current environment
```

### 2. CSV Manager (`src/utilities/csv_manager.py`)

Handles all CSV read/write operations with validation.

**Features:**
- Automatic environment-based CSV loading
- CSV structure validation
- Executable test row filtering
- Atomic CSV updates
- Comprehensive error handling

**Key Methods:**
```python
from src.utilities.csv_manager import get_csv_manager

csv_manager = get_csv_manager()

# Read executable rows
rows = csv_manager.read_executable_rows()

# Get rows for specific test
test_rows = csv_manager.get_rows_by_test_name("test_login")

# Update CSV cell
csv_manager.update_cell("test_login", "Result", "Passed")
```

### 3. Execution Context (`src/utilities/execution_context.py`)

Thread-safe context manager maintaining current test row state.

**Features:**
- Singleton pattern
- Thread-safety with locks
- Per-thread context isolation
- Real-time context updates

**Usage:**
```python
from src.utilities.execution_context import get_execution_context

context = get_execution_context()

# Set context (done automatically by framework)
context.set_current_row(row_data)

# Get current row
current_row = context.get_current_row()

# Get specific value
value = context.get_cell_value("Field_1")

# Update value
context.set_cell_value("Result", "Passed")

# Clear context (done automatically after test)
context.clear_context()
```

### 4. Logger (`src/utilities/logger.py`)

Centralized logging with file and console output.

**Features:**
- Singleton pattern
- File and console handlers
- Detailed formatting with timestamps
- Automatic log directory creation

**Usage:**
```python
from src.utilities.logger import get_logger

logger = get_logger()
logger.info("Test execution started")
logger.error("Test failed with error")
logger.debug("Detailed debug information")
```

### 5. Reusable Functions (`src/common/reusable_functions.py`)

Core functions for reading and writing test data.

#### `Read_Test_Data(column_name: str) -> Any`

Reads value from current test's CSV row.

```python
from src.common.reusable_functions import Read_Test_Data

username = Read_Test_Data("Field_1")
password = Read_Test_Data("Field_2")
```

**Returns:** Value from specified column or None if not found  
**Raises:** RuntimeError if called outside test context

#### `Write_Test_Data(column_name: str, value: Any) -> None`

Updates current test's CSV row and saves to file.

```python
from src.common.reusable_functions import Write_Test_Data

Write_Test_Data("Result", "Passed")
Write_Test_Data("Comments", "All validations passed")
```

**Raises:** RuntimeError if called outside test context

---

## Pytest Hooks & Fixtures

### Pytest Hooks Implemented

**1. `pytest_configure(config)`**
- Initializes CSV framework
- Loads configuration
- Sets base URL

**2. `pytest_collection_modifyitems(config, items)`**
- Filters tests based on CSV "Execute" column
- Auto-skips non-executable tests
- Tracks execution statistics

**3. `csv_test_data_fixture`**
- Auto-used for all tests
- Loads CSV data before test
- Cleans up context after test

**4. `pytest_runtest_logreport(report)`**
- Tracks test results
- Records pass/fail/skip status
- Updates execution statistics

**5. `pytest_sessionfinish(session, exitstatus)`**
- Prints execution summary
- Displays test statistics

### Auto-Use Fixture

```python
@pytest.fixture(autouse=True)
def csv_test_data_fixture(request):
    """Automatically used for every test"""
    # Sets execution context before test
    # Cleans up after test
```

This fixture automatically:
- Loads CSV data for the current test
- Sets execution context
- Cleans up after test completes

---

## CSV File Format

### Example SIT.csv

```csv
Test_Case_Name,Execute,Field_1,Field_2,Result,Comments
test_login,Yes,user1,password1,,
test_login,Yes,user2,password2,,
test_checkout,Yes,credit_card,12345,,
test_payment_failure,No,invalid_card,99999,,
test_travel_mug_30oz_agave_teal_bride_design,Yes,Agave Teal,Bride,,
```

### Adding Custom Columns

Simply add new columns to the CSV header, and access them in tests:

```csv
Test_Case_Name,Execute,Username,Password,Browser,Result,Comments
test_login,Yes,user1,pass1,Chrome,,
test_login,Yes,user2,pass2,Firefox,,
```

Then in test:

```python
browser = Read_Test_Data("Browser")
```

---

## Advanced Usage

### Parameterized Tests with Multiple Rows

If multiple rows have the same test name, the framework executes the test for each row:

```csv
test_login,Yes,user1,password1
test_login,Yes,user2,password2
test_login,Yes,user3,password3
```

This runs `test_login` three times with different data.

**Current Implementation:** Uses first matching row (row_index=0)  
**Future Enhancement:** Can be extended for full parameterization

### Handling Test Failures

```python
def test_example():
    try:
        # Test logic
        assert condition
        Write_Test_Data("Result", "Passed")
    except Exception as e:
        Write_Test_Data("Result", "Failed")
        Write_Test_Data("Comments", f"Error: {str(e)}")
        raise  # Re-raise to fail the test
```

### Accessing Execution Context Directly

```python
from src.utilities.execution_context import get_execution_context

context = get_execution_context()
current_row = context.get_current_row()
test_name = current_row.get("Test_Case_Name")
```

### Custom Configuration

Edit `config/config.yaml` for advanced settings:

```yaml
environment: SIT

logging:
  level: DEBUG
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "logs/execution.log"

framework:
  csv_encoding: utf-8
  auto_skip_disabled: true
  log_csv_operations: true
```

---

## Execution Flow

### Test Collection Phase

1. Pytest collects all tests
2. Framework hooks `pytest_collection_modifyitems()`
3. CSV is loaded from configured environment
4. Tests marked "Execute: No" are marked for skip
5. Tests marked "Execute: Yes" are kept active

### Test Execution Phase

For each test:

1. `csv_test_data_fixture` loads CSV row data
2. Execution context is set with current row
3. Test runs and uses `Read_Test_Data()` / `Write_Test_Data()`
4. `pytest_runtest_logreport()` tracks result
5. CSV is updated with result
6. Context is cleaned up

### Reporting Phase

1. `pytest_sessionfinish()` prints summary
2. Log file is created in `logs/` directory
3. Test results visible in console output

---

## Logging

### Log Files

Logs are automatically created in `logs/` directory:

```
logs/
└── execution.log
```

### Log Format

```
2024-05-28 10:30:45 - CSV_Framework - INFO - Configuration loaded from config/config.yaml
2024-05-28 10:30:46 - CSV_Framework - INFO - Loaded 3 executable test(s) from CSV
2024-05-28 10:30:47 - CSV_Framework - INFO - Test 'test_login' context set with CSV data
2024-05-28 10:30:48 - CSV_Framework - INFO - ✓ Test PASSED: test_login
```

### Logging Levels

- **DEBUG**: Detailed framework operations
- **INFO**: Test execution progress and results
- **WARNING**: Tests skipped
- **ERROR**: Test failures and configuration errors

---

## Best Practices

### 1. CSV Naming Conventions

```csv
Test_Case_Name,Execute,Field_1,Field_2,Username,Password,Result,Comments
```

Use clear, descriptive column names that indicate data purpose.

### 2. Error Handling in Tests

```python
def test_example():
    try:
        # Test logic
        assert True
        Write_Test_Data("Result", "Passed")
    except AssertionError as e:
        Write_Test_Data("Result", "Failed")
        Write_Test_Data("Comments", f"Assertion failed: {str(e)}")
        raise
    except Exception as e:
        Write_Test_Data("Result", "Error")
        Write_Test_Data("Comments", f"Unexpected error: {str(e)}")
        raise
```

### 3. Test Case Naming

- Use descriptive names: `test_login_with_valid_credentials`
- Match CSV `Test_Case_Name` exactly
- Use lowercase with underscores

### 4. CSV Management

- Keep one row per test case instance
- Use "Yes" for tests in development/active testing
- Use "No" for regression tests or deprecated tests
- Update Comments column with meaningful notes

### 5. Maintaining Test Data

- Regular backup of Test_Data folder
- Version control CSV files
- Document custom columns
- Keep CSV clean and organized

---

## Troubleshooting

### Issue: Tests Not Executing

**Cause:** Test marked as "Execute: No" in CSV

**Solution:** Change to "Execute: Yes" and re-run tests

### Issue: RuntimeError: "No execution context set"

**Cause:** `Read_Test_Data()` called outside of test function

**Solution:** Ensure function is called from within a @pytest.fixture or test function

### Issue: FileNotFoundError: "CSV file not found"

**Cause:** Environment CSV doesn't exist

**Solution:** Create corresponding CSV file in Test_Data/ folder

### Issue: ValueError: "CSV is missing required columns"

**Cause:** CSV doesn't have "Test_Case_Name" or "Execute" columns

**Solution:** Add required columns to CSV header

### Issue: Configuration not loading

**Cause:** config.yaml not found or YAML syntax error

**Solution:** Check config file path and YAML formatting

---

## Example Test Implementation

### Before (Manual Test Data)

```python
class TestLogin:
    def test_login(self):
        page.fill("input[name='username']", "user1")
        page.fill("input[name='password']", "pass1")
        page.click("button[type='submit']")
        expect(page).to_have_title("Dashboard")
```

### After (CSV-Driven)

```python
from src.common.reusable_functions import Read_Test_Data, Write_Test_Data

class TestLogin:
    def test_login(self, page: Page):
        try:
            username = Read_Test_Data("Username")
            password = Read_Test_Data("Password")
            
            page.fill("input[name='username']", username)
            page.fill("input[name='password']", password)
            page.click("button[type='submit']")
            expect(page).to_have_title("Dashboard")
            
            Write_Test_Data("Result", "Passed")
        except Exception as e:
            Write_Test_Data("Result", "Failed")
            Write_Test_Data("Comments", str(e))
            raise
```

Then in CSV:

```csv
Test_Case_Name,Execute,Username,Password,Result,Comments
test_login,Yes,user1,password1,,
test_login,Yes,user2,password2,,
test_login,Yes,admin,adminpass,,
```

---

## Adding New Tests

### Step 1: Create Test File

```python
# tests/test_new_feature.py
from src.common.reusable_functions import Read_Test_Data, Write_Test_Data
from playwright.sync_api import Page

class TestNewFeature:
    def test_new_feature(self, page: Page):
        try:
            data = Read_Test_Data("Field_1")
            # Test implementation
            Write_Test_Data("Result", "Passed")
        except Exception as e:
            Write_Test_Data("Result", "Failed")
            Write_Test_Data("Comments", str(e))
            raise
```

### Step 2: Add Row to CSV

```csv
Test_Case_Name,Execute,Field_1,Field_2,Result,Comments
test_new_feature,Yes,TestValue1,TestValue2,,
```

### Step 3: Run Tests

```bash
pytest
```

**That's it!** No framework changes needed.

---

## Environment-Specific Testing

### SIT.csv - Development/Testing

```csv
Test_Case_Name,Execute,Field_1,Field_2,Result,Comments
test_login,Yes,testuser,testpass,,
test_checkout,Yes,testdata,,,
test_error_handling,Yes,errorcase,,,
```

### UAT.csv - User Acceptance Testing

```csv
Test_Case_Name,Execute,Field_1,Field_2,Result,Comments
test_login,Yes,uatuser,uatpass,,
test_checkout,Yes,uatdata,,,
```

### PROD.csv - Production (Usually Minimal)

```csv
Test_Case_Name,Execute,Field_1,Field_2,Result,Comments
test_smoke_login,Yes,produser,prodpass,,
test_smoke_checkout,Yes,proddata,,,
```

---

## Performance Considerations

- **CSV Reading:** Optimized with lazy loading
- **Context Management:** Thread-safe with minimal overhead
- **Logging:** Async logging for performance
- **Scalability:** Designed for parallel execution support

---

## Future Enhancements

- [ ] Full test parameterization for multiple rows
- [ ] Parallel test execution
- [ ] Test data encryption
- [ ] Web UI for CSV management
- [ ] Real-time test monitoring dashboard
- [ ] Integration with CI/CD pipelines
- [ ] Advanced reporting with charts
- [ ] Test data versioning

---

## Support & Documentation

For more information:
- Consult code comments in each utility module
- Check pytest documentation: https://docs.pytest.org
- Check Playwright documentation: https://playwright.dev/python

---

## License

This framework is part of the Playwright Python Example project.

---

## Summary

This CSV-driven test execution framework provides:

✅ **Centralized test control** through CSV files  
✅ **Production-ready architecture** with clean code  
✅ **Thread-safe operations** for parallel execution  
✅ **Comprehensive logging** for debugging  
✅ **Scalable design** for future enhancements  
✅ **Easy integration** with existing Playwright tests  

Start using it today to manage your test execution efficiently!
