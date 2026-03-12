from playwright.sync_api._generated import Browser
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        yield browser
        browser.close()

def test_bing_search_input_discovery(browser: Browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.bing.com")
    page.screenshot(path="bing_input_debug.png")
    print(page.content()[:2000])
    # Try to dismiss cookie banner
    try:
        page.locator('button:has-text("Accept")').click(timeout=3000)
    except Exception:
        pass
    # inputs = page.locator('input')
    # print(f"Found {inputs.count()} input elements.")
    # for i in range(inputs.count()):
    #     nm = inputs.nth(i).get_attribute('name')
    #     print(f"Input {i}: name = {nm} type = {inputs.nth(i).get_attribute('type')}")
    # context.close()
    inputs = page.locator('input')
    print(f"Found {inputs.count()} input elements.")
    for i in range(inputs.count()):
        nm = inputs.nth(i).get_attribute('name')
        type = inputs.nth(i).get_attribute('type')
        print(f"Input {i}: name = {nm} type = {type}")
    context.close()
    
    