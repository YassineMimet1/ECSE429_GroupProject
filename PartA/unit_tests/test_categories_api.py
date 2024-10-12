import unittest
import requests
import json

BASE_URL = "http://localhost:4567"

class TestCategoriesAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up by creating a category and a todo for testing relationships"""
        # Ensure the API is running
        try:
            response = requests.get(BASE_URL)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Cannot connect to the service at {BASE_URL}: {e}")

        # Create a category for testing
        headers = {'Content-Type': 'application/json'}
        category_data = {"title": "Test Category", "description": "Category for testing"}
        response = requests.post(f"{BASE_URL}/categories", headers=headers, json=category_data)
        if response.status_code == 201:
            cls.category_id = response.json().get('id')
        else:
            raise Exception("Failed to create category for test setup")

        # Create a todo for testing relationships
        todo_data = {"title": "Test Todo", "description": "Todo for testing relationships"}
        response = requests.post(f"{BASE_URL}/todos", headers=headers, json=todo_data)
        if response.status_code == 201:
            cls.todo_id = response.json().get('id')
        else:
            raise Exception("Failed to create todo for test setup")

    @classmethod
    def tearDownClass(cls):
        """Clean up by deleting the category and todo created for tests"""
        requests.delete(f"{BASE_URL}/categories/{cls.category_id}")
        requests.delete(f"{BASE_URL}/todos/{cls.todo_id}")

    def setUp(self):
        """Set up for individual test cases"""
        self.category_id = self.__class__.category_id
        self.todo_id = self.__class__.todo_id

    def test_get_categories(self):
        """Test GET /categories - Fetch all categories"""
        response = requests.get(f"{BASE_URL}/categories")
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.headers['Content-Type'])

    def test_head_categories(self):
        """Test HEAD /categories - Fetch headers for all categories"""
        response = requests.head(f"{BASE_URL}/categories")
        self.assertEqual(response.status_code, 200)

    def test_post_category(self):
        """Test POST /categories - Create a new category"""
        headers = {'Content-Type': 'application/json'}
        category_data = {"title": "New Test Category", "description": "Another test category"}
        response = requests.post(f"{BASE_URL}/categories", headers=headers, json=category_data)
        self.assertEqual(response.status_code, 201)

    def test_post_category_invalid(self):
        """Test POST /categories - Invalid and malformed JSON"""
        headers = {'Content-Type': 'application/json'}
        
        # Malformed JSON
        malformed_json = '{"title": "Invalid Category", "description":'
        response = requests.post(f"{BASE_URL}/categories", headers=headers, data=malformed_json)
        self.assertIn(response.status_code, [400, 200], msg="Expected 400 Bad Request or 200 OK for malformed JSON")
        print(f"Malformed JSON response: {response.text}")

        # Invalid JSON types
        invalid_json = {"title": 12345, "description": False}
        response = requests.post(f"{BASE_URL}/categories", headers=headers, json=invalid_json)
        self.assertIn(response.status_code, [400, 201], msg="Expected 400 Bad Request or 201 Created for invalid JSON types")
        print(f"Invalid JSON types response: {response.text}")

        # Invalid XML 
        headers_xml = {'Content-Type': 'application/xml'}
        malformed_xml = '<category><title>Invalid XML</title><description>'  # Missing closing tag for description
        response = requests.post(f"{BASE_URL}/categories", headers=headers_xml, data=malformed_xml)
        self.assertEqual(response.status_code, 400, msg="Expected 400 Bad Request for malformed XML")
        print(f"Malformed XML response: {response.text}")


    def test_get_category_by_id(self):
        """Test GET /categories/:id - Fetch a specific category by ID"""
        response = requests.get(f"{BASE_URL}/categories/{self.category_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.headers['Content-Type'])

    def test_head_category_by_id(self):
        """Test HEAD /categories/:id - Fetch headers for a specific category"""
        response = requests.head(f"{BASE_URL}/categories/{self.category_id}")
        self.assertEqual(response.status_code, 200)

    def test_post_category_amend(self):
        """Test POST /categories/:id - Amend a specific category"""
        headers = {'Content-Type': 'application/json'}
        update_data = {"title": "Updated Test Category", "description": "Updated description"}
        response = requests.post(f"{BASE_URL}/categories/{self.category_id}", headers=headers, json=update_data)
        self.assertEqual(response.status_code, 200)

    def test_put_category_amend(self):
        """Test PUT /categories/:id - Replace a specific category"""
        headers = {'Content-Type': 'application/json'}
        update_data = {"title": "Replaced Test Category", "description": "Replaced description"}
        response = requests.put(f"{BASE_URL}/categories/{self.category_id}", headers=headers, json=update_data)
        self.assertEqual(response.status_code, 200)

    def test_delete_category(self):
        """Test DELETE /categories/:id - Delete a specific category"""
        headers = {'Content-Type': 'application/json'}
        # Create a separate category to delete
        category_data = {"title": "Delete Test Category", "description": "To be deleted"}
        response = requests.post(f"{BASE_URL}/categories", headers=headers, json=category_data)
        self.assertEqual(response.status_code, 201)
        category_id = response.json().get('id')

        # Delete the newly created category
        response = requests.delete(f"{BASE_URL}/categories/{category_id}")
        self.assertEqual(response.status_code, 200)

        # Try to delete it again (should fail with 404)
        response = requests.delete(f"{BASE_URL}/categories/{category_id}")
        self.assertEqual(response.status_code, 404)

    def test_category_todos_relationship(self):
        """Test POST, GET, DELETE relationships between categories and todos"""
        headers = {'Content-Type': 'application/json'}

        # Create relationship between category and todo
        response = requests.post(f"{BASE_URL}/categories/{self.category_id}/todos", headers=headers, json={"id": self.todo_id})
        self.assertEqual(response.status_code, 201)

        # Fetch todos related to the category
        response = requests.get(f"{BASE_URL}/categories/{self.category_id}/todos")
        self.assertEqual(response.status_code, 200)

        # Delete the relationship between category and todo
        response = requests.delete(f"{BASE_URL}/categories/{self.category_id}/todos/{self.todo_id}")
        self.assertEqual(response.status_code, 200)

        # Try to delete a non-existent relationship
        response = requests.delete(f"{BASE_URL}/categories/{self.category_id}/todos/{self.todo_id}")
        self.assertEqual(response.status_code, 404)

    def test_category_projects_relationship(self):
        """Test POST, GET, DELETE relationships between categories and projects"""
        headers = {'Content-Type': 'application/json'}

        # Create a project to link to category
        project_data = {"title": "Test Project", "description": "Project for category relationship"}
        response = requests.post(f"{BASE_URL}/projects", headers=headers, json=project_data)
        self.assertEqual(response.status_code, 201)
        project_id = response.json().get('id')

        # Create relationship between category and project
        response = requests.post(f"{BASE_URL}/categories/{self.category_id}/projects", headers=headers, json={"id": project_id})
        self.assertEqual(response.status_code, 201)

        # Fetch projects related to the category
        response = requests.get(f"{BASE_URL}/categories/{self.category_id}/projects")
        self.assertEqual(response.status_code, 200)

        # Delete the relationship between category and project
        response = requests.delete(f"{BASE_URL}/categories/{self.category_id}/projects/{project_id}")
        self.assertEqual(response.status_code, 200)

        # Try to delete a non-existent relationship
        response = requests.delete(f"{BASE_URL}/categories/{self.category_id}/projects/{project_id}")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
