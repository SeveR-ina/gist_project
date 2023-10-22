# Gist Project

## Purpose

This project is designed to test the functionality of getting and creating GitHub Gists through both the API and the UI.

## Tech Stack

- Python 3.12
- Playwright for UI testing
- pytest for API test automation
- Allure for test reporting
- Docker for containerization

## How to Run Tests

### Via Python

1. Ensure you have Python 3.12 and project dependencies installed.
2. Set up your `.env` file with the required credentials.
3. To run all tests:
   ```
   pytest tests
   ```
   or with logs:
   ```
   python -m pytest -s --log-cli-level=INFO 
   ```

* To run API tests:
   ```
   pytest tests/api
   ```
* To run UI tests:
    ```
    pytest tests/ui
    ```

### Via pytest-html report

To run all tests:

   ```
   pytest tests --html=report.html
   ```

### Via Allure

Before using Allure reporting, you need to have the Allure command-line tool installed on your machine. You can follow
the installation instructions provided on the Allure
website: [Allure Installation Guide](https://docs.qameta.io/allure/#_installing_a_commandline) and look
at [Pytest with Allure documentation](https://docs.qameta.io/allure/#_pytest)

1. To run all tests:
   ```
    pytest --alluredir=allure_results
   ```
2. To see the actual Allure report execute this:
    ```
    allure serve allure_results
    ```

### Via Docker

1. Install Docker on your machine
2. Make sure that Docker is running
3. Build the Docker image:

```
docker-compose build
```

4. Run the tests in a Docker container:

```
docker-compose up
```

## Additional information

Some test are marked as skipped due to limit of working with github api.
After executing the api helpers or running the api tests, github blocks user for some time, so tests start to fail.
To minimize these risks, we skipped some tests.
What tests are NOT skipped:

UI:

- test_create_gists.py (2 working tests)
- test_get_one_private_gist.py (2 working tests)

API:

- test_create_gist.py (1 working test)
- test_get_gists.py (4 working tests)