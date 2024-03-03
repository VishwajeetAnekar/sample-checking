from behave import *
from main import unique_value_validation


@when(u'I compare for unique values in the CSV files')
def step_impl(context):
    context.validation_result= unique_value_validation(
        context.data_file, context.data_file2)


@then(u'the number of unique values should be the same')
def step_impl(context):
    assert context.validation_result == "Success : No common values found", context.validation_result
