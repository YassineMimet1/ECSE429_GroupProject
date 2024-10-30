Feature: Create a new project
  As a user of the project management system
  I want to create a new project
  So that it can be tracked and managed

  Background:
    Given the Todo API is running

  Scenario: Successfully create a new project
    When I send a POST request to /projects with valid project data
    Then a new project is created with an ID returned in the response

  Scenario: Create project with missing optional fields
    When I send a POST request to /projects with missing optional fields
    Then the project is created with default values for the missing fields

  Scenario: Invalid project creation request
    When I send a POST request to /projects with invalid data
    Then I receive a 400 Bad Request response
