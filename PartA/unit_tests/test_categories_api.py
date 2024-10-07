import unittest
import requests
import json

BASE_URL = "http://localhost:4567"

class TestCategoriesAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create a Category and Todo for general use in subsequent tests"""
        # Ensure the service is running
        try:
            response = requests.get(BASE_URL)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Cannot connect to the service at {BASE_URL}: {e}")

        # Create a Category for subsequent tests
        headers = {'Content-Type': 'application/json'}
        category_data = {"title": "Exploratory Category", "description": "Category for testing"}
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

        # Create a Todo for relationship testing
        todo_data = {"title": "Test Todo", "doneStatus": False, "description": "Todo for category relationship testing"}
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

    @classmethod
    def tearDownClass(cls):
        """Clean up the created Category and Todo"""
        requests.delete(f"{BASE_URL}/categories/{cls.category_id}")
        requests.delete(f"{BASE_URL}/todos/{cls.todo_id}")

    def setUp(self):
        # Assign the class-level IDs to instance-level variables
        self.category_id = self.__class__.category_id
        self.todo_id = self.__class__.todo_id

    def test_post_categories(self):
        """Test POST /categories - Valid, Invalid JSON, and Malformed JSON Cases"""
        headers = {'Content-Type': 'application/json'}

        # Valid POST request
        new_category = {"title": "New Category", "description": "Another category"}
        response = requests.post(f"{BASE_URL}/categories", headers=headers, json=new_category)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Location', response.headers)

        # Malformed JSON
        malformed_json = '{"title": "Invalid Category", "description":'
        response = requests.post(f"{BASE_URL}/categories", headers=headers, data=malformed_json)
        self.assertEqual(response.status_code, 400)

        # Invalid JSON Type
        invalid_json = {"title": 12345, "description": False}
        response = requests.post(f"{BASE_URL}/categories", headers=headers, json=invalid_json)
        self.assertEqual(response.status_code, 400)

    def test_head_categories(self):
        """Test HEAD /categories - Valid Case"""
        response = requests.head(f"{BASE_URL}/categories")
        self.assertEqual(response.status_code, 200)

        response = requests.head(f"{BASE_URL}/invalidEndpoint")
        self.assertEqual(response.status_code, 404)

    def test_get_categories(self):
        """Test GET /categories - Valid and Invalid Cases"""
        headers = {'Accept': 'application/json'}
        response = requests.get(f"{BASE_URL}/categories", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.headers['Content-Type'])

        # Invalid GET request
        response = requests.get(f"{BASE_URL}/invalidEndpoint", headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_get_category_by_id(self):
        """Test GET /categories/:id - Valid and Invalid Cases"""
        headers = {'Accept': 'application/json'}
        response = requests.get(f"{BASE_URL}/categories/{self.category_id}", headers=headers)
        self.assertEqual(response.status_code, 200)

        # Invalid Category ID
        response = requests.get(f"{BASE_URL}/categories/99999", headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_head_category_by_id(self):
        """Test HEAD /categories/:id - Valid and Invalid Cases"""
        response = requests.head(f"{BASE_URL}/categories/{self.category_id}")
        self.assertEqual(response.status_code, 200)

        # Invalid Category ID
        response = requests.head(f"{BASE_URL}/categories/99999")
        self.assertEqual(response.status_code, 404)

    def test_post_category_amend_by_id(self):
        """Test POST /categories/:id - Valid and Invalid Cases"""
        headers = {'Content-Type': 'application/json'}
        valid_update = {"title": "Updated Category", "description": "Updated category description"}
        response = requests.post(f"{BASE_URL}/categories/{self.category_id}", headers=headers, json=valid_update)
        self.assertEqual(response.status_code, 200)

        # Invalid POST Request with Missing Fields
        invalid_update = {"title": ""}
        response = requests.post(f"{BASE_URL}/categories/{self.category_id}", headers=headers, json=invalid_update)
        self.assertEqual(response.status_code, 400)

    def test_put_category_by_id(self):
        """Test PUT /categories/:id - Valid and Invalid Cases"""
        headers = {'Content-Type': 'application/json'}
        valid_update = {"title": "Updated Category", "description": "Updated description"}
        response = requests.put(f"{BASE_URL}/categories/{self.category_id}", headers=headers, json=valid_update)
        self.assertEqual(response.status_code, 200)

        # Invalid PUT Request with Missing Fields
        invalid_update = {"title": ""}
        response = requests.put(f"{BASE_URL}/categories/{self.category_id}", headers=headers, json=invalid_update)
        self.assertEqual(response.status_code, 400)

    def test_delete_category_by_id(self):
        """Test DELETE /categories/:id - Valid and Already Deleted Cases"""
        # Create a separate Category for deletion test
        headers = {'Content-Type': 'application/json'}
        category_data = {"title": "Delete Test Category", "description": "Category to delete"}
        response = requests.post(f"{BASE_URL}/categories", headers=headers, json=category_data)
        self.assertEqual(response.status_code, 201)
        delete_category_id = response.json()['id']

        # Valid deletion
        response = requests.delete(f"{BASE_URL}/categories/{delete_category_id}")
        self.assertEqual(response.status_code, 200)

        # Trying to delete the same ID again
        response = requests.delete(f"{BASE_URL}/categories/{delete_category_id}")
        self.assertEqual(response.status_code, 404)

    def test_todo_relationships(self):
        """Test POST, GET, and DELETE /categories/:id/todos - Valid and Invalid Cases"""
        headers = {'Content-Type': 'application/json'}
        # Create Relationship between Category and Todo
        relationship_data = {"id": self.todo_id}
        response = requests.post(f"{BASE_URL}/categories/{self.category_id}/todos", headers=headers, json=relationship_data)
        self.assertEqual(response.status_code, 201)

        # Retrieve Todos Linked to Category
        response = requests.get(f"{BASE_URL}/categories/{self.category_id}/todos", headers={'Accept': 'application/json'})
        self.assertEqual(response.status_code, 200)

        # Delete the Todo Relationship
        response = requests.delete(f"{BASE_URL}/categories/{self.category_id}/todos/{self.todo_id}")
        self.assertEqual(response.status_code, 200)

        # Attempt to Delete a Non-Existent Relationship
        response = requests.delete(f"{BASE_URL}/categories/{self.category_id}/todos/99999")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
