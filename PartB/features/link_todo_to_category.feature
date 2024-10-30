Feature: Link Todo to Category

  Background:
    Given the Todo API is running for Linking Todos
    And a category with ID <category_id> exists for linking todo to a category
    And a todo with ID <todo_id> exists for linking todo to a category

  # Normal Flow
  Scenario: Successfully link a todo to a category
    When the user sends a POST request to /categories/<category_id>/todos with <todo_id>
    Then the response status for Linking Todos should be 201

  # Alternate Flow
  Scenario: Linking a todo to a non-existent category
    When the user sends a POST request to /categories/99999/todos with <todo_id>
    Then the response status for Linking Todos should be 404

  # Error Flow
  Scenario: Linking a non-existent todo to a category
    When the user sends a POST request to /categories/<category_id>/todos with 99999
    Then the response status for Linking Todos should be 404
