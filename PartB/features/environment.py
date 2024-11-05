import requests
import logging

BASE_URL = "http://localhost:4567"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def before_scenario(context, scenario):
    """Set up test data before each scenario."""
    logger.info(f"Running before_scenario for: {scenario.name}")
    print("hello world")

    # Example: Create a test category
    category_data = {"title": "Test Category", "description": "Category for testing"}
    response = requests.post(f"{BASE_URL}/categories", json=category_data)
    if response.status_code == 201:
        context.test_category_id = response.json().get('id')
        logger.info(f"Created test category with ID: {context.test_category_id}")
    else:
        logger.error(f"Failed to create test category. Status: {response.status_code}")

    # Example: Create a test todo
    todo_data = {"title": "Test Todo", "description": "Todo for testing"}
    response = requests.post(f"{BASE_URL}/todos", json=todo_data)
    if response.status_code == 201:
        context.test_todo_id = response.json().get('id')
        logger.info(f"Created test todo with ID: {context.test_todo_id}")
    else:
        logger.error(f"Failed to create test todo. Status: {response.status_code}")

def after_scenario(context, scenario):
    """Restore the system to the initial state after each scenario."""
    logger.info(f"Running after_scenario for: {scenario.name}")

    # Delete all categories
    response = requests.get(f"{BASE_URL}/categories", headers={"Accept": "application/json"})
    if response.status_code == 200:
        categories = response.json().get('categories', [])
        for category in categories:
            delete_response = requests.delete(f"{BASE_URL}/categories/{category['id']}")
            logger.info(f"Deleted category {category['id']}: {delete_response.status_code}")

    # Delete all todos
    response = requests.get(f"{BASE_URL}/todos", headers={"Accept": "application/json"})
    if response.status_code == 200:
        todos = response.json().get('todos', [])
        for todo in todos:
            delete_response = requests.delete(f"{BASE_URL}/todos/{todo['id']}")
            logger.info(f"Deleted todo {todo['id']}: {delete_response.status_code}")

    # Delete all projects
    response = requests.get(f"{BASE_URL}/projects", headers={"Accept": "application/json"})
    if response.status_code == 200:
        projects = response.json().get('projects', [])
        for project in projects:
            delete_response = requests.delete(f"{BASE_URL}/projects/{project['id']}")
            logger.info(f"Deleted project {project['id']}: {delete_response.status_code}")