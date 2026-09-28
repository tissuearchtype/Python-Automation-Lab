# Milestone 1 – Lab Report
## Selenium with Python (Assignments 1–6)

| Field | Details |
|---|---|
| Name | Ishika Mandal |
| Milestone | M1 – Automation with Selenium |
| Language / Tool | Python 3, Selenium 4, Google Chrome |

### Environment Setup
```bash
python -m venv venv
venv\Scripts\activate          # Windows   (Mac/Linux: source venv/bin/activate)
pip install selenium
```
Selenium 4.6+ includes Selenium Manager, so ChromeDriver is downloaded automatically. No manual driver setup is needed.

> **Note:** All practice sites are public demo sites. If a locator stops working because the site was updated, inspect the element in Chrome DevTools and adjust the locator.

---

## Assignment 1: The Multi-Locator Challenge

**Task:** Log in to SauceDemo using `By.ID` (username), `By.NAME` (password) and `By.XPATH` (login button). Assert that the URL contains `/inventory.html`.

**File:** `assignment1_multi_locator.py`
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()

try:
    driver.get("https://www.saucedemo.com/")

    # By.ID for username
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    # By.NAME for password
    driver.find_element(By.NAME, "password").send_keys("secret_sauce")
    # By.XPATH for login button
    driver.find_element(By.XPATH, "//input[@id='login-button']").click()

    # Validation
    WebDriverWait(driver, 10).until(EC.url_contains("/inventory.html"))
    assert "/inventory.html" in driver.current_url, f"Unexpected URL: {driver.current_url}"
    print("PASS: Logged in. Current URL ->", driver.current_url)
finally:
    driver.quit()
```

**Run:** `python assignment1_multi_locator.py`

**Expected output:**
```
PASS: Logged in. Current URL -> https://www.saucedemo.com/inventory.html
```
📸 _Screenshot: paste terminal output / inventory page here_

---

## Assignment 2: Synchronization & Explicit Waits

**Task:** Open a page whose text appears only after a "Start" click (≈5 s). Use `WebDriverWait` + `expected_conditions`, with no `time.sleep()`.

**File:** `assignment2_explicit_wait.py`
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()

try:
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")
    wait = WebDriverWait(driver, 15)

    start_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='start']/button")))
    start_btn.click()

    # Wait until the hidden text becomes visible
    text_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#finish h4")))
    extracted = text_element.text
    print("Extracted text:", extracted)
    assert extracted == "Hello World!"
    print("PASS: Text extracted after explicit wait")
finally:
    driver.quit()
```

**Run:** `python assignment2_explicit_wait.py`

**Expected output:**
```
Extracted text: Hello World!
PASS: Text extracted after explicit wait
```
📸 _Screenshot here_

---

## Assignment 3: Dynamic Dropdowns & Checkboxes

**Task:** On a form with checkboxes and an autocomplete field: select checkboxes, verify with `.is_selected()`, type into the autosuggest box and loop through suggestions to select a match.

**File:** `assignment3_dropdown_checkbox.py`
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()

try:
    driver.get("https://rahulshettyacademy.com/dropdownsPractise/")
    wait = WebDriverWait(driver, 10)

    # ---- Checkboxes ----
    family_chk = driver.find_element(By.CSS_SELECTOR, "input[id*='friendsandfamily']")
    senior_chk = driver.find_element(By.CSS_SELECTOR, "input[id*='SeniorCitizenDiscount']")

    print("Before click  -> Friends&Family selected:", family_chk.is_selected())
    assert not family_chk.is_selected()

    family_chk.click()
    senior_chk.click()

    print("After click   -> Friends&Family selected:", family_chk.is_selected())
    print("After click   -> Senior Citizen selected:", senior_chk.is_selected())
    assert family_chk.is_selected() and senior_chk.is_selected()

    # ---- Autocomplete dropdown ----
    auto_box = driver.find_element(By.ID, "autosuggest")
    auto_box.send_keys("ind")

    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.ui-menu-item a")))
    suggestions = driver.find_elements(By.CSS_SELECTOR, "li.ui-menu-item a")
    print("Suggestions:", [s.text for s in suggestions])

    for option in suggestions:
        if option.text == "India":
            option.click()
            break

    selected_value = auto_box.get_attribute("value")
    print("Selected value:", selected_value)
    assert selected_value == "India"
    print("PASS: Checkboxes and autocomplete verified")
finally:
    driver.quit()
```

**Run:** `python assignment3_dropdown_checkbox.py`

**Expected output:**
```
Before click  -> Friends&Family selected: False
After click   -> Friends&Family selected: True
After click   -> Senior Citizen selected: True
Suggestions: ['British Indian Ocean Territory', 'India', 'Indonesia']
Selected value: India
PASS: Checkboxes and autocomplete verified
```
📸 _Screenshot here_

---

## Assignment 4: JavaScript Alerts and Confirms

**Task:** Trigger an Alert, a Confirm box and a Prompt box. Accept the alert, dismiss the confirm, and type into the prompt using `switch_to.alert.send_keys()`.

**File:** `assignment4_js_alerts.py`
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

try:
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")

    # 1. JS Alert -> accept
    driver.find_element(By.XPATH, "//button[text()='Click for JS Alert']").click()
    wait.until(EC.alert_is_present())
    alert = driver.switch_to.alert
    print("Alert text:", alert.text)
    alert.accept()
    print("Result:", driver.find_element(By.ID, "result").text)

    # 2. JS Confirm -> dismiss
    driver.find_element(By.XPATH, "//button[text()='Click for JS Confirm']").click()
    wait.until(EC.alert_is_present())
    confirm = driver.switch_to.alert
    print("Confirm text:", confirm.text)
    confirm.dismiss()
    result = driver.find_element(By.ID, "result").text
    print("Result:", result)
    assert "Cancel" in result

    # 3. JS Prompt -> send keys, then accept
    driver.find_element(By.XPATH, "//button[text()='Click for JS Prompt']").click()
    wait.until(EC.alert_is_present())
    prompt = driver.switch_to.alert
    prompt.send_keys("Selenium Python")
    prompt.accept()
    result = driver.find_element(By.ID, "result").text
    print("Result:", result)
    assert "Selenium Python" in result
    print("PASS: Alert, Confirm and Prompt handled")
finally:
    driver.quit()
```

**Run:** `python assignment4_js_alerts.py`

**Expected output:**
```
Alert text: I am a JS Alert
Result: You successfully clicked an alert
Confirm text: I am a JS Confirm
Result: You clicked: Cancel
Result: You entered: Selenium Python
PASS: Alert, Confirm and Prompt handled
```
📸 _Screenshot here_

---

## Assignment 5: The HTML Web Table Extractor

**Task:** Iterate through rows/columns of a data table, find a row by a name string and read the value from the neighbouring column ("Due" is used as the Price/Status-style column here).

**File:** `assignment5_web_table.py`
```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.maximize_window()

try:
    driver.get("https://the-internet.herokuapp.com/tables")

    headers = [th.text for th in driver.find_elements(By.XPATH, "//table[@id='table1']/thead/tr/th")]
    print("Columns:", headers)

    rows = driver.find_elements(By.XPATH, "//table[@id='table1']/tbody/tr")
    print(f"Total rows: {len(rows)}\n")

    target_name = "Smith"
    due_index = headers.index("Due")
    last_name_index = headers.index("Last Name")
    found_value = None

    for row in rows:
        cells = [td.text for td in row.find_elements(By.TAG_NAME, "td")]
        print(cells)                                   # iterate rows and columns
        if cells[last_name_index] == target_name:      # match by name string
            found_value = cells[due_index]

    print(f"\nDue amount for '{target_name}': {found_value}")
    assert found_value is not None, "Row not found"
    assert found_value == "$50.00"
    print("PASS: Table value retrieved")
finally:
    driver.quit()
```

**Run:** `python assignment5_web_table.py`

**Expected output:**
```
Columns: ['Last Name', 'First Name', 'Email', 'Due', 'Web Site', 'Action']
Total rows: 4

['Smith', 'John', 'jsmith@gmail.com', '$50.00', 'http://www.jsmith.com', 'edit delete']
['Bach', 'Frank', 'fbach@yahoo.com', '$51.00', 'http://www.frank.com', 'edit delete']
['Doe', 'Jason', 'jdoe@hotmail.com', '$100.00', 'http://www.jdoe.com', 'edit delete']
['Conway', 'Tim', 'tconway@earthlink.net', '$50.00', 'http://www.timconway.com', 'edit delete']

Due amount for 'Smith': $50.00
PASS: Table value retrieved
```
📸 _Screenshot here_

---

## Assignment 6: Windows, Tabs, and Iframes

**Task:** On a page with an iframe and a "new tab" button: switch into the iframe, then open the new tab, switch using `window_handles`, read its title, close it and return to the main window.

**File:** `assignment6_windows_iframes.py`
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

try:
    driver.get("https://rahulshettyacademy.com/AutomationPractice/")
    main_window = driver.current_window_handle
    main_title = driver.title
    print("Main page title:", main_title)

    # ---- Iframe ----
    iframe = wait.until(EC.presence_of_element_located((By.ID, "courses-iframe")))
    driver.execute_script("arguments[0].scrollIntoView(true);", iframe)
    driver.switch_to.frame(iframe)
    iframe_text = driver.find_element(By.TAG_NAME, "body").text
    print("Iframe content length:", len(iframe_text))
    assert len(iframe_text) > 0
    driver.switch_to.default_content()          # back to main layout

    # ---- New tab ----
    open_tab_btn = driver.find_element(By.ID, "opentab")
    driver.execute_script("arguments[0].scrollIntoView(true);", open_tab_btn)
    open_tab_btn.click()
    wait.until(EC.number_of_windows_to_be(2))

    for handle in driver.window_handles:
        if handle != main_window:
            driver.switch_to.window(handle)
            break

    print("New tab title:", driver.title)
    driver.close()                              # close new tab

    driver.switch_to.window(main_window)        # switch back
    assert driver.title == main_title
    print("PASS: Returned to main window ->", driver.title)
finally:
    driver.quit()
```

**Run:** `python assignment6_windows_iframes.py`

**Expected output:**
```
Main page title: Practice Page
Iframe content length: <some number greater than 0>
New tab title: <title of the newly opened tab>
PASS: Returned to main window -> Practice Page
```
📸 _Screenshot here_

---

## Conclusion
All six Selenium assignments cover the M1 objectives: multiple locator strategies, explicit waits without `sleep`, form controls, JavaScript alerts, web tables, and iframe/window switching.
