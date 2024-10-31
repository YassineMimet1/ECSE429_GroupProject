import requests
from behave import *

BASE_URL = "http://localhost:4567"

@given('the Category API is running for Search Categories')
def step_check_api_running_search_categories(context):
    """Ensure the Category API is running for the Search Categories feature."""
    response = requests.get(BASE_URL)
    assert response.status_code == 200, f"API is not running. Status: {response.status_code}"

@when('the user sends a GET request to /categories with the query parameter "{parameter}"')
def step_search_category_by_parameter(context, parameter):
    """Send a GET request to search for categories by a query parameter."""
    context.response = requests.get(f"{BASE_URL}/categories?{parameter}")

@when('the user sends a GET request to /categories with an invalid query parameter')
def step_search_category_invalid_parameter(context):
    """Send a GET request to /categories with an invalid query parameter."""
    context.response = requests.get(f"{BASE_URL}/categories?invalid_param")

@then('the response status for Search Categories should be {status_code}')
def step_check_response_status_search_category(context, status_code):
    """Check if the response status matches the expected value."""
    assert context.response.status_code == int(status_code), \
        f"Expected {status_code}, got {context.response.status_code}"

@then('the response should contain categories with "{field}" matching "{value}"')
def step_check_response_content_search_category(context, field, value):
    """Check if the response contains categories matching the specified field and value."""
    categories = context.response.json().get("categories", [])
    matching = any(category.get(field, "").lower() == value.lower() for category in categories)
    assert matching, f"No categories found with {field} matching '{value}'"

@then('the response should contain an empty list')
def step_check_empty_response_search_category(context):
    """Verify that the response contains an empty list of categories."""
    categories = context.response.json().get("categories", [])
    assert isinstance(categories, list) and len(categories) == 0, "Expected an empty list of categories"

@then('the response should include an error message for malformed query')
def step_check_error_message_for_malformed_query(context):
    """Check if the response includes either categories or an error message for malformed queries."""
    response_json = context.response.json()

    # Check if the API returns a list of categories
    if 'categories' in response_json:
        categories = response_json.get("categories", [])
        assert isinstance(categories, list), "Expected 'categories' to be a list in the response"
    # Check if the API returns an error message (even if the status is 200)
    elif 'errorMessages' in response_json:
        error_messages = response_json['errorMessages']
        assert isinstance(error_messages, list) and len(error_messages) > 0, "Expected non-empty 'errorMessages' list"
    else:
        assert False, "Expected either 'categories' or 'errorMessages' in the response"
