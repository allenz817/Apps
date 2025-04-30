import cv2
import numpy as np
from PIL import Image

def detect_table_structure(image):
    import cv2
    import numpy as np

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to get a binary image
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Use morphological operations to detect lines
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(binary, kernel, iterations=2)

    # Find contours of the detected lines
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    table_structure = []

    for contour in contours:
        # Get the bounding box for each contour
        x, y, w, h = cv2.boundingRect(contour)
        table_structure.append((x, y, w, h))

    return table_structure

def extract_tables_from_image(image_path):
    import cv2

    # Load the image
    image = cv2.imread(image_path)

    # Detect table structures
    table_structure = detect_table_structure(image)

    return table_structure

def detect_tables(image):
    """
    Detect tables in an image and structure them into rows and columns.
    
    Args:
        image (PIL.Image): The input image
        
    Returns:
        list: A list of detected tables, each as a dictionary with 'rows' and 'columns'
    """
    # Convert PIL Image to OpenCV format if necessary
    if isinstance(image, Image.Image):
        import numpy as np
        opencv_image = np.array(image.convert('RGB'))
        opencv_image = opencv_image[:, :, ::-1].copy()  # RGB to BGR
    else:
        opencv_image = image
    
    # Get the table structure
    table_cells = detect_table_structure(opencv_image)
    
    # Group cells into tables
    tables = []
    if table_cells:
        # Sort cells by y-coordinate
        sorted_cells = sorted(table_cells, key=lambda cell: cell[1])
        
        # Basic heuristic to identify row boundaries
        rows = []
        current_row = [sorted_cells[0]]
        current_y = sorted_cells[0][1]
        
        for cell in sorted_cells[1:]:
            # If cell is close to the current row's y-coordinate, add to current row
            if abs(cell[1] - current_y) < 20:  # Threshold for considering cells in the same row
                current_row.append(cell)
            else:
                # Otherwise, start a new row
                rows.append(current_row)
                current_row = [cell]
                current_y = cell[1]
        
        # Add the last row
        if current_row:
            rows.append(current_row)
        
        # Now find columns by sorting cells in each row by x-coordinate
        structured_rows = []
        for row in rows:
            sorted_row = sorted(row, key=lambda cell: cell[0])
            structured_rows.append(sorted_row)
        
        # Create a table dictionary
        table = {
            'rows': structured_rows,
            'columns': []  # To be computed in a more sophisticated implementation
        }
        
        tables.append(table)
    
    return tables