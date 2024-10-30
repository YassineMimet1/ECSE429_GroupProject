import requests
from behave import *

BASE_URL = "http://localhost:4567"

@given('the Todo API is running for Delete Todo')
def step_check_api_running_delete_todo(context):
    """Ensure the Todo API is running for the Delete Todo feature."""
    response = requests.get(BASE_URL)
    assert response.status_code == 200, f"API is not running. Status: {response.status_code}"

@given('a todo with ID <todo_id> exists to delete')
def step_create_todo_for_delete(context):
    """Create a todo for delete operations."""
    headers = {'Content-Type': 'application/json'}
    todo_data = {"title": "Delete Test Todo", "description": "To be deleted"}
    response = requests.post(f"{BASE_URL}/todos", headers=headers, json=todo_data)
    assert response.status_code == 201
    context.todo_id = response.json().get('id')

@given('the todo with ID <todo_id> is linked to a category')
def step_link_todo_to_category(context):
    """Link the todo to a category before deletion."""
    # Create a category
    headers = {'Content-Type': 'application/json'}
    category_data = {"title": "Linked Category", "description": "A category linked to the todo"}
    response = requests.post(f"{BASE_URL}/categories", headers=headers, json=category_data)
    assert response.status_code == 201
    category_id = response.json().get('id')

    # Link the todo to the category
    link_data = {"id": context.todo_id}
    response = requests.post(f"{BASE_URL}/categories/{category_id}/todos", headers=headers, json=link_data)
    assert response.status_code == 201, f"Failed to link todo to category. Status: {response.status_code}"

@when('the user sends a DELETE request to /todos/<todo_id>')
def step_delete_todo(context):
    """Send a DELETE request to delete the todo."""
    context.response = requests.delete(f"{BASE_URL}/todos/{context.todo_id}")

@when('the user sends a DELETE request to /todos/99999')
def step_delete_nonexistent_todo(context):
    """Send a DELETE request for a non-existent todo."""
    context.response = requests.delete(f"{BASE_URL}/todos/99999")

@then('the response status for Delete Todo should be {status_code}')
def step_check_delete_response_status(context, status_code):
    """Verify that the response status code matches the expected value."""
    assert context.response.status_code == int(status_code), \
        f"Expected {status_code}, got {context.response.status_code}"
