# from behave import given, when, then
# from main import required_fields_validation
# import pandas as pd

# from csv_paths import *


# @given('a configuration file')
# def step_impl(context):
#     context.config_file = pd.read_csv(config_file)


# @given('a csv file')
# def step_impl(context):
#     context.data_file = pd.read_csv(latest_extract)


# @when('required fields are validated')
# def step_impl(context):
#     context.validation_result = required_fields_validation(
#         context.config_file, context.data_file)


# @then('all required fields have values')
# def step_impl(context):
#     assert context.validation_result == "Success: All required fields have values", context.validation_result

from behave import given, when, then
from main import required_fields_validation
import pandas as pd

from csv_paths import *


@given('a configuration file')
def step_impl(context):
    context.config_file = pd.read_csv(config_file)


@given('a csv file')
def step_impl(context):
    context.data_file = pd.read_csv(latest_extract)


@when('required fields are validated')
def step_impl(context):
    context.validation_result_df, context.validation_result = required_fields_validation(
        context.config_file, context.data_file)

    # Save the validation result to a CSV file
    context.validation_result_df.to_csv(
        'Results/required_fields_validation_result.csv', index=False)


@then('all required fields have values')
def step_impl(context):
    # Check if the validation result is successful
    if context.validation_result == "Success: All required fields have values":
        validation_result = "Success"
    else:
        validation_result = "Error"

    # Assert that the validation result is Success
    assert validation_result == "Success", "Validation failed"


