import unittest
import sys
import pandas as pd
import matplotlib.pyplot as plt
from unittest.mock import patch

sys.path.append('..')
import visualizations as vis

class TestVisualizations(unittest.TestCase):

    def setUp(self):
        # Create sample data for testing
        self.sample_stocks = pd.DataFrame({
            'Ticker': ['AAPL', 'GOOGL', 'MSFT'],
            'Company Name': ['Apple Inc.', 'Alphabet Inc.', 'Microsoft Corporation'],
            'Current Price': [150.0, 2500.0, 300.0]
        })
        
        self.sample_predictions = pd.DataFrame({
            'Ticker': ['AAPL', 'GOOGL', 'MSFT'],
            'Prediction': [0.7, 0.6, 0.8],
            'Actual_Outcome': [1, 0, 1],
            'Brier_Score': [0.09, 0.36, 0.04]
        })

    @patch('matplotlib.pyplot.show')
    def test_plot_stock_prices(self, mock_show):
        vis.plot_stock_prices(self.sample_stocks)
        self.assertTrue(mock_show.called)

    @patch('matplotlib.pyplot.show')
    def test_plot_prediction_accuracy(self, mock_show):
        vis.plot_prediction_accuracy(self.sample_predictions)
        self.assertTrue(mock_show.called)

    def test_create_bar_chart(self):
        fig, ax = plt.subplots()
        vis.create_bar_chart(ax, ['A', 'B', 'C'], [1, 2, 3], 'Test Chart')
        self.assertEqual(ax.get_title(), 'Test Chart')
        self.assertEqual(len(ax.patches), 3)

    # Add more test methods as needed

if __name__ == '__main__':
    unittest.main()
