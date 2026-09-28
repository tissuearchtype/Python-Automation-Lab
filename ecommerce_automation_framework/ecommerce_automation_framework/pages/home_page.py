from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):
    SIGNUP_LOGIN_LINK = (By.XPATH, "//a[contains(text(),'Signup / Login')]")
    PRODUCTS_LINK = (By.XPATH, "//a[contains(text(),'Products')]")
    LOGGED_IN_AS = (By.XPATH, "//a[contains(text(),'Logged in as')]")

    def load(self):
        self.open("/")

    def go_to_login(self):
        self.click(self.SIGNUP_LOGIN_LINK)

    def go_to_products(self):
        self.click(self.PRODUCTS_LINK)

    def is_user_logged_in(self):
        return self.is_visible(self.LOGGED_IN_AS)
