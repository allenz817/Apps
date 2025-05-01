import pandas as pd
import numpy as np
import cv2
import pytesseract
from PIL import Image

def parse_table(table):
    """Parse a detected table into a structured format"""
    # Check for valid table structure
    if not table or 'rows' not in table or not table['rows']:
        return None
    
    rows = table['rows']
    original_image = table.get('original_image')
    
    if not original_image is not None:
        print("Warning: No image provided for text extraction")
        return None
        
    # Extract text from each cell
    data_rows = []
    for row in rows:
        row_data = []
        for cell in row:
            if isinstance(cell, tuple) and len(cell) >= 4:
                # Enhanced cell text extraction
                text = enhanced_cell_text_extraction(cell, original_image)
                row_data.append(text)
        
        if row_data:
            data_rows.append(row_data)
    
    # Determine headers (first row or create generic)
    if data_rows:
        headers = data_rows[0]
        values = data_rows[1:]
    else:
        headers = []
        values = []
    
    return {'headers': headers, 'values': values}

def enhanced_cell_text_extraction(cell, image):
    """Extract text with enhanced preprocessing for better OCR results"""
    x, y, w, h = cell
    
    try:
        # Ensure coordinates are valid
        height, width = image.shape[:2]
        x1, y1 = max(0, x), max(0, y)
        x2, y2 = min(width, x + w), min(height, y + h)
        
        # Skip tiny or invalid cells
        if x2 <= x1 or y2 <= y1 or (x2 - x1) < 5 or (y2 - y1) < 5:
            return ""
        
        # Extract cell region
        cell_region = image[y1:y2, x1:x2]
        
        # Preprocess for better OCR
        # 1. Convert to grayscale
        gray = cv2.cvtColor(cell_region, cv2.COLOR_BGR2GRAY)
        
        # 2. Apply adaptive thresholding
        # This helps with varying lighting conditions
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # 3. Remove noise
        denoised = cv2.medianBlur(binary, 3)
        
        # 4. Increase image size for better OCR
        scaled = cv2.resize(denoised, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        
        # Convert to PIL image for OCR
        pil_image = Image.fromarray(scaled)
        
        # Apply OCR with optimized settings for financial data
        text = pytesseract.image_to_string(
            pil_image,
            config='--psm 6 --oem 3 -c tessedit_char_whitelist="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz,.()$%-+/ "'
        ).strip()
        
        return text if text else ""
        
    except Exception as e:
        print(f"Error extracting cell text: {str(e)}")
        return ""