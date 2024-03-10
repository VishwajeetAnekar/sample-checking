from behave import when, then
from main import duplicate_keys_validation
import pandas as pd

@when('duplicate keys are validated')
def step_impl(context):
    context.validation_result_df, context.validation_result = duplicate_keys_validation(context.data_file)
    context.validation_result_df.to_csv('Results/duplicate_keys_validation_result.csv', index=False)

@then('no duplicate rows or columns are found')
def step_impl(context):
    if context.validation_result == "Success: No duplicate columns found":
        validation_result = "Success"
    else:
        validation_result = "Error"

    assert validation_result == "Success", "Validation failed"


