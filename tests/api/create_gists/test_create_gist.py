import os
from dotenv import load_dotenv
import requests
import pytest
import allure
import logging

from helpers.delete_gist import delete_gist
from logs.logging_config import configure_logging


configure_logging()
logger = logging.getLogger(__name__)

load_dotenv()
GITHUB_API_URL = "https://api.github.com/gists"
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')


@pytest.fixture(params=[
    {
        "description": "Test Gist 1",
        "public": False,
        "files": {
            "file1.txt": {
                "content": "This is a test file"
            }
        }
    }
])
def test_data(request):
    return request.param


@allure.story("User can create gist")
@allure.title("Test /POST")
def test_create_gist(test_data):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    logger.info(f"Test Data: {test_data}")

    response = requests.post(GITHUB_API_URL, headers=headers, json=test_data)

    # logger.info(f"Response Content: {response.content}")

    with allure.step("Verify response status code"):
        assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"

    response_json = response.json()
    gist_id = response_json.get('id')

    assert gist_id, "Gist ID not found in response"

    # Log the Gist ID
    allure.dynamic.title(f"Test /POST with Gist ID: {gist_id}")

    os.environ['GIST_ID'] = gist_id


# Teardown fixture
@pytest.fixture(scope="function", autouse=True)
def teardown(request):
    yield
    # Delete the gist if the test passed
    if request.node.rep_call.passed:
        delete_gist(os.getenv('GIST_ID'), GITHUB_TOKEN)


if __name__ == "__main__":
    pytest.main()
