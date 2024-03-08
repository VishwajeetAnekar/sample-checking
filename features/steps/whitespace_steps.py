

from main import white_space_validation
from behave import given, when, then


@when(u'CSV file is validated')
def step_impl(context):
    context.validation_result_df, context.validation_result = white_space_validation(
        context.data_file)

    context.validation_result_df.to_csv(
        'Results/WhiteSpace_validation_result.csv', index=False)


@then(u'the validation should be successful')
def step_impl(context):
    if context.validation_result == "Success: There are no spaces in the column values.":
        validation_result = "Success"
    else:
        validation_result = "Error"

    assert validation_result == "Success", "Validation failed"
