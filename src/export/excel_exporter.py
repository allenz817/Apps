import pandas as pd
import os

def export_to_excel(data, output_file):
    """
    Exports the given structured data to an Excel file.

    Args:
        data: A list of dictionaries or a pandas DataFrame containing the data to export
        output_file (str): Path to the output Excel file
    
    Returns:
        bool: True if export was successful, False otherwise
    """
    try:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Convert data to DataFrame if it's a list of dictionaries
        if isinstance(data, list):
            # Create a multi-sheet Excel file
            with pd.ExcelWriter(output_file) as writer:
                for i, table_dict in enumerate(data):
                    if isinstance(table_dict, dict) and 'headers' in table_dict and 'values' in table_dict:
                        # Handle our specific table format with headers and values
                        headers = table_dict['headers']
                        values = table_dict['values']
                        
                        # Make sure we have headers and values
                        if not headers or not values:
                            print(f"Table {i+1} has empty headers or values, skipping")
                            continue
                            
                        # For each row, ensure it has the same length as headers by padding or truncating
                        padded_values = []
                        for row in values:
                            if len(row) < len(headers):
                                # Pad with empty strings if row is shorter than headers
                                padded_row = row + [''] * (len(headers) - len(row))
                            else:
                                # Truncate if row is longer than headers
                                padded_row = row[:len(headers)]
                            padded_values.append(padded_row)
                        
                        # Create DataFrame with headers as columns
                        df = pd.DataFrame(padded_values, columns=headers)
                        df.to_excel(writer, sheet_name=f'Table_{i+1}', index=False)
                    elif isinstance(table_dict, dict):
                        # Regular dictionary
                        df = pd.DataFrame(table_dict)
                        df.to_excel(writer, sheet_name=f'Table_{i+1}', index=False)
                    else:
                        # Other formats
                        df = pd.DataFrame(table_dict)
                        df.to_excel(writer, sheet_name=f'Table_{i+1}', index=False)
        elif isinstance(data, pd.DataFrame):
            # Data is already a DataFrame
            data.to_excel(output_file, index=False)
        else:
            raise TypeError("Data must be a list of dictionaries, a list of rows, or a pandas DataFrame")
        
        return True
    except Exception as e:
        print(f"Error exporting to Excel: {str(e)}")
        return False