"""
Every page object inherits from BasePage. It wraps raw Selenium calls
(find_element, click, send_keys...) with explicit waits, so no page
object or test ever has to write its own WebDriverWait boilerplate.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

from utils.config_reader import CONFIG


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, CONFIG.get("explicit_wait", 15))

    def open(self, path=""):
        self.driver.get(CONFIG["base_url"] + path)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        # This demo site shows ad iframes that can float over any element
        # and intercept a native click. Scroll the target to the center of
        # the viewport first (away from the fixed header/banner ads), and
        # if a native click still gets intercepted, fall back to a JS
        # click, which bypasses the overlapping-element hit-test entirely.
        self.scroll_to(element)
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    def type_text(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find(locator).text

    def is_visible(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def scroll_to(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            element,
        )

    def accept_alert_if_present(self, timeout=3):
        """Handles unexpected JS alerts/popups so a test never hangs on one."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            return True
        except TimeoutException:
            return False