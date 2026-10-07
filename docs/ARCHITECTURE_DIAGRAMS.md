# CSV-Driven Framework - Architecture & Flow Diagrams

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Test Execution Flow                       │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐
│   pytest     │ starts
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│ pytest_configure() Hook                                  │
│ ├─ Load config/config.yaml                             │
│ ├─ Get environment (SIT/UAT/PROD)                       │
│ └─ Initialize ConfigManager                            │
└──────┬───────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│ Pytest Collection Phase                                  │
│ ├─ Collect all test files                              │
│ └─ Gather all test functions                           │
└──────┬───────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│ pytest_collection_modifyitems() Hook                     │
│ ├─ Load Test_Data/{environment}.csv                    │
│ ├─ Parse CSV rows                                      │
│ ├─ Find executable tests (Execute=Yes)               │
│ └─ Mark non-executable tests with skip marker         │
└──────┬───────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│ Test Execution Loop                                      │
└──────┬───────────────────────────────────────────────────┘
       │
       ├─→ For Each Executable Test:
       │   │
       │   ├─→ csv_test_data_fixture (autouse=True)
       │   │   ├─ Load matching CSV row
       │   │   ├─ Set execution context
       │   │   └─ Inject into test
       │   │
       │   ├─→ Test Function Executes
       │   │   ├─ Call Read_Test_Data("Field_1")
       │   │   │  └─ Get value from context
       │   │   │
       │   │   ├─ Call Write_Test_Data("Result", "Passed")
       │   │   │  └─ Update CSV immediately
       │   │   │
       │   │   └─ Test completes (pass/fail/error)
       │   │
       │   ├─→ pytest_runtest_logreport() Hook
       │   │   ├─ Track test result
       │   │   ├─ Update execution statistics
       │   │   └─ Log to console and file
       │   │
       │   └─→ Fixture Cleanup
       │       ├─ Clear execution context
       │       └─ Free resources
       │
       │   ├─→ For Each Skipped Test:
       │       └─ pytest.mark.skip applied
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│ pytest_sessionfinish() Hook                              │
│ ├─ Print execution summary                             │
│ ├─ Display statistics                                  │
│ └─ Show total/passed/failed/skipped count             │
└──────┬───────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│ Test Session Complete                                    │
│ └─ Results in Test_Data/{env}.csv                     │
│ └─ Logs in logs/execution.log                         │
└──────────────────────────────────────────────────────────┘
```

---

## Component Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                   Pytest Configuration                          │
│                                                                 │
│  pytest.ini ──┬─→ Markers                                     │
│               ├─→ Logging config                             │
│               └─→ Python path                               │
└────────┬───────────────────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────────────────────────────┐
│                   Framework Utilities                          │
│                     (src/utilities/)                           │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ ConfigManager (Singleton)                              │   │
│  │ ├─ Loads config/config.yaml                           │   │
│  │ ├─ Validates environment                              │   │
│  │ └─ Provides configuration to framework               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ CSVManager                                             │   │
│  │ ├─ Reads Test_Data/{env}.csv                         │   │
│  │ ├─ Validates CSV structure                           │   │
│  │ ├─ Filters executable rows                           │   │
│  │ └─ Updates CSV with results                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ ExecutionContext (Singleton + Thread-Safe)             │   │
│  │ ├─ Stores current test row data                        │   │
│  │ ├─ Per-thread context isolation                       │   │
│  │ ├─ Read/write cell values                            │   │
│  │ └─ Thread-lock protection                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Logger (Singleton)                                     │   │
│  │ ├─ File handler (logs/execution.log)                 │   │
│  │ ├─ Console handler (colored output)                  │   │
│  │ └─ DEBUG/INFO/WARNING/ERROR levels                  │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────────────────────────────┐
│              Reusable Functions (src/common/)                   │
│                                                                 │
│  ┌──────────────────────────────────────────────────┐           │
│  │ Read_Test_Data(column_name: str)                │           │
│  │ ├─ Access ExecutionContext                     │           │
│  │ ├─ Return cell value or None                   │           │
│  │ └─ Raise error if no context                   │           │
│  └──────────────────────────────────────────────────┘           │
│                                                                 │
│  ┌──────────────────────────────────────────────────┐           │
│  │ Write_Test_Data(column_name, value)            │           │
│  │ ├─ Update ExecutionContext                     │           │
│  │ ├─ Update CSV file                             │           │
│  │ └─ Log operation                               │           │
│  └──────────────────────────────────────────────────┘           │
└────────────────────────────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────────────────────────────┐
│                  Pytest Hooks (tests/conftest.py)              │
│                                                                 │
│  ┌────────────────────────────────────────────────┐             │
│  │ pytest_configure(config)                       │             │
│  │ └─→ Initialize framework                      │             │
│  └────────────────────────────────────────────────┘             │
│                                                                 │
│  ┌────────────────────────────────────────────────┐             │
│  │ pytest_collection_modifyitems(config, items)  │             │
│  │ └─→ Filter & mark skip tests                  │             │
│  └────────────────────────────────────────────────┘             │
│                                                                 │
│  ┌────────────────────────────────────────────────┐             │
│  │ csv_test_data_fixture (autouse=True)          │             │
│  │ └─→ Inject CSV data into test                │             │
│  └────────────────────────────────────────────────┘             │
│                                                                 │
│  ┌────────────────────────────────────────────────┐             │
│  │ pytest_runtest_logreport(report)              │             │
│  │ └─→ Track test results                        │             │
│  └────────────────────────────────────────────────┘             │
│                                                                 │
│  ┌────────────────────────────────────────────────┐             │
│  │ pytest_sessionfinish(session, exitstatus)    │             │
│  │ └─→ Print summary                             │             │
│  └────────────────────────────────────────────────┘             │
└────────────────────────────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────────────────────────────┐
│                   Test Execution                               │
│                                                                 │
│  Your Test Functions:                                          │
│  ├─ test_login()                                              │
│  ├─ test_checkout()                                           │
│  ├─ test_travel_mug_30oz_agave_teal_bride_design()           │
│  └─ test_custom_feature()                                     │
│                                                                 │
│  Each test can:                                                │
│  ├─ Call Read_Test_Data("ColumnName")                        │
│  └─ Call Write_Test_Data("ColumnName", value)               │
└────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      Configuration Loading                      │
└─────────────────────────────────────────────────────────────────┘

config/config.yaml
├─ environment: SIT
├─ logging:
│  ├─ level: INFO
│  └─ file: logs/execution.log
└─ framework:
   ├─ csv_encoding: utf-8
   ├─ auto_skip_disabled: true
   └─ log_csv_operations: true
         │
         ▼
    ConfigManager
         │
         ▼
    Loaded Config


┌─────────────────────────────────────────────────────────────────┐
│                        Test Data Loading                        │
└─────────────────────────────────────────────────────────────────┘

environment: SIT
         │
         ▼
Load: Test_Data/SIT.csv
         │
         ▼
Parse CSV Rows:
         │
┌────────┴─────────────────────────────────────┐
│                                               │
▼                                               ▼
Test_Case_Name=test_login               Test_Case_Name=test_checkout
Execute=Yes                             Execute=No
Field_1=user1                           Field_1=data1
Field_2=pass1                           Field_2=data2
         │                                       │
         ▼                                       ▼
    EXECUTABLE                              SKIP


┌─────────────────────────────────────────────────────────────────┐
│                      Test Execution Loop                        │
└─────────────────────────────────────────────────────────────────┘

For: test_login (Execute=Yes)
         │
         ▼
Get matching CSV row:
{Test_Case_Name: "test_login", Execute: "Yes", Field_1: "user1", ...}
         │
         ▼
Set ExecutionContext with row data
         │
         ▼
Run test_login() function
         │
    ┌────┴──────────────────────────────┐
    │                                    │
    ▼                                    ▼
Read_Test_Data("Field_1")       Write_Test_Data("Result", "Passed")
    │                                    │
    ▼                                    ▼
Query ExecutionContext         Update ExecutionContext
    │                                    │
    ▼                                    ▼
Return: "user1"              Write CSV: Result="Passed"
         │
         ▼
Test logic uses data
         │
         ▼
Test completes (Passed/Failed/Error)
         │
         ▼
Track result + update statistics
         │
         ▼
Clear ExecutionContext


┌─────────────────────────────────────────────────────────────────┐
│                      Result Persistence                         │
└─────────────────────────────────────────────────────────────────┘

Test_Data/SIT.csv (BEFORE):
Test_Case_Name,Execute,Field_1,Field_2,Result,Comments
test_login,Yes,user1,pass1,,

         ▼ (After test runs)

Test_Data/SIT.csv (AFTER):
Test_Case_Name,Execute,Field_1,Field_2,Result,Comments
test_login,Yes,user1,pass1,Passed,Test completed successfully

         │
         ▼
Logged to: logs/execution.log
2024-05-28 10:30:48 - CSV_Framework - INFO - ✓ Test PASSED: test_login
2024-05-28 10:30:48 - CSV_Framework - INFO - Updated CSV: test_login[0].Result = Passed
```

---

## Thread Safety Model

```
┌─────────────────────────────────────────────────────────────────┐
│              Thread-Safe Execution Context                      │
└─────────────────────────────────────────────────────────────────┘

Test Thread 1                   Test Thread 2                Test Thread 3
    │                              │                            │
    ├─ Lock acquired          ├─ Lock acquired         ├─ Lock acquired
    │  Context = Row1         │  Context = Row2        │  Context = Row3
    │  Release lock           │  Release lock          │  Release lock
    │                         │                        │
    ├─ Call Read_Test_Data()  ├─ Call Read_Test_Data() ├─ Call Read_Test_Data()
    │  Get Row1               │  Get Row2              │  Get Row3
    │  No lock needed         │  No lock needed        │  No lock needed
    │                         │                        │
    ├─ Call Write_Test_Data() ├─ Call Write_Test_Data()├─ Call Write_Test_Data()
    │  Lock acquired          │  Lock acquired         │  Lock acquired
    │  Update Row1            │  Update Row2           │  Update Row3
    │  Release lock           │  Release lock          │  Release lock
    │                         │                        │
    └─ Clear context          └─ Clear context         └─ Clear context


Key Features:
✅ Thread IDs used to isolate contexts
✅ threading.Lock prevents race conditions
✅ No deadlocks (lock only held briefly)
✅ Safe for concurrent test execution
✅ Each thread sees only its own data
```

---

## Execution Statistics Tracking

```
┌─────────────────────────────────────────────────────────────────┐
│                   ExecutionTracker Class                        │
└─────────────────────────────────────────────────────────────────┘

During Collection:
  total_tests = 10 (collected from pytest)

During Execution:
  ├─ Test 1 PASSED → passed_tests = 1, executed_tests = 1
  ├─ Test 2 FAILED → failed_tests = 1, executed_tests = 2
  ├─ Test 3 SKIPPED → skipped_tests = 1
  ├─ Test 4 PASSED → passed_tests = 2, executed_tests = 3
  ├─ Test 5 PASSED → passed_tests = 3, executed_tests = 4
  ├─ Test 6 SKIPPED → skipped_tests = 2
  ├─ Test 7 PASSED → passed_tests = 4, executed_tests = 5
  ├─ Test 8 FAILED → failed_tests = 2, executed_tests = 6
  ├─ Test 9 PASSED → passed_tests = 5, executed_tests = 7
  └─ Test 10 SKIPPED → skipped_tests = 3

Final Summary:
================================================================================
CSV-DRIVEN TEST EXECUTION SUMMARY
================================================================================
Total Tests Collected: 10
Executed: 7
Skipped: 3
Passed: 5
Failed: 2
================================================================================
```

---

## Error Handling Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                  Error Handling Strategy                        │
└─────────────────────────────────────────────────────────────────┘

Configuration Errors:
  ├─ config.yaml not found
  │  └─ Raise: FileNotFoundError
  │     └─ Message: "Configuration file not found: ..."
  │
  ├─ Invalid environment (not SIT/UAT/PROD)
  │  └─ Raise: ValueError
  │     └─ Message: "Invalid environment '...' Must be one of: ..."
  │
  └─ YAML syntax error
     └─ Raise: YAMLError
        └─ Message: "Error parsing config.yaml: ..."

CSV Errors:
  ├─ CSV file not found
  │  └─ Raise: FileNotFoundError
  │     └─ Message: "CSV file for environment '...' not found: ..."
  │
  ├─ Missing required columns (Test_Case_Name, Execute)
  │  └─ Raise: ValueError
  │     └─ Message: "CSV is missing required columns: ..."
  │
  └─ Invalid CSV format
     └─ Raise: ValueError
        └─ Message: "Invalid CSV format: ..."

Execution Errors:
  ├─ Read_Test_Data() called outside test
  │  └─ Raise: RuntimeError
  │     └─ Message: "No execution context set. Are you calling this from within a test?"
  │
  ├─ Column not found in CSV
  │  └─ Raise: KeyError
  │     └─ Message: "Column '...' not found in CSV."
  │
  └─ Test assertion fails
     └─ Caught and logged
     └─ CSV updated with failure status

All Errors:
  ├─ Logged to console (ERROR level)
  ├─ Logged to file (logs/execution.log)
  └─ Test marked as FAILED
```

---

## Memory Management

```
┌─────────────────────────────────────────────────────────────────┐
│                  Resource Management                            │
└─────────────────────────────────────────────────────────────────┘

Singletons (Single instance):
  ├─ ConfigManager
  │  └─ Loaded once, reused for all config access
  │  └─ No memory duplication
  │
  ├─ Logger
  │  └─ Single logger instance
  │  └─ File handles managed
  │
  ├─ CSVManager
  │  └─ Created per usage
  │  └─ CSV data released after read/write
  │
  └─ ExecutionContext
     └─ Singleton with per-thread contexts
     └─ Cleaned up after each test
     └─ No memory leaks

Lazy Loading:
  ├─ Config loaded only once at initialization
  ├─ CSV loaded only when accessed
  ├─ Rows loaded only when needed
  └─ Context cleared after each test

Performance:
  ├─ Minimal logging overhead (buffered)
  ├─ CSV operations: O(n) where n = CSV rows
  ├─ Context operations: O(1) average case
  └─ No memory leaks (proper cleanup)
```

---

## Integration Points

```
┌─────────────────────────────────────────────────────────────────┐
│              Framework Integration Points                       │
└─────────────────────────────────────────────────────────────────┘

Pytest Integration:
  ├─ pytest_configure() → Framework initialization
  ├─ pytest_collection_modifyitems() → Test filtering
  ├─ Fixtures (autouse) → Context management
  ├─ pytest_runtest_logreport() → Result tracking
  └─ pytest_sessionfinish() → Summary reporting

Configuration Integration:
  ├─ config.yaml → Environment selection
  └─ YAML parsing → Configuration loading

Test Integration:
  ├─ Test functions → Use Read_Test_Data()
  ├─ Test functions → Use Write_Test_Data()
  └─ Fixtures → Auto-inject data

CSV Integration:
  ├─ Test_Data/{env}.csv → Data source
  ├─ Read operations → Data access
  ├─ Write operations → Result persistence
  └─ Real-time updates → Immediate save

Logging Integration:
  ├─ Console output → Live feedback
  ├─ File output → logs/execution.log
  └─ Error reporting → Detailed messages

Existing Framework Integration:
  ├─ Playwright fixtures → Page object
  ├─ Pytest-playwright → Browser management
  ├─ Allure reporting → Test reporting (optional)
  └─ Existing utilities → No conflicts
```

---

This comprehensive architecture ensures:
✅ Clean separation of concerns
✅ Thread-safe operations
✅ Proper error handling
✅ Memory efficiency
✅ Extensible design
✅ Production-grade reliability
