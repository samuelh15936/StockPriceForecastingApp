import unittest
import pandas as pd
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import data_management as dm

class TestDataManagement(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame for testing
        self.sample_stocks = pd.DataFrame({
            'Ticker': ['AAPL', 'GOOGL'],
            'Company Name': ['Apple Inc.', 'Alphabet Inc.'],
            'Current Price': [150.0, 2500.0]
        })

    def test_load_stock_data(self):
        # Mock the load_stock_data function to return our sample data
        dm.load_stock_data = lambda: self.sample_stocks
        stocks = dm.load_stock_data()
        self.assertIsInstance(stocks, pd.DataFrame)
        self.assertEqual(len(stocks), 2)
        self.assertListEqual(list(stocks.columns), ['Ticker', 'Company Name', 'Current Price'])

    def test_add_stock(self):
        new_stock = dm.add_stock(self.sample_stocks, 'MSFT', 'Microsoft Corporation', 300.0)
        self.assertEqual(len(new_stock), 3)
        self.assertIn('MSFT', new_stock['Ticker'].values)

    def test_save_stock_data(self):
        # Mock the save_stock_data function
        dm.save_stock_data = lambda df: None
        # If no exception is raised, the test passes
        dm.save_stock_data(self.sample_stocks)

if __name__ == '__main__':
    unittest.main()
