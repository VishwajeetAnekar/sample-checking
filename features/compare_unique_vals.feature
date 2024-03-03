Feature: unique values Validations 
    Scenario: To Compare the 2 CSV files to find the unique values in the columns
        Given I have a CSV file
        And I have another CSV file
        When I compare for unique values in the CSV files
        Then the number of unique values should be the same
        