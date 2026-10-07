# Project Structure

Clean, organized folder structure for the Playwright Python automation framework with CSV-driven test execution.

```
Playwright-Python-Example/
│
├── 📂 config/
│   └── config.yaml                    # ✅ Environment configuration (SIT/UAT/PROD)
│
├── 📂 Test_Data/
│   ├── SIT.csv                        # ✅ Test data for SIT environment
│   ├── UAT.csv                        # ✅ Test data for UAT environment
│   └── PROD.csv                       # ✅ Test data for PROD environment
│
├── 📂 src/                            # ✅ Application source code
│   ├── utilities/                     # Framework utilities
│   │   ├── __init__.py
│   │   ├── logger.py                  # Centralized logging
│   │   ├── config_manager.py          # Configuration loader
│   │   ├── csv_manager.py             # CSV read/write operations
│   │   ├── execution_context.py       # Thread-safe context manager
│   │   ├── axe_helper.py              # Accessibility helper (existing)
│   │   ├── constants.py               # Constants (existing)
│   │   └── config.py                  # Configuration (existing)
│   │
│   ├── common/                        # Reusable functions
│   │   ├── __init__.py
│   │   └── reusable_functions.py      # Read_Test_Data(), Write_Test_Data()
│   │
│   └── pages/                         # Page object models (existing)
│
├── 📂 tests/                          # ✅ Test files
│   ├── __init__.py
│   ├── conftest.py                    # Pytest configuration with CSV hooks
│   └── travel_mug_30oz_agave_teal_test.py  # Example test
│
├── 📂 logs/                           # 🔄 Auto-created on first run
│   └── execution.log                  # Execution logs (auto-created)
│
├── 📂 test_results/                   # Test results (auto-created)
│   └── screenshots/                   # Test screenshots
│
├── 📂 docs/                           # 📚 Documentation (read these!)
│   ├── INDEX.md                       # Documentation index (START HERE)
│   ├── README_CSV_FRAMEWORK.md        # Complete framework guide
│   ├── QUICK_REFERENCE.md             # Quick start & commands
│   ├── ARCHITECTURE_DIAGRAMS.md       # System design & flows
│   ├── FRAMEWORK_SUMMARY.md           # Implementation overview
│   ├── IMPLEMENTATION_CHECKLIST.md    # Features & design decisions
│   └── FRAMEWORK_ARCHITECTURE.md      # Original architecture docs
│
├── 📂 resources/                      # Static resources (existing)
│   └── images/
│
├── 📂 allure-results/                 # Allure reports (auto-created)
│
├── pytest.ini                         # ✅ Pytest configuration
├── requirements.txt                   # ✅ Python dependencies
├── README.md                          # Project overview (original)
├── LICENSE
├── SECURITY.md
└── .gitignore
```

---

## 📁 Folder Purposes

### Core Framework Folders (Required)

| Folder | Purpose |
|--------|---------|
| `config/` | Environment and framework configuration |
| `Test_Data/` | Environment-specific test data in CSV format |
| `src/utilities/` | Core framework utilities and helpers |
| `src/common/` | Reusable functions for tests |
| `tests/` | Test files and pytest configuration |

### Auto-Generated Folders (Runtime)

| Folder | Purpose |
|--------|---------|
| `logs/` | Test execution logs (auto-created) |
| `test_results/` | Test artifacts and screenshots |
| `allure-results/` | Allure report data |

### Documentation Folder

| Folder | Purpose |
|--------|---------|
| `docs/` | All documentation files (kept separate) |

---

## 🚀 Quick Navigation

### To Run Tests
```bash
pytest -v
```

### To Understand the Framework
Start here: `docs/INDEX.md`

### To Configure Environment
Edit: `config/config.yaml`

### To Add Test Data
Edit: `Test_Data/SIT.csv` (or UAT.csv, PROD.csv)

### To Check Results
View: `Test_Data/SIT.csv` (Result column)
Or: `logs/execution.log`

---

## 📚 Documentation Organization

All documentation has been moved to the `docs/` folder for cleaner structure:

- 📖 **docs/INDEX.md** - Start here! Documentation index
- 📖 **docs/README_CSV_FRAMEWORK.md** - Complete guide (500+ lines)
- 📖 **docs/QUICK_REFERENCE.md** - Quick start (300+ lines)
- 📖 **docs/ARCHITECTURE_DIAGRAMS.md** - System design (400+ lines)
- 📖 **docs/FRAMEWORK_SUMMARY.md** - Implementation overview
- 📖 **docs/IMPLEMENTATION_CHECKLIST.md** - Features & design
- 📖 **docs/FRAMEWORK_ARCHITECTURE.md** - Original docs

---

## 🎯 Key Files Explained

### Configuration
- **config/config.yaml** - Choose environment and logging level

### Test Data
- **Test_Data/SIT.csv** - Defines which tests to run in SIT environment
- **Test_Data/UAT.csv** - Defines which tests to run in UAT environment
- **Test_Data/PROD.csv** - Defines which tests to run in PROD environment

### Framework Code
- **src/utilities/config_manager.py** - Loads configuration
- **src/utilities/csv_manager.py** - Manages CSV data
- **src/utilities/execution_context.py** - Thread-safe test context
- **src/utilities/logger.py** - Centralized logging
- **src/common/reusable_functions.py** - Read_Test_Data(), Write_Test_Data()

### Test Configuration
- **tests/conftest.py** - Pytest hooks for CSV integration
- **pytest.ini** - Pytest settings

### Dependencies
- **requirements.txt** - All Python dependencies

---

## ✨ Framework Features

✅ **CSV-driven test control** - Enable/disable tests via CSV  
✅ **Environment management** - Separate CSV per environment  
✅ **Dynamic test data** - Read from and write to CSV  
✅ **Thread-safe** - Ready for parallel execution  
✅ **Auto-logging** - Comprehensive execution logs  
✅ **Auto-result tracking** - Results saved to CSV  
✅ **Clean architecture** - Modular and extensible  

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Edit `config/config.yaml`:
```yaml
environment: SIT  # or UAT, PROD
```

### 3. Define Tests
Edit `Test_Data/SIT.csv`:
```csv
Test_Case_Name,Execute,Field_1,Field_2,Result,Comments
test_example,Yes,value1,value2,,
```

### 4. Run Tests
```bash
pytest -v
```

### 5. Check Results
- View CSV: `Test_Data/SIT.csv` (Result column updated)
- View Logs: `logs/execution.log`

---

## 📖 Learn More

1. **New to this framework?** → Read `docs/INDEX.md`
2. **Quick start?** → Read `docs/QUICK_REFERENCE.md`
3. **Need details?** → Read `docs/README_CSV_FRAMEWORK.md`
4. **Want architecture?** → Read `docs/ARCHITECTURE_DIAGRAMS.md`

---

## 💡 Common Commands

```bash
# Run all executable tests
pytest -v

# Run specific test file
pytest tests/test_file.py -v

# Run with debug logging
pytest -v --log-cli-level=DEBUG

# Run with Allure report
pytest --alluredir=allure-results
allure serve allure-results

# Run specific test
pytest tests/test_file.py::TestClass::test_method -v
```

---

## 🎯 Example Usage

### Using Test Data
```python
from src.common.reusable_functions import Read_Test_Data, Write_Test_Data

class TestExample:
    def test_login(self, page):
        username = Read_Test_Data("Field_1")  # Read from CSV
        password = Read_Test_Data("Field_2")
        
        # Your test logic...
        
        Write_Test_Data("Result", "Passed")   # Write to CSV
```

### In CSV
```csv
Test_Case_Name,Execute,Field_1,Field_2,Result,Comments
test_login,Yes,user1,pass1,,
test_login,Yes,user2,pass2,,
```

---

## 📊 Project Statistics

- **Framework Components**: 5 core utilities
- **Documentation**: 7 comprehensive guides
- **Test Files**: Environment-specific (SIT, UAT, PROD)
- **Lines of Code**: 2000+ (framework + utilities)
- **Lines of Docs**: 2500+ (all guides)

---

## ✅ What's Included

✅ Complete CSV-driven framework  
✅ Thread-safe execution context  
✅ Production-grade logging  
✅ Comprehensive documentation  
✅ Example tests  
✅ Configuration management  
✅ Error handling  
✅ Best practices  

---

## 🚀 Next Steps

1. Open `docs/INDEX.md` for complete documentation index
2. Run `pytest -v` to execute your first test
3. Check `Test_Data/SIT.csv` for test results
4. Review `logs/execution.log` for detailed logs

---

**Ready to run your tests?** Execute `pytest -v` now! 🎉
