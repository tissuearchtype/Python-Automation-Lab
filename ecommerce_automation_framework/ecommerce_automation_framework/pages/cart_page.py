from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    CART_PRODUCT_NAMES = (By.CSS_SELECTOR, ".cart_description h4 a")
    CART_QUANTITIES = (By.CSS_SELECTOR, ".cart_quantity button")

    def load(self):
        self.open("/view_cart")

    def get_cart_product_names(self):
        return [" ".join(el.text.split()) for el in self.find_all(self.CART_PRODUCT_NAMES)]

    def get_cart_quantities(self):
        return [el.text.strip() for el in self.find_all(self.CART_QUANTITIES)]

    def is_product_in_cart(self, product_name):
        return product_name in self.get_cart_product_names()
