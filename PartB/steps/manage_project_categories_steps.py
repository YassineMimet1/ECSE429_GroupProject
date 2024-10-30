import requests
import json
from behave import *

BASE_URL = "http://localhost:4567"

@given('a project exists with categories')
def step_create_project_with_categories(context):
    # Create a project
    headers = {'Content-Type': 'application/json'}
    project_data = {
        "title": "Project with Categories",
        "description": "This project has categories",
        "completed": False,
        "active": True
    }
    project_response = requests.post(f"{BASE_URL}/projects", headers=headers, json=project_data)
    assert project_response.status_code == 201, "Failed to create project"
    context.project_id = project_response.json().get("id")

    # Create a category
    category_data = {
        "title": "Category 1"
    }
    category_response = requests.post(f"{BASE_URL}/categories", headers=headers, json=category_data)
    assert category_response.status_code == 201, "Failed to create category"
    context.category_id = category_response.json().get("id")

    # Link the category to the project
    link_data = {'id': context.category_id}
    link_response = requests.post(f"{BASE_URL}/projects/{context.project_id}/categories", headers=headers, json=link_data)
    assert link_response.status_code == 201, "Failed to link category to the project"

@when('I send a GET request to /projects/:id/categories')
def step_get_project_categories(context):
    project_id = context.project_id
    context.response = requests.get(f"{BASE_URL}/projects/{project_id}/categories")

@then('I receive a list of categories related to the project')
def step_verify_project_categories(context):
    assert context.response.status_code == 200, \
        f"Expected status code 200, but got {context.response.status_code}"
    
    categories = context.response.json().get('categories', [])
    assert len(categories) > 0, "No categories returned for the project"
    assert any(category['id'] == context.category_id for category in categories), "Expected category not found"

@when('I send a POST request to /projects/:id/categories with valid category data')
def step_add_category_to_project(context):
    headers = {'Content-Type': 'application/json'}
    project_id = context.project_id

    # Create another category to be added
    new_category_data = {
        "title": "New Category"
    }
    category_response = requests.post(f"{BASE_URL}/categories", headers=headers, json=new_category_data)
    assert category_response.status_code == 201, "Failed to create new category"
    new_category_id = category_response.json().get("id")

    # Link the new category to the project
    link_data = {'id': new_category_id}
    context.response = requests.post(f"{BASE_URL}/projects/{project_id}/categories", headers=headers, json=link_data)

@then('the category is successfully added to the project')
def step_verify_category_added(context):
    assert context.response.status_code == 201, \
        f"Expected status code 201, but got {context.response.status_code}"

    # Verify the category was added
    project_id = context.project_id
    get_response = requests.get(f"{BASE_URL}/projects/{project_id}/categories")
    categories = get_response.json().get('categories', [])
    assert any(category['title'] == "New Category" for category in categories), \
        "New category was not successfully added to the project"

@when('I send a POST request to /projects/:id/categories with an invalid category ID')
def step_add_invalid_category_to_project(context):
    headers = {'Content-Type': 'application/json'}
    project_id = context.project_id

    # Attempt to link a non-existent (invalid) category ID
    invalid_category_id = "999999"  # Assume this ID does not exist
    link_data = {'id': invalid_category_id}
    context.response = requests.post(f"{BASE_URL}/projects/{project_id}/categories", headers=headers, json=link_data)

@then('I receive a 404 Bad Request response')
def step_verify_bad_request(context):
    assert context.response.status_code == 404, \
        f"Expected status code 404, but got {context.response.status_code}"
