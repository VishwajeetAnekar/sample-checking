Feature: Expected Values Validation

  Scenario: Expected Values Validation
    Given a configuration file
    And a csv file
    When expected values are validated
    Then all values in the specified columns are equal to expected values
