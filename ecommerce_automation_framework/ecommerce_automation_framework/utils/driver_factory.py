"""
Creates and configures the Selenium WebDriver instance. Tests never call
selenium.webdriver directly - they always go through this factory, so
switching browsers or adding headless mode later only requires a change
here, not in every test.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from utils.config_reader import CONFIG


def get_driver():
    browser = CONFIG.get("browser", "chrome").lower()
    headless = CONFIG.get("headless", False)

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options,
        )

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options,
        )

    else:
        raise ValueError(f"Unsupported browser in config.yaml: {browser}")

    driver.implicitly_wait(CONFIG.get("implicit_wait", 5))
    if not headless:
        driver.maximize_window()
    return driver
