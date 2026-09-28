"""
Product search + cart functionality tests.
"""

import csv
import os
import pytest

from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from utils.screenshot_util import take_screenshot


def _read_search_keywords():
    csv_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "testdata",
        "search_data.csv",
    )
    with open(csv_path, newline="") as f:
        return [row["keyword"] for row in csv.DictReader(f)]


@pytest.mark.search
def test_search_product_shows_results(driver):
    products_page = ProductsPage(driver)
    products_page.load()
    products_page.search_product("Dress")

    assert products_page.is_search_results_header_visible()
    results = products_page.get_product_names()
    assert len(results) > 0, "Expected at least one product in search results"

    take_screenshot(driver, "search_results_dress")


@pytest.mark.search
@pytest.mark.parametrize("keyword", _read_search_keywords())
def test_search_multiple_keywords(driver, keyword):
    """Data-driven: same test, run once per keyword in testdata/search_data.csv."""
    products_page = ProductsPage(driver)
    products_page.load()
    products_page.search_product(keyword)

    assert products_page.is_search_results_header_visible()


@pytest.mark.search
def test_add_searched_product_to_cart(driver):
    products_page = ProductsPage(driver)
    products_page.load()
    products_page.search_product("Dress")

    assert products_page.is_search_results_header_visible()
    product_names = products_page.get_product_names()
    added_product = product_names[0]

    products_page.add_first_product_to_cart()
    products_page.click_view_cart_from_modal()

    cart_page = CartPage(driver)
    take_screenshot(driver, "cart_after_add")

    assert cart_page.is_product_in_cart(added_product), (
        f"Expected '{added_product}' to be in the cart"
    )
