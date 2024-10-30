Feature: Retrieve Todos

    I want to retrieve all Todos.

  Background:
    Given the Todo API is running for Retrieve Todos
    And multiple todos exist

  # Normal Flow
  Scenario: Retrieve all todos in JSON format
    When the user sends a GET request to /todos with Accept header "application/json"
    Then the response status for Retrieve Todos should be 200

  # Alternate Flow
  Scenario: Retrieve all todos in XML format
    When the user sends a GET request to /todos with Accept header "application/xml"
    Then the response status for Retrieve Todos should be 200

  # Error Flow
  Scenario: Invalid endpoint for todos
    When the user sends a GET request to /invalidEndpoint
    Then the response status for Retrieve Todos should be 404
