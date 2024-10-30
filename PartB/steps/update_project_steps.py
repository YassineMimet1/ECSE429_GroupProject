import requests
from behave import *

BASE_URL = "http://localhost:4567"

@given('a project exists with a specific ID')
def step_check_project_exists(context):
    # Ensure there is a project to update (for example, creating one)
    headers = {'Content-Type': 'application/json'}
    data = {
        "title": "Initial Project",
        "description": "Initial description",
        "completed": False,
        "active": True
    }
    response = requests.post(f"{BASE_URL}/projects", headers=headers, json=data)
    assert response.status_code == 201, "Failed to create a project to test updates"
    context.project_id = response.json().get("id")

@when('I send a PUT request to /projects/:id with updated data')
def step_update_project_with_data(context):
    headers = {'Content-Type': 'application/json'}
    updated_data = {
        "title": "Updated Project Title",
        "description": "Updated Project Description",
        "completed": True,
        "active": False
    }
    project_id = context.project_id
    context.response = requests.put(f"{BASE_URL}/projects/{project_id}", headers=headers, json=updated_data)

@when('I send a PUT request to /projects/:id with only the description updated')
def step_update_project_description_only(context):
    headers = {'Content-Type': 'application/json'}
    updated_data = {
        "description": "Updated Description Only"
    }
    project_id = context.project_id
    context.response = requests.put(f"{BASE_URL}/projects/{project_id}", headers=headers, json=updated_data)

@when('I send a PUT request to /projects/:id with an invalid ID')
def step_update_project_invalid_id(context):
    headers = {'Content-Type': 'application/json'}
    updated_data = {
        "title": "Project With Invalid ID",
        "description": "Trying to update a project with an invalid ID"
    }
    invalid_id = "999999"  # Assuming this ID does not exist
    context.response = requests.put(f"{BASE_URL}/projects/{invalid_id}", headers=headers, json=updated_data)

@then('the project is updated successfully with the new data reflected')
def step_check_project_updated(context):
    assert context.response.status_code == 200, \
        f"Expected 200 OK, but got {context.response.status_code}"
    project = context.response.json()
    assert project['title'] == "Updated Project Title", "Project title was not updated"
    assert project['description'] == "Updated Project Description", "Project description was not updated"
    assert project['completed'] == 'true', "Project completed status was not updated"
    assert project['active'] == 'false', "Project active status was not updated"

@then('only the description is updated and other fields remain unchanged')
def step_check_only_description_updated(context):
    assert context.response.status_code == 200, \
        f"Expected 200 OK, but got {context.response.status_code}"
    project = context.response.json()
    assert project['description'] == "Updated Description Only", "Project description was not updated"

@then('I receive a 404 Not Found response')
def step_check_404_status(context):
    assert context.response.status_code == 404, \
        f"Expected 404 Not Found, but got {context.response.status_code}"
