import os
from dotenv import load_dotenv
import requests
import pytest
import allure

from helpers.bodies import PRIVATE_GIST
from helpers.delete_gist import delete_gist
from helpers.headers import get_headers_for_auth_user

load_dotenv()
GITHUB_API_URL = "https://api.github.com/gists"
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')


@allure.feature("/POST /gists")
class TestGistCreation:

    @allure.story("API Test: User can create gist")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_gist(self):
        with allure.step("/POST /gists and get response"):
            response = requests.post(GITHUB_API_URL, headers=get_headers_for_auth_user(GITHUB_TOKEN), json=PRIVATE_GIST)

        with allure.step("Verify response status code"):
            assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"

        response_json = response.json()
        gist_id = response_json.get('id')

        with allure.step("Verify if gist id exists"):
            assert gist_id, "Gist ID not found in response"

        allure.dynamic.title(f"Test /POST with Gist ID: {gist_id}")

        os.environ['GIST_ID'] = gist_id

        print(f"Gist {gist_id} created successfully.")


@allure.step("Delete gist")
@pytest.fixture(scope="function", autouse=True)
def teardown(request):
    yield
    # Delete the gist if the test passed
    if request.node.rep_call.passed:
        delete_gist(os.getenv('GIST_ID'), GITHUB_TOKEN)
