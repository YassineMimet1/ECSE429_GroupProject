Feature: Delete a project
  As a user of the project management system
  I want to delete a project
  So that it no longer exists in the system

  Background:
    Given a project exists with a specific ID

  Scenario: Successfully delete a project
    When I send a DELETE request to /projects/:id
    Then the project is deleted successfully

  Scenario: Delete project with dependencies
    When I send a DELETE request to /projects/:id and the project has dependencies
    Then the project is deleted and the dependencies are either removed or unlinked

  Scenario: Delete project with invalid ID
    When I send a DELETE request to /projects/:id with an invalid ID
    Then I receive a 404 Not Found response
