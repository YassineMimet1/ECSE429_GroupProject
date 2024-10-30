Feature: Create a Todo
  
  I want to create a Todo.
  
  Background:
    Given the Todo API is running

    # Normal flow
  Scenario: Successfully create a todo
    When the user sends a POST request to /todos with "Grocery Shopping" and "Buy fruits and vegetables"
    Then the response status should be 201

    # Alternate flow
  Scenario: Create a todo without a description
    When the user sends a POST request to /todos with "Workout" and no description
    Then the response status should be 201

    # Error flow
  Scenario: Malformed JSON request
    When the user sends a POST request to /todos with malformed JSON
    Then the response status should be 400
