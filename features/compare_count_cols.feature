Feature: Compare CSV files
    Scenario: Column count
        Given I have a CSV file
        And I have another CSV file
        When I compare the CSV files
        Then the number of columns should be the same

 