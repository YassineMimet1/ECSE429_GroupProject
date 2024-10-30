import requests
from behave import *

BASE_URL = "http://localhost:4567"

@given('the Todo API is running for Retrieve Todos')
def step_check_api_running_retrieve_todos(context):
    """Ensure the Todo API is running for the Retrieve Todos feature."""
    response = requests.get(BASE_URL)
    assert response.status_code == 200, f"API is not running. Status: {response.status_code}"

@given('multiple todos exist')
def step_create_multiple_todos(context):
    """Ensure multiple todos exist in the API."""
    headers = {'Content-Type': 'application/json'}
    todos = [
        {"title": "Test Todo 1", "description": "This is the first test todo"},
        {"title": "Test Todo 2", "description": "This is the second test todo"}
    ]
    for todo in todos:
        response = requests.post(f"{BASE_URL}/todos", headers=headers, json=todo)
        assert response.status_code == 201, f"Failed to create todo. Status: {response.status_code}"

@when('the user sends a GET request to /todos with Accept header "{header}"')
def step_get_todos_with_header(context, header):
    """Send a GET request to /todos with the specified Accept header."""
    headers = {'Accept': header}
    context.response = requests.get(f"{BASE_URL}/todos", headers=headers)

@when('the user sends a GET request to /invalidEndpoint')
def step_get_invalid_endpoint(context):
    """Send a GET request to an invalid endpoint."""
    context.response = requests.get(f"{BASE_URL}/invalidEndpoint")

@then('the response status for Retrieve Todos should be {status_code}')
def step_check_response_status_retrieve_todos(context, status_code):
    """Check if the response status matches the expected status for Retrieve Todos."""
    assert context.response.status_code == int(status_code), \
        f"Expected {status_code}, got {context.response.status_code}"
