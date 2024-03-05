# from behave import *
# import pandas as pd
# from main import column_count_validation
# from csv_paths import *

# @given(u'I have a CSV file')
# def step_impl(context):
#     context.data_file = pd.read_csv(latest_extract)


# @given(u'I have another CSV file')
# def step_impl(context):
#     context.data_file2 = pd.read_csv(old_extract)



# @when(u'I compare the CSV files')
# def step_impl(context):
#     context.validation_result = column_count_validation(
#         context.data_file, context.data_file2)


# @then(u'the number of columns should be the same')
# def step_impl(context):
#     assert context.validation_result == "Both files have the same number of columns", context.validation_result

# Step file for column count validation
from behave import given, when, then
import pandas as pd
from csv_paths import *
from main import column_count_validation

@given(u'I have a CSV file')
def step_impl(context):
    context.data_file = pd.read_csv(latest_extract)

@given(u'I have another CSV file')
def step_impl(context):
    context.data_file2 = pd.read_csv(old_extract)

@when(u'I compare the CSV files')
def step_impl(context):
    context.validation_result_df, context.validation_result = column_count_validation(
        context.data_file, context.data_file2)
    context.validation_result_df.to_csv('Results/column_count_validation_result.csv', index=False)

@then(u'the number of columns should be the same')
def step_impl(context):
    assert context.validation_result == "Both files have the same number of columns", context.validation_result
