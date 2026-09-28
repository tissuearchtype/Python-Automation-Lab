# Milestone 3 – Lab Report
## Python BDD Restful Automation with Behave (Scenarios 1–3)

| Field | Details |
|---|---|
| Name | Ishika Mandal |
| Milestone | M3 – Python BDD (Behave) |
| Tools | Python 3, Behave, Selenium 4, Requests, PyCharm |

### Environment Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install behave selenium requests
```

### Project Structure (used for all three scenarios)
```
behave_lab/
├── behave.ini
├── requirements.txt
└── features/
    ├── environment.py
    ├── e2e_shopping.feature
    ├── api_data_driven.feature
    ├── pom_login.feature
    ├── pages/
    │   ├── __init__.py
    │   ├── base_page.py
    │   ├── login_page.py
    │   └── inventory_page.py
    └── steps/
        ├── e2e_steps.py
        ├── api_steps.py
        └── pom_steps.py
```

**`behave.ini`**
```ini
[behave]
paths = features
format = pretty
show_timings = true
```

**`requirements.txt`**
```
behave
selenium
requests
```

---

## Scenario 1: Implementation of Selenium Python and Behave BDD

**Objective:** Set up the Python BDD framework in PyCharm, then debug and run an end-to-end scenario.

**Day 1 – Setup:** Install Python and PyCharm, create the project and virtual environment, install `behave`, create the `features/` and `features/steps/` folders.

**Day 2–4 – Build, run and debug an end-to-end flow** (login → add to cart → checkout → order confirmation).

**`features/environment.py`** (hooks shared by all scenarios)
```python
import os
import re
from selenium import webdriver


def before_all(context):
    context.headless = context.config.userdata.get("headless", "false").lower() == "true"


def before_scenario(context, scenario):
    # Only start a browser for scenarios tagged @web (API scenarios do not need one)
    if "web" in scenario.effective_tags:
        options = webdriver.ChromeOptions()
        if context.headless:
            options.add_argument("--headless=new")
        context.driver = webdriver.Chrome(options=options)
        context.driver.maximize_window()


def after_step(context, step):
    # Screenshot on failure
    if step.status == "failed" and hasattr(context, "driver"):
        os.makedirs("screenshots", exist_ok=True)
        safe_name = re.sub(r"[^A-Za-z0-9_-]", "_", step.name)[:60]
        context.driver.save_screenshot(f"screenshots/{safe_name}.png")


def after_scenario(context, scenario):
    if hasattr(context, "driver"):
        context.driver.quit()
```

**`features/e2e_shopping.feature`**
```gherkin
@web
Feature: End to end shopping on SauceDemo

  @smoke
  Scenario: Customer completes an order
    Given the user is on the SauceDemo login page
    When the user logs in with username "standard_user" and password "secret_sauce"
    And the user adds the backpack to the cart
    And the user checks out with first name "Test", last name "User" and zip "700001"
    Then the order confirmation message "Thank you for your order!" is displayed
```

**`features/steps/e2e_steps.py`**
```python
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def wait_for(context, locator):
    return WebDriverWait(context.driver, 10).until(EC.element_to_be_clickable(locator))


@given("the user is on the SauceDemo login page")
def step_open_login(context):
    context.driver.get("https://www.saucedemo.com/")


@when('the user logs in with username "{username}" and password "{password}"')
def step_login(context, username, password):
    context.driver.find_element(By.ID, "user-name").send_keys(username)
    context.driver.find_element(By.ID, "password").send_keys(password)
    context.driver.find_element(By.ID, "login-button").click()


@when("the user adds the backpack to the cart")
def step_add_backpack(context):
    wait_for(context, (By.ID, "add-to-cart-sauce-labs-backpack")).click()


@when('the user checks out with first name "{first}", last name "{last}" and zip "{zip_code}"')
def step_checkout(context, first, last, zip_code):
    wait_for(context, (By.CLASS_NAME, "shopping_cart_link")).click()
    wait_for(context, (By.ID, "checkout")).click()
    wait_for(context, (By.ID, "first-name")).send_keys(first)
    context.driver.find_element(By.ID, "last-name").send_keys(last)
    context.driver.find_element(By.ID, "postal-code").send_keys(zip_code)
    context.driver.find_element(By.ID, "continue").click()
    wait_for(context, (By.ID, "finish")).click()


@then('the order confirmation message "{message}" is displayed')
def step_verify_confirmation(context, message):
    element = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
    )
    assert element.text == message, f"Expected '{message}' but got '{element.text}'"
```

**Run:**
```bash
behave features/e2e_shopping.feature
```

**Debugging in PyCharm (Community edition):**
1. `Run` → `Edit Configurations` → `+` → **Python**.
2. Choose **Module name** (instead of Script path) and enter `behave`.
3. Parameters: `features/e2e_shopping.feature`. Working directory: the project root.
4. Click on the line number of a step function to set a **breakpoint**, then press the **Debug** (bug) icon and use Step Over / Step Into and the Variables pane to inspect `context`.

**Expected output:**
```
Feature: End to end shopping on SauceDemo

  @smoke
  Scenario: Customer completes an order
    Given the user is on the SauceDemo login page ... passed
    When the user logs in with username "standard_user" and password "secret_sauce" ... passed
    And the user adds the backpack to the cart ... passed
    And the user checks out with first name "Test", last name "User" and zip "700001" ... passed
    Then the order confirmation message "Thank you for your order!" is displayed ... passed

1 feature passed, 0 failed, 0 skipped
1 scenario passed, 0 failed, 0 skipped
5 steps passed, 0 failed, 0 skipped
```
📸 _Screenshot: PyCharm project + terminal output_
📸 _Screenshot: debugger paused on a breakpoint_

---

## Scenario 2: Test Data Driven Automation in Python Behave Framework (API)

**Objective:** Adapt the Behave framework for REST API automation, driven by `Scenario Outline` example tables.

**Day 1–4:** Add the `requests` library, write API feature files, generic reusable step definitions, and drive test data from `Examples` tables. (Public test API: JSONPlaceholder.)

**`features/api_data_driven.feature`**
```gherkin
@api
Feature: JSONPlaceholder REST API – data driven tests

  Scenario Outline: Fetch a post and verify its owner
    Given the API base url is "https://jsonplaceholder.typicode.com"
    When I send a GET request to "/posts/<post_id>"
    Then the response status code should be 200
    And the response field "userId" should be <user_id>

    Examples:
      | post_id | user_id |
      | 1       | 1       |
      | 11      | 2       |
      | 21      | 3       |
      | 100     | 10      |

  Scenario Outline: Create a new post
    Given the API base url is "https://jsonplaceholder.typicode.com"
    When I send a POST request to "/posts" with title "<title>" and body "<body>"
    Then the response status code should be 201
    And the response field "title" should equal "<title>"

    Examples:
      | title           | body                 |
      | Behave Lab      | First data driven    |
      | API Automation  | Second data driven   |
```

**`features/steps/api_steps.py`**
```python
import requests
from behave import given, when, then


@given('the API base url is "{base_url}"')
def step_base_url(context, base_url):
    context.base_url = base_url
    context.session = requests.Session()
    context.session.headers.update({"Content-Type": "application/json; charset=UTF-8"})


@when('I send a GET request to "{endpoint}"')
def step_get(context, endpoint):
    context.response = context.session.get(context.base_url + endpoint, timeout=15)


@when('I send a POST request to "{endpoint}" with title "{title}" and body "{body}"')
def step_post(context, endpoint, title, body):
    payload = {"title": title, "body": body, "userId": 1}
    context.response = context.session.post(context.base_url + endpoint, json=payload, timeout=15)


@then("the response status code should be {code:d}")
def step_status(context, code):
    assert context.response.status_code == code, (
        f"Expected {code} but got {context.response.status_code}"
    )


@then('the response field "{field}" should be {value:d}')
def step_field_int(context, field, value):
    actual = context.response.json()[field]
    assert actual == value, f"{field}: expected {value} but got {actual}"


@then('the response field "{field}" should equal "{value}"')
def step_field_text(context, field, value):
    actual = context.response.json()[field]
    assert actual == value, f"{field}: expected '{value}' but got '{actual}'"
```

**Run:**
```bash
behave features/api_data_driven.feature
```
To run only API scenarios by tag: `behave --tags=@api`

**Expected output:**
```
1 feature passed, 0 failed, 0 skipped
6 scenarios passed, 0 failed, 0 skipped
24 steps passed, 0 failed, 0 skipped
```
📸 _Screenshot here_

---

## Scenario 3: Selenium Page Object Model in the Python Behave Framework

**Objective:** Debug and optimize web automation using Behave and Gherkin, applying the Page Object Model and a data-driven approach.

**Day-wise tasks:** Leverage the Behave framework for a test-data-driven approach. Steps stay thin and delegate all UI work to page classes.

**`features/pages/__init__.py`** – empty file.

**`features/pages/base_page.py`**
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
```

**`features/pages/login_page.py`**
```python
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def open_page(self):
        self.open(self.URL)

    def login(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def error_message(self):
        return self.text_of(self.ERROR)
```

**`features/pages/inventory_page.py`**
```python
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CSS_SELECTOR, ".title")

    def title(self):
        return self.text_of(self.TITLE)
```

**`features/pom_login.feature`** (data-driven with Scenario Outline)
```gherkin
@web
Feature: Login using Page Object Model

  Scenario Outline: Login with different credentials
    Given the login page is open
    When the user logs in as "<username>" with password "<password>"
    Then the result should be "<result>"

    Examples: Valid user
      | username      | password     | result   |
      | standard_user | secret_sauce | Products |

    Examples: Invalid users
      | username        | password     | result                                                                    |
      | locked_out_user | secret_sauce | Epic sadface: Sorry, this user has been locked out.                       |
      | invalid_user    | wrong_pass   | Epic sadface: Username and password do not match any user in this service |
      |                 | secret_sauce | Epic sadface: Username is required                                        |
      | standard_user   |              | Epic sadface: Password is required                                        |
```

**`features/steps/pom_steps.py`**
```python
from behave import given, when, then
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@given("the login page is open")
def step_open(context):
    context.login_page = LoginPage(context.driver)
    context.login_page.open_page()


@when('the user logs in as "{username}" with password "{password}"')
def step_login(context, username, password):
    context.login_page.login(username, password)


@then('the result should be "{result}"')
def step_result(context, result):
    if result == "Products":
        actual = InventoryPage(context.driver).title()
    else:
        actual = context.login_page.error_message()
    assert actual == result, f"Expected '{result}' but got '{actual}'"
```

> **Note:** Behave treats empty table cells as empty strings. With the empty-username row, `login()` types an empty string, so the site returns "Username is required".

**Debug and optimization done in this scenario**
- Replaced fixed sleeps with explicit waits inside `BasePage` (faster and more reliable).
- Moved browser start-up and shutdown to `environment.py` hooks (`before_scenario` / `after_scenario`), so no step file repeats it.
- Added an `after_step` hook that saves a screenshot to `screenshots/` for any failed step.
- Added a `headless` user-data flag for faster runs.
- Kept steps thin and reusable; all locators live in page classes.

**Run:**
```bash
behave features/pom_login.feature
behave features/pom_login.feature -D headless=true      # optimized headless run
behave --tags=@web                                      # all browser scenarios
```

**Expected output:**
```
1 feature passed, 0 failed, 0 skipped
5 scenarios passed, 0 failed, 0 skipped
15 steps passed, 0 failed, 0 skipped
```
📸 _Screenshot here_

---

## Conclusion
Scenario 1 established the Behave + PyCharm setup with an end-to-end run and debugging. Scenario 2 applied data-driven `Scenario Outline` tables to API testing. Scenario 3 combined Gherkin, Page Object Model and data-driven tests, with hooks for setup, teardown, screenshots and headless execution.
