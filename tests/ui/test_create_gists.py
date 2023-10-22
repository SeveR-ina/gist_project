import logging
import os
import time

import allure
import pytest
from dotenv import load_dotenv
from playwright.sync_api import expect, sync_playwright

from helpers.delete_gist import delete_gist
from helpers_ui.models.gist_create_page import GistCreatePage
from helpers_ui.models.login_page import LoginPage
from logs.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

BROWSER_TYPES = ["chromium", "webkit"]

load_dotenv()
USER_EREKA_EMAIl = os.getenv('USER_EREKA_EMAIl')
USER_PASS = os.getenv('USER_PASS')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')


@allure.feature("/POST /gists")
class TestGistCreationUI:

    @allure.story("UI Test: User can create gist")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("browser_type", BROWSER_TYPES)
    def test_create_gist(self, browser_type):
        with sync_playwright() as p:
            browser = p[browser_type].launch(headless=True)
            page = browser.new_page()
            login_page = LoginPage(page)

            login_page.navigate_to_login_page(GITHUB_TOKEN)
            with allure.step("Login"):
                login_page.login(USER_EREKA_EMAIl, USER_PASS)

            gist_create_page = GistCreatePage(page)
            gist_create_page.navigate()

            expect(gist_create_page.description_input).to_be_visible()

            time_stamp = str(time.time())
            logger.info(f"Filled test data: {time_stamp}")

            with allure.step("Fill the create gist form"):
                expect(gist_create_page.code_input).to_be_editable()
                gist_create_page.fill_form(time_stamp)
                page.keyboard.type(time_stamp)

            gist_create_page.submit_form(False)

            with allure.step("Check that gist is created"):
                page.get_by_text(time_stamp).first.is_visible()

            gist_id = page.url.split("/")[-1]
            os.environ['GIST_ID'] = gist_id

            print(f"Gist {gist_id} created successfully via tests_ui.")

            browser.close()


@allure.step("Delete gist")
@pytest.fixture(scope="function", autouse=True)
def teardown(request):
    yield
    gist_id = os.getenv('GIST_ID')
    if (
            request.node.parent.name == "TestGistCreationUI"
            and request.node.rep_call.passed
    ):
        delete_gist(gist_id, GITHUB_TOKEN)
