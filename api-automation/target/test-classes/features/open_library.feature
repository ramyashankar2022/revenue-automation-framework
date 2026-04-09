Feature: Open Library Author API
  As an API consumer
  I want to fetch author details from the Open Library API
  So that I can verify the author information is correct
 
  Scenario: Fetch and assert author details for OL1A
    Given I send a GET request to "https://openlibrary.org/authors/OL1A.json"
    Then the response status code should be 200
    And the "personal_name" field should be "Sachi Rautroy"
    And the "alternate_names" array should contain "Yugashrashta Sachi Routray"