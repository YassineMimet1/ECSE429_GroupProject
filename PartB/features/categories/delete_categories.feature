Feature: Delete a Category

  I want to delete a Category.

  Background:
    Given the Category API is running for Delete Category

  Scenario: Successfully delete a category
    When the user sends a DELETE request to /categories/1
    Then the response status for Delete Category should be 200

  Scenario: Delete a non-existent category
    When the user sends a DELETE request to /categories/999
    Then the response status for Delete Category should be 404
