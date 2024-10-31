Feature: View Categories

  I want to view all existing categories.

  Background:
    Given the Category API is running for View Categories

  Scenario: Successfully view all categories
    When the user sends a GET request to /categories
    Then the response status for View Categories should be 200
    And the response should contain a list of categories in JSON format

  Scenario: View categories with no existing categories
    Given the database is cleared of all categories
    When the user sends a GET request to /categories
    Then the response status for View Categories should be 200
    And the response should contain an empty list
