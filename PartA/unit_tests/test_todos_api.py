import unittest
import requests
import json

BASE_URL = "http://localhost:4567"

class TestTodoAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create a Todo and Category for general use in subsequent tests"""
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
        """Clean up the created Todo and Category"""
        # Delete the class-level Todo and Category only if they still exist
        requests.delete(f"{BASE_URL}/todos/{cls.todo_id}")
        requests.delete(f"{BASE_URL}/categories/{cls.category_id}")

    def setUp(self):
        # Assign the class-level IDs to instance-level variables
        self.todo_id = self.__class__.todo_id
        self.category_id = self.__class__.category_id

    def test_post_todos(self):
        """Test POST /todos - Valid, Invalid JSON, Malformed JSON and Malformed XML Cases"""
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

        headers_xml = {'Content-Type': 'application/xml'}
        malformed_xml = '<todo><title>Invalid Todo</title><doneStatus>true'  # Missing closing tags
        response = requests.post(f"{BASE_URL}/todos", headers=headers_xml, data=malformed_xml)
        self.assertEqual(response.status_code, 400)
        

    def test_head_todos(self):
        """Test HEAD /todos - Valid Case"""
        response = requests.head(f"{BASE_URL}/todos")
        self.assertEqual(response.status_code, 200)

        response = requests.head(f"{BASE_URL}/invalidEndpoint")
        self.assertEqual(response.status_code, 404)

    def test_get_todos(self):
        """Test GET /todos - Valid and Invalid Cases"""
        headers = {'Accept': 'application/json'}
        response = requests.get(f"{BASE_URL}/todos", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.headers['Content-Type'])

        # Invalid GET request
        response = requests.get(f"{BASE_URL}/invalidEndpoint", headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_get_todo_by_id(self):
        """Test GET /todos/:id - Valid and Invalid Cases"""
        headers = {'Accept': 'application/json'}
        response = requests.get(f"{BASE_URL}/todos/{self.todo_id}", headers=headers)
        self.assertEqual(response.status_code, 200)

        # Invalid Todo ID
        response = requests.get(f"{BASE_URL}/todos/99999", headers=headers)
        self.assertEqual(response.status_code, 404)

        # Invalid HEAD request (non-existent endpoint)
        response = requests.head(f"{BASE_URL}/invalidEndpoint")
        self.assertEqual(response.status_code, 404)
    
    def test_head_todo_by_id(self):
        """Test HEAD /todos/:id - Valid and Invalid Cases"""
        response = requests.head(f"{BASE_URL}/todos/{self.todo_id}")
        self.assertEqual(response.status_code, 200)

        # Invalid Todo ID
        response = requests.head(f"{BASE_URL}/todos/99999")
        self.assertEqual(response.status_code, 404)

    def test_post_todos_amend_by_id(self):
        """Test PUT /todos/:id - Valid and Invalid Cases"""
        headers = {'Content-Type': 'application/json'}
        valid_update = {"title": "Updated Todo", "doneStatus": True, "description": "Updated description"}
        response = requests.post(f"{BASE_URL}/todos/{self.todo_id}", headers=headers, json=valid_update)
        self.assertEqual(response.status_code, 200)

        # Invalid PUT Request with Missing Fields
        invalid_update = {"doneStatus": "invalid_boolean"}
        response = requests.post(f"{BASE_URL}/todos/{self.todo_id}", headers=headers, json=invalid_update)
        self.assertEqual(response.status_code, 400)
    
    def test_put_todo_by_id(self):
        """Test PUT /todos/:id - Valid and Invalid Cases"""
        headers = {'Content-Type': 'application/json'}
        valid_update = {"title": "Updated Todo", "doneStatus": True, "description": "Updated description"}
        response = requests.put(f"{BASE_URL}/todos/{self.todo_id}", headers=headers, json=valid_update)
        self.assertEqual(response.status_code, 200)

        # Invalid PUT Request with Missing Fields
        invalid_update = {"doneStatus": "invalid_boolean"}
        response = requests.put(f"{BASE_URL}/todos/{self.todo_id}", headers=headers, json=invalid_update)
        self.assertEqual(response.status_code, 400)

    def test_delete_todo_by_id(self):
        """Test DELETE /todos/:id - Valid and Already Deleted Cases"""
        # Create a separate Todo for deletion test
        headers = {'Content-Type': 'application/json'}
        todo_data = {"title": "Delete Test Todo", "doneStatus": False, "description": "todo to delete"}
        response = requests.post(f"{BASE_URL}/todos", headers=headers, json=todo_data)
        self.assertEqual(response.status_code, 201)
        delete_todo_id = response.json()['id']

        # Valid deletion
        response = requests.delete(f"{BASE_URL}/todos/{delete_todo_id}")
        self.assertEqual(response.status_code, 200)

        # Trying to delete the same ID again
        response = requests.delete(f"{BASE_URL}/todos/{delete_todo_id}")
        self.assertEqual(response.status_code, 404)

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

        # Retrieve Headers for Categories Linked to Todo (HEAD)
        response = requests.head(f"{BASE_URL}/todos/{self.todo_id}/categories")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Content-Type', response.headers)

        # Delete the Category Relationship
        response = requests.delete(f"{BASE_URL}/todos/{self.todo_id}/categories/{self.category_id}")
        self.assertEqual(response.status_code, 200)

        # Attempt to Delete a Non-Existent Relationship
        response = requests.delete(f"{BASE_URL}/todos/{self.todo_id}/categories/99999")
        self.assertEqual(response.status_code, 404)

    def test_post_todo_invalid_done_status(self):
        """Test POST /todos - Invalid data type for `doneStatus` field"""
        headers = {'Content-Type': 'application/json'}
        invalid_todo = {"title": "Invalid Todo", "doneStatus": "notABoolean", "description": "Invalid boolean for doneStatus"}
        response = requests.post(f"{BASE_URL}/todos", headers=headers, json=invalid_todo)
        self.assertEqual(response.status_code, 400)  # Expecting Bad Request due to invalid data type

    def test_post_to_invalid_todo_id(self):
        """Test POST /todos/:id - Using POST to an unsupported endpoint"""
        headers = {'Content-Type': 'application/json'}
        # Attempt to POST to a non-existent Todo ID
        invalid_post_data = {"title": "Invalid POST"}
        response = requests.post(f"{BASE_URL}/todos/9999", headers=headers, json=invalid_post_data)
        self.assertEqual(response.status_code, 404)  # Expecting Not Found due to non-existent ID

    def test_patch_undocumented_method(self):
        """Test PATCH /todos/:id - Attempting to update with PATCH (undocumented)"""
        headers = {'Content-Type': 'application/json'}
        patch_data = {"title": "Updated Title with PATCH"}
        response = requests.patch(f"{BASE_URL}/todos/{self.todo_id}", headers=headers, json=patch_data)
        self.assertEqual(response.status_code, 405)  # Expecting Method Not Allowed as PATCH is not supported

if __name__ == "__main__":
    unittest.main()
