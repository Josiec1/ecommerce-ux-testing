import pytest
from playwright.sync_api import expect

BASE = "https://www.saucedemo.com"

class TestLogin:

    def test_valid_login_succeeds(self, browser):
        """Positive: Valid credentials navigate to inventory page"""
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        page.goto(BASE)
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")
        expect(page).to_have_url(f"{BASE}/inventory.html")
        context.close()

    def test_invalid_password_shows_error(self, browser):
        """Negative: Wrong password shows error message"""
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        page.goto(BASE)
        page.fill("#user-name", "standard_user")
        page.fill("#password", "wrong_password")
        page.click("#login-button")
        expect(page.locator("[data-test='error']")).to_be_visible()
        context.close()

    def test_locked_out_user_shows_error(self, browser):
        """Negative: Locked out user cannot login"""
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        page.goto(BASE)
        page.fill("#user-name", "locked_out_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")
        expect(page.locator("[data-test='error']")).to_be_visible()
        context.close()

    def test_empty_username_shows_error(self, browser):
        """Negative: Empty username shows error"""
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        page.goto(BASE)
        page.fill("#password", "secret_sauce")
        page.click("#login-button")
        expect(page.locator("[data-test='error']")).to_be_visible()
        context.close()

    def test_empty_password_shows_error(self, browser):
        """Negative: Empty password shows error"""
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        page.goto(BASE)
        page.fill("#user-name", "standard_user")
        page.click("#login-button")
        expect(page.locator("[data-test='error']")).to_be_visible()
        context.close()

    def test_empty_both_fields_shows_error(self, browser):
        """Negative: Both fields empty shows error"""
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        page.goto(BASE)
        page.click("#login-button")
        expect(page.locator("[data-test='error']")).to_be_visible()
        context.close()

    def test_logout_returns_to_login(self, page):
        """Positive: Logout returns user to login page"""
        page.click("#react-burger-menu-btn")
        page.wait_for_selector("#logout_sidebar_link")
        page.click("#logout_sidebar_link")
        expect(page).to_have_url(BASE + "/")
        expect(page.locator("#login-button")).to_be_visible()

    def test_cannot_access_inventory_without_login(self, browser):
        """Negative: Direct access to inventory without login redirects"""
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        page.goto(f"{BASE}/inventory.html")
        expect(page).to_have_url(BASE + "/")
        context.close()

    def test_login_page_has_username_and_password_fields(self, browser):
        """Positive: Login page renders all required form fields"""
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        page.goto(BASE)
        expect(page.locator("#user-name")).to_be_visible()
        expect(page.locator("#password")).to_be_visible()
        expect(page.locator("#login-button")).to_be_visible()
        context.close()

    def test_mobile_login_succeeds(self, browser):
        """Mobile viewport: Login works on mobile screen"""
        context = browser.new_context(
            viewport={"width": 390, "height": 844},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)"
        )
        page = context.new_page()
        page.goto(BASE)
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")
        expect(page).to_have_url(f"{BASE}/inventory.html")
        context.close()
