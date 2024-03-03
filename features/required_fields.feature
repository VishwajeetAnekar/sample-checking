Feature: Required Fields Validation

  Scenario: Required Fields Validation
    Given a configuration file
    And a csv file
    When required fields are validated
    Then all required fields have values
    # Then the validation result is saved to a CSV file
