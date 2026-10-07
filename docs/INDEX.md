# Documentation Index

Welcome to the CSV-Driven Test Execution Framework documentation! This folder contains all comprehensive guides and references.

## 📚 Quick Navigation

### Getting Started
- **[README_CSV_FRAMEWORK.md](README_CSV_FRAMEWORK.md)** - Complete framework guide
  - Setup and installation
  - Component descriptions
  - API reference
  - Usage examples
  - Best practices
  - Troubleshooting

### Quick References
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick start guide
  - 30-second setup
  - Common commands
  - CSV format reference
  - Debugging tips
  - Code examples

### Technical Documentation
- **[ARCHITECTURE_DIAGRAMS.md](ARCHITECTURE_DIAGRAMS.md)** - System design
  - Execution flow diagrams
  - Component architecture
  - Data flow
  - Thread safety model
  - Integration points

- **[IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md)** - What's implemented
  - Feature checklist
  - File structure
  - Design decisions
  - Tested scenarios

- **[FRAMEWORK_SUMMARY.md](FRAMEWORK_SUMMARY.md)** - Implementation overview
  - What was created
  - Quick start
  - Key features
  - Example code

- **[FRAMEWORK_ARCHITECTURE.md](FRAMEWORK_ARCHITECTURE.md)** - Architecture overview
  - Original framework documentation

---

## 🎯 Where to Start?

### For First Time Users
1. Start with **QUICK_REFERENCE.md** (5 min read)
2. Run your first test: `pytest -v`
3. Check **README_CSV_FRAMEWORK.md** for details

### For Detailed Understanding
1. Read **README_CSV_FRAMEWORK.md** (comprehensive)
2. Review **ARCHITECTURE_DIAGRAMS.md** for design
3. Check **IMPLEMENTATION_CHECKLIST.md** for what's included

### For Troubleshooting
- Check **QUICK_REFERENCE.md** → Debugging section
- Read **README_CSV_FRAMEWORK.md** → Troubleshooting section
- Review logs in `logs/execution.log`

---

## 📖 Document Overview

| Document | Length | Purpose |
|----------|--------|---------|
| README_CSV_FRAMEWORK.md | 500+ lines | Complete API reference and guide |
| QUICK_REFERENCE.md | 300+ lines | Quick commands and snippets |
| ARCHITECTURE_DIAGRAMS.md | 400+ lines | System design and flows |
| FRAMEWORK_SUMMARY.md | 200+ lines | Implementation overview |
| IMPLEMENTATION_CHECKLIST.md | 300+ lines | Features and design decisions |
| FRAMEWORK_ARCHITECTURE.md | Original docs | Project architecture |

---

## 🔑 Key Concepts

### Framework Components
- **ConfigManager** - Load and manage configuration
- **CSVManager** - Read/write test data
- **ExecutionContext** - Thread-safe test data context
- **Logger** - Centralized logging
- **Reusable Functions** - `Read_Test_Data()`, `Write_Test_Data()`

### Files to Know
- `config/config.yaml` - Environment configuration
- `Test_Data/{env}.csv` - Test data
- `src/utilities/` - Framework utilities
- `src/common/` - Reusable functions
- `tests/conftest.py` - Pytest integration
- `logs/execution.log` - Execution logs

---

## 💡 Common Tasks

### Run Tests
```bash
pytest -v
```

### Change Environment
Edit `config/config.yaml`:
```yaml
environment: SIT  # or UAT, PROD
```

### Add New Test
1. Create test function in `tests/`
2. Add row to `Test_Data/SIT.csv`
3. Set Execute = Yes
4. Done! ✅

### Read Test Data
```python
from src.common.reusable_functions import Read_Test_Data
data = Read_Test_Data("ColumnName")
```

### Write Results
```python
from src.common.reusable_functions import Write_Test_Data
Write_Test_Data("Result", "Passed")
```

---

## 📋 CSV Format Reminder

```csv
Test_Case_Name,Execute,Field_1,Field_2,Result,Comments
test_login,Yes,user1,pass1,,
test_checkout,No,data1,data2,,
```

**Rules:**
- `Test_Case_Name` must match function name exactly
- `Execute` = "Yes" to run, "No" to skip
- `Result` auto-updated by tests
- `Comments` auto-updated with notes

---

## 🎯 Next Steps

1. **Understand the structure** → Open [README_CSV_FRAMEWORK.md](README_CSV_FRAMEWORK.md)
2. **Run your first test** → `pytest -v`
3. **Check the results** → Look at `Test_Data/SIT.csv` Result column
4. **View logs** → Check `logs/execution.log`
5. **Add more tests** → Follow the pattern

---

## ❓ FAQ

**Q: Where is the framework code?**  
A: In `src/utilities/` and `src/common/`

**Q: How do I run tests?**  
A: `pytest -v` or `pytest`

**Q: How do I control which tests run?**  
A: Edit `Test_Data/SIT.csv` and set Execute = Yes/No

**Q: Where are the test results saved?**  
A: In the CSV file (Result column) and in `logs/execution.log`

**Q: Can I run tests in parallel?**  
A: Yes! Framework is thread-safe. Use `pytest -n auto`

**Q: How do I add test data?**  
A: Use `Read_Test_Data("ColumnName")` in your test

**Q: How do I update results?**  
A: Use `Write_Test_Data("Result", "Passed")` in your test

---

## 📞 Support

- Check the relevant documentation file above
- Review the code comments in `src/` files
- Check `logs/execution.log` for execution details
- Run `pytest -v --log-cli-level=DEBUG` for detailed logs

---

**Happy Testing! 🎉**

Start with [QUICK_REFERENCE.md](QUICK_REFERENCE.md) if you're new to the framework.
