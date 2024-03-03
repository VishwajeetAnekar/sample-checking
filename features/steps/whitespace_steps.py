from main import white_space_validation
from behave import given, when, then


@when(u'CSV file is validated')
def step_impl(context):
    context.validation_result = white_space_validation(context.data_file)


@then(u'the validation should be successful')
def step_impl(context):
    assert context.validation_result == "Success: There are no spaces in the column names.", context.validation_result
