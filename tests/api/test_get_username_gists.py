import os
import pytest
import requests
from dotenv import load_dotenv
import logging

from helpers.bodies import PRIVATE_GIST, PUBLIC_GIST
from helpers.create_gist import create_gist
from helpers.delete_gist import delete_gist
import allure

from helpers.headers import get_headers, get_headers_for_auth_user
from logs.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

load_dotenv()
GITHUB_API_URL = "https://api.github.com/users/"
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
USERNAME_EREKA = os.getenv('USERNAME_EREKA')


@pytest.fixture(params=[
    (get_headers_for_auth_user(GITHUB_TOKEN), PRIVATE_GIST),
    (get_headers_for_auth_user(GITHUB_TOKEN), PUBLIC_GIST),
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
    gist_id = create_gist(body, GITHUB_TOKEN)
    os.environ['GIST_ID'] = gist_id
    yield gist_id


@allure.step("Delete gist")
@pytest.fixture(scope="function")
def teardown_gist():
    gist_id = os.getenv('GIST_ID')
    yield
    # Delete the gist in teardown
    if gist_id:
        delete_gist(gist_id, GITHUB_TOKEN)


@allure.feature("/GET Gists via /users/{username}/gists")
class TestGistInUsernameGists:

    @allure.story("API Test: check visibility of gist via GET /users/{username}/gists")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_api_gist_visibility_in_username_gists(self, setup_gist, teardown_gist, test_data):
        headers, body = test_data
        gist_id = setup_gist

        logger.info(f"Test Data: {body}")

        with allure.step("GET /users/{username}/gists and get response"):
            response = requests.get(GITHUB_API_URL + USERNAME_EREKA + "/gists", headers=headers)

        with allure.step("Verify response status code"):
            assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

        user_gists = response.json()
        gist_ids = [gist["id"] for gist in user_gists]

        with allure.step("Assert gist visibility in response for GET /users/{username}/gists"):
            if body == PRIVATE_GIST:
                if headers == get_headers_for_auth_user(GITHUB_TOKEN):
                    assert gist_id in gist_ids, f"Private Gist ID {gist_id} not found in response for authed user."
                    print(f"Private Gist {gist_id} is found in response for auth user. Test passed")
                elif headers == get_headers():
                    assert gist_id not in gist_ids, (f"Private Gist ID {gist_id} is found in response for not authed "
                                                     f"user.")
                    print(f"Private Gist {gist_id} is not visible for unauthorized users in response. Test passed")
            elif body == PUBLIC_GIST:
                if headers == get_headers_for_auth_user(GITHUB_TOKEN):
                    assert gist_id in gist_ids, f"Public Gist ID {gist_id} not found in response for authed user."
                    print(f"Public Gist {gist_id} is found in response for auth user. Test passed")
                elif headers == get_headers():
                    assert gist_id in gist_ids, f"Public Gist ID {gist_id} not found in response for not authed user."
                    print(f"Public Gist {gist_id} is found in response. Test passed")
