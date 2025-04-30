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
            if all(isinstance(item, dict) for item in data):
                # Multiple tables case - create a multi-sheet Excel file
                with pd.ExcelWriter(output_file) as writer:
                    for i, table_dict in enumerate(data):
                        df = pd.DataFrame(table_dict)
                        df.to_excel(writer, sheet_name=f'Table_{i+1}', index=False)
            else:
                # Single table as list of rows
                df = pd.DataFrame(data)
                df.to_excel(output_file, index=False)
        elif isinstance(data, pd.DataFrame):
            # Data is already a DataFrame
            data.to_excel(output_file, index=False)
        else:
            raise TypeError("Data must be a list of dictionaries, a list of rows, or a pandas DataFrame")
        
        return True
    except Exception as e:
        print(f"Error exporting to Excel: {str(e)}")
        return False