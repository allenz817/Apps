def parse_table(detected_table):
    """
    Convert a detected table into a structured format.

    Args:
        detected_table (list of list): A list of rows, where each row is a list of cell values.

    Returns:
        dict: A structured representation of the table, with headers as keys and lists of column values.
    """
    if not detected_table or not isinstance(detected_table, list):
        return {}

    headers = detected_table[0]  # Assuming the first row contains headers
    structured_data = {header: [] for header in headers}

    for row in detected_table[1:]:
        for header, value in zip(headers, row):
            structured_data[header].append(value)

    return structured_data


def convert_to_dataframe(structured_data):
    """
    Convert structured data into a pandas DataFrame.

    Args:
        structured_data (dict): The structured data to convert.

    Returns:
        DataFrame: A pandas DataFrame containing the structured data.
    """
    import pandas as pd

    return pd.DataFrame(structured_data)