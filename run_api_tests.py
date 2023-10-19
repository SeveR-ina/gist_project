import pytest
import os

# Set the test directory to the location of your tests
test_directory = os.path.join(os.path.dirname(__file__), 'tests/api')

# Set the output directory to the location of the Allure results
output_directory = os.path.join(os.path.dirname(__file__), 'allure_results/api')

# Run the API tests with Allure reporting
pytest.main([
    test_directory,               # Path to the test directory
    '--alluredir', output_directory,  # Path to the Allure results directory
    '--allure-epics', 'API Tests'     # Optional: Set an epic label for your tests
])
