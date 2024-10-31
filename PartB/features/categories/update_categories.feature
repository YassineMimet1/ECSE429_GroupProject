Feature: Update a Category

  I want to update an existing category.

  Background:
    Given the Category API is running for Update Category

  Scenario: Successfully update a category
    When the user sends a PUT request to /categories/1 with "Updated Work" and "Updated work tasks"
    Then the response status for Update Category should be 200

  Scenario: Update a category with missing title
    When the user sends a PUT request to /categories/1 with no title and "Updated work tasks"
    Then the response status for Update Category should be 400

  Scenario: Update a non-existent category
    When the user sends a PUT request to /categories/999 with "Nonexistent Category" and "This category does not exist"
    Then the response status for Update Category should be 404