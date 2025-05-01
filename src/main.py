import argparse
import os
from image_processing.image_loader import load_image
from image_processing.preprocessing import enhance_image
from ocr.text_recognition import extract_text
from ocr.table_detection import detect_tables
from data_processing.table_parser import parse_table
from data_processing.data_cleaner import clean_data
from export.excel_exporter import export_to_excel
import config

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Financial Statement OCR')
    parser.add_argument('--image', type=str, help='Path to financial statement image',
                       default=config.IMAGE_INPUT_PATH)
    parser.add_argument('--output', type=str, help='Path to output Excel file',
                       default=config.EXCEL_OUTPUT_PATH)
    args = parser.parse_args()
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    print(f"Processing image: {args.image}")
    
    # Load and process the image
    image = load_image(args.image)
    processed_image = enhance_image(image) if image else image
    
    # Extract text
    print("Extracting text...")
    extracted_text = extract_text(image)
    print(f"Extracted {len(extracted_text)} characters of text")
    
    # Detect tables
    print("Detecting tables...")
    tables = detect_tables(image)
    print(f"Detected {len(tables)} tables")
    
    # Process and clean the data
    structured_data = []
    for table in tables:
        parsed_table = parse_table(table)
        if parsed_table:
            structured_data.append(parsed_table)
    
    # Clean the data
    cleaned_data = clean_data(structured_data) if structured_data else []
    
    # Export to Excel
    if cleaned_data:
        print(f"Exporting to Excel: {args.output}")
        export_to_excel(cleaned_data, args.output)
        print("Export complete!")
    else:
        print("No tables found to export")

if __name__ == "__main__":
    main()