Feature: Update an existing project
  As a user of the project management system
  I want to update an existing project
  So that the project details reflect current information

  Background:
    Given a project exists with a specific ID

  Scenario: Successfully update a project
    When I send a PUT request to /projects/:id with updated data
    Then the project is updated successfully with the new data reflected

  Scenario: Update project description only
    When I send a PUT request to /projects/:id with only the description updated
    Then only the description is updated and other fields remain unchanged

  Scenario: Update project with invalid ID
    When I send a PUT request to /projects/:id with an invalid ID
    Then I receive a 404 Not Found response
