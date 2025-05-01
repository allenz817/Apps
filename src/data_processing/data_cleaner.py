def clean_data(raw_data):
    """
    Clean and process structured data from parsed tables
    
    Args:
        raw_data (list): List of dictionaries with 'headers' and 'values' keys
        
    Returns:
        list: Cleaned structured data
    """
    cleaned_data = []
    
    for table_data in raw_data:
        # Clean headers - strip whitespace and remove empty headers
        if 'headers' in table_data:
            cleaned_headers = [h.strip() if isinstance(h, str) else str(h) for h in table_data['headers']]
            cleaned_headers = [h for h in cleaned_headers if h]  # Remove empty headers
        else:
            cleaned_headers = []
            
        # Clean values - strip whitespace from strings and handle non-string values
        if 'values' in table_data:
            cleaned_values = []
            for row in table_data['values']:
                cleaned_row = []
                for cell in row:
                    if isinstance(cell, str):
                        cleaned_row.append(cell.strip())
                    else:
                        cleaned_row.append(str(cell))
                cleaned_values.append(cleaned_row)
        else:
            cleaned_values = []
            
        # Create cleaned table data
        cleaned_table = {
            'headers': cleaned_headers,
            'values': cleaned_values
        }
        
        cleaned_data.append(cleaned_table)
            
    return cleaned_data