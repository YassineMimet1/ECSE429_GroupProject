Feature: Search Categories by Title or Description

  I want to search categories by title or description keywords to quickly find relevant categories.

  Background:
    Given the Category API is running for Search Categories

  Scenario: Successfully search categories by title keyword
    When the user sends a GET request to /categories with the query parameter "title=Work"
    Then the response status for Search Categories should be 200
    And the response should contain categories with "title" matching "Work"

  Scenario: Successfully search categories by description keyword
    When the user sends a GET request to /categories with the query parameter "description=personal"
    Then the response status for Search Categories should be 200
    And the response should contain an empty list

  Scenario: Search categories with no matching results
    When the user sends a GET request to /categories with the query parameter "title=NonexistentCategory"
    Then the response status for Search Categories should be 200
    And the response should contain an empty list

  Scenario: Search categories with malformed query parameter
    When the user sends a GET request to /categories with an invalid query parameter
    Then the response status for Search Categories should be 200
    And the response should include an error message for malformed query
