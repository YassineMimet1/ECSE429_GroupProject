#!/bin/bash

# Base URL for API
BASE_URL="http://localhost:4567"

test_projects() {
    echo "Testing GET /projects (all projects, JSON format)"
    curl -s -X GET "${BASE_URL}/projects" -H "Accept: application/json"

    echo -e "\nTesting GET /projects with filter (completed=false)"
    curl -s -X GET "${BASE_URL}/projects?completed=false&title=Office%20Work" -H "Accept: application/json"

    echo -e "\nTesting HEAD /projects (headers only)"
    curl -s -I -X HEAD "${BASE_URL}/projects"
}

test_project_crud() {
    echo -e "\n\nTesting POST /projects (Create a project)"
    create_response=$(curl -s -X POST "${BASE_URL}/projects" -H "Content-Type: application/json" -d '{"title": "New Project", "completed": false, "active": true, "description": "Project Description"}')
    echo $create_response
    project_id=$(echo $create_response | grep -o '"id":"[^"]*' | grep -o '[^"]*$')

    echo -e "\nTesting GET /projects/:id (Retrieve the project)"
    curl -s -X GET "${BASE_URL}/projects/${project_id}"

    echo -e "\nTesting PUT /projects/:id (Update the project)"
    curl -s -X PUT "${BASE_URL}/projects/${project_id}" -H "Content-Type: application/json" -d '{"description": "Updated Description"}'

    echo -e "\nTesting DELETE /projects/:id (Delete the project)"
    curl -s -X DELETE "${BASE_URL}/projects/${project_id}"

    echo -e "\nTesting GET /projects/:id (After deletion 'Should fail')"
    curl -s -X GET "${BASE_URL}/projects/${project_id}"
}

test_project_tasks() {
    project_id=$1

    echo -e "\n\nTesting GET /projects/:id/tasks (Retrieve tasks related to the project)"
    curl -s -X GET "${BASE_URL}/projects/${project_id}/tasks"

    echo -e "\nTesting POST /projects/:id/tasks (Link a task)"
    curl -s -X POST "${BASE_URL}/projects/${project_id}/tasks" -H "Content-Type: application/json" -d '{"id":"1"}'

    echo -e "\nTesting DELETE /projects/:id/tasks/:id (Unlink a task)"
    curl -s -X DELETE "${BASE_URL}/projects/${project_id}/tasks/1"
}

test_project_categories() {
    project_id=$1

    echo -e "\n\nTesting GET /projects/:id/categories (Retrieve categories related to the project)"
    curl -s -X GET "${BASE_URL}/projects/${project_id}/categories" -H "Accept: application/json"

    echo -e "\nTesting HEAD /projects/:id/categories (Headers for categories related to the project)"
    curl -s -I -X HEAD "${BASE_URL}/projects/${project_id}/categories"
}

test_category_relationship() {
    project_id=$1
    category_id=$2

    echo -e "\nTesting POST /projects/:id/categories (Create a category relationship for the project)"
    curl -s -X POST "${BASE_URL}/projects/${project_id}/categories" -H "Content-Type: application/json" -d '{"id":"'$category_id'"}'

    echo -e "\n\nTesting GET /projects/:id/categories (Retrieve categories related to the project after adding a category)"
    curl -s -X GET "${BASE_URL}/projects/${project_id}/categories" -H "Accept: application/json"

    echo -e "\nTesting DELETE /projects/:id/categories/:id (Delete a category relationship for the project)"
    curl -s -X DELETE "${BASE_URL}/projects/${project_id}/categories/$category_id"

    echo -e "\n\nTesting GET /projects/:id/categories (Retrieve categories related to the project after deleting the category)"
    curl -s -X GET "${BASE_URL}/projects/${project_id}/categories" -H "Accept: application/json"
}

test_projects
test_project_crud

test_project_tasks "1"

test_project_categories "1"
test_category_relationship "1" "2"
