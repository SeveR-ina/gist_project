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
GITHUB_API_URL = "https://api.github.com/gists/"
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')


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


@allure.feature("/GET /gists/{gist_id}")
class TestGist:

    @allure.story("API Test: check visibility of gist via /GET /gists/{gist_id}")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_api_gist_visibility(self, setup_gist, teardown_gist, test_data):
        headers, body = test_data
        gist_id = setup_gist

        logger.info(f"Test Data: {body}")

        with allure.step("/GET /gists/{gist_id} and get response"):
            response = requests.get(GITHUB_API_URL + gist_id, headers=headers)

        with allure.step("Verify response status code"):
            assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

        with allure.step("Assert Gist ID in the response"):
            response_data = response.json()
            assert response_data["id"] == gist_id, f"Gist ID in the response does not match the expected Gist ID."
