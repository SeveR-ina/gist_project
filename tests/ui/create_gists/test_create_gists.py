import os

import pytest
from dotenv import load_dotenv
from playwright.sync_api import expect, sync_playwright

from helpers_ui.models.gist_create_page import GistCreatePage
from helpers_ui.models.login_page import LoginPage

BROWSER_TYPES = ["chromium", "webkit"]

load_dotenv()
USER_EREKA_EMAIl = os.getenv('USER_EREKA_EMAIl')
USER_PASS = os.getenv('USER_PASS')


@pytest.mark.parametrize("browser_type", BROWSER_TYPES)
def test_create_gist(browser_type):
    with sync_playwright() as p:
        browser = p[browser_type].launch(headless=False)

        page = browser.new_page()

        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(USER_EREKA_EMAIl, USER_PASS)

        gist_create_page = GistCreatePage(page)
        gist_create_page.navigate()

        expect(gist_create_page.discription_input).to_be_visible()

        browser.close()


