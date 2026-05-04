import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.saucedemo.com"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context(viewport={"width": 1280, "height": 720})
    page = context.new_page()
    page.goto(BASE_URL)
    page.fill("#user-name", USERNAME)
    page.fill("#password", PASSWORD)
    page.click("#login-button")
    page.wait_for_load_state("networkidle")
    yield page
    context.close()

@pytest.fixture
def mobile_page(browser):
    context = browser.new_context(
        viewport={"width": 390, "height": 844},
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)"
    )
    page = context.new_page()
    page.goto(BASE_URL)
    page.fill("#user-name", USERNAME)
    page.fill("#password", PASSWORD)
    page.click("#login-button")
    page.wait_for_load_state("networkidle")
    yield page
    context.close()
