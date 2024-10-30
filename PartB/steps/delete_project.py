import requests
from behave import *

BASE_URL = "http://localhost:4567"

@when('I send a DELETE request to /projects/:id')
def step_send_delete_project(context):
    project_id = context.project_id
    context.response = requests.delete(f"{BASE_URL}/projects/{project_id}")

@when('I send a DELETE request to /projects/:id and the project has dependencies')
def step_send_delete_project_with_dependencies(context):
    # Create a project
    headers = {'Content-Type': 'application/json'}
    project_data = {
        "title": "Project with Dependencies",
        "description": "This project has todos",
        "completed": False,
        "active": True
    }
    project_response = requests.post(f"{BASE_URL}/projects", headers=headers, json=project_data)
    assert project_response.status_code == 201, f"Failed to create a project with dependencies"
    project_id = project_response.json().get("id")

    # Create a todo (dependency) associated with the project
    todo_data = {
        "title": "Todo for the project",
        "description": "This todo belongs to the project"
    }
    todo_response = requests.post(f"{BASE_URL}/todos", headers=headers, json=todo_data)
    assert todo_response.status_code == 201, "Failed to create a todo for the project"
    todo_id = todo_response.json().get("id")

    # Save project ID to context and then delete the project
    context.project_id = project_id
    context.response = requests.delete(f"{BASE_URL}/projects/{project_id}")

@when('I send a DELETE request to /projects/:id with an invalid ID')
def step_send_delete_invalid_id(context):
    invalid_id = "999999"  # Assuming this ID does not exist
    context.response = requests.delete(f"{BASE_URL}/projects/{invalid_id}")

@then('the project is deleted successfully')
def step_check_project_deleted(context):
    assert context.response.status_code == 200, \
        f"Expected 200 No Content, but got {context.response.status_code}"

    # Check if the project no longer exists
    project_id = context.project_id
    check_response = requests.get(f"{BASE_URL}/projects/{project_id}")
    assert check_response.status_code == 404, "Project was not deleted successfully"

@then('the project is deleted and the dependencies are either removed or unlinked')
def step_check_dependencies_removed_or_unlinked(context):
    assert context.response.status_code == 200, \
        f"Expected 200 No Content, but got {context.response.status_code}"

    # Verify project is deleted
    project_id = context.project_id
    check_response = requests.get(f"{BASE_URL}/projects/{project_id}")
    assert check_response.status_code == 404, "Project was not deleted successfully"

    todos_response = requests.get(f"{BASE_URL}/todos")
    assert todos_response.status_code == 200, "Failed to retrieve todos"
    
    todos = todos_response.json()['todos']
    
    # Assuming todos related to a project have a specific title or description pattern
    for todo in todos:
        if "Todo for the project" in todo['title'] or todo['description'] == "This todo belongs to the project":
            assert 'projectId' not in todo or todo['projectId'] != project_id, \
                f"Todo {todo['id']} is still linked to the deleted project"