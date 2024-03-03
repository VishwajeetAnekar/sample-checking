Feature: Duplicate Keys Validation

  Scenario: Duplicate Keys Validation
    Given a csv file
    When duplicate keys are validated
    Then no duplicate rows or columns are found
