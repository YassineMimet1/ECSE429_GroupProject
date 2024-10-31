import requests
from behave import *

BASE_URL = "http://localhost:4567"

@given('the Todo API is running')
def step_check_api_running(context):
    response = requests.get(BASE_URL)
    assert response.status_code == 200, f"API is not running. Status: {response.status_code}"

@when('I send a POST request to /projects with valid project data')
def step_send_post_valid_project(context):
    headers = {'Content-Type': 'application/json'}
    data = {
        "title": "New Project",
        "description": "This is a test project",
        "completed": False,
        "active": True
    }
    context.response = requests.post(f"{BASE_URL}/projects", headers=headers, json=data)

@when('I send a POST request to /projects with missing optional fields')
def step_send_post_missing_optional_fields(context):
    headers = {'Content-Type': 'application/json'}
    data = {
        "title": "New Project Without Optional Fields"
        # No description, completed, or active fields
    }
    context.response = requests.post(f"{BASE_URL}/projects", headers=headers, json=data)

@when('I send a POST request to /projects with invalid data')
def step_send_post_invalid_data(context):
    headers = {'Content-Type': 'application/json'}
    data = {
        "title": "Project with Invalid Data",
        "description": "This project contains invalid data for the completed field",
        "completed": "invalid_boolean"  # This should be a boolean, but we send a string
    }
    context.response = requests.post(f"{BASE_URL}/projects", headers=headers, json=data)

@then('a new project is created with an ID returned in the response')
def step_check_project_created(context):
    assert context.response.status_code == 201, \
        f"Expected status code 201, but got {context.response.status_code}"
    response_data = context.response.json()
    assert "id" in response_data, "No project ID returned in the response"

@then('the project is created with default values for the missing fields')
def step_check_project_with_default_values(context):
    assert context.response.status_code == 201, \
        f"Expected status code 201, but got {context.response.status_code}"
    project = context.response.json()
    print(project)
    assert project['description'] == '', "Default description is not empty"
    assert project['completed'] == 'false', "Default completed status is not false"
    assert project['active'] == 'false', "Default active status is not false"

@then('I receive a 400 Bad Request response')
def step_check_400_status(context):
    assert context.response.status_code == 400, \
        f"Expected 400 Bad Request, but got {context.response.status_code}"
