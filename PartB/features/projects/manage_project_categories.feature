Feature: Manage project categories
  As a user of the project management system
  I want to manage categories related to a project
  So that I can organize projects better

  Background:
    Given a project exists with categories

  Scenario: Successfully retrieve project categories
    When I send a GET request to /projects/:id/categories
    Then I receive a list of categories related to the project

  Scenario: Add a category to a project
    When I send a POST request to /projects/:id/categories with valid category data
    Then the category is successfully added to the project

  Scenario: Invalid category ID while adding category
    When I send a POST request to /projects/:id/categories with an invalid category ID
    Then I receive a 404 Bad Request response
