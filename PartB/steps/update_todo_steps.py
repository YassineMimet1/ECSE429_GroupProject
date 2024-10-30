import requests
from behave import *

BASE_URL = "http://localhost:4567"

@given('the Todo API is running for Update Todo')
def step_check_api_running_update_todo(context):
    """Ensure the Todo API is running for the Update Todo feature."""
    response = requests.get(BASE_URL)
    assert response.status_code == 200, f"API is not running. Status: {response.status_code}"

@given('a todo with ID <todo_id> exists')
def step_create_todo_for_update(context):
    """Create a todo for update operations."""
    headers = {'Content-Type': 'application/json'}
    todo_data = {"title": "Old Title", "description": "Old Description"}
    response = requests.post(f"{BASE_URL}/todos", headers=headers, json=todo_data)
    assert response.status_code == 201
    context.todo_id = response.json().get('id')

@when('the user sends a PUT request to /todos/<todo_id> with "{title}" and "{description}"')
def step_update_todo_with_data(context, title, description):
    """Send a PUT request to update the todo with new title and description."""
    headers = {'Content-Type': 'application/json'}
    data = {"title": title, "description": description}
    context.response = requests.put(f"{BASE_URL}/todos/{context.todo_id}", headers=headers, json=data)

@when('the user sends a PUT request to /todos/<todo_id> with only a new title "{title}"')
def step_update_todo_with_partial_data(context, title):
    """Send a PUT request to update the todo with only a new title."""
    headers = {'Content-Type': 'application/json'}
    data = {"title": title}
    context.response = requests.put(f"{BASE_URL}/todos/{context.todo_id}", headers=headers, json=data)

@when('the user sends a PUT request to /todos/99999 with "{title}" and "{description}"')
def step_update_non_existent_todo(context, title, description):
    """Send a PUT request to update a non-existent todo."""
    headers = {'Content-Type': 'application/json'}
    data = {"title": title, "description": description}
    context.response = requests.put(f"{BASE_URL}/todos/99999", headers=headers, json=data)

@then('the response status for Update Todo should be {status_code}')
def step_check_update_response_status(context, status_code):
    """Verify that the response status code matches the expected value."""
    assert context.response.status_code == int(status_code), \
        f"Expected {status_code}, got {context.response.status_code}"
