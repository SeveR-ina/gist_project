import os
from dotenv import load_dotenv
import requests
import allure

from helpers_api.bodies import PRIVATE_GIST
from helpers_api.delete_gist import delete_gist
from helpers_api.headers import get_headers_for_auth_user, get_bad_headers

load_dotenv()
GITHUB_API_URL = "https://api.github.com/gists"
GITHUB_TOKEN_2 = os.getenv('GITHUB_TOKEN_2')


@allure.feature("/POST /gists")
class TestGistCreationStatuses:

    @allure.story("API Test: Check 201 status for /POST /gists")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_201_status_for_post_gist(self):
        with allure.step("/POST /gists and get response"):
            response = requests.post(GITHUB_API_URL,
                                     headers=get_headers_for_auth_user(GITHUB_TOKEN_2), json=PRIVATE_GIST)

        with allure.step("Verify response status code"):
            assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"

        gist_id = response.json().get('id')
        delete_gist(gist_id, GITHUB_TOKEN_2)

    @allure.story("API Test: Check 400 status for /POST /gists")
    @allure.severity(allure.severity_level.NORMAL)
    def test_400_status_for_post_gist(self):
        with allure.step("/POST /gists and get response"):
            response = requests.post(GITHUB_API_URL, headers=get_bad_headers(), json=PRIVATE_GIST)

        with allure.step("Verify response status code"):
            assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"

    @allure.story("API Test: Check 401 status for /POST /gists")
    @allure.severity(allure.severity_level.NORMAL)
    def test_401_status_for_post_gist(self):
        with allure.step("/POST /gists and get response"):
            response = requests.post(GITHUB_API_URL, headers=get_headers_for_auth_user(111), json=PRIVATE_GIST)

        with allure.step("Verify response status code"):
            assert response.status_code == 401, f"Expected status code 401, but got {response.status_code}"

    @allure.story("API Test: Check 422 status for /POST /gists")
    @allure.severity(allure.severity_level.NORMAL)
    def test_422_status_for_post_gist(self):
        with allure.step("/POST /gists and get response"):
            response = requests.post(GITHUB_API_URL, headers=get_headers_for_auth_user(GITHUB_TOKEN_2), json="")

        with allure.step("Verify response status code"):
            assert response.status_code == 422, f"Expected status code 422, but got {response.status_code}"
