from behave import given, when, then
from main import maximum_length_validation

@when('maximum length is validated')
def step_impl(context):
    context.validation_result, context.validation_result_df = maximum_length_validation(
        context.config_file, context.data_file)
    context.validation_result_df.to_csv('Results/maximum_length_validation_result.csv', index=False)

@then('the length of each field is within the specified limits')
def step_impl(context):
        assert context.validation_result == "All test cases passed successfully", "Validation failed"


