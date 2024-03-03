from behave import given, when, then
from main import expected_values_validation
import pandas as pd


@when('expected values are validated')
def step_impl(context):
    context.validation_result = expected_values_validation(context.config_file, context.data_file)


@then('all values in the specified columns are equal to expected values')
def step_impl(context):
    assert context.validation_result == "Success: All values in expected columns are valid" , context.validation_result