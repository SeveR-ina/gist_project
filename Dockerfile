# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install project dependencies
RUN pip install -r requirements.txt

# Entry point to run your tests
CMD ["pytest", "--alluredir=/app/allure_results", "tests"]