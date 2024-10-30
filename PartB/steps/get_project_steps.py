import requests
from behave import *

BASE_URL = "http://localhost:4567"

@when('I send a GET request to /projects')
def step_send_get_projects(context):
    context.response = requests.get(f"{BASE_URL}/projects")

@when('I send a GET request to /projects with completed=false')
def step_send_get_incomplete_projects(context):
    params = {'completed': False}
    context.response = requests.get(f"{BASE_URL}/projects", params=params)

@when('I send a GET request to /projects with completed=invalid_value')
def step_send_get_projects_invalid_filter(context):
    params = {'completed': 'invalid_value'}
    context.response = requests.get(f"{BASE_URL}/projects", params=params)

@then('I received a 200 Status response instead of 400')
def step_check_400_status(context):
    assert context.response.status_code == 200, \
        f"Expected a 400 Bad Request, but got {context.response.status_code}"

@then('I receive a response containing a list of all projects in JSON format')
def step_check_response_json_format(context):
    assert context.response.headers['Content-Type'] == 'application/json', \
        "Response is not in JSON format"

    response_data = context.response.json()

    assert 'projects' in response_data, "'projects' key not found in the response"
    assert isinstance(response_data['projects'], list), "'projects' is not a list"

@then('I receive a response containing all incomplete projects')
def step_check_incomplete_projects(context):
    projects = context.response.json()['projects']
    assert all(not project.get('completed', True) for project in projects), \
        "Not all projects are incomplete"
