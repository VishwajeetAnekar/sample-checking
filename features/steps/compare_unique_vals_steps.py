from behave import *
from main import unique_value_validation



@when(u'I compare for unique values in the CSV files')
def step_impl(context):
    context.validation_result_df, context.validation_result = unique_value_validation(
        context.data_file, context.data_file2)
    context.validation_result_df.to_csv('Results/unique_value_validation_result.csv', index=False)

@then(u'the number of unique values should be the same')
def step_assert_unique_values(context):
    if context.validation_result.startswith("Success"):
        assert True, "No repeated values found in either file"
    else:
        assert False, f"Error: {context.validation_result}"