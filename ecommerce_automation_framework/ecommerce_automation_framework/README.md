# E-Commerce Selenium Automation Framework

Selenium WebDriver + PyTest + Page Object Model (POM) framework automating
the Login and Product Search functionality of an e-commerce web application.

Built as a Capstone project demonstrating: Unittest/PyTest, Page Object
Model, Utility Classes, Configuration Management, CSV-driven test data,
automatic screenshots on failure, and HTML test reporting.

**Target application:** https://automationexercise.com/

---

## 🎥 Demo Video

**Watch the demo here:** https://drive.google.com/file/d/17AmCbhwqii7Fi7eSCpELO4xtYuyf-tfZ/view?usp=sharing

---

## Overview

This framework automates two core flows of an e-commerce site:

- **Login** — validates both invalid-credential rejection and successful
  login with a real account
- **Product Search** — searches for products (single and data-driven,
  multi-keyword via CSV), and verifies an item can be added to the cart

It's built to be maintainable and scalable: locators live only in page
object classes, configuration lives only in a YAML file, and every test
run produces an HTML report plus automatic screenshots on any failure.

---

## Features

| Requirement | How it's implemented |
|---|---|
| Unittest + PyTest | PyTest (unittest's modern, compatible successor) with native `assert` statements and fixtures |
| Page Object Model (POM) | One class per page (`Home`, `Login`, `Products`, `Cart`) in `pages/`, all inheriting shared wait/click/type helpers from `base_page.py` |
| Utility Classes | `config_reader.py`, `driver_factory.py`, `screenshot_util.py` in `utils/` |
| Configuration Management | Single `config/config.yaml` — base URL, browser, wait times, test credentials |
| Test Data Handling (CSV) | `testdata/search_data.csv`, consumed via PyTest `parametrize` |
| Screenshots on Failure | Automatic capture via a `pytest_runtest_makereport` hook in `tests/conftest.py` — zero extra code per test |
| HTML Reporting | Self-contained `reports/report.html` generated on every run via `pytest-html` |

---

## Tech Stack

- Python 3.9+
- Selenium WebDriver 4.x
- PyTest 8.x + pytest-html
- webdriver-manager (automatic ChromeDriver management)
- PyYAML

---

## Project Structure

```
ecommerce_automation_framework/
├── config/
│   └── config.yaml          # URL, browser, waits, test credentials
├── pages/                   # Page Object Model classes
│   ├── base_page.py         # shared Selenium wait/click/type helpers
│   ├── home_page.py
│   ├── login_page.py
│   ├── products_page.py
│   └── cart_page.py
├── utils/
│   ├── config_reader.py     # loads config.yaml
│   ├── driver_factory.py    # creates the WebDriver (Chrome/Firefox)
│   └── screenshot_util.py   # saves timestamped screenshots
├── testdata/
│   └── search_data.csv      # keywords used for data-driven search tests
├── tests/
│   ├── conftest.py          # driver fixture + auto screenshot-on-failure
│   ├── test_login.py
│   └── test_search.py
├── reports/                 # generated: report.html + screenshots/
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Setup & Run

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\Activate.ps1        # Windows PowerShell
# source venv/bin/activate       # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) add a real account's credentials to config/config.yaml
#    for the valid-login test — see comments inside that file

# 4. Run the full suite
pytest

# Or run a subset:
pytest -m login
pytest -m search
```

After a run, open `reports/report.html` for the pass/fail summary, or
check `reports/screenshots/` for failure captures.

---

## Test Cases Covered

1. **Invalid login** — verifies an error message on wrong credentials
2. **Valid login** — verifies successful login with a real account
3. **Product search** — verifies search results render for a keyword
4. **Data-driven search** — same search test run across multiple keywords from CSV
5. **Add to cart** — searches a product, adds it to the cart, verifies it appears on the cart page

---

## Author

Built as part of a Python Test Automation Capstone Assignment.
