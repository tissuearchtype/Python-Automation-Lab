# Python Automation – Lab Tasks

## Milestone 1 – Selenium with Python

### Tier 1: Core Fundamentals & Locators
*Focus: Mastering element identification, synchronization, and basic browser actions.*

**Assignment 1: The Multi-Locator Challenge**
- Task: Navigate to a login page (e.g., SauceDemo). Find and interact with the username field using `By.ID`, the password field using `By.NAME`, and the login button using `By.XPATH`.
- Validation: Assert that the resulting page URL contains `/inventory.html` after logging in.

**Assignment 2: Synchronization & Explicit Waits**
- Task: Navigate to a page with dynamic content (e.g., an AJAX loader or a "Start" button that reveals text after 5 seconds).
- Constraint: Do not use `time.sleep()`. Implement `WebDriverWait` along with `expected_conditions` to wait until the text element is visible before extracting it.

**Assignment 3: Dynamic Dropdowns & Checkboxes**
- Task: Open a flight booking or registration form containing multiple checkboxes and a search-as-you-type autocomplete dropdown.
- Task Steps: Select specific checkboxes, verify their state using `.is_selected()`, type into the dropdown, and loop through the suggested results to select a matching option.

### Tier 2: Advanced User Interactions
*Focus: Handling complex web behaviors like overlays, pop-ups, and data structures.*

**Assignment 4: JavaScript Alerts and Confirms**
- Task: Trigger a JavaScript Alert, a Confirm Box, and a Prompt Box on a practice page.
- Task Steps: Accept the first alert, dismiss the confirm box, and use `driver.switch_to.alert.send_keys()` to input text into the prompt before submitting.

**Assignment 5: The HTML Web Table Extractor**
- Task: Find a page containing a multi-column dynamic data table (e.g., a stock list or user directory).
- Task Steps: Write a script to iterate through rows and columns. Locate a specific row by matching a name string, and retrieve the corresponding value from the "Status" or "Price" column next to it.

**Assignment 6: Windows, Tabs, and Iframes**
- Task: Open a page that contains an embedded iframe and a button that opens a new browser tab.
- Task Steps: Use `driver.switch_to.frame()` to interact with elements inside the iframe. Then, click the tab button, use `driver.window_handles` to switch context to the new tab, grab its title, close it, and switch back to the main layout.

---

## Milestone 2 – Unit Test Frameworks & Page Object Model

**Assignment 7: Page Object Model (POM) Restructure**
- Task: Take your working scripts from Tier 1 and restructure them into a Page Object Model design pattern.
- Architecture: Create separate page classes (e.g., `LoginPage`, `DashboardPage`) containing only locator definitions and UI methods. Keep your actual test assertions completely separate from the locators.

**Assignment 8: Data-Driven Automation (DDT)**
- Task: Build a login script that reads multiple test cases from an external source (such as an Excel file via pandas or a local JSON/CSV file).
- Execution: Loop through the test data to execute combinations of correct/incorrect usernames and passwords, asserting that the proper validation errors show up for each.

**Assignment 9: PyTest Integration with HTML Reporting**
- Task: Convert your setup to run via PyTest.
- Implementation: Use PyTest fixtures for driver initialization and teardown (opening and closing the browser cleanly). Run your test suite from the terminal and configure it to auto-generate an HTML execution report with embedded screenshots of any failed test steps.

---

## Milestone 3 – Python BDD Restful Automation (Behave)

**Assignment 1 – Scenario 1: Implementation of Selenium Python and Behave BDD**
- Objective: Setup Python BDD framework and debug and run automation framework for end to end scenarios.
- Tools and Platforms: Behave (BDD framework for Python), PyCharm setup as an IDE.

**Assignment 2 – Scenario 2: Use of test data driven Automation in Python Behave Framework**
- Objective: Perform Python automations using Python Behave Framework.
- Tools and Platforms: Python, Behave, PyCharm Community.
- Day-wise Tasks: Day 1-4: Adapt Python BDD framework for API automation.

**Assignment 3 – Scenario 3: Selenium Page Object Model in the Python Behave Framework**
- Objective: Debug and optimize a web application automations using behave framework and Gherkin language.
- Tools and Platforms: Behave, Python.
- Day-wise Tasks: Leverage Behave framework for test data driven approach.

---

## Milestone 4 – Robot Framework

1. **Basic Syntax and Keywords**
   - Create a Robot Framework test case to open a web browser and navigate to a specific URL.
   - Use the "Input Text" keyword to fill in a form field on a webpage.
   - Write a test case to verify the presence of a specific element on a webpage using the "Page Should Contain Element" keyword.
2. **Variables and Data-Driven Automation**
   - Implement a test case that uses variables to store data like usernames and passwords.
   - Create a data-driven test that reads test data from an external file and performs the same set of actions on multiple data sets.
3. **Custom Keywords and Libraries**
   - Build a custom Robot Framework keyword using Python to perform a specific action, such as calculating the sum of two numbers.
   - Utilize the "BuiltIn" library to manipulate strings or perform mathematical operations within your test cases.
4. **Assertions and Verification**
   - Write a test case that performs an action and then uses an assertion to check whether the expected outcome matches the actual result.
   - Implement a test case that verifies the response of an API request using the "Should Be Equal As Strings" keyword.
5. **Test Setup and Teardown**
   - Set up a test suite with a common test setup that opens a browser and logs in before each test case.
   - Define a test teardown that logs out or cleans up resources after each test case.
6. **Tags and Test Execution**
   - Assign tags to test cases and test suites and execute only those tests with a specific tag using the "--include" or "--exclude" command-line options.
   - Run your tests in parallel by utilizing the "--processes" option.
7. **Reports and Logs**
   - Execute a test suite and generate an HTML report that includes details about test cases and their outcomes.
   - Use the "Log" keyword to write custom log messages during test execution for debugging purposes.
