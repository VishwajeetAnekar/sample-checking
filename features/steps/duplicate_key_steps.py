from behave import when, then
from main import duplicate_keys_validation
import pandas as pd


@when('duplicate keys are validated')
def step_impl(context):
    context.validation_result = duplicate_keys_validation(context.data_file)


@then('no duplicate rows or columns are found')
def step_impl(context):
    assert context.validation_result == "Success: No duplicate columns found", context.validation_result
