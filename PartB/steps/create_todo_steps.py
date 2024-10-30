import requests
from behave import *

BASE_URL = "http://localhost:4567"

@given('the Todo API is running for Create Todo')
def step_check_api_running_create_todo(context):
    """Ensure the Todo API is running for the Create Todo feature."""
    response = requests.get(BASE_URL)
    assert response.status_code == 200, f"API is not running. Status: {response.status_code}"

@when('the user sends a POST request to /todos with "{title}" and "{description}"')
@when('the user sends a POST request to /todos with "{title}" and no description')
def step_create_todo_dynamic(context, title, description=""):
    """Send a POST request to create a new todo with or without a description."""
    headers = {'Content-Type': 'application/json'}
    data = {"title": title}

    if description and description.lower() != "no description":
        data["description"] = description

    context.response = requests.post(f"{BASE_URL}/todos", headers=headers, json=data)

@when('the user sends a POST request to /todos with malformed JSON')
def step_create_todo_with_malformed_json(context):
    """Send a POST request with malformed JSON to simulate an error."""
    headers = {'Content-Type': 'application/json'}
    malformed_data = '{"title": "Invalid Todo", "description": '  # Missing closing brace

    context.response = requests.post(f"{BASE_URL}/todos", headers=headers, data=malformed_data)

@then('the response status for Create Todo should be {status_code}')
def step_check_response_status_create_todo(context, status_code):
    """Check if the response status matches the expected value."""
    assert context.response.status_code == int(status_code), \
        f"Expected {status_code}, got {context.response.status_code}"
