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
    context.validation_result = required_fields_validation(
        context.config_file, context.data_file)


@then('all required fields have values')
def step_impl(context):
    assert context.validation_result == "Success: All required fields have values", context.validation_result



# from behave import given, when, then
# from main import required_fields_validation, write_to_csv
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
#     assert context.validation_result['status'] == "Success", context.validation_result['detail']

# @then('the validation result is saved to a CSV file')
# def step_impl(context):
#     write_to_csv('Validate Required Fields', context.validation_result)
