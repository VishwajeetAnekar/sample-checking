Feature: Whitespace Validation
    Scenario: Whitespace Validation in the CSV file
        Given a csv file
        When CSV file is validated
        Then the validation should be successful
