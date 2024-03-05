Feature: unique values Validations 
    Scenario: Unique Value 
        Given I have a CSV file
        And I have another CSV file
        When I compare for unique values in the CSV files
        Then the number of unique values should be the same
        