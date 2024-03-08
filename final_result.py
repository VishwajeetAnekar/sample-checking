import pandas as pd
import re
import numpy as np
from datetime import datetime


def column_count_validation(df1, df2):
    col_count_df1 = df1.shape[1]
    col_count_df2 = df2.shape[1]
    if col_count_df1 != col_count_df2:
        error_message = f"Error: Number of columns in ({col_count_df1}) and ({col_count_df2}) are not equal."
        result_df = pd.DataFrame({"PHARMACY_TRANSACTION_ID": ["Column Count"],
                                  "Column Name": [""],
                                  "Required Values": [""],
                                  "Status for column_count_validation": ["Failed"],
                                  "Error Value for column_count_validation": [""],
                                  "Details for column_count_validation": [error_message]})
        return result_df
    else:
        success_message = "Both files have the same number of columns"
        result_df = pd.DataFrame({"PHARMACY_TRANSACTION_ID": ["Column Count"],
                                  "Column Name": [""],
                                  "Required Values": [""],
                                  "Status for column_count_validation": ["Passed"],
                                  "Error Value for column_count_validation": [""],
                                  "Details for column_count_validation": [success_message]})
        return result_df


def unique_value_validation(df1, df2, pharmacy_transaction_id_col):
    common_ids = set(df1[pharmacy_transaction_id_col]).intersection(
        df2[pharmacy_transaction_id_col])

    result_rows = []

    for transaction_id in common_ids:
        result_rows.append({'PHARMACY_TRANSACTION_ID': transaction_id,
                            'Column Name': 'PHARMACY_TRANSACTION_ID',
                            'Required Values': '',
                            'Status for unique_value_validation': 'Failed',
                            'Error Value for unique_value_validation': '',
                            'Details for unique_value_validation': f'Transaction ID {transaction_id} is repeated in both files'})

    for transaction_id in df1[pharmacy_transaction_id_col]:
        if transaction_id not in common_ids:
            result_rows.append({'PHARMACY_TRANSACTION_ID': transaction_id,
                                'Column Name': 'PHARMACY_TRANSACTION_ID',
                                'Required Values': '',
                                'Status for unique_value_validation': 'Success',
                                'Error Value for unique_value_validation': '',
                                'Details for unique_value_validation': f'Transaction ID {transaction_id} is unique to File 1'})

    for transaction_id in df2[pharmacy_transaction_id_col]:
        if transaction_id not in common_ids:
            result_rows.append({'PHARMACY_TRANSACTION_ID': transaction_id,
                                'Column Name': 'PHARMACY_TRANSACTION_ID',
                                'Required Values': '',
                                'Status for unique_value_validation': 'Success',
                                'Error Value for unique_value_validation': '',
                                'Details for unique_value_validation': f'Transaction ID {transaction_id} is unique to File 2'})

    result_df = pd.DataFrame(result_rows)

    return result_df


def required_fields_validation(config_df, data_df):
    required_columns = config_df[config_df['Requirement']
                                 == 'Y']['Field Name'].tolist()
    missing_columns = []
    for col in required_columns:
        if col not in data_df.columns:
            missing_columns.append({
                "PHARMACY_TRANSACTION_ID": "",
                "Column Name": col,
                "Required Values": col,
                "Status for required_value_validation": "Failed",
                "Error Value for required_value_validation": "",
                "Details for required_value_validation": "Error: Required column is missing"
            })
        else:
            if data_df[col].isnull().values.any():
                missing_columns.append({
                    "PHARMACY_TRANSACTION_ID": "",
                    "Column Name": col,
                    "Required Values": col,
                    "Status for required_value_validation": "Failed",
                    "Error Value for required_value_validation": "",
                    "Details for required_value_validation": f"Error: Required field '{col}' has empty values"
                })
            else:
                missing_columns.append({
                    "PHARMACY_TRANSACTION_ID": "",
                    "Column Name": col,
                    "Required Values": col,
                    "Status for required_value_validation": "Success",
                    "Error Value for required_value_validation": "",
                    "Details for required_value_validation": "Success: All required fields have values"
                })

    for col in data_df.columns:
        if col not in required_columns:
            missing_columns.append({
                "PHARMACY_TRANSACTION_ID": "",
                "Column Name": col,
                "Required Values": "",
                "Status for required_value_validation": "Failed",
                "Error Value for required_value_validation": "",
                "Details for required_value_validation": f"Error: Non-required field '{col}' is present"
            })

    result_df = pd.DataFrame(missing_columns)

    return result_df


def expected_values_validation(config_df, data_df):
    expected_columns = config_df[config_df['Expected Value/s (comma separated)'].notnull(
    )]['Field Name'].tolist()
    error_messages = []

    for col in expected_columns:
        expected_values = config_df.loc[config_df['Field Name'] == col,
                                        'Expected Value/s (comma separated)'].iloc[0].strip('""').split(',')
        col_values = data_df[col].astype(str)
        empty_cells = (col_values == 'nan').sum()
        valid_values = col_values[col_values != ""]
        if 'nan' in valid_values.values:
            error_messages.append({
                "PHARMACY_TRANSACTION_ID": "",
                "Column Name": col,
                "Required Values": col,
                "Status for expected_value_validation": "Failed",
                "Error Value for expected_value_validation": "",
                "Details for expected_value_validation": f"Error: Column contains empty cells"
            })
        elif not set(valid_values).issubset(expected_values):
            error_messages.append({
                "PHARMACY_TRANSACTION_ID": "",
                "Column Name": col,
                "Required Values": col,
                "Status for expected_value_validation": "Failed",
                "Error Value for expected_value_validation": ", ".join(valid_values),
                "Details for expected_value_validation": f"Error: Column contains values not in expected values"
            })
        else:
            error_messages.append({
                "PHARMACY_TRANSACTION_ID": "",
                "Column Name": col,
                "Required Values": col,
                "Status for expected_value_validation": "Success",
                "Error Value for expected_value_validation": "",
                "Details for expected_value_validation": f"Success: All values in column are valid"
            })

    result_df = pd.DataFrame(error_messages)

    return result_df


def duplicate_keys_validation(df):
    column_names = df.columns.tolist()
    status_list = ["Success"] * len(column_names)
    details_list = [""] * len(column_names)

    for i, col_name in enumerate(column_names):
        if f"{col_name}.1" in column_names[i + 1:]:
            status_list[i] = "Success"
            details_list[i] = "Duplicate Columns: Original"
        elif '.1' in col_name:
            index = column_names.index(col_name)
            status_list[index] = "Failed"
            details_list[index] = "Duplicate Column"

    column_names = [col_name.split('.')[0] for col_name in column_names]

    result_df = pd.DataFrame({
        "PHARMACY_TRANSACTION_ID": "",
        "Column Name": column_names,
        "Required Values": column_names,
        "Status for duplicate_keys_validation": status_list,
        "Error Value for duplicate_keys_validation": "",
        "Details for duplicate_keys_validation": details_list
    })

    if result_df['Status for duplicate_keys_validation'].eq('Success').all():
        validation_result = "Success: No duplicate columns found"
    else:
        validation_result = "Failed: Duplicate columns found"

    return result_df


def merge_results(*args):
    merged_df = pd.concat(args)
    final_status = "Passed" if all(df['Status for column_count_validation'].eq('Success').all() for df in args) else "Failed"
    merged_df['Final Status'] = final_status
    return merged_df


# Example usage
# Load CSV files and configuration
df1 = pd.read_csv("extract-new.csv")
df2 = pd.read_csv("extract-old.csv")
config_df = pd.read_csv("configuration.csv")

# Perform validations
column_count_result = column_count_validation(df1, df2)
unique_value_result = unique_value_validation(df1, df2, "PHARMACY_TRANSACTION_ID")
required_fields_result = required_fields_validation(config_df, df1)
expected_values_result = expected_values_validation(config_df, df1)
duplicate_keys_result = duplicate_keys_validation(df1)

# Merge results
merged_result = merge_results(column_count_result, unique_value_result,
                              required_fields_result, expected_values_result, duplicate_keys_result)

# Save merged result to CSV
merged_result.to_csv("merged_result.csv", index=False)
