"""
Login functionality tests.

test_invalid_login runs with zero setup - it always works because it
never needs a real account.

test_valid_login needs a real account. Create one at
https://automationexercise.com/signup and put its email/password into
config/config.yaml under valid_email / valid_password before running it.
"""

import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from utils.config_reader import CONFIG


@pytest.mark.login
def test_invalid_login_shows_error(driver):
    login_page = LoginPage(driver)
    login_page.load()

    login_page.login("not_a_real_user@example.com", "WrongPassword123")

    assert login_page.has_error_message(), "Expected an error message for invalid login"
    assert "incorrect" in login_page.get_error_message().lower()


@pytest.mark.login
def test_valid_login_succeeds(driver):
    email = CONFIG.get("valid_email")
    password = CONFIG.get("valid_password")

    if not email or "your_test_email" in email:
        pytest.skip(
            "Set a real valid_email / valid_password in config/config.yaml "
            "(create an account at automationexercise.com/signup first)"
        )

    login_page = LoginPage(driver)
    login_page.load()
    login_page.login(email, password)

    home_page = HomePage(driver)
    assert home_page.is_user_logged_in(), "Expected to see 'Logged in as' after valid login"
