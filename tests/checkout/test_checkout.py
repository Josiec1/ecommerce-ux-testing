import pytest
from playwright.sync_api import expect

BASE = "https://www.saucedemo.com"

class TestCheckout:

    def go_to_checkout(self, page):
        """Helper: add item and navigate to checkout step 1"""
        page.locator("button[data-test='add-to-cart-sauce-labs-backpack']").click()
        page.locator(".shopping_cart_link").click()
        page.locator("button[data-test='checkout']").click()

    def test_checkout_button_visible_in_cart(self, page):
        """Positive: Checkout button is visible in cart"""
        page.locator("button[data-test='add-to-cart-sauce-labs-backpack']").click()
        page.locator(".shopping_cart_link").click()
        expect(page.locator("button[data-test='checkout']")).to_be_visible()

    def test_checkout_step1_loads(self, page):
        """Positive: Checkout step 1 form loads correctly"""
        self.go_to_checkout(page)
        expect(page).to_have_url(f"{BASE}/checkout-step-one.html")
        expect(page.locator("[data-test='firstName']")).to_be_visible()
        expect(page.locator("[data-test='lastName']")).to_be_visible()
        expect(page.locator("[data-test='postalCode']")).to_be_visible()

    def test_checkout_completes_with_valid_info(self, page):
        """Positive: Checkout completes successfully with valid info"""
        self.go_to_checkout(page)
        page.fill("[data-test='firstName']", "John")
        page.fill("[data-test='lastName']", "Doe")
        page.fill("[data-test='postalCode']", "10001")
        page.click("[data-test='continue']")
        expect(page).to_have_url(f"{BASE}/checkout-step-two.html")

    def test_checkout_step2_shows_order_summary(self, page):
        """Positive: Step 2 shows item summary and total price"""
        self.go_to_checkout(page)
        page.fill("[data-test='firstName']", "John")
        page.fill("[data-test='lastName']", "Doe")
        page.fill("[data-test='postalCode']", "10001")
        page.click("[data-test='continue']")
        expect(page.locator(".cart_item")).to_have_count(1)
        expect(page.locator(".summary_total_label")).to_be_visible()

    def test_checkout_finish_shows_confirmation(self, page):
        """Positive: Completing order shows confirmation screen"""
        self.go_to_checkout(page)
        page.fill("[data-test='firstName']", "John")
        page.fill("[data-test='lastName']", "Doe")
        page.fill("[data-test='postalCode']", "10001")
        page.click("[data-test='continue']")
        page.click("[data-test='finish']")
        expect(page).to_have_url(f"{BASE}/checkout-complete.html")
        expect(page.locator("[data-test='complete-header']")).to_have_text("Thank you for your order!")

    def test_checkout_error_on_empty_firstname(self, page):
        """Negative: Error shown when first name is empty"""
        self.go_to_checkout(page)
        page.fill("[data-test='lastName']", "Doe")
        page.fill("[data-test='postalCode']", "10001")
        page.click("[data-test='continue']")
        expect(page.locator("[data-test='error']")).to_be_visible()

    def test_checkout_error_on_empty_lastname(self, page):
        """Negative: Error shown when last name is empty"""
        self.go_to_checkout(page)
        page.fill("[data-test='firstName']", "John")
        page.fill("[data-test='postalCode']", "10001")
        page.click("[data-test='continue']")
        expect(page.locator("[data-test='error']")).to_be_visible()

    def test_checkout_error_on_empty_postal(self, page):
        """Negative: Error shown when postal code is empty"""
        self.go_to_checkout(page)
        page.fill("[data-test='firstName']", "John")
        page.fill("[data-test='lastName']", "Doe")
        page.click("[data-test='continue']")
        expect(page.locator("[data-test='error']")).to_be_visible()

    def test_cancel_checkout_returns_to_cart(self, page):
        """Positive: Cancel button returns user to cart"""
        self.go_to_checkout(page)
        page.click("[data-test='cancel']")
        expect(page).to_have_url(f"{BASE}/cart.html")

    def test_mobile_checkout_completes(self, mobile_page):
        """Mobile viewport: Full checkout flow works on mobile"""
        mobile_page.locator("button[data-test='add-to-cart-sauce-labs-backpack']").click()
        mobile_page.locator(".shopping_cart_link").click()
        mobile_page.locator("button[data-test='checkout']").click()
        mobile_page.fill("[data-test='firstName']", "Jane")
        mobile_page.fill("[data-test='lastName']", "Smith")
        mobile_page.fill("[data-test='postalCode']", "90210")
        mobile_page.click("[data-test='continue']")
        mobile_page.click("[data-test='finish']")
        expect(mobile_page.locator("[data-test='complete-header']")).to_have_text("Thank you for your order!")
