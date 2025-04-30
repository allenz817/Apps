import unittest
from src.ocr.table_detection import detect_tables
from src.image_processing.image_loader import load_image

class TestTableDetection(unittest.TestCase):

    def setUp(self):
        self.image_path = 'resources/sample_images/sample_financial_statement.jpg'
        self.image = load_image(self.image_path)

    def test_table_detection(self):
        tables = detect_tables(self.image)
        self.assertIsInstance(tables, list)
        self.assertGreater(len(tables), 0, "No tables detected in the image.")

    def test_table_structure(self):
        tables = detect_tables(self.image)
        for table in tables:
            self.assertIn('rows', table)
            self.assertIn('columns', table)
            self.assertIsInstance(table['rows'], list)
            self.assertIsInstance(table['columns'], list)

if __name__ == '__main__':
    unittest.main()