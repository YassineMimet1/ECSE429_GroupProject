Feature: Update a Todo

    I want to update a Todo.

  Background:
    Given the Todo API is running for Update Todo
    And a todo with ID <todo_id> exists

  # Normal Flow
  Scenario: Successfully update a todo
    When the user sends a PUT request to /todos/<todo_id> with "New Title" and "New Description"
    Then the response status for Update Todo should be 200

  # Alternate Flow
  Scenario: Update a todo with partial data
    When the user sends a PUT request to /todos/<todo_id> with only a new title "Partial Title"
    Then the response status for Update Todo should be 200

  # Error Flow
  Scenario: Update a non-existent todo
    When the user sends a PUT request to /todos/99999 with "Non-existent" and "This todo does not exist"
    Then the response status for Update Todo should be 404
