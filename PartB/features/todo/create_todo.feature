Feature: Create a Todo

  I want to create a Todo.

  Background:
    Given the Todo API is running for Create Todo

  Scenario: Successfully create a todo
    When the user sends a POST request to /todos with "Grocery Shopping" and "Buy fruits and vegetables"
    Then the response status for Create Todo should be 201

  Scenario: Create a todo without a description
    When the user sends a POST request to /todos with "Workout" and no description
    Then the response status for Create Todo should be 201

  Scenario: Malformed JSON request
    When the user sends a POST request to /todos with malformed JSON
    Then the response status for Create Todo should be 400
