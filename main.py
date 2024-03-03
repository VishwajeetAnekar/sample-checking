import pandas as pd
import re
import csv
import numpy as np
from datetime import datetime

# def required_fields_validation(config_file, data_file):
#     config_df = config_file
#     required_columns = config_df[config_df['Requirement'] == 'Y']['Field Name'].tolist()

#     data_df =data_file
#     for col in required_columns:
#         if data_df[col].isnull().values.any():
#             return f"Error: Required field '{col}' has empty values"
#     return "Success: All required fields have values"


def required_fields_validation(config_file, data_file):
    config_df = config_file
    data_df = data_file
    required_columns = config_df[config_df['Requirement'] == 'Y']['Field Name'].tolist()
    missing_columns = []
    for col in required_columns:
        if col not in data_df.columns:
            missing_columns.append(col)
        else:
            if data_df[col].isnull().values.any():
                missing_columns.append(
                    f"Error: Required field '{col}' has empty values")
    if missing_columns:
        return '\n'.join(missing_columns)
    else:
        return "Success: All required fields have values"


def maximum_length_validation(config_file, csv_file):
    config_df = config_file
    col_dtype_map = dict(zip(config_df['Field Name'], config_df['Data Type']))
    data_df = csv_file
    all_test_cases_passed = True

    for col, dtype in col_dtype_map.items():
        if col not in data_df.columns:
            continue

        col_values = data_df[col].astype(str)
        for value in col_values:
            if value.lower() in ['nan']:
                continue

            if not value.strip():
                continue

            if isinstance(dtype, float) and np.isnan(dtype):
                continue

            if dtype.startswith('DATE'):
                if pd.isna(value):
                    try:
                        datetime.strptime(value, '%Y%m%d')
                    except ValueError:
                        print(
                            f"Invalid date format in column '{col}': {value}")
                        all_test_cases_passed = False

            elif dtype.startswith('VARCHAR'):
                length = int(re.search(r'\((\d+)\)', dtype).group(1))
                if len(value) > length:
                    print(f"Exceeded length limit in column '{col}': {value}")
                    all_test_cases_passed = False

            elif dtype.startswith('INTEGER'):
                if not value.isnumeric():
                    print(f"Invalid number format in column '{col}': {value}")
                    all_test_cases_passed = False

            elif dtype.startswith('NUMERIC'):
                length, decimal_length = map(int, re.search(
                    r'\((\d+),(\d+)\)', dtype).groups())
                if len(value.split('.')[0]) > length or len(value.split('.')[1]) > decimal_length:
                    print(f"Exceeded length limit in column '{col}': {value}")
                    all_test_cases_passed = False
                if not re.match(r'^\d+\.\d+$', value):
                    print(f"Invalid double format in column '{col}': {value}")
                    all_test_cases_passed = False

            elif dtype.startswith('TIMESTAMP'):
                try:
                    datetime.strptime(value, '%Y%m%d %H:%M:%S')
                except ValueError:
                    print(
                        f"Invalid timestamp format in column '{col}': {value}")
                    all_test_cases_passed = False

    if all_test_cases_passed:
        return "All test cases passed successfully"
    else:
        return "Some test cases failed. Please check the output for more details"


def expected_values_validation(config_file, data_file):
    config_df = config_file
    expected_columns = config_df[config_df['Expected Value/s (comma separated)'].notnull(
    )]['Field Name'].tolist()
    data_df = data_file
    error_messages = {}

    for col in expected_columns:
        expected_values = config_df.loc[config_df['Field Name'] == col,
                                        'Expected Value/s (comma separated)'].iloc[0].strip('""').split(',')

        col_values = data_df[col].dropna().astype(str).tolist()
        if all(value in expected_values for value in col_values):
            error_messages[
                col] = f"Success: All values in column '{col}' are equal to '{', '.join(expected_values)}'"
        else:
            error_messages[
                col] = f"Error: Values in column '{col}' are not equal to '{', '.join(expected_values)}': {col_values}"

    if any('Error' in message for message in error_messages.values()):
        return '\n'.join(error_messages.values())
    else:
        return "Success: All values in expected columns are valid"


def white_space_validation(df):
    invalid_columns = [col for col in df.columns if re.search(r'\s', col)]
    if invalid_columns:
        return f"Error: The following column names contain spaces: {', '.join(invalid_columns)}."
    else:
        return "Success: There are no spaces in the column names."


# def duplicate_keys_validation(csv_file):
#     df = pd.read_csv(csv_file)
#     duplicate_rows = df[df.duplicated()]
#     df_transposed = df.transpose()
#     duplicate_cols = df_transposed[df_transposed.duplicated()]
#     if duplicate_rows.empty and duplicate_cols.empty:
#         return "Success: No duplicate rows or columns found."
#     else:
#         result = "Error: "
#         if not duplicate_rows.empty:
#             result += f"Duplicate rows found at index: {', '.join(map(str, duplicate_rows.index))}. "
#         if not duplicate_cols.empty:
#             result += f"Duplicate columns found: {', '.join(map(str, duplicate_cols))}."
#         return result
def duplicate_keys_validation(csv_file):
    df = csv_file
    column_names = df.columns.tolist()
    duplicate_columns = []
    for col_name in column_names:
        if f"{col_name}.1" in column_names:
            duplicate_columns.append(col_name)

    if duplicate_columns:
        return f"Error: Duplicate columns found: {', '.join(duplicate_columns)}"
    else:
        return "Success: No duplicate columns found"




def column_count_validation(csv_file, csv_file2):
    df1 = csv_file
    df2 = csv_file2
    col_count_df1 = df1.shape[1]
    col_count_df2 = df2.shape[1]
    if col_count_df1 != col_count_df2:
        return f"Error: Number of columns in ({col_count_df1}) and ({col_count_df2}) are not equal."
    return "Both files have the same number of columns"



def unique_value_validation(csv_file1, csv_file2):
    df1 = csv_file1
    df2 = csv_file2
    common_values = df1.merge(df2, how='inner')
    if not common_values.empty:
        return "Error : Common values found", common_values
    else:
        return "Success : No common values found"

    

def generate_csv_report(passed_features, failed_features, failed_features_details, validation_message, common_values_df, filename="test_results.csv"):
    df = pd.DataFrame({"Feature": passed_features + failed_features, "Status": ["Passed"] * len(passed_features) + ["Failed"] * len(failed_features)})
    df["Details"] = df["Feature"].map(lambda x: failed_features_details.get(x, ""))
    df["Validation Message"] = validation_message
    df = df.append(common_values_df, ignore_index=True)
    df.to_csv(filename, index=False)
    print(f"CSV file '{filename}' created successfully.")



# def unique_value_validation(csv_file1, csv_file2):
#     df1 = pd.read_csv(csv_file1)
#     df2 = pd.read_csv(csv_file2)
#     combined_df = pd.concat([df1, df2])
#     unique_values = combined_df.drop_duplicates(subset=df1.columns)
#     if unique_values.empty:
#             return "Success : No common values found"
#     else:
#         return "Error : Common values found", unique_values


# config = 'configuration.csv'
# csv_file = 'extract-new.csv'
# csv_file2 = 'extract-old.csv'
# results_file = 'result.csv'


# results = []
# results.append(['required_fields_validation', required_fields_validation(config, csv_file)])
# results.append(['maximum_length_validation', maximum_length_validation(csv_file, config)])
# results.append(['expected_values_validation', expected_values_validation(config, csv_file)])
# results.append(['duplicate_keys_validation', duplicate_keys_validation(csv_file)])
# results.append(['white_space_validation', white_space_validation(csv_file)])
# results.append(['compare_csv_files', compare_csv_files(csv_file, csv_file2)])
# results.append(['unique_value_validation', unique_value_validation(csv_file, csv_file2)])

# with open(results_file, 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Function','Result'])
#     writer.writerows(results)
