#!/bin/bash

# Base URL for the Todo API
BASE_URL="http://localhost:4567"

# Global variable to hold the created Todo ID
created_todo_id=""

# Function to test all basic `todos` operations
test_todos() {
    echo "Testing GET /todos (All todos in JSON format)"
    response=$(curl -s -X GET "${BASE_URL}/todos" -H "Accept: application/json")
    echo "Response: $response"
    echo -e "\n"

    echo "Testing HEAD /todos (Headers only for all todos)"
    response=$(curl -s -I -X HEAD "${BASE_URL}/todos")
    echo "Response: $response"
    echo -e "\n"

    echo "Testing POST /todos (Create a new todo)"
    create_todo_response=$(curl -s -X POST "${BASE_URL}/todos" -H "Content-Type: application/json" -d '{"title": "Exploratory Testing Todo","doneStatus": false,"description": "todo to test"}')
    echo "Response: $create_todo_response"
    created_todo_id=$(echo $create_todo_response | grep -o '"id":"[^"]*' | grep -o '[^"]*$')
    echo "Created Todo ID: $created_todo_id"
    echo -e "\n"
}

# Function to test CRUD operations for the created todo ID
test_todo_crud() {
    echo "Testing GET /todos/:id (Retrieve a specific todo by ID)"
    response=$(curl -s -X GET "${BASE_URL}/todos/${created_todo_id}" -H "Accept: application/json")
    echo "Response: $response"
    echo -e "\n"

    echo "Testing HEAD /todos/:id (Retrieve headers for a specific todo)"
    response=$(curl -s -I -X HEAD "${BASE_URL}/todos/${created_todo_id}")
    echo "Response: $response"
    echo -e "\n"

    echo "Testing POST /todos/:id (Amend a specific todo using POST)"
    response=$(curl -s -X POST "${BASE_URL}/todos/${created_todo_id}" -H "Content-Type: application/json" -d '{"title": "Updated Exploratory Testing Todo","description": "Updated description for the todo item"}')
    echo "Response: $response"
    echo -e "\n"

    echo "Testing PUT /todos/:id (Amend a specific todo using PUT)"
    response=$(curl -s -X PUT "${BASE_URL}/todos/${created_todo_id}" -H "Content-Type: application/json" -d '{"title": "Updated Exploratory Testing Todo x2","description": "Updated description for the todo item x2"}')
    echo "Response: $response"
    echo -e "\n"

    echo "Testing DELETE /todos/:id (Delete the specific todo)"
    response=$(curl -s -X DELETE "${BASE_URL}/todos/${created_todo_id}")
    echo "Response: $response"
    echo -e "\n"

    echo "Testing GET /todos/:id (After deletion, should return 404)"
    response=$(curl -s -X GET "${BASE_URL}/todos/${created_todo_id}" -H "Accept: application/json")
    echo "Response: $response"
    echo -e "\n"
}

# Function to test operations related to categories for a todo
test_todo_categories() {
    echo "Testing POST /categories (Create a new category)"
    category_response=$(curl -s -X POST "${BASE_URL}/categories" -H "Content-Type: application/json" -d '{"title": "Urgent","description": "Tasks that need immediate attention"}')
    echo "Response: $category_response"
    category_id=$(echo $category_response | grep -o '"id":"[^"]*' | grep -o '[^"]*$')
    echo "Created Category ID: $category_id"
    echo -e "\n"

    echo "Testing POST /todos/:id/categories (Create a relationship with a category)"
    response=$(curl -s -X POST "${BASE_URL}/todos/${created_todo_id}/categories" -H "Content-Type: application/json" -d '{"id": "'$category_id'"}')
    echo "Response: $response"
    echo -e "\n"

    echo "Testing GET /todos/:id/categories (Retrieve categories related to the todo)"
    response=$(curl -s -X GET "${BASE_URL}/todos/${created_todo_id}/categories" -H "Accept: application/json")
    echo "Response: $response"
    echo -e "\n"

    echo "Testing HEAD /todos/:id/categories (Retrieve headers for categories related to the todo)"
    response=$(curl -s -I -X HEAD "${BASE_URL}/todos/${created_todo_id}/categories")
    echo "Response: $response"
    echo -e "\n"

    echo "Testing DELETE /todos/:id/categories/:id (Delete the category relationship for the todo)"
    response=$(curl -s -X DELETE "${BASE_URL}/todos/${created_todo_id}/categories/${category_id}")
    echo "Response: $response"
    echo -e "\n"

    echo "Testing GET /todos/:id/categories (After deletion, categories should be empty)"
    response=$(curl -s -X GET "${BASE_URL}/todos/${created_todo_id}/categories" -H "Accept: application/json")
    echo "Response: $response"
    echo -e "\n"
}

# Function to test invalid input scenarios for todos
test_invalid_todo_input() {
    echo "Testing POST /todos (Invalid data type for doneStatus)"
    response=$(curl -s -X POST "${BASE_URL}/todos" -H "Content-Type: application/json" -d '{"title": "Invalid Todo", "doneStatus": "notABoolean", "description": "Invalid boolean for doneStatus"}')
    echo "Response: $response"
    echo -e "\n"

    echo "Testing POST /todos/:id (Using POST to an unsupported endpoint)"
    response=$(curl -s -X POST "${BASE_URL}/todos/9999" -H "Content-Type: application/json" -d '{"title": "Invalid POST"}')
    echo "Response: $response"
    echo -e "\n"
}

# Function to test undocumented methods on endpoints
test_undocumented_methods() {
    echo "Testing PATCH /todos/:id (Attempting to update a field with PATCH)"
    response=$(curl -s -X PATCH "${BASE_URL}/todos/${created_todo_id}" -H "Content-Type: application/json" -d '{"title": "Updated Title with PATCH"}')
    echo "Response: $response"
    echo -e "\n"
}

# Run all test cases
test_todos
test_todo_crud
test_todo_categories
test_invalid_todo_input
test_undocumented_methods
