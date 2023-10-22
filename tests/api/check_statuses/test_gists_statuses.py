import pytest
import requests

import allure

from helpers.headers import get_headers, get_bad_headers, get_headers_for_auth_user

GITHUB_API_URL = "https://api.github.com/gists"


@allure.feature("/GET Gists")
class TestGetGistStatuses:

    @allure.story("API Test: check 200 status for GET /gists")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_api_check_200_status(self):
        with allure.step("/GET /gists and get response"):
            response = requests.get(GITHUB_API_URL, headers=get_headers())

        with allure.step("Verify response status code"):
            assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    @allure.story("API Test: check 401 status for GET /gists")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_api_check_401_status(self):
        with allure.step("/GET /gists and get response"):
            response = requests.get(GITHUB_API_URL, headers=get_headers_for_auth_user("invalid"))

        with allure.step("Verify response status code"):
            assert response.status_code == 401, f"Expected status code 401, but got {response.status_code}"

    @pytest.mark.skip(reason="Doesn't work while running in class. TODO: fix that")
    @allure.story("API Test: check 400 status for GET /gists")
    @allure.severity(allure.severity_level.NORMAL)
    def test_api_check_400_status(self):
        with allure.step("/GET /gists and get response"):
            response = requests.get(GITHUB_API_URL, headers=get_bad_headers())

        with allure.step("Verify response status code"):
            assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
