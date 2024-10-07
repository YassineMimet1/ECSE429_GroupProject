#!/bin/bash

# Base URL for the Category API
BASE_URL="http://localhost:4567"

# Global variable to hold the created Category ID
created_category_id=""

# Function to test all basic `categories` operations
test_categories() {
    echo "Testing GET /categories (All categories in JSON format)"
    response=$(curl -s -X GET "${BASE_URL}/categories" -H "Accept: application/json")
    echo "Response: $response"
    echo -e "\n"

    echo "Testing HEAD /categories (Headers only for all categories)"
    response=$(curl -s -I -X HEAD "${BASE_URL}/categories")
    echo "Response: $response"
    echo -e "\n"

    echo "Testing POST /categories (Create a new category)"
    create_category_response=$(curl -s -X POST "${BASE_URL}/categories" -H "Content-Type: application/json" -d '{"title": "New Category","description": "Category for testing"}')
    echo "Response: $create_category_response"
    created_category_id=$(echo $create_category_response | grep -o '"id":"[^"]*' | grep -o '[^"]*$')
    echo "Created Category ID: $created_category_id"
    echo -e "\n"
}

# Function to test CRUD operations for the created category ID
test_category_crud() {
    echo "Testing GET /categories/:id (Retrieve a specific category by ID)"
    response=$(curl -s -X GET "${BASE_URL}/categories/${created_category_id}" -H "Accept: application/json")
    echo "Response: $response"
    echo -e "\n"

    echo "Testing HEAD /categories/:id (Retrieve headers for a specific category)"
    response=$(curl -s -I -X HEAD "${BASE_URL}/categories/${created_category_id}")
    echo "Response: $response"
    echo -e "\n"

    echo "Testing POST /categories/:id (Amend a specific category using POST)"
    response=$(curl -s -X POST "${BASE_URL}/categories/${created_category_id}" -H "Content-Type: application/json" -d '{"title": "Updated Category","description": "Updated description"}')
    echo "Response: $response"
    echo -e "\n"

    echo "Testing PUT /categories/:id (Amend a specific category using PUT)"
    response=$(curl -s -X PUT "${BASE_URL}/categories/${created_category_id}" -H "Content-Type: application/json" -d '{"title": "Updated Category x2","description": "Updated description x2"}')
    echo "Response: $response"
    echo -e "\n"

    echo "Testing DELETE /categories/:id (Delete the specific category)"
    response=$(curl -s -X DELETE "${BASE_URL}/categories/${created_category_id}")
    echo "Response: $response"
    echo -e "\n"

    echo "Testing GET /categories/:id (After deletion, should return 404)"
    response=$(curl -s -X GET "${BASE_URL}/categories/${created_category_id}" -H "Accept: application/json")
    echo "Response: $response"
    echo -e "\n"
}

# Function to test operations related to todos for a category
test_category_todos() {
    echo "Testing POST /todos (Create a new todo)"
    todo_response=$(curl -s -X POST "${BASE_URL}/todos" -H "Content-Type: application/json" -d '{"title": "Test Todo", "description": "Todo for testing categories"}')
    echo "Response: $todo_response"
    todo_id=$(echo $todo_response | grep -o '"id":"[^"]*' | grep -o '[^"]*$')
    echo "Created Todo ID: $todo_id"
    echo -e "\n"

    echo "Testing POST /categories/:id/todos (Create a relationship between category and todo)"
    response=$(curl -s -X POST "${BASE_URL}/categories/${created_category_id}/todos" -H "Content-Type: application/json" -d '{"id": "'$todo_id'"}')
    echo "Response: $response"
    echo -e "\n"

    echo "Testing GET /categories/:id/todos (Retrieve todos related to the category)"
    response=$(curl -s -X GET "${BASE_URL}/categories/${created_category_id}/todos" -H "Accept: application/json")
    echo "Response: $response"
    echo -e "\n"

    echo "Testing DELETE /categories/:id/todos/:id (Delete the todo relationship for the category)"
    response=$(curl -s -X DELETE "${BASE_URL}/categories/${created_category_id}/todos/${todo_id}")
    echo "Response: $response"
    echo -e "\n"

    echo "Testing GET /categories/:id/todos (After deletion, todos should be empty)"
    response=$(curl -s -X GET "${BASE_URL}/categories/${created_category_id}/todos" -H "Accept: application/json")
    echo "Response: $response"
    echo -e "\n"
}

# Function to test invalid input scenarios for categories
test_invalid_category_input() {
    echo "Testing POST /categories (Invalid data format)"
    response=$(curl -s -X POST "${BASE_URL}/categories" -H "Content-Type: application/json" -d '{"title": 12345, "description": "Invalid title format"}')
    echo "Response: $response"
    echo -e "\n"
}

# Function to test undocumented methods on endpoints
test_undocumented_methods() {
    echo "Testing PATCH /categories/:id (Attempting to update a field with PATCH)"
    response=$(curl -s -X PATCH "${BASE_URL}/categories/${created_category_id}" -H "Content-Type: application/json" -d '{"title": "Updated Title with PATCH"}')
    echo "Response: $response"
    echo -e "\n"
}

# Run all test cases
test_categories
test_category_crud
test_category_todos
test_invalid_category_input
test_undocumented_methods
