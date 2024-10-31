import requests
from behave import *

BASE_URL = "http://localhost:4567"

@given('the Category API is running for Create Category')
def step_check_api_running_create_category(context):
    """Ensure the Category API is running for the Create Category feature."""
    response = requests.get(BASE_URL)
    assert response.status_code == 200, f"API is not running. Status: {response.status_code}"

@when('the user sends a POST request to /categories with "{title}" and "{description}"')
@when('the user sends a POST request to /categories with "{title}" and no description')
def step_create_category_dynamic(context, title, description=""):
    """Send a POST request to create a new category with or without a description."""
    headers = {'Content-Type': 'application/json'}
    data = {"title": title}

    if description and description.lower() != "no description":
        data["description"] = description

    context.response = requests.post(f"{BASE_URL}/categories", headers=headers, json=data)

@when('the user sends a POST request to /categories with malformed JSON')
def step_create_category_with_malformed_json(context):
    """Send a POST request with malformed JSON to simulate an error."""
    headers = {'Content-Type': 'application/json'}
    malformed_data = '{"title": "Invalid Category", "description": '  # Missing closing brace

    context.response = requests.post(f"{BASE_URL}/categories", headers=headers, data=malformed_data)

@then('the response status for Create Category should be {status_code}')
def step_check_response_status_create_category(context, status_code):
    """Check if the response status matches the expected value."""
    assert context.response.status_code == int(status_code), \
        f"Expected {status_code}, got {context.response.status_code}"
