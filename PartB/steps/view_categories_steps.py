import requests
from behave import *

BASE_URL = "http://localhost:4567"

@given('the Category API is running for View Categories')
def step_check_api_running_view_categories(context):
    """Ensure the Category API is running for the View Categories feature."""
    response = requests.get(BASE_URL)
    assert response.status_code == 200, f"API is not running. Status: {response.status_code}"

@given('the database is cleared of all categories')
def step_clear_all_categories(context):
    """Clear all categories in the database to simulate an empty state."""
    response = requests.get(f"{BASE_URL}/categories")
    if response.status_code == 200:
        categories = response.json().get('categories', [])
        for category in categories:
            category_id = category.get("id")
            delete_response = requests.delete(f"{BASE_URL}/categories/{category_id}")
            assert delete_response.status_code == 200, f"Failed to delete category {category_id}"

@when('the user sends a GET request to /categories')
def step_view_all_categories(context):
    """Send a GET request to retrieve all categories."""
    context.response = requests.get(f"{BASE_URL}/categories")

@then('the response status for View Categories should be {status_code}')
def step_check_response_status_view_categories(context, status_code):
    """Check if the response status matches the expected value."""
    assert context.response.status_code == int(status_code), \
        f"Expected {status_code}, got {context.response.status_code}"

@then('the response should contain a list of categories in JSON format')
def step_check_response_content_view_categories(context):
    """Verify that the response contains a list of categories in JSON format."""
    assert 'categories' in context.response.json(), "Response does not contain a 'categories' field"
    assert isinstance(context.response.json()['categories'], list), "Categories field is not a list"

@then('the response should contain an empty categories list')
def step_check_response_empty_list_view_categories(context):
    """Verify that the response contains an empty list of categories specifically for view categories."""
    categories = context.response.json().get('categories', [])
    assert isinstance(categories, list), "Categories field is not a list"
    assert len(categories) == 0, "Expected an empty list, but categories were found"
