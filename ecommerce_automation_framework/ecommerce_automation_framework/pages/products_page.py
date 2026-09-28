from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class ProductsPage(BasePage):
    SEARCH_INPUT = (By.ID, "search_product")
    SEARCH_BUTTON = (By.ID, "submit_search")
    SEARCHED_PRODUCTS_TITLE = (By.XPATH, "//h2[contains(text(),'Searched Products')]")
    PRODUCT_ITEMS = (By.CSS_SELECTOR, ".product-image-wrapper")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".productinfo p")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, ".productinfo .add-to-cart")
    ADD_TO_CART_MODAL = (By.ID, "cartModal")
    CONTINUE_SHOPPING_BUTTON = (By.CSS_SELECTOR, "button.close-modal")
    VIEW_CART_LINK = (By.CSS_SELECTOR, "#cartModal a[href='/view_cart']")

    def load(self):
        self.open("/products")

    def search_product(self, keyword):
        self.type_text(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)

    def is_search_results_header_visible(self):
        return self.is_visible(self.SEARCHED_PRODUCTS_TITLE)

    def get_product_names(self):
        # Collapse any double/irregular whitespace the site's markup
        # produces (e.g. "Sleeveless  Dress") so names compare reliably
        # against the cart page later.
        return [" ".join(el.text.split()) for el in self.find_all(self.PRODUCT_NAMES)]

    def add_first_product_to_cart(self):
        # The site only reveals/activates the "Add to cart" button on a real
        # mouseover of the product image, so we hover with ActionChains
        # before clicking - a JS-injected click alone does not trigger it.
        product_wrapper = self.find_all(self.PRODUCT_ITEMS)[0]

        # Scroll it to the vertical center of the viewport (not just "into
        # view") so it isn't sitting behind the top banner ad that this
        # site displays, which otherwise intercepts the click.
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            product_wrapper,
        )
        ActionChains(self.driver).move_to_element(product_wrapper).perform()

        add_to_cart_button = self.wait.until(
            EC.element_to_be_clickable(self.ADD_TO_CART_BUTTONS)
        )
        # A native .click() can still be intercepted by an ad iframe that
        # overlaps the button's coordinates. A JS click dispatches the
        # click event directly on the element, bypassing that overlap.
        self.driver.execute_script("arguments[0].click();", add_to_cart_button)

        # A JS-dispatched click doesn't always fully trigger the site's
        # Bootstrap "Added!" modal the first time. Give it a short window,
        # and if the modal hasn't appeared, retry with a real mouse click
        # (which fires the full native event sequence jQuery listens for).
        if not self.is_visible(self.ADD_TO_CART_MODAL, timeout=5):
            ActionChains(self.driver).move_to_element(
                add_to_cart_button
            ).click().perform()

        # Now wait properly for the modal - if it still hasn't shown,
        # this will raise a clear TimeoutException.
        self.wait.until(EC.visibility_of_element_located(self.ADD_TO_CART_MODAL))

    def click_view_cart_from_modal(self):
        self.wait.until(EC.visibility_of_element_located(self.ADD_TO_CART_MODAL))
        self.click(self.VIEW_CART_LINK)

    def close_add_to_cart_modal(self):
        if self.is_visible(self.CONTINUE_SHOPPING_BUTTON, timeout=3):
            self.click(self.CONTINUE_SHOPPING_BUTTON)
