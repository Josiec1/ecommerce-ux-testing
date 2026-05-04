import pytest
from playwright.sync_api import expect

BASE = "https://www.saucedemo.com"

class TestProductListing:

    def test_product_page_loads(self, page):
        """Positive: Inventory page loads after login"""
        expect(page).to_have_url(f"{BASE}/inventory.html")
        expect(page.locator(".inventory_list")).to_be_visible()

    def test_six_products_displayed(self, page):
        """Positive: All 6 products are displayed"""
        items = page.locator(".inventory_item")
        expect(items).to_have_count(6)

    def test_each_product_has_name(self, page):
        """Positive: Every product has a visible name"""
        names = page.locator(".inventory_item_name")
        expect(names.first).to_be_visible()
        assert names.count() == 6

    def test_each_product_has_price(self, page):
        """Positive: Every product has a visible price"""
        prices = page.locator(".inventory_item_price")
        expect(prices.first).to_be_visible()
        assert prices.count() == 6

    def test_each_product_has_add_to_cart(self, page):
        """Positive: Every product has Add to cart button"""
        buttons = page.locator("button[data-test*='add-to-cart']")
        assert buttons.count() == 6

    def test_navigate_to_product_detail(self, page):
        """Positive: Clicking product name navigates to detail page"""
        page.locator(".inventory_item_name").first.click()
        page.wait_for_load_state("networkidle")
        assert "inventory-item" in page.url

    def test_sort_by_price_low_to_high(self, page):
        """Positive: Sorting by price low-to-high reorders products"""
        page.select_option(".product_sort_container", "lohi")
        prices = page.locator(".inventory_item_price").all()
        values = [float(p.inner_text().replace("$","")) for p in prices]
        assert values == sorted(values)

    def test_sort_by_name_z_to_a(self, page):
        """Positive: Sorting Z-A reorders products alphabetically"""
        page.select_option(".product_sort_container", "za")
        names = page.locator(".inventory_item_name").all()
        values = [n.inner_text() for n in names]
        assert values == sorted(values, reverse=True)

    def test_empty_cart_on_load(self, page):
        """Boundary: Cart is empty when first loading the page"""
        badge = page.locator(".shopping_cart_badge")
        expect(badge).not_to_be_visible()

    def test_mobile_product_list_visible(self, mobile_page):
        """Mobile viewport: Product list renders on mobile screen"""
        expect(mobile_page.locator(".inventory_list")).to_be_visible()
        items = mobile_page.locator(".inventory_item")
        expect(items.first).to_be_visible()
