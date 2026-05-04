import pytest
from playwright.sync_api import expect

BASE = "https://www.saucedemo.com"

class TestUXRegression:

    def test_product_images_all_visible(self, page):
        """Regression: All product images render correctly"""
        images = page.locator(".inventory_item img").all()
        assert len(images) == 6
        for img in images:
            expect(img).to_be_visible()

    def test_product_descriptions_not_empty(self, page):
        """Regression: All product descriptions have content"""
        descriptions = page.locator(".inventory_item_desc").all()
        for desc in descriptions:
            assert desc.inner_text().strip() != ""

    def test_price_format_has_dollar_sign(self, page):
        """Regression: All prices display with $ symbol"""
        prices = page.locator(".inventory_item_price").all()
        for price in prices:
            assert "$" in price.inner_text()

    def test_sort_then_add_to_cart_correct_count(self, page):
        """Regression: Sorting does not affect add-to-cart functionality"""
        page.select_option(".product_sort_container", "lohi")
        page.locator("button[data-test*='add-to-cart']").first.click()
        expect(page.locator(".shopping_cart_badge")).to_have_text("1")

    def test_footer_is_visible(self, page):
        """Regression: Footer renders on inventory page"""
        expect(page.locator("footer")).to_be_visible()

    def test_cart_count_consistent_across_pages(self, page):
        """Regression: Cart badge count stays consistent after navigation"""
        page.locator("button[data-test='add-to-cart-sauce-labs-backpack']").click()
        page.locator(".inventory_item_name").first.click()
        expect(page.locator(".shopping_cart_badge")).to_have_text("1")
        page.go_back()
        expect(page.locator(".shopping_cart_badge")).to_have_text("1")

    def test_add_to_cart_button_changes_to_remove(self, page):
        """Regression: Add to cart button changes to Remove after click"""
        page.locator("button[data-test='add-to-cart-sauce-labs-backpack']").click()
        expect(page.locator("button[data-test='remove-sauce-labs-backpack']")).to_be_visible()

    def test_product_detail_back_button_works(self, page):
        """Regression: Back button on product detail returns to inventory"""
        page.locator(".inventory_item_name").first.click()
        page.locator("[data-test='back-to-products']").click()
        expect(page).to_have_url(f"{BASE}/inventory.html")

    def test_mobile_footer_visible(self, mobile_page):
        """Mobile Regression: Footer visible on mobile viewport"""
        expect(mobile_page.locator("footer")).to_be_visible()

    def test_mobile_sort_dropdown_visible(self, mobile_page):
        """Mobile Regression: Sort dropdown accessible on mobile"""
        expect(mobile_page.locator(".product_sort_container")).to_be_visible()
