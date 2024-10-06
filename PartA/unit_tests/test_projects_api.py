import unittest
import requests
import json
from requests.exceptions import ConnectionError

BASE_URL = "http://localhost:4567"

class TestProjectsAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Ensure the service is running
        try:
            response = requests.get(BASE_URL)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Cannot connect to the service at {BASE_URL}: {e}")

        headers = {'Content-Type': 'application/json'}
        payload = {
            'title': 'Test Project',
            'completed': False,
            'active': True,
            'description': 'Project for testing'
        }
        response = requests.post(f"{BASE_URL}/projects", headers=headers, data=json.dumps(payload))
        if response.status_code == 201:
            try:
                data = response.json()
                cls.project_id = data.get('id')
            except json.JSONDecodeError:
                raise Exception("Failed to create project: Response is not valid JSON")
        else:
            raise Exception(f"Failed to create project: Status code {response.status_code}")

    @classmethod
    def tearDownClass(cls):
        # Delete the project created in setUpClass
        response = requests.delete(f"{BASE_URL}/projects/{cls.project_id}")

    def setUp(self):
        # Assign project_id
        self.project_id = self.__class__.project_id

    def test_get_projects_json(self):
        """Test GET /projects with JSON response"""
        headers = {'Accept': 'application/json'}
        response = requests.get(f"{BASE_URL}/projects", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.headers['Content-Type'])
        try:
            data = response.json()
            self.assertIn('projects', data)
        except json.JSONDecodeError:
            self.fail("Response is not valid JSON")

    def test_get_projects_xml(self):
        """Test GET /projects with XML response"""
        headers = {'Accept': 'application/xml'}
        response = requests.get(f"{BASE_URL}/projects", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/xml', response.headers['Content-Type'])
        # Check if response contains <projects> root element, indicating valid XML format
        self.assertTrue('<projects>' in response.text)

    def test_get_projects_with_filter(self):
        """Test GET /projects with query parameters"""
        headers = {'Accept': 'application/json'}
        params = {'completed': 'false', 'title': 'Office Work'}
        response = requests.get(f"{BASE_URL}/projects", headers=headers, params=params)
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.headers['Content-Type'])
        try:
            data = response.json()
            self.assertIn('projects', data)
            for project in data['projects']:
                self.assertEqual(project.get('completed'), 'false')
                self.assertEqual(project.get('title'), 'Office Work')
        except json.JSONDecodeError:
            self.fail("Response is not valid JSON")

    def test_head_projects(self):
        """Test HEAD /projects"""
        response = requests.head(f"{BASE_URL}/projects")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, '')

    def test_create_project_valid(self):
        """Test POST /projects with valid data"""
        headers = {'Content-Type': 'application/json'}
        payload = {
            'title': 'New Project',
            'completed': False,
            'active': True,
            'description': 'Project Description'
        }
        response = requests.post(f"{BASE_URL}/projects", headers=headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 201)
        self.assertIn('Location', response.headers)
        try:
            data = response.json()
            self.assertIn('id', data)
            project_id = data['id']
            # Clean up by deleting the created project
            requests.delete(f"{BASE_URL}/projects/{project_id}")
        except json.JSONDecodeError:
            self.fail("Response is not valid JSON")

    def test_create_project_invalid_data_types(self):
        """Test POST /projects with invalid data types"""
        headers = {'Content-Type': 'application/json'}
        payload = {
            'title': 12345,  # Title should be a string
            'completed': 'not_a_boolean',  # Should be a boolean
            'active': 'not_a_boolean',  # Should be a boolean
            'description': False  # Should be a string
        }
        response = requests.post(f"{BASE_URL}/projects", headers=headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 400)

    def test_create_project_with_extra_fields(self):
        """Test POST /projects with extra invalid fields"""
        headers = {'Content-Type': 'application/json'}
        payload = {
            'title': 'Extra Fields Project',
            'completed': False,
            'active': True,
            'description': 'Project with extra fields',
            'invalid_field': 'invalid_value'
        }
        response = requests.post(f"{BASE_URL}/projects", headers=headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 400)

    def test_create_project_malformed_json(self):
        """Test POST /projects with malformed JSON"""
        headers = {'Content-Type': 'application/json'}
        payload = '{"title": "Malformed JSON Project", "completed": false'  # Missing closing brace
        response = requests.post(f"{BASE_URL}/projects", headers=headers, data=payload)
        self.assertEqual(response.status_code, 400)

    def test_get_projects_unsupported_accept(self):
        """Test GET /projects with unsupported Accept header"""
        headers = {'Accept': 'application/unsupported'}
        response = requests.get(f"{BASE_URL}/projects", headers=headers)
        self.assertEqual(response.status_code, 406)  # Not Acceptable

    def test_get_project_by_id_json(self):
        """Test GET /projects/:id with JSON response"""
        headers = {'Accept': 'application/json'}
        response = requests.get(f"{BASE_URL}/projects/{self.project_id}", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.headers['Content-Type'])
        try:
            data = response.json()
            self.assertIn('projects', data)
            self.assertEqual(data['projects'][0]['id'], self.project_id)
        except json.JSONDecodeError:
            self.fail("Response is not valid JSON")

    def test_get_project_by_id_xml(self):
        """Test GET /projects/:id with XML response"""
        headers = {'Accept': 'application/xml'}
        response = requests.get(f"{BASE_URL}/projects/{self.project_id}", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/xml', response.headers['Content-Type'])
        # Check if response contains <projects> root element, indicating valid XML format
        self.assertTrue('<projects>' in response.text)

    def test_get_project_by_invalid_id(self):
        """Test GET /projects/:id with invalid id"""
        invalid_id = 'nonexistent'
        response = requests.get(f"{BASE_URL}/projects/{invalid_id}")
        self.assertEqual(response.status_code, 404)

    def test_get_project_by_invalid_id_format(self):
        """Test GET /projects/:id with invalid id format"""
        invalid_id = '!@#$%'
        response = requests.get(f"{BASE_URL}/projects/{invalid_id}")
        self.assertEqual(response.status_code, 404)

    def test_update_project(self):
        """Test PUT /projects/:id with valid data"""
        headers = {'Content-Type': 'application/json'}
        payload = {
            'description': 'Updated Description'
        }
        response = requests.put(f"{BASE_URL}/projects/{self.project_id}", headers=headers, data=json.dumps(payload))
        self.assertIn(response.status_code, [200, 204])
        # Verify update
        response = requests.get(f"{BASE_URL}/projects/{self.project_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        project = data['projects'][0]
        self.assertEqual(project['description'], 'Updated Description')

    def test_update_project_invalid(self):
        """Test PUT /projects/:id with invalid data"""
        headers = {'Content-Type': 'application/json'}
        payload = {
            'completed': 'invalid_boolean'
        }
        response = requests.put(f"{BASE_URL}/projects/{self.project_id}", headers=headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 400)

    def test_update_project_invalid_data_types(self):
        """Test PUT /projects/:id with invalid data types"""
        headers = {'Content-Type': 'application/json'}
        payload = {
            'title': 12345,  # Title should be a string
            'completed': 'not_a_boolean',  # Should be a boolean
        }
        response = requests.put(f"{BASE_URL}/projects/{self.project_id}", headers=headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 400)

    def test_update_project_invalid_id(self):
        """Test PUT /projects/:id with invalid id"""
        headers = {'Content-Type': 'application/json'}
        payload = {'description': 'Should Fail'}
        invalid_id = 'nonexistent'
        response = requests.put(f"{BASE_URL}/projects/{invalid_id}", headers=headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 404)

    def test_update_project_malformed_json(self):
        """Test PUT /projects/:id with malformed JSON"""
        headers = {'Content-Type': 'application/json'}
        payload = '{"description": "Malformed JSON'  # Missing closing brace
        response = requests.put(f"{BASE_URL}/projects/{self.project_id}", headers=headers, data=payload)
        self.assertEqual(response.status_code, 400)

    def test_delete_project(self):
        """Test DELETE /projects/:id"""
        # Create a project to delete
        headers = {'Content-Type': 'application/json'}
        payload = {
            'title': 'Project to Delete',
            'completed': False,
            'active': True,
            'description': 'This project will be deleted'
        }
        response = requests.post(f"{BASE_URL}/projects", headers=headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 201)
        data = response.json()
        project_id = data['id']
        # Delete the project
        response = requests.delete(f"{BASE_URL}/projects/{project_id}")
        self.assertIn(response.status_code, [200, 204])
        # Verify deletion
        response = requests.get(f"{BASE_URL}/projects/{project_id}")
        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistent_project(self):
        """Test DELETE /projects/:id with invalid id"""
        invalid_id = 'nonexistent'
        response = requests.delete(f"{BASE_URL}/projects/{invalid_id}")
        self.assertEqual(response.status_code, 404)

    def test_delete_project_with_empty_id(self):
        """Test DELETE /projects/ with empty id"""
        response = requests.delete(f"{BASE_URL}/projects/")
        self.assertIn(response.status_code, [400, 404])

    def test_delete_project_with_invalid_id_format(self):
        """Test DELETE /projects/:id with invalid id format"""
        invalid_id = '!@#$%'
        response = requests.delete(f"{BASE_URL}/projects/{invalid_id}")
        self.assertEqual(response.status_code, 404)

    def test_invalid_http_method_on_projects(self):
        """Test invalid HTTP method on /projects"""
        response = requests.patch(f"{BASE_URL}/projects")
        self.assertEqual(response.status_code, 405)

    def test_put_on_projects_without_id(self):
        """Test PUT /projects without providing an ID"""
        headers = {'Content-Type': 'application/json'}
        payload = {
            'title': 'Should Not Work'
        }
        response = requests.put(f"{BASE_URL}/projects", headers=headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 405)

    def test_link_task_to_project(self):
        """Test POST /projects/:id/tasks (link a task)"""
        # Create a task
        headers = {'Content-Type': 'application/json'}
        payload = {
            'title': 'Task to Link'
        }
        response = requests.post(f"{BASE_URL}/todos", headers=headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 201)
        data = response.json()
        task_id = data['id']
        # Link the task to the project
        payload = {'id': task_id}
        response = requests.post(f"{BASE_URL}/projects/{self.project_id}/tasks", headers=headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 201)
        # Verify linkage
        response = requests.get(f"{BASE_URL}/projects/{self.project_id}/tasks")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        tasks = data['todos']
        self.assertTrue(any(task['id'] == task_id for task in tasks))
        # Clean up
        requests.delete(f"{BASE_URL}/projects/{self.project_id}/tasks/{task_id}")
        requests.delete(f"{BASE_URL}/tasks/{task_id}")

    def test_link_invalid_task_to_project(self):
        """Test POST /projects/:id/tasks with invalid task id"""
        headers = {'Content-Type': 'application/json'}
        payload = {'id': 'nonexistent'}
        response = requests.post(f"{BASE_URL}/projects/{self.project_id}/tasks", headers=headers, data=json.dumps(payload))
        self.assertIn(response.status_code, [400, 404])

    def test_link_task_to_nonexistent_project(self):
        """Test POST /projects/:id/tasks to a nonexistent project"""
        headers = {'Content-Type': 'application/json'}
        payload = {'id': '1'}
        invalid_project_id = 'nonexistent'
        response = requests.post(f"{BASE_URL}/projects/{invalid_project_id}/tasks", headers=headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 404)

    def test_link_task_to_project_missing_id(self):
        """Test POST /projects/:id/tasks with missing 'id' in payload"""
        headers = {'Content-Type': 'application/json'}
        payload = {}  # Missing 'id'
        response = requests.post(f"{BASE_URL}/projects/{self.project_id}/tasks", headers=headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 400)

    def test_link_task_invalid_payload(self):
        """Test POST /projects/:id/tasks with invalid payload"""
        headers = {'Content-Type': 'application/json'}
        payload = {'invalid_field': 'value'}
        response = requests.post(f"{BASE_URL}/projects/{self.project_id}/tasks", headers=headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 400)

    def test_unlink_task_not_linked(self):
        """Test DELETE /projects/:id/tasks/:id for a task not linked to the project"""
        response = requests.delete(f"{BASE_URL}/projects/{self.project_id}/tasks/9999")  # Assuming 9999 is not linked
        self.assertEqual(response.status_code, 404)

    def test_get_project_categories(self):
        """Test GET /projects/:id/categories"""
        headers = {'Accept': 'application/json'}
        response = requests.get(f"{BASE_URL}/projects/{self.project_id}/categories", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.headers['Content-Type'])
        try:
            data = response.json()
            self.assertIn('categories', data)
        except json.JSONDecodeError:
            self.fail("Response is not valid JSON")

    def test_get_project_categories_invalid_accept(self):
        """Test GET /projects/:id/categories with invalid Accept header"""
        headers = {'Accept': 'application/unsupported'}
        response = requests.get(f"{BASE_URL}/projects/{self.project_id}/categories", headers=headers)
        self.assertEqual(response.status_code, 406)

    def test_head_project_categories(self):
        """Test HEAD /projects/:id/categories"""
        response = requests.head(f"{BASE_URL}/projects/{self.project_id}/categories")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, '')

    def test_head_project_by_invalid_id(self):
        """Test HEAD /projects/:id with invalid id"""
        invalid_id = 'nonexistent'
        response = requests.head(f"{BASE_URL}/projects/{invalid_id}")
        self.assertEqual(response.status_code, 404)

    def test_category_relationship(self):
        """Test POST and DELETE /projects/:id/categories/:id"""
        headers = {'Content-Type': 'application/json'}
        payload = {'title': 'Test Category'}
        # Create a category
        response = requests.post(f"{BASE_URL}/categories", headers=headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 201)
        data = response.json()
        category_id = data['id']
        # Link the category to the project
        payload = {'id': category_id}
        response = requests.post(f"{BASE_URL}/projects/{self.project_id}/categories", headers=headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 201)
        # Verify linkage
        response = requests.get(f"{BASE_URL}/projects/{self.project_id}/categories")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        categories = data['categories']
        self.assertTrue(any(category['id'] == category_id for category in categories))
        # Unlink the category
        response = requests.delete(f"{BASE_URL}/projects/{self.project_id}/categories/{category_id}")
        self.assertIn(response.status_code, [200, 204])
        # Verify unlinking
        response = requests.get(f"{BASE_URL}/projects/{self.project_id}/categories")
        data = response.json()
        categories = data['categories']
        self.assertFalse(any(category['id'] == category_id for category in categories))
        # Clean up
        requests.delete(f"{BASE_URL}/categories/{category_id}")

    def test_category_relationship_invalid(self):
        """Test POST /projects/:id/categories with invalid category id"""
        headers = {'Content-Type': 'application/json'}
        payload = {'id': 'nonexistent'}
        response = requests.post(f"{BASE_URL}/projects/{self.project_id}/categories", headers=headers, data=json.dumps(payload))
        self.assertIn(response.status_code, [400, 404])

if __name__ == '__main__':
    unittest.main()
