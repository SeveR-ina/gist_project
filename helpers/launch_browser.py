from playwright.sync_api import sync_playwright


def launch_browser(browser_type):
    with sync_playwright() as p:
        browser = p[browser_type].launch(headless=False)
        return browser
