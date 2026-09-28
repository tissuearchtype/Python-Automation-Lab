# Milestone 2 – Lab Report
## Unit Test Frameworks & Page Object Model (Assignments 7–9)

| Field | Details |
|---|---|
| Name | Ishika Mandal |
| Milestone | M2 – PyTest, Page Object Model |
| Language / Tool | Python 3, Selenium 4, PyTest, pytest-html |

> A complete, larger implementation of the same concepts (config, base page, page classes, CSV test data, screenshot utility, reports) is available in the **`ecommerce_automation_framework`** folder of this repository. The code below is a compact SauceDemo version that demonstrates each assignment.

### Environment Setup
```bash
pip install selenium pytest pytest-html
```
(`pytest-html` version 4.x is assumed.)

### Project Structure Used
```
lab_m2/
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   ├── login_page.py
│   └── inventory_page.py
├── tests/
│   ├── conftest.py
│   ├── test_login_pom.py
│   └── test_login_ddt.py
├── testdata/
│   └── login_data.csv
├── reports/
├── pytest.ini
└── requirements.txt
```

---

## Assignment 7: Page Object Model (POM) Restructure

**Task:** Restructure the Tier-1 login script (Assignment 1) into POM. Page classes hold only locators and UI methods; assertions live only in the test files.

**`pages/__init__.py`** – empty file.

**`pages/base_page.py`**
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url):
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def text_of(self, locator):
        return self.find(locator).text

    def current_url(self):
        return self.driver.current_url
```

**`pages/login_page.py`** (locators + UI methods only)
```python
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"

    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//input[@id='login-button']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def open_page(self):
        self.open(self.URL)

    def login(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        return self.text_of(self.ERROR_MESSAGE)
```

**`pages/inventory_page.py`** (the "Dashboard" page)
```python
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CSS_SELECTOR, ".title")
    ITEMS = (By.CSS_SELECTOR, ".inventory_item")
    ADD_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")

    def get_title(self):
        return self.text_of(self.TITLE)

    def item_count(self):
        self.find(self.TITLE)
        return len(self.driver.find_elements(*self.ITEMS))

    def add_backpack_to_cart(self):
        self.click(self.ADD_BACKPACK)

    def cart_count(self):
        return self.text_of(self.CART_BADGE)
```

**`tests/conftest.py`** (basic fixture, extended in Assignment 9)
```python
import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    drv = webdriver.Chrome()
    drv.maximize_window()
    yield drv
    drv.quit()
```

**`tests/test_login_pom.py`** (assertions only here)
```python
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


def test_valid_login_lands_on_inventory(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    assert inventory.get_title() == "Products"
    assert "/inventory.html" in inventory.current_url()


def test_inventory_shows_six_items(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    assert inventory.item_count() == 6


def test_add_item_updates_cart_badge(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    inventory.add_backpack_to_cart()
    assert inventory.cart_count() == "1"
```

**Run:** `python -m pytest tests/test_login_pom.py -v`

**Expected output:**
```
tests/test_login_pom.py::test_valid_login_lands_on_inventory PASSED
tests/test_login_pom.py::test_inventory_shows_six_items PASSED
tests/test_login_pom.py::test_add_item_updates_cart_badge PASSED
============ 3 passed in ~15s ============
```
📸 _Screenshot here_

---

## Assignment 8: Data-Driven Automation (DDT)

**Task:** Read multiple login combinations from an external CSV file, run them in a loop and assert the correct validation message for each.

**`testdata/login_data.csv`**
```csv
username,password,expected_error
standard_user,secret_sauce,
locked_out_user,secret_sauce,Sorry this user has been locked out
invalid_user,wrong_pass,Username and password do not match any user in this service
,secret_sauce,Username is required
standard_user,,Password is required
```
(An empty `expected_error` means the login should succeed.)

**`tests/test_login_ddt.py`**
```python
import csv
from pathlib import Path

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

DATA_FILE = Path(__file__).resolve().parent.parent / "testdata" / "login_data.csv"


def load_login_data():
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        return [
            (row["username"], row["password"], row["expected_error"])
            for row in csv.DictReader(f)
        ]


@pytest.mark.parametrize("username, password, expected_error", load_login_data())
def test_login_combinations(driver, username, password, expected_error):
    login = LoginPage(driver)
    login.open_page()
    login.login(username, password)

    if expected_error == "":
        inventory = InventoryPage(driver)
        assert inventory.get_title() == "Products"
    else:
        # the locked-out message has a comma and period, so strip them before comparing
        message = login.get_error_message().replace(".", "").replace(",", "")
        assert expected_error in message
```

**Run:** `python -m pytest tests/test_login_ddt.py -v`

**Expected output:**
```
tests/test_login_ddt.py::test_login_combinations[standard_user-secret_sauce-] PASSED
tests/test_login_ddt.py::test_login_combinations[locked_out_user-secret_sauce-Sorry this user has been locked out] PASSED
tests/test_login_ddt.py::test_login_combinations[invalid_user-wrong_pass-Username and password do not match any user in this service] PASSED
tests/test_login_ddt.py::test_login_combinations[-secret_sauce-Username is required] PASSED
tests/test_login_ddt.py::test_login_combinations[standard_user--Password is required] PASSED
============ 5 passed ============
```
📸 _Screenshot here_

---

## Assignment 9: PyTest Integration with HTML Reporting

**Task:** Run through PyTest using fixtures for setup/teardown and auto-generate an HTML report with embedded screenshots for failed tests.

**`tests/conftest.py`** (final version – replaces the basic one)
```python
import pytest
import pytest_html
from selenium import webdriver


@pytest.fixture
def driver(request):
    drv = webdriver.Chrome()
    drv.maximize_window()
    request.node.driver = drv          # expose driver to the report hook
    yield drv                          # test runs here
    drv.quit()                         # teardown: browser always closes


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call" and report.failed:
        drv = getattr(item, "driver", None)
        if drv is not None:
            screenshot = drv.get_screenshot_as_base64()
            extras.append(pytest_html.extras.png(screenshot, "Failure screenshot"))
    report.extras = extras
```

**`pytest.ini`**
```ini
[pytest]
testpaths = tests
addopts = -v --html=reports/report.html --self-contained-html
```

**`requirements.txt`**
```
selenium
pytest
pytest-html
```

**Run (from the project root):**
```bash
python -m pytest
```
The report is created automatically at `reports/report.html`. Open it in a browser.

**To demonstrate a failure screenshot:** temporarily change an expected value (for example `assert inventory.item_count() == 7`) and re-run. The failed test row in the report will have the embedded screenshot.

**Expected output:**
```
collected 8 items
tests/test_login_ddt.py ..... PASSED
tests/test_login_pom.py ... PASSED
- Generated html report: file:///.../reports/report.html -
============ 8 passed ============
```
📸 _Screenshot: terminal output_
📸 _Screenshot: HTML report (with a failed test and its embedded screenshot)_

---

## Conclusion
Assignments 7–9 show a maintainable framework: POM separates locators from assertions, CSV-driven tests cover many login combinations, and PyTest fixtures plus `pytest-html` give clean setup/teardown and reports with failure screenshots.
