import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope = "function")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = False, slow_mo = 300)
        yield browser
        browser.close()

def test_bing_search_for_playwright(browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.bing.com")

   # OPTIONAL: Dismiss cookie banner if it appears
    try:
        page.locator('button:has-text("Accept")').click(timeout = 3000)
    except Exception:
        pass
    # Try discovering input field just once, assume sb_form_q (adjust if your discovery run showed a different name)
    page.screenshot(path="debug_after_nav.png")
    page.wait_for_selector('input[name="sb_form_q"]', timeout = 100000)
    page.fill('input[name = "sb_form_q"]', "playwright python")
    page.keyboard.press("Enter")
    print(page.content()[:3000])
    page.screenshot(path="debug_after_search.png")

    # Wait for the results to be visible (adjust selector if you found a better one)
    page.wait_for_selector('li.b_algo h2 a', timeout = 5000)

    # Get all the result titles
    titles = page.locator('li.b_algo h2 a')
    count = titles.count()
    print(f"no of results : {count}")
    
    found = False
    for i in range(count):
        title = titles.nth(i).inner_text()
        print(f"Result {i+1}: {title}")
        if "playwright" in title.lower():
            found = True

 # Assert that "playwright" appears in at least one result
    assert found, "No search result contained 'playwright' in the title."
    context.close()

