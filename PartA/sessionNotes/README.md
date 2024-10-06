# Session Notes

This folder contains the session notes taken during Charter Driven Session Based Exploratory Testing of the REST API Todo List Manager. Each session note documents the activities, observations, and findings from the testing sessions.

## Overview
- Each file corresponds to a single exploratory testing session.
- The notes are structured to cover the charter objectives, session findings, and any bugs or issues discovered during testing.

## Structure of Session Notes
Each session note file is organized as follows:

1. **Session Charter**:
   - Defines the focus and objectives of the session.
   - Example: "Explore the capabilities related to managing todos and identify any undocumented behaviors."

2. **Participants**:
   - Names, student IDs, and email addresses of team members who participated in the session.

3. **Session Findings**:
   - A bullet list summarizing what was learned during the session.
   - Example: "Learned that the `/todos` endpoint allows duplicate entries if no title is specified."

4. **List of Concerns**:
   - Any issues or potential instabilities identified.
   - Example: "The `/categories` endpoint does not validate input fields correctly."

5. **New Testing Ideas**:
   - Suggestions for additional test cases or areas to explore in future sessions.
   - Example: "Test how the system handles a large volume of concurrent `POST` requests to `/todos`."
