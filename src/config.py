# Configuration settings for the financial statement OCR application

# Input/Output paths
IMAGE_INPUT_PATH = 'resources/sample_images/sample_financial_statement.jpg'
EXCEL_OUTPUT_PATH = 'output/financial_data.xlsx'

# OCR settings
OCR_LANG = 'eng'  # Language for OCR
OCR_CONFIG = '--psm 6'  # Page segmentation mode

# Image preprocessing settings
RESIZE_WIDTH = 1280
THRESHOLD_VALUE = 150