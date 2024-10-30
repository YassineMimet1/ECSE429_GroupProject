Feature: Delete a Todo

  Background:
    Given the Todo API is running for Delete Todo
    And a todo with ID <todo_id> exists to delete

  # Normal Flow
  Scenario: Successfully delete a todo
    When the user sends a DELETE request to /todos/<todo_id>
    Then the response status for Delete Todo should be 200

  # Alternate Flow
  Scenario: Delete a todo linked to a category
    Given the todo with ID <todo_id> is linked to a category
    When the user sends a DELETE request to /todos/<todo_id>
    Then the response status for Delete Todo should be 200

  # Error Flow
  Scenario: Deleting a non-existent todo
    When the user sends a DELETE request to /todos/99999
    Then the response status for Delete Todo should be 404
