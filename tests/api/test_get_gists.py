import os
import pytest
import requests
from dotenv import load_dotenv
import logging

from helpers_api.bodies import PRIVATE_GIST, PUBLIC_GIST
from helpers_api.create_gist import create_gist
from helpers_api.delete_gist import delete_gist
import allure

from helpers_api.headers import get_headers, get_headers_for_auth_user
from logs.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

load_dotenv()
GITHUB_API_URL = "https://api.github.com/gists"
GITHUB_TOKEN_2 = os.getenv('GITHUB_TOKEN_2')


@pytest.fixture(params=[
    (get_headers_for_auth_user(GITHUB_TOKEN_2), PRIVATE_GIST),
    (get_headers_for_auth_user(GITHUB_TOKEN_2), PUBLIC_GIST),
    (get_headers(), PUBLIC_GIST),
    (get_headers(), PRIVATE_GIST),
], ids=["AuthPrivate", "AuthPublic", "NoAuthPublic", "NoAuthPrivate"])
def test_data(request):
    return request.param


@allure.step("Create gist")
@pytest.fixture(scope="function")
def setup_gist(test_data):
    headers, body = test_data
    # Create a gist
    gist_id = create_gist(body, GITHUB_TOKEN_2)
    os.environ['GIST_ID'] = gist_id
    yield gist_id


@allure.step("Delete gist")
@pytest.fixture(scope="function")
def teardown_gist():
    gist_id = os.getenv('GIST_ID')
    yield
    # Delete the gist in teardown
    if gist_id:
        delete_gist(gist_id, GITHUB_TOKEN_2)


@allure.feature("/GET Gists")
class TestGistInLists:

    @allure.story("API Test: check visibility of gist via /GET /gists")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_api_gist_visibility_in_gists(self, setup_gist, teardown_gist, test_data):
        headers, body = test_data
        gist_id = setup_gist

        logger.info(f"Test Data: {body}")

        with allure.step("/GET /gists and get response"):
            response = requests.get(GITHUB_API_URL, headers=headers)

        with allure.step("Verify response status code"):
            assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

        user_gists = response.json()
        gist_ids = [gist["id"] for gist in user_gists]

        with allure.step("Assert gist visibility in response for GET /gists"):
            if body == PRIVATE_GIST:
                if headers == get_headers_for_auth_user(GITHUB_TOKEN_2):
                    assert gist_id in gist_ids, f"Private Gist ID {gist_id} not found in gists for authed user."
                    print(f"Private Gist {gist_id} is found in gists for auth user. Test passed")
                elif headers == get_headers():
                    assert gist_id not in gist_ids, (f"Private Gist ID {gist_id} is found in response for not authed "
                                                     f"user.")
                    print(f"Private Gist {gist_id} is not visible for unauthorized users in GET /gists. Test passed")
            elif body == PUBLIC_GIST:
                if headers == get_headers_for_auth_user(GITHUB_TOKEN_2):
                    assert gist_id in gist_ids, f"Public Gist ID {gist_id} not found in gists for authed user."
                    print(f"Public Gist {gist_id} is found in gists for auth user. Test passed")
                elif headers == get_headers():
                    assert gist_id in gist_ids, f"Public Gist ID {gist_id} not found in gists for not authed user."
                    print(f"Public Gist {gist_id} is found in user's gists. Test passed")
