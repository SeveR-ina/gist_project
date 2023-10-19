import os
import pytest
import requests
from dotenv import load_dotenv
import logging

from helpers.create_gist import create_gist
from helpers.delete_gist import delete_gist
import allure

from logs.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

load_dotenv()
GITHUB_API_URL = "https://api.github.com/gists"
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')


@pytest.fixture(params=[
    {
        "description": "Test Gist 1",
        "files": {
            "file1.txt": {
                "content": "This is a test file"
            }
        }
    }
])
def test_data(request):
    return request.param


@allure.step("Create gist")
@pytest.fixture(scope="function")
def setup_gist(test_data):
    # Create a gist
    gist_id = create_gist(test_data, GITHUB_TOKEN)
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


@allure.feature("/GET Private Gists")
class TestPrivateGists:

    @allure.story("Test visibility of a private gist by the same user via GET /gists")
    @allure.severity(allure.severity_level.NORMAL)
    def test_private_gist_visibility(self, setup_gist, teardown_gist, test_data):
        gist_id = setup_gist

        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        logger.info(f"Test Data: {test_data}")

        with allure.step("/GET /gists and get response"):
            response = requests.get(GITHUB_API_URL, headers=headers)

        with allure.step("Verify response status code"):
            assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

        # Check if the gist is visible in the user's gists
        user_gists = response.json()
        gist_ids = [gist["id"] for gist in user_gists]

        with allure.step("Assert if gist id in response json for GET /gists"):
            assert gist_id in gist_ids, f"Gist ID {gist_id} not found in user's gists."

        print(f"Gist {gist_id} is found in user's gists. Test passed")
