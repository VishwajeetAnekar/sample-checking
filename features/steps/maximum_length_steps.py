from behave import given, when, then
from main import maximum_length_validation


@when('maximum length is validated')
def step_impl(context):
    context.validation_result = maximum_length_validation(
        context.config_file,  context.data_file)


@then('the length of each field is within the specified limits')
def step_impl(context):
    assert context.validation_result == "All test cases passed successfully", context.validation_result
    
    
