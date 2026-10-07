# CSV-Driven Framework - Quick Reference Guide

## 🚀 Quick Start

### 1. Configure Environment
Edit `config/config.yaml`:
```yaml
environment: SIT  # or UAT, PROD
```

### 2. Define Test Execution in CSV
Edit `Test_Data/SIT.csv`:
```csv
Test_Case_Name,Execute,Field_1,Field_2,Result,Comments
test_login,Yes,user1,pass1,,
test_checkout,No,data1,data2,,
```

### 3. Use in Test
```python
from src.common.reusable_functions import Read_Test_Data, Write_Test_Data

def test_login(page):
    username = Read_Test_Data("Field_1")
    password = Read_Test_Data("Field_2")
    # ... test logic ...
    Write_Test_Data("Result", "Passed")
```

### 4. Run Tests
```bash
pytest
# Only tests marked "Execute: Yes" will run!
```

---

## 📁 File Structure

```
project/
├── config/config.yaml                    # Set environment: SIT/UAT/PROD
├── Test_Data/
│   ├── SIT.csv                          # Control which tests run in SIT
│   ├── UAT.csv                          # Control which tests run in UAT
│   └── PROD.csv                         # Control which tests run in PROD
├── src/utilities/
│   ├── config_manager.py                # Load config
│   ├── csv_manager.py                   # Read/write CSV
│   ├── execution_context.py             # Track current row
│   └── logger.py                        # Logging
├── src/common/
│   └── reusable_functions.py            # Read_Test_Data(), Write_Test_Data()
└── tests/conftest.py                    # Pytest hooks (updated)
```

---

## 🔑 Key Functions

### Read Test Data
```python
Read_Test_Data("ColumnName") -> Any
```
- Reads value from current test's CSV row
- Must be called from within test
- Returns None if column doesn't exist

### Write Test Data
```python
Write_Test_Data("ColumnName", value) -> None
```
- Updates current test's CSV row
- Saves to file immediately
- Must be called from within test

---

## 📊 CSV Format

### Required Columns
- `Test_Case_Name` - Must match test function name exactly
- `Execute` - "Yes" to run, "No" to skip

### Optional Columns
- `Result` - Auto-updated with test status
- `Comments` - Auto-updated with error messages
- `Field_1`, `Field_2`, ... - Your custom test data

### Example
```csv
Test_Case_Name,Execute,Username,Password,Browser,Result,Comments
test_login,Yes,user1,pass1,Chrome,,
test_login,Yes,user2,pass2,Firefox,,
test_checkout,No,testdata,,,
```

---

## 🔄 Execution Flow

1. **Config Load** → Read `config/config.yaml`
2. **CSV Load** → Load `Test_Data/{environment}.csv`
3. **Test Filter** → Skip tests marked "Execute: No"
4. **Test Run** → Execute tests marked "Execute: Yes"
5. **Data Sync** → `Read_Test_Data()` fetches CSV data
6. **Result Update** → `Write_Test_Data()` updates CSV
7. **Report** → Print execution summary

---

## ✅ Adding New Tests

1. Create test function:
```python
def test_new_feature(page):
    data = Read_Test_Data("Field_1")
    # test logic
    Write_Test_Data("Result", "Passed")
```

2. Add CSV row:
```csv
test_new_feature,Yes,TestValue1,TestValue2,,
```

3. Run:
```bash
pytest
```

---

## 🛠️ Configuration

### config/config.yaml
```yaml
environment: SIT              # Active environment

logging:
  level: INFO                 # DEBUG, INFO, WARNING, ERROR
  format: "custom format"
  file: "logs/execution.log"

framework:
  csv_encoding: utf-8         # CSV file encoding
  auto_skip_disabled: true    # Auto-skip non-executable tests
  log_csv_operations: true    # Log all CSV reads/writes
```

---

## 📋 CSV Rules

| Rule | Example |
|------|---------|
| Test name must match function | CSV: `test_login` → Code: `def test_login()` |
| Execute column values | "Yes", "No", "YES", "NO" (case-insensitive) |
| Column names are case-sensitive | `Field_1` ≠ `field_1` |
| Empty Execute = Skip | Default behavior |
| Multiple rows same test | Test runs multiple times |
| Custom columns supported | Add any column, access via `Read_Test_Data()` |

---

## 🔍 Debugging

### View Logs
```bash
# Console output
pytest -v

# Detailed debug logs
pytest -v --log-cli-level=DEBUG

# Log file
cat logs/execution.log
```

### Common Issues

**"Test marked for skip"**
- Test not in CSV or Execute = No
- Solution: Add to CSV with Execute = Yes

**"No execution context set"**
- Called Read_Test_Data() outside test
- Solution: Call only from test function

**"CSV file not found"**
- Environment CSV doesn't exist
- Solution: Create Test_Data/{environment}.csv

---

## 🎯 Best Practices

✅ Use descriptive column names  
✅ Keep CSV organized and clean  
✅ Update Comments with meaningful notes  
✅ Use "No" to disable regression tests  
✅ Handle exceptions with Write_Test_Data()  
✅ Regular backup of Test_Data/  
✅ Version control CSV files  

❌ Don't modify framework code for each test  
❌ Don't hardcode test data in test code  
❌ Don't forget to update CSV Execute column  
❌ Don't leave tests in "No" without comments  

---

## 🚦 Test Execution Examples

### Example 1: Simple Login Test
**CSV:**
```csv
Test_Case_Name,Execute,Username,Password,Result,Comments
test_login,Yes,testuser,testpass,,
```

**Test:**
```python
def test_login(page):
    username = Read_Test_Data("Username")
    password = Read_Test_Data("Password")
    page.fill("#username", username)
    page.fill("#password", password)
    page.click("button[type=submit]")
    Write_Test_Data("Result", "Passed")
```

### Example 2: Multi-User Test
**CSV:**
```csv
Test_Case_Name,Execute,Username,Password,Result,Comments
test_login,Yes,user1,pass1,,
test_login,Yes,user2,pass2,,
test_login,Yes,admin,admin123,,
```

**Result:** Test runs 3 times with different data automatically!

### Example 3: Environment-Specific Tests
**SIT.csv:**
```csv
test_all_features,Yes,...
test_stress,Yes,...
```

**PROD.csv:**
```csv
test_all_features,No,...  # Disabled in prod
test_stress,No,...        # Disabled in prod (only smoke tests)
test_smoke_login,Yes,...
```

---

## 📈 Execution Summary

After test runs, you'll see:
```
================================================================================
CSV-DRIVEN TEST EXECUTION SUMMARY
================================================================================
Total Tests Collected: 10
Executed: 7
Skipped: 3
Passed: 6
Failed: 1
================================================================================
```

---

## 🔐 Thread Safety

Framework is thread-safe for:
- Execution context management
- CSV read/write operations
- Concurrent test execution
- Logger operations

Perfect for parallel test execution!

---

## 📝 Quick Commands

```bash
# Run all executable tests
pytest

# Run with output
pytest -v

# Run with debug logs
pytest -v --log-cli-level=DEBUG

# Run specific file
pytest tests/test_login.py

# Run specific test
pytest tests/test_login.py::TestLogin::test_login

# Run with markers
pytest -m "not skip"

# Generate Allure report
pytest --alluredir=allure-results
allure serve allure-results
```

---

## 🎓 Learning Path

1. **Start:** Understand CSV structure
2. **Try:** Modify SIT.csv, run pytest
3. **Implement:** Use Read_Test_Data() in test
4. **Update:** Use Write_Test_Data() for results
5. **Scale:** Add more tests, change environments
6. **Master:** Advanced features, parallel execution

---

## 💡 Tips & Tricks

1. **Bulk Enable/Disable:**
   - Find & Replace "No" → "Yes" (or vice versa) in CSV

2. **Track Test Progress:**
   - Look at Result column to see which tests passed/failed

3. **Add Custom Fields:**
   - Just add column to CSV and Read_Test_Data()

4. **Environment Switching:**
   - Edit config.yaml: environment: UAT
   - Re-run: pytest (will use UAT.csv)

5. **Debug Single Test:**
   - Set all other tests to Execute: No
   - Run: pytest
   - Check logs/execution.log

---

## 🆘 Support

For issues:
1. Check logs/execution.log
2. Run with --log-cli-level=DEBUG
3. Verify CSV format (no extra spaces)
4. Ensure Test_Case_Name matches function name exactly
5. Check config.yaml syntax

---

## 📚 See Also

- README_CSV_FRAMEWORK.md - Detailed documentation
- config/config.yaml - Configuration options
- Test_Data/*.csv - Environment-specific data
- tests/conftest.py - Pytest hooks
- src/utilities/ - Framework implementation

---

**Version:** 1.0  
**Last Updated:** 2024  
**Framework:** CSV-Driven Playwright + Pytest  
