import pytest
from playwright.sync_api import expect

BASE = "https://www.saucedemo.com"

class TestOrderManagement:

    def test_add_single_item_to_cart(self, page):
        """Positive: Adding one item updates cart badge to 1"""
        page.locator("button[data-test='add-to-cart-sauce-labs-backpack']").click()
        expect(page.locator(".shopping_cart_badge")).to_have_text("1")

    def test_add_multiple_items_to_cart(self, page):
        """Positive: Adding 3 items updates cart badge to 3"""
        buttons = page.locator("button[data-test*='add-to-cart']").all()
        for btn in buttons[:3]:
            btn.click()
        expect(page.locator(".shopping_cart_badge")).to_have_text("3")

    def test_remove_item_from_inventory(self, page):
        """Positive: Removing item from inventory page updates cart"""
        page.locator("button[data-test='add-to-cart-sauce-labs-backpack']").click()
        page.locator("button[data-test='remove-sauce-labs-backpack']").click()
        expect(page.locator(".shopping_cart_badge")).not_to_be_visible()

    def test_cart_page_shows_added_items(self, page):
        """Positive: Cart page displays all added items"""
        page.locator("button[data-test='add-to-cart-sauce-labs-backpack']").click()
        page.locator(".shopping_cart_link").click()
        expect(page).to_have_url(f"{BASE}/cart.html")
        expect(page.locator(".cart_item")).to_have_count(1)

    def test_cart_item_has_correct_name(self, page):
        """Positive: Cart item name matches what was added"""
        page.locator("button[data-test='add-to-cart-sauce-labs-backpack']").click()
        page.locator(".shopping_cart_link").click()
        expect(page.locator(".inventory_item_name")).to_have_text("Sauce Labs Backpack")

    def test_remove_item_from_cart(self, page):
        """Positive: Removing item from cart page empties cart"""
        page.locator("button[data-test='add-to-cart-sauce-labs-backpack']").click()
        page.locator(".shopping_cart_link").click()
        page.locator("button[data-test='remove-sauce-labs-backpack']").click()
        expect(page.locator(".cart_item")).to_have_count(0)

    def test_continue_shopping_returns_to_inventory(self, page):
        """Positive: Continue Shopping button returns to product list"""
        page.locator(".shopping_cart_link").click()
        page.locator("button[data-test='continue-shopping']").click()
        expect(page).to_have_url(f"{BASE}/inventory.html")

    def test_add_all_six_items(self, page):
        """Boundary: Adding all 6 items shows badge count of 6"""
        for i in range(6):
            page.locator("button[data-test*='add-to-cart']").first.click()
        expect(page.locator(".shopping_cart_badge")).to_have_text("6")

    def test_cart_persists_after_navigation(self, page):
        """Positive: Cart count persists after navigating to detail and back"""
        page.locator("button[data-test='add-to-cart-sauce-labs-backpack']").click()
        page.locator(".inventory_item_name").first.click()
        page.go_back()
        expect(page.locator(".shopping_cart_badge")).to_have_text("1")

    def test_mobile_add_to_cart(self, mobile_page):
        """Mobile viewport: Add to cart works on mobile screen"""
        mobile_page.locator("button[data-test='add-to-cart-sauce-labs-backpack']").click()
        expect(mobile_page.locator(".shopping_cart_badge")).to_have_text("1")
