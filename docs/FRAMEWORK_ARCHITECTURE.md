# Framework Architecture Overview

## High-Level Vision
This is an **Enterprise-Grade Test Automation Framework** for YETI Commerce Platform built on:
- **Playwright** for cross-browser automation
- **Pytest** for test execution
- **Allure** for rich test reporting
- **Python** for clean, maintainable code

The framework follows the **Page Object Model (POM)** pattern to separate test logic from UI interaction logic. Designed to test critical YETI e-commerce flows including product customization, add-to-cart, checkout, and order placement.

---

## Architecture Layers

```
┌─────────────────────────────────────────────────────┐
│          Tests (test_*.py)                          │
│   - Contains test scenarios and assertions         │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│     Page Objects (src/pages/*.py)                   │
│   - Encapsulates UI selectors & interactions        │
│   - Methods represent user actions                  │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│      Utilities & Helpers (src/utilities/)           │
│   - Config management                              │
│   - Constants                                       │
│   - Accessibility helpers                          │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│     Playwright & Browser (via Conftest)             │
│   - Browser initialization                         │
│   - Session management                             │
│   - Fixtures & setup/teardown                      │
└─────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. **Page Objects** (`src/pages/`)
**Purpose:** Encapsulate page elements and interactions

**Example: CheckoutPage**
```python
class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_field = page.get_by_role("textbox", name="Email Address")
        self.continue_button = page.get_by_role("button", name="Continue To Payment")
    
    def fill_email(self, email: str):
        # Business logic abstracted from test
        self.email_field.fill(email)
    
    def proceed_to_payment(self):
        self.continue_button.click()
```

**Benefits:**
- ✅ UI changes only affect the page object, not 50 tests
- ✅ Reusable methods across multiple tests
- ✅ Readable test code: `self.login_page.login(user, pwd)` vs raw `page.get_by_test_id(...)`

---

### 2. **Tests** (`tests/`)
**Purpose:** Define test scenarios using page objects

**Example: Add-to-Cart Test**
```python
class TestATC:
    def test_atc_customize_rambler(self, page: Page):
        customize_page = CustomizePage(page)
        customize_page.close_filter()
        customize_page.click_customize()
        customize_page.select_drinkware()
        customize_page.add_to_bag()
```

**Why this is clean:**
- Test logic is business-focused, not technical
- No raw Playwright selectors in tests
- Tests mirror actual user workflows on YETI platform

---

### 3. **Configuration Management** (`src/utilities/config.py`)
**Purpose:** Support YETI environments (Staging, Production)

**How it works:**
```python
# Define environments
YETI_STG = "https://storefront:Yeti2017@stg.yeti.com/"
YETI_PROD = "https://storefront:credentials@yeti.com/"

# Runtime selection
def get_base_url():
    env = os.getenv("TEST_ENV", "yeti_stg")
    # Returns appropriate URL based on environment
```

**Usage:**
```powershell
# Staging environment (default)
$env:TEST_ENV="yeti_stg"; python -m pytest tests/ -v

# Production environment
$env:TEST_ENV="yeti_prod"; python -m pytest tests/ -v
```

**Benefits:**
- ✅ Same tests run across YETI staging and production
- ✅ No hardcoded credentials or URLs in code
- ✅ Easy to add new YETI environments (dev, QA, prod)

---

### 4. **Fixtures & Setup** (`tests/conftest.py`)
**Purpose:** Centralized setup, teardown, and shared functionality

**Key Fixtures:**

| Fixture | Scope | Purpose |
|---------|-------|---------|
| `goto` | function | Auto-navigate to base URL before each test |
| `page` | function | Playwright page object (provided by pytest-playwright) |
| `browser_context_args` | function | Configure browser settings (viewport, user agent, permissions) |
| `axe_playwright` | session | Accessibility testing helper |
| `attach_playwright_results` | function | Attach screenshots/traces on failure |

**Why conftest.py matters:**
- Fixture are run automatically before/after tests
- Reduces code duplication across tests
- Centralized test lifecycle management

---

### 5. **Enums** (`src/enums/`)
**Purpose:** Type-safe constants for test data

**Example: User enum**
```python
class User(Enum):
    STANDARD_USER = "standard_user"
    LOCKED_OUT_USER = "locked_out_user"
```

**Why enums?**
- ✅ Prevents typos (IDE autocomplete)
- ✅ Single source of truth for test data
- ✅ Self-documenting code

---

## Data Flow: How a Test Executes

```
1. User runs: pytest tests/login_test.py
   ↓
2. pytest_configure() hook loads TEST_ENV and sets base_url
   ↓
3. Playwright launches browser (chromium, firefox, webkit)
   ↓
4. browser_context_args fixture configures browser settings
   ↓
5. goto fixture navigates page to base_url
   ↓
6. Test method executes:
   - Creates page object: LoginPage(page)
   - Calls high-level methods: login_page.login(user, pwd)
   - Page object interacts with UI via Playwright
   - Test asserts expected results
   ↓
7. attach_playwright_results fixture captures artifacts on failure
   ↓
8. Allure collects metadata and generates report
```

---

## Key Design Patterns

### 1. **Page Object Model (POM)**
- ✅ Separates test logic from UI interaction
- ✅ Improves maintainability
- ✅ Enables code reuse

### 2. **Fixture-Based Setup**
- ✅ Centralized test initialization
- ✅ Automatic cleanup
- ✅ Dependency injection via pytest

### 3. **Environment Abstraction**
- ✅ Runtime configuration selection
- ✅ Multiple environment support
- ✅ Credentials management

### 4. **Allure Integration**
- ✅ Rich test reporting with steps
- ✅ Screenshots on failure
- ✅ Trace/video recordings
- ✅ Customizable severity/categories

---

## Technology Stack

| Component | Purpose | Why? |
|-----------|---------|------|
| **Playwright** | Browser automation | Cross-browser, reliable, modern |
| **Pytest** | Test framework | Easy to learn, powerful fixtures, large ecosystem |
| **pytest-playwright** | Pytest + Playwright integration | Automatic browser/page management |
| **Allure** | Test reporting | Beautiful reports, CI/CD integration, detailed traces |
| **Ruff** | Code linting | Fast, modern Python linter |
| **pytest-split** | Parallel test execution | Faster CI/CD pipelines |

---

## Folder Structure & Responsibilities

```
Playwright-Python-Example/
├── src/
│   ├── pages/              # YETI Page Object Models
│   │   ├── customize_page.py   # Product customization flow
│   │   ├── checkout_page.py    # Checkout and payment forms
│   │   └── (additional YETI pages as needed)
│   ├── enums/              # Type-safe constants
│   │   └── User.py         # YETI user types/roles
│   └── utilities/          # Shared utilities
│       ├── config.py       # YETI environment configuration
│       ├── constants.py    # YETI application constants
│       └── axe_helper.py   # Accessibility testing helpers
│
├── tests/
│   ├── conftest.py         # Global fixtures & YETI setup
│   ├── atc_test.py         # Add-to-cart customization tests
│   ├── e2e_order_test.py   # End-to-end order flow tests
│   └── (additional YETI test suites)
│
├── pyproject.toml          # Dependencies & pytest config
├── FRAMEWORK_ARCHITECTURE.md # This document
└── README.md               # YETI test automation guide
```

---

## Execution Flow: Real Example

### Running the E2E Order Test:

```powershell
$env:TEST_ENV="yeti_stg"; python -m pytest tests/e2e_order_test.py -v
```

### What Happens Behind the Scenes:

1. **Configuration Phase**
   - `pytest_configure()` reads `TEST_ENV=yeti_stg`
   - Base URL set to `https://storefront:Yeti2017@stg.yeti.com/`

2. **Test Collection**
   - Pytest discovers `TestE2EOrder.test_e2e_order`

3. **Setup Phase**
   - Browser launched (chromium, headless=False for visibility)
   - Context created with YETI-specific settings (user agent, permissions)
   - Page navigated to YETI staging homepage

4. **Test Execution**
   - CustomizePage object customizes Rambler product with Basketball design
   - Product added to cart
   - Checkout page collects shipping info (address, phone)
   - CheckoutPage handles payment form (card details in secure iframes)
   - Order placed successfully
   - Order confirmation page verified

5. **Assertion & Verification**
   - Screenshots captured throughout flow
   - Order confirmation page loaded
   - Results attached to Allure report

6. **Teardown Phase**
   - Browser closed
   - Allure metadata collected with video recording
   - Report generated with full transaction trail

---

## Best Practices Implemented

| Practice | Implementation | Benefit |
|----------|---|---|
| **DRY (Don't Repeat Yourself)** | Page objects, fixtures, enums | Less code, easier maintenance |
| **SOLID Principles** | Single Responsibility per class | Clear, testable code |
| **Separation of Concerns** | Test logic vs UI interaction | Different teams can own different layers |
| **Environment Abstraction** | Config-based URL selection | Works across dev/staging/prod |
| **Automated Reporting** | Allure integration | No manual report creation |
| **CI/CD Ready** | Parallel execution, artifact collection | Fast feedback, easy integration |

---

## How to Extend the Framework

### Adding a New YETI Test:

1. **Create Page Object** (if testing new YETI page)
   ```python
   # src/pages/cart_page.py
   class CartPage:
       def __init__(self, page: Page):
           self.page = page
       
       @allure.step("Click view cart")
       def view_cart(self):
           self.page.get_by_role("link", name="Cart").click()
   ```

2. **Create Test**
   ```python
   # tests/cart_test.py
   class TestCart:
       @pytest.mark.devRun
       @allure.title("Verify cart totals calculation")
       def test_cart_totals(self, page: Page):
           cart_page = CartPage(page)
           cart_page.view_cart()
           # Assertions...
   ```

3. **Run Test**
   ```powershell
   $env:TEST_ENV="yeti_stg"; python -m pytest tests/cart_test.py -v
   ```

---

## Summary

This framework demonstrates **production-grade test automation for YETI Commerce** by:

1. ✅ **Separation of Concerns** → YETI tests vs page objects vs utilities
2. ✅ **Reusability** → Page objects for checkout, customize, cart prevent duplication
3. ✅ **Maintainability** → YETI UI changes impact only page objects, not 50+ tests
4. ✅ **Scalability** → Easy to add new YETI test suites (inventory, search, filtering, etc.)
5. ✅ **Visibility** → Allure reports with videos, traces, and payment form recordings
6. ✅ **Best Practices** → POM, fixtures, type hints, iframe handling for payment forms

This architecture enables YETI teams to build robust, maintainable e-commerce test automation covering critical user flows: customization → checkout → payment → order confirmation.
