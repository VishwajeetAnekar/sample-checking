Feature: Compare CSV files
    Scenario: To Compare the 2 CSV files to find the count of columns
        Given I have a CSV file
        And I have another CSV file
        When I compare the CSV files
        Then the number of columns should be the same

 