import requests
from behave import *

BASE_URL = "http://localhost:4567"

@given('the Category API is running for Delete Category')
def step_check_api_running_delete_category(context):
    """Ensure the Category API is running for the Delete Category feature."""
    response = requests.get(BASE_URL)
    assert response.status_code == 200, f"API is not running. Status: {response.status_code}"

@given('a category with ID "{category_id}" exists')
def step_ensure_category_exists(context, category_id):
    """Ensure a category with the specified ID exists for deletion."""
    # Check if the category exists
    response = requests.get(f"{BASE_URL}/categories/{category_id}")
    if response.status_code == 404:
        # If it doesn't exist, create a new category
        category_data = {"title": "Test Category", "description": "Category for deletion test"}
        create_response = requests.post(f"{BASE_URL}/categories", json=category_data)
        assert create_response.status_code == 201, "Failed to create a category for testing deletion"
        # Store the created category ID
        context.category_id = create_response.json().get("id")
    else:
        context.category_id = category_id

@when('the user sends a DELETE request to /categories/{category_id}')
def step_delete_category(context, category_id):
    """Send a DELETE request to remove a specific category by ID."""
    # If the category ID is 999 (non-existent test), use it directly without setup.
    if category_id == "999":
        context.response = requests.delete(f"{BASE_URL}/categories/{category_id}")
    else:
        # Otherwise, use the existing ID if it was created in the setup
        actual_id = context.category_id if hasattr(context, 'category_id') else category_id
        context.response = requests.delete(f"{BASE_URL}/categories/{actual_id}")

@then('the response status for Delete Category should be {status_code}')
def step_check_response_status_delete_category(context, status_code):
    """Check if the response status matches the expected value."""
    assert context.response.status_code == int(status_code), \
        f"Expected {status_code}, got {context.response.status_code}"
