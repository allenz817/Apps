import cv2
import numpy as np
from PIL import Image
import pytesseract
from collections import defaultdict

def detect_tables(image):
    """
    Enhanced table detection that captures full table structure including all columns
    
    Args:
        image (PIL.Image): The input image
        
    Returns:
        list: A list of detected tables
    """
    # Convert PIL Image to OpenCV format if necessary
    if isinstance(image, Image.Image):
        opencv_image = np.array(image.convert('RGB'))
        opencv_image = opencv_image[:, :, ::-1].copy()  # RGB to BGR
    else:
        opencv_image = image
    
    # Use enhanced detection to capture the complete table grid
    # Detect horizontal and vertical lines for better grid structure
    gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding to handle varying lighting conditions
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 10
    )
    
    # Create separate kernels for horizontal and vertical lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
    
    # Detect horizontal and vertical lines
    horizontal_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    vertical_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    
    # Combine horizontal and vertical lines to create a grid
    table_grid = cv2.bitwise_or(horizontal_lines, vertical_lines)
    
    # Detect grid structure - find contours of cells
    contours, _ = cv2.findContours(table_grid, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours by size to find actual cells
    min_cell_area = 100  # Minimum area to be considered a cell
    cells = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w * h > min_cell_area:
            cells.append((x, y, w, h))
    
    # Sort cells by y-coordinate first, then x-coordinate to organize into rows and columns
    sorted_cells = sorted(cells, key=lambda cell: (cell[1], cell[0]))
    
    # Group cells into rows based on y-coordinate
    rows = []
    current_row = []
    current_y = None
    y_tolerance = 15  # Pixels of tolerance for row grouping
    
    for cell in sorted_cells:
        x, y, w, h = cell
        
        if current_y is None:
            current_y = y
            current_row.append(cell)
        elif abs(y - current_y) <= y_tolerance:
            current_row.append(cell)
        else:
            # Sort cells in the current row by x-coordinate
            current_row = sorted(current_row, key=lambda c: c[0])
            rows.append(current_row)
            current_row = [cell]
            current_y = y
    
    # Add the last row
    if current_row:
        current_row = sorted(current_row, key=lambda c: c[0])
        rows.append(current_row)
    
    # If no cells detected through line detection, try text-based approach
    if not rows:
        text_table = detect_table_from_text(image)
        if text_table:
            return [{'rows': text_table, 'original_image': opencv_image}]
        return []
    
    # Return the detected table with the original image for text extraction
    return [{'rows': rows, 'original_image': opencv_image}]

# Add helper functions for text-based detection
def detect_table_from_text(image):
    """Detect table structure based on text alignment when no grid lines are visible"""
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    
    # Group words by line (y-coordinate)
    lines = defaultdict(list)
    for i in range(len(data['text'])):
        if data['text'][i].strip():
            y = data['top'][i]
            lines[y].append({
                'text': data['text'][i],
                'x': data['left'][i],
                'y': data['top'][i],
                'w': data['width'][i],
                'h': data['height'][i]
            })
    
    # Format lines into rows of cells
    rows = []
    for y in sorted(lines.keys()):
        # Sort words in line by x-coordinate
        line = sorted(lines[y], key=lambda word: word['x'])
        
        # Create cell-like structures from words
        row = [(word['x'], word['y'], word['w'], word['h']) for word in line]
        rows.append(row)
    
    return rows