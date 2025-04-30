import unittest
from src.ocr.text_recognition import extract_text
from src.image_processing.image_loader import load_image

class TestOCR(unittest.TestCase):

    def setUp(self):
        self.image_path = 'resources/sample_images/sample_financial_statement.jpg'
        self.image = load_image(self.image_path)

    def test_extract_text(self):
        extracted_text = extract_text(self.image)
        self.assertIsInstance(extracted_text, str)
        self.assertGreater(len(extracted_text), 0)

if __name__ == '__main__':
    unittest.main()