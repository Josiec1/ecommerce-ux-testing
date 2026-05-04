cat > README.md << 'README'
# E-commerce UX Automated Testing Framework

A data-driven end-to-end UX testing framework built with **Python + Playwright + Pytest**, targeting a merchant-facing e-commerce platform. Covers 30 test cases across 3 core merchant user flows.

## Test Coverage

| Module | Tests | Techniques |
|---|---|---|
| Product Listing | 10 | Positive, Boundary, Mobile viewport |
| Order Management | 10 | Positive, Negative, Boundary |
| Checkout | 10 | Positive, Negative, Mobile viewport |

**Total: 30 tests across desktop and mobile viewports**

## Tech Stack

- **Python 3.14** - test logic
- **Playwright** - browser automation (Chromium)
- **Pytest** - test runner and fixture management
- **GitHub Actions** - CI/CD pipeline (auto-run on push)

## Testing Methodology

- **Black-box testing**: positive, negative, and boundary value tests
- **Mobile viewport testing**: key flows validated on 390x844 (iPhone)
- **Data-driven scenario coverage**: test cases derived from systematic merchant user journey analysis

## Project Structure

- `conftest.py` - shared fixtures (login, browser, mobile viewports)
- `pytest.ini` - pytest configuration
- `tests/product_listing/test_product_listing.py` - catalog browsing, sorting, navigation
- `tests/order_management/test_order_management.py` - cart add/remove, persistence
- `tests/checkout/test_checkout.py` - checkout flow, form validation
- `.github/workflows/playwright.yml` - CI/CD pipeline

## Running Tests

```bash
pip install playwright pytest pytest-playwright
playwright install chromium
pytest -v
```

## Sample Results
```
30 passed in 33.63s
```
