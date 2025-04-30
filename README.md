# Financial Statement OCR Application

This project is designed to recognize text and tables in images of financial statements and convert them into a structured table format that can be exported to Excel. 

## Features

- Image processing to enhance and prepare images for OCR.
- Optical Character Recognition (OCR) to extract text from images.
- Detection of table structures within the images.
- Conversion of detected tables into structured data formats.
- Cleaning and formatting of extracted data for accuracy.
- Exporting the structured data to Excel format.

## Project Structure

```
financial-statement-ocr
├── src
│   ├── main.py                 # Application entry point
│   ├── config.py               # Configuration settings
│   ├── image_processing
│   │   ├── __init__.py
│   │   ├── preprocessing.py    # Image enhancement and preparation
│   │   └── image_loader.py     # Image loading and handling
│   ├── ocr
│   │   ├── __init__.py
│   │   ├── text_recognition.py # OCR text extraction
│   │   └── table_detection.py  # Table structure detection
│   ├── data_processing
│   │   ├── __init__.py
│   │   ├── table_parser.py     # Convert detected tables to structured data
│   │   └── data_cleaner.py     # Clean and format extracted data
│   └── export
│       ├── __init__.py
│       └── excel_exporter.py   # Export data to Excel format
├── tests
│   ├── __init__.py
│   ├── test_ocr.py
│   ├── test_table_detection.py
│   └── test_excel_export.py
├── resources
│   └── sample_images          # Sample financial statements for testing
├── requirements.txt           # Dependencies
├── setup.py                   # Package installation script
├── .gitignore
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd financial-statement-ocr
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py <path_to_image>
```

Replace `<path_to_image>` with the path to the financial statement image you want to process.

## Testing

To run the tests, use:
```
pytest tests/
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.