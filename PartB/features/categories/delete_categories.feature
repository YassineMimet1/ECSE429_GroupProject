Feature: Delete a Category

  I want to delete a Category.

  Background:
    Given the Category API is running for Delete Category
    And a category with ID "1" exists

  Scenario: Successfully delete a category
    When the user sends a DELETE request to /categories/1
    Then the response status for Delete Category should be 200

  Scenario: Delete a non-existent category
    When the user sends a DELETE request to /categories/999
    Then the response status for Delete Category should be 404

  Scenario: Unauthorized deletion attempt
    When the user sends an unauthorized DELETE request to /categories/1
    Then the response status for Delete Category should be 401
    And the response should indicate an authorization error


