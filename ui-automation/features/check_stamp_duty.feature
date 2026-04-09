Feature: Motor Vehicle Stamp Duty Calculator
  As a user
  I want to check motor vehicle stamp duty online
  So that I can know the payable amount
 
  Scenario: Calculate stamp duty
    Given I am on the Service NSW motor vehicle stamp duty page
    When I click the "Check Online" button
    Then I should be redirected to the Revenue NSW calculator page
    When I select "Yes" for NSW residency
    And I enter a vehicle amount of 50000
    And I click the "Calculate" button
    Then I should see the stamp duty result popup
    And the popup title should be "Calculation"
    And the popup heading should be "Motor vehicle registration"
    And the popup details table should show "Is this registration for a passenger vehicle?" as "Yes"
    And the popup details table should show the correct purchase price
    And the popup details table should show a valid duty payable amount
    And the popup should contain the note "All amounts are in Australian dollars."
    And the popup should have a "contact us" link
    And the popup should have a "Close" button
    And close the browser