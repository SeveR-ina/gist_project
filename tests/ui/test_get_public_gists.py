import os
import pytest
from dotenv import load_dotenv
import logging

from playwright.sync_api import sync_playwright, expect

from helpers_api.bodies import PUBLIC_GIST
from helpers_api.create_gist import create_gist
from helpers_api.delete_gist import delete_gist
import allure

from helpers.models.login_page import LoginPage
from logs.logging_config import configure_logging
from tests.ui.models.dicover_gists_page import DiscoverGistsPage
from tests.ui.models.gist_username_page import GistUserNamePage

configure_logging()
logger = logging.getLogger(__name__)

load_dotenv()

USER_EREKA_EMAIl = os.getenv('USER_EREKA_EMAIl')
USER_PASS = os.getenv('USER_PASS')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
USERNAME_EREKA = os.getenv('USERNAME_EREKA')
BROWSER_TYPES = ["chromium", "webkit"]


@allure.step("Create gist")
@pytest.fixture(scope="session")
def setup_gist():
    body = PUBLIC_GIST
    # Create a gist
    gist_id = create_gist(body, GITHUB_TOKEN)
    os.environ['GIST_ID'] = gist_id
    yield gist_id


@allure.step("Delete gist")
@pytest.fixture(scope="session")
def teardown_gist():
    gist_id = os.getenv('GIST_ID')
    yield
    # Delete the gist in teardown
    if gist_id:
        delete_gist(gist_id, GITHUB_TOKEN)


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

    @allure.story("UI Test: check visibility of a public gist on https://gist.github.com/username for authed user")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("browser_type", BROWSER_TYPES)
    def test_get_public_gist_on_username_page_by_authed_user(self, browser_type, setup_gist, teardown_gist):
        with sync_playwright() as p:
            gist_id = setup_gist

            browser = p[browser_type].launch(headless=True)
            page = browser.new_page()
            login_page = LoginPage(page)

            login_page.navigate_to_login_page(GITHUB_TOKEN)
            with allure.step("Login"):
                login_page.login(USER_EREKA_EMAIl, USER_PASS)

            gist_username_page = GistUserNamePage(page, gist_id, USERNAME_EREKA)
            gist_username_page.navigate(USERNAME_EREKA)

            with allure.step("Check that public gist is visible for creator"):
                expect(page.get_by_role("link", name=f"gist:{gist_id}")).to_be_visible()
            browser.close()

    @allure.story("UI Test: check visibility of a public gist on https://gist.github.com/username for NOT authed user")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("browser_type", BROWSER_TYPES)
    def test_get_public_gist_on_username_page(self, browser_type, setup_gist, teardown_gist):
        with sync_playwright() as p:
            gist_id = setup_gist

            browser = p[browser_type].launch(headless=True)
            page = browser.new_page()

            gist_username_page = GistUserNamePage(page, gist_id, USERNAME_EREKA)
            gist_username_page.navigate(USERNAME_EREKA)

            with allure.step("Check that public gist is visible for stranger"):
                expect(page.get_by_role("link", name=f"gist:{gist_id}")).to_be_visible()
            browser.close()
