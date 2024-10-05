import unittest
import sys
import io
from unittest.mock import patch
import pandas as pd

sys.path.append('..')
import main

class TestMain(unittest.TestCase):

    def setUp(self):
        # Set up any necessary test data or objects
        self.sample_stocks = main.dm.load_stock_data()
        self.sample_predictions = main.pt.load_predictions()

    @patch('builtins.input', side_effect=['1', '', '12', 'Y', ''])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_menu_view_stocks(self, mock_stdout, mock_input):
        main.main(test_mode=True)
        output = mock_stdout.getvalue()
        self.assertIn("Current Stocks", output)
        self.assertIn("Ticker", output)
        self.assertIn("Company Name", output)
        self.assertIn("Current Price", output)

    @patch('main.confirm_action', return_value=True)
    @patch('main.input', side_effect=['AAPL', '0.7', '3'])
    @patch('main.get_valid_input', return_value='3')
    def test_make_prediction(self, mock_get_valid_input, mock_input, mock_confirm_action):
        stocks = pd.DataFrame({'Ticker': ['AAPL'], 'Current Price': [150.0]})
        predictions = pd.DataFrame(columns=['Ticker', 'Prediction', 'Timestamp', 'Timeframe', 'Actual_Outcome', 'Brier_Score'])
        updated_predictions = main.make_prediction(stocks, predictions)
        
        self.assertIn('AAPL', updated_predictions['Ticker'].values)
        self.assertIn(0.7, updated_predictions['Prediction'].values)
        self.assertIn('3 months', updated_predictions['Timeframe'].values)

    @patch('main.pt.load_predictions')
    @patch('builtins.input', side_effect=['6', '', '12', 'Y', ''])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_view_brier_score(self, mock_stdout, mock_input, mock_load_predictions):
        mock_predictions = pd.DataFrame({
            'Ticker': ['AAPL'],
            'Prediction': [0.7],
            'Timestamp': [pd.Timestamp.now()],  # Add this line
            'Timeframe': ['3 months'],  # Add this line
            'Actual_Outcome': [1],
            'Brier_Score': [0.09]
        })
        mock_load_predictions.return_value = mock_predictions
        main.main(test_mode=True)
        output = mock_stdout.getvalue()
        self.assertIn("Overall Brier Score:", output)

    @patch('builtins.input', side_effect=['10', 'AAPL', '', '12', 'Y', ''])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_check_real_time_stock_price(self, mock_stdout, mock_input):
        main.main(test_mode=True)
        output = mock_stdout.getvalue()
        self.assertIn("Real-time data for AAPL:", output)
        self.assertIn("Current Price:", output)
        self.assertIn("Previous Close:", output)

    # Add more test methods as needed

if __name__ == '__main__':
    unittest.main()
