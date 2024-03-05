import pandas as pd
import re
import csv
import numpy as np
from datetime import datetime


def column_count_validation(csv_file, csv_file2):
    df1 = csv_file
    df2 = csv_file2
    col_count_df1 = df1.shape[1]
    col_count_df2 = df2.shape[1]
    if col_count_df1 != col_count_df2:
        error_message = f"Error: Number of columns in ({col_count_df1}) and ({col_count_df2}) are not equal."
        result_df = pd.DataFrame({"No. of Columns in CSV 1": [col_count_df1],
                                   "No. of Columns in CSV 2": [col_count_df2],
                                   "Result": [error_message],
                                   "Status": ["Failed"]})
        return result_df, error_message
    else:
        success_message = "Both files have the same number of columns"
        result_df = pd.DataFrame({"No. of Columns in CSV 1": [col_count_df1],
                                   "No. of Columns in CSV 2": [col_count_df2],
                                   "Result": [success_message],
                                   "Status": ["Passed"]})
        return result_df, success_message

def unique_value_validation(csv_file1, csv_file2):
    df1 = csv_file1
    df2 = csv_file2
    
    # Check if "PHARMACY_TRANSACTION_ID" column exists in both DataFrames
    if "PHARMACY_TRANSACTION_ID" not in df1.columns or "PHARMACY_TRANSACTION_ID" not in df2.columns:
        return pd.DataFrame(), "Error: 'PHARMACY_TRANSACTION_ID' column not found in one or both CSV files"
    
    # Compare the rest of the data based on "PHARMACY_TRANSACTION_ID" column
    common_values = df1.merge(df2, how='inner', on='PHARMACY_TRANSACTION_ID')
    if not common_values.empty:
        error_message = "Error: Common values found"
        result_df = pd.DataFrame({"Result": [error_message],
                                   "Status": ["Failed"]})
        return result_df, error_message
    else:
        success_message = "Success: No common values found"
        result_df = pd.DataFrame({"Result": [success_message],
                                   "Status": ["Passed"]})
        return result_df, success_message
    

# def unique_value_validation(csv_file1, csv_file2):
#     df1 = csv_file1
#     df2 = csv_file2
#     common_values = df1.merge(df2, how='inner')
#     if not common_values.empty:
#         error_message = "Error: Common values found"
#         result_df = pd.DataFrame({"Result": [error_message],
#                                    "Status": ["Failed"]})
#         return result_df, error_message
#     else:
#         success_message = "Success: No common values found"
#         result_df = pd.DataFrame({"Result": [success_message],
#                                    "Status": ["Passed"]})
#         return result_df, success_message
    
# def column_count_validation(csv_file, csv_file2):
#     df1 = csv_file
#     df2 = csv_file2
#     col_count_df1 = df1.shape[1]
#     col_count_df2 = df2.shape[1]
#     if col_count_df1 != col_count_df2:
#         return f"Error: Number of columns in ({col_count_df1}) and ({col_count_df2}) are not equal."
#     return "Both files have the same number of columns"


# def unique_value_validation(csv_file1, csv_file2):
#     df1 = csv_file1
#     df2 = csv_file2
#     common_values = df1.merge(df2, how='inner')
#     if not common_values.empty:
#         return "Error : Common values found", common_values
#     else:
#         return "Success : No common values found"


def required_fields_validation(config_file, data_file):
    config_df = config_file
    data_df = data_file
    required_columns = config_df[config_df['Requirement']
                                 == 'Y']['Field Name'].tolist()
    missing_columns = []
    for col in required_columns:
        if col not in data_df.columns:
            missing_columns.append({
                "Column Name": col,
                "Required Field (Y/N)": "Y",
                "Status": "Failed",
                "Details": "Error: Required column is missing"
            })
        else:
            if data_df[col].isnull().values.any():
                missing_columns.append({
                    "Column Name": col,
                    "Required Field (Y/N)": "Y",
                    "Status": "Failed",
                    "Details": f"Error: Required field '{col}' has empty values"
                })
            else:
                missing_columns.append({
                    "Column Name": col,
                    "Required Field (Y/N)": "Y",
                    "Status": "Success",
                    "Details": "Success: All required fields have values"
                })

    for col in data_df.columns:
        if col not in required_columns:
            missing_columns.append({
                "Column Name": col,
                "Required Field (Y/N)": "N",
                "Status": "Failed",
                "Details": f"Error: Non-required field '{col}' is present"
            })

    result_df = pd.DataFrame(missing_columns)
    result_df = result_df[['Column Name',
                           'Required Field (Y/N)', 'Status', 'Details']]

    validation_result = "Success: All required fields have values" if result_df['Status'].eq(
        'Success').all() else result_df.to_string(index=False)

    return result_df, validation_result


# def required_fields_validation(config_file, data_file):
#     config_df = config_file
#     data_df = data_file
#     required_columns = config_df[config_df['Requirement']
#                                  == 'Y']['Field Name'].tolist()
#     missing_columns = []
#     for col in required_columns:
#         if col not in data_df.columns:
#             missing_columns.append(col)
#         else:
#             if data_df[col].isnull().values.any():
#                 missing_columns.append(
#                     f"Error: Required field '{col}' has empty values")

#     if missing_columns:
#         return '\n'.join(missing_columns)
#     else:
#         return "Success: All required fields have values"


def expected_values_validation(config_file, data_file):
    config_df = config_file
    expected_columns = config_df[config_df['Expected Value/s (comma separated)'].notnull(
    )]['Field Name'].tolist()
    data_df = data_file
    error_messages = []

    for col in expected_columns:
        expected_values = config_df.loc[config_df['Field Name'] == col,
                                        'Expected Value/s (comma separated)'].iloc[0].strip('""').split(',')
        col_values = data_df[col].astype(str)
        empty_cells = (col_values == 'nan').sum()
        valid_values = col_values[col_values != ""]
        if 'nan' in valid_values.values:

            error_messages.append({
                "Column Name": col,
                "Expected Values": ", ".join(expected_values),
                "Status": "Failed",
                "Column Values": ", ".join(valid_values),
                "Empty Cell": empty_cells,
                "Details": f"Error: Column contains empty cells"
            })
        elif not set(valid_values).issubset(expected_values):
            error_messages.append({
                "Column Name": col,
                "Expected Values": ", ".join(expected_values),
                "Status": "Failed",
                "Column Values": ", ".join(valid_values),
                "Details": f"Error: Column contains values not in expected values"
            })
        else:
            error_messages.append({
                "Column Name": col,
                "Expected Values": ", ".join(expected_values),
                "Status": "Success",
                "Column Values": ", ".join(valid_values),
                "Details": f"Success: All values in column are valid"
            })

    result_df = pd.DataFrame(error_messages)
    result_df = result_df[['Column Name', 'Expected Values',
                           'Status', 'Column Values', 'Empty Cell', 'Details']]

    validation_result = "Success: All values in expected columns are valid" if result_df['Status'].eq(
        'Success').all() else result_df.to_string(index=False)

    return result_df, validation_result


# def expected_values_validation(config_file, data_file):
#     config_df = config_file
#     expected_columns = config_df[config_df['Expected Value/s (comma separated)'].notnull(
#     )]['Field Name'].tolist()
#     data_df = data_file
#     error_messages = {}

#     for col in expected_columns:
#         expected_values = config_df.loc[config_df['Field Name'] == col,
#                                         'Expected Value/s (comma separated)'].iloc[0].strip('""').split(',')

#         col_values = data_df[col].dropna().astype(str).tolist()
#         if all(value in expected_values for value in col_values):
#             error_messages[
#                 col] = f"Success: All values in column '{col}' are equal to '{', '.join(expected_values)}'"
#         else:
#             error_messages[
#                 col] = f"Error: Values in column '{col}' are not equal to '{', '.join(expected_values)}': {col_values}"

#     if any('Error' in message for message in error_messages.values()):
#         return '\n'.join(error_messages.values())
#     else:
#         return "Success: All values in expected columns are valid"


# def white_space_validation(df):
#     invalid_columns = [col for col in df.columns if re.search(r'\s', col)]
#     if invalid_columns:
#         return f"Error: The following column names contain spaces: {', '.join(invalid_columns)}."
#     else:
#         return "Success: There are no spaces in the column names."


def white_space_validation(df):
    invalid_columns = [col for col in df.columns if re.search(r'\s', col)]
    status_list = []
    details_list = []
    for col in df.columns:
        if col in invalid_columns:
            if re.match(r'^\s', col) and re.search(r'\s$', col):
                details = "Before and After"
            elif re.match(r'^\s', col):
                details = "Before"
            elif re.search(r'\s$', col):
                details = "After"
            elif re.search(r'\s', col):
                details = "Between"
            else:
                details = ""
            status_list.append("Failed")
            details_list.append(details)
        else:
            status_list.append("Success")
            details_list.append("")

    result_df = pd.DataFrame({
        "Column Name": df.columns,
        "Status": status_list,
        "Details": details_list
    })
    if result_df['Status'].eq('Success').all():
        validation_result = "Success: There are no spaces in the column names."
    else:
        validation_result = result_df.to_string(index=False)

    return result_df, validation_result


# def duplicate_keys_validation(csv_file):
#     df = csv_file
#     column_names = df.columns.tolist()
#     duplicate_columns = []
#     for col_name in column_names:
#         if f"{col_name}.1" in column_names:
#             duplicate_columns.append(col_name)

#     if duplicate_columns:
#         return f"Error: Duplicate columns found: {', '.join(duplicate_columns)}"
#     else:
#         return "Success: No duplicate columns found"


def duplicate_keys_validation(df):
    column_names = df.columns.tolist()
    status_list = ["Success"] * len(column_names)
    details_list = [""] * len(column_names)

    for i, col_name in enumerate(column_names):
        if f"{col_name}.1" in column_names[i + 1:]:
            status_list[i] = "Failed"
            details_list[i] = "Duplicate Columns"

    result_df = pd.DataFrame({
        "Column Name": column_names,
        "Status": status_list,
        "Details": details_list
    })

    if result_df['Status'].eq('Success').all():
        validation_result = "Success: No duplicate columns found"
    else:
        validation_result = result_df.to_string(index=False)

    return result_df, validation_result

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


# def unique_value_validation(csv_file1, csv_file2):
#     df1 = pd.read_csv(csv_file1)
#     df2 = pd.read_csv(csv_file2)
#     combined_df = pd.concat([df1, df2])
#     unique_values = combined_df.drop_duplicates(subset=df1.columns)
#     if unique_values.empty:
#             return "Success : No common values found"
#     else:
#         return "Error : Common values found", unique_values


# def maximum_length_validation(config_file, csv_file):
#     config_df = config_file
#     col_dtype_map = dict(zip(config_df['Field Name'], config_df['Data Type']))
#     data_df = csv_file
#     all_test_cases_passed = True

#     for col, dtype in col_dtype_map.items():
#         if col not in data_df.columns:
#             continue

#         col_values = data_df[col].astype(str)
#         for value in col_values:
#             if value.lower() in ['nan']:
#                 continue

#             if not value.strip():
#                 continue

#             if isinstance(dtype, float) and np.isnan(dtype):
#                 continue

#             if dtype.startswith('DATE'):
#                 if pd.isna(value):
#                     try:
#                         datetime.strptime(value, '%Y%m%d')
#                     except ValueError:
#                         print(
#                             f"Invalid date format in column '{col}': {value}")
#                         all_test_cases_passed = False

#             elif dtype.startswith('VARCHAR'):
#                 length = int(re.search(r'\((\d+)\)', dtype).group(1))
#                 if len(value) > length:
#                     print(f"Exceeded length limit in column '{col}': {value}")
#                     all_test_cases_passed = False

#             elif dtype.startswith('INTEGER'):
#                 if not value.isnumeric():
#                     print(f"Invalid number format in column '{col}': {value}")
#                     all_test_cases_passed = False

#             elif dtype.startswith('NUMERIC'):
#                 length, decimal_length = map(int, re.search(
#                     r'\((\d+),(\d+)\)', dtype).groups())
#                 if len(value.split('.')[0]) > length or len(value.split('.')[1]) > decimal_length:
#                     print(f"Exceeded length limit in column '{col}': {value}")
#                     all_test_cases_passed = False
#                 if not re.match(r'^\d+\.\d+$', value):
#                     print(f"Invalid double format in column '{col}': {value}")
#                     all_test_cases_passed = False

#             elif dtype.startswith('TIMESTAMP'):
#                 try:
#                     datetime.strptime(value, '%Y%m%d %H:%M:%S')
#                 except ValueError:
#                     print(
#                         f"Invalid timestamp format in column '{col}': {value}")
#                     all_test_cases_passed = False

#     if all_test_cases_passed:
#         return "All test cases passed successfully"
#     else:
#         return "Some test cases failed. Please check the output for more details"

def maximum_length_validation(config_file, csv_file):
    config_df = config_file
    col_dtype_map = dict(zip(config_df['Field Name'], config_df['Data Type']))
    data_df = csv_file
    all_test_cases_passed = True

    validation_result_list = []

    for col, dtype in col_dtype_map.items():
        if col not in data_df.columns:
            validation_result_list.append({
                "Column Name": col,
                "Data Type": dtype,
                "Status": "Failed",
                "Details": f"Error: Column not present in data: '{col}'"
            })
            all_test_cases_passed = False
            continue

        col_values = data_df[col].astype(str)
        for value in col_values:
            if value.lower() in ['nan']:
                continue

            if not value.strip():
                validation_result_list.append({
                    "Column Name": col,
                    "Data Type": dtype,
                    "Status": "Failed",
                    "Details": f"Error: Empty value in column '{col}'"
                })
                all_test_cases_passed = False
                break

            if isinstance(dtype, float) and np.isnan(dtype):
                continue

            if dtype.startswith('DATE'):
                if pd.isna(value):
                    try:
                        datetime.strptime(value, '%Y%m%d')
                    except ValueError:
                        validation_result_list.append({
                            "Column Name": col,
                            "Data Type": dtype,
                            "Status": "Failed",
                            "Details": f"Error: Invalid date format in column '{col}': {value}"
                        })
                        all_test_cases_passed = False

            elif dtype.startswith('VARCHAR'):
                length = int(re.search(r'\((\d+)\)', dtype).group(1))
                if len(value) > length:
                    validation_result_list.append({
                        "Column Name": col,
                        "Data Type": dtype,
                        "Status": "Failed",
                        "Details": f"Error: Exceeded length limit in column '{col}': {value}"
                    })
                    all_test_cases_passed = False

            elif dtype.startswith('INTEGER'):
                if not value.isnumeric():
                    validation_result_list.append({
                        "Column Name": col,
                        "Data Type": dtype,
                        "Status": "Failed",
                        "Details": f"Error: Invalid number format in column '{col}': {value}"
                    })
                    all_test_cases_passed = False

            elif dtype.startswith('NUMERIC'):
                length, decimal_length = map(int, re.search(
                    r'\((\d+),(\d+)\)', dtype).groups())
                if len(value.split('.')[0]) > length or len(value.split('.')[1]) > decimal_length:
                    validation_result_list.append({
                        "Column Name": col,
                        "Data Type": dtype,
                        "Status": "Failed",
                        "Details": f"Error: Exceeded length limit in column '{col}': {value}"
                    })
                    all_test_cases_passed = False
                if not re.match(r'^\d+\.\d+$', value):
                    validation_result_list.append({
                        "Column Name": col,
                        "Data Type": dtype,
                        "Status": "Failed",
                        "Details": f"Error: Invalid double format in column '{col}': {value}"
                    })
                    all_test_cases_passed = False

            elif dtype.startswith('TIMESTAMP'):
                try:
                    datetime.strptime(value, '%Y%m%d %H:%M:%S')
                except ValueError:
                    validation_result_list.append({
                        "Column Name": col,
                        "Data Type": dtype,
                        "Status": "Failed",
                        "Details": f"Error: Invalid timestamp format in column '{col}': {value}"
                    })
                    all_test_cases_passed = False

    for col in data_df.columns:
        if col not in col_dtype_map.keys():
            validation_result_list.append({
                "Column Name": col,
                "Data Type": "Not Specified",
                "Status": "Success",
                "Details": ""
            })

    validation_result_df = pd.DataFrame(validation_result_list, columns=[
                                        "Column Name", "Data Type", "Status", "Details"])

    if all_test_cases_passed:
        return "All test cases passed successfully", validation_result_df
    else:
        return "Some test cases failed. Please check the output for more details", validation_result_df
