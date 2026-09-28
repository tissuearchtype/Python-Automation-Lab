# Milestone 4 – Lab Report
## Robot Framework (Topics 1–7)

| Field | Details |
|---|---|
| Name | Ishika Mandal |
| Milestone | M4 – Robot Framework |
| Tools | Python 3, Robot Framework 6.1+, SeleniumLibrary, RequestsLibrary, Pabot |

### Environment Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install robotframework robotframework-seleniumlibrary robotframework-requests robotframework-pabot
```

### Project Structure Used
```
robot_lab/
├── data/
│   └── users.csv
├── libraries/
│   └── CustomLib.py
├── resources/
│   └── common.resource
├── tests/
│   ├── 01_basic_syntax.robot
│   ├── 02_variables_ddt.robot
│   ├── 03_custom_keywords.robot
│   ├── 04_assertions.robot
│   ├── 05_setup_teardown.robot
│   ├── 06_tags_execution.robot
│   └── 07_reports_logs.robot
└── results/
```

**`resources/common.resource`** (shared variables and keywords used by several topics)
```robotframework
*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}               https://www.saucedemo.com/
${BROWSER}           chrome
${VALID_USER}        standard_user
${VALID_PASSWORD}    secret_sauce

*** Keywords ***
Open SauceDemo
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window

Login With Credentials
    [Arguments]    ${username}    ${password}
    Input Text     id:user-name    ${username}
    Input Text     id:password    ${password}
    Click Button   id:login-button

Logout
    Click Button                     id:react-burger-menu-btn
    Wait Until Element Is Visible    id:logout_sidebar_link
    Click Link                       id:logout_sidebar_link
    Wait Until Element Is Visible    id:login-button
```

---

## 1. Basic Syntax and Keywords

**Task:** Open a browser and navigate to a URL; fill a form field with `Input Text`; verify an element with `Page Should Contain Element`.

**`tests/01_basic_syntax.robot`**
```robotframework
*** Settings ***
Library          SeleniumLibrary
Test Teardown    Close Browser

*** Variables ***
${URL}        https://www.saucedemo.com/
${BROWSER}    chrome

*** Test Cases ***
Open Browser And Navigate To URL
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Title Should Be    Swag Labs

Fill Form Field Using Input Text
    Open Browser      ${URL}    ${BROWSER}
    Input Text        id:user-name    standard_user
    Input Password    id:password     secret_sauce
    Click Button      id:login-button
    Location Should Contain    /inventory.html

Verify Presence Of Element
    Open Browser    ${URL}    ${BROWSER}
    Page Should Contain Element    id:login-button
    Page Should Contain Element    id:user-name
    Page Should Contain Element    id:password
```

**Run:** `robot -d results tests/01_basic_syntax.robot`

**Expected output:**
```
Open Browser And Navigate To URL          | PASS |
Fill Form Field Using Input Text          | PASS |
Verify Presence Of Element                | PASS |
3 tests, 3 passed, 0 failed
```
📸 _Screenshot here_

---

## 2. Variables and Data-Driven Automation

**Task:** Use variables for credentials; build a data-driven test that reads an external file and repeats the same actions for each data set.

**`data/users.csv`**
```csv
username,password,expected
standard_user,secret_sauce,success
locked_out_user,secret_sauce,locked out
invalid_user,wrong_pass,do not match
,secret_sauce,Username is required
standard_user,,Password is required
```

**`tests/02_variables_ddt.robot`**
```robotframework
*** Settings ***
Library     OperatingSystem
Library     String
Resource    ../resources/common.resource

*** Variables ***
${CSV_FILE}    ${CURDIR}/../data/users.csv

*** Test Cases ***
Login Using Variables
    Open SauceDemo
    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}
    Location Should Contain    /inventory.html
    [Teardown]    Close Browser

Login Using Data From CSV File
    ${content}=    Get File    ${CSV_FILE}
    @{lines}=      Split To Lines    ${content}    1
    FOR    ${line}    IN    @{lines}
        @{cols}=    Split String    ${line}    ,
        Login Scenario    ${cols}[0]    ${cols}[1]    ${cols}[2]
    END

*** Keywords ***
Login Scenario
    [Arguments]    ${username}    ${password}    ${expected}
    Open SauceDemo
    Login With Credentials    ${username}    ${password}
    IF    '${expected}' == 'success'
        Location Should Contain    /inventory.html
    ELSE
        Element Should Contain    css:[data-test="error"]    ${expected}
    END
    [Teardown]    Close Browser
```

**Run:** `robot -d results tests/02_variables_ddt.robot`

**Expected output:**
```
Login Using Variables                     | PASS |
Login Using Data From CSV File            | PASS |
2 tests, 2 passed, 0 failed
```
📸 _Screenshot here_

---

## 3. Custom Keywords and Libraries

**Task:** Build a custom keyword in Python (sum of two numbers) and use the `BuiltIn` library for string and math operations.

**`libraries/CustomLib.py`**
```python
def add_two_numbers(a, b):
    """Returns the sum of two numbers. Used in Robot as: Add Two Numbers"""
    return int(a) + int(b)


def is_even(number):
    """Returns True when the number is even. Used in Robot as: Is Even"""
    return int(number) % 2 == 0
```

**`tests/03_custom_keywords.robot`**
```robotframework
*** Settings ***
Library    ../libraries/CustomLib.py

*** Test Cases ***
Sum Of Two Numbers Using Custom Keyword
    ${result}=    Add Two Numbers    10    25
    Should Be Equal As Integers    ${result}    35
    Log    Sum is ${result}

Check Even Number Using Custom Keyword
    ${flag}=    Is Even    8
    Should Be True    ${flag}

BuiltIn Math Operations
    ${product}=    Evaluate    6 * 7
    ${power}=      Evaluate    2 ** 5
    ${number}=     Convert To Integer    42
    ${total}=      Evaluate    ${number} + 8
    Should Be Equal As Integers    ${product}    42
    Should Be Equal As Integers    ${power}      32
    Should Be Equal As Integers    ${total}      50

BuiltIn String Operations
    ${full}=      Catenate    SEPARATOR=${SPACE}    Robot    Framework    Lab
    ${length}=    Get Length    ${full}
    ${upper}=     Evaluate    "${full}".upper()
    Should Be Equal As Integers    ${length}    19
    Should Be Equal    ${upper}    ROBOT FRAMEWORK LAB
    Log    Combined string: ${full}
```

**Run:** `robot -d results tests/03_custom_keywords.robot`

**Expected output:**
```
Sum Of Two Numbers Using Custom Keyword   | PASS |
Check Even Number Using Custom Keyword    | PASS |
BuiltIn Math Operations                   | PASS |
BuiltIn String Operations                 | PASS |
4 tests, 4 passed, 0 failed
```
📸 _Screenshot here_

---

## 4. Assertions and Verification

**Task:** Assert expected vs actual results, and verify an API response using `Should Be Equal As Strings`.

**`tests/04_assertions.robot`**
```robotframework
*** Settings ***
Library     RequestsLibrary
Resource    ../resources/common.resource

*** Test Cases ***
Verify Page Title Matches Expected Result
    Open SauceDemo
    ${actual}=    Get Title
    Should Be Equal    ${actual}    Swag Labs
    [Teardown]    Close Browser

Verify API Response Using Should Be Equal As Strings
    Create Session    jsonplaceholder    https://jsonplaceholder.typicode.com
    ${response}=      GET On Session     jsonplaceholder    /posts/1
    Should Be Equal As Strings    ${response.status_code}    200
    ${body}=          Set Variable    ${response.json()}
    Should Be Equal As Strings    ${body}[userId]    1
    Should Be Equal As Strings    ${body}[id]        1
```

**Run:** `robot -d results tests/04_assertions.robot`

**Expected output:**
```
Verify Page Title Matches Expected Result             | PASS |
Verify API Response Using Should Be Equal As Strings  | PASS |
2 tests, 2 passed, 0 failed
```
📸 _Screenshot here_

---

## 5. Test Setup and Teardown

**Task:** Common test setup that opens a browser and logs in before every test; teardown that logs out and cleans up after every test.

**`tests/05_setup_teardown.robot`**
```robotframework
*** Settings ***
Resource         ../resources/common.resource
Test Setup       Open Browser And Login
Test Teardown    Logout And Close Browser

*** Test Cases ***
Inventory Page Title Is Products
    [Tags]    smoke
    Element Text Should Be    css:.title    Products

Cart Icon Is Visible
    [Tags]    smoke
    Page Should Contain Element    id:shopping_cart_container

Add Item To Cart Updates Badge
    [Tags]    regression
    Click Button    id:add-to-cart-sauce-labs-backpack
    Element Text Should Be    css:.shopping_cart_badge    1

*** Keywords ***
Open Browser And Login
    Open SauceDemo
    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}
    Wait Until Location Contains    /inventory.html

Logout And Close Browser
    Run Keyword And Ignore Error    Logout
    Close Browser
```

**Run:** `robot -d results tests/05_setup_teardown.robot`

**Expected output:**
```
Inventory Page Title Is Products          | PASS |
Cart Icon Is Visible                      | PASS |
Add Item To Cart Updates Badge            | PASS |
3 tests, 3 passed, 0 failed
```
📸 _Screenshot here_

---

## 6. Tags and Test Execution

**Task:** Tag tests and suites; run selected tests with `--include` / `--exclude`; run in parallel.

**`tests/06_tags_execution.robot`**
```robotframework
*** Settings ***
Documentation    Simple tests used to demonstrate tags and parallel execution
Test Tags        demo

*** Test Cases ***
Addition Smoke Test
    [Tags]    smoke
    ${r}=    Evaluate    2 + 3
    Should Be Equal As Integers    ${r}    5

Subtraction Smoke Test
    [Tags]    smoke
    ${r}=    Evaluate    10 - 4
    Should Be Equal As Integers    ${r}    6

Multiplication Regression Test
    [Tags]    regression
    ${r}=    Evaluate    6 * 7
    Should Be Equal As Integers    ${r}    42

Division Regression Test
    [Tags]    regression
    ${r}=    Evaluate    20 / 4
    Should Be Equal As Numbers    ${r}    5
```
`Test Tags` in the Settings section tags every test in the suite with `demo` (requires Robot Framework 6.0+); `[Tags]` adds test-level tags.

**Commands:**
```bash
# Run only tests tagged smoke
robot -d results --include smoke tests/06_tags_execution.robot

# Run everything except regression tests
robot -d results --exclude regression tests/06_tags_execution.robot

# Combine tags: smoke AND demo
robot -d results --include smokeANDdemo tests/06_tags_execution.robot

# Run tagged tests across the entire tests folder
robot -d results --include smoke tests/

# Parallel execution with 2 processes (Pabot)
pabot --processes 2 --outputdir results_parallel tests/
pabot --processes 2 --include smoke --outputdir results_parallel tests/06_tags_execution.robot
```
> **Note:** `--processes` is an option of **Pabot** (`robotframework-pabot`), the parallel executor for Robot Framework. Plain `robot` does not support it. Pabot combines all results into a single `log.html`, `report.html` and `output.xml`.

**Expected output (`--include smoke`):**
```
Addition Smoke Test                       | PASS |
Subtraction Smoke Test                    | PASS |
2 tests, 2 passed, 0 failed
```
**Expected output (`--exclude regression`):** the same two smoke tests run.
📸 _Screenshot: --include run_
📸 _Screenshot: pabot parallel run_

---

## 7. Reports and Logs

**Task:** Generate an HTML report with test details and outcomes; use the `Log` keyword for custom debug messages.

**`tests/07_reports_logs.robot`**
```robotframework
*** Settings ***
Documentation    Demonstrates custom log messages and report generation

*** Test Cases ***
Custom Log Messages Demo
    Log    Test started                              INFO
    Log    This is a DEBUG message for debugging     DEBUG
    Log    Something needs attention                 WARN
    Log To Console    Printed directly on the console
    ${x}=    Set Variable    10
    Log    Value of x is ${x}
    Log    <b>Bold message using HTML</b>            html=True
    Should Be Equal As Integers    ${x}    10
    Log    Test finished successfully                INFO

Log Many Values
    Log Many    Robot    Framework    Reporting
```

**Run:**
```bash
robot --outputdir results --loglevel DEBUG --report report.html --log log.html --name "Robot Lab Suite" tests/07_reports_logs.robot
```
This produces three files in `results/`:
- `report.html`: high-level report with pass/fail statistics, tags and test details
- `log.html`: detailed keyword-level log including all custom `Log` messages (the DEBUG message is visible because of `--loglevel DEBUG`)
- `output.xml`: machine-readable results

Open `results/report.html` and `results/log.html` in a browser.

**Expected output:**
```
Test started
Printed directly on the console
[ WARN ] Something needs attention
Robot Lab Suite
Custom Log Messages Demo                  | PASS |
Log Many Values                           | PASS |
2 tests, 2 passed, 0 failed
Output:  results/output.xml
Log:     results/log.html
Report:  results/report.html
```
📸 _Screenshot: report.html_
📸 _Screenshot: log.html showing the custom log messages_

---

## Conclusion
The seven topics covered core Robot Framework skills: browser keywords, variables and CSV-driven testing, a custom Python library with `BuiltIn` keywords, assertions on UI and API responses, suite-wide setup and teardown, tag-based selection with parallel runs via Pabot, and HTML reports with custom logging.
