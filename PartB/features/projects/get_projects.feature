Feature: Retrieve all projects
  As a user of the project management system
  I want to retrieve all projects
  So that I can view them in JSON format

  Background:
    Given the Todo API is running

  Scenario: Successfully retrieve all projects in JSON format
    When I send a GET request to /projects
    Then I receive a response containing a list of all projects in JSON format

  Scenario: Retrieve incomplete projects with filter
    When I send a GET request to /projects with completed=false
    Then I receive a response containing all incomplete projects

  Scenario: Invalid filter for retrieving projects
    When I send a GET request to /projects with completed=invalid_value
    # Application error
    Then I received a 200 Status response instead of 400
