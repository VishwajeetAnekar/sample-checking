import pandas as pd
import re
import numpy as np
from datetime import datetime


def column_count_validation(csv_file, csv_file2):
    df1 = csv_file
    df2 = csv_file2
    col_count_df1 = df1.shape[1]
    col_count_df2 = df2.shape[1]
    if col_count_df1 != col_count_df2:
        error_message = f"Error: Number of columns in ({col_count_df1}) and ({col_count_df2}) are not equal."
        result_df = pd.DataFrame({"Feature ": 'Column Count Validation',
                                  "No. of Columns in CSV 1": [col_count_df1],
                                   "No. of Columns in CSV 2": [col_count_df2],
                                   "Result": [error_message],
                                   "Status": ["Failed"]})
        return result_df, error_message
    else:
        success_message = "Both files have the same number of columns"
        result_df = pd.DataFrame({"Feature ": 'Column Count Validation',
                                    "No. of Columns in CSV 1": [col_count_df1],
                                    "No. of Columns in CSV 2": [col_count_df2],
                                 "Result": [success_message],
                                   "Status": ["Passed"]})
        return result_df, success_message


def unique_value_validation(csv_file1, csv_file2):
    df1 = csv_file1
    df2 = csv_file2
    
    if "PHARMACY_TRANSACTION_ID" not in df1.columns or "PHARMACY_TRANSACTION_ID" not in df2.columns:
        return pd.DataFrame(), "Error: 'PHARMACY_TRANSACTION_ID' column not found in one or both CSV files"
    common_ids = set(df1["PHARMACY_TRANSACTION_ID"]).intersection(df2["PHARMACY_TRANSACTION_ID"])

    result_rows = []

    for transaction_id in common_ids:
        result_rows.append({'Column Name': 'PHARMACY_TRANSACTION_ID', 
                            'Status': 'Failed', 
                            'Repeated Value': transaction_id, 
                            'Details': f'Transaction ID {transaction_id} is repeated in both files'})
        

    for transaction_id in df1["PHARMACY_TRANSACTION_ID"]:
        if transaction_id not in common_ids:

            result_rows.append({'Column Name': 'PHARMACY_TRANSACTION_ID', 
                                'Status': 'Success', 
                                'Repeated Value': transaction_id, 
                                'Details': f'Transaction ID {transaction_id} is unique to File 1'})
            
    for transaction_id in df2["PHARMACY_TRANSACTION_ID"]:
        if transaction_id not in common_ids:

            result_rows.append({'Column Name': 'PHARMACY_TRANSACTION_ID', 
                                'Status': 'Success', 
                                'Repeated Value': transaction_id, 
                                'Details': f'Transaction ID {transaction_id} is unique to File 2'})

    result_df = pd.DataFrame(result_rows)

    return result_df , "Success: No common values found"


def required_fields_validation(config_file, data_file):
    config_df = config_file
    data_df = data_file
    required_columns = config_df[config_df['Requirement'] == 'Y']['Field Name'].tolist()
    missing_columns = []

    for txn_id in data_df['PHARMACY_TRANSACTION_ID'].unique():
        txn_df = data_df[data_df['PHARMACY_TRANSACTION_ID'] == txn_id]
        for col in required_columns:
            if col not in txn_df.columns:
                missing_columns.append({
                    "PHARMACY_TRANSACTION_ID": txn_id,
                    "Column Name": col,
                    "Required Field (Y/N)": "Y",
                    "Value": " ",
                    "Status": "Failed",
                    "Details": "Error: Required column is missing"
                    
                })
            else:
                if txn_df[col].isnull().values.any():
                    missing_columns.append({
                        "PHARMACY_TRANSACTION_ID": txn_id,
                        "Column Name": col,
                        "Required Field (Y/N)": "Y",
                        "Value": txn_df[col].iloc[0],
                        "Status": "Failed",
                        "Details": f"Error: Required field '{col}' has empty values"
                        })
                else:
                    missing_columns.append({
                        "PHARMACY_TRANSACTION_ID": txn_id,
                        "Column Name": col,
                        "Required Field (Y/N)": "Y",
                        "Value": txn_df[col].iloc[0],
                        "Status": "Success",
                        "Details": "Success: All required fields have values"
                        
                    })

        for col in txn_df.columns:
            if col not in required_columns:
                missing_columns.append({
                    "PHARMACY_TRANSACTION_ID": txn_id,
                    "Column Name": col,
                    "Required Field (Y/N)": "N",
                    "Value": txn_df[col].iloc[0],
                    "Status": "Success",
                    "Details": f"Non-required field '{col}' is present"
                    
                })

    result_df = pd.DataFrame(missing_columns)
    result_df = result_df[['PHARMACY_TRANSACTION_ID', 'Column Name', 'Required Field (Y/N)', 'Value','Status', 'Details']]

    validation_result = "Success: All required fields have values" if result_df['Status'].eq(
        'Success').all() else result_df.to_string(index=False)

    return result_df, validation_result


def expected_values_validation(config_file, data_file):
    config_df = config_file
    data_df = data_file
    error_messages = []

    for txn_id in data_df['PHARMACY_TRANSACTION_ID'].unique():  # Loop over unique transaction IDs
        txn_df = data_df[data_df['PHARMACY_TRANSACTION_ID'] == txn_id]
        for _, config_row in config_df.iterrows():  # Loop through each row in the config
            col = config_row['Field Name']
            expected_values_str = str(config_row['Expected Value/s (comma separated)']).strip('""')
            expected_values = expected_values_str.split(',') if expected_values_str.lower() != 'nan' else []

            if col not in txn_df.columns:
                # Handle missing column in data file
                error_messages.append({
                    "PHARMACY_TRANSACTION_ID": txn_id,
                    "Column Name": col,
                    "Expected Values": expected_values_str,
                    "Status": "Failed",
                    "Column Value": "",
                    "Details": f"Error: Column '{col}' not found in the data file"
                })
                continue

            for index, row in txn_df.iterrows():  # Loop through each row within the transaction
                col_value = row[col] if col in row.index else None
                if pd.isnull(col_value) or col_value == "":
                    # If column value is empty or NaN, mark as success
                    error_messages.append({
                        "PHARMACY_TRANSACTION_ID": txn_id,
                        "Column Name": col,
                        "Expected Values": expected_values_str,
                        "Status": "Success",
                        "Column Value": col_value,
                        "Details": f"Success: Column value '{col_value}' is valid"
                    })
                elif expected_values and col_value not in expected_values:
                    error_messages.append({
                        "PHARMACY_TRANSACTION_ID": txn_id,
                        "Column Name": col,
                        "Expected Values": expected_values_str,
                        "Status": "Failed",
                        "Column Value": col_value,
                        "Details": f"Error: Column value '{col_value}' not in expected values"
                    })
                else:
                    error_messages.append({
                        "PHARMACY_TRANSACTION_ID": txn_id,
                        "Column Name": col,
                        "Expected Values": expected_values_str,
                        "Status": "Success",
                        "Column Value": col_value,
                        "Details": f"Success: Column value '{col_value}' is valid"
                    })

    result_df = pd.DataFrame(error_messages)
    result_df = result_df[['PHARMACY_TRANSACTION_ID', 'Column Name', 'Expected Values',
                           'Status', 'Column Value', 'Details']]

    validation_result = "Success: All values in expected columns are valid" if result_df['Status'].eq(
        'Success').all() else result_df.to_string(index=False)

    return result_df, validation_result

def white_space_validation(df):
    result_data = []

    for txn_id in df['PHARMACY_TRANSACTION_ID'].unique():
        txn_df = df[df['PHARMACY_TRANSACTION_ID'] == txn_id]
        for col in df.columns:
            for index, value in txn_df[col].items():
                if isinstance(value, str) and re.search(r'\s\s', value):
                    if re.match(r'^\s', value) and re.search(r'\s$', value):
                        details = "Before and After"
                    elif re.match(r'^\s', value):
                        details = "Before"
                    elif re.search(r'\s$', value):
                        details = "After"
                    elif re.search(r'\s\s', value):
                        details = "Between"
                    else:
                        details = ""
                    result_data.append({
                        "PHARMACY_TRANSACTION_ID": txn_id,
                        "Column Name": col,
                        "Value": value,
                        "Status": "Failed",
                        "Details": details
                    })
                else:
                    result_data.append({
                        "PHARMACY_TRANSACTION_ID": txn_id,
                        "Column Name": col,
                        "Value": value,
                        "Status": "Success",
                        "Details": ""
                    })

    result_df = pd.DataFrame(result_data)

    if result_df['Status'].eq('Success').all():
        validation_result = "Success: There are no spaces in the column values."
    else:
        validation_result = result_df.to_string(index=False)

    return result_df, validation_result

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
        "Column Name": column_names,
        "Status": status_list,
        "Details": details_list
    })

    if result_df['Status'].eq('Success').all():
        validation_result = "Success: No duplicate columns found"
    else:
        validation_result = result_df.to_html(index=False)

    return result_df, validation_result



def maximum_length_validation(config_file, csv_file):
    config_df = config_file
    col_dtype_map = dict(zip(config_df['Field Name'], config_df['Data Type']))
    data_df = csv_file
    all_test_cases_passed = True
    validation_result_list = []

    for txn_id in data_df['PHARMACY_TRANSACTION_ID'].unique():
        txn_df = data_df[data_df['PHARMACY_TRANSACTION_ID'] == txn_id]

        for col in txn_df.columns:
            column_passed = True
            if col not in col_dtype_map.keys():
                validation_result_list.append({
                    "PHARMACY_TRANSACTION_ID": txn_id,
                    "Column Name": col,
                    "Data Type": "Not Specified",
                    "Value": value,
                    "Status": "Success",
                    "Details": "Data Type not Specified for column"
                })
                continue

            dtype = col_dtype_map[col]
            col_values = txn_df[col].astype(str)

            for value in col_values:
                if value.lower() in ['nan']:
                    continue

                if not value.strip():
                    validation_result_list.append({
                        "PHARMACY_TRANSACTION_ID": txn_id,
                        "Column Name": col,
                        "Data Type": dtype,
                        "Value": value,
                        "Status": "Failed",
                        "Details": f"Error: Empty value in column '{col}'"
                    })
                    column_passed = False
                    all_test_cases_passed = False
                
                elif dtype.startswith('DATE'):
                    
                    length = int(re.search(r'\((\d+)\)', dtype).group(1))
                    value = value.replace('.0','')
                    if not value.strip():
                        validation_result_list.append({
                            "PHARMACY_TRANSACTION_ID": txn_id,
                            "Column Name": col,
                            "Data Type": dtype,
                            "Value": value,
                            "Status": "Failed",
                            "Details": f"Error: Empty value in column '{col}'"
                        })
                        column_passed = False
                        all_test_cases_passed = False
                    elif len(value) != length:  
                      


                        validation_result_list.append({
                            "PHARMACY_TRANSACTION_ID": txn_id,
                            "Column Name": col,
                            "Data Type": dtype,
                            "Value": value,
                            "Status": "Failed",
                            "Details": f"Error: Invalid date length in column '{col}'. Expected length: {length}"
                        })
                        column_passed = False
                        all_test_cases_passed = False
                    else:
                        
                        try:
                            datetime.strptime(value, '%Y%m%d') 
                        except ValueError:
                            validation_result_list.append({
                                "PHARMACY_TRANSACTION_ID": txn_id,
                                "Column Name": col,
                                "Data Type": dtype,
                                "Value": value,
                                "Status": "Failed",
                                "Details": f"Error: Invalid date format in column '{col}'"
                            })
                            column_passed = False
                            all_test_cases_passed = False

                elif dtype.startswith('VARCHAR'):
                    length = int(re.search(r'\((\d+)\)', dtype).group(1))
                    if len(value) > length:
                        validation_result_list.append({
                            "PHARMACY_TRANSACTION_ID": txn_id,
                            "Column Name": col,
                            "Data Type": dtype,
                            "Value": value,
                            "Status": "Failed",
                            "Details": f"Error: Exceeded length limit in column '{col}'"
                        })
                        column_passed = False
                        all_test_cases_passed = False

                elif dtype.startswith('INTEGER'):
                    if not value.replace('.0', '').isnumeric() and value.strip() != '':
                        validation_result_list.append({
                            "PHARMACY_TRANSACTION_ID": txn_id,
                            "Column Name": col,
                            "Data Type": dtype,
                            "Value": value,
                            "Status": "Failed",
                            "Details": f"Error: Invalid number format in column '{col}'"
                        })
                        column_passed = False
                        all_test_cases_passed = False

                elif dtype.startswith('NUMERIC'):
                    match = re.search(r'\(\d+,\d+\)', dtype)
                    print(match)
                    if match:
                        length, decimal_length = map(int, match.groups())

                        if len(value.split('.')[0]) > length or len(value.split('.')[1]) > decimal_length:
                            validation_result_list.append({
                                "PHARMACY_TRANSACTION_ID": txn_id,
                                "Column Name": col,
                                "Data Type": dtype,
                                "Value": value,
                                "Status": "Failed",
                                "Details": f"Error: Exceeded length limit in column '{col}'"
                            })
                            column_passed = False
                            all_test_cases_passed = False
                        if not re.match(r'^\d+\.\d+$', value):
                            validation_result_list.append({
                                "PHARMACY_TRANSACTION_ID": txn_id,
                                "Column Name": col,
                                "Data Type": dtype,
                                "Value": value,
                                "Status": "Failed",
                                "Value": value,
                                "Details": f"Error: Invalid double format in column '{col}'"
                            })
                            column_passed = False
                            all_test_cases_passed = False
                
                
                elif dtype.startswith('TIMESTAMP'):
                    try:
                        datetime.strptime(value, '%Y%m%d %H:%M:%S')
                    except ValueError:
                        validation_result_list.append({
                            "PHARMACY_TRANSACTION_ID": txn_id,
                            "Column Name": col,
                            "Data Type": dtype,
                            "Value": value,
                            "Status": "Failed",
                            "Value": value,
                            "Details": f"Error: Invalid timestamp format in column '{col}'"
                        })
                        column_passed = False
                        all_test_cases_passed = False

            if column_passed:
                validation_result_list.append({
                    "PHARMACY_TRANSACTION_ID": txn_id,
                    "Column Name": col,
                    "Data Type": dtype,
                    "Value": value,
                    "Status": "Success",
                    "Details": "All values passed validation"
                })

    validation_result_df = pd.DataFrame(validation_result_list, columns=[
                                        "PHARMACY_TRANSACTION_ID", "Column Name", "Data Type", "Status","Value", "Details"])

    if all_test_cases_passed:
        return "All test cases passed successfully", validation_result_df
    else:
        return "Some test cases failed. Please check the output for more details", validation_result_df    