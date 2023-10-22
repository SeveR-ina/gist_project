import os
import pytest
from dotenv import load_dotenv
import logging

from playwright.sync_api import sync_playwright, expect

from helpers_api.bodies import PUBLIC_GIST
from helpers_api.create_gist import create_gist
from helpers_api.delete_gist import delete_gist
import allure

from helpers_ui.models.login_page import LoginPage
from logs.logging_config import configure_logging
from ui.models.discover_gists_page import DiscoverGistsPage
from ui.models.gist_username_page import GistUserNamePage

configure_logging()
logger = logging.getLogger(__name__)

BROWSER_TYPES = ["chromium", "webkit"]

load_dotenv()
USER_PASS = os.getenv('USER_PASS')

# USER_EREKA_EMAIl = os.getenv('USER_EREKA_EMAIl')
# USERNAME_EREKA = os.getenv('USERNAME_EREKA')
# GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

USER_MAX_EMAIl = os.getenv('USER_MAX_EMAIl')
USERNAME_MAX = os.getenv('USERNAME_MAX')
TOKEN_2 = os.getenv('TOKEN_2')


@allure.step("Create gist")
@pytest.fixture(scope="session")
def setup_gist():
    body = PUBLIC_GIST
    # Create a gist
    gist_id = create_gist(body, TOKEN_2)
    os.environ['GIST_ID'] = gist_id
    yield gist_id


@allure.step("Delete gist")
@pytest.fixture(scope="session")
def teardown_gist():
    gist_id = os.getenv('GIST_ID')
    yield
    # Delete the gist in teardown
    if gist_id:
        delete_gist(gist_id, TOKEN_2)


@allure.feature("/GET Public Gists")
class TestPublicGists:

    @allure.story("UI Test: check visibility of a public gist on https://gist.github.com/discover for NOT authed user")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("browser_type", BROWSER_TYPES)
    def test_public_gist_visibility_on_discover(self, browser_type, setup_gist, teardown_gist):
        with sync_playwright() as p:
            gist_id = setup_gist

            browser = p[browser_type].launch(headless=True)
            page = browser.new_page()

            discover_gists_page = DiscoverGistsPage(page)
            discover_gists_page.navigate()

            with allure.step("Check that public gist is visible for stranger"):
                expect(page.get_by_role("link", name=f"gist:{gist_id}")).to_be_visible()
            browser.close()

    @pytest.mark.skip
    @allure.story("UI Test: check visibility of a public gist on https://gist.github.com/username for authed user")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("browser_type", BROWSER_TYPES)
    def test_get_public_gist_on_username_page_by_authed_user(self, browser_type, setup_gist, teardown_gist):
        with sync_playwright() as p:
            gist_id = setup_gist

            browser = p[browser_type].launch(headless=True)
            page = browser.new_page()
            login_page = LoginPage(page)

            login_page.navigate_to_login_page(TOKEN_2)
            with allure.step("Login"):
                login_page.login(USER_MAX_EMAIl, USER_PASS)

            gist_username_page = GistUserNamePage(page, gist_id, USERNAME_MAX)
            gist_username_page.navigate(USERNAME_MAX)

            with allure.step("Check that public gist is visible for creator"):
                expect(page.get_by_role("link", name=f"gist:{gist_id}")).to_be_visible()
            browser.close()

    @pytest.mark.skip(reason="Doesn't work while running in class. TODO: fix that")
    @allure.story("UI Test: check visibility of a public gist on https://gist.github.com/username for NOT authed user")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("browser_type", BROWSER_TYPES)
    def test_get_public_gist_on_username_page(self, browser_type, setup_gist, teardown_gist):
        with sync_playwright() as p:
            gist_id = setup_gist

            browser = p[browser_type].launch(headless=True)
            page = browser.new_page()

            gist_username_page = GistUserNamePage(page, gist_id, USERNAME_MAX)
            gist_username_page.navigate(USERNAME_MAX)

            with allure.step("Check that public gist is visible for stranger"):
                expect(page.get_by_role("link", name=f"gist:{gist_id}")).to_be_visible()
            browser.close()
