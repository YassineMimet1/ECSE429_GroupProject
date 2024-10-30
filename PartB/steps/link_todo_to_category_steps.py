import requests
from behave import *

BASE_URL = "http://localhost:4567"

@given('the Todo API is running for Linking Todos')
def step_check_api_running_linking_todos(context):
    """Ensure the Todo API is running."""
    response = requests.get(BASE_URL)
    assert response.status_code == 200, f"API is not running. Status: {response.status_code}"

@given('a category with ID <category_id> exists for linking todo to a category')
def step_create_category_for_linking(context):
    """Create the first category."""
    headers = {'Content-Type': 'application/json'}
    category_data = {"title": "Category One", "description": "First category"}
    response = requests.post(f"{BASE_URL}/categories", headers=headers, json=category_data)
    assert response.status_code == 201
    context.category_id = response.json().get('id')

@given('a second category with ID <second_category_id> exists for linking todo to another category')
def step_create_second_category_for_linking(context):
    """Create the second category."""
    headers = {'Content-Type': 'application/json'}
    category_data = {"title": "Category Two", "description": "Second category"}
    response = requests.post(f"{BASE_URL}/categories", headers=headers, json=category_data)
    assert response.status_code == 201
    context.second_category_id = response.json().get('id')

@given('a todo with ID <todo_id> exists for linking todo to a category')
def step_create_todo_for_linking(context):
    """Create a todo to link with categories."""
    headers = {'Content-Type': 'application/json'}
    todo_data = {"title": "Link Test Todo", "description": "Todo to link with categories"}
    response = requests.post(f"{BASE_URL}/todos", headers=headers, json=todo_data)
    assert response.status_code == 201
    context.todo_id = response.json().get('id')

@when('the user sends a POST request to /categories/<category_id>/todos with <todo_id>')
def step_link_todo_to_first_category(context):
    """Link the todo to the first category."""
    context.response = requests.post(
        f"{BASE_URL}/categories/{context.category_id}/todos", 
        json={"id": context.todo_id}
    )

@when('the user sends a POST request to /categories/<second_category_id>/todos with <todo_id>')
def step_link_todo_to_second_category(context):
    """Link the todo to the second category."""
    context.response = requests.post(
        f"{BASE_URL}/categories/{context.second_category_id}/todos", 
        json={"id": context.todo_id}
    )

@when('the user sends a POST request to /categories/<category_id>/todos with 99999')
def step_link_nonexistent_todo(context):
    """Attempt to link a non-existent todo to the first category."""
    context.response = requests.post(
        f"{BASE_URL}/categories/{context.category_id}/todos", 
        json={"id": 99999}
    )

@then('the response status for Linking Todos should be {status_code}')
def step_check_link_response_status(context, status_code):
    """Verify the response status code matches the expected value."""
    assert context.response.status_code == int(status_code), \
        f"Expected {status_code}, got {context.response.status_code}"
