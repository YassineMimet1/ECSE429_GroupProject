import unittest
import requests
import json
from requests.exceptions import ConnectionError

BASE_URL = "http://localhost:4567"

class TestTodoAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Ensure the service is running
        try:
            response = requests.get(BASE_URL)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Cannot connect to the service at {BASE_URL}: {e}")

        # Create a Todo for subsequent tests
        headers = {'Content-Type': 'application/json'}
        todo_data = {"title": "Exploratory Testing Todo", "doneStatus": False, "description": "todo to test"}
        response = requests.post(f"{BASE_URL}/todos", headers=headers, json=todo_data)
        if response.status_code == 201:
            try:
                data = response.json()
                cls.todo_id = data.get('id')
                print(f"Created Todo ID: {cls.todo_id}")
            except json.JSONDecodeError:
                raise Exception("Failed to create Todo: Response is not valid JSON")
        else:
            raise Exception(f"Failed to create Todo: Status code {response.status_code}")

        # Create a Category for the category relationship tests
        category_data = {"title": "Urgent", "description": "Tasks that need immediate attention"}
        response = requests.post(f"{BASE_URL}/categories", headers=headers, json=category_data)
        if response.status_code == 201:
            try:
                data = response.json()
                cls.category_id = data.get('id')
                print(f"Created Category ID: {cls.category_id}")
            except json.JSONDecodeError:
                raise Exception("Failed to create Category: Response is not valid JSON")
        else:
            raise Exception(f"Failed to create Category: Status code {response.status_code}")

    @classmethod
    def tearDownClass(cls):
        # Cleanup the created Todo and Category
        requests.delete(f"{BASE_URL}/todos/{cls.todo_id}")
        requests.delete(f"{BASE_URL}/categories/{cls.category_id}")

    def setUp(self):
        # Assign the class-level IDs to instance-level variables
        self.todo_id = self.__class__.todo_id
        self.category_id = self.__class__.category_id

    def test_post_todos(self):
        """Test POST /todos - Valid, Invalid JSON, and Malformed JSON Cases"""
        headers = {'Content-Type': 'application/json'}

        # Valid POST request
        new_todo = {"title": "New Todo", "doneStatus": False, "description": "Another todo"}
        response = requests.post(f"{BASE_URL}/todos", headers=headers, json=new_todo)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Location', response.headers)

        # Malformed JSON
        malformed_json = '{"title": "Invalid Todo", "doneStatus": "notABoolean"'
        response = requests.post(f"{BASE_URL}/todos", headers=headers, data=malformed_json)
        self.assertEqual(response.status_code, 400)

        # Invalid JSON Type
        invalid_json = {"title": 12345, "doneStatus": "not_a_boolean", "description": False}
        response = requests.post(f"{BASE_URL}/todos", headers=headers, json=invalid_json)
        self.assertEqual(response.status_code, 400)

    def test_get_todos(self):
        """Test GET /todos - Valid and Invalid Cases"""
        headers = {'Accept': 'application/json'}
        response = requests.get(f"{BASE_URL}/todos", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.headers['Content-Type'])

        # Invalid GET request
        response = requests.get(f"{BASE_URL}/invalidEndpoint", headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_head_todos(self):
        """Test HEAD /todos - Valid and Invalid Cases"""
        response = requests.head(f"{BASE_URL}/todos")
        self.assertEqual(response.status_code, 200)

        # Invalid HEAD request
        response = requests.head(f"{BASE_URL}/invalidEndpoint")
        self.assertEqual(response.status_code, 404)

    def test_post_todos_malformed_xml(self):
        """Test POST /todos with a malformed XML payload"""
        headers = {'Content-Type': 'application/xml'}
        malformed_xml = "<todo><title>Test</title><doneStatus>False</doneStatus>"
        response = requests.post(f"{BASE_URL}/todos", headers=headers, data=malformed_xml)
        self.assertEqual(response.status_code, 400)
    
    def test_post_todos_malformed_json(self):
        """Test POST /todos with a malformed JSON payload"""
        headers = {'Content-Type': 'application/json'}
        malformed_json = '{"title": "Invalid Todo", "doneStatus": "notABoolean"'  # Missing closing brace
        response = requests.post(f"{BASE_URL}/todos", headers=headers, data=malformed_json)
        self.assertEqual(response.status_code, 400)


    def test_get_todo_by_id(self):
        """Test GET /todos/:id - Valid and Invalid Cases"""
        headers = {'Accept': 'application/json'}

        # Create todo
        headers = {'Content-Type': 'application/json'}
        todo_data = {"title": "Exploratory Testing Todo", "doneStatus": False, "description": "todo to test"}
        response = requests.post(f"{BASE_URL}/todos", headers=headers, json=todo_data)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        todo_id = data['id']
        self.todo_id = todo_id

        # Valid request
        response = requests.get(f"{BASE_URL}/todos/{todo_id}", headers=headers)  # No extra quotes around the ID
        self.assertEqual(response.status_code, 200)

        # Invalid Todo ID
        response = requests.get(f"{BASE_URL}/todos/99999", headers=headers)
        self.assertEqual(response.status_code, 404)
    
    def test_put_todos(self):
        # Create todo
        headers = {'Content-Type': 'application/json'}
        todo_data = {"title": "Exploratory Testing Todo", "doneStatus": False, "description": "todo to test"}
        response = requests.post(f"{BASE_URL}/todos", headers=headers, json=todo_data)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        todo_id = data['id']
        self.todo_id = todo_id

        """Test PUT /todos/:id - Valid and Invalid Cases"""
        headers = {'Content-Type': 'application/json'}
        valid_update = {"title": "Updated Todo", "doneStatus": True, "description": "Updated description"}
        response = requests.put(f"{BASE_URL}/todos/{todo_id}", headers=headers, json=valid_update)
        self.assertEqual(response.status_code, 200)

        # Invalid PUT Request with Missing Fields
        invalid_update = {"doneStatus": "invalid_boolean"}
        response = requests.put(f"{BASE_URL}/todos/{todo_id}", headers=headers, json=invalid_update)
        self.assertEqual(response.status_code, 400)

    def test_post_todos_amend(self):
        # Create todo
        headers = {'Content-Type': 'application/json'}
        todo_data = {"title": "Exploratory Testing Todo", "doneStatus": False, "description": "todo to test"}
        response = requests.post(f"{BASE_URL}/todos", headers=headers, json=todo_data)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        todo_id = data['id']
        self.todo_id = todo_id

        """Test PUT /todos/:id - Valid and Invalid Cases"""
        headers = {'Content-Type': 'application/json'}
        valid_update = {"title": "Updated Todo", "doneStatus": True, "description": "Updated description"}
        response = requests.post(f"{BASE_URL}/todos/{todo_id}", headers=headers, json=valid_update)
        self.assertEqual(response.status_code, 200)

        # Invalid PUT Request with Missing Fields
        invalid_update = {"doneStatus": "invalid_boolean"}
        response = requests.post(f"{BASE_URL}/todos/{todo_id}", headers=headers, json=invalid_update)
        self.assertEqual(response.status_code, 400)
    
    def test_category_relationships(self):
        """Test POST, GET, and DELETE /todos/:id/categories - Valid and Invalid Cases"""
        headers = {'Content-Type': 'application/json'}

        # Create Relationship between Todo and Category
        relationship_data = {"id": self.category_id}
        response = requests.post(f"{BASE_URL}/todos/{self.todo_id}/categories", headers=headers, json=relationship_data)
        self.assertEqual(response.status_code, 201)

        # Retrieve Categories Linked to Todo
        response = requests.get(f"{BASE_URL}/todos/{self.todo_id}/categories", headers={'Accept': 'application/json'})
        self.assertEqual(response.status_code, 200)

        # Delete the Category Relationship
        response = requests.delete(f"{BASE_URL}/todos/{self.todo_id}/categories/{self.category_id}")
        self.assertEqual(response.status_code, 200)

        # Attempt to Delete a Non-Existent Relationship
        response = requests.delete(f"{BASE_URL}/todos/{self.todo_id}/categories/99999")
        self.assertEqual(response.status_code, 404)

    def test_delete_todo_by_id(self):
        """Test DELETE /todos/:id - Valid and Already Deleted Cases"""
        response = requests.delete(f"{BASE_URL}/todos/{self.todo_id}")
        self.assertEqual(response.status_code, 200)

        # Trying to delete the same ID again
        response = requests.delete(f"{BASE_URL}/todos/{self.todo_id}")
        self.assertEqual(response.status_code, 404)

    def test_patch_todos(self):
        """Test PATCH /todos/:id - Valid and Invalid Cases"""
        headers = {'Content-Type': 'application/json'}

        # Invalid request (PATCH not supported)
        patch_data = {"title": "Updated Title with PATCH"}
        response = requests.patch(f"{BASE_URL}/todos/{self.todo_id}", headers=headers, json=patch_data)
        self.assertEqual(response.status_code, 405)
if __name__ == "__main__":
    unittest.main()
