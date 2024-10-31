Feature: Create a Category

  I want to create a Category.

  Background:
    Given the Category API is running for Create Category

  Scenario: Successfully create a category
    When the user sends a POST request to /categories with "Work" and "Work-related tasks"
    Then the response status for Create Category should be 201

  Scenario: Create a category without a description
    When the user sends a POST request to /categories with "Personal" and no description
    Then the response status for Create Category should be 201

  Scenario: Malformed JSON request
    When the user sends a POST request to /categories with malformed JSON
    Then the response status for Create Category should be 400
