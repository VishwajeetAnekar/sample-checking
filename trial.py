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
                            'Is it repeated': 'Yes', 
                            'Details': f'Transaction ID {transaction_id} is repeated in both files'})

    for transaction_id in df1["PHARMACY_TRANSACTION_ID"]:
        if transaction_id not in common_ids:
            result_rows.append({'Column Name': 'PHARMACY_TRANSACTION_ID', 
                                'Status': 'Success', 
                                'Repeated Value': transaction_id, 
                                'Is it repeated': 'No', 
                                'Details': f'Transaction ID {transaction_id} is unique to File 1'})
            
    for transaction_id in df2["PHARMACY_TRANSACTION_ID"]:
        if transaction_id not in common_ids:
            result_rows.append({'Column Name': 'PHARMACY_TRANSACTION_ID', 
                                'Status': 'Success', 
                                'Repeated Value': transaction_id, 
                                'Is it repeated': 'No', 
                                'Details': f'Transaction ID {transaction_id} is unique to File 2'})

    result_df = pd.DataFrame(result_rows)

    return result_df, "Error: Common values found"


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
