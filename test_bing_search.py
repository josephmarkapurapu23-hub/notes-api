import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)  # See browser actions
        yield browser
        browser.close()

def test_bing_search(browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.bing.com")

    # Screenshot and print HTML before waiting for input box
    page.screenshot(path="bing_debug.png")
    html = page.content()
    print("\n\n---- PAGE HTML ----\n", html[:2000], "\n---- END HTML ----\n")

    # Try different selectors for inputs
    input_found = False
    try:
        page.wait_for_selector('input[name="q"]', timeout=5000)
        print("Found input[name='q']")
        input_found = True
    except Exception as e:
        print("input[name='q'] not found:", e)
        try:
            page.wait_for_selector('input[name="sb_form_q"]', timeout=5000)
            print("Found input[name='sb_form_q']")
            input_found = True
        except Exception as e2:
            print("input[name='sb_form_q'] not found:", e2)
            # Try any <input>
            try:
                page.wait_for_selector('input', timeout=5000)
                print("Found an <input> tag")
                input_found = True
            except Exception as e3:
                print("No input tag found:", e3)
    
    # List all input names on the page
    inputs = page.locator('input')
    print(f"\nNumber of input elements: {inputs.count()}")
    for i in range(inputs.count()):
        print(f"Input {i}: name = {inputs.nth(i).get_attribute('name')}")
    
    context.close()