import unittest
import os
import pandas as pd
import tempfile
from src.export.excel_exporter import export_to_excel

class TestExcelExport(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for test output
        self.test_dir = tempfile.mkdtemp()
        self.output_file = os.path.join(self.test_dir, 'test_export.xlsx')
        
        # Sample data for testing
        self.sample_data = [
            {'Company': 'ABC Corp', 'Revenue': 1000000, 'Expenses': 750000, 'Profit': 250000},
            {'Company': 'XYZ Inc', 'Revenue': 2000000, 'Expenses': 1500000, 'Profit': 500000},
            {'Company': 'DEF Ltd', 'Revenue': 1500000, 'Expenses': 1200000, 'Profit': 300000},
        ]

    def test_export_list_of_dicts(self):
        # Test exporting a list of dictionaries
        result = export_to_excel(self.sample_data, self.output_file)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.output_file))
        
        # Verify the data was exported correctly
        df = pd.read_excel(self.output_file)
        self.assertEqual(len(df), len(self.sample_data))
        self.assertListEqual(list(df.columns), ['Company', 'Revenue', 'Expenses', 'Profit'])
    
    def test_export_dataframe(self):
        # Test exporting a pandas DataFrame
        df = pd.DataFrame(self.sample_data)
        result = export_to_excel(df, self.output_file)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.output_file))
        
        # Verify the data was exported correctly
        df_read = pd.read_excel(self.output_file)
        self.assertEqual(len(df_read), len(df))
        self.assertListEqual(list(df_read.columns), list(df.columns))
    
    def test_export_empty_data(self):
        # Test exporting empty data
        result = export_to_excel([], self.output_file)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.output_file))
        
        # Verify an empty sheet was created
        df = pd.read_excel(self.output_file)
        self.assertEqual(len(df), 0)
    
    def tearDown(self):
        # Clean up test files
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        os.rmdir(self.test_dir)

if __name__ == '__main__':
    unittest.main()